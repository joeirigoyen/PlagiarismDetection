"""
Contains different modules to manage files and directories under different operating systems.

Author: Youthan Irigoyen
Creation date: 04-20-2023
"""
from pathlib import Path
from typing import Any


class UnitaryFile:
    def __init__(self, file_path: str | Path):
        self._file = self.convert_to_path(file_path)

    @staticmethod
    def convert_to_path(file_path: str | Path) -> Path:
        return Path(file_path) if isinstance(file_path, str) else file_path

    def exists(self) -> bool:
        return self._file.exists()

    def create(self) -> None:
        if self._file.is_file():
            self._file.touch()
        else:
            self._file.mkdir(parents=True, exist_ok=True)


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
