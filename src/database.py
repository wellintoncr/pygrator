from model import Model

import psycopg2
import os
import json

class Database:
    def __init__(self, **kwargs):
        self.conn = None
        self.migration_path = kwargs.get("migration_path", "migrations/")

    async def migrate(self):
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute("create table my_table")
        self.conn.close()

    async def script_generator(self, table, model):
        script = f"CREATE TABLE {table} "
        for key, value in model.items():
            field_type = await self.type_converter(value.field_type)
            script += f"{key} {field_type}"
        return script

    async def type_converter(self, field_type):
        relation = {
            int: "int",
            str: "varchar(255)",
            float: "decimal(10,2)"
        }
        return relation[field_type] if field_type in relation else "varchar(255)"

    async def update_migration_file(self, migration_file: str, model: Model):
        with open(migration_file, "a+") as file:
           json.dump(await model.to_dict(), file)
