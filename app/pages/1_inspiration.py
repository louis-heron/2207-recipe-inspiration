import base64

import requests
import streamlit as st

from components.file_uploader import accessible_file_uploader
from components.ingredient_selector import ingredient_selector, load_ingredient_options
from components.recipe_controls import recipe_controls

API_URL = st.secrets["API_URL"]

st.title("AI Recipe Recommender")

st.markdown("""
<style>
[data-testid="stHorizontalBlock"] {
    align-items: flex-start !important;
}
h1::before {
    content: "🍳";
    speak: never;
    margin-right: 0.3em;
}
</style>
""", unsafe_allow_html=True)

# ── Part 1 ────────────────────────────────────────────────────────────────────
st.header("1. Upload Image")

file_info, detect_clicked = accessible_file_uploader(key="fridge-photo")

if file_info and detect_clicked:
    file_bytes = base64.b64decode(file_info["data"])
    files = {"file": (file_info["name"], file_bytes, file_info["type"])}
    response = requests.post(f"{API_URL}/detect-ingredients", files=files)

    if response.status_code == 200:
        detected = [ing.lower() for ing in response.json()["detected_ingredients"]]
        st.session_state["ing_selected"] = detected
        st.session_state["ing_version"] = st.session_state.get("ing_version", 0) + 1
    else:
        st.error("Detection failed.")

st.divider()

# ── Part 2 ────────────────────────────────────────────────────────────────────
st.header("2. Confirm & Cook")

col_select, col_controls = st.columns([2, 1], vertical_alignment="top")

options = load_ingredient_options()
current = st.session_state.get("ing_selected", [])

with col_select:
    selected_ingredients = ingredient_selector(
        options=options,
        selected=current,
        version=st.session_state.get("ing_version", 0),
        label="We found these! Add or remove as needed:",
        placeholder="Search for more ingredients...",
        key="ing_selector",
    )
    st.session_state["ing_selected"] = selected_ingredients

with col_controls:
    num_res, get_recipes_clicked = recipe_controls(key="recipe-controls")

if get_recipes_clicked:
    payload = {"ingredients": selected_ingredients, "num_recipes": num_res}
    res = requests.post(f"{API_URL}/predict", json=payload)

    if res.status_code == 200:
        st.session_state["recipes"] = res.json()["recipes"]
        st.session_state["ingredients_used"] = selected_ingredients
        st.switch_page("pages/3_recipes.py")
    else:
        st.error("Recommendation failed.")
