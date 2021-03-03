# -*- coding: utf-8 -*-

from pathlib import Path


PROJECT_PATH = Path(__file__).parent.parent
MODULES_DIR = "modules"
UPDATES_DIR = ".update"


def build_backup_file_path(file_name: str) -> str:
    """
    Build the path to the desired static data file backup
    :param file_name: name of the static data file backup
    :return: file path
    """

    # fmt: off
    backup_path = PROJECT_PATH \
        .joinpath(UPDATES_DIR) \
        .joinpath("old") \
        .joinpath(file_name)

    # fmt: on
    return str(backup_path)


def build_differ_file_path(file_name: str) -> str:
    """
    Build the path to the desired static data file diff
    :param file_name: name of the static data file diff
    :return: file path
    """

    # fmt: off
    diff_path = PROJECT_PATH \
        .joinpath(UPDATES_DIR) \
        .joinpath("diff") \
        .joinpath(file_name)

    # fmt: on
    return str(diff_path)


def build_module_file_path(file_name: str) -> str:
    """
    Build the path to the desired static data file
    :param file_name: name of the static data file
    :return: file path
    """

    # fmt: off
    data_path = PROJECT_PATH \
        .joinpath(MODULES_DIR) \
        .joinpath("dialect-map-data") \
        .joinpath("data") \
        .joinpath(file_name)

    # fmt: on
    return str(data_path)
