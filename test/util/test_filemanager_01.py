import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock
from src.util.file_manager import UnitaryFile, FileManager

class TestUnitaryFile(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, dir=self.temp_dir.name)
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_file.close()
        self.temp_dir.cleanup()

    def test_convert_to_path(self):
        file_path_str = "path/to/file.txt"
        file_path = Path(file_path_str)
        self.assertEqual(UnitaryFile.convert_to_path(file_path_str), file_path)
        self.assertEqual(UnitaryFile.convert_to_path(file_path), file_path)

    def test_exists(self):
        file = UnitaryFile(self.temp_path / "existing_file.txt")
        self.assertTrue(file.exists())

        file = UnitaryFile(self.temp_path / "non_existing_file.txt")
        self.assertFalse(file.exists())

    def test_create_file(self):
        file = UnitaryFile(self.temp_path / "new_file.txt")
        self.assertFalse(file.exists())
        file.create()
        self.assertTrue(file.exists())
        self.assertTrue(os.path.isfile(str(file._f)))
        os.remove(str(file._f))

    def test_create_directory(self):
        dir = UnitaryFile(self.temp_path / "new_directory")
        self.assertFalse(dir.exists())
        dir.create()
        self.assertTrue(dir.exists())
        self.assertTrue(os.path.isdir(str(dir._f)))


class TestFileManager(unittest.TestCase):

    def setUp(self):
        self.file_manager = FileManager()

    def test_validate_file_existing_file(self):
        # Arrange
        file_path = "test/resources/file.txt"

        # Act
        result = self.file_manager.validate_file(file_path)

        # Assert
        self.assertTrue(result)

    def test_validate_file_non_existing_file(self):
        # Arrange
        file_path = "test/resources/file.txt"

        # Act
        result = self.file_manager.validate_file(file_path, create=False)

        # Assert
        self.assertFalse(result)

    def test_validate_file_create_file(self):
        # Arrange
        file_path = "test/resources/file.txt"

        # Act
        result = self.file_manager.validate_file(file_path, create=True)

        # Assert
        self.assertTrue(result)

    def test_read_file(self):
        # Create a temporary file for testing
        temp_file = "temp.txt"
        with open(temp_file, "w") as f:
            f.write("hello world")

        # Test that the file can be read
        self.assertEqual(FileManager.read_file(temp_file), "hello world")

        # Delete the temporary file
        os.remove(temp_file)

    def test_create_corpus(self):
        # Mock the read_file method to return a string
        FileManager.read_file = MagicMock(return_value="hello world")

        # Test that the create_corpus method correctly reads multiple files and returns a list
        corpus = FileManager.create_corpus("file1.txt", "file2.txt", "file3.txt")
        self.assertEqual(corpus, ["hello world", "hello world", "hello world"])

        # Reset the read_file mock
        FileManager.read_file.reset_mock()
