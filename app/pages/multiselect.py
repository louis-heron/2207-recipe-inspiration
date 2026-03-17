import streamlit as st
import pandas as pd

class IngredientSelector:
    """
    Manages the logic for the Streamlit multiselect widget
    using a pre-processed parquet file for speed.
    """
    def __init__(self, file_path='ingredients.parquet'):
        self.file_path = file_path
        self.options = []

    @st.cache_data
    def load_options(_self):
        """Loads pre-filtered ingredients from the parquet file."""
        try:
            df = pd.read_parquet(_self.file_path)
            return df['ingredient_name'].tolist()
        except FileNotFoundError:
            st.error(f"File not found: {_self.file_path}")
            return []

    def render(self, label="Which ingredients do you have?", placeholder="Type 'r' for rice..."):
        """Displays the multiselect widget and a clear button."""
        if not self.options:
            self.options = self.load_options()

        # Layout: Multiselect takes most space, Button sits next to it or below
        # Using a unique key 'ing_selector' to control the state
        selection = st.multiselect(
            label=label,
            options=self.options,
            placeholder=placeholder,
            key="ing_selector",
            help=f"Searching through {len(self.options)} ingredients."
        )

        if st.button("Clear All Selection"):
            st.session_state.ing_selector = []
            st.rerun()

        return selection

    def format_for_model(self, selection):
        """Formats selection for the AI model."""
        return " ".join(selection).lower()
