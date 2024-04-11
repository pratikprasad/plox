import unittest
import parser

from expr import *
from tokens import *


def parse(text):
    """
    Adds a semicolon so I don't have to rewrite all the tests
    """
    return parser.Parse(text + ";")[0].expression


class TestPrimary(unittest.TestCase):
    """"""

    def testTrue(self):
        self.assertEqual(parse("true"), Literal(True))

    def testFalse(self):
        self.assertEqual(parse("false"), Literal(False))

    def testNil(self):
        self.assertEqual(parse("nil"), Literal(None))

    def testString(self):
        self.assertEqual(parse('"hello world"'), Literal("hello world"))

    def testNumber(self):
        self.assertEqual(parse("123.456"), Literal(123.456))

    def testGrouping(self):
        self.assertEqual(parse("(432.234234)"), Grouping(Literal(432.234234)))
        self.assertEqual(parse("(false)"), Grouping(Literal(False)))


class TestUnary(unittest.TestCase):
    def testNumberNegation(self):
        self.assertEqual(
            parse("-4321"),
            Unary(Token.fromTokenType(TokenType.MINUS, 1), Literal(4321)),
        )
        self.assertEqual(
            parse("--4321"),
            Unary(
                Token.fromTokenType(TokenType.MINUS, 1),
                Unary(Token.fromTokenType(TokenType.MINUS, 1), Literal(4321)),
            ),
        )

    def testBooleNegation(self):
        self.assertEqual(
            parse('!"hello world"'),
            Unary(Token.fromTokenType(TokenType.BANG, 1), Literal("hello world")),
        )
        self.assertEqual(
            parse('!!"hello world"'),
            Unary(
                Token.fromTokenType(TokenType.BANG, 1),
                Unary(Token.fromTokenType(TokenType.BANG, 1), Literal("hello world")),
            ),
        )

    def testFunnyStuff(self):
        self.assertEqual(
            parse('-!"hello world"'),
            Unary(
                Token.fromTokenType(TokenType.MINUS, 1),
                Unary(Token.fromTokenType(TokenType.BANG, 1), Literal("hello world")),
            ),
        )


class TestFactor(unittest.TestCase):

    def testDiv(self):
        self.assertEqual(
            parse("34/23"),
            Binary(Literal(34), Token.fromTokenType(TokenType.SLASH, 1), Literal(23)),
        )

    def testDivAndNegative(self):
        self.assertEqual(repr(parse("-34/-23")), "(/ (- 34.0) (- 23.0))")

    def testMultiple(self):
        self.assertEqual(
            repr(parse("--23*23/---3")), "(/ (* (- (- 23.0)) 23.0) (- (- (- 3.0))))"
        )


class TestTerm(unittest.TestCase):

    def testPlus(self):
        self.assertEqual(
            repr(parse("0 + 1 + 2 + 3  + 4")), "(+ (+ (+ (+ 0.0 1.0) 2.0) 3.0) 4.0)"
        )

    def testPlusMinusTimes(self):
        self.assertEqual(
            repr(parse("3 * 4 - 3 * -3")), "(- (* 3.0 4.0) (* 3.0 (- 3.0)))"
        )


class TestBooleanOperations(unittest.TestCase):
    def testMisc(self):
        self.assertEqual(repr(parse("3 * 4 == 4 * 3")), "(== (* 3.0 4.0) (* 4.0 3.0))")
        self.assertEqual(
            repr(parse("3 * -4 != -4 * 3")), "(!= (* 3.0 (- 4.0)) (* (- 4.0) 3.0))"
        )


class TestCommaOperations(unittest.TestCase):
    def testMisc(self):
        self.assertEqual(repr(parse("(3, 4, 5)")), "(group (, (, 3.0 4.0) 5.0))")
        self.assertEqual(
            repr(parse("(true, 3 == 4 - 2, 5)")),
            "(group (, (, True (== 3.0 (- 4.0 2.0))) 5.0))",
        )


class TestTernary(unittest.TestCase):
    def testMisc(self):
        self.assertEqual(
            repr(parse('false ? 32 * 4 : "error"')), "(? False (* 32.0 4.0) 'error')"
        )


class TestDeclaration(unittest.TestCase):
    def testMisc(self):
        self.assertEqual(repr(parser.Parse('var name = "bob";')), "[(var name 'bob')]")
