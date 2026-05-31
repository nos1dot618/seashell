from dataclasses import dataclass, field
from typing import Iterator

from mypy.nodes import Callable

from seashell.diagnostics.errors import (
    DivisionByZeroError,
    IncompatibleTypeError,
    UnknownMemberError,
    UnsupportedOperandTypesError,
)
from seashell.parser.ast_nodes import FunctionDeclaration


class RuntimeValue:
    def type_name(self) -> str:
        return "value"

    def get_members(self) -> dict[str, RuntimeValue]:
        return {
            "type": StringValue(self.type_name()),
        }

    def get_member(self, name: str) -> RuntimeValue:
        methods = self.get_members()
        if name not in methods:
            raise UnknownMemberError(self, name)
        return methods[name]

    def is_truthy(self) -> bool:
        raise IncompatibleTypeError(cause=f"{self.type_name()} is not truthy")

    def iterate_values(self):
        raise IncompatibleTypeError(cause=f"{self.type_name()} is not iterable")

    def or_op(self, other: "RuntimeValue") -> "RuntimeValue":
        raise UnsupportedOperandTypesError("or", self.type_name(), other.type_name())

    def and_op(self, other: "RuntimeValue") -> "RuntimeValue":
        raise UnsupportedOperandTypesError("and", self.type_name(), other.type_name())

    def eq_op(self, other: "RuntimeValue") -> "BooleanValue":
        raise UnsupportedOperandTypesError("eq", self.type_name(), other.type_name())

    def ne_op(self, other: "RuntimeValue") -> "BooleanValue":
        return BooleanValue(self.eq_op(other).value)

    def gt_op(self, other: "RuntimeValue") -> "BooleanValue":
        raise UnsupportedOperandTypesError("gt", self.type_name(), other.type_name())

    def lt_op(self, other: "RuntimeValue") -> "BooleanValue":
        return BooleanValue(other.gt_op(self).value)

    def ge_op(self, other: "RuntimeValue") -> "BooleanValue":
        return BooleanValue(not self.lt_op(other).value)

    def le_op(self, other: "RuntimeValue") -> "BooleanValue":
        return BooleanValue(not self.gt_op(other).value)

    def add_op(self, other: "RuntimeValue") -> "RuntimeValue":
        raise UnsupportedOperandTypesError("+", self.type_name(), other.type_name())

    def sub_op(self, other: "RuntimeValue") -> "RuntimeValue":
        raise UnsupportedOperandTypesError("-", self.type_name(), other.type_name())

    def mul_op(self, other: "RuntimeValue") -> "RuntimeValue":
        raise UnsupportedOperandTypesError("*", self.type_name(), other.type_name())

    def div_op(self, other: "RuntimeValue") -> "RuntimeValue":
        raise UnsupportedOperandTypesError("/", self.type_name(), other.type_name())

    def neg_op(self) -> "RuntimeValue":
        raise UnsupportedOperandTypesError("-", self.type_name())

    def not_op(self) -> "BooleanValue":
        raise UnsupportedOperandTypesError("not", self.type_name())

    def __str__(self) -> str:
        return "<value>"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


@dataclass(frozen=True)
class StringValue(RuntimeValue):
    value: str

    def type_name(self) -> str:
        return "string"

    def get_members(self) -> dict[str, RuntimeValue]:
        members = super().get_members()
        members.update(
            {
                "upper": NativeFunction(
                    "string.upper", lambda: StringValue(self.value.upper())
                ),
                "lower": NativeFunction(
                    "string.lower", lambda: StringValue(self.value.lower())
                ),
                "length": NativeFunction(
                    "string.length", lambda: NumberValue(len(self.value))
                ),
                "format": NativeFunction(
                    "string.format", lambda *args: self._format(*args)
                ),
            }
        )
        return members

    def is_truthy(self) -> bool:
        return len(self.value) > 0

    def eq_op(self, other: RuntimeValue) -> RuntimeValue:
        if not isinstance(other, StringValue):
            return BooleanValue(False)
        return BooleanValue(self.value == other.value)

    def gt_op(self, other: RuntimeValue) -> RuntimeValue:
        if not isinstance(other, StringValue):
            raise UnsupportedOperandTypesError(
                "gt", self.type_name(), other.type_name()
            )
        return BooleanValue(self.value > other.value)

    def add_op(self, other: RuntimeValue) -> RuntimeValue:
        if not isinstance(other, StringValue):
            raise UnsupportedOperandTypesError("+", self.type_name(), other.type_name())
        return StringValue(self.value + other.value)

    def mul_op(self, other: RuntimeValue) -> RuntimeValue:
        if not isinstance(other, NumberValue):
            raise UnsupportedOperandTypesError("*", self.type_name(), other.type_name())
        return StringValue(self.value * other.value)

    def neg_op(self) -> RuntimeValue:
        return NumberValue(-self.value)

    def _format(self, *args) -> RuntimeValue:
        result = self.value
        # Protect escaped braces.
        result = result.replace("{{", "\0OPEN\0")
        result = result.replace("}}", "\0CLOSE\0")
        for i, arg in enumerate(args):
            result = result.replace(f"{{{i}}}", str(arg))
        # Restore escaped braces.
        result = result.replace("\0OPEN\0", "{")
        result = result.replace("\0CLOSE\0", "}")
        return StringValue(result)

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"StringValue({self.value!r})"


@dataclass(frozen=True)
class NumberValue(RuntimeValue):
    value: int | float

    def type_name(self) -> str:
        return "number"

    def is_truthy(self) -> bool:
        return self.value > 0

    def eq_op(self, other: RuntimeValue) -> RuntimeValue:
        if not isinstance(other, NumberValue):
            return BooleanValue(False)
        return BooleanValue(self.value == other.value)

    def gt_op(self, other: RuntimeValue) -> RuntimeValue:
        if not isinstance(other, NumberValue):
            raise UnsupportedOperandTypesError(
                "gt", self.type_name(), other.type_name()
            )
        return BooleanValue(self.value > other.value)

    def add_op(self, other: RuntimeValue) -> RuntimeValue:
        if not isinstance(other, NumberValue):
            raise UnsupportedOperandTypesError("+", self.type_name(), other.type_name())
        return NumberValue(self.value + other.value)

    def sub_op(self, other: RuntimeValue) -> RuntimeValue:
        if not isinstance(other, NumberValue):
            raise UnsupportedOperandTypesError("-", self.type_name(), other.type_name())
        return NumberValue(self.value - other.value)

    def mul_op(self, other: RuntimeValue) -> RuntimeValue:
        if not isinstance(other, NumberValue):
            raise UnsupportedOperandTypesError("*", self.type_name(), other.type_name())
        return NumberValue(self.value * other.value)

    def div_op(self, other: RuntimeValue) -> RuntimeValue:
        if not isinstance(other, NumberValue):
            raise UnsupportedOperandTypesError("/", self.type_name(), other.type_name())
        if other.value == 0:
            raise DivisionByZeroError()
        return NumberValue(self.value / other.value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"NumberValue({self.value!r})"


@dataclass(frozen=True)
class BooleanValue(RuntimeValue):
    value: bool

    def type_name(self) -> str:
        return "boolean"

    def is_truthy(self) -> bool:
        return self.value

    def or_op(self, other: RuntimeValue) -> RuntimeValue:
        if not isinstance(other, BooleanValue):
            raise UnsupportedOperandTypesError(
                "or", self.type_name(), other.type_name()
            )
        return BooleanValue(self.value or other.value)

    def and_op(self, other: RuntimeValue) -> RuntimeValue:
        if not isinstance(other, BooleanValue):
            raise UnsupportedOperandTypesError(
                "and", self.type_name(), other.type_name()
            )
        return BooleanValue(self.value and other.value)

    def eq_op(self, other: RuntimeValue) -> RuntimeValue:
        if not isinstance(other, BooleanValue):
            return BooleanValue(False)
        return BooleanValue(self.value == other.value)

    def not_op(self) -> RuntimeValue:
        return BooleanValue(not self.value)

    def __str__(self):
        return "true" if self.value else "false"

    def __repr__(self):
        return f"BooleanValue({self.value!r})"


@dataclass
class Module(RuntimeValue):
    name: str
    exports: dict[str, RuntimeValue] = field(default_factory=dict)

    def type_name(self) -> str:
        return "module"

    def register(self, name: str, value: RuntimeValue) -> None:
        self.exports[name] = value

    def get_members(self) -> dict[str, RuntimeValue]:
        members = super().get_members()
        members.update(self.exports)
        return members

    def __str__(self) -> str:
        return f"<module: {self.name}>"

    def __repr__(self) -> str:
        exports = ", ".join(self.exports.keys())
        return f"Module(name={self.name!r}, exports=[{exports}])"


class FunctionValue(RuntimeValue):
    def type_name(self) -> str:
        return "function"

    def __str__(self) -> str:
        return "<function>"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


@dataclass(frozen=True)
class NativeFunction(FunctionValue):
    name: str
    implementation: Callable

    def __str__(self) -> str:
        return f"<native function: {self.name}>"

    def __repr__(self) -> str:
        return f"NativeFunction(name={self.name!r})"


@dataclass
class UserFunction(FunctionValue):
    declaration: FunctionDeclaration

    def __str__(self) -> str:
        return f"<user declared function: {self.declaration.name}>"

    def __repr__(self) -> str:
        return f"NativeFunction(name={self.declaration.name!r})"


@dataclass
class Iterable(RuntimeValue):
    iterator_factory: Callable[[], Iterator[RuntimeValue]]

    def iterate_values(self):
        return self.iterator_factory()


@dataclass(frozen=True)
class NullValue(RuntimeValue):
    def type_name(self) -> str:
        return "null"

    def is_truthy(self) -> bool:
        return False

    def eq_op(self, other: RuntimeValue) -> RuntimeValue:
        return BooleanValue(isinstance(other, NullValue))

    def __str__(self) -> str:
        return "null"

    def __repr__(self) -> str:
        return "NullValue()"


NULL = NullValue()

BINARY_OPERATOR_METHODS = {
    "or": "or_op",
    "and": "and_op",
    "eq": "eq_op",
    "ne": "ne_op",
    "gt": "gt_op",
    "lt": "lt_op",
    "ge": "ge_op",
    "le": "le_op",
    "+": "add_op",
    "-": "sub_op",
    "*": "mul_op",
    "/": "div_op",
}

UNARY_OPERATOR_METHODS = {
    "-": "neg_op",
    "not": "not_op",
}
