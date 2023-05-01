from pathlib import Path
from unittest import TestCase
from src.entities.algorithms.main.cosine_algorithm import CosineAlgorithm


class TestCosineAlgorithm(TestCase):
    def setup(self, vec_type: str) -> None:
        self.original_dir = Path().cwd().parent.joinpath("resources", "original")
        self.original = Path().cwd().parent.joinpath("resources", "original", "original_001.txt")
        self.comparison = Path().cwd().parent.joinpath("resources", "comparison.txt")
        self.cosine_algorithm = CosineAlgorithm(vec_type=vec_type)

    def test_compare_text_count(self) -> None:
        self.setup("count")
        result = self.cosine_algorithm.compare_text(self.original, self.comparison)
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], float)
        self.assertIsInstance(result[1], str)

    def test_compare_text_tfidf(self) -> None:
        self.setup("tfidf")
        result = self.cosine_algorithm.compare_text(self.original, self.comparison)
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], float)
        self.assertIsInstance(result[1], str)

    def test_compare_text_fail(self) -> None:
        self.setup("count")
        self.assertRaises(ValueError, self.cosine_algorithm.compare_text, "NOT_A_FILE", self.comparison)

    def test_compare_text_multiple_success(self) -> None:
        self.setup("count")
        result = self.cosine_algorithm.compare_texts(self.original_dir, self.comparison)
        for r in result:
            self.assertIsInstance(r, tuple)
            self.assertIsInstance(r[0], float)
            self.assertIsInstance(r[1], str)

    def test_compare_text_multiple_fail(self) -> None:
        self.setup("count")
        self.assertRaises(ValueError, self.cosine_algorithm.compare_texts, "NOT_A_DIR", self.comparison)
