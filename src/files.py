# -*- coding: utf-8 -*-

from mapping.record_types import *

from typing import List
from typing import NamedTuple


class DataFile(NamedTuple):
    """ Named tuple for the data file names and mappable data types """

    name: str
    types: List[DataType]


DATA_FILES = [
    DataFile(
        name="categories.json",
        types=[TYPE_CATEGORY],
    ),
    DataFile(
        name="jargons.json",
        types=[TYPE_JARGON, TYPE_GROUP],
    ),
]
