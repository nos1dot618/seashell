from dataclasses import dataclass
from typing import Any

from rich.pretty import pretty_repr

from seashell.diagnostics import SourceLocation


@dataclass(slots=True, kw_only=True)
class Node:
    location: SourceLocation | None = None


@dataclass
class Statement(Node):
    pass


@dataclass
class Expression(Node):
    pass


@dataclass
class Program:
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

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, Parameter)
            and (self.name == other.name)
            and (self.type_annotation == other.type_annotation)
        )


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
class IncludeStatement(Node):
    path: str

@dataclass
class String(Expression):
    value: str

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, String) and (self.value == other.value)


@dataclass
class Number(Expression):
    value: int

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Number) and (self.value == other.value)


@dataclass
class Boolean(Expression):
    value: bool

    def __str__(self) -> str:
        return "true" if self.value else "false"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Boolean) and (self.value == other.value)


class Null(Expression):
    pass

    def __str__(self) -> str:
        return "null"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Null)


@dataclass
class Variable(Expression):
    name: str

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Variable) and (self.name == other.name)


@dataclass
class FunctionCall(Statement, Expression):
    callee: Expression
    arguments: list[Expression]

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, FunctionCall)
            and (len(self.arguments) == len(other.arguments))
            and all(
                self.arguments[i] == other.arguments[i]
                for i in range(len(self.arguments))
            )
        )


@dataclass
class AccessMember(Expression):
    obj: Expression
    member: str

    def __str__(self) -> str:
        return f"{self.obj}.{self.member}"

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, AccessMember)
            and (self.obj == other.obj)
            and (self.member == other.member)
        )


@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: str
    right: Expression

    def __str__(self) -> str:
        return f"{self.left} {self.operator} {self.right}"


@dataclass
class UnaryExpression(Expression):
    operator: str
    expr: Expression

    def __str__(self) -> str:
        return f"{self.operator} {self.expr}"
