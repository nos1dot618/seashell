class SeashellRuntimeError(Exception):
    pass


class UndefinedVariableError(SeashellRuntimeError):
    pass


class UndefinedFunctionError(SeashellRuntimeError):
    pass


class UnknownTypeError(SeashellRuntimeError):
    pass


class UnknownStatementError(SeashellRuntimeError):
    pass
