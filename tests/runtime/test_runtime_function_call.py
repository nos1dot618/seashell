from seashell.runtime.interpreter import Interpreter


def test_io_write_exists():
    interpreter = Interpreter()

    assert "io" in interpreter.context.modules
    assert "write" in interpreter.context.modules["io"].functions
