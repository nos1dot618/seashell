from seashell.parser.ast_nodes import Assignment, Program, String
from seashell.parser.parser import parse


def test_assignment() -> None:
    program = parse('name = "John Doe"')
    assert isinstance(program, Program)

    assignment_statement = program.statements[0]
    assert isinstance(assignment_statement, Assignment)

    assert assignment_statement.name == "name"
    assert assignment_statement.value == String(value="John Doe")
