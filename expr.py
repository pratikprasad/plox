from typing import Any, NamedTuple

from tokens import Token
from abc import ABC, abstractmethod
from util import Visitable


class Expr(ABC):
    """"""

    @abstractmethod
    def visit(self, vis):
        pass


class _Literal(NamedTuple):
    value: Any


class _Unary(NamedTuple):
    operator: Token  # ! or -
    value: Expr


class _Grouping(NamedTuple):
    expr: Expr


class _Ternary(NamedTuple):
    test: Expr
    left: Expr
    right: Expr


class _Binary(NamedTuple):
    left: Expr
    operator: Token
    right: Expr


class _Variable(NamedTuple):
    name: Token


class _Assign(NamedTuple):
    name: Token
    value: Expr


class ExprVisitor(ABC):

    @abstractmethod
    def visitLiteral(self, val: _Literal) -> Any:
        pass

    @abstractmethod
    def visitGrouping(self, val: _Grouping) -> Any:
        pass

    @abstractmethod
    def visitUnary(self, val: _Unary) -> Any:
        pass

    @abstractmethod
    def visitBinary(self, val: _Binary) -> Any:
        pass

    @abstractmethod
    def visitTernary(self, val: _Ternary) -> Any:
        pass

    @abstractmethod
    def visitVariable(self, val: _Variable) -> Any:
        pass

    @abstractmethod
    def visitAssign(self, val: _Assign) -> Any:
        pass


class Variable(Visitable, Expr, _Variable):
    pass


class Binary(Visitable, Expr, _Binary):
    pass


class Literal(Visitable, Expr, _Literal):
    pass


class Ternary(Visitable, Expr, _Ternary):
    pass


class Grouping(Visitable, Expr, _Grouping):
    pass


class Unary(Visitable, Expr, _Unary):
    pass


class Assign(Visitable, Expr, _Assign):
    pass
