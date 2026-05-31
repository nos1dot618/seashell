from seashell.parser.ast_nodes import (
    AccessMember,
    FunctionCall,
    Program,
    String,
    Variable,
)
from seashell.parser.parser import parse


def test_function_call():
    program = parse('io.writeln("hello")')
    assert isinstance(program, Program)

    function_call_statement = program.statements[0]
    assert isinstance(function_call_statement, FunctionCall)

    assert function_call_statement.callee == AccessMember(
        obj=Variable(name="io"),
        member="writeln",
    )
    assert function_call_statement.arguments == [String(value="hello")]
