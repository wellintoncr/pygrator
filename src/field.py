
class Field:
    def __init__(self, field_type, **kwargs):
        self.field_type = field_type

    async def to_dict(self):
        print(self.field_type)
        output = {
            'field_type': str(self.field_type)
        }
        return output

    @staticmethod
    def convert_str_to_class(data: str):
        try:
            return globals()[data]
        except KeyError:
            raise ValueError("This type is not available")

    @staticmethod
    async def from_str(data: str):
        field_type = data['field_type'].replace('<type ', '').replace('>', '')
        return Field(field_type=Field.convert_str_to_class(field_type))


class Integer:

    def __str__(self):
        return '<type Integer>'


class String:

    def __str__(self):
        return '<type String>'


class Float:

    def __str__(self):
        return '<type Float>'
