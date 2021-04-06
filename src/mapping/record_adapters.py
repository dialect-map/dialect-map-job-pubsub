# -*- coding: utf-8 -*-

import re
from abc import ABC
from abc import abstractmethod


class BaseAdapter(ABC):
    """ Interface for the data model adapter classes """

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
            "description": values["name"],
            "created_at": values["created_at"],
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

    @staticmethod
    def extract_words_num(jargon_term: str) -> int:
        """
        Extracts the jargon term number of words.
        :param jargon_term: jargon term
        :return: number of words
        """

        return len(jargon_term.split())

    def adapt_fields(self, values: dict) -> dict:
        """
        Adapts a given data record to its standardized set of fields
        :param values: entry data fields
        :return: standardized record
        """

        jargon_id = values["id"]
        jargon_term = values["name"]

        group_id = self.extract_group_id(jargon_id)
        words_num = self.extract_words_num(jargon_term)

        return {
            "group_id": group_id,
            "num_words": words_num,
            "jargon_id": jargon_id,
            "jargon_term": jargon_term,
            "jargon_regex": values["regex"],
            "archived": values["archived"],
            "created_at": values["created_at"],
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
            "created_at": values["created_at"],
        }
