from seashell.runtime.interpreter import Interpreter


def test_io_write_exists():
    interpreter = Interpreter()

    assert "io" in interpreter.context.scopes[0]
    assert "write" in interpreter.context.get_symbol("io").get_members()
