"""
Module to handle the plagiarism check commands.

Author: Raúl Youthan Irigoyen Osorio
Date: May 3rd, 2023
"""
from heapq import nlargest
from pathlib import Path
from src.cli.ioutils import perr
from src.entities.nlpmodel import NLPModel
from src.entities.textdata import TextData
from src.util.config import ConfigManager as Cm
from src.util.file_manager import FileManager as Fm


PLAGCHECK_METHODS = ["nlp", "deep-learning"]
config = Cm()


def do_get_top_candidates(n: int, suspicious_obj: TextData, params: dict) -> list[tuple]:
    """
    Get the top n candidates from the source directory.
    :param params: The parameters provided by the user.
    :param suspicious_obj: The suspicious text content.
    :param n: Number of candidates to get.
    :return: List of the top n candidates' paths.
    """
    scores = []
    for f in Path(config.get("ORIGINAL_FILES")).iterdir():
        if f.is_file():
            text_data = TextData(Fm.read_file(f))
            scores.append((f, suspicious_obj.get_distance(text_data, params.get("pre_distance"))))
    return nlargest(n, scores, key=lambda x: x[1])


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

    # Parse input file content to TextData
    file_content = Fm.read_file(Path(input_file))
    text_data = TextData(file_content)

    # Get top 10 candidates
    candidates = do_get_top_candidates(10, text_data, params)

    # Perform the plagiarism check according to the selected method
    match method:
        case "nlp":
            nlp_model = NLPModel(TextData(file_content), config.get("ORIGINAL_FILES"))
            nlp_model.check(params)
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
