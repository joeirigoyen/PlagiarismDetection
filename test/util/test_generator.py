"""
Module to perform unit tests for the generator code.

Author: Rebeca Rojas Pérez
Date: May 3rd 2023
"""

import os
import shutil
import tempfile
import unittest
from src.util.generator import Generator

class TestGenerator(unittest.TestCase):


    def setUp(self):
        """
        Initial setup to perform unit tests in the Generator class
        """
        self.generator = Generator()
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """
        Restore changes after unit tests are finished in the Generator  Class.
        """
        shutil.rmtree(self.test_dir)

    def test_random_string(self):
        """
        Unit test for the random_string() function in the Generator Class.
        """
        # Test that the method returns a string
        self.assertIsInstance(self.generator.random_string(), str)

        # Test that the method returns a string of the expected length
        expected_len = 10
        result = self.generator.random_string(max_len=expected_len)
        self.assertEqual(len(result), expected_len)

    def test_generate_random_texts(self):
        """
        Unit test for the generate_random_texts() function in the Generator Class.
        """
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
        """
        Unit test for the generate_random_texts() function with an invalid directory as parameter
        in the Generator Class.
        """
        # Arrange
        invalid_dir = "invalid/directory.txt"
        number_of_files = 5
        prefix = "test_file"

        # Act
        self.assertRaises(ValueError, self.generator.generate_random_texts, invalid_dir, 5)

        # Assert
        self.assertFalse(os.path.exists(invalid_dir))

