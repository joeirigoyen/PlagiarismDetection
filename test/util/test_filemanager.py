"""
Module to perform unit tests for the file_manager code.

Author: Rebeca Rojas Pérez
Date: May 3rd 2023
"""

import os
import tempfile
import unittest

from pathlib import Path
from src.util.file_manager import UnitaryFile, FileManager
from unittest.mock import MagicMock
from unittest.mock import patch


class TestUnitaryFile(unittest.TestCase):
    def setUp(self):
        """
        Initial setup to perform unit tests in the UnitaryFile class
        """
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, dir=self.temp_dir.name)
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        """
        Restore changes after unit tests are finished in the UnitaryFile  Class.
        """
        self.temp_file.close()
        self.temp_dir.cleanup()

    def test_convert_to_path(self):
        """
        Unit test for the convert_to_path() function in the UnitaryFile Class.
        """
        file_path_str = "path/to/file.txt"
        file_path = Path(file_path_str)
        self.assertEqual(UnitaryFile.convert_to_path(file_path_str), file_path)
        self.assertEqual(UnitaryFile.convert_to_path(file_path), file_path)

    def test_exists(self):

        """
        Unit test for the exists() function in the UnitaryFile Class.
        """
        self.assertTrue(Path.cwd())

        file = UnitaryFile(self.temp_path / "non_existing_file.txt")
        self.assertFalse(file.exists())

    def test_create_file(self):
        """
        Unit test for the create_file() function in the UnitaryFile Class.
        """
        file = UnitaryFile(Path.cwd().parent.joinpath('resources', 'file_0.txt'))
        self.assertFalse(file.exists())
        file.create()
        self.assertTrue(file.exists())
        os.rmdir(file._f)

    def test_create_directory(self):
        """
        Unit test for the create_directory() function in the UnitaryFile Class.
        """
        dir = UnitaryFile(self.temp_path / "new_directory")
        self.assertFalse(dir.exists())
        dir.create()
        self.assertTrue(dir.exists())
        self.assertTrue(os.path.isdir(str(dir._f)))


class TestFileManager(unittest.TestCase):

    def setUp(self):
        self.file_manager = FileManager()

    def test_validate_dir_existing_dir(self):
        """
        Unit test for the validate_dir() function with an existing directory as parameter
        in the FileManager Class.
        """
        # Arrange
        dir_path = "test/resources/dir"

        # Act
        result = self.file_manager.validate_dir(dir_path)

        # Assert
        self.assertTrue(result)

    def test_validate_dir_non_existing_dir(self):
        """
        Unit test for the validate_dir() function with a non-existing directory as parameter
        in the FileManager Class.
        """
        # Arrange
        dir_path = "test/resources/dir_0"

        # Act
        result = self.file_manager.validate_dir(dir_path, create=False)

        # Assert
        self.assertFalse(result)

    def test_validate_dir_create_dir(self):
        """
        Unit test for the validate_dir() function with the create parameter as true
        in the FileManager Class.
        """
        # Arrange
        dir_path = "test_files/resources/dir"

        # Act
        result = self.file_manager.validate_dir(dir_path, create=True)

        # Assert
        self.assertTrue(result)

        # Destroy created directories
        for root in Path(dir_path).iterdir():
            curr_dir = Path(dir_path)
            if curr_dir.is_dir() and curr_dir.exists():
                for f in curr_dir.iterdir():
                    if f.is_file():
                        os.rmdir(os.path.join(f))
                os.rmdir(os.path.join(root))



    def test_validate_file_existing_file(self):
        """
        Unit test for the validate_file() function with an existing file as parameter
        in the FileManager Class.
        """
        # Arrange
        file_path = "test/resources/file.txt"

        # Act
        result = self.file_manager.validate_file(file_path)

        # Assert
        self.assertTrue(result)

    def test_validate_file_non_existing_file(self):
        """
        Unit test for the validate_file() function with a non-existing file as parameter
        in the FileManager Class.
        """
        # Arrange
        file_path = "test/resources/file_0.txt"

        # Act
        result = self.file_manager.validate_file(file_path, create=False)

        # Assert
        self.assertFalse(result)

    def test_validate_file_create_file(self):
        """
        Unit test for the validate_file() function with the create parameter as true
        in the FileManager Class.
        """
        # Arrange
        file_path = "test_files/resources/file.txt"

        # Act
        result = self.file_manager.validate_file(file_path, create=True)

        # Assert
        self.assertTrue(result)

        # Destroy created directories
        for root, dirs, files in os.walk(file_path.split('/')[0], topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

        os.rmdir(file_path.split('/')[0])

    def test_read_file(self):
        """
        Unit test for the read_file() function in the FileManager Class.
        """
        # Create a temporary file for testing
        temp_file = Path("temp.txt")
        with open(temp_file, "w") as f:
            f.write("hello world")

        # Test that the file can be read
        self.assertEqual(FileManager.read_file(temp_file), "hello world")

        # Delete the temporary file
        os.remove(temp_file)

    def test_create_corpus(self):
        """
        Unit test for the createe_corpus() function in the FileManager Class.
        """
        # Mock the read_file method to return a string
        FileManager.read_file = MagicMock(return_value="hello world")

        # Test that the create_corpus method correctly reads multiple files and returns a list
        corpus = FileManager.create_corpus(Path("file1.txt"), Path("file2.txt"), Path("file3.txt"))
        self.assertEqual(corpus, ["hello world", "hello world", "hello world"])

        # Reset the read_file mock
        FileManager.read_file.reset_mock()

    def test_extract_file_name_without_ext(self):
        """
        Unit test for the extract_file_name() function with the ext parameter as false
        in the FileManager Class.
        """
        # Test extracting file name without extension
        file_path = "path/to/myfile.txt"
        expected_output = "myfile"
        self.assertEqual(FileManager.extract_file_name(file_path), expected_output)

    def test_extract_file_name_with_ext(self):
        """
        Unit test for the extract_file_name() function with the ext parameter as true
        in the FileManager Class.
        """
        # Test extracting file name with extension
        file_path = "path/to/myfile.txt"
        expected_output = "myfile.txt"
        self.assertEqual(FileManager.extract_file_name(file_path, ext=True), expected_output)

    def test_extract_file_name_from_path_object(self):
        """
        Unit test for the extract_file_name() function with the file_path parameter as a path object
        in the FileManager Class.
        """
        # Test extracting file name from Path object
        file_path = Path("path/to/myfile.txt")
        expected_output = "myfile"
        self.assertEqual(FileManager.extract_file_name(file_path), expected_output)

    def test_extract_file_name_from_path_object_with_ext(self):
        """
        Unit test for the extract_file_name() function with the file_path parameter as a path object
        and the ext parameter as true in the FileManager Class.
        """
        # Test extracting file name with extension from Path object
        file_path = Path("path/to/myfile.txt")
        expected_output = "myfile.txt"
        self.assertEqual(FileManager.extract_file_name(file_path, ext=True), expected_output)
