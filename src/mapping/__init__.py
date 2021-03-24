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


TYPE_ADAPTERS = {
    TYPE_CATEGORY.name: CategoryAdapter,
    TYPE_GROUP.name: JargonGroupAdapter,
    TYPE_JARGON.name: JargonAdapter,
}

FILE_MAPPERS = {
    FILE_CATEGORY.name: FieldRecordMapper,
    FILE_JARGONS.name: FieldRecordMapper,
}

API_ROUTES = {
    TYPE_CATEGORY.name: CATEGORY_ROUTE,
    TYPE_GROUP.name: GROUP_ROUTE,
    TYPE_JARGON.name: JARGON_ROUTE,
}


def get_route(type_name: str) -> APIRoute:
    """
    Selects the corresponding API route given a data type name
    :param type_name: name of the data type
    :return: API route object
    """

    try:
        return API_ROUTES[type_name]
    except KeyError:
        raise ValueError(f"Invalid model type: {type_name}")


def init_adapter(type_name: str) -> BaseAdapter:
    """
    Selects the corresponding record adapter given a data type name
    :param type_name: name of the data type
    :return: record adapter
    """

    try:
        adapter_cls = TYPE_ADAPTERS[type_name]
        adapter_obj = adapter_cls()  # type: ignore
        return adapter_obj
    except KeyError:
        raise ValueError(f"Invalid model type: {type_name}")


def init_mapper(source_file: str, **kwargs) -> BaseRecordMapper:
    """
    Selects the corresponding file mapper given a source file
    :param source_file: source file from where the diff comes
    :return: file mapper
    """

    try:
        mapper_cls = FILE_MAPPERS[source_file]
        mapper_obj = mapper_cls(**kwargs)  # type: ignore
        return mapper_obj
    except KeyError:
        raise ValueError(f"Invalid source file: {source_file}")
    except TypeError:
        raise ValueError(f"Invalid keyword args: {kwargs}")
