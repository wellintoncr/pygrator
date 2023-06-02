import asyncio

from database import Database
from migrator import Migrator
from model import Model

from pydantic import Field


class Sample(Model):
    field_1: int = Field(column_type="int4", unique_id=1)


if __name__ == "__main__":
    print("Main file")
    migration_file = "migrations/my_table.json"
    database = Database()
    asyncio.run(database.update_migration_file(migration_file, Sample))
    migrator = Migrator()
    output = asyncio.run(
        migrator.create_script(migration_file=migration_file, table_name="my_table"))
    print(output)
