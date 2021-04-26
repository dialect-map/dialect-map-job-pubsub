# -*- coding: utf-8 -*-

import logging
from abc import ABC
from abc import abstractmethod
from typing import Dict

from dialect_map_io import APIRoute
from dialect_map_io import RestOutputAPI

from mapping import BaseAdapter

logger = logging.getLogger()


class BaseAPIOperator(ABC):
    """Interface for the data object operator classes"""

    @abstractmethod
    def create_record(self, record_data: dict, record_type: str):
        """
        Performs the creation of a record on a REST API
        :param record_data: data record
        :param record_type: data record type
        """

        raise NotImplementedError()

    @abstractmethod
    def archive_record(self, record_data: dict, record_type: str):
        """
        Performs the archival of a record on a REST API
        :param record_data: data record
        :param record_type: data record type
        """

        raise NotImplementedError()


class DialectMapOperator(BaseAPIOperator):
    """Class to operate on the Dialect map API"""

    def __init__(
        self,
        api_object: RestOutputAPI,
        api_routes: Dict[str, APIRoute],
        adapters: Dict[str, BaseAdapter],
    ):
        """
        Initializes the Dialect map API operator object
        :param api_object: Dialect map API instantiated object
        :param api_routes: Dialect map API routes dictionary
        :param adapters: data record adapters dictionary
        """

        self.api_object = api_object
        self.api_routes = api_routes
        self.adapters = adapters

    def _create(self, api_path: str, record: dict) -> None:
        """
        Creates the given record on the specified API path
        :param api_path: API path to send the data
        :param record: data record to send
        """

        try:
            self.api_object.create_record(api_path, record)
        except Exception as error:
            logger.error(f"Cannot create record: {record}")
            logger.error(f"Error: {error}")
            raise

    def _archive(self, api_path: str, record_id: str) -> None:
        """
        Archives an existing record on the specified API path
        :param api_path: API path to patch
        :param record_id: record ID to patch
        """

        try:
            self.api_object.archive_record(f"{api_path}/{record_id}")
        except Exception as error:
            logger.error(f"Cannot archive record with ID: {record_id}")
            logger.error(f"Error: {error}")
            raise

    def create_record(self, record_data: dict, record_type: str) -> None:
        """
        Performs the creation of a record on a REST API
        :param record_data: data record
        :param record_type: data record type
        """

        record_route = self.api_routes[record_type]
        record_adapt = self.adapters[record_type]

        self._create(
            record_route.api_path,
            record_adapt.adapt_fields(record_data),
        )

    def archive_record(self, record_data: dict, record_type: str) -> None:
        """
        Performs the archival of a record on a REST API
        :param record_data: data record
        :param record_type: data record type
        """

        record_route = self.api_routes[record_type]

        self._archive(
            record_route.api_path,
            record_data["id"],
        )
