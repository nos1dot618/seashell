from seashell.diagnostics import StackFrame
from seashell.diagnostics.errors import InternalError
from seashell.runtime.values import RuntimeValue


class RuntimeContext:
    def __init__(self) -> None:
        self.scopes: list[dict[str, RuntimeValue]] = [{}]
        self.stack_trace: list[StackFrame] = []
        self.cwd = None

    @property
    def current_scope(self) -> dict[str, RuntimeValue]:
        return self.scopes[-1]

    @property
    def global_scope(self) -> dict[str, RuntimeValue]:
        return self.scopes[0]

    def push_scope(self) -> None:
        return self.scopes.append({})

    def pop_scope(self) -> None:
        if len(self.scopes) == 1:
            raise InternalError(message="cannot pop global scope")
        self.scopes.pop()

    def push_stack_frame(self, stack_frame: StackFrame) -> None:
        return self.stack_trace.append(stack_frame)

    def pop_stack_frame(self) -> None:
        if len(self.stack_trace) == 0:
            raise InternalError(message="cannot pop stack trace")
        self.stack_trace.pop()

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

    def include(self, context: "RuntimeContext") -> None:
        # Just includes the global symbols.
        self.scopes[-1].update(context.global_scope)
