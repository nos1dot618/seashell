from seashell.parser.parser import parse
from seashell.runtime.interpreter import Interpreter


def test_user_function(capsys):
    program = parse(
        """
        function greet(name) {
            io.writeln(name)
        }

        greet("hello")
        """
    )

    interpreter = Interpreter()
    interpreter.run(program)

    captured = capsys.readouterr()
    assert "hello\n" == captured.out
