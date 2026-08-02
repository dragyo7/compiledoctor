"""
CompileDoctor Lexer
===================

This module implements the lexical analyzer (scanner) for CompileDoctor.

Responsibilities:
- Convert source code into tokens.
- Recognize reserved keywords.
- Recognize identifiers.
- Recognize literals.
- Recognize operators.
- Recognize delimiters.
- Ignore whitespace and comments.
- Track line numbers.
- Report educational lexical errors.

Uses:
    PLY (Python Lex-Yacc)
"""

import ply.lex as lex

from backend.constants import RESERVED_KEYWORDS
from backend.constants import TOKENS


class CompileDoctorLexer:
    """
    Wrapper around the PLY lexer.

    Responsibilities:
    - Build the lexer
    - Tokenize source code
    - Handle lexical errors
    """

    tokens = TOKENS

    def __init__(self):
        self.lexer = None
        self.source_code = ""

    # ======================================================
    # Operators
    # ======================================================

    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"\*"
    t_DIVIDE = r"/"
    t_MODULO = r"%"

    t_EQUAL = r"=="
    t_NOT_EQUAL = r"!="

    t_LESS_EQUAL = r"<="
    t_GREATER_EQUAL = r">="

    t_LESS_THAN = r"<"
    t_GREATER_THAN = r">"

    t_AND = r"&&"
    t_OR = r"\|\|"

    t_ASSIGN = r"="
    t_NOT = r"!"

    # ======================================================
    # Delimiters
    # ======================================================

    t_LPAREN = r"\("
    t_RPAREN = r"\)"

    t_LBRACE = r"\{"
    t_RBRACE = r"\}"

    t_LBRACKET = r"\["
    t_RBRACKET = r"\]"

    t_SEMICOLON = r";"
    t_COMMA = r","

    # ======================================================
    # Ignore spaces and tabs
    # ======================================================

    t_ignore = " \t"

    # ======================================================
    # Floating-point numbers
    # ======================================================

    def t_FLOAT_NUMBER(self, token):
        r"\d+\.\d+"
        token.value = float(token.value)
        return token

    # ======================================================
    # Integer numbers
    # ======================================================

    def t_INTEGER(self, token):
        r"\d+"
        token.value = int(token.value)
        return token

    # ======================================================
    # Identifiers & Reserved Keywords
    # ======================================================

    def t_IDENTIFIER(self, token):
        r"[A-Za-z_][A-Za-z0-9_]*"

        token.type = RESERVED_KEYWORDS.get(
            token.value,
            "IDENTIFIER",
        )

        return token

    # ======================================================
    # Single-line comments
    # ======================================================

    def t_COMMENT(self, token):
        r"//.*"
        pass

    # ======================================================
    # Multi-line comments
    # ======================================================

    def t_MULTILINE_COMMENT(self, token):
        r"/\*[\s\S]*?\*/"

        token.lexer.lineno += token.value.count("\n")

    # ======================================================
    # Newlines
    # ======================================================

    def t_newline(self, token):
        r"\n+"
        token.lexer.lineno += len(token.value)

    # ======================================================
    # Lexical Error Handler
    # ======================================================

    def t_error(self, token):
        column = self.find_column(token)

        print(
            "\nLexical Error"
            "\n--------------"
            f"\nLine       : {token.lineno}"
            f"\nColumn     : {column}"
            f"\nCharacter  : '{token.value[0]}'"
            "\nReason     : This character is not valid in the language."
            "\nSuggestion : Remove or replace the invalid character.\n"
        )

        token.lexer.skip(1)

    # ======================================================
    # Build Lexer
    # ======================================================

    def build(self, **kwargs):
        """
        Construct the PLY lexer.
        """
        self.lexer = lex.lex(module=self, **kwargs)

    # ======================================================
    # Find Token Column
    # ======================================================

    def find_column(self, token):
        """
        Return the column number of a token.
        """

        line_start = self.source_code.rfind(
            "\n",
            0,
            token.lexpos,
        ) + 1

        return token.lexpos - line_start + 1

    # ======================================================
    # Tokenize Source Code
    # ======================================================

    def tokenize(self, source_code):
        """
        Convert source code into a list of tokens.
        """

        if self.lexer is None:
            raise RuntimeError(
                "Lexer has not been built. Call build() first."
            )

        self.source_code = source_code

        # Reset line numbering for each new analysis.
        self.lexer.lineno = 1

        self.lexer.input(source_code)

        tokens = []

        while True:

            token = self.lexer.token()

            if token is None:
                break

            tokens.append(token)

        return tokens