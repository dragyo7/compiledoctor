"""
Unit tests for CompileDoctor AST nodes.

Run with:

    python -m pytest -v

These tests verify that the AST node classes can be created,
store their expected data, and can be composed into a tree.
"""

from backend.ast_nodes.nodes import Assignment
from backend.ast_nodes.nodes import BinaryExpression
from backend.ast_nodes.nodes import Block
from backend.ast_nodes.nodes import Function
from backend.ast_nodes.nodes import Identifier
from backend.ast_nodes.nodes import Literal
from backend.ast_nodes.nodes import Program
from backend.ast_nodes.nodes import ReturnStatement
from backend.ast_nodes.nodes import UnaryExpression
from backend.ast_nodes.nodes import VariableDeclaration


# ==========================================================
# Program
# ==========================================================

def test_program():
    program = Program()

    assert program.functions == []


# ==========================================================
# Function
# ==========================================================

def test_function():
    function = Function(
        "int",
        "main",
        Block(),
    )

    assert function.return_type == "int"
    assert function.name == "main"
    assert isinstance(function.body, Block)


# ==========================================================
# Block
# ==========================================================

def test_block():
    statement = ReturnStatement(
        Literal(0, "int")
    )

    block = Block([
        statement
    ])

    assert len(block.statements) == 1
    assert block.statements[0] is statement


# ==========================================================
# Variable Declaration
# ==========================================================

def test_variable_declaration():
    declaration = VariableDeclaration(
        "int",
        "x",
        Literal(10, "int"),
    )

    assert declaration.variable_type == "int"
    assert declaration.name == "x"
    assert declaration.initializer.value == 10
    assert declaration.initializer.value_type == "int"


def test_variable_declaration_without_initializer():
    declaration = VariableDeclaration(
        "float",
        "value",
    )

    assert declaration.variable_type == "float"
    assert declaration.name == "value"
    assert declaration.initializer is None


# ==========================================================
# Assignment
# ==========================================================

def test_assignment():
    assignment = Assignment(
        "x",
        Literal(20, "int"),
    )

    assert assignment.name == "x"
    assert assignment.expression.value == 20


# ==========================================================
# Return Statement
# ==========================================================

def test_return_statement():
    statement = ReturnStatement(
        Literal(0, "int")
    )

    assert statement.expression.value == 0
    assert statement.expression.value_type == "int"


def test_empty_return_statement():
    statement = ReturnStatement()

    assert statement.expression is None


# ==========================================================
# Identifier
# ==========================================================

def test_identifier():
    identifier = Identifier("x")

    assert identifier.name == "x"


# ==========================================================
# Literal
# ==========================================================

def test_integer_literal():
    literal = Literal(
        42,
        "int",
    )

    assert literal.value == 42
    assert literal.value_type == "int"


def test_float_literal():
    literal = Literal(
        3.14,
        "float",
    )

    assert literal.value == 3.14
    assert literal.value_type == "float"


# ==========================================================
# Binary Expression
# ==========================================================

def test_binary_expression():
    expression = BinaryExpression(
        Literal(10, "int"),
        "+",
        Literal(20, "int"),
    )

    assert expression.operator == "+"
    assert expression.left.value == 10
    assert expression.right.value == 20


# ==========================================================
# Unary Expression
# ==========================================================

def test_unary_expression():
    expression = UnaryExpression(
        "-",
        Literal(10, "int"),
    )

    assert expression.operator == "-"
    assert expression.operand.value == 10


# ==========================================================
# Complete AST Structure
# ==========================================================

def test_complete_program_ast():
    expression = BinaryExpression(
        Literal(10, "int"),
        "+",
        Literal(20, "int"),
    )

    declaration = VariableDeclaration(
        "int",
        "x",
        expression,
    )

    return_statement = ReturnStatement(
        Identifier("x")
    )

    block = Block([
        declaration,
        return_statement,
    ])

    function = Function(
        "int",
        "main",
        block,
    )

    program = Program([
        function,
    ])

    assert len(program.functions) == 1

    assert program.functions[0].name == "main"

    assert program.functions[0].return_type == "int"

    assert len(program.functions[0].body.statements) == 2

    assert (
        program.functions[0]
        .body
        .statements[0]
        .name
        == "x"
    )


# ==========================================================
# Node Type Verification
# ==========================================================

def test_ast_node_types():
    assert isinstance(Program(), Program)

    assert isinstance(
        Function(
            "int",
            "main",
            Block(),
        ),
        Function,
    )

    assert isinstance(
        Identifier("x"),
        Identifier,
    )

    assert isinstance(
        Literal(10, "int"),
        Literal,
    )

    assert isinstance(
        BinaryExpression(
            Literal(1, "int"),
            "+",
            Literal(2, "int"),
        ),
        BinaryExpression,
    )

    assert isinstance(
        UnaryExpression(
            "-",
            Literal(1, "int"),
        ),
        UnaryExpression,
    )