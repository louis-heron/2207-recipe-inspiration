import streamlit as st
import requests
from PIL import Image

st.set_page_config(page_title="AI Recipe Chef", layout="wide")
st.title("🍳 AI Recipe Recommender")

# Setup layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. Upload Image")
    uploaded_file = st.file_uploader("Snap a photo of your fridge...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Your Ingredients", use_container_width=True)

        if st.button("🔍 Detect Ingredients"):
            # Call the Detection API
            files = {"file": uploaded_file.getvalue()}
            response = requests.post("http://localhost:8000/detect-ingredients", files=files)

            if response.status_code == 200:
                st.session_state.detected = response.json()["detected_ingredients"]
            else:
                st.error("Detection failed.")

with col2:
    st.header("2. Confirm & Cook")

    # If ingredients are detected, show them in a multi-select box so user can edit
    if "detected" in st.session_state:
        selected_ingredients = st.multiselect(
            "We found these! Add or remove as needed:",
            options=st.session_state.detected + ["salt", "pepper", "oil"], # Add common staples
            default=st.session_state.detected
        )

        num_res = st.slider("How many recipes?", 1, 10, 5)

        if st.button("📖 Get Recipes"):
            # Call the Recommendation API
            payload = {"ingredients": selected_ingredients, "num_recipes": num_res}
            res = requests.post("http://localhost:8000/predict", json=payload)

            if res.status_code == 200:
                st.session_state["recipes"] = res.json()["recipes"]
                st.session_state["ingredients_used"] = selected_ingredients
                st.switch_page("pages/3_recipes.py")
            else:
                st.error("Recommendation failed.")
