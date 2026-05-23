from seashell.parser.parser import parse
from seashell.runtime.interpreter import Interpreter
from seashell.runtime.values import StringValue


def test_assignment():
    program = parse(
        """
        name = "hello"
        """
    )

    interpreter = Interpreter()
    interpreter.run(program)

    assert interpreter.context.symbols["name"] == StringValue("hello")
