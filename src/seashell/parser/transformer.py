import ast
from typing import Any

from lark import Token, Transformer

from seashell.parser.ast_nodes import (
    AccessMember,
    Assignment,
    BreakStatement,
    ContinueStatement,
    ForStatement,
    FunctionCall,
    FunctionDeclaration,
    IfStatement,
    Number,
    Parameter,
    Program,
    ReturnStatement,
    String,
    Variable,
)


# noinspection PyMethodMayBeStatic,PyPep8Naming
class ASTTransformer(Transformer):
    def start(self, items: list[Any]) -> Program:
        return Program(
            statements=items,
        )

    def assignment(self, items: list[Any]) -> Assignment:
        return Assignment(
            name=str(items[0]),
            value=items[2],
            type_annotation=items[1],
        )

    def if_statement(self, items: list[Any]) -> IfStatement:
        return IfStatement(
            condition=items[0],
            body=items[1],
        )

    def function_declaration(self, items) -> FunctionDeclaration:
        return FunctionDeclaration(
            name=items[0],
            parameters=(items[1] if len(items) == 3 else []),
            body=items[-1],
        )

    def parameters(self, items: Any) -> list[Parameter]:
        return list(items)

    def parameter(self, items: list[Any]) -> Parameter:
        return Parameter(
            name=items[0],
            type_annotation=items[1],
        )

    def for_statement(self, items):
        return ForStatement(
            variable_name=str(items[0]),
            iterable=items[1],
            body=items[2],
        )

    def break_statement(self, _):
        return BreakStatement()

    def continue_statement(self, _):
        return ContinueStatement()

    def return_statement(self, items):
        return ReturnStatement(
            value=(items[0] if items else None),
        )

    def STRING(self, token: Token) -> String:
        return String(
            value=ast.literal_eval(token.value),
        )

    def NUMBER(self, token: Token) -> Number:
        return Number(
            value=int(token.value),
        )

    def IDENTIFIER(self, token: Token) -> str:
        return str(token)

    def variable(self, items: list[Any]) -> Variable:
        return Variable(name=items[0])

    def function_call(self, items: list[Any]) -> FunctionCall:
        return FunctionCall(
            callee=items[0],
            arguments=(items[1] if len(items) > 1 else []),
        )

    def arguments(self, items: Any) -> list[Any]:
        return list(items)

    def access_member(self, items: list[Any]) -> AccessMember:
        return AccessMember(object=items[0], member=items[1])

    def block(self, items: Any) -> list[Any]:
        return list(items)
