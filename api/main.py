import pickle
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from Model.vectorizer import Vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Accept", "Accept-Language", "Content-Language"
    ],
)

app.state.model = pickle.load(open("Model/model.pkl", "rb"))

@app.get("/")
def root():
    return {"greeting": "Hello"}

@app.post("/predict")
def predict(ingredients: List[str], num_recipes: int):
    tf_idf = TfidfVectorizer()
    vectorizer = Vectorizer(tf_idf)
    ing_vec = vectorizer.transform(ingredients)

    recommendations = app.state.model.predict_to_users(ing_vec, ingredients, num_recipes)

    return {"Recipes": recommendations}
