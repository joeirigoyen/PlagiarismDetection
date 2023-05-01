"""
Module to handle the command line interface.

Author: Youthan Irigoyen
Date: April 24th, 2023
"""

import commands.system as syscli

from src.cli.ioutils import perr

PREFIX = "user> "
COMMANDS = {
    "system": {
        "exit": syscli.do_exit
    }
}


def parse_params(params: list[str]) -> dict[str, str]:
    """
    Parses the parameters and returns a dictionary of the parameters.

    :param params: The parameters to parse.
    :return: The dictionary of parameters.
    """
    params_dict = {}
    for param in params:
        key, value = param.split("=")
        params_dict[key] = value
    return params_dict


def parse_line(line: str) -> tuple[str, str, dict[str, str]]:
    """
    Parses the line and returns the command and the arguments.

    :param line: The line to parse.
    :return: The command and the arguments.
    """
    line_args = line.split()
    if len(line_args) < 2:
        raise ValueError("Invalid command. Try again.")
    command, sub_command = line_args[0], line_args[1]
    params = parse_params(line_args[2:]) if len(line_args) > 2 else {}
    return command, sub_command, params


def do_command(line: str) -> None:
    """
    Gets the command from the user and executes it.
    :return: None
    """
    try:
        command, sub_command, params = parse_line(line)
        if len(params):
            COMMANDS[command][sub_command](params)
        else:
            COMMANDS[command][sub_command]()
    except ValueError:
        perr("Invalid syntax. Try using <command> <sub-command> <params>.")
    except KeyError:
        perr("Invalid command. Try again.")


def run() -> None:
    """
    Runs the CLI.
    :return: None
    """
    while True:
        line = input(PREFIX)
        do_command(line)


if __name__ == "__main__":
    run()