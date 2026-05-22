from seashell.runtime.module import Module


# noinspection PyMethodMayBeStatic
class IOModule(Module):
    def __init__(self) -> None:
        super().__init__(name="io")

        self.register("write", self.write)
        self.register("writeln", self.writeln)

    def write(self, *values):
        print(*values, end="")

    def writeln(self, *values):
        print(*values)
