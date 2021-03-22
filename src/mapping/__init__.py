# -*- coding: utf-8 -*-

from models import *

from .record_adapters import BaseAdapter
from .record_adapters import CategoryAdapter
from .record_adapters import JargonAdapter
from .record_adapters import JargonGroupAdapter

from .record_mappers import BaseRecordMapper
from .record_mappers import DummyRecordMapper
from .record_mappers import FieldRecordMapper


ADAPTERS = {
    TYPE_CATEGORY.name: CategoryAdapter,
    TYPE_GROUP.name: JargonGroupAdapter,
    TYPE_JARGON.name: JargonAdapter,
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
