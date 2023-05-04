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


class TextDataDirectory:
    def __init__(self, data: str | Path) -> None:
        """
        Class that contains a directory of text data.
        """
        self.data = self.__convert_directory(data)

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
