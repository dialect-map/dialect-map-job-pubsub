# -*- coding: utf-8 -*-

import logging
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import List
from typing import Set

from dialect_map_gcp import DiffMessage

logger = logging.getLogger()


class BaseMessageOperator(ABC):
    """Interface for the data types operator classes"""

    @abstractmethod
    def get_default_records(self, message: DiffMessage) -> List[dict]:
        """
        Gets the default version of the message contained data records
        :param message: records wrapping message
        :return: raw records
        """

        raise NotImplementedError()

    @abstractmethod
    def get_enriched_records(self, message: DiffMessage) -> List[dict]:
        """
        Gets the enriched version of the message contained data records
        :param message: records wrapping message
        :return: enriched records
        """

        raise NotImplementedError()


class DiffMessageOperator(ABC):
    """Message operator for the DiffMessage objects"""

    def __init__(self, propagated_fields: Set[str] = None):
        """
        Initializes the message operator with a list of fields to propagate
        :param propagated_fields: message fields to propagate to the records
        """

        if propagated_fields is None:
            propagated_fields = {"created_at"}

        self._check_msg_fields(propagated_fields)
        self.propagated_fields = propagated_fields

    @staticmethod
    def _check_msg_fields(message_fields: Set[str]) -> None:
        """
        Checks that the specified fields are present in the message
        :param message_fields: message fields to propagate to the records
        """

        # Checks the provided fields are a subset
        assert message_fields <= DiffMessage.fields()

    @staticmethod
    def _prune_nested(record: dict) -> dict:
        """
        Prunes every nested data structure out of a data record
        :param record: data record to prune
        :return: pruned data record
        """

        return {
            key: val
            for key, val in record.items()
            if type(val) is not dict and type(val) is not list
        }

    def _unfold_nested(self, val: Any) -> List[dict]:
        """
        Unfolds a nested containing message into its different records
        :param val: nested message value
        :return: list of nested records
        """

        records = []

        if type(val) is dict:
            records += [val]
            records += [obj for elem in val.values() for obj in self._unfold_nested(elem)]
        if type(val) is list:
            records += [obj for elem in val for obj in self._unfold_nested(elem)]

        return records

    def _extract_records(self, message: DiffMessage) -> List[dict]:
        """
        Extracts the record data objects from a wrapping message
        :param message: record wrapping message
        :return: record objects
        """

        if message.is_creation:
            records = self._unfold_nested(message.value_post)
            records = [self._prune_nested(record) for record in records]
            return records
        if message.is_edition:
            return [message.container]

        raise ValueError("Invalid message structure")

    def get_default_records(self, message: DiffMessage) -> List[dict]:
        """
        Gets the default version of the message contained data records
        :param message: records wrapping message
        :return: raw records
        """

        return self._extract_records(message)

    def get_enriched_records(self, message: DiffMessage) -> List[dict]:
        """
        Gets the enriched version of the message contained data records
        :param message: records wrapping message
        :return: enriched records
        """

        # Augment records with specific message fields
        message_attrs = {field: getattr(message, field) for field in self.propagated_fields}
        revised_records = [{**record, **message_attrs} for record in self._extract_records(message)]

        return revised_records
