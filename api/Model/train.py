"""Train and serialize the recipe recommendation model."""

import os
import pickle
from pathlib import Path

from dotenv import load_dotenv
from api.Model.clean_dataset import Clean
from api.Model.vectorizer import Vectorizer
from api.Model.recommander import Recommander
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

load_dotenv(Path(__file__).parent.parent / ".env")

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
    texts = [' '.join(row) for row in data['NER_clean']]
    data_vec = vectorizer.fit_transform(texts)

    with open("api/Model/vectorizer.pkl", "wb") as f:
        pickle.dump(tf_idf, f)

    print("✅ Vectorizer saved in Model/vectorizer.pkl")

    print("🔬 Data vectorized ")

    model = NearestNeighbors(n_neighbors=5, metric="cosine")
    trainer = Recommander(model, data, "NER_clean")
    trainer.fit(data_vec)

    print("🤖 Model fitted, ready to predict")

    with open("api/Model/model.pkl", "wb") as file:
        pickle.dump(trainer, file)

    print("✅ Model saved in Model/model.pkl")

if __name__ == '__main__':
    main()
