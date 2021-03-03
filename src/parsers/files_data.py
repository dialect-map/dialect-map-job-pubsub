# -*- coding: utf-8 -*-

import json
from abc import ABC
from abc import abstractmethod
from typing import Any


class BaseDataParser(ABC):
    """ Interface for parsing the data files """

    @abstractmethod
    def get_content(self, file_path: str) -> dict:
        """
        Parses a given data files and extracts its structured content
        :param file_path: path to the data file
        :return: whole data structure
        """

        raise NotImplementedError()

    @abstractmethod
    def get_object(self, file_path: str, obj_path: list) -> Any:
        """
        Parses a given data files and the path indicated data object
        :param file_path: path to the data file
        :param obj_path: path within the data structure
        :return: specific data object
        """

        raise NotImplementedError()


class JSONDataParser(BaseDataParser):
    """ Class parsing the JSON data files """

    def __init__(self):
        """ Initializes the JSON data parser """

        self.parse_func = json.loads

    def get_content(self, file_path: str) -> dict:
        """
        Parses a given data file and extracts its structured content
        :param file_path: path to the data file
        :return: whole data structure
        """

        with open(file_path, "r") as data_file:
            content = data_file.read()
            content = self.parse_func(content)

        return content

    def get_object(self, file_path: str, obj_path: list) -> Any:
        """
        Parses a given data file and the path indicated data object
        :param file_path: path to the data file
        :param obj_path: path within the data structure
        :return: specific data object
        """

        data_obj = self.get_content(file_path)

        for step in obj_path:
            data_obj = data_obj[step]

        return data_obj
