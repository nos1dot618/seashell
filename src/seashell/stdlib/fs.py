from pathlib import Path

from seashell.runtime.module import Module


# noinspection PyMethodMayBeStatic
class FSModule(Module):
    def __init__(self) -> None:
        super().__init__(name="fs")

        self.register("read_file", self.read_file)
        self.register("write_file", self.write_file)

    def read_file(self, path: str) -> str:
        return Path(path).read_text()

    def write_file(self, path: str, content: str):
        Path(path).write_text(content)
