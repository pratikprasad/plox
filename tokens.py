from typing import NamedTuple

from enum import Enum


class TokenType(Enum):
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    COMMA = ","
    DOT = "."
    MINUS = "-"
    PLUS = "+"
    SEMICOLON = ";"
    SLASH = "/"
    STAR = "*"
    QUESTION = "?"
    COLON = ":"
    MOD = "%"

    BANG = "!"
    BANG_EQUAL = "!="
    EQUAL = "="
    EQUAL_EQUAL = "=="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="

    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"

    AND = "and"
    BREAK = "break"
    CLASS = "class"
    ELSE = "else"
    FALSE = "false"
    FOR = "for"
    FUN = "fun"
    IF = "if"
    NIL = "nil"
    OR = "or"
    PRINT = "print"
    RETURN = "return"
    SUPER = "super"
    THIS = "this"
    TRUE = "true"
    VAR = "var"
    WHILE = "while"
    EOF = ""


SINGLE_CHAR_LEXEMES = {
    tp.value
    for tp in [
        TokenType.LEFT_PAREN,
        TokenType.RIGHT_PAREN,
        TokenType.LEFT_BRACE,
        TokenType.RIGHT_BRACE,
        TokenType.COMMA,
        TokenType.DOT,
        TokenType.MINUS,
        TokenType.PLUS,
        TokenType.SEMICOLON,
        TokenType.STAR,
        TokenType.QUESTION,
        TokenType.COLON,
        TokenType.MOD,
    ]
}

RESERVED_KEYWORDS = {
    tp.value
    for tp in [
        TokenType.AND,
        TokenType.BREAK,
        TokenType.CLASS,
        TokenType.ELSE,
        TokenType.FALSE,
        TokenType.FOR,
        TokenType.FUN,
        TokenType.IF,
        TokenType.NIL,
        TokenType.OR,
        TokenType.PRINT,
        TokenType.RETURN,
        TokenType.SUPER,
        TokenType.THIS,
        TokenType.TRUE,
        TokenType.VAR,
        TokenType.WHILE,
    ]
}


class Token(NamedTuple):
    """A lexical token."""

    type: TokenType
    lexeme: str
    literal: object
    line: int

    @classmethod
    def fromTokenType(cls, t_type: TokenType, line: int = 1):
        return Token(t_type, t_type.value, None, line)
