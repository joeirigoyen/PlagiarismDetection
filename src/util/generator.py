"""
This module contains a set of classes that generate different useful data types for testing purposes.

Author: Youthan Irigoyen
Creation date: 04-20-2023
"""
import secrets
import string

from pathlib import Path
from src.util.file_manager import FileManager as fm


class Generator:
    """
    This class generates useful data for testing purposes.
    """

    @staticmethod
    def random_string(max_len: int = -1) -> str:
        """
        Generates a random string of a given length (if given).
        :param max_len: The maximum length of the string to be generated. If not given, a random length will be chosen.
        :return: a random string of max_len.
        """
        # Set random length if a maximum length wasn't given.
        if max_len == -1:
            max_len = secrets.randbelow(1000) + 100
        # Generate random string
        return ''.join(secrets.choice(string.ascii_letters) for _ in range(max_len))

    def generate_random_texts(self, parent_directory: str, number_of_files: int, prefix: str = "test_file") -> None:
        """
        Generates a given number of random text files in a given directory.
        :param parent_directory: The directory where the files will be created.
        :param number_of_files: The number of files that will be created.
        :param prefix: An optional prefix for the file names. Default is "test_file".
        """
        # Validate parent directory
        parent_directory = Path(parent_directory)
        if not parent_directory.is_dir():
            raise ValueError('Path is not a directory')
        fm.validate_file(parent_directory)
        # Generate random files in parent directory
        for i in range(number_of_files):
            curr_filename = f"{prefix}_{i:03d}.txt"
            curr_file = Path.joinpath(parent_directory, curr_filename)
            with open(curr_file, "w") as file:
                file.write(self.random_string())
