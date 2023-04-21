import os
import shutil
import tempfile
import unittest
from src.util.generator import Generator
from src.util.file_manager import  FileManager

class TestGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = Generator()
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_random_string(self):
        # Test that the method returns a string
        self.assertIsInstance(self.generator.random_string(), str)

        # Test that the method returns a string of the expected length
        expected_len = 10
        result = self.generator.random_string(max_len=expected_len)
        self.assertEqual(len(result), expected_len)

    def test_generate_random_texts(self):
        # Arrange
        number_of_files = 5
        prefix = "test_file"

        # Act
        self.generator.generate_random_texts(self.test_dir, number_of_files, prefix)

        # Assert
        for i in range(number_of_files):
            curr_filename = f"{prefix}_{i:03d}.txt"
            curr_file_path = os.path.join(self.test_dir, curr_filename)
            self.assertTrue(os.path.isfile(curr_file_path))

    def test_generate_random_texts_invalid_parent_directory(self):
        # Arrange
        invalid_dir = "/invalid/directory"
        number_of_files = 5
        prefix = "test_file"

        # Act
        with self.assertRaises(FileNotFoundError):
            self.generator.generate_random_texts(invalid_dir, number_of_files, prefix)

        # Assert
        self.assertFalse(os.path.exists(invalid_dir))