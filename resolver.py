from typing import List, Dict, Union, Optional
from enum import Enum

from tokens import Token
from expr import ExprVisitor, Expr
from stmt import Function, StmtVisitor, Stmt
from interpreter import Interpreter
from logging import error

from printer import ExprPrinter

prnt = ExprPrinter()


class ClassType(Enum):
    NONE = None
    CLASS = "CLASS"


class Resolver(ExprVisitor, StmtVisitor):
    scopes: List[Dict[str, bool]]
    interpreter: Interpreter
    currentFunction = None

    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.currentClass = ClassType.NONE

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

    # TODO: function type should be an enum
    def resolveFunction(self, val: Function, type: Optional[str] = None):
        self.currentFunction = type

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
        enclosingClass = self.currentClass
        self.currentClass = ClassType.CLASS
        self.declare(val.name)
        self.define(val.name)

        if val.superclass is not None:
            if val.superclass.name.lexeme == val.name.lexeme:
                raise Exception(
                    f"A class cannot inherit from itself: {val.name.lexeme}"
                )
            self.resolve(val.superclass)

        if val.superclass is not None:
            self.beginScope()
            self.scopes[-1]["super"] = True

        self.beginScope()
        self.scopes[-1]["this"] = True

        for method in val.methods:
            kind = "method"
            if method.name and method.name.lexeme == "init":
                kind = "initialzer"
            self.resolveFunction(method, kind)
        self.endScope()

        if val.superclass is not None:
            self.endScope()

        self.currentClass = enclosingClass

    def visitPrint(self, val):
        self.resolve(val.expression)

    def visitSuper(self, val):
        self.resolveLocal(val, val.keyword)

    def visitReturn(self, val):
        if self.currentFunction is None:
            raise Exception(
                "cant return from top-level"
            )  # should this be error vs runtime code?
        if val.expression is not None:
            if self.currentFunction == "initialzer":
                raise Exception("can't return a value from an initializer")
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

    def visitThis(self, val):
        if self.currentClass == ClassType.NONE:
            error("Can't use 'this' outside of a class")

        self.resolveLocal(val, val.keyword)

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
