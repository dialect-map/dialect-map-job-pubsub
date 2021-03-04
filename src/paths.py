# -*- coding: utf-8 -*-

import shutil

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


def build_differ_file_path(file_name: str, check: bool = False) -> str:
    """
    Build the path to the desired static data file diff
    :param file_name: name of the static data file diff
    :param check: whether to check that the path exists (optional)
    :return: file path
    """

    # fmt: off
    diff_path = PROJECT_PATH \
        .joinpath(UPDATES_DIR) \
        .joinpath("diff") \
        .joinpath(file_name)

    # fmt: on
    if check and not diff_path.is_file():
        raise OSError(f"There is no diff file: {file_name}")

    return str(diff_path)


def build_module_file_path(file_name: str, check: bool = False) -> str:
    """
    Build the path to the desired static data file
    :param file_name: name of the static data file
    :param check: whether to check that the path exists (optional)
    :return: file path
    """

    # fmt: off
    data_path = PROJECT_PATH \
        .joinpath(MODULES_DIR) \
        .joinpath("dialect-map-data") \
        .joinpath("data") \
        .joinpath(file_name)

    # fmt: on
    if check and not data_path.is_file():
        raise OSError(f"There is no data file: {file_name}")

    return str(data_path)


def safe_file_copy(source_file: str, target_file: str) -> None:
    """
    Copies the specified file creating intermediate directories
    :param source_file: source file path
    :param target_file: target file path
    """

    target_folder = Path(target_file).parent
    target_folder.mkdir(exist_ok=True)

    shutil.copy(source_file, target_folder)
