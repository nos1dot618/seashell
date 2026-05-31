from pathlib import Path

from seashell.runtime.constants import ExitCode
from seashell.runtime.interpreter import Interpreter


def test_stdlib_integration(capsys):
    interpreter = Interpreter.drive(
        "examples/json_integration_test.cshl", str(Path.cwd())
    )

    assert interpreter.exitcode == ExitCode.SUCCESS

    _ = capsys.readouterr()
    assert not Path.exists(str(interpreter.context.get_symbol("root")))
