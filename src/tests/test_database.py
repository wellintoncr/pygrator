import json

from database import Database
from field import Field
from model import Model

import pytest


@pytest.mark.asyncio
async def test_script_generator(tmp_path):
    database = Database()
    model = Model({
        "id": Field(field_type=int)
    })
    # Should write data to the file
    migration_file = tmp_path / 'new_table.json'
    await database.update_migration_file(migration_file=migration_file, model=model)
    migration_data = json.loads(migration_file.read_text())
    migration_data = await Model.from_dict(migration_data)
    # Should be possible to read an object reflecting the original Model object
    assert await migration_data.to_dict() == await model.to_dict()


@pytest.mark.asyncio
async def test_type_converter():
    database = Database()
    response = await database.type_converter(int)
    assert response == 'int'

    response = await database.type_converter(str)
    assert response == 'varchar(255)'

    response = await database.type_converter(float)
    assert response == 'decimal(10,2)'
