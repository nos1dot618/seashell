from seashell.parser.ast_nodes import (
    AccessMember,
    FunctionCall,
    IfStatement,
    Program,
    String,
    Variable,
)
from seashell.parser.parser import parse


def test_if_statement():
    program = parse(
        """
        if enabled {
            io.writeln("hello")
        }
        """
    )
    assert isinstance(program, Program)

    if_statement = program.statements[0]
    assert isinstance(if_statement, IfStatement)

    assert if_statement.condition == Variable(name="enabled")
    assert if_statement.body == [
        FunctionCall(
            AccessMember(
                obj=Variable(name="io"),
                member="writeln",
            ),
            arguments=[String(value="hello")],
        )
    ]
