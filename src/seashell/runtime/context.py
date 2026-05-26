from seashell.runtime.values import RuntimeValue
from seashell.runtime.errors import SeashellRuntimeError


class RuntimeContext:
    def __init__(self) -> None:
        self.scopes: list[dict[str, RuntimeValue]] = [{}]

    @property
    def current_scope(self) -> dict[str, RuntimeValue]:
        return self.scopes[-1]

    def push_scope(self) -> None:
        return self.scopes.append({})

    def pop_scope(self) -> None:
        if len(self.scopes) == 1:
            raise SeashellRuntimeError("cannot pop global scope")
        self.scopes.pop()

    def register_symbol(self, name: str, value: RuntimeValue) -> None:
        self.current_scope[name] = value

    def assign_symbol(self, name: str, value: RuntimeValue) -> None:
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name] = value
                return
        self.register_symbol(name, value)

    def get_symbol(self, name: str) -> RuntimeValue:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def copy(self) -> RuntimeContext:
        context = RuntimeContext()
        context.scopes = [scope.copy() for scope in self.scopes]
        return context

    def recover_checkpoint(self, context: "RuntimeContext") -> None:
        self.scopes = [scope.copy() for scope in context.scopes]
