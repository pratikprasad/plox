import sys
from parser import Parse


def err(line, message):
    print(f"[line {line}] Error where: {message}")


def run(content):
    program = Parse(content)
    for line in program:
        line.execute()


def runFile(filename):
    with open(filename) as contents:
        data = contents.read()
        run(data)


def runPrompt():
    while True:
        try:
            line = input("> ")
            run(line)
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
