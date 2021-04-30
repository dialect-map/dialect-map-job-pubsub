# -*- coding: utf-8 -*-

import pytest

from src.mapping import FieldRecordMapper
from src.mapping import TYPE_CATEGORY
from src.mapping import TYPE_JARGON
from src.mapping import TYPE_GROUP


class TestCategoryFieldMapper:
    """Class to group all category field mapper tests"""

    @pytest.fixture(scope="class")
    def mapper(self):
        """
        Data record to data model name mapper
        :return: record mapper object
        """

        return FieldRecordMapper("prop", [TYPE_CATEGORY])

    def test_field_mapper_valid(self, mapper: FieldRecordMapper):
        """
        Test the correct type mapping of valid samples
        :param mapper: record mapper object
        """

        assert mapper.infer_type({"prop": "top"}) == TYPE_CATEGORY.name
        assert mapper.infer_type({"prop": "top-suffix"}) == TYPE_CATEGORY.name
        assert mapper.infer_type({"prop": "top-suffix.low"}) == TYPE_CATEGORY.name
        assert mapper.infer_type({"prop": "top-suffix.low-suffix"}) == TYPE_CATEGORY.name

    def test_field_mapper_error(self, mapper: FieldRecordMapper):
        """
        Test the correct type mapping of valid samples
        :param mapper: record mapper object
        """

        assert pytest.raises(ValueError, mapper.infer_type, {"prop": "wrong."})
        assert pytest.raises(ValueError, mapper.infer_type, {"prop": "wrong.wrong-"})
        assert pytest.raises(ValueError, mapper.infer_type, {"prop": "wrong-wrong."})


class TestJargonFieldMapper:
    """Class to group all jargon types field mapper tests"""

    @pytest.fixture(scope="class")
    def mapper(self):
        """
        Data record to data model name mapper
        :return: record mapper object
        """

        return FieldRecordMapper("prop", [TYPE_JARGON, TYPE_GROUP])

    def test_field_mapper_valid(self, mapper: FieldRecordMapper):
        """
        Test the correct type mapping of valid samples
        :param mapper: record mapper object
        """

        assert mapper.infer_type({"prop": "group-1"}) == TYPE_GROUP.name
        assert mapper.infer_type({"prop": "group-123"}) == TYPE_GROUP.name
        assert mapper.infer_type({"prop": "group-1-jargon-1"}) == TYPE_JARGON.name
        assert mapper.infer_type({"prop": "group-1-jargon-123"}) == TYPE_JARGON.name

    def test_field_mapper_error(self, mapper: FieldRecordMapper):
        """
        Test the correct type mapping of valid samples
        :param mapper: record mapper object
        """

        assert pytest.raises(ValueError, mapper.infer_type, {"prop": "wrong"})
        assert pytest.raises(ValueError, mapper.infer_type, {"prop": "groups"})
        assert pytest.raises(ValueError, mapper.infer_type, {"prop": "group-X"})
        assert pytest.raises(ValueError, mapper.infer_type, {"prop": "group-1-jargon-X"})
