"""
Module for unit tests for plagcheck

Author: Rebeca Rojas Pérez A01751192
Created: 4 May 2023
"""
import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.cli.commands.plagcheck import do_get_top_candidates
from src.entities.textdata import TextData
from src.util.file_manager import FileManager


class TestDoGetTopCandidates(unittest.TestCase):

    @patch('pathlib.Path.iterdir')
    def test_returns_top_n_candidates(self, mock_iterdir):
        """
        Unit test for the return_top_n_candidates() function in the plagcheck code
        """
        file_path = "../resources/original/original_001.txt"

        suspicious_obj = TextData(Path(file_path).read_text())
        params = {"pre_distance": "cosine"}

        result = do_get_top_candidates(10, suspicious_obj, params)

        # Assert
        self.assertTrue(len(result) == 0)


    @patch('pathlib.Path.iterdir')
    def test_returns_empty_list_if_no_files(self, mock_iterdir):
        """
        Unit test for the return_top_n_candidates() function with an empty file list as parameter
        in the plagcheck code
        """
        # Arrange
        mock_iterdir.return_value = []
        n = 2
        suspicious_obj = MagicMock()
        params = {"pre_distance": MagicMock()}

        # Act
        result = do_get_top_candidates(n, suspicious_obj, params)

        # Assert
        self.assertListEqual(result, [])


