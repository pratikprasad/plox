from typing import List
from dataclasses import dataclass

from expr import *
from tokens import *
from scanner import Scanner


@dataclass
class TokenIter:
    tokens: List[Token]
    current: int = 0

    def previous(self):
        return self.tokens[self.current - 1]

    def advance(self):
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    def isAtEnd(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def check(self, token_type: TokenType) -> bool:
        if self.isAtEnd():
            return False
        return self.peek().type == token_type

    def match(self, *types) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        raise Exception(f"Peek: \n {self.peek()} \n\nError: \n {message}")


"""
Version 1

    expression -> primary
    primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")"

Probably the reason he wrote it as one pass was so that you don't have to keep adding and changing the value of `expr`.


Version 2

    expression -> unary
    unary -> ("!" | "-") unary | primary
    primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")"

Probably the reason he wrote it as one pass was so that you don't have to keep adding and changing the value of `expr`.
"""


def expression(ti: TokenIter) -> Expr:
    return unary(ti)


def unary(ti):
    if ti.match(TokenType.BANG, TokenType.MINUS):
        return Unary(ti.previous(), unary(ti))
    else:
        return primary(ti)


def primary(ti: TokenIter) -> Expr:
    if ti.match(TokenType.FALSE):
        return Literal(False)
    if ti.match(TokenType.TRUE):
        return Literal(True)
    if ti.match(TokenType.NIL):
        return Literal(None)

    if ti.match(TokenType.STRING, TokenType.NUMBER):
        return Literal(ti.previous().literal)

    if ti.match(TokenType.LEFT_PAREN):
        expr = expression(ti)
        ti.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
        return Grouping(expr)

    # TODO wat to do
    raise Exception("huh?")


def Parse(text):
    sc = Scanner(text)
    tokens = sc.scanTokens()
    ti = TokenIter(tokens)
    return expression(ti)
