import json as pyjson

from seashell.runtime.types import (
    conv_python_to_runtime_type,
    conv_runtime_to_python_type,
)
from seashell.runtime.values import Module, StringValue


class JSONModule(Module):
    def __init__(self) -> None:
        super().__init__(name="data.json")

        self.register_native_function_implementations(
            [
                (
                    "parse",
                    lambda data: conv_python_to_runtime_type(pyjson.loads(str(data))),
                ),
                (
                    "stringify",
                    lambda value: StringValue(
                        value=pyjson.dumps(conv_runtime_to_python_type(value), indent=4)
                    ),
                ),
            ]
        )
