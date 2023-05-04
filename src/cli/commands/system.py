from pathlib import Path
from src.util.config import ConfigManager


def do_exit(params: dict[str, str]) -> None:
    """
    Exits the program.

    :param params: The parameters of the command. (Unused but kept for consistency).
    """
    print("Exiting CLI...")
    exit(0)


def do_change_source(params: dict[str, str]) -> None:
    """
    Changes the ML model dataset in order to retrain it.
    :param params: The parameters of the command.
    """
    config = ConfigManager()
    key, value = params.get("key"), Path(params.get("value"))
    config.update_env_var(key, value)
    print(f"New value for {key}: {config.get(key)}")
