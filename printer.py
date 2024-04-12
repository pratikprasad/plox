from expr import ExprVisitor
from stmt import StmtVisitor
from parser import Parse


class ExprPrinter(ExprVisitor, StmtVisitor):
    """"""

    def visitLiteral(self, val):
        if type(val.value) == str:
            return f"'{val.value}'"
        return val.value

    def visitGrouping(self, val):
        return f"(group {val.expr.visit(self)})"

    def visitUnary(self, val):
        return f"({val.operator.lexeme} {val.value.visit(self)})"

    def visitBinary(self, val):
        return f"({val.operator.lexeme} {val.left.visit(self)} {val.right.visit(self)})"

    def visitTernary(self, val):
        return (
            f"(? {val.test.visit(self)} {val.left.visit(self)} {val.right.visit(self)})"
        )

    def visitVariable(self, val):
        return f"(var {val.name})"

    def visitPrint(self, val):
        return f"(print {val.expression.visit(self)})"

    def visitExpression(self, val):
        return val.expression.visit(self)

    def visitVar(self, val):
        value = None
        if val.value:
            value = val.value.visit(self)
        return f"(var {val.name.lexeme} {value})"

    def visitAssign(self, val):
        return f"(assign {val.name.lexeme} {val.value.visit(self)})"


def PolishNotation(expression):
    """Parses text and returns the polish notation"""
    text = expression
    if expression[-1] != ";":
        text += ";"
    expr = Parse(text)[0]
    return expr.visit(ExprPrinter())


if __name__ == "__main__":
    print(PolishNotation("1+2+3;"))
    print(PolishNotation("a = 3;"))
