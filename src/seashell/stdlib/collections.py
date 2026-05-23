from seashell.runtime.errors import (
    ArgumentCountError,
)
from seashell.runtime.values import Iterable, Module, NativeFunction, NumberValue


# noinspection PyMethodMayBeStatic
class CollectionsModule(Module):
    def __init__(self) -> None:
        super().__init__(name="collections")

        self.register("range", NativeFunction("range", self.native_range))

    def native_range(self, *args):
        values = [arg.value for arg in args]
        if len(values) == 1:
            start = 0
            stop = values[0]
            step = 1
        elif len(values) == 2:
            start, stop = values
            step = 1
        elif len(values) == 3:
            start, stop, step = values
        else:
            raise ArgumentCountError("range", "1-3", len(values))
        return Iterable(lambda: (NumberValue(i) for i in range(start, stop, step)))
