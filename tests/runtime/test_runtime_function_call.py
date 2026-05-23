from seashell.runtime.interpreter import Interpreter


def test_io_write_exists():
    interpreter = Interpreter()

    assert "io" in interpreter.context.symbols
    assert "write" in interpreter.context.symbols["io"].get_members()
