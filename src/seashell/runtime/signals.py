from dataclasses import dataclass

from seashell.runtime.values import RuntimeValue


class ControlSignal(Exception):
    pass


class BreakSignal(ControlSignal):
    pass


class ContinueSignal(ControlSignal):
    pass


@dataclass
class ReturnSignal(ControlSignal):
    value: RuntimeValue
