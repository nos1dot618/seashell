import sys

from seashell.parser.ast_nodes import Program
from seashell.parser.parser import parse
from seashell.runtime.interpreter import Interpreter


def main() -> None:
    filepath: str = sys.argv[1]
    with open(filepath) as file:
        source: str = file.read()

    program: Program = parse(source)
    interpreter = Interpreter()

    interpreter.run(program)
