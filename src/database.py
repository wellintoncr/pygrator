import json

from model import Model


class Database:
    def __init__(self, **kwargs):
        self.conn = None
        self.migration_path = kwargs.get("migration_path", "migrations/")

    async def update_migration_file(self, migration_file: str, model: Model):
        with open(migration_file, "r") as file:
            try:
                current_content = json.loads(file.read())
            except Exception:
                current_content = []

        if not len(current_content) or current_content[-1]["model"] != model.as_dict():
            with open(migration_file, "w+") as file:
                current_content.append({"model": model.as_dict()})
                json.dump(current_content, file)
