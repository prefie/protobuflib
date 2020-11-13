class ClassDescription:
    def __init__(self, name, fields, classes, enums):
        self.name = name
        self.fields = fields
        self.classes = classes
        self.enums = enums


class FieldDescription:
    def __init__(self, modifier, type, name, index, default=None):
        self.modifier = modifier
        self.type = type
        self.name = name
        self.index = index
        self.default = default


class EnumDescription:
    def __init__(self, name, values):
        self.name = name
        self.values = values


class ValueEnumDescription:
    def __init__(self, name, index):
        self.name = name
        self.index = index
