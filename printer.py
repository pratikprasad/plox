from expr import ExprVisitor
from stmt import StmtVisitor
from parser import Parse


class ExprPrinter(ExprVisitor, StmtVisitor):
    """"""

    def visitLiteral(self, val):
        return str(val)

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
        return f"(var {val.name.lexeme} {val.value})"


def PolishNotation(expression):
    """Parses text and returns the polish notation"""
    expr = Parse(f"{expression};")[0]
    return expr.visit(ExprPrinter())


if __name__ == "__main__":
    print(PolishNotation("1+2+3"))
