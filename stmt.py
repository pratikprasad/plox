from expr import Expr
from typing import NamedTuple


class Stmt:
    pass

    def execute(self) -> None:
        raise Exception("Not implemented")


class _Expression(NamedTuple):
    expression: Expr


class Expression(_Expression, Stmt):
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
