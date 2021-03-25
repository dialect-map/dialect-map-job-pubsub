# -*- coding: utf-8 -*-

import pytest
from datetime import datetime
from typing import Any

from dialect_map_io import DiffMessage
from src.operators import DiffMessageOperator


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
def diff_operator() -> DiffMessageOperator:
    """
    Diff messages type operator
    :return: initialized operator
    """

    return DiffMessageOperator(propagated_fields=[])


def test_operator_creation_record_objs(diff_operator: DiffMessageOperator):
    """
    Tests the correct extraction of record objects from a creation diff
    :param diff_operator: initialized operator
    """

    prev = None
    nested_post = [{"id": "A"}, {"id": "B"}]
    holder_post = {"id": "example", "count": 5, "list": nested_post}

    diff = create_dummy_diff(prev, holder_post)
    objs = diff_operator.get_default_records(diff)

    assert objs == [holder_post, *nested_post]


def test_operator_edition_record_objs(diff_operator: DiffMessageOperator):
    """
    Tests the correct extraction of record objects from a edition diff
    :param diff_operator: initialized operator
    """

    prev = {"id": "example", "count": 5, "archived": False}
    post = {"id": "example", "count": 5, "archived": True}

    diff = create_dummy_diff(prev, post)
    objs = diff_operator.get_default_records(diff)

    assert objs == [DUMMY_DIFF_CONTAINER]
