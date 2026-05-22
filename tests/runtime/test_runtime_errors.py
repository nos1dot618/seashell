from seashell.parser.parser import parse
from seashell.runtime.interpreter import Interpreter


def test_undefined_variable(capsys):
    program = parse(
        """
        io.writeln(name)
        """
    )

    interpreter = Interpreter()
    interpreter.run(program)

    captured = capsys.readouterr()
    assert "error: undefined variable 'name'" in captured.out
