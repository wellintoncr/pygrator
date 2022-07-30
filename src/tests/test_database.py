import json

from database import Database
from field import Field, Integer
from model import Model

import pytest


@pytest.mark.asyncio
async def test_update_migration_file(tmp_path):
    database = Database()
    model = Model({
        "id": Field(field_type=Integer)
    })
    # Should write data to the file
    migration_file = tmp_path / 'new_table.json'
    await database.update_migration_file(migration_file=migration_file, model=model)
    migration_data = json.loads(migration_file.read_text())
    assert 'id' in migration_data
    assert 'Integer' in migration_data['id']['field_type']
