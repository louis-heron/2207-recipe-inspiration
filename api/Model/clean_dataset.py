"""
This class allows you to clean up the data.
Recipes with too few ingredients are removed.
Recipes without a valid list of steps are removed.
Ingredients that are too specific are filtered out based on ingredient redundancy.
"""

import logging
import re
from collections import Counter
import pandas as pd
from script.Enums import brands, incorrect_ingredients, dropped_ing, minimum
from script.clean_ingredients import CleanIng

class Clean():
    """
    Class for cleaning recipe data.

    Removes recipes with too few ingredients.
    Removes recipes without valid steps list.
    Filters out overly specific ingredients based on redundancy.
    """

    logger = logging.getLogger(__name__)

    # class attribute
    URL_PATTERN = r'http\S+|www\.\S+'
    MIN_FREQUENCY = minimum.MIN_FREQUENCY

    DROPPED_INGREDIENTS = dropped_ing.DROPPED_INGREDIENTS
    MIN_INGREDIENTS = minimum.MIN_INGREDIENT
    MIN_CHAR = minimum.MIN_CHARACTER
    KNOWN_BRANDS = brands.KNOWN_BRANDS
    NON_FOOD = incorrect_ingredients.INCORRECT_INGREDIENTS

    # Constructor
    def __init__(self, file_path: str, parquet_path: str ='ingredients.parquet'):
        """
        Initialize Clean instance.
        """
        self.file_path = file_path

        #Call the Parquet file
        valid_df = pd.read_parquet(parquet_path)
        self.valid_set = set(valid_df['ingredient_name'])

        #Call the clean_ingredients functions
        df = pd.read_csv(self.file_path)
        self.data = CleanIng.process_dataframe(df, col_raw='NER', col_clean='NER_clean')

    def clean_text_field(self, text, url_pat):
        """Removes URLs and cleans whitespace from strings."""
        if not isinstance(text, str):
            return ""
        return re.sub(url_pat, '', text).strip()

    def clean_dataset(self, col_title, col_ingredients, col_directions):
        #Clean essential columns
        for col in [col_title, col_ingredients, col_directions]:
            self.data[col] = self.data[col].apply(lambda x: self.clean_text_field(x, self.URL_PATTERN))

        # Remove rows with missing essential data or too few ingredients
        self.data = self.data.dropna(subset=[col_title, col_ingredients, col_directions])

        #Filter ingredients agains parquet file & remove them
        self.data['NER_clean'] = self.data['NER_clean'].apply(
            lambda ing_list: [ing for ing in ing_list if ing in self.valid_set]
            if isinstance(ing_list, list) else []
        )
        self.data = self.data.dropna(subset='NER_clean')

        # Ensure we have at least 3 ingredients left after cleaning against parquet
        self.data = self.data[self.data['NER_clean'].map(len) > self.MIN_INGREDIENTS]

        return self.data
