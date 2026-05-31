from dataclasses import dataclass

from seashell.runtime.constants import ExitCode
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


# Used internally to force stop execution.
@dataclass(slots=True)
class HaltSignal(ControlSignal):
    exitcode: ExitCode
