from field import Field, Float, Integer, String

import pytest


@pytest.mark.asyncio
async def test_to_dict():
    field = Field(field_type=Integer())
    assert await field.to_dict() == {"field_type": "<class 'Integer'>"}

    field = Field(field_type=String())
    assert await field.to_dict() == {"field_type": "<class 'String'>"}

    field = Field(field_type=Float())
    assert await field.to_dict() == {"field_type": "<class 'Float'>"}

    # New type
    class NewType:
        def __str__(self):
            return "<class 'NewType'>"

    field = Field(field_type=NewType())
    assert await field.to_dict() == {"field_type": "<class 'NewType'>"}


@pytest.mark.asyncio
async def test_convert_str_to_class():
    response = Field.convert_str_to_class('Integer')
    assert response == Integer

    response = Field.convert_str_to_class('String')
    assert response == String

    with pytest.raises(ValueError):
        Field.convert_str_to_class('UnknownClass')


@pytest.mark.asyncio
async def test_from_str():
    response = await Field.from_str({'field_type': '<class \'Integer\'>'})
    assert isinstance(response, Field)
