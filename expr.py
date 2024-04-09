from tokens import Token, TokenType
from typing import Any
from dataclasses import dataclass
import operator


class Expr:
    """"""

    def evaluate(self) -> Any:
        raise Exception("not implemented")


@dataclass(frozen=True)
class Literal(Expr):
    value: Any

    def __repr__(self):
        return repr(self.value)

    def evaluate(self):
        return self.value


def isTruthy(value):
    if value is None:
        return False
    if type(value) == bool:
        return value
    return True


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
            return not isTruthy(value)

        raise Exception("not implemented")


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

    def evaluate(self):
        if isTruthy(self.test.evaluate()):
            return self.left.evaluate()
        else:
            return self.right.evaluate()


BINARY_OPERATIONS = {
    TokenType.PLUS: operator.add,
    TokenType.STAR: operator.mul,
    TokenType.MOD: operator.mod,
    TokenType.SLASH: operator.truediv,
    TokenType.BANG_EQUAL: operator.ne,
    TokenType.EQUAL_EQUAL: operator.eq,
    TokenType.LESS: operator.lt,
    TokenType.LESS_EQUAL: operator.le,
    TokenType.GREATER: operator.gt,
    TokenType.GREATER_EQUAL: operator.ge,
}


@dataclass(frozen=True)
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def __repr__(self):
        return f"({self.operator.lexeme} {repr(self.left)} {repr(self.right)})"

    def evaluate(self):
        if self.operator.type not in BINARY_OPERATIONS:
            raise Exception("not implemented")

        left = self.left.evaluate()
        right = self.right.evaluate()
        opr = BINARY_OPERATIONS[self.operator.type]
        return opr(left, right)
