from operator import attrgetter
from expr import Expr
from tokens import Token
from typing import NamedTuple, Optional


class Stmt:
    pass

    def execute(self) -> None:
        raise Exception("Not implemented")


class _Expression(NamedTuple):
    expression: Expr


class Expression(_Expression, Stmt):
    attrgetter("expression")

    def __repr__(self):
        return f"(expression {self.expression})"

    def execute(self) -> None:
        self.expression.evaluate()


class _Print(NamedTuple):
    expression: Expr


class Print(_Print, Stmt):
    def __repr__(self):
        return f"(print {self.expression})"

    def execute(self) -> None:
        print(str(self.expression.evaluate()))


class _Var(NamedTuple):
    name: Token
    value: Optional[Expr]


class Var(_Var, Stmt):
    def __repr__(self):
        return f"(var {self.name.lexeme} {self.value})"
