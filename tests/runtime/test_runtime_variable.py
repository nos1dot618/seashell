from seashell.parser.parser import parse
from seashell.runtime.interpreter import Interpreter


def test_assignment():
    program = parse(
        """
        name = "hello"
        """
    )

    interpreter = Interpreter()
    interpreter.run(program)

    assert interpreter.context.variables["name"] == "hello"
