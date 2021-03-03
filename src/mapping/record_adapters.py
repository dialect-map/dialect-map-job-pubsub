# -*- coding: utf-8 -*-

import re

from abc import ABC
from abc import abstractmethod
from datetime import datetime


class BaseAdapter(ABC):
    """ Interface for the data model adapter classes """

    @staticmethod
    @abstractmethod
    def adapt_fields(values: dict) -> dict:
        """
        Adapts a given data record to its standardized set of fields
        :param values: entry data fields
        :return: standardized record
        """

        raise NotImplementedError()


class CategoryAdapter(BaseAdapter):
    """ Category data model adapter class """

    @staticmethod
    def adapt_fields(values: dict) -> dict:
        """
        Adapts a given data record to its standardized set of fields
        :param values: entry data fields
        :return: standardized record
        """

        return {
            "category_id": values["id"],
            "description": values["description"],
            "created_at": datetime.now(),
        }


class JargonAdapter(BaseAdapter):
    """ Jargon data model adapter class """

    @staticmethod
    def _extract_group_id(jargon_id: str) -> str:
        """
        Extracts the jargon group ID from the jargon ID itself.
        :param jargon_id: jargon ID values
        :return: group ID
        """

        matches = re.search(r"group-\d+", jargon_id)
        if matches is None:
            raise ValueError(f"Invalid jargon ID: {jargon_id}")

        return matches.group(0)

    @staticmethod
    def adapt_fields(values: dict) -> dict:
        """
        Adapts a given data record to its standardized set of fields
        :param values: entry data fields
        :return: standardized record
        """

        jargon_id = values["id"]
        group_id = JargonAdapter._extract_group_id(jargon_id)

        return {
            "group_id": group_id,
            "jargon_id": jargon_id,
            "jargon_str": values["name"],
            "jargon_regex": values["regex"],
            "archived": values["archived"],
            "created_at": datetime.now(),
        }


class JargonGroupAdapter(BaseAdapter):
    """ Jargon data model adapter class """

    @staticmethod
    def adapt_fields(values: dict) -> dict:
        """
        Adapts a given data record to its standardized set of fields
        :param values: entry data fields
        :return: standardized record
        """

        return {
            "group_id": values["id"],
            "description": values["description"],
            "archived": values["archived"],
            "created_at": datetime.now(),
        }
