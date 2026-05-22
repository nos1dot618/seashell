from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass
class Module:
    name: str
    functions: dict[str, Callable] = field(default_factory=dict)

    def register(self, name: str, function: Callable) -> None:
        self.functions[name] = function

    def get(self, name: str) -> Callable:
        return self.functions[name]
