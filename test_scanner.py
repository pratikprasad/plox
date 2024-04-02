import unittest
from scanner import *
from tokens import *


class TestScanner(unittest.TestCase):
    def testComment(self):
        sc = Scanner("// this is a comment")
        self.assertListEqual(sc.scanTokens(), [Token(TokenType.EOF, "", None, 1)])

    def testEmpty(self):
        sc = Scanner("")
        self.assertListEqual(
            sc.scanTokens(),
            [Token(TokenType.EOF, "", None, 1)],
        )

    def testBracesAndSingleChars(self):
        sc = Scanner("(( )) {}")
        self.assertListEqual(
            sc.scanTokens(),
            [
                Token.fromTokenType(TokenType.LEFT_PAREN, 1),
                Token.fromTokenType(TokenType.LEFT_PAREN, 1),
                Token.fromTokenType(TokenType.RIGHT_PAREN, 1),
                Token.fromTokenType(TokenType.RIGHT_PAREN, 1),
                Token.fromTokenType(TokenType.LEFT_BRACE, 1),
                Token.fromTokenType(TokenType.RIGHT_BRACE, 1),
                Token.fromTokenType(TokenType.EOF, 1),
            ],
        )

    def testOperators(self):
        sc = Scanner("!*+/=<> <= >= ==")
        self.assertListEqual(
            sc.scanTokens(),
            [
                Token.fromTokenType(TokenType.BANG, 1),
                Token.fromTokenType(TokenType.STAR, 1),
                Token.fromTokenType(TokenType.PLUS, 1),
                Token.fromTokenType(TokenType.SLASH, 1),
                Token.fromTokenType(TokenType.EQUAL, 1),
                Token.fromTokenType(TokenType.LESS, 1),
                Token.fromTokenType(TokenType.GREATER, 1),
                Token.fromTokenType(TokenType.LESS_EQUAL, 1),
                Token.fromTokenType(TokenType.GREATER_EQUAL, 1),
                Token.fromTokenType(TokenType.EQUAL_EQUAL, 1),
                Token.fromTokenType(TokenType.EOF, 1),
            ],
        )

    def testString(self):
        sc = Scanner('"ham sandwich"')
        self.assertListEqual(
            sc.scanTokens(),
            [
                Token(TokenType.STRING, '"ham sandwich"', "ham sandwich", 1),
                Token.fromTokenType(TokenType.EOF, 1),
            ],
        )

    def testNumber(self):
        sc = Scanner("123.432")
        self.assertListEqual(
            sc.scanTokens(),
            [
                Token(TokenType.NUMBER, "123.432", 123.432, 1),
                Token.fromTokenType(TokenType.EOF, 1),
            ],
        )
