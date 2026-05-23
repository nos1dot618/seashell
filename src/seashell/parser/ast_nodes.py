from dataclasses import dataclass

from rich.pretty import pretty_repr


class Node:
    pass


class Statement(Node):
    pass


class Expression(Node):
    pass


@dataclass
class Program(Node):
    statements: list[Statement]

    def __repr__(self):
        return "\n".join(pretty_repr(stmt) for stmt in self.statements)


@dataclass
class Assignment(Statement):
    name: str
    value: Expression
    type_annotation: str | None = None


@dataclass
class IfStatement(Statement):
    condition: Expression
    # TODO: Add then_clause and else_clause instead of just a body.
    body: list[Statement]


@dataclass
class Parameter(Node):
    name: str
    type_annotation: str | None = None


@dataclass
class FunctionDeclaration(Statement):
    name: str
    parameters: list[Parameter]
    body: list[Statement]


@dataclass
class ForStatement(Node):
    variable_name: str
    iterable: Expression
    body: list[Node]


@dataclass
class BreakStatement(Node):
    pass


@dataclass
class ContinueStatement(Node):
    pass


@dataclass
class ReturnStatement(Node):
    value: Expression | None


@dataclass
class String(Expression):
    value: str


@dataclass
class Number(Expression):
    value: int


@dataclass
class Variable(Expression):
    name: str


@dataclass
class FunctionCall(Statement, Expression):
    callee: Expression
    arguments: list[Expression]


@dataclass
class AccessMember(Expression):
    object: Expression
    member: str
