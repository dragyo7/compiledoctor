"""
CompileDoctor Parser
====================

This module implements the syntax analyzer for CompileDoctor.

Responsibilities:
- Receive tokens from the lexer.
- Validate grammar.
- Build the parser.
- Prepare for AST generation.

Current Stage:
    Parser Infrastructure

Future Stages:
    - Grammar Rules
    - AST Generation
    - Syntax Error Recovery
"""

import ply.yacc as yacc

from backend.constants import TOKENS
from backend.lexer.lexer import CompileDoctorLexer


class CompileDoctorParser:
    """
    Wrapper around the PLY parser.

    This class is responsible for:

    - Building the parser
    - Connecting the lexer
    - Parsing source code
    """

    tokens = TOKENS

    # ======================================================
    # Operator Precedence
    # ======================================================

    precedence = (
        ("left", "OR"),
        ("left", "AND"),

        ("left", "EQUAL", "NOT_EQUAL"),

        (
            "left",
            "LESS_THAN",
            "LESS_EQUAL",
            "GREATER_THAN",
            "GREATER_EQUAL",
        ),

        ("left", "PLUS", "MINUS"),

        ("left", "TIMES", "DIVIDE", "MODULO"),

        ("right", "NOT"),
    )

    def __init__(self):

        self.lexer = CompileDoctorLexer()
        self.lexer.build()

        self.parser = None

    # ======================================================
    # Temporary Start Rule
    # ======================================================

    def p_program(self, production):
        """
        program :
        """

        production[0] = None

    # ======================================================
    # Syntax Error Handler
    # ======================================================

    def p_error(self, token):

        if token is None:

            print(
                "\nSyntax Error"
                "\n------------"
                "\nUnexpected end of input.\n"
            )

            return

        print(
            "\nSyntax Error"
            "\n------------"
            f"\nLine : {token.lineno}"
            f"\nUnexpected token : '{token.value}'\n"
        )

    # ======================================================
    # Build Parser
    # ======================================================

    def build(self, **kwargs):
        """
        Build the parser.
        """

        self.parser = yacc.yacc(
            module=self,
            start="program",
            **kwargs,
        )

    # ======================================================
    # Parse Source Code
    # ======================================================

    def parse(self, source_code):
        """
        Parse source code.
        """

        if self.parser is None:
            raise RuntimeError(
                "Parser has not been built. "
                "Call build() first."
            )

        return self.parser.parse(
            source_code,
            lexer=self.lexer.lexer,
        )