#!/usr/bin/env python3

import re
from enum import Enum


def create(filename):
    with open(filename, 'r') as f:
        parse(f.read())
        pass


def parse(text):
    stack = []
    constructions = []

    index = 0
    for i in range(len(text)):
        if text[i] == '{' or text[i] == '}' or text[i] == ';':
            if text[i] == '{':
                stack.append(index)
            if text[i] == '}':
                x = stack.pop()
                constructions.append((x, i, text[x:i + 1].strip()))

            index = i + 1

    constructions.reverse()
    tree = Tree(constructions[0][0], constructions[0][1], constructions[0][2])

    for i in range(len(constructions)):
        print(constructions[i])

    for i in range(1, len(constructions)):
        tree.add_child(constructions[i][0], constructions[i][1], constructions[i][2])

    description = tree.get_description()  # Вернёт внутреннее представление класса !!!!!!!!!!!!!!!


def parse_message(text, classes, enums):
    fields = []
    text_split = re.split(r'[{};]', text)
    class_name = re.search(r'message\s+(.+?)\s+', text_split[0])[1]
    for i in range(1, len(text_split)):
        field_text = text_split[i].strip()
        if not field_text:
            continue

        a = re.search(r'(required|optional|repeated)\s+(.+?)\s+(.+?)\s+=\s+(.+?)', field_text)
        modifier = a[1]
        type_field = a[2]
        name_field = a[3]
        index_field = a[4]
        fields.append(FieldDescription(modifier=modifier, type=type_field,
                                       name=name_field, index=index_field))

    return ClassDescription(name=class_name, fields=fields, classes=classes, enums=enums)


def parse_enum(text):
    values = []
    text_split = re.split(r'[{};]', text)
    enum_name = re.search(r'enum\s+(.+?)\s+', text_split[0])[1]
    for i in range(1, len(text_split)):
        value_text = text_split[i].strip()
        if not value_text:
            continue

        a = re.search(r'(.+?)\s+=\s+(.+?)', value_text)
        name_value = a[1]
        index_value = a[2]
        values.append(ValueEnumDescription(name=name_value, index=index_value))

    return EnumDescription(name=enum_name, values=values)


class ClassDescription:
    def __init__(self, name, fields, classes, enums):
        self.name = name
        self.fields = fields
        self.classes = classes
        self.enums = enums


class FieldDescription:
    def __init__(self, modifier, type, name, index):
        self.modifier = modifier
        self.type = type
        self.name = name
        self.index = index


class EnumDescription:
    def __init__(self, name, values):
        self.name = name
        self.values = values


class ValueEnumDescription:
    def __init__(self, name, index):
        self.name = name
        self.index = index


class TypeConstructions(Enum):
    message = 0,
    enum = 1


class Tree:
    def __init__(self, begin, end, value):
        self.begin = begin
        self.end = end
        self.value = value
        self.type = TypeConstructions[self.value.split()[0]]

        self.children = []

    def add_child(self, begin, end, value):
        """Возвращает True, если удалось добавить ребенка"""
        if begin < self.begin or end > self.end:
            return False

        for child in self.children:
            if child.add_child(begin, end, value):
                return True

        self.children.append(Tree(begin, end, value))

        self.value = self.value.replace(value, '')  # Чтобы у родителей не было повторений сообщений детей
        return True

    def get_description(self):
        classes = []
        enums = []
        for child in self.children:
            description = child.get_description()
            if type(description) == ClassDescription:
                classes.append(description)
            if type(description) == EnumDescription:
                enums.append(description)

        if self.type == TypeConstructions.message:
            return parse_message(self.value, classes, enums)
        else:
            return parse_enum(self.value)


if __name__ == '__main__':
    create('2.proto')
