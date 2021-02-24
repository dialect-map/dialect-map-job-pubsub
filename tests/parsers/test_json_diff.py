# -*- coding: utf-8 -*-

import pytest

from src.parsers import JDDiffParser
from ..__paths import DIFFS_FOLDER


@pytest.fixture(scope="module")
def json_diff_parser() -> JDDiffParser:
    """
    JSON diff parser based on the JD tool
    :return: diff parser object
    """

    return JDDiffParser()


def test_creation_entries(json_diff_parser: JDDiffParser):
    """
    Test the correct parsing and identification of creation entries
    :param json_diff_parser: diff parsing object
    """

    diff_file = DIFFS_FOLDER.joinpath("jd_patch.txt")
    diff_file = str(diff_file)

    entries = json_diff_parser.get_creation_entries(diff_file)
    entries = list(entries)

    assert len(entries) == 1
    assert entries[0].path == [26, "terms", 2]


def test_deletion_entries(json_diff_parser: JDDiffParser):
    """
    Test the correct parsing and identification of deletion entries
    :param json_diff_parser: diff parsing object
    """

    diff_file = DIFFS_FOLDER.joinpath("jd_patch.txt")
    diff_file = str(diff_file)

    entries = json_diff_parser.get_deletion_entries(diff_file)
    entries = list(entries)

    assert len(entries) == 1
    assert entries[0].path == [29, "terms", 1]


def test_edition_entries(json_diff_parser: JDDiffParser):
    """
    Test the correct parsing and identification of edition entries
    :param json_diff_parser: diff parsing object
    """

    diff_file = DIFFS_FOLDER.joinpath("jd_patch.txt")
    diff_file = str(diff_file)

    entries = json_diff_parser.get_edition_entries(diff_file)
    entries = list(entries)

    assert len(entries) == 2
    assert entries[0].path == [0, "terms", 1, "archived"]
    assert entries[1].path == [2, "archived"]
