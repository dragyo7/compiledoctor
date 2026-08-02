"""
Unit tests for the CompileDoctor lexer.

Run:
    pytest

or

    pytest tests/test_lexer.py -v
"""

from backend.lexer.lexer import CompileDoctorLexer


def build_lexer():
    """Create and build a fresh lexer instance."""
    lexer = CompileDoctorLexer()
    lexer.build()
    return lexer


def token_types(source_code):
    """
    Return only token types for easier assertions.
    """
    lexer = build_lexer()
    return [token.type for token in lexer.tokenize(source_code)]


# ==========================================================
# Reserved Keywords
# ==========================================================

def test_reserved_keywords():
    code = "int float char bool void if else while for return true false"

    expected = [
        "INT",
        "FLOAT",
        "CHAR",
        "BOOL",
        "VOID",
        "IF",
        "ELSE",
        "WHILE",
        "FOR",
        "RETURN",
        "TRUE",
        "FALSE",
    ]

    assert token_types(code) == expected


# ==========================================================
# Identifiers
# ==========================================================

def test_identifier():
    assert token_types("student") == ["IDENTIFIER"]


def test_identifier_with_underscore():
    assert token_types("student_name") == ["IDENTIFIER"]


def test_identifier_with_numbers():
    assert token_types("value123") == ["IDENTIFIER"]


# ==========================================================
# Integer Literals
# ==========================================================

def test_integer():
    lexer = build_lexer()

    token = lexer.tokenize("42")[0]

    assert token.type == "INTEGER"
    assert token.value == 42


# ==========================================================
# Float Literals
# ==========================================================

def test_float():
    lexer = build_lexer()

    token = lexer.tokenize("3.14")[0]

    assert token.type == "FLOAT_NUMBER"
    assert token.value == 3.14


# ==========================================================
# Operators
# ==========================================================

def test_arithmetic_operators():

    code = "+ - * / %"

    expected = [
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",
        "MODULO",
    ]

    assert token_types(code) == expected


def test_assignment_operator():
    assert token_types("=") == ["ASSIGN"]


def test_comparison_operators():

    code = "== != < <= > >="

    expected = [
        "EQUAL",
        "NOT_EQUAL",
        "LESS_THAN",
        "LESS_EQUAL",
        "GREATER_THAN",
        "GREATER_EQUAL",
    ]

    assert token_types(code) == expected


def test_logical_operators():

    code = "&& || !"

    expected = [
        "AND",
        "OR",
        "NOT",
    ]

    assert token_types(code) == expected


# ==========================================================
# Delimiters
# ==========================================================

def test_delimiters():

    code = "( ) { } [ ] ; ,"

    expected = [
        "LPAREN",
        "RPAREN",
        "LBRACE",
        "RBRACE",
        "LBRACKET",
        "RBRACKET",
        "SEMICOLON",
        "COMMA",
    ]

    assert token_types(code) == expected


# ==========================================================
# Comments
# ==========================================================

def test_single_line_comment():

    code = """
    // This is a comment
    int
    """

    assert token_types(code) == ["INT"]


def test_multiline_comment():

    code = """
    /*
        Comment Block
    */
    int
    """

    assert token_types(code) == ["INT"]


# ==========================================================
# Empty Input
# ==========================================================

def test_empty_input():
    assert token_types("") == []


def test_whitespace_only():
    assert token_types("      \t\t\n\n") == []


# ==========================================================
# Simple Program
# ==========================================================

def test_simple_program():

    code = """
    int main() {
        int x = 10;
        return 0;
    }
    """

    expected = [
        "INT",
        "IDENTIFIER",
        "LPAREN",
        "RPAREN",
        "LBRACE",
        "INT",
        "IDENTIFIER",
        "ASSIGN",
        "INTEGER",
        "SEMICOLON",
        "RETURN",
        "INTEGER",
        "SEMICOLON",
        "RBRACE",
    ]

    assert token_types(code) == expected


# ==========================================================
# Invalid Character
# ==========================================================

def test_invalid_character():

    lexer = build_lexer()

    tokens = lexer.tokenize("$")

    # Lexer should skip invalid characters
    assert tokens == []