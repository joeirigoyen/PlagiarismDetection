import subprocess

from pathlib import Path


def init_globals() -> dict:
    # Initialize dictionary
    global_variables = {
        "PROJECT_ROOT": Path.cwd().parent.parent
    }
    # Add global environment variables
    global_variables["SRC"] = global_variables["PROJECT_ROOT"] / "src"
    global_variables["UTIL"] = global_variables["SRC"] / "util"
    global_variables["RESOURCES"] = global_variables["PROJECT_ROOT"] / "resources"
    global_variables["ORIGINAL_FILES"] = global_variables["RESOURCES"] / "original"
    global_variables["SUSPICIOUS_FILES"] = global_variables["RESOURCES"] / "suspicious"
    return global_variables


print(init_globals())
