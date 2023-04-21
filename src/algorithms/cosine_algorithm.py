"""
This module executes the cosine similarity algorithm using different methods defined as the classes below.

Author: Youthan Irigoyen
Creation date: 04-20-2023
"""


from pathlib import Path
from typing import Any
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from src.algorithms.model import BaseModel
from src.utils import file_manager as fm

class CosineTfidfAlgorithm(BaseModel):
    def __init__(self, vec_type: str = "count"):
        self.__vectorizer_types = {"tfidf": TfidfVectorizer(), "count": CountVectorizer()}
        self.validate_vectorizer(vec_type)

    def validate_vectorizer(self, vec_type: str) -> bool:
        if vec_type in self.__vectorizer_types.keys():
            self._vectorizer = self.__vectorizer_types.get(vec_type)
        else:
            raise ValueError("Invalid vectorizer type.")

    def compare_text(self, original: str, suspicious: str) -> tuple[float, str]:
        """
        Calculates the cosine similarity between two documents using the TfidfVectorizer or CountVectorizer method.
        :param original: The document to compare from.
        :param suspicious: The document to analyze.
        :return: The cosine similarity between the two documents.
        """
        corpus = fm.create_corpus(original, suspicious)
        trsfm = self._vectorizer.fit_transform(corpus)

        res = (cosine_similarity(trsfm[0:1], trsfm)[0][1]) * 100
        return f'{res:.2f}', original

    def compare_texts(self, f_dir: str, s_file_path: str) -> list[tuple[float, str]]:
        values = []
        for child in Path(f_dir).iterdir():
            if child.is_file():
                res = self.compare_text(child, s_file_path)
                values.append(res)
        return values