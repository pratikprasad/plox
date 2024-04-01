import sys


def err(line, message):
    print(f"[line {line}] Error where: {message}")


def run(content):
    print(content)


def runFile(filename):
    with open(filename) as contents:
        data = contents.read()
        run(data)


def runPrompt():
    while True:
        line = input("> ")
        run(line)
    print("Repl goes here")


args = sys.argv[1:]
if len(args) > 1:
    print("Usage: plox [script]")
    exit(64)

if len(args) == 1:
    runFile(args[0])
elif len(args) < 1:
    runPrompt()
