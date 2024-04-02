from typing import List, Optional
from tokens import Token, TokenType, SINGLE_CHAR_LEXEMES


class Scanner:
    """Scans a string and returns tokens."""

    source: str
    start: int = 0
    current: int = 0
    line: int = 1
    tokens: List[Token]
    error: Optional[str] = None

    def __init__(self, source):
        self.source = source
        self.tokens = []

    def __repr__(self):
        return f"{self.line},{self.current}, {self.tokens}, {self.source}"

    def isAtEnd(self):
        return self.current >= len(self.source)

    def peek(self):
        if self.isAtEnd():
            return "\0"
        return self.source[self.current]

    def advance(self) -> str:
        """Advance the `current` counter by one and return the character at the current position."""
        out = self.source[self.current]
        self.current += 1
        return out

    def match(self, expected: str) -> bool:
        """
        Advance the `current` counter if the current character matches
        """
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def addToken(self, type: TokenType, literal: object = None):
        """ """
        lexeme = self.source[self.start : self.current]
        self.tokens.append(Token(type, lexeme, literal, self.line))

    def scanToken(self):  # -> tokens.Token:
        """Yields the next token."""
        char = self.advance()

        if char in SINGLE_CHAR_LEXEMES:
            self.addToken(TokenType(char))

        elif char == "!":
            if self.match("="):
                self.addToken(TokenType.BANG_EQUAL)
            else:
                self.addToken(TokenType.BANG)
        elif char == "=":
            if self.match("="):
                self.addToken(TokenType.EQUAL_EQUAL)
            else:
                self.addToken(TokenType.EQUAL)
        elif char == "<":
            if self.match("="):
                self.addToken(TokenType.LESS_EQUAL)
            else:
                self.addToken(TokenType.LESS)
        elif char == ">":
            if self.match("="):
                self.addToken(TokenType.GREATER_EQUAL)
            else:
                self.addToken(TokenType.GREATER)
        elif char == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.isAtEnd():
                    self.advance()
            else:
                self.addToken(TokenType.SLASH)
        elif char.isspace():
            if char == "\n":
                self.line += 1
        else:
            # TODO: Handle errors nicely
            print(self.line, f"Unexpected character found: {char}")

    def scanTokens(self) -> List[Token]:
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens