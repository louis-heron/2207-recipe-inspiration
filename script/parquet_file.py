import pandas as pd
from collections import Counter
import ast
from tqdm import tqdm
# Import your logic from the other file
from clean_ingredients import CleanIng
from Enums.minimum import MIN_FREQUENCY

def create_ingredient_list(input_csv, output_file):
    """
    Reads a large CSV, cleans ingredients using the shared CleanIng class,
    and saves the most frequent ones to a Parquet file.
    """
    # Initialize the shared cleaning class
    cleaner = CleanIng()
    master_counter = Counter()

    # Using chunksize to save RAM
    chunks = pd.read_csv(input_csv, chunksize=100000)

    for chunk in tqdm(chunks):
        # 1. Parse string lists into Python lists
        # We dropna() first to ensure we only iterate over valid rows
        raw_ingredients = chunk['ingredients'].dropna().apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else x
        )

        for sublist in raw_ingredients:
            if isinstance(sublist, list):
                for item in sublist:
                    # 2. Use the shared cleaning method from CleanIng
                    cleaned_name = cleaner.clean_single_ingredient(item)

                    # 3. Use the shared validation logic (brands, non-food, etc.)
                    if cleaned_name and cleaner._is_valid_text(cleaned_name):
                        master_counter.update([cleaned_name])

    # 4. Filter by frequency for the Parquet file
    # This ensures your model only sees 'real' ingredients, not typos or rare noise
    filtered = sorted([
        ing for ing, count in master_counter.items()
        if count >= MIN_FREQUENCY
    ])

    # 5. Save to Parquet
    df_out = pd.DataFrame(filtered, columns=['ingredient_name'])
    df_out.to_parquet(output_file, index=False)

if __name__ == "__main__":
    # Update these paths to match your actual file system
    INPUT_CSV = "raw_data/recipes_data.csv"
    OUTPUT_PARQUET = "ingredients.parquet"

    create_ingredient_list(INPUT_CSV, OUTPUT_PARQUET)
