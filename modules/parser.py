import re
from enum import Enum
from modules.description import (ClassDescription, FieldDescription,
                                 EnumDescription, ValueEnumDescription)


class TypeConstructions(Enum):
    message = 0,
    enum = 1


class Parser:
    @staticmethod
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
        tree = Tree(
            constructions[0][0], constructions[0][1], constructions[0][2])

        '''for i in range(len(constructions)):
            print(constructions[i])'''

        for i in range(1, len(constructions)):
            tree.add_child(
                constructions[i][0], constructions[i][1], constructions[i][2])

        return tree.get_description()  # Вернёт внутреннее представление класса

    @staticmethod
    def parse_message(text, classes, enums):
        fields = []
        text_split = re.split(r'[{};]', text)
        class_name = re.search(r'message\s+(.+)', text_split[0].strip())[1]
        for i in range(1, len(text_split)):
            field_text = text_split[i].strip()
            if not field_text:
                continue

            a = re.search(
                r'(required|optional|repeated)\s+(.+?)\s+(.+?)\s*=\s*(.+?)',
                field_text)
            modifier = a[1]
            type_field = a[2]
            name_field = a[3]
            index_field = a[4]

            b = re.search(r'default\s*=\s*(.+?)\s*]', field_text)
            default = b[1] if b is not None else None

            fields.append(FieldDescription(modifier=modifier, type=type_field,
                                           name=name_field, index=index_field,
                                           default=default))

        return ClassDescription(name=class_name, fields=fields,
                                classes=classes, enums=enums)

    @staticmethod
    def parse_enum(text):
        values = []
        text_split = re.split(r'[{};]', text)
        enum_name = re.search(r'enum\s+(.+)', text_split[0].strip())[1]
        for i in range(1, len(text_split)):
            value_text = text_split[i].strip()
            if not value_text:
                continue

            a = re.search(r'(.+?)\s*=\s*(.+?)', value_text)
            name_value = a[1]
            index_value = a[2]
            values.append(ValueEnumDescription(
                name=name_value, index=index_value))

        return EnumDescription(name=enum_name, values=values)


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

        self.value = self.value.replace(value, '')
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
            return Parser.parse_message(self.value, classes, enums)
        else:
            return Parser.parse_enum(self.value)
