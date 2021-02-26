# -*- coding: utf-8 -*-

import json
from abc import ABC
from abc import abstractmethod
from typing import Generator
from typing import List

from ..models import DiffEntry


class BaseDiffParser(ABC):
    """ Interface for parsing the data file diff results """

    @abstractmethod
    def get_creation_entries(self, file_path: str) -> Generator:
        """
        Parses a given difference file to extract the creation entries
        :param file_path: path to the diff file
        :return: list of creation entries
        """

        raise NotImplementedError()

    @abstractmethod
    def get_deletion_entries(self, file_path: str) -> Generator:
        """
        Parses a given difference file to extract the deletion entries
        :param file_path: path to the diff file
        :return: list of deletion entries
        """

        raise NotImplementedError()

    @abstractmethod
    def get_edition_entries(self, file_path: str) -> Generator:
        """
        Parses a given difference file to extract the edition entries
        :param file_path: path to the diff file
        :return: list of edition entries
        """

        raise NotImplementedError()


class JDDiffParser(BaseDiffParser):
    """
    Class parsing the JSON differences generated by the JD tool
    Reference: https://github.com/josephburnett/jd
    """

    def __init__(self):
        """ Initializes the JSON diff parser """

        self.parse_func = json.loads

    def _parse_diff_lines(self, lines: List[str]) -> DiffEntry:
        """
        Parses a given list of JSON diff file lines
        :param lines: lines from the JSON diff file
        :return: object representing a JSON diff entry
        """

        path, prev, post = [], None, None

        for line in lines:
            if line.startswith("@"):
                path = self.parse_func(line[2:])
                continue
            if line.startswith("-"):
                prev = self.parse_func(line[2:])
                continue
            if line.startswith("+"):
                post = self.parse_func(line[2:])
                continue

        return DiffEntry(path, prev, post)

    def _parse_diff_file(self, file_path: str) -> Generator:
        """
        Opens the provided JSON diff file and parses its entries
        :param file_path: path to the JSON diff file
        :return: JSON difference entry
        """

        unparsed_lines = []  # type: ignore
        with open(file_path, "r") as diff_file:

            for line in diff_file.readlines():
                is_new_entry = line.startswith("@")
                is_not_empty = len(unparsed_lines) > 0

                if is_new_entry and is_not_empty:
                    yield self._parse_diff_lines(unparsed_lines)
                    unparsed_lines = []

                unparsed_lines.append(line)

            # VIP: return the last entry
            yield self._parse_diff_lines(unparsed_lines)

    def get_creation_entries(self, file_path: str) -> Generator:
        """
        Parses a given JSON difference file to extract the creation entries
        :param file_path: path to the JSON diff file
        :return: list of creation entries
        """

        diff_entries = self._parse_diff_file(file_path)
        post_entries = (e for e in diff_entries if e.is_creation())

        return post_entries

    def get_deletion_entries(self, file_path: str) -> Generator:
        """
        Parses a given JSON difference file to extract the deletion entries
        :param file_path: path to the JSON diff file
        :return: list of deletion entries
        """

        diff_entries = self._parse_diff_file(file_path)
        prev_entries = (e for e in diff_entries if e.is_deletion())

        return prev_entries

    def get_edition_entries(self, file_path: str) -> Generator:
        """
        Parses a given JSON difference file to extract the edition entries
        :param file_path: path to the JSON diff file
        :return: list of edition entries
        """

        diff_entries = self._parse_diff_file(file_path)
        edit_entries = (e for e in diff_entries if e.is_edition())

        return edit_entries
