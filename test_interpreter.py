import unittest
from interpreter import Interpreter
from parser import Parse


def getLines(program):
    expr = Parse(program)
    inpr = Interpreter()
    return [line.visit(inpr) for line in expr]


class TestInterpreter(unittest.TestCase):

    def testAssignment(self):
        program = """
        var a = 1;
        a = a + 4;
        a = a - 1;
        a + 2;"""

        self.assertEqual(getLines(program)[-1], 6.0)

    def testLogicalOperators(self):
        program = """
        var a = 2;
        var b = false;
        b or a;
        """
        self.assertEqual(getLines(program)[-1], 2.0)

        program = """
        var a = 2;
        var b = false;
        a and b;
        """
        self.assertEqual(getLines(program)[-1], False)

        program = """
        var a = 2;
        var b = false;
        nil or a and b;
        """
        self.assertEqual(getLines(program)[-1], False)

    def testClass(self):
        program = """
        class Pebbles {
            barf() {
                return "barfo";
            }
        }
        Pebbles;
        Pebbles();
        """
        self.assertEqual(repr(getLines(program)[-2]), "Pebbles")
        self.assertEqual(repr(getLines(program)[-1]), "Pebbles instance")

        program = """
        class Pebbles {
            barf() {
                return "barfo";
            }
        }
        var peb = Pebbles();
        peb.age = "8 months";
        peb.age;
        peb.barf();
        """
        self.assertEqual(getLines(program)[-2], "8 months")
        self.assertEqual(getLines(program)[-1], "barfo")
