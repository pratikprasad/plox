from expr import *
from tokens import *
from parser import *

import unittest

expr = Binary(
    Unary(Token.fromTokenType(TokenType.MINUS, 1), Literal(123)),
    Token.fromTokenType(TokenType.STAR, 1),
    Grouping(Literal(45.67)),
)

assert repr(expr) == "(* (- 123) (group 45.67))", "AST Classes broken"


def Eval(text):
    expr = Parse(text)
    return expr.evaluate()


class TestExpr(unittest.TestCase):
    def testUnary(self):
        self.assertEqual(Eval("-2"), -2)
        self.assertEqual(Eval("--2"), 2)

        self.assertEqual(Eval("!true"), False)
        self.assertEqual(Eval("!!true"), True)

    def testBooleanStuff(self):
        self.assertTrue(Eval('"potato"'))  # strings are truthy
        self.assertTrue(Eval("!nil"))  # nil is false, negating it is true
        self.assertTrue(Eval("!!true"))  # double negate true

    def testBinary(self):
        self.assertEqual(Eval("1+1"), 2)
        self.assertEqual(Eval("1+1+(2+2)+(3)"), 9)

        self.assertEqual(Eval("1+2*3"), 7)
        self.assertEqual(Eval("1+2*3*4*5"), 121)

        self.assertEqual(Eval("10 % 3"), 1)
        self.assertEqual(Eval("10 % 3 * 2 + 1"), 3)

        self.assertEqual(Eval("10 / 3"), (10 / 3))
        self.assertEqual(Eval("15 / 3 * 8 "), 40)

        with self.assertRaises(RuntimeException) as err:
            Eval('2 * "potato" * 2')

    def testBinaryBool(self):
        true_strings = [
            "15%4==3",
            "10%3!=3",
            "3==3",
            '11*3!="potato"',
            '"potato" == "potato"',
            "11*3!=3",
            "6 > 3",
            "5 >= 3",
        ]
        for s in true_strings:
            self.assertTrue(Eval(s))

        false_strings = [
            "3!=3",
            "15%4!=3",
            "10%3==3",
            "11*3==3",
            "4/3==3/4",
            "5 < 3",
            "5 <= 3",
        ]
        for s in false_strings:
            self.assertFalse(Eval(s))

    def testTernary(self):
        self.assertEqual(Eval("5 < 3 ? 32 : 10"), 10)
        self.assertEqual(Eval("5 > 3 ? 32 : 10"), 32)

        self.assertEqual(Eval("5 == 3 ? 32 : 10"), 10)
        self.assertEqual(Eval("5 != 3 ? 32 : 10"), 32)
