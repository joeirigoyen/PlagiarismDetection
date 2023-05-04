"""

"""

from src.cli.ioutils import perr
from src.util.file_manager import FileManager as Fm

PLAGCHECK_METHODS = ["nlp", "deep-learning"]


def do_check_file(params: dict[str, str]) -> None:
    """
    Perform a plagiarism check on a file.
    :return:
    """
    # Check that the input file is valid
    result = None
    input_file = params.get("input_file")
    if not input_file or not Fm.validate_file(input_file, create=False):
        perr("Invalid input file. Try again.")
        return result
    # Check that the selected method is valid
    method = params.get("method") or "nlp"
    if method not in PLAGCHECK_METHODS:
        perr("Invalid method. Try again.")
        return result
    # Perform the plagiarism check according to the selected method
    match params:
        case "nlp":
            # TODO: Implement NLP method
            pass
        case "deep-learning":
            # TODO: Implement deep learning method
            pass
    return result


def do_check_dir(params: dict[str, str]) -> None:
    """
    Perform a plagiarism check on a whole directory (only .txt files).
    :return:
    """
    pass


def do_plot_last(params: dict[str, str]) -> None:
    """
    Perform a plagiarism check on a file.
    :return:
    """
    pass
