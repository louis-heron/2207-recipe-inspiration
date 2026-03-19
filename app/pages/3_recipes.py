import streamlit as st

from components.recipes import recipes_section

if "recipes" not in st.session_state:
    st.info("No recipes yet. Go to the **Inspiration** page to detect ingredients and get recommendations!")
    st.stop()

recipes_section(
    recipes=st.session_state["recipes"],
    ingredients_used=st.session_state.get("ingredients_used", []),
)
