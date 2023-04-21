import os
import tempfile
import unittest
from pathlib import Path
import src.util.file_manager as fm


class Testfm(unittest.TestCase):
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
        self.assertEqual(fm.convert_to_path(file_path_str), file_path)
        self.assertEqual(fm.convert_to_path(file_path), file_path)

    def test_exists(self):
        file = fm(self.temp_path / "existing_file.txt")
        self.assertTrue(file.exists())

        file = fm(self.temp_path / "non_existing_file.txt")
        self.assertFalse(file.exists())

    def test_create_file(self):
        file = fm(self.temp_path / "new_file.txt")
        self.assertFalse(file.exists())
        file.create()
        self.assertTrue(file.exists())
        self.assertTrue(os.path.isfile(str(file._file)))
        os.remove(str(file._file))

    def test_create_directory(self):
        dir = fm(self.temp_path / "new_directory")
        self.assertFalse(dir.exists())
        dir.create()
        self.assertTrue(dir.exists())
        self.assertTrue(os.path.isdir(str(dir._file)))