import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


class CosineVectorizerAlgorithm:
    def __init__(self, original: str, suspicious: str):
        self.data = {"original": original, "suspicious": suspicious}
        self._count_vect = CountVectorizer()

    def get_cosine_similarity(self, original: str, suspicious: str) -> tuple[float, str]:
        """
        Calculates the cosine similarity between two documents
        :param original: The document to compare from.
        :param suspicious: The document to analyze.
        :return: The cosine similarity between the two documents.
        """
        corpus = [original,suspicious]

        X_train_counts = self._count_vect.fit_transform(corpus)