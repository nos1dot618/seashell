from typing import Any


class SeashellRuntimeError(Exception):
    pass


class UndefinedVariableError(SeashellRuntimeError):
    def __init__(self, name: Any) -> None:
        self.name = name
        super().__init__(f"undefined variable '{name}'")

    def __repr__(self) -> str:
        return f"UndefinedVariableError(name={self.name!r})"


class UnknownTypeError(SeashellRuntimeError):
    def __init__(self, value: str | Any) -> None:
        self.value = value
        type_str = value if isinstance(value, str) else type(value).__name__
        super().__init__(f"unknown type '{type_str}'")

    def __repr__(self) -> str:
        return f"UnknownTypeError(type={self.value!r})"


class UnknownStatementError(SeashellRuntimeError):
    def __init__(self, node: Any) -> None:
        self.node = node
        super().__init__(f"unknown statement '{type(node).__name__}'")

    def __repr__(self) -> str:
        return f"UnknownStatementError(statement={self.node!r})"


class UnknownMemberError(SeashellRuntimeError):
    def __init__(self, obj: Any, member: str) -> None:
        self.obj = obj
        self.member = member
        super().__init__(f"unknown member '{member}' of value '{type(obj).__name__}'")

    def __repr__(self) -> str:
        return f"UnknownMemberError(obj={self.obj!r}, member={self.member!r})"


class InvalidFunctionCallError(SeashellRuntimeError):
    def __init__(self, value: Any) -> None:
        self.value = value
        super().__init__(f"value '{value}' is not callable")

    def __repr__(self) -> str:
        return f"InvalidFunctionCallError(value={self.value!r})"


class ArgumentCountError(SeashellRuntimeError):
    def __init__(
        self, function_name: str, expected_count: int | str, actual_count: int
    ) -> None:
        self.function_name = function_name
        self.expected_count = expected_count
        self.actual_count = actual_count
        super().__init__(
            f"function '{function_name}' expected {expected_count} arguments but got {actual_count}"
        )

    def __repr__(self) -> str:
        return (
            f"ArgumentCountError(function_name={self.function_name!r}, expected_count={self.expected_count!r}), "
            f"actual_count={self.actual_count!r}"
        )


class TypeMismatchError(SeashellRuntimeError):
    def __init__(self, expected_type: str, actual_type: str) -> None:
        self.expected_type = expected_type
        self.actual_type = actual_type
        super().__init__(
            f"expected type '{expected_type}' but got type '{actual_type}'"
        )

    def __repr__(self) -> str:
        return f"TypeMismatchError(expected_type={self.expected_type!r}, actual_type={self.actual_type!r})"
