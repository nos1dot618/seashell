import sys
from seashell.runtime.interpreter import Interpreter
from pathlib import Path


def main() -> None:
    if Interpreter.drive(sys.argv[1], str(Path.cwd())):
        exit(0)
    else:
        exit(1)
