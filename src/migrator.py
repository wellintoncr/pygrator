import json

from field import Field


class Migrator:
    async def create_script(
        self,
        migration_file: str,
        table_name: str
    ) -> list:
        with open(migration_file, "r") as file:
            try:
                content = json.load(file)
            except Exception:
                return None
        if not content:
            return None
        output = []
        for pos, each_migration in enumerate(content):
            if pos == 0:
                script = await self.create_table(each_migration["model"], table_name)
                output.append(script)
        return output

    async def create_table(self, migration_data, table_name):
        script = "CREATE TABLE {table_name} ({columns})"
        columns = []
        for column, data in migration_data.items():
            field = await Field.from_str(data)
            columns.append(f"{column} {field.field_type.to_database()}")
        script = script.format(table_name=table_name, columns=",".join(columns))
        return script
