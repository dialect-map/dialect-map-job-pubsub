# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Pattern


@dataclass
class DataType:
    """
    Data class for the data type mappings

    Class attributes:
        name: name of the data type
        regex: regular expression to identify the data type
    """

    name: str
    regex: Pattern

    def __post_init__(self):
        """Post-init trigger to check regex correctness"""

        assert self.regex.pattern.startswith("^")
        assert self.regex.pattern.endswith("$")
