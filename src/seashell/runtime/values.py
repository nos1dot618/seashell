from dataclasses import dataclass

from seashell.parser.ast_nodes import FunctionDeclaration


@dataclass
class UserFunction:
    declaration: FunctionDeclaration
