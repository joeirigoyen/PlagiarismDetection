import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
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
