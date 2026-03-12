from clean import Clean
from multiselect import IngredientSelector

# 1. Initialize CLEAN class
data_manager = Clean()
data = data_manager.clean_dataset()

# 2. Initialize MODEL class
#recipe_model = RecipeModel(data)
#recipe_model.train()

# 3. Use the MULTISELECT Class
selector = IngredientSelector(data)


# --- Streamlit ---
st.title("AI Sous-Chef")
