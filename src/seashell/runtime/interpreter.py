from typing import Any

from mypy.nodes import Expression

from seashell.parser.ast_nodes import (
    AccessMember,
    Assignment,
    FunctionCall,
    FunctionDeclaration,
    IfStatement,
    Node,
    Number,
    Program,
    String,
    Variable,
)
from seashell.runtime.context import RuntimeContext
from seashell.runtime.errors import (
    SeashellRuntimeError,
    UndefinedVariableError,
    UnknownStatementError,
    UnknownTypeError,
)
from seashell.runtime.module import Module
from seashell.runtime.values import UserFunction
from seashell.stdlib.fs import FSModule
from seashell.stdlib.io import IOModule


class Interpreter:
    def __init__(self) -> None:
        self.context = RuntimeContext()

        self._register_builtins()

    def run(self, program: Program):
        for statement in program.statements:
            try:
                self.execute(statement)
            except SeashellRuntimeError as error:
                # TODO: Better diagnostics.
                print(f"error: {error}")
                break

    def register_module(self, module: Module) -> None:
        self.context.register_module(module)

    def execute(self, node: Node) -> Any:
        match node:
            case Assignment():
                self.execute_assignment(node)
                return None
            case FunctionCall():
                return self.execute_function_call(node)
            case IfStatement():
                self.execute_if_statement(node)
                return None
            case FunctionDeclaration():
                self.execute_function_declaration(node)
                return None
            case _:
                raise UnknownStatementError(f"unknown statement: {node}")

    def execute_assignment(self, node: Assignment) -> None:
        value = self.evaluate(node.value)
        self.context.variables[node.name] = value

    def execute_function_call(self, node: FunctionCall) -> Any:
        self.evaluate_function_call(node)

    def execute_if_statement(self, node: IfStatement) -> None:
        condition = self.evaluate(node.condition)
        if condition:
            for statement in node.body:
                self.execute(statement)

    def execute_function_declaration(self, node: FunctionDeclaration) -> None:
        function = UserFunction(
            declaration=node,
        )
        self.context.variables[node.name] = function

    def execute_user_function(self, function: UserFunction, arguments: list):
        declaration = function.declaration
        local_variables = {}
        for parameter, argument in zip(declaration.parameters, arguments):
            local_variables[parameter.name] = argument
        previous_variables = self.context.variables.copy()
        self.context.variables.update(local_variables)
        try:
            for statement in declaration.body:
                self.execute(statement)
        finally:
            self.context.variables = previous_variables

    def evaluate(self, node: Expression):
        match node:
            case String():
                return node.value
            case Number():
                return node.value
            case Variable():
                return self.evaluate_variable(node)
            case AccessMember():
                return self.evaluate_access_member(node)
            case FunctionCall():
                return self.evaluate_function_call(node)
            case _:
                raise UnknownTypeError(f"unknown variable type {node}")

    def evaluate_variable(self, node: Variable) -> Any:
        if node.name in self.context.variables:
            return self.context.variables[node.name]
        if node.name in self.context.modules:
            return self.context.modules[node.name]
        raise UndefinedVariableError(f"undefined variable '{node.name}'")

    def evaluate_access_member(self, node: AccessMember) -> Any:
        object_value = self.evaluate(node.object)
        return getattr(object_value, node.member)

    def evaluate_function_call(self, node: FunctionCall) -> Any:
        function = self.evaluate(node.callee)
        arguments = [self.evaluate(argument) for argument in node.arguments]
        if isinstance(function, UserFunction):
            self.execute_user_function(
                function,
                arguments,
            )
            return None
        return function(*arguments)

    def _register_builtins(self) -> None:
        self.register_module(IOModule())
        self.register_module(FSModule())
