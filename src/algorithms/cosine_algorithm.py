"""
This module executes the cosine similarity algorithm using different methods defined as the classes below.

Authors: Eduardo Rodriguez
Creation date: 04-20-2023
"""


from pathlib import Path
from typing import Any

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from src.algorithms.model import BaseModel
from src.util.file_manager import FileManager as fm


class CosineAlgorithm(BaseModel):
    """
    This class executes the cosine similarity algorithm using the provided method (uses CountVectorizer as the default method).
    """
    def __init__(self, vec_type: str = "count"):
        super().__init__()
        self.__vectorizer = None
        self.__vectorizer_types = {"tfidf": TfidfVectorizer(), "count": CountVectorizer()}
        self.validate_vectorizer(vec_type)

    def validate_vectorizer(self, vec_type: str) -> None:
        """
        Validates that the currently chosen vectorizer type is whitelisted.
        :param vec_type:
        :return:
        """
        if vec_type in self.__vectorizer_types.keys():
            self.__vectorizer = self.__vectorizer_types.get(vec_type)
        else:
            raise ValueError("Invalid vectorizer type.")

    def compare_text(self, original: Path | str, suspicious: Path | str) -> tuple[int | Any, str]:
        """
        Calculates the cosine similarity between two documents using the TfidfVectorizer or CountVectorizer method.
        :param original: The document to compare from.
        :param suspicious: The document to analyze.
        :return: A tuple containing the cosine similarity between the two documents and the original document's content.
        """
        if not fm.validate_file(original, create=False) or not fm.validate_file(suspicious, create=False):
            raise ValueError("The provided path is not a file.")
        corpus = fm.create_corpus(Path(original), Path(suspicious))
        trsfm = self.__vectorizer.fit_transform(corpus)

        res = cosine_similarity(trsfm[0:1], trsfm)[0][1] * 100
        return res, str(original)

    def compare_texts(self, f_dir: str | Path, s_file_path: str | Path) -> list[tuple[float, str]]:
        """
        Compares all the files in a directory against a single file.
        :param f_dir: The directory containing the files to compare.
        :param s_file_path: The file to compare against.
        :return: A list of tuples containing the cosine similarity between the two documents and the original document's content.
        """
        values = []
        if not Path(f_dir).is_dir():
            raise ValueError("The provided path is not a directory.")

        for child in Path(f_dir).iterdir():
            if child.is_file():
                res = self.compare_text(child, s_file_path)
                values.append(res)
        return values
