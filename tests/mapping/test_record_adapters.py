# -*- coding: utf-8 -*-

import pytest

from src.mapping import CategoryAdapter
from src.mapping import JargonAdapter
from src.mapping import JargonGroupAdapter


def test_category_adapter_valid():
    """ Test the adaptation of valid category samples """

    sample = {"id": "example", "description": "example"}
    record = CategoryAdapter().adapt_fields(sample)
    fields = record.keys()

    assert "category_id" in fields
    assert "description" in fields
    assert "created_at" in fields


def test_category_adapter_invalid():
    """ Test the adaptation of invalid category samples """

    assert pytest.raises(KeyError, CategoryAdapter().adapt_fields, {})


def test_jargon_adapter_valid():
    """ Test the adaptation of valid jargon samples """

    sample = {
        "id": "group-1-jargon-1",
        "name": "name",
        "regex": "[Ee]xample",
        "archived": False,
    }

    record = JargonAdapter().adapt_fields(sample)
    fields = record.keys()

    assert "jargon_id" in fields
    assert "jargon_str" in fields
    assert "jargon_regex" in fields
    assert "group_id" in fields
    assert "archived" in fields
    assert "created_at" in fields

    assert record["group_id"] == "group-1"


def test_jargon_adapter_invalid():
    """ Test the adaptation of invalid jargon samples """

    sample = {
        "id": "wrong-id",
        "name": "name",
        "regex": "[Ee]xample",
        "archived": False,
    }

    assert pytest.raises(AssertionError, JargonAdapter().adapt_fields, sample)


def test_group_adapter_valid():
    """ Test the adaptation of valid jargon group samples """

    sample = {
        "id": "group-1",
        "description": "example",
        "archived": False,
        "terms": [],
    }

    record = JargonGroupAdapter().adapt_fields(sample)
    fields = record.keys()

    assert "group_id" in fields
    assert "description" in fields
    assert "archived" in fields
    assert "created_at" in fields


def test_group_adapter_invalid():
    """ Test the adaptation of invalid jargon samples """

    assert pytest.raises(KeyError, JargonGroupAdapter().adapt_fields, {})
