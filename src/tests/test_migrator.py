import tempfile

from migrator import Migrator

import pytest


@pytest.mark.asyncio
async def test_create_script():
    migrator = Migrator()
    migration_file = tempfile.NamedTemporaryFile()
    # Migration file is empty -> should do nothing
    migration_file.write(b'')
    response = await migrator.create_script(migration_file=migration_file.name)
    assert response is None
