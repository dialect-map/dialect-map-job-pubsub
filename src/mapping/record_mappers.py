# -*- coding: utf-8 -*-

import re

from abc import ABC
from abc import abstractmethod
from typing import List

from .record_types import TYPE_CATEGORY
from .record_types import TYPE_JARGON
from .record_types import TYPE_GROUP
from ..models import DataType


class BaseRecordMapper(ABC):
    """ Interface for data API route mapping classes """

    @abstractmethod
    def infer_type(self, record: dict) -> str:
        """
        Infers the corresponding data model type from a given data record
        :param record: data record to infer the type from
        :return: corresponding model type
        """

        raise NotImplementedError()


class PropertyRecordMapper(BaseRecordMapper):
    """
    Model type mapper that uses a certain data record property

    Class attributes:
        mappings: list of mappings between patterns and model types
        property: field to be subject of the patterns
    """

    mappings: List[DataType]
    property: str

    def infer_type(self, record: dict) -> str:
        """
        Infers the corresponding data model type from a given data record
        :param record: data record to infer the type from
        :return: corresponding model type
        """

        value = record[self.property]

        for mapping in self.mappings:
            if re.match(mapping.id_regex, value):
                return mapping.name

        raise ValueError(f"No corresponding type. Record: {record}")


class IDRecordMapper(PropertyRecordMapper):
    """ Model type mapper that uses the data entry ID """

    mappings = [TYPE_CATEGORY, TYPE_GROUP, TYPE_JARGON]
    property = "id"
