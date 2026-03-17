"""
Recipe Recommander API - FastAPI server for recipe recommendations.
Input: ingredient list → Output: ranked recipes with match scores.
"""

import pickle
import sys
from pathlib import Path
from typing import Dict, List
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing_extensions import TypedDict
from pydantic import BaseModel
import api.Model.recommander as _recommander_mod
import api.Model.vectorizer as _vectorizer_mod
from api.Vision.detector import IngredientDetector


class RecipeResult(TypedDict):
    """Recipe recommendation result structure."""
    title: str
    ingredients: str
    directions: str
    matched_ingredients: List[str]
    match_score: str

sys.modules.setdefault('recommander', _recommander_mod)
sys.modules.setdefault('vectorizer', _vectorizer_mod)


app = FastAPI(
    title="Recipe Recommander API",
    version="1.0",
    description="Recipe recommendation API using TF-IDF similarity + ingredient coverage scoring.",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


BASE_DIR = Path(__file__).parent
model_path = BASE_DIR / "Model" / "model.pkl"
vectorizer_path = BASE_DIR / "Model" / "vectorizer.pkl"
vision_model_path = BASE_DIR / "Vision" / "best.pt"

app.state.model = pickle.load(open(model_path, "rb"))
app.state.vectorizer = pickle.load(open(vectorizer_path, "rb"))
app.state.detector = IngredientDetector(str(vision_model_path))

@app.get("/", tags=["health"])
def root() -> Dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Health status and API documentation links.
    """
    return {
        "greeting": "Recipe Recommander API v1.0",
        "status": "healthy",
        "docs": "/docs",
        "redoc": "/redoc"
    }


class PredictRequest(BaseModel):
    """
    Request schema for recipe recommendations.

    Attributes:
        ingredients: User ingredients list (e.g., ["pasta", "tomato"]).
        num_recipes: Number of recipes to return (default: 5, max: 20).
    """
    ingredients: List[str]
    num_recipes: int = 5

@app.post("/detect-ingredients", tags=["vision"])
async def detect_ingredients(file: UploadFile = File(...)):
    """Upload a JPEG/PNG to get a list of detected ingredients."""
    try:
        contents = await file.read()
        ingredients = app.state.detector.detect(contents)
        return {"detected_ingredients": ingredients}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict", tags=["recommendations"], response_model=Dict[str, List[RecipeResult]])
def predict(request: PredictRequest) -> Dict[str, List[RecipeResult]]:
    """
    Generate personalized recipe recommendations.

    Args:
        request: Prediction request with ingredients and recipe count.

    Returns:
        Dictionary containing recommended recipes with match details.

    Raises:
        HTTPException: 500 if prediction fails (model error, invalid data).

    Example:
        Input: {"ingredients": ["pasta", "tomato"], "num_recipes": 3}
        Output: {"recipes": [{"title": "Spaghetti Bolognese", "match_score": "2/8", ...}]}
    """
    try:
        text = " ".join(request.ingredients)
        ing_vec = app.state.vectorizer.transform([text])

        indices: List[int] = app.state.model.predict_to_users(
            ing_vec, request.ingredients, request.num_recipes
        )

        query_set: set[str] = set(request.ingredients)
        recipes_df = app.state.model.recipes

        results: List[RecipeResult] = []
        for idx in indices:
            recipe = recipes_df.iloc[idx]

            recipe_ner = recipe["NER_clean"]
            recipe_set: set[str] = (
                {str(ing) for ing in recipe_ner}  # type: ignore[union-attr]
                if isinstance(recipe_ner, list)
                else set(str(recipe_ner).split(','))
            )

            matched: set[str] = query_set & recipe_set

            results.append({
                "title": str(recipe["title"]),
                "ingredients": str(recipe["ingredients"]),
                "directions": str(recipe["directions"]),
                "matched_ingredients": sorted(matched),
                "match_score": f"{len(matched)}/{len(recipe_set)}",
            })

        return {"recipes": results}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        ) from e
