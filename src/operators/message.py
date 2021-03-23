# -*- coding: utf-8 -*-

import logging
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import List

from dialect_map_io import DiffMessage

logger = logging.getLogger()


class BaseMessageOperator(ABC):
    """ Interface for the data types operator classes """

    @abstractmethod
    def get_msg_records(self, message: object) -> List[dict]:
        """
        Extracts the record data objects wrapping message
        :param message: record wrapping message
        :return: record objects
        """

        raise NotImplementedError()


class DiffMessageOperator(ABC):
    """ Message operator for the DiffMessage objects """

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

    def get_msg_records(self, message: DiffMessage) -> List[dict]:
        """
        Extracts the record data objects from a wrapping message
        :param message: record wrapping message
        :return: record objects
        """

        if message.is_creation():
            return self._unfold_nested(message.value_post)

        if message.is_edition():
            return [message.container]

        raise ValueError("Invalid message structure")
