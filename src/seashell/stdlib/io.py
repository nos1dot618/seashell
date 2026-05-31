from seashell.runtime.values import Module, NativeFunction


class IOModule(Module):
    def __init__(self) -> None:
        super().__init__(name="io")

        self.register(
            "write", NativeFunction("io.write", lambda *value: print(*value, end=""))
        )
        self.register(
            "writeln", NativeFunction("io.writeln", lambda *value: print(*value))
        )
