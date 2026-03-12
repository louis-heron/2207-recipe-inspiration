"""
Recommander wrapper with strict typing via Protocol.
"""

from typing import Protocol, runtime_checkable, Optional, List
import numpy as np
import pandas as pd
from numpy.typing import NDArray

@runtime_checkable
class PredictModel(Protocol):
    """
    Protocol for prediction models implementing fit/predict interface.
    """

    def fit(self, features: NDArray[np.float64], target: Optional[NDArray[np.int64]] = None) -> 'PredictModel':
        """
        Fit model on feature matrix.
        """
        raise NotImplementedError

    def predict_to_users(self, features: NDArray[np.float64]) -> List[int]:
        """
        Return sorted indices of nearest neighbours.
        """
        return []

class Recommander:
    """
    Production wrapper enforcing PredictModel protocol.
    """
    TOP_DEFAULT = 5

    def __init__(self, model: PredictModel, recipes: pd.DataFrame, clean_column: str) -> None:
        """
        Initialize wrapper with compatible model and dataset.
        """
        self.model = model
        self.recipes = recipes
        self.clean_column = clean_column
        self.is_fitted: bool = False

    def fit(self, features: NDArray[np.float64], target: Optional[NDArray[np.int64]] = None) -> None:
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

        _, indices = self.model.predict(features)[:top_k]
        cosine_scores = self.model.predict_scores(features)[:top_k]
        query_set = set(ingredients)
        recipes: pd.DataFrame = self.recipes

        scored: List[tuple[int, float]] = []
        for idx, cosine in zip(indices, cosine_scores):
            recipe_idx: int = int(idx)
            recipe = recipes.iloc[recipe_idx]
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
