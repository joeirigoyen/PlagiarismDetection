import json
from pathlib import Path


def get_user_input(prompt: str, retry: bool = True) -> str | None:
    input_path = None
    while input_path != 'q':
        # Get input file
        input_path = input(prompt)
        # Check if file exists
        if input_path == 'q':
            return None
        if not Path(input_path).exists():
            print("The provided path doesn't exist.\n")
            if not retry:
                return None
            continue
        return input_path


def load_from_json_file(json_path: str | Path) -> dict:
    file_content = None
    try:
        file_content = json.load(open(json_path, "r"))
    except FileNotFoundError:
        print(f"File {json_path} not found.")
    except json.decoder.JSONDecodeError:
        print(f"File {json_path} is not a valid json file.")
    return file_content
