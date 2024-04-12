from typing import List, Optional
from dataclasses import dataclass

from expr import Unary, Binary, Literal, Grouping, Ternary, Variable
from stmt import Print, Expression, Stmt, Var
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

    def synchronize(self):
        self.advance()
        while not self.isAtEnd():
            if self.previous().type == TokenType.SEMICOLON:
                return
            if self.peek().type in {
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            }:
                return
            self.advance()


"""
Probably the reason he wrote it as one pass was so that you don't have to keep adding and changing the value of `expr`.

Version 1

    expression -> primary
    primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")"



Version 2

    expression -> unary
    unary -> ("!" | "-") unary | primary
    primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")"

Version 3

    expression -> factor
    factor -> unary ( ("\" | "*") unary)*
    unary -> ("!" | "-") unary | primary
    primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")"

Version 4

    expression -> term
    term -> factor (( "-" | "+" ) factor)*
    factor -> unary ( ("\" | "*") unary)*
    unary -> ("!" | "-") unary | primary
    primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")"

Version 5

    expression -> comparison
    comparison -> term (( > | >= | < | <=))*
    term -> factor (( "-" | "+" ) factor)*
    factor -> unary ( ("\" | "*") unary)*
    unary -> ("!" | "-") unary | primary
    primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")"

Version 6

    expression -> comma
    comma -> comparision (, comparision)*
    comparison -> term (( > | >= | < | <=))*
    term -> factor (( "-" | "+" ) factor)*
    factor -> unary ( ("\" | "*") unary)*
    unary -> ("!" | "-") unary | primary
    primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")"

Version 7

    expression -> ternary
    ternary -> comma | comma "?" comma : comma 
    comma -> comparision (, comparision)*
    comparison -> term (( > | >= | < | <=))*
    term -> factor (( "-" | "+" ) factor)*
    factor -> unary ( ("\" | "*") unary)*
    unary -> ("!" | "-") unary | primary
    primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")"
    

Version 8 -- add ternary

    expression -> ternary
    ternary -> comma | comma "?" comma : comma 
    comma -> comparision (, comparision)*
    comparison -> term (( > | >= | < | <=))*
    term -> factor (( "-" | "+" ) factor)*
    factor -> unary (("%" | \" | "*") unary)*
    unary -> ("!" | "-") unary | primary
    primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")"

Version 9 -- Add expression statements and prints statements

    program -> statement* EOF
    statement -> exprStmt | printStmt
    exprStmt -> expression ";"
    printStmt -> "print" expression ";"
    expression -> ternary
    ternary -> comma | comma "?" comma : comma 
    comma -> comparision (, comparision)*
    comparison -> term (( > | >= | < | <=))*
    term -> factor (( "-" | "+" ) factor)*
    factor -> unary (("%" | \" | "*") unary)*
    unary -> ("!" | "-") unary | primary
    primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")"

Version 10 -- Add variable declarations

    program -> declaration* EOF
    declaration -> varDecl | statement
    varDecl -> "var" identifier ("=" expression)? ";"
    statement -> exprStmt | printStmt
    exprStmt -> expression ";"
    printStmt -> "print" expression ";"
    expression -> ternary
    ternary -> comma | comma "?" comma : comma 
    comma -> comparision (, comparision)*
    comparison -> term (( > | >= | < | <=))*
    term -> factor (( "-" | "+" ) factor)*
    factor -> unary (("%" | \" | "*") unary)*
    unary -> ("!" | "-") unary | primary
    primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" | IDENTIFIER
"""


def declaration(ti) -> Optional[Stmt]:
    try:
        if ti.match(TokenType.VAR):
            return varDecl(ti)
        return statement(ti)
    except Exception as e:
        print(e)
        ti.synchronize()
        return None


def varDecl(ti) -> Stmt:
    name = ti.consume(TokenType.IDENTIFIER, "Expect variable name")
    initializer = None
    if ti.match(TokenType.EQUAL):
        initializer = expression(ti)
    ti.consume(TokenType.SEMICOLON, "Expect statement to end with ';'")
    return Var(name, initializer)


def statement(ti):
    if ti.match(TokenType.PRINT):
        return printStmt(ti)
    return exprStmt(ti)


def exprStmt(ti: TokenIter):
    value = expression(ti)
    ti.consume(TokenType.SEMICOLON, "Expect statement to end with ';'")
    return Expression(value)


def printStmt(ti: TokenIter):
    value = expression(ti)
    ti.consume(TokenType.SEMICOLON, "Expect statement to end with ';'")
    return Print(value)


def expression(ti: TokenIter):
    return ternary(ti)


def ternary(ti: TokenIter):
    test = comma(ti)
    if not ti.match(TokenType.QUESTION):
        return test

    left = comma(ti)
    if not ti.match(TokenType.COLON):
        raise Exception("Expected colon for ternary operator")
    right = comma(ti)

    return Ternary(test, left, right)


def comma(ti: TokenIter):
    out = equality(ti)
    while ti.match(TokenType.COMMA):
        out = Binary(out, ti.previous(), equality(ti))
    return out


def equality(ti):
    out = comparison(ti)
    while ti.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
        out = Binary(out, ti.previous(), comparison(ti))
    return out


def comparison(ti):
    out = term(ti)
    while ti.match(
        TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL
    ):
        out = Binary(out, ti.previous(), term(ti))
    return out


def term(ti):
    out = factor(ti)
    while ti.match(TokenType.PLUS, TokenType.MINUS):
        out = Binary(out, ti.previous(), factor(ti))

    return out


def factor(ti):
    out = unary(ti)
    while ti.match(TokenType.STAR, TokenType.SLASH, TokenType.MOD):
        out = Binary(out, ti.previous(), unary(ti))

    return out


def unary(ti):
    if ti.match(TokenType.BANG, TokenType.MINUS):
        return Unary(ti.previous(), unary(ti))

    return primary(ti)


def primary(ti: TokenIter):
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

    if ti.match(TokenType.IDENTIFIER):
        return Variable(ti.previous())

    # TODO fix up the error handling thing
    raise Exception(f"{ti.peek()}")


def Parse(text):
    sc = Scanner(text)
    tokens = sc.scanTokens()
    ti = TokenIter(tokens)
    out = []
    while not ti.isAtEnd():
        decl = declaration(ti)
        out.append(decl)
    return out
