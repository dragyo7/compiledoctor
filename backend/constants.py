"""
CompileDoctor Language Constants
--------------------------------

This module contains all language-level constants used by the compiler.

Keeping language definitions in one place improves readability,
maintainability, and consistency between the lexer and parser.
"""

# ==========================================================
# Reserved Keywords
# ==========================================================

RESERVED_KEYWORDS = {
    "int": "INT",
    "float": "FLOAT",
    "char": "CHAR",
    "bool": "BOOL",
    "void": "VOID",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
    "return": "RETURN",
    "true": "TRUE",
    "false": "FALSE",
}

# ==========================================================
# Operator Tokens
# ==========================================================

OPERATORS = (
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MODULO",

    "ASSIGN",

    "EQUAL",
    "NOT_EQUAL",

    "LESS_THAN",
    "LESS_EQUAL",

    "GREATER_THAN",
    "GREATER_EQUAL",

    "AND",
    "OR",
    "NOT",
)

# ==========================================================
# Delimiter Tokens
# ==========================================================

DELIMITERS = (
    "LPAREN",
    "RPAREN",

    "LBRACE",
    "RBRACE",

    "LBRACKET",
    "RBRACKET",

    "SEMICOLON",
    "COMMA",
)

# ==========================================================
# Literal Tokens
# ==========================================================

LITERALS = (
    "IDENTIFIER",
    "INTEGER",
    "FLOAT_NUMBER",
)

# ==========================================================
# Complete Token List
# ==========================================================

TOKENS = (
    LITERALS
    + OPERATORS
    + DELIMITERS
    + tuple(RESERVED_KEYWORDS.values())
)