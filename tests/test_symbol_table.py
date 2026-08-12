"""
Unit tests for the CompileDoctor Symbol Table.
"""

from backend.semantic.symbol_table import Symbol
from backend.semantic.symbol_table import SymbolTable


# ==========================================================
# Symbol
# ==========================================================

def test_create_symbol():
    symbol = Symbol(
        "x",
        "int",
    )

    assert symbol.name == "x"
    assert symbol.symbol_type == "int"


# ==========================================================
# Declaration
# ==========================================================

def test_declare_symbol():
    table = SymbolTable()

    result = table.declare(
        "x",
        "int",
    )

    assert result is True
    assert table.exists("x")


def test_declare_multiple_symbols():
    table = SymbolTable()

    table.declare("x", "int")
    table.declare("y", "float")
    table.declare("flag", "bool")

    assert table.exists("x")
    assert table.exists("y")
    assert table.exists("flag")

    assert len(table) == 3


# ==========================================================
# Duplicate Declaration
# ==========================================================

def test_duplicate_declaration_is_rejected():
    table = SymbolTable()

    first = table.declare(
        "x",
        "int",
    )

    second = table.declare(
        "x",
        "float",
    )

    assert first is True
    assert second is False

    assert table.get_type("x") == "int"


# ==========================================================
# Lookup
# ==========================================================

def test_lookup_existing_symbol():
    table = SymbolTable()

    table.declare(
        "x",
        "int",
    )

    symbol = table.lookup("x")

    assert symbol is not None
    assert symbol.name == "x"
    assert symbol.symbol_type == "int"


def test_lookup_missing_symbol():
    table = SymbolTable()

    symbol = table.lookup("missing")

    assert symbol is None


# ==========================================================
# Exists
# ==========================================================

def test_exists_returns_true_for_declared_symbol():
    table = SymbolTable()

    table.declare(
        "value",
        "float",
    )

    assert table.exists("value") is True


def test_exists_returns_false_for_unknown_symbol():
    table = SymbolTable()

    assert table.exists("value") is False


# ==========================================================
# Type Lookup
# ==========================================================

def test_get_type():
    table = SymbolTable()

    table.declare(
        "count",
        "int",
    )

    table.declare(
        "price",
        "float",
    )

    assert table.get_type("count") == "int"
    assert table.get_type("price") == "float"


def test_get_type_for_unknown_symbol():
    table = SymbolTable()

    assert table.get_type("unknown") is None


# ==========================================================
# Clear
# ==========================================================

def test_clear_symbol_table():
    table = SymbolTable()

    table.declare("x", "int")
    table.declare("y", "float")

    assert len(table) == 2

    table.clear()

    assert len(table) == 0
    assert table.exists("x") is False
    assert table.exists("y") is False