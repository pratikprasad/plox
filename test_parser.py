import unittest

from parser import *
from scanner import *
from tokens import *


class TestPrimary(unittest.TestCase):
    """"""

    def testTrue(self):
        self.assertEqual(Parse("true"), Literal(True))

    def testFalse(self):
        self.assertEqual(Parse("false"), Literal(False))

    def testNil(self):
        self.assertEqual(Parse("nil"), Literal(None))

    def testString(self):
        self.assertEqual(Parse('"hello world"'), Literal("hello world"))

    def testNumber(self):
        self.assertEqual(Parse("123.456"), Literal(123.456))

    def testGrouping(self):
        self.assertEqual(Parse("(432.234234)"), Grouping(Literal(432.234234)))
        self.assertEqual(Parse("(false)"), Grouping(Literal(False)))


class TestUnary(unittest.TestCase):
    def testNumberNegation(self):
        self.assertEqual(
            Parse("-4321"),
            Unary(Token.fromTokenType(TokenType.MINUS, 1), Literal(4321)),
        )
        self.assertEqual(
            Parse("--4321"),
            Unary(
                Token.fromTokenType(TokenType.MINUS, 1),
                Unary(Token.fromTokenType(TokenType.MINUS, 1), Literal(4321)),
            ),
        )

    def testBooleNegation(self):
        self.assertEqual(
            Parse('!"hello world"'),
            Unary(Token.fromTokenType(TokenType.BANG, 1), Literal("hello world")),
        )
        self.assertEqual(
            Parse('!!"hello world"'),
            Unary(
                Token.fromTokenType(TokenType.BANG, 1),
                Unary(Token.fromTokenType(TokenType.BANG, 1), Literal("hello world")),
            ),
        )

    def testFunnyStuff(self):
        self.assertEqual(
            Parse('-!"hello world"'),
            Unary(
                Token.fromTokenType(TokenType.MINUS, 1),
                Unary(Token.fromTokenType(TokenType.BANG, 1), Literal("hello world")),
            ),
        )
