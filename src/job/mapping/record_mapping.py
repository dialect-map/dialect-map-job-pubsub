# -*- coding: utf-8 -*-

import logging

from abc import ABC
from abc import abstractmethod
from typing import List
from typing import override

from dialect_map_schemas import APIRoute
from dialect_map_schemas import SchemaError

logger = logging.getLogger()


class BaseRecordMapper(ABC):
    """Interface for data record type mapping classes"""

    @abstractmethod
    def infer_route(self, record: dict) -> APIRoute:
        """
        Infers the corresponding API route from a given data record
        :param record: data record to infer the API route from
        :return: the data record route
        """

        raise NotImplementedError()


class SchemaRecordMapper(BaseRecordMapper):
    """Schema based record type mapper"""

    def __init__(self, routes: List[APIRoute]):
        """
        Initializes the mapper
        :param routes: list of schema mappable routes
        """

        self.routes = routes

    @override
    def infer_route(self, record: dict) -> APIRoute:
        """
        Infers the corresponding API route from a given data record
        :param record: data record to infer the API route from
        :return: the data record route
        """

        for route in self.routes:
            schema = route.schema()

            try:
                schema.load(record)
            except SchemaError:
                logger.info(f"Incompatible schema {schema.name}")
            else:
                return route

        raise ValueError(f"No matching schema. Record: {record}")
