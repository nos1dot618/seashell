from dataclasses import dataclass, field

from mypy.nodes import Callable

from seashell.parser.ast_nodes import FunctionDeclaration
from seashell.runtime.errors import UnknownMemberError


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
        return False

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
                    "upper", lambda: StringValue(self.value.upper())
                ),
                "lower": NativeFunction(
                    "lower", lambda: StringValue(self.value.lower())
                ),
            }
        )
        return members

    def is_truthy(self) -> bool:
        return len(self.value) > 0

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

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"NumberValue({self.value!r})"


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

    def is_truthy(self) -> bool:
        # TODO: raise error.
        return False

    def __str__(self) -> str:
        return f"<module: {self.name}>"

    def __repr__(self) -> str:
        exports = ", ".join(self.exports.keys())
        return f"Module(name={self.name!r}, exports=[{exports}])"


class FunctionValue(RuntimeValue):
    def type_name(self) -> str:
        return "function"

    def is_truthy(self) -> bool:
        # TODO: raise error.
        return False

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


@dataclass(frozen=True)
class NullValue(RuntimeValue):
    def type_name(self) -> str:
        return "null"

    def is_truthy(self) -> bool:
        return False

    def __str__(self) -> str:
        return "null"

    def __repr__(self) -> str:
        return "NullValue()"


NULL = NullValue()
