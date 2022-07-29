from field import Field

class Model:
    def __init__(self, model):
        self.model = model

    async def to_dict(self):
        output = {}
        for key, value in self.model.items():
            output[key] = await value.to_dict()
        return output

    @staticmethod
    async def from_dict(data: dict):
        output = {}
        for key, value in data.items():
            each_value = await Field.from_str(value)
            output[key] = each_value
        return Model(output)
