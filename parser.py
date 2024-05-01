from logging import error
from typing import List
from dataclasses import dataclass

from expr import (
    This,
    Get,
    Set,
    Unary,
    Binary,
    Literal,
    Grouping,
    Ternary,
    Variable,
    Assign,
    Logical,
    Call,
)
from stmt import (
    BreakStmt,
    Function,
    Print,
    Expression,
    Return,
    Stmt,
    Var,
    Block,
    IfStmt,
    WhileStmt,
    Class,
)
from tokens import TokenType as TT, Token
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
        return self.peek().type == TT.EOF

    def peek(self):
        return self.tokens[self.current]

    def check(self, token_type: TT) -> bool:
        if self.isAtEnd():
            return False
        return self.peek().type == token_type

    def match(self, *types) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def consume(self, token_type: TT, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        raise Exception(f"Peek: \n {self.peek()} \n\nError: \n {message}")

    def synchronize(self):
        self.advance()
        while not self.isAtEnd():
            if self.previous().type == TT.SEMICOLON:
                return
            if self.peek().type in {
                TT.CLASS,
                TT.FUN,
                TT.VAR,
                TT.FOR,
                TT.IF,
                TT.WHILE,
                TT.PRINT,
                TT.RETURN,
            }:
                return
            self.advance()


def function(ti, kind):
    name = None
    if kind != "lambda":
        name = ti.consume(TT.IDENTIFIER, f"Expect {kind} name")
    ti.consume(TT.LEFT_PAREN, f"Expect ( after {kind} name")
    params = []
    while True:
        if ti.check(TT.RIGHT_PAREN):
            break
        if len(params) > 255:
            error(ti.peek(), "Can't have more than 255 params")
        params.append(ti.consume(TT.IDENTIFIER, "Expect param name"))
        if not ti.match(TT.COMMA):
            break
    ti.consume(TT.RIGHT_PAREN, "Expect ) after params")

    ti.consume(TT.LEFT_BRACE, "Expect { before " + kind + " body")
    body = block(ti)
    return Function(name, params, body.statements)


def classDecl(ti):
    name = ti.consume(TT.IDENTIFIER, "Expect class name")
    ti.consume(TT.LEFT_BRACE, "Expect { before class body")
    methods = []
    while not ti.check(TT.RIGHT_BRACE) and not ti.isAtEnd():
        methods.append(function(ti, "method"))
    ti.consume(TT.RIGHT_BRACE, "Expect } after class body")

    return Class(name, methods)


def declaration(ti):
    if ti.match(TT.CLASS):
        return classDecl(ti)
    if ti.match(TT.VAR):
        return varDecl(ti)
    if ti.match(TT.FUN):
        return function(ti, "function")
    return statement(ti)
    try:
        if ti.match(TT.VAR):
            return varDecl(ti)
        return statement(ti)
    except Exception as e:
        print(e)
        ti.synchronize()
        return None


def varDecl(ti) -> Stmt:
    name = ti.consume(TT.IDENTIFIER, "Expect variable name")
    initializer = None
    if ti.match(TT.EQUAL):
        initializer = expression(ti)
    ti.consume(TT.SEMICOLON, "Expect statement to end with ';'")
    return Var(name, initializer)


def block(ti):
    out = []
    while not ti.check(TT.RIGHT_BRACE) and not ti.isAtEnd():
        out.append(declaration(ti))
    ti.consume(TT.RIGHT_BRACE, "Expect block to end with '}'")
    return Block(out)


def whileStmt(ti):
    ti.consume(TT.LEFT_PAREN, "Expect '(' after while")
    condition = expression(ti)
    ti.consume(TT.RIGHT_PAREN, "Expect ')' after while")
    body = statement(ti)

    return WhileStmt(condition, body)


def ifStmt(ti):
    ti.consume(TT.LEFT_PAREN, "Expect ( after if")
    condition = expression(ti)
    ti.consume(TT.RIGHT_PAREN, "Expect ) after if condition")
    thenBranch = statement(ti)
    elseBranch = None
    if ti.match(TT.ELSE):
        elseBranch = statement(ti)
    return IfStmt(condition, thenBranch, elseBranch)


def forStmt(ti):
    ti.consume(TT.LEFT_PAREN, "Expect ( after for")
    initializer = None
    if ti.match(TT.SEMICOLON):
        pass
    elif ti.match(TT.VAR):
        initializer = varDecl(ti)
    else:
        initializer = exprStmt(ti)

    condition = None
    if not ti.check(TT.SEMICOLON):
        condition = expression(ti)
    ti.consume(TT.SEMICOLON, "Expect ; after loop condition")

    increment = None
    if not ti.check(TT.RIGHT_PAREN):
        increment = expression(ti)
    ti.consume(TT.RIGHT_PAREN, "expect ) after for clauses")

    body = statement(ti)
    if increment is not None:
        body = Block([body, Expression(increment)])
    if condition is None:
        condition = Literal(True)
    body = WhileStmt(condition, body)

    if initializer is not None:
        body = Block([initializer, body])

    return body


def statement(ti) -> Stmt:
    if ti.match(TT.LEFT_BRACE):
        return block(ti)
    if ti.match(TT.PRINT):
        return printStmt(ti)
    if ti.match(TT.IF):
        return ifStmt(ti)
    if ti.match(TT.WHILE):
        return whileStmt(ti)
    if ti.match(TT.FOR):
        return forStmt(ti)
    if ti.match(TT.BREAK):
        return breakStmt(ti)
    if ti.match(TT.RETURN):
        return returnStmt(ti)
    return exprStmt(ti)


def returnStmt(ti):
    keyword = ti.previous()
    value = None
    if not ti.check(TT.SEMICOLON):
        value = expression(ti)

    ti.consume(TT.SEMICOLON, "Expect ; after return statement")
    return Return(keyword, value)


def breakStmt(ti):
    out = BreakStmt()
    ti.consume(TT.SEMICOLON, "Expect break statement to end with ';'")
    return out


def exprStmt(ti: TokenIter):
    value = expression(ti)
    ti.consume(TT.SEMICOLON, "Expect statement to end with ';'")
    return Expression(value)


def printStmt(ti: TokenIter):
    value = expression(ti)
    ti.consume(TT.SEMICOLON, "Expect statement to end with ';'")
    return Print(value)


def expression(ti: TokenIter):
    return assignment(ti)


def logic_or(ti):
    left = logic_and(ti)
    while ti.match(TT.OR):
        operator = ti.previous()
        right = logic_and(ti)
        left = Logical(left, operator, right)
    return left


def logic_and(ti):
    left = ternary(ti)
    while ti.match(TT.AND):
        operator = ti.previous()
        right = ternary(ti)
        left = Logical(left, operator, right)
    return left


def assignment(ti):
    if ti.match(TT.FUN):
        return function(ti, "lambda")

    expr = logic_or(ti)

    if ti.match(TT.EQUAL):
        eql = ti.previous()
        value = assignment(ti)

        if type(expr) == Variable:
            name = expr.name
            return Assign(name, value)
        if type(expr) == Get:
            get = expr
            return Set(get.obj, get.name, value)

        raise Exception(f"invalid assignment target: {eql}")
    return expr


def ternary(ti: TokenIter):
    test = equality(ti)
    if not ti.match(TT.QUESTION):
        return test

    left = equality(ti)
    if not ti.match(TT.COLON):
        raise Exception("Expected colon for ternary operator")
    right = equality(ti)

    return Ternary(test, left, right)


def equality(ti):
    out = comparison(ti)
    while ti.match(TT.EQUAL_EQUAL, TT.BANG_EQUAL):
        out = Binary(out, ti.previous(), comparison(ti))
    return out


def comparison(ti):
    out = term(ti)
    while ti.match(TT.GREATER, TT.GREATER_EQUAL, TT.LESS, TT.LESS_EQUAL):
        out = Binary(out, ti.previous(), term(ti))
    return out


def term(ti):
    out = factor(ti)
    while ti.match(TT.PLUS, TT.MINUS):
        out = Binary(out, ti.previous(), factor(ti))

    return out


def factor(ti):
    out = unary(ti)
    while ti.match(TT.STAR, TT.SLASH, TT.MOD):
        out = Binary(out, ti.previous(), unary(ti))

    return out


def unary(ti):
    if ti.match(TT.BANG, TT.MINUS):
        return Unary(ti.previous(), unary(ti))

    return call(ti)


def call(ti):
    expr = primary(ti)
    while True:
        if ti.match(TT.LEFT_PAREN):
            expr = finishCall(ti, expr)
        elif ti.match(TT.DOT):
            name = ti.consume(TT.IDENTIFIER, "Expect property name after '.'")
            expr = Get(expr, name)
        else:
            break
    return expr


def finishCall(ti, callee):
    if ti.check(TT.RIGHT_PAREN):
        paren = ti.consume(TT.RIGHT_PAREN, "Expect ) after arguments")
        return Call(callee, paren, [])

    arguments = []
    while True:
        arguments.append(expression(ti))
        if not ti.match(TT.COMMA):
            break
    if len(arguments) > 255:
        error(ti.peek(), "Can't have more than 255 arguments")
    paren = ti.consume(TT.RIGHT_PAREN, "Expect ) after arguments")
    return Call(callee, paren, arguments)


def primary(ti: TokenIter):
    if ti.match(TT.FALSE):
        return Literal(False)
    if ti.match(TT.TRUE):
        return Literal(True)
    if ti.match(TT.NIL):
        return Literal(None)
    if ti.match(TT.THIS):
        return This(ti.previous())

    if ti.match(TT.STRING, TT.NUMBER):
        return Literal(ti.previous().literal)

    if ti.match(TT.LEFT_PAREN):
        expr = expression(ti)
        ti.consume(TT.RIGHT_PAREN, "Expect ')' after expression.")
        return Grouping(expr)

    if ti.match(TT.IDENTIFIER):
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
