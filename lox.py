import sys
from interpreter import Interpreter
from parser import Parse
from resolver import Resolver


def err(line, message):
    print(f"[line {line}] Error where: {message}")


def run(content):
    inpr = Interpreter()
    resolver = Resolver(inpr)
    program = Parse(content)
    resolver.resolve(program)
    for line in program:
        line.visit(inpr)


def runFile(filename):
    with open(filename) as contents:
        data = contents.read()
        run(data)


def runPrompt():
    inpr = Interpreter()

    while True:
        try:
            line = input("> ")
            expr = Parse(line)[0]
            out = expr.visit(inpr)
            if out is not None:
                print(out)
        except Exception as e:
            print(e)


args = sys.argv[1:]
if len(args) > 1:
    print("Usage: plox [script]")
    exit(64)

if len(args) == 1:
    runFile(args[0])
elif len(args) < 1:
    runPrompt()
