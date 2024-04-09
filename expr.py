from typing import Any, NamedTuple
import operator

from tokens import Token, TokenType


class RuntimeException(Exception):
    pass


def isTruthy(value):
    if value is None:
        return False
    if type(value) == bool:
        return value
    return True


class Expr:
    """"""

    def evaluate(self) -> Any:
        raise RuntimeException("Expression evaluation not implemented")


class _Literal(NamedTuple):
    value: Any


class Literal(Expr, _Literal):

    def __repr__(self):
        return repr(self.value)

    def evaluate(self):
        return self.value


class _Unary(NamedTuple):
    operator: Token  # ! or -
    value: Expr


class Unary(Expr, _Unary):

    def __repr__(self):
        return f"({self.operator.lexeme} {repr(self.value)})"

    def evaluate(self):
        """
        if operator == '-' and
        if value.type == number then return - number
        """
        if self.operator.type not in {TokenType.MINUS, TokenType.BANG}:
            raise RuntimeException(f"invalid unary: {self.operator} {self.value}")

        value = self.value.evaluate()
        if self.operator.type == TokenType.MINUS:
            if not isinstance(value, float):
                raise RuntimeException(f"not able to negate number {self} == {value}")
            else:
                return 0 - value

        if self.operator.type == TokenType.BANG:
            return not isTruthy(value)

        raise RuntimeException("Unary expression not implemented")


class _Grouping(NamedTuple):
    expr: Expr


class Grouping(Expr, _Grouping):

    def __repr__(self):
        return f"(group {repr(self.expr)})"

    def evaluate(self):
        return self.expr.evaluate()


class _Ternary(NamedTuple):
    test: Expr
    left: Expr
    right: Expr


class Ternary(Expr, _Ternary):

    def __repr__(self):
        return f"(? {repr(self.test)} {repr(self.left)} {repr(self.right)})"

    def evaluate(self):
        if isTruthy(self.test.evaluate()):
            return self.left.evaluate()
        else:
            return self.right.evaluate()


def plus(left, right):
    if type(left) == type(right) == float:
        return operator.add(left, right)
    if type(left) == str and type(right) in [float, str]:
        return f"{left}{right}"

    raise RuntimeException(f"Unknown behavior for `+` with values: {left} and {right}")


def div(left, right):
    if right == 0:
        raise RuntimeException("divide by zero is not allowed")
    return operator.truediv(left, right)


BINARY_OPERATIONS = {
    TokenType.PLUS: plus,
    TokenType.MINUS: operator.sub,
    TokenType.STAR: operator.mul,
    TokenType.MOD: operator.mod,
    TokenType.SLASH: div,
    TokenType.BANG_EQUAL: operator.ne,
    TokenType.EQUAL_EQUAL: operator.eq,
    TokenType.LESS: operator.lt,
    TokenType.LESS_EQUAL: operator.le,
    TokenType.GREATER: operator.gt,
    TokenType.GREATER_EQUAL: operator.ge,
}
NUMBER_BINARY_OPERATIONS = {
    TokenType.MINUS,
    TokenType.STAR,
    TokenType.MOD,
    TokenType.SLASH,
    TokenType.LESS,
    TokenType.LESS_EQUAL,
    TokenType.GREATER,
    TokenType.GREATER_EQUAL,
}


class _Binary(NamedTuple):
    left: Expr
    operator: Token
    right: Expr


class Binary(Expr, _Binary):

    def __repr__(self):
        return f"({self.operator.lexeme} {repr(self.left)} {repr(self.right)})"

    def evaluate(self):
        if self.operator.type not in BINARY_OPERATIONS:
            raise RuntimeException(f"Binary operation not implemented: {self.operator}")

        left = self.left.evaluate()
        right = self.right.evaluate()

        if self.operator.type in NUMBER_BINARY_OPERATIONS:
            if type(left) is not float:
                raise RuntimeException(f"Non-float in number operation: {left}")

            if type(right) is not float:
                raise RuntimeException(f"Non-float in number operation: {right}")

        opr = BINARY_OPERATIONS[self.operator.type]
        return opr(left, right)
