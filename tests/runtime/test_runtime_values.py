from seashell.parser.parser import parse
from seashell.runtime.interpreter import Interpreter
from seashell.runtime.values import NumberValue


def test_variable_assignment():
    program = parse(
        """
        x = 123
        """
    )

    interpreter = Interpreter()
    interpreter.run(program)

    value = interpreter.context.get_symbol("x")

    assert isinstance(value, NumberValue)
    assert value.value == 123


