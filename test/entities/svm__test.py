"""
Module to perform unit tests for the svm (Support Vector Machine) code.

Author: Rebeca Rojas Pérez
Date: May 3rd 2023
"""

import nltk
import unittest

from os import path
from pathlib import Path
from src.entities.svm import SVMModel
from src.entities.textdata import TextData


class TestSVMModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.text_data = 'This is a test text.'
        cls.model = SVMModel(TextData(cls.text_data))

    def test_get_vectors_with_count_vectorizer(self):
        params = {'ngrams': 2, 'vectorizer': 'count'}
        vectorizer = self.model.get_vectors(params)
        self.assertEqual(type(vectorizer).__name__, 'CountVectorizer')

    def test_get_vectors_with_tfidf_vectorizer(self):
        params = {'ngrams': 2, 'vectorizer': 'tfidf'}
        vectorizer = self.model.get_vectors(params)
        self.assertEqual(type(vectorizer).__name__, 'TfidfVectorizer')

    def test_get_vectors_with_invalid_vectorizer(self):
        params = {'ngrams': 2, 'vectorizer': 'invalid'}
        vectorizer = self.model.get_vectors(params)
        self.assertEqual(type(vectorizer).__name__, 'CountVectorizer')

    def test_predict_with_linear_svc(self):
        params = {'model': 'linear_svc', 'ngrams': 2, 'vectorizer': 'count'}
        self.assertIsNone(self.model.predict(params, train=False))

    def test_predict_with_naive_bayes(self):
        params = {'model': 'naive_bayes', 'ngrams': 2, 'vectorizer': 'count'}
        self.assertIsNone(self.model.predict(params, train=False))

    def test_predict_with_random_forest(self):
        params = {'model': 'random_forest', 'ngrams': 2, 'vectorizer': 'count'}
        self.assertIsNone(self.model.predict(params, train=False))

    def test_predict_with_kmeans(self):
        params = {'model': 'kmeans', 'ngrams': 2, 'vectorizer': 'count'}
        self.assertIsNone(self.model.predict(params, train=False))
