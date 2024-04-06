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
