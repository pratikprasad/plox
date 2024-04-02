import unittest
from scanner import *
from tokens import *


class TestScanner(unittest.TestCase):
    def testComment(self):
        sc = Scanner("// this is a comment")
        self.assertListEqual(sc.scanTokens(), [Token(TokenType.EOF, "", None, 1)])
