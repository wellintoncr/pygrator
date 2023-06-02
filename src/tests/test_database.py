import json
import tempfile

from database import Database
from model import Model

import pytest


@pytest.mark.asyncio
async def test_update_migration_file():
    database = Database()
    migration_file = tempfile.NamedTemporaryFile()

    class SampleModel(Model):
        field_1: int

    # Should write data to the file
    file_name = str(migration_file.name)
    await database.update_migration_file(migration_file=file_name, model=SampleModel)
    migration_file.seek(0)
    migration_data = json.loads(migration_file.read())
    assert len(migration_data) == 1
    assert 'field_1' in migration_data[0]['model']['fields'].keys()

    # The model is exactly the same, so it should not update the file
    await database.update_migration_file(migration_file=file_name, model=SampleModel)
    migration_file.seek(0)
    migration_data = json.loads(migration_file.read())
    assert len(migration_data) == 1

    # Change model and it should append it to the migration file
    class SampleModel(Model):
        field_1: int
        field_2: str

    await database.update_migration_file(migration_file=file_name, model=SampleModel)
    migration_file.seek(0)
    migration_data = json.loads(migration_file.read())
    assert len(migration_data) == 2
