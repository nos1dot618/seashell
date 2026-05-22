from typing import Any

from seashell.runtime.module import Module


class RuntimeContext:
    def __init__(self) -> None:
        self.variables: dict[str, Any] = {}
        self.modules: dict[str, Module] = {}

    def register_module(self, module: Module) -> None:
        self.modules[module.name] = module
