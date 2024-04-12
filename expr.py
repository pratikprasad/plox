from typing import Any, NamedTuple

from tokens import Token
from abc import ABC, abstractmethod


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


class Variable(_Variable, Expr):
    def visit(self, vis: ExprVisitor):
        return vis.visitVariable(self)


class Binary(Expr, _Binary):

    def visit(self, vis: ExprVisitor):
        return vis.visitBinary(self)


class Literal(Expr, _Literal):

    def visit(self, vis: ExprVisitor):
        return vis.visitLiteral(self)


class Ternary(Expr, _Ternary):
    def visit(self, vis: ExprVisitor):
        return vis.visitTernary(self)


class Grouping(Expr, _Grouping):
    def visit(self, vis: ExprVisitor):
        return vis.visitGrouping(self)


class Unary(Expr, _Unary):
    def visit(self, vis: ExprVisitor):
        return vis.visitUnary(self)
