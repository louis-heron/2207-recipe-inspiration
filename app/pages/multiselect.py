import streamlit as st
import pandas as pd
from pathlib import Path

PARQUET_PATH = Path(__file__).parent.parent.parent / "ingredients.parquet"

class IngredientSelector:
    """
    Manages the logic for the Streamlit multiselect widget
    using a pre-processed parquet file for speed.
    """
    def __init__(self, file_path=str(PARQUET_PATH)):
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

        if "ing_selector_gen" not in st.session_state:
            st.session_state.ing_selector_gen = 0

        widget_key = f"ing_selector_{st.session_state.ing_selector_gen}"

        # Pre-populate with detected ingredients on first render of this generation
        if widget_key not in st.session_state:
            pre = st.session_state.get("ing_detected", [])
            if pre:
                st.session_state[widget_key] = pre

        # Ensure any selected ingredients are present in options
        selected = st.session_state.get(widget_key, [])
        extra = [item for item in selected if item not in self.options]
        options = extra + self.options if extra else self.options

        if st.button("Clear All Selection"):
            st.session_state.ing_selector_gen += 1
            st.session_state.pop("ing_detected", None)
            st.rerun()

        selection = st.multiselect(
            label=label,
            options=options,
            placeholder=placeholder,
            key=widget_key,
            help=f"Searching through {len(options)} ingredients."
        )

        return selection

    def format_for_model(self, selection):
        """Formats selection for the AI model."""
        return " ".join(selection).lower()
