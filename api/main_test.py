from clean import Clean
from multiselect import IngredientSelector

# 1. Initialize CLEAN class
data_manager = Clean()
data = data_manager.clean_dataset()

# 2. Initialize MODEL class
#recipe_model = RecipeModel(data)
#recipe_model.train()

# 3. Use the MULTISELECT Class
selector = IngredientSelector()
user_input = selector.render()

if user_input:
    formatted_input = selector.format_for_model(user_input)
    st.info(f"Ready for Vectorizer: {formatted_input}")


# --- Streamlit ---
st.title("AI Sous-Chef")
