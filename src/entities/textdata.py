"""
Module to perform different preprocessing methods to the data.

Author: Raúl Youthan Irigoyen Osorio
Date: May 3rd 2023
"""
from typing import List

import nltk

from nltk import ngrams
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from os import path
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from src.util.file_manager import FileManager as Fm
from string import punctuation


class TextData:
    def __init__(self, data: str) -> None:
        """
        Constructor of the Preprocessor class.
        """
        self._original = data
        self.data = data

    def __download_nltk_stopwords(self, dev: bool = False) -> None:
        """
        Download the nltk stopwords.
        """
        dev_root = Path(path.dirname(path.abspath(__file__))).parent.parent.joinpath("self") / "stopwords"
        normal_root = Path(path.dirname(path.abspath(__file__))).parent / "stopwords"
        root = dev_root if dev else normal_root
        Fm.download_nltk_stopwords(root)

    def remove_punctuation(self) -> str:
        """
        Remove punctuation from the data.
        :return:
        """
        self.data = self.data.translate(str.maketrans('', '', punctuation))
        return self.data

    def remove_stopwords(self, dev=False) -> str:
        """
        Remove stopwords from the data.
        """
        self.__download_nltk_stopwords(dev)
        self.data = ' '.join([word for word in self.data.split() if word not in stopwords.words('english')])
        return self.data

    def lemmatize(self) -> set:
        """
        Lemmatize the data.
        """
        lemmatizer = WordNetLemmatizer()
        words = nltk.word_tokenize(self.remove_punctuation())
        lemms = []
        for word in words:
            lemms.append(lemmatizer.lemmatize(word))
        return set(lemms)

    def stem(self) -> set:
        """
        Stem the data.
        """
        stemmer = PorterStemmer()
        words = nltk.word_tokenize(self.remove_punctuation())
        stems = []
        for word in words:
            stems.append(stemmer.stem(word))
        return set(stems)

    def vectorize(self, other, method: str = "count", n_grams: int = 8) -> tuple:
        """
        Vectorize the data.
        """
        match method:
            case "count":
                vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, n_grams))
            case "tfidf":
                vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, n_grams))
            case _:
                vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, n_grams))
        corpus = [self.data, other.data]
        transform = vectorizer.fit_transform(corpus).toarray()
        return transform[0].reshape(1, -1), transform[1].reshape(1, -1)

    def cosine_distance(self, other, vector: str = "count") -> float:
        """
        Calculate the cosine distance between two TextData objects.
        """
        vector_1, vector_2 = self.vectorize(other, method=vector)
        return cosine_similarity(vector_1, vector_2)[0][0]

    def jaccard_distance(self, other) -> float:
        """
        Calculate the jaccard distance between two TextData objects.
        """
        return len(self.lemmatize().intersection(other.lemmatize())) / len(self.lemmatize().union(other.lemmatize()))

    def euclidean_distance(self, other, vector: str = "count") -> float:
        """
        Calculate the euclidean distance between two TextData objects.
        """
        vector_1, vector_2 = self.vectorize(other, method=vector)
        return euclidean_distances(vector_1, vector_2)[0][0]

    def get_distance(self, other, method: str):
        """
        Get the distance between two TextData objects according to a provided method.
        :param other: The other TextData object.
        :param method: The preferred method.
        :return: The result of the measurement.
        """
        match method:
            case "cosine":
                return self.cosine_distance(other)
            case "jaccard":
                return self.jaccard_distance(other)
            case "euclidean":
                return self.euclidean_distance(other)
            case _:
                return self.cosine_distance(other)

    def get_ngrams(self, n: str) -> set:
        """
        Get the ngrams of the data.
        """
        return set(ngrams(self.data.split(), int(n)))


class TextDataDirectory:
    def __init__(self, data: str | Path | list[TextData]) -> None:
        """
        Class that contains a directory of text data.
        """
        self.data: list[TextData] = self.__convert_directory(data) if isinstance(data, str) or isinstance(data, Path) else data

    @staticmethod
    def __validate_dir(data: str | Path) -> bool:
        datapath = Path(data)
        return datapath.exists() and datapath.is_dir()

    def __convert_directory(self, data: str | Path) -> list[TextData]:
        """
        Convert the data directory into a list of TextData objects.
        """
        textdata_list = []
        if self.__validate_dir(data):
            for file in Path(data).iterdir():
                if file.is_file() and file.suffix == ".txt":
                    textdata_list.append(TextData(Fm.read_file(file)))
            return textdata_list
        else:
            raise FileNotFoundError("The specified path does not exist or is not a directory.")

    def __download_nltk_stopwords(self, dev: bool = False) -> None:
        """
        Download the nltk stopwords.
        """
        dev_root = Path(path.dirname(path.abspath(__file__))).parent.parent.joinpath("self") / "stopwords"
        normal_root = Path(path.dirname(path.abspath(__file__))).parent / "stopwords"
        root = dev_root if dev else normal_root
        Fm.download_nltk_stopwords(root)

    def remove_punctuation(self) -> list[TextData]:
        """
        Remove punctuation from the data.
        :return:
        """
        for textdata in self.data:
            textdata.remove_punctuation()
        return self.data

    def remove_stopwords(self, dev=False) -> list[TextData]:
        """
        Remove stopwords from the data.
        """
        self.__download_nltk_stopwords(dev)
        for textdata in self.data:
            textdata.remove_stopwords()
        return self.data

    def lemmatize(self) -> list[set]:
        """
        Lemmatize the data.
        """
        lemms = []
        for textdata in self.data:
            lemms.append(textdata.lemmatize())
        return lemms

    def stem(self) -> list[set]:
        """
        Stem the data.
        """
        stems = []
        for textdata in self.data:
            stems.append(textdata.stem())
        return stems

    def preprocess(self, method: str):
        """
        Preprocess each data file.
        """
        match method:
            case "punctuation":
                return self.remove_punctuation()
            case "stopwords":
                return self.remove_stopwords()
            case "lemmatize":
                return self.lemmatize()
            case "stem":
                return self.stem()
            case _:
                return self.remove_punctuation()
            

    def get_ngrams(self, n: str) -> list[set]:
        """
        Get the ngrams of the data.
        """
        ngrams = []
        for f in self.data:
            ngrams.append(f.get_ngrams(n))
        return ngrams
