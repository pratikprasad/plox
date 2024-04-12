import unittest
from interpreter import Interpreter
from parser import Parse


class TestInterpreter(unittest.TestCase):

    def testAssignment(self):
        program = """var a = 1; a = a + 4; a = a - 1; a + 2;"""
        expr = Parse(program)
        inpr = Interpreter()
        last = None
        for line in expr:
            last = line.visit(inpr)
        self.assertEqual(last, 6.0)
