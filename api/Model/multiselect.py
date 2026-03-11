import streamlit as st
import pandas as pd

class IngredientSelector:
    """
    Manages the logic for the Streamlit multiselect widget
    using a pre-processed parquet file for speed.
    """
    def __init__(self, file_path='filtered_ingredients.parquet'):
        self.file_path = file_path
        self.options = []

    @st.cache_data
    def load_options(_self):
        """Loads the pre-filtered ingredients from the parquet file."""
        df = pd.read_parquet(_self.file_path)
        return df['ingredient_name'].tolist()

    def render(self, label="Which ingredients do you have?", placeholder="Type 'r' for rice..."):
        if not self.options:
            self.options = self.load_options()

        selection = st.multiselect(
            label=label,
            options=self.options,
            placeholder=placeholder,
            help=f"Searching through {len(self.options)} common ingredients."
        )
        return selection

    def format_for_model(self, selection):
        return " ".join(selection).lower()

# Usage in app.py
selector = IngredientSelector()
user_input = selector.render()

if user_input:
    formatted_input = selector.format_for_model(user_input)
    st.info(f"Ready for Vectorizer: {formatted_input}")
