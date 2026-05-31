import sys
from seashell.runtime.interpreter import Interpreter
from pathlib import Path


def main() -> None:
    interpreter = Interpreter.drive(sys.argv[1], str(Path.cwd()))
    exit(interpreter.exitcode.value)
