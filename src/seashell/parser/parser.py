from pathlib import Path

from lark import Lark

from seashell.parser.transformer import ASTTransformer

GRAMMAR = Path(__file__).parent.parent / "lexer" / "grammar.lark"

parser = Lark.open(
    str(GRAMMAR),
    parser="lalr",
    transformer=ASTTransformer(),
)


def parse(source: str):
    return parser.parse(source)
