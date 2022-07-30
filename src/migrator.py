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
            else:
                script = await self.update_table(
                    content=content, position=pos, table_name=table_name)
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

    async def update_table(self, content: list, position: int, table_name: str):
        delta = await self.calculate_delta(
            content[position - 1]["model"], content[position]["model"])
        script_to_add = ""
        script_to_delete = ""
        if delta["add"]:
            columns = []
            for column, data in delta["add"].items():
                field = await Field.from_str(data)
                columns.append(f"{column} {field.field_type.to_database()}")
            columns.sort(key=lambda item: item)
            script_to_add = "ALTER TABLE {table_name} ADD {columns};"
            script_to_add = script_to_add.format(table_name=table_name, columns=",".join(columns))
        if delta["remove"]:
            columns = list(delta["remove"].keys())
            columns.sort(key=lambda item: item)
            script_to_add = "ALTER TABLE {table_name} DROP COLUMN {columns};"
            script_to_add = script_to_add.format(table_name=table_name, columns=",".join(columns))
        return script_to_add + script_to_delete

    async def calculate_delta(self, old_model, new_model):
        old_fields = set(old_model.keys())
        new_fields = set(new_model.keys())
        output = {
            "add": {},
            "remove": {}
        }
        for field in new_fields:
            if field not in old_fields:
                output["add"][field] = new_model[field]
        for field in old_fields:
            if field not in new_fields:
                output["remove"][field] = old_model[field]
        return output
