# -*- coding: utf-8 -*-

import logging
from abc import ABC
from abc import abstractmethod

from dialect_map_io import DialectMapAPI

from mapping import select_adapter
from mapping import select_route
from mapping import BaseRecordMapper

logger = logging.getLogger()


class BaseOperator(ABC):
    """ Interface for the data object operator classes """

    @abstractmethod
    def create_records(self, messages: list) -> int:
        """
        Transform received data-diff messages into DB records
        :param messages: list of data-diff messages
        :return: number of inserted records
        """

        raise NotImplementedError()

    @abstractmethod
    def archive_records(self, messages: list) -> int:
        """
        Transform received data-diff messages into archived DB records
        :param messages: list of data-diff messages
        :return: number of archived records
        """

        raise NotImplementedError()


class DialectMapOperator(BaseOperator):
    """ Class to operate on Dialect map data objects """

    def __init__(self, api_object: DialectMapAPI, type_mapper: BaseRecordMapper):
        """
        Initializes the Dialect map operator object
        :param api_object: Dialect map API instantiated object
        :param type_mapper: diff entries to data types mapper
        """

        self.api_object = api_object
        self.type_mapper = type_mapper

    def _create(self, api_path: str, record: dict) -> int:
        """
        Creates a DB record returning the number of successful creations
        :param api_path: API path to send the data
        :param record: data record to send
        :return: 1 | 0
        """

        try:
            self.api_object.create_record(api_path, record)
            return 1
        except Exception as error:
            logger.error(f"Cannot create record: {record}")
            logger.error(f"Error: {error}")
            return 0

    def _archive(self, api_path: str, record_id: str) -> int:
        """
        Archives a DB record returning the number of successful archival
        :param api_path: API path to patch
        :param record_id: record ID to patch
        :return: 1 | 0
        """

        try:
            self.api_object.archive_record(f"{api_path}/{record_id}")
            return 1
        except Exception as error:
            logger.error(f"Cannot archive record with ID: {record_id}")
            logger.error(f"Error: {error}")
            return 0

    def create_records(self, messages: list) -> int:
        """
        Transform received data-diff messages into DB records
        :param messages: list of data-diff messages
        :return: number of inserted records
        """

        created = 0

        for message in messages:
            record_type = self.type_mapper.infer_type(message)
            record_route = select_route(record_type)
            record_adapt = select_adapter(record_type)

            data_obj = record_adapt.adapt_fields(message)
            created += self._create(record_route.api_path, data_obj)

        return created

    def archive_records(self, messages: list) -> int:
        """
        Transform received data-diff messages into archived DB records
        :param messages: list of data-diff messages
        :return: number of archived records
        """

        archived = 0

        for message in messages:
            record_type = self.type_mapper.infer_type(message)
            record_route = select_route(record_type)

            archived += self._archive(record_route.api_path, message["id"])

        return archived
