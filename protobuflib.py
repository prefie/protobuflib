#!/usr/bin/env python3

from enum import Enum
from modules.parser import Parser

TYPES = {'int32': int,
         'int64': int,
         'float': float,
         'double': float,
         'bool': bool,
         'string': str}


def create(filename):
    with open(filename, 'r') as f:
        description = Parser.parse(f.read())
        return _generate_class(description)


def _generate_class(class_description):
    classes = {}
    for cls in class_description.classes:
        classes[cls.name] = _generate_class(cls)

    enums = {}
    for enum in class_description.enums:
        enums[enum.name] = Enum(enum.name, list(map(lambda x: x.name, enum.values)))

    types = {}
    types.update(TYPES)
    types.update(classes)
    types.update(enums)

    required_fields = sorted(
        filter(lambda x: x.modifier == 'required', class_description.fields),
        key=lambda x: x.index)

    def init(self, *args):
        if len(args) != len(required_fields):
            raise Exception()

        for i in range(len(args)):
            key, value = required_fields[i].name, types[required_fields[i].type]
            if not isinstance(args[i], value):
                raise Exception()
            setattr(self, key, args[i])

    fields = {}
    for field in class_description.fields:
        if field.type in enums.keys():
            fields[field.name] = types[field.type][field.default] if field.default is not None else None
        else:
            fields[field.name] = types[field.type](field.default) if field.default is not None else None

    attr = {'__init__': init}
    attr.update(fields)
    attr.update(enums)
    attr.update(classes)
    return type(class_description.name, (), attr)


if __name__ == '__main__':
    Car = create('examples/bad/incorrect3.proto')
    car = Car('model', Car.BodyType.hatchback, 2008)
    pass
