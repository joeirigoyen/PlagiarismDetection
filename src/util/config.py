# Initialize dictionary
import json
import os

from pathlib import Path


class ConfigManager:

    whitelist = ["PROJECT_ROOT", "SRC", "UTIL", "RESOURCES", "ORIGINAL_FILES", "SUSPICIOUS_FILES", "GROUND_TRUTH"]

    def __init__(self, json_path: str | Path = None):
        # Initialize dictionary
        self.__root = Path(__file__).parent.parent.parent.absolute() if not json_path else None
        self.__env_vars = {}
        try:
            self.__env_vars = self.__initialize_env_vars(json_path)
        except FileNotFoundError:
            self.__env_vars = self.__initialize_env_vars(None, self.__root)

    @property
    def env_vars(self) -> dict:
        return self.__env_vars

    def __initialize_env_vars(self, json_path: str | None) -> dict:
        if json_path is not None:
            self.__from_json(json_path)
        else:
            self.__env_vars = {
                "PROJECT_ROOT": self.__root
            }
            # Add global environment variables
            self.__env_vars.update({"SRC": self.__env_vars.get("PROJECT_ROOT") / "src"})
            self.__env_vars.update({"UTIL": self.__env_vars.get("SRC") / "util"})
            self.__env_vars.update({"RESOURCES": self.__env_vars.get("PROJECT_ROOT") / "resources"})
            self.__env_vars.update({"ORIGINAL_FILES": self.__env_vars.get("RESOURCES") / "original"})
            self.__env_vars.update({"SUSPICIOUS_FILES": self.__env_vars.get("RESOURCES") / "suspicious"})
            self.__env_vars.update({"GROUND_TRUTH": self.__env_vars.get("RESOURCES") / "groundTruth.json"})
        return self.__env_vars

    def __update_attr(self, key: str, value: str | Path) -> None:
        self.__env_vars[key] = value

    def __from_json(self, json_path: str | Path) -> None:
        # Load json file
        if json_path and Path(json_path).is_file() and Path(json_path).exists():
            with open(json_path, "r") as f:
                json_data = json.load(f)
            # Update dictionary
            for key, value in json_data.items():
                if key in self.whitelist:
                    if key == "PROJECT_ROOT":
                        self.__root = value
                    self.__update_attr(key, value)
        else:
            raise FileNotFoundError(f"File {json_path} not found.")

    def get(self, key: str) -> str | Path | None:
        path = self.__env_vars.get(key)
        return Path(self.__env_vars.get(key)) if path else None
