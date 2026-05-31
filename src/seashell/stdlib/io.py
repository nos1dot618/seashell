from seashell.runtime.values import Module, StringValue, NullValue


class IOModule(Module):
    def __init__(self) -> None:
        super().__init__(name="io")

        self.register_native_function_implementations(
            [
                ("write", lambda *value: NullValue(dummy=print(*value, end=""))),
                ("writeln", lambda *value: NullValue(dummy=print(*value))),
                (
                    "input",
                    lambda prompt=StringValue(value="> "): StringValue(
                        str(input(str(prompt)))
                    ),
                ),
            ]
        )
