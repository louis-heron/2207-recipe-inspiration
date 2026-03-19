"""
This class allows you to clean up the data.
Recipes with too few ingredients are removed.
Recipes without a valid list of steps are removed.
Ingredients that are too specific are filtered out based on ingredient redundancy.
"""

import ast
import logging
import re
from collections import Counter
from typing import List, Set
import pandas as pd

from script.Enums import brands, incorrect_ingredients, dropped_ing, minimum

class CleanIng():
    """
    Class for cleaning recipe data.

    Removes recipes with too few ingredients.
    Removes recipes without valid steps list.
    Filters out overly specific ingredients based on redundancy.
    """

    # class attribute
    DROPPED_INGREDIENTS = dropped_ing.DROPPED_INGREDIENTS
    MIN_INGREDIENTS = minimum.MIN_INGREDIENT
    MIN_CHAR = minimum.MIN_CHARACTER
    KNOWN_BRANDS = brands.KNOWN_BRANDS
    NON_FOOD = incorrect_ingredients.INCORRECT_INGREDIENTS

    logger = logging.getLogger(__name__)

    def __init__(self):
        """
        Initialize CleanIng instance.
        No specific initialization required.
        """

    def _is_valid_text(self, text: str) -> bool:
        """Internal helper to validate if a string looks like a real ingredient."""
        if len(text) <= self.MIN_CHAR or text in self.KNOWN_BRANDS or text in self.NON_FOOD:
            return False
        # Reject strings ending in connectors or starting/ending with hyphens
        if re.search(r'\b(de|of|with|and|or|a|the|in|for)$', text) or text.startswith("-") or text.endswith("-"):
            return False
        return True


    def clean_single_ingredient(self, ing: str) -> str:
        """Normalizes text and filters out brands/non-food."""
        if not isinstance(ing, str):
            return ""

        # 1. Lowercase and basic cleaning
        ing = ing.lower().strip()
        ing = re.sub(r"[^a-z\s\-]", "", ing)

        # 2. Remove prefixes at the START
        prefix_pattern = r"^(a|an|all-purpose|freshly|grated|american|-|additional|zest|one|chopped|pinch|of|diced|sliced|the|some|c)\s+"
        ing = re.sub(prefix_pattern, "", ing).strip()

        # 3. Remove suffixes at the END (The specific change you wanted)
        ing = re.sub(r"\s+(sliced|chopped|diced)$", "", ing).strip()

        # 4. Check against your Enum lists
        # If it's a brand or non-food, we return an EMPTY string
        if ing in self.DROPPED_INGREDIENTS or \
           ing in self.KNOWN_BRANDS or \
           ing in self.NON_FOOD:
            return ""

        return ing

    def filter_redundant(self, ing_list: List[str]) -> List[str]:
        """Removes 'rice' if 'basmati rice' is present."""
        # quid in case of brown sugar and other-type-of sugar?
        unique_ings = sorted(list(set(ing_list)), key=len, reverse=True)
        kept = []
        for current in unique_ings:
            # If current ingredient isn't a subset of something already kept, keep it
            if not any(set(current.split()).issubset(set(k.split())) for k in kept):
                kept.append(current)
        return kept

    def process_dataframe(self, df: pd.DataFrame, col_raw: str, col_clean: str) -> pd.DataFrame:
        """The main pipeline to clean the entire dataframe."""

        def clean_pipeline(raw_value):
            # 1. Parse string representation of list
            try:
                items = ast.literal_eval(raw_value) if isinstance(raw_value, str) else raw_value
                if not isinstance(items, list): return []
            except (ValueError, SyntaxError):
                self.logger.warning("Failed to parse row: %s", raw_value)
                return [""]

            # 2. Clean and Validate
            cleaned = []
            for i in items:
                name = self.clean_single_ingredient(i)
                if name and name not in self.DROPPED_INGREDIENTS and self._is_valid_text(name):
                    cleaned.append(name)

            # 3. Remove subsets (e.g., keep 'brown rice', drop 'rice')
            return self.filter_redundant(cleaned)

        # Apply the pipeline
        df[col_clean] = df[col_raw].apply(clean_pipeline)

        # 4. Global Filters: Remove recipes with too few ingredients and drop duplicates
        df = df[df[col_clean].map(len) >= self.MIN_INGREDIENTS]

        # Deduplicate based on the content of the ingredients
        df['temp_hash'] = df[col_clean].apply(lambda x: tuple(sorted(x)))
        df = df.drop_duplicates('temp_hash').drop(columns=['temp_hash'])

        return df.reset_index(drop=True)
