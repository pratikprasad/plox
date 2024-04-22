from typing import Any, List, NamedTuple

from tokens import Token
from abc import ABC, abstractmethod
from util import Visitable


class Expr(Visitable):
    pass


class _Literal(NamedTuple):
    value: Any


class Literal(Expr, _Literal):
    pass


class _Call(NamedTuple):
    callee: Expr
    paren: Token
    arguments: List[Expr]


class Call(Expr, _Call):
    pass


class _Unary(NamedTuple):
    operator: Token  # ! or -
    value: Expr


class Unary(Expr, _Unary):
    pass


class _Grouping(NamedTuple):
    expr: Expr


class Grouping(Expr, _Grouping):
    pass


class _Ternary(NamedTuple):
    test: Expr
    left: Expr
    right: Expr


class Ternary(Expr, _Ternary):
    pass


class _Binary(NamedTuple):
    left: Expr
    operator: Token
    right: Expr


class Binary(Expr, _Binary):
    pass


class _Variable(NamedTuple):
    name: Token


class Variable(Expr, _Variable):
    pass


class _Assign(NamedTuple):
    name: Token
    value: Expr


class Assign(Expr, _Assign):
    pass


class _Logical(NamedTuple):
    left: Expr
    operator: Token
    right: Expr


class Logical(Expr, _Logical):
    pass


class ExprVisitor(ABC):

    @abstractmethod
    def visitLiteral(self, val: Literal) -> Any:
        pass

    @abstractmethod
    def visitGrouping(self, val: Grouping) -> Any:
        pass

    @abstractmethod
    def visitUnary(self, val: Unary) -> Any:
        pass

    @abstractmethod
    def visitBinary(self, val: Binary) -> Any:
        pass

    @abstractmethod
    def visitTernary(self, val: Ternary) -> Any:
        pass

    @abstractmethod
    def visitVariable(self, val: Variable) -> Any:
        pass

    @abstractmethod
    def visitAssign(self, val: Assign) -> Any:
        pass

    @abstractmethod
    def visitLogical(self, val: Logical) -> Any:
        pass

    @abstractmethod
    def visitCall(self, val: Call) -> Any:
        pass
