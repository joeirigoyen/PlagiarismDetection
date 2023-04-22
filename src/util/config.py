# Initialize dictionary
import json
from pathlib import Path


class ConfigManager:

    whitelist = ["PROJECT_ROOT", "SRC", "UTIL", "RESOURCES", "ORIGINAL_FILES", "SUSPICIOUS_FILES", "GROUND_TRUTH"]

    def __init__(self, json_path: str | Path = None):
        # Initialize dictionary
        try:
            self.__initialize_env_vars(json_path)
        except FileNotFoundError:
            self.__initialize_env_vars(None)

    def __initialize_env_vars(self, json_path: str | None) -> None:
        if json_path is not None:
            self.from_json(json_path)
        else:
            self.__env_vars = {
                "PROJECT_ROOT": Path.cwd().parent.parent
            }
            # Add global environment variables
            self.__env_vars.update({"SRC": self.__env_vars.get("PROJECT_ROOT") / "src"})
            self.__env_vars.update({"UTIL": self.__env_vars.get("SRC") / "util"})
            self.__env_vars.update({"RESOURCES": self.__env_vars.get("PROJECT_ROOT") / "resources"})
            self.__env_vars.update({"ORIGINAL_FILES": self.__env_vars.get("RESOURCES") / "original"})
            self.__env_vars.update({"SUSPICIOUS_FILES": self.__env_vars.get("RESOURCES") / "suspicious"})
            self.__env_vars.update({"GROUND_TRUTH": self.__env_vars.get("RESOURCES") / "groundTruth.json"})

    def __update_attr(self, key: str, value: str | Path) -> None:
        self.__env_vars[key] = value

    def from_json(self, json_path: str | Path) -> None:
        # Load json file
        if Path(json_path).is_file() and Path(json_path).exists():
            with open(json_path, "r") as f:
                json_data = json.load(f)
            # Update dictionary
            for key, value in json_data.items():
                if key in self.whitelist:
                    self.__update_attr(key, value)
        else:
            raise FileNotFoundError(f"File {json_path} not found.")

    def get(self, key: str) -> str | Path:
        return Path(self.__env_vars.get(key))
