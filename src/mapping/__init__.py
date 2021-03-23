# -*- coding: utf-8 -*-

from models import *

from .record_adapters import BaseAdapter
from .record_adapters import CategoryAdapter
from .record_adapters import JargonAdapter
from .record_adapters import JargonGroupAdapter

from .record_mappers import BaseRecordMapper
from .record_mappers import DummyRecordMapper
from .record_mappers import FieldRecordMapper

from .record_routes import APIRoute
from .record_routes import CATEGORY_ROUTE
from .record_routes import GROUP_ROUTE
from .record_routes import JARGON_ROUTE


ADAPTERS = {
    TYPE_CATEGORY.name: CategoryAdapter,
    TYPE_GROUP.name: JargonGroupAdapter,
    TYPE_JARGON.name: JargonAdapter,
}

API_ROUTES = {
    TYPE_CATEGORY.name: CATEGORY_ROUTE,
    TYPE_GROUP.name: GROUP_ROUTE,
    TYPE_JARGON.name: JARGON_ROUTE,
}


def select_adapter(type_name: str) -> BaseAdapter:
    """
    Selects the corresponding record adapter given a data model type
    :param type_name: name of the data model
    :return: record adapter
    """

    try:
        adapter_cls = ADAPTERS[type_name]
        adapter_obj = adapter_cls()  # type: ignore
        return adapter_obj
    except KeyError:
        raise ValueError(f"Invalid model type: {type_name}")


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
