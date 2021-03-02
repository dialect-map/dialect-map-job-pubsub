# -*- coding: utf-8 -*-

import pytest

from src.mapping.record_mappers import BaseRecordMapper
from src.mapping.record_mappers import PropertyRecordMapper
from src.mapping.record_types import *


@pytest.fixture(scope="module")
def mapper() -> BaseRecordMapper:
    """
    Data record to data model name mapper
    :return: record mapper object
    """

    mapper = PropertyRecordMapper()
    mapper.mappings = [TYPE_CATEGORY, TYPE_JARGON, TYPE_GROUP]
    mapper.property = "prop"

    return mapper


@pytest.mark.parametrize(
    ["sample", "expected"],
    [
        ({"prop": "cs.AI"}, TYPE_CATEGORY.name),
        ({"prop": "group-1"}, TYPE_GROUP.name),
        ({"prop": "group-123"}, TYPE_GROUP.name),
        ({"prop": "group-1-jargon-1"}, TYPE_JARGON.name),
        ({"prop": "group-1-jargon-123"}, TYPE_JARGON.name),
    ],
)
def test_prop_mapper_infer(mapper: PropertyRecordMapper, sample: dict, expected: str):
    """
    Test the correct type mapping of valid samples
    :param mapper: record mapper object
    :param sample: record sample dictionary
    :param expected: record corresponding data type
    """

    assert mapper.infer_type(sample) == expected


@pytest.mark.parametrize(
    "sample",
    [
        {"prop": "wrong"},
        {"prop": "groups"},
        {"prop": "group-X"},
        {"prop": "group-1-jargon-X"},
    ],
)
def test_prop_mapper_infer_invalid(mapper: PropertyRecordMapper, sample: dict):
    """
    Test the correct exception raised when invalid samples
    :param mapper: record mapper object
    :param sample: record sample dictionary
    """

    assert pytest.raises(ValueError, mapper.infer_type, sample)
