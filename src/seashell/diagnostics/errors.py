from dataclasses import dataclass
from typing import Any

from seashell.diagnostics import SourceLocation, StackFrame
from seashell.parser.ast_nodes import Node


@dataclass(slots=True, kw_only=True)
class SeashellRuntimeError(Exception):
    location: SourceLocation | None = None
    category: str = "error"

    def format_message(self) -> str:
        return "<blank>"

    @property
    def message(self) -> str:
        return self.format_message()

    def __str__(self) -> str:
        return self.message

    def __post_init__(self) -> None:
        super().__init__(self.message)

    def print_diagnostic(self, stack_trace: list[StackFrame]):
        if self.location is not None:
            print(f"{self.location}: ", end="")
        print(f"{self.category}: {self.message}")

        print("Stack Trace:")
        if len(stack_trace) == 0:
            print("<empty>")
        else:
            for stack_frame in reversed(stack_trace):
                print(stack_frame)


@dataclass(slots=True)
class UndefinedVariableError(SeashellRuntimeError):
    name: str

    def format_message(self) -> str:
        return f"undefined variable '{self.name}'"


@dataclass(slots=True)
class UnknownTypeError(SeashellRuntimeError):
    value: str | Any

    def format_message(self) -> str:
        type_str = (
            self.value if isinstance(self.value, str) else type(self.value).__name__
        )
        return f"unknown type '{type_str}'"


@dataclass(slots=True)
class UnknownStatementError(SeashellRuntimeError):
    node: Node

    def format_message(self) -> str:
        return f"unknown statement '{type(self.node).__name__}'"


@dataclass(slots=True)
class UnknownMemberError(SeashellRuntimeError):
    obj: Any
    member: str

    def format_message(self) -> str:
        return f"unknown member '{self.member}' of value '{type(self.obj).__name__}'"


@dataclass(slots=True)
class InvalidFunctionCallError(SeashellRuntimeError):
    value: Any

    def format_message(self) -> str:
        return f"value '{self.value}' is not callable"


@dataclass(slots=True)
class ArgumentCountError(SeashellRuntimeError):
    function_name: str
    expected_count: int | str
    actual_count: int

    def format_message(self) -> str:
        return (
            f"function '{self.function_name}' "
            f"expected {self.expected_count} arguments"
            f"but got {self.actual_count}"
        )


@dataclass(slots=True)
class TypeMismatchError(SeashellRuntimeError):
    expected_type: str
    actual_type: str

    def format_message(self) -> str:
        return f"expected type '{self.expected_type}' but got '{self.actual_type}'"


@dataclass(slots=True)
class UnsupportedOperandTypesError(SeashellRuntimeError):
    operator: str
    left_type: str
    right_type: str | None = None

    def format_message(self) -> str:
        if self.right_type is None:
            return f"unsupported operand type for '{self.operator}': {self.left_type}"
        return (
            f"unsupported operand types for '{self.operator}': "
            f"{self.left_type} and {self.right_type}"
        )


@dataclass(slots=True)
class DivisionByZeroError(SeashellRuntimeError):
    def format_message(self) -> str:
        return "division by zero"


@dataclass
class UnknownOperatorError(SeashellRuntimeError):
    operator: str

    def format_message(self) -> str:
        return f"unknown operator '{self.operator}'"


@dataclass
class InternalError(SeashellRuntimeError):
    category: str = "internal error"
    message: str

    def format_message(self) -> str:
        return self.message


@dataclass
class IncompatibleTypeError(SeashellRuntimeError):
    cause: str

    def format_message(self) -> str:
        return self.cause
