
import pandas as pd
import numpy as np
import ast
import re

from Enums import dropped_ing

class Clean():

    # class attribute
    DROPPED_INGREDIENTS = dropped_ing.DROPPED_INGREDIENTS
    URL_PATTERN = r'http\S+|www\.\S+'
    MIN_INGREDIENTS = 3

    # Constructor
    def __init__(self):
        pass

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
