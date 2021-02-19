# -*- coding: utf-8 -*-

from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass
class JSONDiffEntry:
    """
    Data class for the JSON diff entries

    Class attributes:
        path: path to the JSON entry that was changed
        value_prev: entry value before the change
        value_post: entry value after the change
    """

    path: list
    value_prev: Any = field(default=None)
    value_post: Any = field(default=None)

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
