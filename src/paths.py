# -*- coding: utf-8 -*-

from pathlib import Path


PROJECT_PATH = Path(__file__).parent.parent


def build_data_path(file_name: str) -> str:
    """
    Build the path to the desired static data file
    :param file_name: name of the static data file
    :return: file path
    """

    # fmt: off
    data_path = PROJECT_PATH \
        .joinpath("modules") \
        .joinpath("dialect-map-data") \
        .joinpath("data") \
        .joinpath(file_name)

    # fmt: on
    return str(data_path)


def build_diff_path(file_name: str) -> str:
    """
    Build the path to the desired static data file diff
    :param file_name: name of the static data file diff
    :return: file path
    """

    # fmt: off
    diff_path = PROJECT_PATH \
        .joinpath(".update") \
        .joinpath("diff") \
        .joinpath(file_name)

    # fmt: on
    return str(diff_path)
