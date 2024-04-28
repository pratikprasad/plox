from typing import List, Dict, Union

from tokens import Token
from expr import ExprVisitor, Expr
from stmt import Function, StmtVisitor, Stmt
from interpreter import Interpreter
from logging import error

from printer import ExprPrinter

prnt = ExprPrinter()


class Resolver(ExprVisitor, StmtVisitor):
    scopes: List[Dict[str, bool]]
    interpreter: Interpreter

    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []

    def beginScope(self):
        self.scopes.append({})

    def endScope(self):
        self.scopes.pop()

    def resolve(self, val: Union[List[Stmt], Stmt, Expr]):
        if isinstance(val, List):
            for v in val:
                v.visit(self)
        else:
            val.visit(self)

    def visitBlock(self, val):
        self.beginScope()
        self.resolve(val.statements)
        self.endScope()

    def declare(self, val: Token):
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        scope[val.lexeme] = False

    def define(self, val: Token):
        if len(self.scopes) == 0:
            return
        self.scopes[-1][val.lexeme] = True

    def visitVar(self, val):
        self.declare(val.name)
        if val.value is not None:
            self.resolve(val.value)
        self.define(val.name)

    def resolveLocal(self, val: Expr, name: Token):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(val, len(self.scopes) - i - 1)
                return

    def visitVariable(self, val):
        if (
            len(self.scopes) > 0
            and val.name.lexeme in self.scopes[-1]
            and self.scopes[-1][val.name.lexeme] == False
        ):
            error(val.name, "Can't read local variable in its own initalizer")
        self.resolveLocal(val, val.name)

    def visitAssign(self, val):
        self.resolve(val.value)
        self.resolveLocal(val, val.name)

    def resolveFunction(self, val: Function):
        self.beginScope()
        for param in val.params:
            self.declare(param)
            self.define(param)
        self.resolve(val.body)
        self.endScope()

    def visitFunction(self, val):
        if val.name:
            self.declare(val.name)
            self.define(val.name)
        self.resolveFunction(val)

    def visitExpression(self, val):
        self.resolve(val.expression)

    def visitIfStmt(self, val):
        self.resolve(val.condition)
        self.resolve(val.thenBranch)
        if val.elseBranch:
            self.resolve(val.elseBranch)

    def visitClass(self, val):
        self.declare(val.name)
        self.define(val.name)

    def visitPrint(self, val):
        self.resolve(val.expression)

    def visitReturn(self, val):
        if val.expression:
            self.resolve(val.expression)

    def visitWhileStmt(self, val):
        self.resolve(val.condition)
        self.resolve(val.body)

    def visitBinary(self, val):
        self.resolve(val.left)
        self.resolve(val.right)

    def visitCall(self, val):
        self.resolve(val.callee)
        for arg in val.arguments:
            self.resolve(arg)

    def visitGrouping(self, val):
        self.resolve(val.expr)

    def visitGet(self, val):
        self.resolve(val.obj)

    def visitSet(self, val):
        self.resolve(val.val)
        self.resolve(val.obj)

    def visitBreakStmt(self, val):
        return

    def visitLiteral(self, val):
        return

    def visitLogical(self, val):
        self.resolve(val.left)
        self.resolve(val.right)

    def visitTernary(self, val):
        self.resolve(val.left)
        self.resolve(val.test)
        self.resolve(val.right)

    def visitUnary(self, val):
        self.resolve(val.value)


if __name__ == "__main__":
    r = Resolver(Interpreter())
