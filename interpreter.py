import time
import operator
from abc import ABC, abstractmethod
from typing import List, Any, Dict, NamedTuple

from environment import Environment, Undefined
from expr import ExprVisitor, Expr
from util import ToDoException
from stmt import StmtVisitor, Function, Block
from tokens import TokenType, Token
from util import BreakException, RuntimeException, ReturnException


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
    locals: Dict[Expr, int]
    """"""

    def __init__(self):
        self.locals = {}
        self.globals = Environment()
        self.env = self.globals
        self.globals.define("clock", ClockFn())

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
        return self.lookupVariable(val.name, val)

    def lookupVariable(self, name: Token, expr: Expr):
        depth = None
        if expr in self.locals:
            depth = self.locals[expr]
        if depth is None:
            return self.globals.get(name.lexeme)

        return self.env.getAt(depth, name.lexeme)

    def visitVar(self, val):
        value = Undefined
        if val.value:
            value = val.value.visit(self)
        self.env.define(val.name.lexeme, value)

    def visitAssign(self, val):
        value = val.value.visit(self)
        dist = self.locals.get(val)
        if dist is not None:
            self.env.assignAt(dist, val.name, value)
        else:
            self.globals.assign(val.name.lexeme, value)

    def visitBlock(self, val):
        self.executeBlock(val, Environment(self.env))

    def executeBlock(self, val, env):
        prior = self.env
        try:
            self.env = env
            for stmt in val.statements:
                stmt.visit(self)
        finally:
            self.env = prior

    def visitClass(self, val):
        superclass = None

        if val.superclass is not None:
            superclass = val.superclass.visit(self)
            if type(superclass) is not LoxClass:
                raise RuntimeException("superclass must be a class")
            self.env.define("super", superclass)

        self.env.define(val.name.lexeme, None)
        methods = dict(
            [
                (
                    method.name and method.name.lexeme or "",
                    LoxFunction(
                        method,
                        self.env,
                        bool(method.name and method.name.lexeme == "init"),
                    ),
                )
                for method in val.methods
            ]
        )
        klass = LoxClass(val.name.lexeme, methods, superclass)
        if (
            superclass is not None and self.env and self.env.parent
        ):  # lot of defensiveness
            self.env = self.env.parent

        self.env.assign(val.name.lexeme, klass)

    def visitSuper(self, val):
        distance = self.locals.get(val, 0)
        superclass = self.env.getAt(distance, "super")
        obj = self.env.getAt(distance - 1, "this")
        method = superclass.findMethod(val.method.lexeme)
        if method is None:
            raise Exception(f"undefined method: {method}")

        return method.bind(obj)

    def visitIfStmt(self, val):
        if isTruthy(val.condition.visit(self)):
            return val.thenBranch.visit(self)
        if val.elseBranch is not None:
            val.elseBranch.visit(self)

    def visitLogical(self, val):
        left = val.left.visit(self)
        if val.operator.type == TokenType.OR and isTruthy(left):
            return left
        if val.operator.type == TokenType.AND and not isTruthy(left):
            return left
        return val.right.visit(self)

    def visitWhileStmt(self, val):
        while isTruthy(val.condition.visit(self)):
            try:
                val.body.visit(self)
            except BreakException as _:
                return

    def visitBreakStmt(self, val):
        raise BreakException()

    def visitCall(self, val):
        callee = val.callee.visit(self)
        args = [arg.visit(self) for arg in val.arguments]

        callFunc = getattr(callee, "call", None)
        arityFunc = getattr(callee, "arity")
        if callFunc is None or arityFunc is None:
            raise RuntimeException("Can only call functions and classes")
        if arityFunc() != len(args):
            # TODO: more helpful instruction
            raise RuntimeException("Wrong arity for function")

        return callFunc(self, args)

    def visitFunction(self, val):
        fn = LoxFunction(val, self.env)
        if val.name is not None:
            self.env.define(val.name.lexeme, fn)
        return fn

    def visitReturn(self, val):
        value = None
        if val.expression is not None:
            value = val.expression.visit(self)
        raise ReturnException(value)

    def visitGet(self, val):
        obj = val.obj.visit(self)
        if type(obj) is not LoxInstance:
            raise RuntimeError("Only instances can have proerties")

        return obj.get(val.name)

    def visitSet(self, val):
        obj = val.obj.visit(self)
        if type(obj) != LoxInstance:
            raise RuntimeError("Only instances have fields")
        value = val.val.visit(self)
        obj.set(val.name, value)
        return val

    def visitThis(self, val):
        return self.lookupVariable(val.keyword, val)

    def resolve(self, expr: Expr, depth: int):
        self.locals[expr] = depth


if __name__ == "__main__":
    inpr = Interpreter()


class LoxCallable(ABC):
    @abstractmethod
    def arity(self) -> int:
        raise Exception("not implemented")

    @abstractmethod
    def call(self, inpr: Interpreter, args: List[Any]) -> Any:
        raise Exception("not implemented")


class ClockFn(LoxCallable):
    def arity(self):
        return 0

    def call(self, inpr, args):
        return time.time_ns()


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function, closure: Environment, isintializer=False):
        self.declaration = declaration
        self.closure = closure
        self.isintializer = False

    def arity(self):
        return len(self.declaration.params)

    def call(self, inpr, args):
        env = Environment(self.closure)

        for i in range(self.arity()):
            env.define(self.declaration.params[i].lexeme, args[i])

        try:
            inpr.executeBlock(Block(self.declaration.body), env)
        except ReturnException as e:
            if self.isintializer:
                return self.closure.getAt(0, "this")
            return e.value

    def bind(self, instance):
        env = Environment(self.closure)
        env.define("this", instance)
        # raise Exception(str(env.data))
        return LoxFunction(self.declaration, env, self.isintializer)


class _LoxClass(NamedTuple):
    name: str
    methods: Dict[str, LoxFunction]
    superclass: Any


class LoxClass(_LoxClass, LoxCallable):
    def __repr__(self):
        return self.name

    def arity(self):
        initializer = self.findMethod("init")
        if initializer is None:
            return 0
        return initializer.arity()

    def call(self, inpr, args):
        instance = LoxInstance(self, {})
        initializer = self.findMethod("init")
        if initializer is not None:
            initializer.bind(instance).call(inpr, args)
        return instance

    def findMethod(self, name: str):
        if name in self.methods:
            return self.methods.get(name, None)
        if self.superclass is not None:
            return self.superclass.findMethod(name)


class _LoxInstance(NamedTuple):
    klass: LoxClass
    fields: Dict[str, Any]


class LoxInstance(_LoxInstance):

    def __repr__(self):
        return f"{self.klass.name} instance"

    def get(self, name: Token) -> Any:
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        method = self.klass.findMethod(name.lexeme)
        if method is not None:
            return method.bind(self)

        print(name, self.fields, self.klass.methods)
        raise RuntimeError(
            f"Field '{name.lexeme}' is not in class instance of {self.klass.name}"
        )

    def set(self, name: Token, value: Any):
        self.fields[name.lexeme] = value
