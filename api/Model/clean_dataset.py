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

from Enums import brands, incorrect_ingredients, dropped_ing

class Clean():
    """
    Class for cleaning recipe data.

    Removes recipes with too few ingredients.
    Removes recipes without valid steps list.
    Filters out overly specific ingredients based on redundancy.
    """

    logger = logging.getLogger(__name__)

    # class attribute
    DROPPED_INGREDIENTS = dropped_ing.DROPPED_INGREDIENTS
    URL_PATTERN = r'http\S+|www\.\S+'
    MIN_INGREDIENTS = 3

    MIN_CHAR = 2
    KNOWN_BRANDS = brands.KNOWN_BRANDS
    NON_FOOD = incorrect_ingredients.INCORRECT_INGREDIENTS
    DEFAULT_MIN_FREQUENCY = 200

    # Constructor
    def __init__(self):
        """
        Initialize Clean instance.

        No specific initialization required.
        """

    def filter_redundant_ingredients(self, ing_list):
        """
        Advanced filter: If 'basmati rice' words are entirely contained
        within 'basmati brown rice', the shorter one is removed.
        """
        # Remove exact duplicates and sort by length (longest first)
        unique_set = list(set(ing_list))
        sorted_ings = sorted(unique_set, key=len, reverse=True)

        kept_ings = []
        for current_ing in sorted_ings:
            current_tokens = set(current_ing.split())

            is_redundant = False
            for kept_ing in kept_ings:
                kept_tokens = set(kept_ing.split())
                # Check if all words of current item exist in a longer item already kept
                if current_tokens.issubset(kept_tokens):
                    is_redundant = True
                    break

            if not is_redundant:
                kept_ings.append(current_ing)

        return kept_ings

    def clean_text_field(self, text, url_pat):
        """Removes URLs and cleans whitespace from strings."""
        if not isinstance(text, str):
            return ""
        return re.sub(url_pat, '', text).strip()

    def clean_dataset(self, data, col_raw, col_clean, col_title, col_ingredients, col_directions ):

        # Convert string-lists to Python lists
        data[col_clean] = data[col_raw].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

        # Clean ingredients: lowercase, remove URLs, remove common items
        data[col_clean] = data[col_clean].apply(lambda x: [
            self.clean_text_field(ing, self.URL_PATTERN).strip().lower()
            for ing in x if ing.lower() not in self.DROPPED_INGREDIENTS
        ])

        # Apply the smart Token-Subset filter
        data[col_clean] = data[col_clean].apply(self.filter_redundant_ingredients)

        for col in [col_title, col_ingredients, col_directions]:
            data[col] = data[col].apply(lambda x: self.clean_text_field(x, self.URL_PATTERN))

        # Remove rows with missing essential data or too few ingredients
        data = data.dropna(subset=[col_title, col_ingredients, col_directions])
        data = data[(data[col_title] != "") & (data[col_clean].map(len) > self.MIN_INGREDIENTS)]

        # Drop duplicate recipes (exact same ingredient set)
        data['temp_key'] = data[col_clean].apply(lambda x: tuple(sorted(x)))
        data = data.drop_duplicates(subset=['temp_key']).drop(columns=['temp_key'])

        data = data.reset_index(drop=True)
        return data

    def parse_row(self, row: str) -> List[str]:
        """
        Parse a data column into Python list using ast.literal_eval.

        Parameters
        ----------
        row : str
            String representing a Python list (ex: "['ingredient1', 'ingredient2']").

        Returns
        -------
        list
            Parsed list of ingredients/steps, or empty list if parsing fails.

        Raises
        ------
        ValueError, SyntaxError
            Handled silently, returns [].
        """
        try:
            return ast.literal_eval(row)
        except (ValueError, SyntaxError):
            self.logger.warning("Failed to parse row: %s", row)
            return [""]

    def clean_ingredient(self, ingredient: str | None) -> str | None:
        """
        Normalize and clean a single ingredient string.

        Removes articles, special chars, normalizes case, filters short/noisy terms.

        Parameters
        ----------
        ingredient : str | None
            Raw ingredient string from recipe dataset

        Returns
        -------
        str | None
            Cleaned lowercase ingredient without articles/special chars,
            or None if empty/short/invalid
        """
        if not ingredient or pd.isna(ingredient):
            return None
        cleaned = ingredient.strip().lower()
        cleaned = re.sub(r"[^a-z\s\-]", "", cleaned)
        cleaned = re.sub(r"^(a|an|the|some)\s+", "", cleaned).strip()
        if len(cleaned) <= self.MIN_CHAR:
            return None
        return cleaned

    def is_valid(self, ing: str) -> bool:
        """
        Validate if a cleaned ingredient represents real food (not brand/noise).

        Filters known brands, stop words, malformed strings.

        Parameters
        ----------
        ing : str
            Cleaned ingredient from clean_ingredient()

        Returns
        -------
        bool
            True if valid food ingredient, False if brand/stopword/malformed
        """
        if ing in self.KNOWN_BRANDS or ing in self.NON_FOOD:
            return False
        if re.search(r'\b(de|of|with|and|or|a|the|in|for)$', ing):
            return False
        if ing.startswith("-") or ing.endswith("-"):
            return False
        return True

    def extract_valid_ingredients(self, row: str, min_frequency: int = DEFAULT_MIN_FREQUENCY) -> Set[str]:
        """
        Extract, clean, and validate ingredients from row, keeping frequent ones.

        Parameters
        ----------
        row : List[str]
            List of ingredients from dataset (comma-separated tags)
        min_frequency : int
            Minimum occurrences to keep ingredient

        Returns
        -------
        Set[str]
            Valid, cleaned ingredients appearing >= min_frequency times
        """
        ingredient_counter: Counter[str] = Counter()

        for ingredients in self.parse_row(row):
            cleaned = self.clean_ingredient(ingredients)
            if cleaned:
                ingredient_counter[cleaned] += 1

        valid_ingredients = {
            ing for ing, count in ingredient_counter.items()
            if count >= min_frequency and self.is_valid(ing)
        }

        return valid_ingredients

    def get_clean_ingredients(self, row: List[str], valid_ingredients: Set[str]) -> List[str]:
        """
        Extract clean ingredients from NER row list, keeping only valid ones.

        Parameters
        ----------
        ner_row : List[str]
            List of raw ingredients from NER row (already parsed)
        valid_ingredients : Set[str]
            Precomputed set of valid ingredients

        Returns
        -------
        List[str]
            List of cleaned ingredients present in valid_ingredients
        """
        return [
            cleaned_ing
            for ingredients in row
            if (cleaned_ing := self.clean_ingredient(ingredients))
            and cleaned_ing in valid_ingredients
        ]
