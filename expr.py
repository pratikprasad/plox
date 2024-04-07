from tokens import Token, TokenType
from typing import Any
from dataclasses import dataclass


class Expr:
    """"""

    def evaluate(self):
        raise Exception("not implemented")


@dataclass(frozen=True)
class Literal(Expr):
    value: Any

    def __repr__(self):
        return repr(self.value)

    def evaluate(self):
        return self.value


@dataclass(frozen=True)
class Unary(Expr):
    operator: Token  # ! or -
    value: Expr

    def __repr__(self):
        return f"({self.operator.lexeme} {repr(self.value)})"

    def evaluate(self):
        """
        if operator == '-' and
        if value.type == number then return - number
        """
        if self.operator.type not in {TokenType.MINUS, TokenType.BANG}:
            raise Exception(f"invalid unary: {self.operator} {self.value}")

        value = self.value.evaluate()
        if self.operator.type == TokenType.MINUS:
            if not isinstance(value, float):
                raise Exception(f"not able to negate number {self} == {value}")
            else:
                return 0 - value

        if self.operator.type == TokenType.BANG:
            if not isinstance(value, bool):
                raise Exception(f"not able to negate non-boolean {self} == {value}")
            return not value


@dataclass(frozen=True)
class Grouping(Expr):
    expr: Expr

    def __repr__(self):
        return f"(group {repr(self.expr)})"

    def evaluate(self):
        return self.expr.evaluate()


@dataclass(frozen=True)
class Ternary(Expr):
    test: Expr
    left: Expr
    right: Expr

    def __repr__(self):
        return f"(? {repr(self.test)} {repr(self.left)} {repr(self.right)})"


@dataclass(frozen=True)
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def __repr__(self):
        return f"({self.operator.lexeme} {repr(self.left)} {repr(self.right)})"
