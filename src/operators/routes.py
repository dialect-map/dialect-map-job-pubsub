# -*- coding: utf-8 -*-

from dialect_map_io import APIRoute
from dialect_map_io import DM_CATEGORY_ROUTE
from dialect_map_io import DM_JARGON_ROUTE
from dialect_map_io import DM_JARGON_GROUP_ROUTE

from mapping import TYPE_CATEGORY
from mapping import TYPE_GROUP
from mapping import TYPE_JARGON


API_ROUTES = {
    TYPE_CATEGORY.name: DM_CATEGORY_ROUTE,
    TYPE_GROUP.name: DM_JARGON_GROUP_ROUTE,
    TYPE_JARGON.name: DM_JARGON_ROUTE,
}


def select_route(type_name: str) -> APIRoute:
    """
    Selects the corresponding API route given a data model type
    :param type_name: name of the data model
    :return: API route object
    """

    try:
        return API_ROUTES[type_name]
    except KeyError:
        raise ValueError(f"Invalid model type: {type_name}")
