import ast
from typing import Any

from lark import Token, Transformer, Tree

from seashell.diagnostics import SourceLocation
from seashell.parser.ast_nodes import (
    AccessMember,
    Assignment,
    BinaryExpression,
    Boolean,
    BreakStatement,
    ContinueStatement,
    ForStatement,
    FunctionCall,
    FunctionDeclaration,
    IfStatement,
    IncludeStatement,
    Node,
    Null,
    Number,
    Parameter,
    Program,
    ReturnStatement,
    String,
    UnaryExpression,
    Variable,
)


# noinspection PyMethodMayBeStatic,PyPep8Naming
class ASTTransformer(Transformer):
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def start(self, items: list[Any]) -> Program:
        return Program(
            statements=items,
        )

    def assignment(self, items: list[Any]) -> Assignment:
        return Assignment(
            name=str(items[0]),
            value=items[2],
            type_annotation=(None if items[1] is None else str(items[1])),
            location=self._loc(items[0]),
        )

    def if_statement(self, items: list[Any]) -> IfStatement:
        return IfStatement(
            condition=items[0],
            body=items[1],
            location=self._loc(items[0]),
        )

    def function_declaration(self, items) -> FunctionDeclaration:
        return FunctionDeclaration(
            name=str(items[0]),
            parameters=([] if items[1] is None else items[1]),
            body=items[-1],
            location=self._loc(items[0]),
        )

    def parameters(self, items: Any) -> list[Parameter]:
        return list(items)

    def parameter(self, items: list[Any]) -> Parameter:
        return Parameter(
            name=str(items[0]),
            type_annotation=(None if items[1] is None else str(items[1])),
            location=self._loc(items[0]),
        )

    def for_statement(self, items):
        return ForStatement(
            variable_name=str(items[0]),
            iterable=items[1],
            body=items[2],
            location=self._loc(items[0]),
        )

    def break_statement(self, token: Token):
        return BreakStatement(
            location=self._loc(token[0]),
        )

    def continue_statement(self, token: Token):
        return ContinueStatement(
            location=self._loc(token[0]),
        )

    def return_statement(self, items: list[Any]):
        return ReturnStatement(
            value=(items[0] if items else None),
            location=self._loc(items[0]),
        )

    def include_statement(self, items: [Node]) -> IncludeStatement:
        string_expression: String = items[0]
        return IncludeStatement(
            path=str(string_expression),
            location=string_expression.location,
        )

    def STRING(self, token: Token) -> String:
        return String(
            value=ast.literal_eval(token.value),
            location=self._loc(token),
        )

    def MULTILINE_STRING(self, token: Token) -> String:
        raw_value = str(token.value)[1:-1]  # Remove the backticks.
        return String(
            value=raw_value,
            location=self._loc(token),
        )

    def NUMBER(self, token: Token) -> Number:
        return Number(
            value=int(token.value),
            location=self._loc(token),
        )

    def BOOLEAN(self, token: Token) -> Boolean:
        return Boolean(
            value=(token.value == "true"),
            location=self._loc(token),
        )

    def NULL(self, token: Token) -> Null:
        return Null(
            location=self._loc(token),
        )

    def IDENTIFIER(self, token: Token) -> str:
        return token

    def variable(self, items: list[Any]) -> Variable:
        return Variable(
            name=str(items[0]),
            location=self._loc(items[0]),
        )

    def function_call(self, items: list[Any]) -> FunctionCall:
        return FunctionCall(
            callee=items[0],
            arguments=(items[1] if len(items) > 1 else []),
            location=self._loc(items[0]),
        )

    def arguments(self, items: Any) -> list[Any]:
        return list(items)

    def access_member(self, items: list[Any]) -> AccessMember:
        return AccessMember(
            obj=items[0],
            member=str(items[1]),
            location=self._loc(items[0]),
        )

    def block(self, items: Any) -> list[Any]:
        return list(items)

    # Binary expressions.

    def or_op(self, items: Any) -> BinaryExpression:
        return self._construct_binary_expression(items, "or")

    def and_op(self, items: Any) -> BinaryExpression:
        return self._construct_binary_expression(items, "and")

    def eq_op(self, items: Any) -> BinaryExpression:
        return self._construct_binary_expression(items, "eq")

    def ne_op(self, items: Any) -> BinaryExpression:
        return self._construct_binary_expression(items, "ne")

    def gt_op(self, items: Any) -> BinaryExpression:
        return self._construct_binary_expression(items, "gt")

    def lt_op(self, items: Any) -> BinaryExpression:
        return self._construct_binary_expression(items, "lt")

    def ge_op(self, items: Any) -> BinaryExpression:
        return self._construct_binary_expression(items, "ge")

    def le_op(self, items: Any) -> BinaryExpression:
        return self._construct_binary_expression(items, "le")

    def add_op(self, items: Any) -> BinaryExpression:
        return self._construct_binary_expression(items, "+")

    def sub_op(self, items: Any) -> BinaryExpression:
        return self._construct_binary_expression(items, "-")

    def mul_op(self, items: Any) -> BinaryExpression:
        return self._construct_binary_expression(items, "*")

    def div_op(self, items: Any) -> BinaryExpression:
        return self._construct_binary_expression(items, "/")

    def neg_op(self, items: Any) -> BinaryExpression:
        return self._construct_unary_expression(items, "-")

    def not_op(self, items: Any) -> BinaryExpression:
        return self._construct_unary_expression(items, "not")

    def _construct_binary_expression(
        self, items: Any, operator: str
    ) -> BinaryExpression:
        return BinaryExpression(
            left=items[0],
            operator=operator,
            right=items[1],
            location=self._loc(items[0]),
        )

    def _construct_unary_expression(self, items: Any, operator: str) -> UnaryExpression:
        return UnaryExpression(
            expr=items[0],
            operator=operator,
            location=self._loc(items[0]),
        )

    def _loc(self, value):
        if isinstance(value, Token) or isinstance(value, Tree):
            return SourceLocation(
                row=value.line, column=value.column, filepath=self.filepath
            )
        if isinstance(value, Node):
            return value.location
