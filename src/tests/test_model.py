from model import Model
from pydantic import Field

import pytest


@pytest.mark.asyncio
async def test_to_dict():

    class SampleModel(Model):
        field_1: int = Field(unique_id=123, column_type="int4")
        field_2: str

    expected = {
        "name": "SampleModel",
        "fields": {
            "field_1": {
                "unique_id": 123,
                "column_type": "int4"
            },
            "field_2": {
                "unique_id": None,
                "column_type": "text"
            }
        }
    }
    result = SampleModel.as_dict(database_type="postgresql")
    assert result == expected
