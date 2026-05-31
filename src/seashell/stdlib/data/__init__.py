from seashell.runtime.values import Module
from seashell.stdlib.data.json import JSONModule


class DataModule(Module):
    def __init__(self) -> None:
        super().__init__(name="data")

        self.register("json", JSONModule())
