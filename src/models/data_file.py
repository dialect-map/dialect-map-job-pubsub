# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List

from .data_type import DataType


@dataclass
class DataFile:
    """
    Data class for the data file mappable data types

    Class attributes:
        name: name of the data file
        types: data types found in the file
    """

    name: str
    types: List[DataType]
