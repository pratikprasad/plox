from tokens import Token
from typing import Any
from dataclasses import dataclass


@dataclass
class Expr:
    """"""


@dataclass
class Literal(Expr):
    value: Any

    def __repr__(self):
        return repr(self.value)


@dataclass
class Grouping(Expr):
    expr: Expr

    def __repr__(self):
        return f"(group {repr(self.expr)})"


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def __repr__(self):
        return f"({self.operator.lexeme} {repr(self.left)} {repr(self.right)})"


@dataclass
class Unary(Expr):
    operator: Token
    value: Expr

    def __repr__(self):
        return f"({self.operator.lexeme} {repr(self.value)})"
