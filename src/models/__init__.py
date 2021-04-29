# -*- coding: utf-8 -*-

import re

from .data_file import DataFile
from .data_type import DataType


##########################
####### Data types #######
##########################

TYPE_CATEGORY = DataType(
    name="Category",
    regex=re.compile(r"^\w+(-\w+)?(\.\w+)?(-\w+)?$"),
)

TYPE_GROUP = DataType(
    name="JargonGroup",
    regex=re.compile(r"^group-\d+$"),
)

TYPE_JARGON = DataType(
    name="Jargon",
    regex=re.compile(r"^group-\d+-jargon-\d+$"),
)

DATA_TYPES = [
    TYPE_CATEGORY,
    TYPE_GROUP,
    TYPE_JARGON,
]


##########################
####### Data files #######
##########################

FILE_CATEGORY = DataFile(
    name="categories.json",
    types=[TYPE_CATEGORY],
)

FILE_JARGONS = DataFile(
    name="jargons.json",
    types=[TYPE_JARGON, TYPE_GROUP],
)

DATA_FILES = [
    FILE_CATEGORY,
    FILE_JARGONS,
]
