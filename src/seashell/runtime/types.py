from seashell.diagnostics import SourceLocation
from seashell.diagnostics.errors import TypeMismatchError, UnknownTypeError
from seashell.runtime.values import (
    BooleanValue,
    FunctionValue,
    Iterable,
    Module,
    NullValue,
    NumberValue,
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
        value, get_runtime_type(type_annotation)
    ):
        raise TypeMismatchError(
            expected_type=type_annotation,
            actual_type=value.type_name(),
            location=location,
        )
