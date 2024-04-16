from expr import Expr
from tokens import Token
from typing import NamedTuple, Optional, Any, List

from abc import abstractmethod, ABC
from util import Visitable


class Stmt(Visitable):
    pass


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


class _WhileStmt(NamedTuple):
    condition: Expr
    body: Stmt


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

    @abstractmethod
    def visitWhileStmt(self, val: _WhileStmt) -> Any:
        pass


class Var(Stmt, _Var):
    pass


class Print(Stmt, _Print):
    pass


class Expression(
    Stmt,
    _Expression,
):
    pass


class Block(
    Stmt,
    _Block,
):
    pass


class IfStmt(Stmt, _IfStmt):
    pass


class WhileStmt(Stmt, _WhileStmt):
    pass
