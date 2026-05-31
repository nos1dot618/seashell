from seashell.runtime.values import Module, StringValue


class IOModule(Module):
    def __init__(self) -> None:
        super().__init__(name="io")

        self.register_native_function_implementations(
            [
                ("write", lambda *value: print(*value, end="")),
                ("writeln", lambda *value: print(*value)),
                (
                    "input",
                    lambda prompt=StringValue(value="> "): StringValue(
                        str(input(str(prompt)))
                    ),
                ),
            ]
        )
