"""
Module to perform unit tests for the textdata (data preprocessing) code.

Author: Rebeca Rojas Pérez
Date: May 3rd 2023
"""

import shutil
import unittest
import tempfile

from pathlib import Path
from src.entities.textdata import TextData, TextDataDirectory


class TestTextData(unittest.TestCase):
    def setUp(self):
        """
        Initial setup to perform unit tests in the TextData class
        """
        self.text_data = TextData(
            "This is some text. It contains punctuation, stopwords, and needs to be lemmatized and stemmed!")

    def test_remove_punctuation(self):
        expected = "This is some text It contains punctuation stopwords and needs to be lemmatized and stemmed"
        result = self.text_data.remove_punctuation()
        self.assertEqual(result, expected)

    def test_remove_stopwords(self):
        expected = "This text contains punctuation needs lemmatized stemmed"
        result = self.text_data.remove_stopwords()
        self.assertEqual(result, expected)

    def test_lemmatize(self):
        expected = {'This', 'is', 'some', 'text', 'It', 'contains', 'punctuation', 'stopword', 'and', 'need', 'to',
                    'be', 'lemmatized', 'stemmed'}
        result = self.text_data.lemmatize()
        self.assertEqual(result, expected)

    def test_stem(self):
        expected = {'thi', 'is', 'some', 'text', 'it', 'contain', 'punctuat', 'stopword', 'and', 'need', 'to', 'be',
                    'lemmat', 'stem'}
        result = self.text_data.stem()
        self.assertEqual(result, expected)

    def test_vectorize(self):
        other = TextData("This is some other text.")
        expected = (
            [[1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
            [[1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0]]
        )
        result = self.text_data.vectorize(other)
        self.assertTrue(len(result) > 0)

    def test_cosine_distance(self):
        other = TextData("This is some other text.")
        result = self.text_data.cosine_distance(other)
        self.assertTrue(result > 0)

    def test_jaccard_distance(self):
        other = TextData("This is some other text.")
        result = self.text_data.jaccard_distance(other)
        self.assertTrue(result > 0)

    def test_euclidean_distance(self):
        other = TextData("This is some other text.")
        result = self.text_data.euclidean_distance(other)
        self.assertTrue(result > 0)

class TestTextDataDirectory(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.file1 = Path(self.temp_dir) / "file1.txt"
        self.file1.write_text("This is a test file.\nIt contains some text.")
        self.file2 = Path(self.temp_dir) / "file2.txt"
        self.file2.write_text("This is another test file.\nIt also contains some text.")
        self.dir = TextDataDirectory(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)


    def test_validate_dir(self):
        self.assertTrue(TextDataDirectory._TextDataDirectory__validate_dir(self.temp_dir))
        self.assertFalse(TextDataDirectory._TextDataDirectory__validate_dir(self.file1))

    def test_convert_directory(self):
        data = self.dir._TextDataDirectory__convert_directory(self.temp_dir)
        self.assertEqual(len(data), 2)
        self.assertIsInstance(data[0], TextData)

    def test_remove_punctuation(self):
        data = self.dir.remove_punctuation()
        self.assertTrue(data[0].data.count(".") == 0)

    def test_remove_stopwords(self):
        data = self.dir.remove_stopwords()
        self.assertEqual("This another test file. It also contains text.", data[0].data)

    def test_lemmatize(self):
        lemmas = self.dir.lemmatize()
        self.assertTrue(len(lemmas[0]) > 0)

    def test_stem(self):
        stems = self.dir.stem()
        self.assertTrue(len(stems[0]) > 0)