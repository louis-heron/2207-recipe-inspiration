import pandas as pd
from collections import Counter
import ast
from tqdm import tqdm
from clean import Clean

def create_ingredient_list(input_csv, output_file, min_freq=100):
    # Using chunksize if the file is massive to save RAM
    chunks = pd.read_csv(input_csv, chunksize=100000)

    master_counter = Counter()

    for chunk in tqdm(chunks):
        # Convert string representation of list to actual list
        # We use .dropna() to avoid errors on empty rows
        ingredients_list = chunk['ingredients'].dropna().apply(ast.literal_eval)

        for sublist in ingredients_list:
            master_counter.update(sublist)

    # Filter by frequency for better UX
    filtered = sorted([
        ing for ing, count in master_counter.items()
        if count >= min_freq
    ])

    # Save to Parquet
    df_out = pd.DataFrame(filtered, columns=['ingredient_name'])
    df_out.to_parquet(output_file, index=False)
    print(f"--- Success! {len(filtered)} ingredients saved to {output_file} ---")

if __name__ == "__main__":
    create_ingredient_list(Clean.clean_dataset, 'ingredients.parquet')
