# -*- coding: utf-8 -*-

import re

from .data_file import DataFile
from .data_type import DataType


##########################
####### Data types #######
##########################

TYPE_CATEGORY = DataType(
    name="Category",
    regex=re.compile(
        r"^"
        r"("
        r"(astro)|(cond)|(cs)|(econ)|(eess)|(gr)|(hep)|"
        r"(math)|(nlin)|(nucl)|(physics)|(q)|(quant)|(stat)"
        r")"
        r"(-\w+)?"
        r"(\.\w+)?"
        r"(-\w+)?"
        r"$"
    ),
)

TYPE_GROUP = DataType(
    name="JargonGroup",
    regex=re.compile(r"^group-\d+$"),
)

TYPE_JARGON = DataType(
    name="Jargon",
    regex=re.compile(r"^group-\d+-jargon-\d+$"),
)


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
