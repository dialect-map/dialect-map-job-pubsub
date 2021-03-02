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
        """ Post-init trigger to check regex correctness """

        assert self.regex.pattern.startswith("^")
        assert self.regex.pattern.endswith("$")

    @property
    def id_regex(self) -> Pattern:
        """
        Identifier regular expression for the ID field
        :return: regular expression
        """

        return self.regex
