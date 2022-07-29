
class Field:
    def __init__(self, field_type, **kwargs):
        self.field_type = field_type

    async def to_dict(self):
        output = {
            'field_type': str(self.field_type)
        }
        return output

    @staticmethod
    def convert_str_to_class(data: str):
        relation = {
            'int': int
        }
        return relation[data]

    @staticmethod
    async def from_str(data: str):
        field_type = data['field_type'].replace('<class \'', '').replace('\'>', '')
        return Field(field_type=Field.convert_str_to_class(field_type))
