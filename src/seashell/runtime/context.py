from seashell.runtime.values import RuntimeValue


class RuntimeContext:
    def __init__(self) -> None:
        self.symbols: dict[str, RuntimeValue] = {}

    def register_symbol(self, name: str, value: RuntimeValue) -> None:
        self.symbols[name] = value

    def get_symbol(self, name: str) -> RuntimeValue | None:
        if name in self.symbols:
            return self.symbols[name]
        return None

    def copy(self) -> "RuntimeContext":
        context = RuntimeContext()
        context.symbols = self.symbols.copy()
        return context

    def recover_checkpoint(self, context: "RuntimeContext") -> None:
        self.symbols.clear()
        self.symbols.update(context.symbols)
