"""
Contains different modules to manage files and directories under different operating systems.

Authors: Youthan Irigoyen, Eduardo Rodríguez
Creation date: 04-20-2023
"""
from pathlib import Path
from typing import Any


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
    def validate_file(file_path: Any, create: bool = True) -> bool | None:
        curr_file = UnitaryFile(file_path)
        if not curr_file.exists():
            if create:
                curr_file.create()
                return True
            else:
                return False
        return True

    @staticmethod
    def read_file(file_path: Any) -> str:
        with open(file_path, 'r') as file:
            file_contents = file.read()
        return file_contents

    @staticmethod
    def create_corpus(*args: str) -> list[str]:
        corpus = []
        for doc in args:
            corpus.append(FileManager.read_file(doc))
        return corpus
