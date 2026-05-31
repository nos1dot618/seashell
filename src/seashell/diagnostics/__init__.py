from __future__ import annotations
from dataclasses import dataclass


@dataclass(slots=True)
class SourceLocation:
    row: int
    column: int
    filepath: str = "<stdin>"

    def __str__(self) -> str:
        return f"{self.filepath}:{self.row}:{self.column}"


@dataclass(slots=True)
class StackFrame:
    callee: str
    arguments: list[RuntimeValue]  # noqa: F821
    location: SourceLocation

    def __str__(self) -> str:
        arguments_str = ", ".join(str(argument) for argument in self.arguments)
        return f"{self.location}: {self.callee}({arguments_str})"
