"""
Recommander wrapper with strict typing via Protocol.
"""

from typing import Any, Protocol, runtime_checkable, Optional, List
import numpy as np
import pandas as pd
from numpy.typing import NDArray

TOP_DEFAULT: int = 5

@runtime_checkable
class PredictModel(Protocol):
    """
    Protocol for prediction models implementing fit/kneighbors interface.
    Le `/` rend les paramètres positionnels uniquement : les noms n'ont pas à correspondre.
    """

    def fit(self, X: Any, /, y: Any = None) -> Any:
        """Fit model on feature matrix."""

    def kneighbors(self, X: Any, /) -> Any:
        """Return (distances, indices) of nearest neighbours."""

class Recommander:
    """
    Production wrapper enforcing PredictModel protocol.
    """

    def __init__(self, model: PredictModel, recipes: pd.DataFrame, clean_column: str) -> None:
        """
        Initialize wrapper with compatible model and dataset.
        """
        self.model = model
        self.recipes = recipes
        self.clean_column = clean_column
        self.is_fitted: bool = False

    def fit(
        self, features: NDArray[np.float64], target: Optional[NDArray[np.int64]] = None
    ) -> None:
        """
        Train wrapped model.
        """
        self.model.fit(features, target)
        self.is_fitted = True

    def predict_to_users(
        self,
        features: NDArray[np.float64],
        ingredients: List[str],
        top_k: int = TOP_DEFAULT
    ) -> List[int]:
        """
        Return top-k recipe indices ranked by cosine + coverage score.
        """
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")

        distances, indices_matrix = self.model.kneighbors(features)
        indices = indices_matrix[0][:top_k]
        cosine_scores = distances[0][:top_k]
        query_set = set(ingredients)
        recipes: pd.DataFrame = self.recipes

        scored: List[tuple[int, float]] = []
        for idx, cosine in zip(indices, cosine_scores):
            recipe_idx: int = int(idx)
            recipe = recipes.iloc[recipe_idx] # type: ignore
            recipe_str: str = recipe[self.clean_column]
            recipe_set = set(recipe_str.split(','))
            score = float(cosine) + self.coverage(query_set, recipe_set)
            scored.append((recipe_idx, score))

        return [idx for idx, _ in sorted(scored, key=lambda x: x[1], reverse=True)]

    def coverage(self, query_set: set[str], recipe_set: set[str]) -> float:
        """
        Calculate ingredient overlap coverage ratio.
        """
        return len(query_set & recipe_set) / len(query_set) if query_set else 0.0
