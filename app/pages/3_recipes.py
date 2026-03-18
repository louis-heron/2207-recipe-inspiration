import streamlit as st
import json

st.title("📋 Recipes")

# --- Guard: if no recipes in session, show a message ---
if "recipes" not in st.session_state:
    st.info("No recipes yet. Go to the **Inspiration** page to detect ingredients and get recommendations!")
    st.stop()

recipes = st.session_state["recipes"]
ingredients_used = st.session_state.get("ingredients_used", [])

# --- Summary header ---
st.subheader(f"{len(recipes)} recipes found")
if ingredients_used:
    st.caption("Based on: " + ", ".join(ingredients_used))

st.divider()

# --- Recipe cards ---
for recipe in recipes:
    title = recipe.get("title", "Untitled")
    match_score = recipe.get("match_score", "")       # e.g. "5/5"
    matched = recipe.get("matched_ingredients", [])

    # Parse ingredients and directions (they come as JSON strings from the API)
    try:
        ingredients = json.loads(recipe.get("ingredients", "[]"))
    except Exception:
        ingredients = []

    try:
        directions = json.loads(recipe.get("directions", "[]"))
        directions = [d for d in directions if d.strip()]  # Remove empty strings
    except Exception:
        directions = []

    # --- Match score bar ---
    score_label = ""
    score_pct = 0
    if "/" in match_score:
        matched_count, total = match_score.split("/")
        try:
            score_pct = int(matched_count) / int(total)
            if score_pct == 1.0:
                score_label = "✅ Perfect match"
            elif score_pct >= 0.8:
                score_label = "🟢 Great match"
            elif score_pct >= 0.5:
                score_label = "🟡 Good match"
            else:
                score_label = "🟠 Partial match"
        except ValueError:
            pass

    # --- Expandable card ---
    with st.expander(f"**{title}** — {match_score} {score_label}"):

        # Progress bar for match score
        if score_pct > 0:
            st.progress(score_pct)

        # Matched ingredients as tags
        if matched:
            st.markdown("**Matched ingredients:** " + " · ".join([f"`{i}`" for i in matched]))

        st.divider()

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("**🧂 Ingredients**")
            for item in ingredients:
                st.write(f"- {item}")

        with col2:
            st.markdown("**👨‍🍳 Directions**")
            for i, step in enumerate(directions, start=1):
                st.write(f"{i}. {step}")
