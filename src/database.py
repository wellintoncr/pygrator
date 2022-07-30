import json

from model import Model


class Database:
    def __init__(self, **kwargs):
        self.conn = None
        self.migration_path = kwargs.get("migration_path", "migrations/")

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
