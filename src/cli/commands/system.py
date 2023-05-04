def do_exit(params: dict[str, str]) -> None:
    """
    Exits the program.

    :param params: The parameters of the command. (Unused but kept for consistency).
    """
    print("Exiting CLI...")
    exit(0)


def do_change_dataset(params: dict[str, str]) -> None:
    """
    Changes the ML model dataset in order to retrain it.
    :param params: The parameters of the command.
    """
    pass
