# -*- coding: utf-8 -*-

import logging
from abc import ABC
from abc import abstractmethod

from dialect_map_io import DialectMapAPI

from .routes import select_route
from ..mapping import select_adapter
from ..mapping import BaseRecordMapper
from ..parsers import BaseDataParser
from ..parsers import BaseDiffParser
from ..parsers import JSONDataParser
from ..parsers import JDDiffParser

logger = logging.getLogger()


class BaseOperator(ABC):
    """ Interface for the data object operator classes """

    @abstractmethod
    def create_records(self, data_path: str, diff_path: str) -> int:
        """
        Transform creation diff file entries into API operations
        :param data_path: path to the data file
        :param diff_path: path to the diff file
        :return: number of inserted records
        """

        raise NotImplementedError()

    @abstractmethod
    def archive_records(self, data_path: str, diff_path: str) -> int:
        """
        Transform edition diff file entries into API operations
        :param data_path: path to the data file
        :param diff_path: path to the diff file
        :return: number of archived records
        """

        raise NotImplementedError()


class DialectMapOperator(BaseOperator):
    """ Class to operate on Dialect map data objects """

    def __init__(
        self,
        api_object: DialectMapAPI,
        type_mapper: BaseRecordMapper,
        data_parser: BaseDataParser = None,
        diff_parser: BaseDiffParser = None,
    ):
        """
        Initializes the Dialect map operator object
        :param api_object: Dialect map API instantiated object
        :param type_mapper: diff entries to data types mapper
        :param data_parser: parser to read data files contents (optional)
        :param diff_parser: parser to read data files diffs (optional)
        """

        if data_parser is None:
            data_parser = JSONDataParser()
        if diff_parser is None:
            diff_parser = JDDiffParser()

        self.api_object = api_object
        self.data_parser = data_parser
        self.diff_parser = diff_parser
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

    def create_records(self, data_path: str, diff_path: str) -> int:
        """
        Transform creation diff file entries into API operations
        :param data_path: path to the data file
        :param diff_path: path to the diff file
        :return: number of inserted records
        """

        entries = self.diff_parser.get_creation_entries(diff_path)
        created = 0

        for entry in entries:
            model = self.type_mapper.infer_type(entry.value_post)

            record_api = select_route(model)
            record_ada = select_adapter(model)
            record_obj = self.data_parser.get_object(data_path, entry.object_path)
            record_obj = record_ada.adapt_fields(record_obj)

            created += self._create(record_api.api_path, record_obj)

        return created

    def archive_records(self, data_path: str, diff_path: str) -> int:
        """
        Transform edition diff file entries into API operations
        :param data_path: path to the data file
        :param diff_path: path to the diff file
        :return: number of archived records
        """

        entries = self.diff_parser.get_edition_entries(diff_path)
        archived = 0

        for entry in entries:
            model = self.type_mapper.infer_type(entry.value_post)

            record_api = select_route(model)
            record_obj = self.data_parser.get_object(data_path, entry.object_path)
            record_id = record_obj["id"]

            archived += self._archive(record_api.api_path, record_id)

        return archived
