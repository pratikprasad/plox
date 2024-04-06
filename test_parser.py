import unittest

from parser import Parse
from expr import *
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


class TestFactor(unittest.TestCase):

    def testDiv(self):
        self.assertEqual(
            Parse("34/23"),
            Binary(Literal(34), Token.fromTokenType(TokenType.SLASH, 1), Literal(23)),
        )

    def testDivAndNegative(self):
        self.assertEqual(repr(Parse("-34/-23")), "(/ (- 34.0) (- 23.0))")

    def testMultiple(self):
        self.assertEqual(
            repr(Parse("--23*23/---3")), "(/ (* (- (- 23.0)) 23.0) (- (- (- 3.0))))"
        )


class TestTerm(unittest.TestCase):

    def testPlus(self):
        self.assertEqual(
            repr(Parse("0 + 1 + 2 + 3  + 4")), "(+ (+ (+ (+ 0.0 1.0) 2.0) 3.0) 4.0)"
        )

    def testPlusMinusTimes(self):
        self.assertEqual(
            repr(Parse("3 * 4 - 3 * -3")), "(- (* 3.0 4.0) (* 3.0 (- 3.0)))"
        )


class TestBooleanOperations(unittest.TestCase):
    def testMisc(self):
        self.assertEqual(repr(Parse("3 * 4 == 4 * 3")), "(== (* 3.0 4.0) (* 4.0 3.0))")
        self.assertEqual(
            repr(Parse("3 * -4 != -4 * 3")), "(!= (* 3.0 (- 4.0)) (* (- 4.0) 3.0))"
        )


class TestCommaOperations(unittest.TestCase):
    def testMisc(self):
        self.assertEqual(repr(Parse("(3, 4, 5)")), "(group (, (, 3.0 4.0) 5.0))")
        self.assertEqual(
            repr(Parse("(true, 3 == 4 - 2, 5)")),
            "(group (, (, True (== 3.0 (- 4.0 2.0))) 5.0))",
        )


class TestTernary(unittest.TestCase):
    def testMisc(self):
        self.assertEqual(
            repr(Parse('false ? 32 * 4 : "error"')), "(? False (* 32.0 4.0) 'error')"
        )
