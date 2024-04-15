from expr import Expr
from tokens import Token
from typing import NamedTuple, Optional, Any, List

from abc import abstractmethod, ABC
from util import Visitable


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


class _IfStmt(NamedTuple):
    condition: Expr
    thenBranch: Stmt
    elseBranch: Optional[Stmt]


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

    @abstractmethod
    def visitIfStmt(self, val: _IfStmt) -> Any:
        pass


class Var(Visitable, Stmt, _Var):
    pass


class Print(Visitable, Stmt, _Print):
    pass


class Expression(
    Visitable,
    Stmt,
    _Expression,
):
    pass


class Block(
    Visitable,
    Stmt,
    _Block,
):
    pass


class IfStmt(Visitable, Stmt, _IfStmt):
    pass
