from unittest import mock

from field import Field, Integer
from model import Model

import pytest


@pytest.mark.asyncio
async def test_to_dict():
    model = {
        "field": Field(field_type=Integer())
    }
    model = Model(model)
    with mock.patch("field.Field.to_dict") as to_dict_mock:
        to_dict_mock.return_value = {"field_type": '<class "Integer">'}
        response = await model.to_dict()
        assert response == {
            "field": {"field_type": '<class "Integer">'}
        }


@pytest.mark.asyncio
async def test_from_dict():
    model = {
        "field": {"field_type": '<class "Integer">'}
    }
    with mock.patch("field.Field.from_str") as from_str_mock:
        from_str_mock.return_value = Field(field_type=Integer)
        response = await Model.from_dict(model)
        assert isinstance(response, Model)
        assert isinstance(response.model["field"], Field)
