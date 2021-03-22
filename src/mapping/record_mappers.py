# -*- coding: utf-8 -*-

import re

from abc import ABC
from abc import abstractmethod
from typing import List

from models import DataType


class BaseRecordMapper(ABC):
    """ Interface for data record type mapping classes """

    @abstractmethod
    def infer_type(self, record: dict) -> str:
        """
        Infers the corresponding data model type from a given data record
        :param record: data record to infer the type from
        :return: corresponding model type
        """

        raise NotImplementedError()


class DummyRecordMapper(BaseRecordMapper):
    """ Dummy record type mapper """

    def __init__(self, expected_type: str):
        """
        Initializes the dummy mapper
        :param expected_type: mapped type to return
        """

        self.expected_type = expected_type

    def infer_type(self, record: dict) -> str:
        """
        Infers the corresponding data model type from a given data record
        :param record: data record to infer the type from
        :return: corresponding model type
        """

        return self.expected_type


class FieldRecordMapper(BaseRecordMapper):
    """ Field based record type mapper """

    def __init__(self, field: str, types: List[DataType]):
        """
        Initializes the mapper
        :param field: field to apply the mapping patterns on
        :param types: list of pattern mappable data types
        """

        self.field = field
        self.types = types

    def infer_type(self, record: dict) -> str:
        """
        Infers the corresponding data model type from a given data record
        :param record: data record to infer the type from
        :return: corresponding model type
        """

        value = record[self.field]

        for data_type in self.types:
            if re.match(data_type.regex, value):
                return data_type.name

        raise ValueError(f"No corresponding type. Record: {record}")
