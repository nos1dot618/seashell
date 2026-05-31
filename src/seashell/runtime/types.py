from typing import Any

from seashell.diagnostics import SourceLocation
from seashell.diagnostics.errors import TypeMismatchError, UnknownTypeError
from seashell.runtime.values import (
    BooleanValue,
    FunctionValue,
    Iterable,
    Module,
    NullValue,
    NumberValue,
    ObjectValue,
    RuntimeValue,
    StringValue,
)

TYPE_REGISTRY: dict[str, type[RuntimeValue]] = {
    "string": StringValue,
    "number": NumberValue,
    "boolean": BooleanValue,
    "module": Module,
    "function": FunctionValue,
    "iterable": Iterable,
    "object": ObjectValue,
    "null": NullValue,
}


def get_runtime_type(
    type_name: str,
    location: SourceLocation = None,
) -> type[RuntimeValue]:
    try:
        return TYPE_REGISTRY[type_name]
    except KeyError:
        raise UnknownTypeError(
            value=type_name,
            location=location,
        )


def assert_type_annotation(
    type_annotation: str | None,
    value: RuntimeValue,
    location: SourceLocation = None,
) -> None:
    if type_annotation is not None and not isinstance(
        value, get_runtime_type(type_annotation, location=location)
    ):
        raise TypeMismatchError(
            expected_type=type_annotation,
            actual_type=value.type_name(),
            location=location,
        )


def conv_python_to_runtime_type(value: Any) -> RuntimeValue:
    match value:
        case None:
            return NullValue()
        case bool():
            return BooleanValue(value=value)
        case int():
            return NumberValue(value=value)
        case float():
            return NumberValue(value=value)
        case str():
            return StringValue(value=value)
        case list():
            return Iterable(source=[conv_python_to_runtime_type(v) for v in value])
        case dict():
            return ObjectValue(
                values={
                    str(k): conv_python_to_runtime_type(v) for k, v in value.items()
                }
            )
        case _:
            raise UnknownTypeError(value=value)


def conv_runtime_to_python_type(value: RuntimeValue) -> Any:
    match value:
        case NullValue():
            return None
        case BooleanValue():
            return value.value
        case NumberValue():
            return value.value
        case StringValue():
            return value.value
        case Iterable():
            return [conv_runtime_to_python_type(v) for v in value.source]
        case ObjectValue():
            return {k: conv_runtime_to_python_type(v) for k, v in value.values.items()}
        case _:
            raise UnknownTypeError(value=value)
