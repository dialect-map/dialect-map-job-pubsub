# -*- coding: utf-8 -*-

import logging

from abc import ABC
from abc import abstractmethod

from dialect_map_io import RestOutputAPI
from dialect_map_schemas import APIRoute

logger = logging.getLogger()


class BaseAPIOperator(ABC):
    """Interface for the data object operator classes"""

    @abstractmethod
    def create_record(self, record_data: dict, record_route: APIRoute):
        """
        Performs the creation of a record on a REST API
        :param record_data: data record
        :param record_route: data record route
        """

        raise NotImplementedError()

    @abstractmethod
    def archive_record(self, record_data: dict, record_route: APIRoute):
        """
        Performs the archival of a record on a REST API
        :param record_data: data record
        :param record_route: data record route
        """

        raise NotImplementedError()


class DialectMapOperator(BaseAPIOperator):
    """Class to operate on the Dialect map API"""

    def __init__(self, api_object: RestOutputAPI):
        """
        Initializes the Dialect map API operator object
        :param api_object: Dialect map API instantiated object
        """

        self.api_object = api_object

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

    def create_record(self, record_data: dict, record_route: APIRoute) -> None:
        """
        Performs the creation of a record on a REST API
        :param record_data: data record
        :param record_route: data record route
        """

        record_schema = record_route.model_schema()
        record_data = record_schema.load(record_data)

        self._create(
            record_route.api_path,
            record_schema.dump(record_data),
        )

    def archive_record(self, record_data: dict, record_route: APIRoute) -> None:
        """
        Performs the archival of a record on a REST API
        :param record_data: data record
        :param record_route: data record route
        """

        record_schema = record_route.model_schema()
        schema_id_field = record_schema.schema_id

        self._archive(
            record_route.api_path,
            record_data[schema_id_field],
        )
