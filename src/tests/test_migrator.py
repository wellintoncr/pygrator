import json
import tempfile

from migrator import Migrator

import pytest


@pytest.mark.asyncio
async def test_create_script():
    migrator = Migrator()
    migration_file = tempfile.NamedTemporaryFile()

    # Migration file is empty -> should do nothing
    migration_file.write(b'')
    response = await migrator.create_script(
        migration_file=migration_file.name,
        table_name="new_table"
    )
    assert response is None

    # Migration file is empty list -> should do nothing
    migration_file.write(b'[]')
    migration_file.seek(0)
    response = await migrator.create_script(
        migration_file=migration_file.name,
        table_name="new_table"
    )
    assert response is None

    # Migration file has one entry -> should create table
    content = [
        {
            "model": {
                "id": {
                    "field_type": "<type Integer>"
                },
                "name": {
                    "field_type": "<type String>"
                }
            }
        }
    ]
    migration_file.write(bytes(json.dumps(content), 'utf-8'))
    migration_file.seek(0)
    response = await migrator.create_script(
        migration_file=migration_file.name,
        table_name="new_table"
    )
    expected = ["CREATE TABLE new_table (id INT,name VARCHAR(255))"]
    assert response == expected
