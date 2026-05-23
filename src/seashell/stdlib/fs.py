from pathlib import Path

from seashell.runtime.values import Module, NativeFunction


class FSModule(Module):
    def __init__(self) -> None:
        super().__init__(name="fs")

        self.register(
            "read_file",
            NativeFunction("read_file", lambda path: Path(path).read_text()),
        )
        self.register(
            "write_file",
            NativeFunction(
                "write_file", lambda path, content: Path(path).write_text(content)
            ),
        )
