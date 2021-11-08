# -*- coding: utf-8 -*-

from .record_mapping import BaseRecordMapper
from .record_mapping import SchemaRecordMapper

from .record_routes import CATEGORY_ROUTE
from .record_routes import GROUP_ROUTE
from .record_routes import JARGON_ROUTE


ROUTES = {
    "categories.json": [
        CATEGORY_ROUTE,
    ],
    "jargons.json": [
        GROUP_ROUTE,
        JARGON_ROUTE,
    ],
}


def init_all_mappers() -> dict:
    """
    Initializes all data file mappers
    :return: dictionary file - mapper
    """

    return {file_name: SchemaRecordMapper(routes) for file_name, routes in ROUTES.items()}
