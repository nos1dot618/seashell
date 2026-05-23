from seashell.parser.ast_nodes import (
    AccessMember,
    Assignment,
    Expression,
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
    ArgumentCountError,
    InvalidFunctionCallError,
    SeashellRuntimeError,
    UndefinedVariableError,
    UnknownStatementError,
    UnknownTypeError,
)
from seashell.runtime.types import assert_type_annotation
from seashell.runtime.values import (
    NULL,
    Module,
    NativeFunction,
    NumberValue,
    RuntimeValue,
    StringValue,
    UserFunction,
)
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

    def execute(self, node: Node) -> RuntimeValue:
        match node:
            case Assignment():
                return self.execute_assignment(node)
            case FunctionCall():
                return self.execute_function_call(node)
            case IfStatement():
                return self.execute_if_statement(node)
            case FunctionDeclaration():
                return self.execute_function_declaration(node)
            case _:
                raise UnknownStatementError(f"unknown statement: {node}")

    def execute_assignment(self, node: Assignment) -> RuntimeValue:
        value = self.evaluate(node.value)
        assert_type_annotation(node.type_annotation, value)
        self.context.register_symbol(node.name, value)
        return NULL

    def execute_function_call(self, node: FunctionCall) -> RuntimeValue:
        return self.evaluate_function_call(node)

    def execute_if_statement(self, node: IfStatement) -> RuntimeValue:
        condition = self.evaluate(node.condition)
        if condition.is_truthy():
            for statement in node.body:
                self.execute(statement)
        return NULL

    def execute_function_declaration(self, node: FunctionDeclaration) -> RuntimeValue:
        function = UserFunction(declaration=node)
        self.context.register_symbol(node.name, function)
        return NULL

    def execute_user_function(
        self, function: UserFunction, arguments: list[RuntimeValue]
    ):
        expected_count, actual_count = (
            len(function.declaration.parameters),
            len(arguments),
        )
        if expected_count != actual_count:
            raise ArgumentCountError(
                function.declaration.name, expected_count, actual_count
            )

        checkpoint_context = self.context.copy()
        for parameter, argument in zip(function.declaration.parameters, arguments):
            assert_type_annotation(parameter.type_annotation, argument)
            self.context.register_symbol(parameter.name, argument)

        try:
            for statement in function.declaration.body:
                self.execute(statement)
        finally:
            self.context.recover_checkpoint(checkpoint_context)

    def evaluate(self, node: Expression) -> RuntimeValue:
        match node:
            case String():
                return StringValue(node.value)
            case Number():
                return NumberValue(node.value)
            case Variable():
                return self.evaluate_variable(node)
            case AccessMember():
                return self.evaluate_access_member(node)
            case FunctionCall():
                return self.evaluate_function_call(node)
            case _:
                raise UnknownTypeError(node)

    def evaluate_variable(self, node: Variable) -> RuntimeValue:
        value = self.context.get_symbol(node.name)
        if value is not None:
            return value
        raise UndefinedVariableError(node.name)

    def evaluate_access_member(self, node: AccessMember) -> RuntimeValue:
        object_value = self.evaluate(node.object)
        return object_value.get_member(node.member)

    def evaluate_function_call(self, node: FunctionCall) -> RuntimeValue:
        function = self.evaluate(node.callee)
        arguments = [self.evaluate(argument) for argument in node.arguments]
        if isinstance(function, UserFunction):
            self.execute_user_function(function, arguments)
            return NULL
        if isinstance(function, NativeFunction):
            return function.implementation(*arguments)
        raise InvalidFunctionCallError(function)

    def _register_builtins(self) -> None:
        def register_module(module: Module) -> None:
            self.context.register_symbol(module.name, module)

        register_module(IOModule())
        register_module(FSModule())
