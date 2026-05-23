from seashell.runtime.errors import TypeMismatchError, UnknownTypeError
from seashell.runtime.values import (
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
    "module": Module,
    "function": FunctionValue,
    "iterable": Iterable,
    "null": NullValue,
}


def get_runtime_type(type_name: str) -> type[RuntimeValue]:
    try:
        return TYPE_REGISTRY[type_name]
    except KeyError:
        raise UnknownTypeError(type_name)


def assert_type_annotation(type_annotation: str | None, value: RuntimeValue) -> None:
    if type_annotation is not None and not isinstance(
        value, get_runtime_type(type_annotation)
    ):
        # TODO: Better diagnostics.
        raise TypeMismatchError(type_annotation, value.type_name())
