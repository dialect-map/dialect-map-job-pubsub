# -*- coding: utf-8 -*-

import logging
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import List
from mapping import BaseRecordMapper

from dialect_map_io import DiffMessage

logger = logging.getLogger()


class BaseTypeOperator(ABC):
    """ Interface for the data types operator classes """

    @abstractmethod
    def get_record_objs(self, struct: object) -> List[dict]:
        """
        Extracts the record data objects from a wrapping structure
        :param struct: record objects wrapping structure
        :return: record objects
        """

        raise NotImplementedError()

    @abstractmethod
    def get_record_type(self, record_data: dict, source_file: str) -> str:
        """
        Infers a record type from its data fields
        :param record_data: record data fields
        :param source_file: source file from where the diff comes
        :return: record type
        """

        raise NotImplementedError()


class DiffTypeOperator(ABC):
    """ Type operator for the DiffMessage objects """

    def __init__(self, mappers: Dict[str, BaseRecordMapper]):
        """
        Initializes the type DiffMessage type operator
        :param mappers: dictionary of source data files to mappers
        """

        self.type_mappers = mappers

    def _unfold_nested(self, val: Any) -> List[dict]:
        """
        Unfolds a nested containing record into its different objects
        :param val: data record value
        :return: list of nested objects
        """

        objects = []

        if type(val) is dict:
            objects += [val]
            objects += [obj for elem in val.values() for obj in self._unfold_nested(elem)]
        if type(val) is list:
            objects += [obj for elem in val for obj in self._unfold_nested(elem)]

        return objects

    def get_record_objs(self, struct: DiffMessage) -> List[dict]:
        """
        Extracts the record data objects from a wrapping structure
        :param struct: record objects wrapping structure
        :return: record objects
        """

        if struct.is_creation():
            return self._unfold_nested(struct.value_post)

        if struct.is_edition():
            return [struct.container]

        raise ValueError("Invalid message structure")

    def get_record_type(self, record_data: dict, source_file: str) -> str:
        """
        Infers a record type from its data fields
        :param record_data: record data fields
        :param source_file: source file from where the diff comes
        :return: record type
        """

        try:
            mapper = self.type_mappers[source_file]
        except KeyError:
            logger.error(f"Unknown source file: {source_file}")
            logger.error("The provided source file has no mapper")
            raise
        else:
            return mapper.infer_type(record_data)
