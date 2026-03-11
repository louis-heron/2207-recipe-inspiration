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

# Get list from user
user_items = selector.render()

if user_items:
    # Format the list into a string for your model
    query = selector.format_for_model(user_items)

    # Run your existing recommendation logic
    results = #recipe_model.get_recommendations(query)
    st.write(results)
