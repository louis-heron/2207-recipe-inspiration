import streamlit as st
from collections import Counter

class IngredientSelector:
    """
    Manages the logic for the Streamlit multiselect widget,
    including frequency filtering and input formatting.
    """
    def __init__(self, data, column_name):
        self.data = data
        self.column_name = column_name
        self.options = []

    @st.cache_data
    def get_filtered_options(_self, min_occurrence=100):
        """
        Extracts unique ingredients from the column and filters by
        popularity to ensure the UX remains fast (Real-time speed)
        the _self seems to be quite useful for that
        """
        # Flatten all lists in the column into one master list
        all_ingredients = [
            ing for sublist in _self.data[_self.column_name]
            for ing in sublist
        ]

        # Count occurrences
        counts = Counter(all_ingredients)

        # Filter: Only keep ingredients that appear frequently enough
        # This prevents the 'r' search from lagging with 1.7M rows
        _self.options = sorted([
            ing for ing, count in counts.items()
            if count >= min_occurrence
        ])

        return _self.options

    def render(self, label="Which ingredients would you use for today's cooking?", placeholder="Type 'r' for rice..."):
        """
        Renders the multiselect widget and returns the selected list.
        """
        if not self.options:
            self.get_filtered_options()

        selection = st.multiselect(
            label=label,
            options=self.options,
            placeholder=placeholder,
            help=f"Searching through {len(self.options)} ingredients."
        )
        return selection

    def format_for_model(self, selection):
        """
        Converts the list selection into a space-separated string
        ready for the TfidataVectorizer.
        """
        return " ".join(selection).lower()
