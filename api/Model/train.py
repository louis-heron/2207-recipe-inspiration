"""Train and serialize the recipe recommendation model."""

import os
import pickle
from pathlib import Path

from dotenv import load_dotenv
from clean import Clean
from vectorizer import Vectorizer
from recommander import Recommander
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

load_dotenv()

def main() -> None:
    """Train and save the recommendation model."""
    print("🚀 Start training...")

    BASE_DIR = Path(__file__).parent
    dataset_env = os.getenv("PATH_DATASET")
    if dataset_env is None:
        raise ValueError("La variable d'environnement PATH_DATASET n'est pas définie")
    path_to_dataset = BASE_DIR / dataset_env

    if not path_to_dataset.exists():
        raise FileNotFoundError(f"Dataset manquant : {path_to_dataset}")

    cleaner = Clean(path_to_dataset)
    data = cleaner.clean_dataset("title", "ingredients", "directions")

    print(f"🧽 Dataset cleaned : {len(data)} recipes yet")

    tf_idf = TfidfVectorizer()
    vectorizer = Vectorizer(tf_idf)
    data_vec = vectorizer.fit_transform(data["clean_ingredients"])

    print("🔬 Data vectorized ")

    model = NearestNeighbors(n_neighbors=5, metric="cosine")
    trainer = Recommander(model, data, "clean_ingredients")
    trainer.fit(data_vec)

    print("🤖 Model fitted, ready to predict")

    with open("Model/model.pkl", "wb") as file:
        pickle.dump(model, file)

    print("✅ Model saved in Model/model.pkl")

if __name__ == '__main__':
    main()
