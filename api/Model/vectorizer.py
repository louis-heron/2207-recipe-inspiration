"""
Vectorizer wrapper with strict typing via Protocol.
"""

from typing import Protocol, List, runtime_checkable

@runtime_checkable
class VectorModel(Protocol):
    """
    Protocol for vectorization models (TfidfVectorizer, SentenceTransformer, etc.).
    """

    def fit_transform(self, texts: List[str]) -> object:
        """
        Fit model on training texts and transform to vectors.

        Parameters
        ----------
        texts : List[str]
            Training documents as list of strings

        Returns
        -------
        object
            Training vectors (sparse matrix, ndarray, tensor)
        """

    def transform(self, texts: List[str]) -> object:
        """
        Transform new texts to match training vector space.

        Parameters
        ----------
        texts : List[str]
            New documents to vectorize

        Returns
        -------
        object
            Query vectors matching training space
        """

class Vectorizer:
    """
    Type-safe vectorizer wrapper enforcing VectorModel protocol.
    """

    def __init__(self, vectorizer: VectorModel) -> None:
        """
        Parameters
        ----------
        vectorizer : VectorModel
            Vectorization model implementing the protocol
        """
        self.vectorizer = vectorizer

    def fit_transform(self, recipes: List[str]) -> object:
        """
        Fit and transform recipes to vectors.

        Parameters
        ----------
        recipes : List[List[str]]
            Training recipes (list of ingredient lists)

        Returns
        -------
        object
            Feature matrix from vectorizer
        """
        texts = [' '.join(recipe) for recipe in recipes]
        return self.vectorizer.fit_transform(texts)

    def transform(self, ingredients: List[str]) -> object:
        """
        Transform query ingredients.

        Parameters
        ----------
        ingredients : List[str]
            Query ingredients

        Returns
        -------
        object
            Query vector
        """
        text = ' '.join(ingredients)
        return self.vectorizer.transform([text])
