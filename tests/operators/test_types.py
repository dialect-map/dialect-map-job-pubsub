# -*- coding: utf-8 -*-

import pytest
from datetime import datetime
from typing import Any

from dialect_map_io import DiffMessage
from src.mapping import DummyRecordMapper
from src.operators import DiffTypeOperator


DUMMY_DIFF_CONTAINER = {"id": "test"}
DUMMY_DIFF_FIELD_NAME = "field_name"
DUMMY_DIFF_SOURCE_FILE = "file.json"
DUMMY_DIFF_CREATED_AT = datetime.utcnow()


def create_dummy_diff(value_prev: Any, value_post: Any, source_file: str = "") -> DiffMessage:
    """
    Creates a dummy DiffMessage to use during the tests
    :param value_prev: diff previous value
    :param value_post: diff posterior value
    :param source_file: file name where the change have been originated
    :return: DiffMessage object
    """

    if len(source_file) == 0:
        source_file = DUMMY_DIFF_SOURCE_FILE

    return DiffMessage(
        DUMMY_DIFF_CONTAINER,
        DUMMY_DIFF_FIELD_NAME,
        value_prev,
        value_post,
        source_file,
        DUMMY_DIFF_CREATED_AT,
    )


@pytest.fixture(scope="module")
def diff_operator() -> DiffTypeOperator:
    """
    Diff messages type operator
    :return: initialized operator
    """

    dummy_mapper_a = DummyRecordMapper("type_A")
    dummy_mapper_b = DummyRecordMapper("type_B")

    return DiffTypeOperator(
        {
            "file_A.json": dummy_mapper_a,
            "file_B.json": dummy_mapper_b,
        }
    )


def test_operator_creation_record_objs(diff_operator: DiffTypeOperator):
    """
    Tests the correct extraction of record objects from a creation diff
    :param diff_operator: initialized operator
    """

    prev = None
    nested_post = [{"id": "A"}, {"id": "B"}]
    holder_post = {"id": "example", "count": 5, "list": nested_post}

    diff = create_dummy_diff(prev, holder_post)
    objs = diff_operator.get_record_objs(diff)

    assert objs == [holder_post, *nested_post]


def test_operator_edition_record_objs(diff_operator: DiffTypeOperator):
    """
    Tests the correct extraction of record objects from a edition diff
    :param diff_operator: initialized operator
    """

    prev = {"id": "example", "count": 5, "archived": False}
    post = {"id": "example", "count": 5, "archived": True}

    diff = create_dummy_diff(prev, post)
    objs = diff_operator.get_record_objs(diff)

    assert objs == [DUMMY_DIFF_CONTAINER]


def test_operator_record_type(diff_operator: DiffTypeOperator):
    """
    Tests the correct extraction of record type from a diff
    :param diff_operator: initialized operator
    """

    data = {"id": "example", "count": 5}
    type_a = diff_operator.get_record_type(data, "file_A.json")
    type_b = diff_operator.get_record_type(data, "file_B.json")

    assert type_a == "type_A"
    assert type_b == "type_B"
