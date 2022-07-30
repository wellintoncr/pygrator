import json
import tempfile

from database import Database
from field import Field, Integer
from model import Model

import pytest


@pytest.mark.asyncio
async def test_update_migration_file():
    database = Database()
    migration_file = tempfile.NamedTemporaryFile()
    model = Model({
        "id": Field(field_type=Integer())
    })

    # Should write data to the file
    file_name = str(migration_file.name)
    await database.update_migration_file(migration_file=file_name, model=model)
    migration_file.seek(0)
    migration_data = json.loads(migration_file.read())
    assert len(migration_data) == 1
    assert 'id' in migration_data[0]['model']
    assert 'Integer' in migration_data[0]['model']['id']['field_type']

    # The model is exactly the same, so it should not update the file
    await database.update_migration_file(migration_file=file_name, model=model)
    migration_file.seek(0)
    migration_data = json.loads(migration_file.read())
    assert len(migration_data) == 1
