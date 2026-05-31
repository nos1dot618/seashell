from pathlib import Path

from lark import Lark

from seashell.parser.transformer import ASTTransformer

GRAMMAR = Path(__file__).parent.parent / "lexer" / "grammar.lark"


def parse(source: str, filepath: str | None = None):
    parser = Lark.open(
        str(GRAMMAR),
        parser="lalr",
        transformer=ASTTransformer(filepath),
        propagate_positions=True,
    )

    return parser.parse(source)
