# -*- coding: utf-8 -*-

from models import *

from .record_mappers import BaseRecordMapper
from .record_mappers import DummyRecordMapper
from .record_mappers import FieldRecordMapper

from .record_routes import CATEGORY_ROUTE
from .record_routes import GROUP_ROUTE
from .record_routes import JARGON_ROUTE


FILE_MAPPERS = {
    FILE_CATEGORY.name: FieldRecordMapper,
    FILE_JARGONS.name: FieldRecordMapper,
}

API_ROUTES = {
    TYPE_CATEGORY.name: CATEGORY_ROUTE,
    TYPE_GROUP.name: GROUP_ROUTE,
    TYPE_JARGON.name: JARGON_ROUTE,
}


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
