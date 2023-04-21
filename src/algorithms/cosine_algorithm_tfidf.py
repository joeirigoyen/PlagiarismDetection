"""
This module executes the cosine similarity algorithm using different methods defined as the classes below.

Author: Youthan Irigoyen
Creation date: 04-20-2023
"""


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


class CosineAlgorithm:
    def __init__(self, original: str, suspicious: str):
        self.data = {"original": original, "suspicious": suspicious}
        self._vectorizer = TfidfVectorizer()

    def get_cosine_similarity(self, original: str, suspicious: str) -> tuple[float, str]:
        """
        Calculates the cosine similarity between two documents
        :param original: The document to compare from.
        :param suspicious: The document to analyze.
        :return: The cosine similarity between the two documents.
        """
        original = self.data.loc[original]
        suspicious = self.data.loc[suspicious]

        # Calculate the dot product
        dot_product = (original * suspicious).sum()

        # Calculate the magnitude of the vectors
        magnitude = (original.pow(2).sum() * suspicious.pow(2).sum()).pow(0.5)

        # Calculate the cosine similarity
        cosine_similarity = dot_product / magnitude

        return cosine_similarity
