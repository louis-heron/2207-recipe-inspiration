"""
Vectorizer wrapper with strict typing via Generic + Protocol.
"""

from typing import Any, Iterable, Protocol, List, runtime_checkable, TypeVar, Generic

V = TypeVar('V', bound='VectorModel')

@runtime_checkable
class VectorModel(Protocol):
    """
    Protocol for vectorization models (TfidfVectorizer, SentenceTransformer, etc.).
    Le `/` rend les paramètres positionnels uniquement : les noms n'ont pas à correspondre.
    """

    def fit_transform(self, texts: Iterable[str], /) -> Any:
        """Fit model on training texts and transform to vectors."""


    def transform(self, texts: Iterable[str], /) -> Any:
        """Transform new texts to match training vector space."""



class Vectorizer(Generic[V]):
    """
    Type-safe vectorizer wrapper enforcing VectorModel protocol.
    """

    def __init__(self, vectorizer: V) -> None:
        """Initialize with a model implementing VectorModel protocol."""
        self.vectorizer = vectorizer

    def fit_transform(self, recipes: Iterable[str]) -> Any:
        """Fit and transform recipes to feature vectors."""
        return self.vectorizer.fit_transform(recipes)

    def transform(self, ingredients: List[str]) -> Any:
        """Transform query ingredients to a feature vector."""
        text = ' '.join(ingredients)
        return self.vectorizer.transform([text])
