import os
import platform
import sys

from seashell.runtime.values import (
    BooleanValue,
    Module,
    NativeFunction,
    NullValue,
    NumberValue,
    StringValue,
)


class OSModule(Module):
    def __init__(self) -> None:
        super().__init__(name="os")

        self.register_symbols(
            [
                ("name", StringValue(value=platform.system())),
                ("platform", StringValue(value=platform.platform())),
                ("architecture", StringValue(value=platform.machine())),
                ("name", StringValue(platform.system())),
            ]
        )

        self.register_native_function_implementations(
            [
                ("cwd", lambda: StringValue(value=os.getcwd())),
                ("chdir", lambda path: NullValue(dummy=os.chdir(str(path)))),
                ("pid", lambda: NumberValue(value=os.getpid())),
                ("getenv", lambda key: StringValue(value=os.getenv(str(key), ""))),
                (
                    "setenv",
                    lambda key, value: NullValue(
                        dummy=os.environ.__setitem__(str(key), str(value))
                    ),
                ),
                (
                    "unsetenv",
                    lambda key: NullValue(dummy=os.environ.pop(str(key), None)),
                ),
                (
                    "is_windows",
                    lambda: BooleanValue(value=sys.platform.startswith("win")),
                ),
                (
                    "is_linux",
                    lambda: BooleanValue(value=sys.platform.startswith("linux")),
                ),
                ("is_macos", lambda: BooleanValue(value=(sys.platform == "darwin"))),
                (
                    "exit",
                    lambda code=NumberValue(value=0): NullValue(sys.exit(int(code))),
                ),
            ]
        )
