from pydantic import BaseModel


class Model(BaseModel):

    @classmethod
    def as_dict(cls, database_type: str = "postgresql"):
        available_types = {
            "postgresql": {
                int: "int4",
                str: "text"
            }
        }
        class_data = cls.schema()
        fields = cls.__fields__
        output = {
            "name": class_data["title"],
            "model_id": class_data.get("class_id"),
            "fields": {
                k: {
                    "unique_id": v.get("unique_id"),
                    "column_type": v.get(
                        "column_type",
                        available_types[database_type].get(fields[k].type_))
                } for k, v in class_data["properties"].items()}
        }
        return output
