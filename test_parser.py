import unittest
import parser

from expr import *
from tokens import *

from printer import PolishNotation


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
        self.assertEqual(PolishNotation("-34/-23"), "(/ (- 34.0) (- 23.0))")

    def testMultiple(self):
        self.assertEqual(
            PolishNotation("--23*23/---3"), "(/ (* (- (- 23.0)) 23.0) (- (- (- 3.0))))"
        )


class TestTerm(unittest.TestCase):

    def testPlus(self):
        self.assertEqual(
            PolishNotation("0 + 1 + 2 + 3  + 4"), "(+ (+ (+ (+ 0.0 1.0) 2.0) 3.0) 4.0)"
        )

    def testPlusMinusTimes(self):
        self.assertEqual(
            PolishNotation("3 * 4 - 3 * -3"), "(- (* 3.0 4.0) (* 3.0 (- 3.0)))"
        )


class TestBooleanOperations(unittest.TestCase):
    def testMisc(self):
        self.assertEqual(
            PolishNotation("3 * 4 == 4 * 3"), "(== (* 3.0 4.0) (* 4.0 3.0))"
        )
        self.assertEqual(
            PolishNotation("3 * -4 != -4 * 3"), "(!= (* 3.0 (- 4.0)) (* (- 4.0) 3.0))"
        )


class TestCommaOperations(unittest.TestCase):
    def testMisc(self):
        self.assertEqual(PolishNotation("(3, 4, 5)"), "(group (, (, 3.0 4.0) 5.0))")
        self.assertEqual(
            PolishNotation("(true, 3 == 4 - 2, 5)"),
            "(group (, (, True (== 3.0 (- 4.0 2.0))) 5.0))",
        )


class TestTernary(unittest.TestCase):
    def testMisc(self):
        self.assertEqual(
            PolishNotation('false ? 32 * 4 : "error"'), "(? False (* 32.0 4.0) 'error')"
        )


class TestDeclaration(unittest.TestCase):
    def testMisc(self):
        self.assertEqual(PolishNotation('var name = "bob";'), "(var name 'bob')")


class TestAssignment(unittest.TestCase):
    def testMisc(self):
        self.assertEqual(PolishNotation("a= 3"), "(assign a 3.0)")
        self.assertEqual(PolishNotation(" potato = 3"), "(assign potato 3.0)")


class TestBlock(unittest.TestCase):
    def testMisc(self):
        self.assertEqual(
            PolishNotation("{ var a = 1; var b = 2; a = 3;}"),
            "(block (var a 1.0) (var b 2.0) (assign a 3.0))",
        )


class TestLogical(unittest.TestCase):
    def testMisc(self):
        self.assertEqual(
            PolishNotation("var a = 23 or false;"),
            "(var a (or 23.0 False))",
        )
        self.assertEqual(
            PolishNotation("var a = true and false;"), "(var a (and True False))"
        )
        self.assertEqual(
            PolishNotation("var a = true and false or 2;"),
            "(var a (or (and True False) 2.0))",
        )
        self.assertEqual(
            PolishNotation("var a = true and (false or 2);"),
            "(var a (and True (group (or False 2.0))))",
        )


class TestWhile(unittest.TestCase):
    def testMisc(self):
        self.maxDiff = None
        self.assertEqual(
            PolishNotation(
                """
            while (true)
              print 3;""",
            ),
            "(while True (print 3.0))",
        )
        self.assertEqual(
            PolishNotation(
                """
            while (a == b) {
              print a;
              print b;
              print c;
              print a+b or false;
              }""",
            ),
            "(while (== (var a) (var b)) (block (print (var a)) (print (var b)) (print (var c)) (print (or (+ (var a) (var b)) False))))",
        )
        self.assertEqual(
            PolishNotation(
                """
            while (a == b) {
              print a;
              print b;
              break;
              print c;
              print a+b or false;
              }""",
            ),
            "(while (== (var a) (var b)) (block (print (var a)) (print (var b)) (break) (print (var c)) (print (or (+ (var a) (var b)) False))))",
        )
