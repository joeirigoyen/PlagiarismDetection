import unittest
from pathlib import Path
from src.util.config import ConfigManager

class TestConfigManager(unittest.TestCase):

    def test_initialize_env_vars_without_json_file(self):
        # Test that initialization without JSON file works as expected
        config = ConfigManager()
        self.assertEqual(config.get("PROJECT_ROOT"), Path.cwd().parent.parent)
        self.assertEqual(config.get("SRC"), Path.cwd().parent.parent / "src")
        self.assertEqual(config.get("UTIL"), Path.cwd().parent.parent / "src/util")
        self.assertEqual(config.get("RESOURCES"), Path.cwd().parent.parent / "resources")
        self.assertEqual(config.get("ORIGINAL_FILES"), Path.cwd().parent.parent / "resources/original")
        self.assertEqual(config.get("SUSPICIOUS_FILES"), Path.cwd().parent.parent / "resources/suspicious")
        self.assertEqual(config.get("GROUND_TRUTH"), Path.cwd().parent.parent / "resources/groundTruth.json")

    def test_from_json_with_invalid_file_path(self):
        # Test that exception is raised if invalid file path is given
        config = ConfigManager("invalid_path.json")
        self.assertEqual(len(config.whitelist), len(config.env_vars.keys()))


    def test_from_json_with_valid_file_path_and_invalid_key(self):
        # Test that invalid key is ignored when loading JSON file
        config = ConfigManager("test_config.json")
        self.assertEqual(config.get("INVALID_KEY"), None)

    def test_get_with_valid_key(self):
        # Test that get method returns expected value for valid key
        config = ConfigManager()
        self.assertEqual(config.get("PROJECT_ROOT"), Path.cwd().parent.parent)

    def test_get_with_invalid_key(self):
        # Test that get method returns None for invalid key
        config = ConfigManager()
        self.assertEqual(config.get("INVALID_KEY"), None)

