import unittest
import json
from tempfile import NamedTemporaryFile
from pathlib import Path
from src.util.ioutils import load_from_json_file


class TestMyModule(unittest.TestCase):

    def test_load_from_json_file(self):
        # Test valid JSON file
        with NamedTemporaryFile(mode='w', delete=False) as f:
            json.dump({'test': 1}, f)
        self.assertEqual(load_from_json_file(f.name), {'test': 1})
        Path(f.name).unlink()

        # Test non-existent file
        self.assertIsNone(load_from_json_file('invalid_file.json'))

        # Test invalid JSON file
        with NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('{"test": 1')
        self.assertIsNone(load_from_json_file(f.name))
        Path(f.name).unlink()