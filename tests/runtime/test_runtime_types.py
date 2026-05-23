from seashell.parser.parser import parse
from seashell.runtime.interpreter import Interpreter


def test_variable_type_mismatch_error(capsys):
    program = parse(
        """
        x: string = 123
        """
    )

    interpreter = Interpreter()
    interpreter.run(program)

    captured = capsys.readouterr()
    assert "error: expected type 'string' but got type 'number'\n" == captured.out


def test_function_call_parameter_type_mismatch_error(capsys):
    program = parse(
        """
        function foo(x: number) {
            io.writeln(x)
        }
        
        foo("hello")
        """
    )

    interpreter = Interpreter()
    interpreter.run(program)

    captured = capsys.readouterr()
    assert "error: expected type 'number' but got type 'string'\n" == captured.out
