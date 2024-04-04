from expr import *
from tokens import *

expr = Binary(
    Unary(Token.fromTokenType(TokenType.MINUS, 1), Literal(123)),
    Token.fromTokenType(TokenType.STAR, 1),
    Grouping(Literal(45.67)),
)

assert repr(expr) == "(* (- 123) (group 45.67))", "AST Classes broken"
