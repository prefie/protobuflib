#!/usr/bin/env python3

import unittest
import os
from modules.parser import Parser
import protobuflib as pb


class ParserTest(unittest.TestCase):
    def test_incorrect_syntax_proto(self):
        with self.assertRaises(Exception):
            with open('examples/bad/incorrect1.proto', 'r') as f:
                Parser.parse(f.read())

        with self.assertRaises(Exception):
            with open('examples/bad/incorrect2.proto', 'r') as f:
                Parser.parse(f.read())


class GeneratorClassTest(unittest.TestCase):
    def test_incorrect_value_in_proto(self):
        with self.assertRaises(Exception):
            pb.create('examples/bad/incorrect2.proto')

    def test_class_created(self):
        files = os.listdir('examples/good')
        for file in files:
            if file.endswith('.proto'):
                self.assertTrue(isinstance(pb.create('examples/good/car_normal.proto'), type))


if __name__ == '__main__':
    unittest.main()
