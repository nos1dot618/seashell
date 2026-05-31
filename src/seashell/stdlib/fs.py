import shutil
from pathlib import Path

from seashell.runtime.values import (
    BooleanValue,
    Iterable,
    Module,
    NullValue,
    StringValue,
)


class FSModule(Module):
    def __init__(self) -> None:
        super().__init__(name="fs")

        self.register_native_function_implementations(
            [
                ("exists", lambda path: BooleanValue(value=Path(str(path)).exists())),
                ("is_file", lambda path: BooleanValue(value=Path(str(path)).is_file())),
                ("is_dir", lambda path: BooleanValue(value=Path(str(path)).is_dir())),
                (
                    "read_text",
                    lambda path: StringValue(
                        value=Path(str(path)).read_text(encoding="utf-8")
                    ),
                ),
                (
                    "write_text",
                    lambda path, text: StringValue(
                        value=Path(str(path)).write_text(str(text), encoding="utf-8")
                    ),
                ),
                (
                    "append_text",
                    lambda path, text: StringValue(
                        value=Path(str(path))
                        .open("a", encoding="utf-8")
                        .write(str(text))
                    ),
                ),
                (
                    "create_dir",
                    lambda path: StringValue(
                        value=Path(str(path)).mkdir(parents=True, exist_ok=True)
                    ),
                ),
                ("remove", lambda path: NullValue(dummy=Path(str(path)).unlink())),
                ("remove_dir", lambda path: NullValue(dummy=shutil.rmtree(str(path)))),
                (
                    "copy",
                    lambda src, dst: NullValue(dummy=shutil.copy2(str(src), str(dst))),
                ),
                (
                    "move",
                    lambda src, dst: NullValue(dummy=shutil.move(str(src), str(dst))),
                ),
                (
                    "list",
                    lambda path=".": Iterable(
                        source=[
                            StringValue(entry.name)
                            for entry in Path(str(path)).iterdir()
                        ]
                    ),
                ),
                (
                    "join",
                    lambda *parts: StringValue(
                        value=str(Path(str(parts[0])).joinpath(*map(str, parts[1:])))
                    ),
                ),
                ("basename", lambda path: StringValue(value=Path(str(path)).name)),
                (
                    "dirname",
                    lambda path: StringValue(value=str(Path(str(path)).parent)),
                ),
                (
                    "absolute",
                    lambda path: StringValue(value=str(Path(str(path)).resolve())),
                ),
            ]
        )
