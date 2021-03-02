# -*- coding: utf-8 -*-

from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass
class DiffEntry:
    """
    Data class for the data files diff entries

    Class attributes:
        path: data file path to the entry that was changed
        value_prev: entry value before the change
        value_post: entry value after the change
    """

    path: list
    value_prev: Any = field(default=None)
    value_post: Any = field(default=None)

    @property
    def object_path(self) -> list:
        """
        Path to the object containing an edited field
        :return: list of keys / indexes
        """

        if self.is_edition():
            return self.path[:-1]
        else:
            return self.path[:]

    def is_creation(self) -> bool:
        """
        Checks if the diff entry correspond to a creation
        :return: whether it is a creation
        """

        return self.value_prev is None and self.value_post is not None

    def is_deletion(self) -> bool:
        """
        Checks if the diff entry correspond to a deletion
        :return: whether it is a deletion
        """

        return self.value_prev is not None and self.value_post is None

    def is_edition(self) -> bool:
        """
        Checks if the diff entry correspond to an edition
        :return: whether it is a edition
        """

        return self.value_prev is not None and self.value_post is not None
