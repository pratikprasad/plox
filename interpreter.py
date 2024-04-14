import operator

from environment import Environment, Undefined
from expr import ExprVisitor
from stmt import StmtVisitor
from tokens import TokenType
from util import RuntimeException


def isTruthy(value):
    if value is None:
        return False
    if type(value) == bool:
        return value
    return True


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


class Interpreter(ExprVisitor, StmtVisitor):
    """"""

    def __init__(self):
        self.env = Environment()

    def visitLiteral(self, val):
        return val.value

    def visitGrouping(self, val):
        return val.expr.visit(self)

    def visitUnary(self, val):
        """
        if operator == '-' and
        if value.type == number then return - number
        """
        if val.operator.type not in {TokenType.MINUS, TokenType.BANG}:
            raise RuntimeException(f"invalid unary: {val.operator} {val.value}")

        value = val.value.visit(self)
        if val.operator.type == TokenType.MINUS:
            if not isinstance(value, float):
                raise RuntimeException(f"not able to negate number {val} == {value}")
            else:
                return 0 - value

        if val.operator.type == TokenType.BANG:
            return not isTruthy(value)

        raise RuntimeException("Unary expression not implemented")

    def visitBinary(self, val):
        if val.operator.type == TokenType.COMMA:
            val.left.visit(self)
            return val.right.visit(self)

        if val.operator.type not in BINARY_OPERATIONS:
            raise RuntimeException(f"Binary operation not implemented: {val.operator}")

        left = val.left.visit(self)
        right = val.right.visit(self)

        if val.operator.type in NUMBER_BINARY_OPERATIONS:
            if type(left) is not float:
                raise RuntimeException(f"Non-float in number operation: {left}")

            if type(right) is not float:
                raise RuntimeException(f"Non-float in number operation: {right}")

        opr = BINARY_OPERATIONS[val.operator.type]
        return opr(left, right)

    def visitTernary(self, val):
        if isTruthy(val.test.visit(self)):
            return val.left.visit(self)
        else:
            return val.right.visit(self)

    def visitPrint(self, val):
        print(val.expression.visit(self))

    def visitExpression(self, val):
        return val.expression.visit(self)

    def visitVariable(self, val):
        return self.env.get(val.name.lexeme)

    def visitVar(self, val):
        value = Undefined
        if val.value:
            value = val.value.visit(self)
        self.env.define(val.name.lexeme, value)

    def visitAssign(self, val):
        self.env.assign(val.name.lexeme, val.value.visit(self))

    def visitBlock(self, val):
        priorEnv = self.env
        env = Environment(self.env)
        try:
            self.env = env
            for stmt in val.statements:
                stmt.visit(self)

        except Exception as e:
            raise e
        self.env = priorEnv

    def visitIfStmt(self, val):
        if isTruthy(val.condition.visit(self)):
            return val.thenBranch.visit(self)
        if val.elseBranch is not None:
            val.elseBranch.visit(self)


if __name__ == "__main__":
    inpr = Interpreter()
