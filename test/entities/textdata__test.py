"""
Module to perform unit tests for the textdata (data preprocessing) code.

Author: Rebeca Rojas Pérez
Date: May 3rd 2023
"""

import nltk
import unittest

from os import path
from pathlib import Path
from src.entities.textdata import TextData


class TestTextData(unittest.TestCase):



    def test_remove_punctuation(self):
        td = TextData("Hello, world!")
        self.assertEqual(td.remove_punctuation(), "Hello world")

    def test_remove_stopwords(self):
        td = TextData("This is a test sentence")
        self.assertEqual(td.remove_stopwords(), "This test sentence")

    def test_remove_stopwords_with_dev(self):
        td = TextData("This is a test sentence")
        self.assertEqual(td.remove_stopwords(dev=True), "This test sentence")

