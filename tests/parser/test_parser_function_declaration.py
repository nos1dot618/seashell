from seashell.parser.ast_nodes import (
    AccessMember,
    FunctionCall,
    FunctionDeclaration,
    Parameter,
    Variable,
)
from seashell.parser.parser import parse


def test_function_declaration():
    program = parse(
        """
        function greet(name: string) {
            io.writeln(name)
        }
        """
    )

    function_declaration_statement = program.statements[0]
    assert isinstance(function_declaration_statement, FunctionDeclaration)

    assert function_declaration_statement.name == "greet"
    assert function_declaration_statement.parameters == [
        Parameter(name="name", type_annotation="string")
    ]
    assert function_declaration_statement.body == [
        FunctionCall(
            AccessMember(
                obj=Variable(name="io"),
                member="writeln",
            ),
            arguments=[Variable(name="name")],
        )
    ]
