"""
Module to perform different preprocessing methods to the data.

Author: Raúl Youthan Irigoyen Osorio
Date: May 3rd 2023
"""
import nltk

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
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
        words = nltk.word_tokenize(self.remove_punctuation(self))
        lemms = []
        for word in words:
            lemms.append(lemmatizer.lemmatize(word))
        return set(lemms)

    def stem(self) -> set:
        """
        Stem the data.
        """
        stemmer = PorterStemmer()
        words = nltk.word_tokenize(self.remove_punctuation(self))
        stems = []
        for word in words:
            stems.append(stemmer.stem(word))
        return set(stems)


class TextDataDirectory:
    def __init__(self, data: str | Path) -> None:
        """
        Class that contains a directory of text data.
        """
        self.data: list[TextData] = self.__convert_directory(data)

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
