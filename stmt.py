from expr import Expr, Variable
from tokens import Token
from typing import NamedTuple, Optional, Any, List

from abc import abstractmethod, ABC
from util import Visitable


class Stmt(Visitable):
    pass


class _Expression(NamedTuple):
    expression: Expr


class Expression(
    Stmt,
    _Expression,
):
    pass


class _Print(NamedTuple):
    expression: Expr


class Print(Stmt, _Print):
    pass


class _Var(NamedTuple):
    name: Token
    value: Optional[Expr]


class Var(Stmt, _Var):
    pass


class _Block(NamedTuple):
    statements: List[Stmt]


class Block(
    Stmt,
    _Block,
):
    pass


class _IfStmt(NamedTuple):
    condition: Expr
    thenBranch: Stmt
    elseBranch: Optional[Stmt]


class IfStmt(Stmt, _IfStmt):
    pass


class _WhileStmt(NamedTuple):
    condition: Expr
    body: Stmt


class WhileStmt(Stmt, _WhileStmt):
    pass


class BreakStmt(Stmt):
    pass


class _Function(NamedTuple):
    name: Optional[Token]
    params: List[Token]
    body: List[Stmt]


class Function(Expr, Stmt, _Function):
    pass


class _Return(NamedTuple):
    keyword: Token
    expression: Optional[Expr]


class Return(Stmt, _Return):
    pass


class _Class(NamedTuple):
    name: Token
    methods: List[Function]
    superclass: Optional[Variable]


class Class(Stmt, _Class):
    pass


class StmtVisitor(ABC):
    @abstractmethod
    def visitPrint(self, val: Print) -> Any:
        pass

    @abstractmethod
    def visitVar(self, val: Var) -> Any:
        pass

    @abstractmethod
    def visitExpression(self, val: Expression) -> Any:
        pass

    @abstractmethod
    def visitBlock(self, val: Block) -> Any:
        pass

    @abstractmethod
    def visitIfStmt(self, val: IfStmt) -> Any:
        pass

    @abstractmethod
    def visitWhileStmt(self, val: WhileStmt) -> Any:
        pass

    @abstractmethod
    def visitBreakStmt(self, val: None) -> Any:
        pass

    @abstractmethod
    def visitFunction(self, val: Function) -> Any:
        pass

    @abstractmethod
    def visitReturn(self, val: Return) -> Any:
        pass

    @abstractmethod
    def visitClass(self, val: Class) -> Any:
        pass
