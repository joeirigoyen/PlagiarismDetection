"""
Contains different modules to manage files and directories under different operating systems.

Authors: Youthan Irigoyen, Eduardo Rodríguez
Creation date: 04-20-2023
"""
import nltk

from pathlib import Path
from typing import Any

from src.entities.textdata import TextDataDirectory


class UnitaryFile:
    def __init__(self, file_path: str | Path):
        self._f = self.convert_to_path(file_path)

    @property
    def f(self):
        return self._f

    @f.setter
    def f(self, new_f: str | Path):
        self._f = self.convert_to_path(new_f)

    @staticmethod
    def convert_to_path(file_path: str | Path) -> Path:
        return Path(file_path) if isinstance(file_path, str) else file_path

    def exists(self) -> bool:
        return self._f.exists()

    def create(self) -> None:
        if self._f.is_file():
            self._f.touch()
        else:
            self._f.mkdir(parents=True, exist_ok=True)


class FileManager:
    @staticmethod
    def validate_dir(dir_path: str | Path, create: bool = True) -> bool:
        curr_dir = UnitaryFile(dir_path)
        if not curr_dir.exists():
            if create:
                curr_dir.create()
                return True
            else:
                return False
        return True

    @staticmethod
    def validate_file(file_path: Any, create: bool = True) -> bool:
        curr_file = UnitaryFile(file_path)
        if not curr_file.exists():
            if create:
                curr_file.create()
                return True
            else:
                return False
        return True

    @staticmethod
    def read_file(file_path: Path) -> str:
        with open(file_path, 'r', encoding="utf-8") as file:
            file_contents = file.read()
        return file_contents

    @staticmethod
    def create_corpus(*args: Path) -> list[str]:
        corpus = []
        for doc in args:
            corpus.append(FileManager.read_file(doc))
        return corpus

    @staticmethod
    def extract_file_name(file_path: Path | str, ext: bool = False) -> str:
        file_path = Path(file_path)
        if ext:
            return file_path.name
        return file_path.stem

    @staticmethod
    def download_nltk_stopwords(path: str | Path) -> None:
        if not Path(path).exists():
            nltk.download('stopwords', download_dir=path)

    @staticmethod
    def get_max_len(texts: list[str]) -> int:
        return max(len(text.split()) for text in texts)
    
    @staticmethod
    def get_list_texts(dir: TextDataDirectory) -> list[str]:
        return [text.data for text in dir.data]