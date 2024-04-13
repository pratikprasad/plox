from expr import Expr
from tokens import Token
from typing import NamedTuple, Optional, Any, List

from abc import abstractmethod, ABC


class Stmt(ABC):

    @abstractmethod
    def visit(self, vis):
        raise Exception("Stmt visit called")


class _Expression(NamedTuple):
    expression: Expr


class _Print(NamedTuple):
    expression: Expr


class _Var(NamedTuple):
    name: Token
    value: Optional[Expr]


class _Block(NamedTuple):
    statements: List[Stmt]


class StmtVisitor(ABC):
    @abstractmethod
    def visitPrint(self, val: _Print) -> Any:
        pass

    @abstractmethod
    def visitVar(self, val: _Var) -> Any:
        pass

    @abstractmethod
    def visitExpression(self, val: _Expression) -> Any:
        pass

    @abstractmethod
    def visitBlock(self, val: _Block) -> Any:
        pass


class Var(_Var, Stmt):
    def visit(self, vis: StmtVisitor):
        return vis.visitVar(self)


class Print(_Print, Stmt):
    def visit(self, vis: StmtVisitor):
        return vis.visitPrint(self)


class Expression(_Expression, Stmt):
    def visit(self, vis: StmtVisitor):
        return vis.visitExpression(self)


class Block(_Block, Stmt):
    def visit(self, vis: StmtVisitor):
        return vis.visitBlock(self)
