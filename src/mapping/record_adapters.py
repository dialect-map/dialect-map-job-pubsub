# -*- coding: utf-8 -*-

import re

from abc import ABC
from abc import abstractmethod
from datetime import datetime


class BaseAdapter(ABC):
    """ Interface for the data model adapter classes """

    @property
    def datetime_now(self) -> str:
        """
        Returns the current date-time in ISO format
        :return: current date-time in ISO format
        """

        return datetime.now().isoformat(sep=" ", timespec="seconds")

    @abstractmethod
    def adapt_fields(self, values: dict) -> dict:
        """
        Adapts a given data record to its standardized set of fields
        :param values: entry data fields
        :return: standardized record
        """

        raise NotImplementedError()


class CategoryAdapter(BaseAdapter):
    """ Category data model adapter class """

    def adapt_fields(self, values: dict) -> dict:
        """
        Adapts a given data record to its standardized set of fields
        :param values: entry data fields
        :return: standardized record
        """

        return {
            "category_id": values["id"],
            "description": values["description"],
            "created_at": self.datetime_now,
        }


class JargonAdapter(BaseAdapter):
    """ Jargon data model adapter class """

    @staticmethod
    def extract_group_id(jargon_id: str) -> str:
        """
        Extracts the jargon group ID from the jargon ID itself.
        :param jargon_id: jargon ID values
        :return: group ID
        """

        matches = re.search(r"^(group-\d+)-jargon-\d+$", jargon_id)
        assert matches is not None, f"Invalid jargon ID: {jargon_id}"
        return matches.group(1)

    def adapt_fields(self, values: dict) -> dict:
        """
        Adapts a given data record to its standardized set of fields
        :param values: entry data fields
        :return: standardized record
        """

        jargon_id = values["id"]
        group_id = self.extract_group_id(jargon_id)

        return {
            "group_id": group_id,
            "jargon_id": jargon_id,
            "jargon_str": values["name"],
            "jargon_regex": values["regex"],
            "archived": values["archived"],
            "created_at": self.datetime_now,
        }


class JargonGroupAdapter(BaseAdapter):
    """ Jargon data model adapter class """

    def adapt_fields(self, values: dict) -> dict:
        """
        Adapts a given data record to its standardized set of fields
        :param values: entry data fields
        :return: standardized record
        """

        return {
            "group_id": values["id"],
            "description": values["description"],
            "archived": values["archived"],
            "created_at": self.datetime_now,
        }
