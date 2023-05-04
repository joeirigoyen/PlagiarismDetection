"""
Module to perform different preprocessing methods to the data.

Author: Raúl Youthan Irigoyen Osorio
Date: May 3rd 2023
"""
import nltk

from nltk.corpus import stopwords
from os import path
from pathlib import Path
from src.util.file_manager import FileManager as Fm
from string import punctuation


class TextData:
    def __init__(self, data: str) -> None:
        """
        Constructor of the Preprocessor class.
        """
        self._original = data
        self.data = data

    def __reset(self) -> None:
        """
        Reset the data to the original state.
        """
        self.data = self._original

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
        self.__reset()
        self.data = self.data.translate(str.maketrans('', '', punctuation))
        return self.data

    def remove_stopwords(self, dev=False) -> str:
        """
        Remove stopwords from the data.
        """
        self.__reset()
        self.__download_nltk_stopwords(dev)
        self.data = ' '.join([word for word in self.data.split() if word not in stopwords.words('english')])
        return self.data

    def lemmatize(self):
        """
        Lemmatize the data.
        """
        pass

    def stem(self):
        """
        Stem the data.
        """
        pass


if __name__ == '__main__':
    textdata = TextData("Hello, people of the world! I love everyone!")
    textdata.remove_stopwords()
