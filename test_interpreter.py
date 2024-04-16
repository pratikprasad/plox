import unittest
from interpreter import Interpreter
from parser import Parse


def getLastLine(program):
    expr = Parse(program)
    inpr = Interpreter()
    last = None
    for line in expr:
        last = line.visit(inpr)
    return last


class TestInterpreter(unittest.TestCase):

    def testAssignment(self):
        program = """
        var a = 1;
        a = a + 4;
        a = a - 1;
        a + 2;"""

        self.assertEqual(getLastLine(program), 6.0)

    def testLogicalOperators(self):
        program = """
        var a = 2;
        var b = false;
        b or a;
        """
        self.assertEqual(getLastLine(program), 2.0)

        program = """
        var a = 2;
        var b = false;
        a and b;
        """
        self.assertEqual(getLastLine(program), False)

        program = """
        var a = 2;
        var b = false;
        nil or a and b;
        """
        self.assertEqual(getLastLine(program), False)
