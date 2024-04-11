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


def eval_as_expression(text):
    sc = Scanner(text)
    tokens = sc.scanTokens()
    ti = TokenIter(tokens)
    expr = expression(ti)
    return expr.evaluate()


class TestExpr(unittest.TestCase):
    def testUnary(self):
        self.assertEqual(eval_as_expression("-2"), -2)
        self.assertEqual(eval_as_expression("--2"), 2)

        self.assertEqual(eval_as_expression("!true"), False)
        self.assertEqual(eval_as_expression("!!true"), True)

    def testBooleanStuff(self):
        self.assertTrue(eval_as_expression('"potato"'))  # strings are truthy
        self.assertTrue(eval_as_expression("!nil"))  # nil is false, negating it is true
        self.assertTrue(eval_as_expression("!!true"))  # double negate true

    def testBinary(self):
        self.assertEqual(eval_as_expression("1+1"), 2)
        self.assertEqual(eval_as_expression("1+1+(2+2)+(3)"), 9)

        self.assertEqual(eval_as_expression("1+2*3"), 7)
        self.assertEqual(eval_as_expression("1+2*3*4*5"), 121)

        self.assertEqual(eval_as_expression("10 % 3"), 1)
        self.assertEqual(eval_as_expression("10 % 3 * 2 + 1"), 3)

        self.assertEqual(eval_as_expression("10 / 3"), (10 / 3))
        self.assertEqual(eval_as_expression("15 / 3 * 8 "), 40)

        with self.assertRaises(RuntimeException) as err:
            eval_as_expression('2 * "potato" * 2')
        with self.assertRaises(RuntimeException) as err:
            eval_as_expression('"tomato" > 3')
        with self.assertRaises(RuntimeException) as err:
            eval_as_expression("4/0")

        self.assertEqual(eval_as_expression('"potato " + "tomato"'), "potato tomato")
        self.assertEqual(eval_as_expression('"potato " +3'), "potato 3.0")

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
            self.assertTrue(eval_as_expression(s))

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
            self.assertFalse(eval_as_expression(s))

    def testTernary(self):
        self.assertEqual(eval_as_expression("5 < 3 ? 32 : 10"), 10)
        self.assertEqual(eval_as_expression("5 > 3 ? 32 : 10"), 32)

        self.assertEqual(eval_as_expression("5 == 3 ? 32 : 10"), 10)
        self.assertEqual(eval_as_expression("5 != 3 ? 32 : 10"), 32)

    def testComma(self):
        self.assertEqual(eval_as_expression("(true, 3 == 4 - 2, 5)"), 5)
        self.assertEqual(eval_as_expression("(5*5)"), 25)
        self.assertEqual(eval_as_expression("(3*1/54%4, false, 5*5)"), 25)
        with self.assertRaises(RuntimeException) as _:
            eval_as_expression('(3*1/54%4*"sdf", false, 5*5)')
