import sys

from seashell.diagnostics import SourceLocation, StackFrame
from seashell.diagnostics.errors import (
    ArgumentCountError,
    InvalidFunctionCallError,
    SeashellRuntimeError,
    UndefinedVariableError,
    UnknownOperatorError,
    UnknownStatementError,
    UnknownTypeError,
    UnsupportedOperandTypesError,
)
from seashell.parser.ast_nodes import (
    AccessMember,
    Assignment,
    BinaryExpression,
    BreakStatement,
    ContinueStatement,
    Expression,
    ForStatement,
    FunctionCall,
    FunctionDeclaration,
    IfStatement,
    Node,
    Null,
    Number,
    Program,
    ReturnStatement,
    String,
    UnaryExpression,
    Variable,
)
from seashell.runtime.context import RuntimeContext
from seashell.runtime.signals import BreakSignal, ContinueSignal, ReturnSignal
from seashell.runtime.types import assert_type_annotation
from seashell.runtime.values import (
    BINARY_OPERATOR_METHODS,
    NULL,
    UNARY_OPERATOR_METHODS,
    FunctionValue,
    Module,
    NativeFunction,
    NumberValue,
    RuntimeValue,
    StringValue,
    UserFunction,
)
from seashell.stdlib.collections import CollectionsModule
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
                error.print_diagnostic(self.context.stack_trace)
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
            case ForStatement():
                return self.execute_for_statement(node)
            case ContinueStatement():
                return self.execute_continue_statement(node)
            case BreakStatement():
                return self.execute_break_statement(node)
            case ReturnStatement():
                return self.execute_return_statement(node)
            case _:
                raise UnknownStatementError(
                    node=node,
                    location=node.location,
                )

    def execute_assignment(self, node: Assignment) -> RuntimeValue:
        value = self.evaluate(node.value)
        assert_type_annotation(
            type_annotation=node.type_annotation,
            value=value,
            location=node.location,
        )
        self.context.assign_symbol(node.name, value)
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
        self.context.assign_symbol(node.name, function)
        return NULL

    def execute_for_statement(self, node: ForStatement) -> RuntimeValue:
        iterable = self.evaluate(node.iterable)
        for value in iterable.iterate_values():
            self.context.register_symbol(node.variable_name, value)
            try:
                for statement in node.body:
                    self.execute(statement)
            except ContinueSignal:
                continue
            except BreakSignal:
                break
        return NULL

    def execute_continue_statement(self, node: ContinueStatement) -> RuntimeValue:
        raise ContinueSignal()

    def execute_break_statement(self, node: BreakStatement) -> RuntimeValue:
        raise BreakSignal()

    def execute_return_statement(self, node: ReturnStatement) -> RuntimeValue:
        value = self.evaluate(node.value) if node.value else NULL
        raise ReturnSignal(value)

    def execute_user_function(
        self,
        function: UserFunction,
        arguments: list[RuntimeValue],
        caller_location: SourceLocation,
    ) -> RuntimeValue:
        expected_count, actual_count = (
            len(function.declaration.parameters),
            len(arguments),
        )
        if expected_count != actual_count:
            raise ArgumentCountError(
                function_name=function.declaration.name,
                expected_count=expected_count,
                actual_count=actual_count,
                location=caller_location,
            )

        for parameter, argument in zip(function.declaration.parameters, arguments):
            assert_type_annotation(
                type_annotation=parameter.type_annotation,
                value=argument,
                location=parameter.location,
            )
            self.context.register_symbol(parameter.name, argument)
        try:
            for statement in function.declaration.body:
                self.execute(statement)
        except ReturnSignal as signal:
            return signal.value

        return NULL

    def evaluate(self, node: Expression) -> RuntimeValue:
        match node:
            case String():
                return StringValue(node.value)
            case Number():
                return NumberValue(node.value)
            case Variable():
                return self.evaluate_variable(node)
            case Null():
                return NULL
            case AccessMember():
                return self.evaluate_access_member(node)
            case FunctionCall():
                return self.evaluate_function_call(node)
            case BinaryExpression():
                return self.evaluate_binary_expression(node)
            case UnaryExpression():
                return self.evaluate_unary_expression(node)
            case _:
                raise UnknownTypeError(
                    value=node,
                    location=node.location,
                )

    def evaluate_variable(self, node: Variable) -> RuntimeValue:
        value = self.context.get_symbol(node.name)
        if value is not None:
            return value
        raise UndefinedVariableError(
            name=node.name,
            location=node.location,
        )

    def evaluate_access_member(self, node: AccessMember) -> RuntimeValue:
        object_value = self.evaluate(node.obj)
        return object_value.get_member(node.member)

    def evaluate_function_call(self, node: FunctionCall) -> RuntimeValue:
        callee = self.evaluate(node.callee)
        arguments = [self.evaluate(argument) for argument in node.arguments]

        if not isinstance(callee, FunctionValue):
            raise InvalidFunctionCallError(
                value=callee,
                location=node.location,
            )

        self.context.push_scope()
        self.context.push_stack_frame(
            StackFrame(
                callee=str(node.callee),
                arguments=arguments,
                location=node.location,
            )
        )

        should_pop_frame = False

        try:
            if isinstance(callee, UserFunction):
                result = self.execute_user_function(
                    function=callee,
                    arguments=arguments,
                    caller_location=node.location,
                )
            if isinstance(callee, NativeFunction):
                result = callee.implementation(*arguments)
            should_pop_frame = True
            return result
        except ReturnSignal:
            should_pop_frame = True
            raise
        finally:
            if should_pop_frame:
                self.context.pop_stack_frame()
            self.context.pop_scope()

    def evaluate_binary_expression(self, node: BinaryExpression) -> RuntimeValue:
        left = self.evaluate(node.left)
        method_name = BINARY_OPERATOR_METHODS.get(node.operator)
        if method_name is None:
            raise UnknownOperatorError(
                operator=node.operator,
                location=node.location,
            )
        if not hasattr(left, method_name):
            raise UnsupportedOperandTypesError(
                operator=node.operator,
                left_type=left.type_name(),
                location=node.location,
            )
        method = getattr(left, method_name)
        right = self.evaluate(node.right)
        return method(right)

    def evaluate_unary_expression(self, node: UnaryExpression) -> RuntimeValue:
        expr = self.evaluate(node.left)
        method_name = UNARY_OPERATOR_METHODS.get(node.operator)
        if method_name is None:
            raise UnknownOperatorError(
                operator=node.operator,
                location=node.location,
            )
        if not hasattr(expr, method_name):
            raise UnsupportedOperandTypesError(
                operator=node.operator,
                left_type=expr.type_name(),
                location=node.location,
            )
        method = getattr(expr, method_name)
        return method()

    def _register_builtins(self) -> None:
        def register_module(module: Module) -> None:
            self.context.register_symbol(module.name, module)

        register_module(IOModule())
        register_module(FSModule())
        register_module(CollectionsModule())
