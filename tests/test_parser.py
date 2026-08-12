"""
Unit tests for the CompileDoctor parser.

Run with:

    python -m pytest -v

These tests verify that source code is transformed from
tokens into the expected Abstract Syntax Tree (AST).
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
from backend.parser.parser import CompileDoctorParser


def create_parser():
    """Create and build a fresh parser for a test."""
    parser = CompileDoctorParser()
    parser.build()
    return parser


# ==========================================================
# Basic Program Parsing
# ==========================================================

def test_parse_empty_function():
    parser = create_parser()

    source = """
    int main() {
    }
    """

    ast = parser.parse(source)

    assert isinstance(ast, Program)
    assert len(ast.functions) == 1

    function = ast.functions[0]

    assert isinstance(function, Function)
    assert function.name == "main"
    assert function.return_type == "int"

    assert isinstance(function.body, Block)
    assert function.body.statements == []


def test_parse_simple_function():
    parser = create_parser()

    source = """
    int main() {
        return 0;
    }
    """

    ast = parser.parse(source)

    function = ast.functions[0]

    assert function.name == "main"
    assert function.return_type == "int"
    assert len(function.body.statements) == 1

    statement = function.body.statements[0]

    assert isinstance(statement, ReturnStatement)
    assert isinstance(statement.expression, Literal)

    assert statement.expression.value == 0
    assert statement.expression.value_type == "int"


# ==========================================================
# Variable Declarations
# ==========================================================

def test_parse_variable_declaration():
    parser = create_parser()

    source = """
    int main() {
        int x;
    }
    """

    ast = parser.parse(source)

    statement = ast.functions[0].body.statements[0]

    assert isinstance(statement, VariableDeclaration)
    assert statement.variable_type == "int"
    assert statement.name == "x"
    assert statement.initializer is None


def test_parse_initialized_integer_declaration():
    parser = create_parser()

    source = """
    int main() {
        int x = 10;
    }
    """

    ast = parser.parse(source)

    statement = ast.functions[0].body.statements[0]

    assert isinstance(statement, VariableDeclaration)
    assert statement.variable_type == "int"
    assert statement.name == "x"

    assert isinstance(statement.initializer, Literal)
    assert statement.initializer.value == 10
    assert statement.initializer.value_type == "int"


def test_parse_initialized_float_declaration():
    parser = create_parser()

    source = """
    int main() {
        float value = 2.5;
    }
    """

    ast = parser.parse(source)

    statement = ast.functions[0].body.statements[0]

    assert isinstance(statement, VariableDeclaration)
    assert statement.variable_type == "float"
    assert statement.name == "value"

    assert isinstance(statement.initializer, Literal)
    assert statement.initializer.value == 2.5
    assert statement.initializer.value_type == "float"


# ==========================================================
# Assignment
# ==========================================================

def test_parse_assignment():
    parser = create_parser()

    source = """
    int main() {
        int x = 10;
        x = 20;
    }
    """

    ast = parser.parse(source)

    statement = ast.functions[0].body.statements[1]

    assert isinstance(statement, Assignment)
    assert statement.name == "x"

    assert isinstance(statement.expression, Literal)
    assert statement.expression.value == 20


# ==========================================================
# Identifier Expressions
# ==========================================================

def test_parse_identifier_expression():
    parser = create_parser()

    source = """
    int main() {
        int x = 10;
        return x;
    }
    """

    ast = parser.parse(source)

    statement = ast.functions[0].body.statements[1]

    assert isinstance(statement, ReturnStatement)
    assert isinstance(statement.expression, Identifier)

    assert statement.expression.name == "x"


# ==========================================================
# Arithmetic Expressions
# ==========================================================

def test_parse_addition():
    parser = create_parser()

    source = """
    int main() {
        int x = 10 + 20;
    }
    """

    ast = parser.parse(source)

    declaration = ast.functions[0].body.statements[0]

    expression = declaration.initializer

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "+"

    assert isinstance(expression.left, Literal)
    assert expression.left.value == 10

    assert isinstance(expression.right, Literal)
    assert expression.right.value == 20


def test_parse_subtraction():
    parser = create_parser()

    source = """
    int main() {
        int x = 20 - 10;
    }
    """

    ast = parser.parse(source)

    expression = ast.functions[0].body.statements[0].initializer

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "-"


def test_parse_multiplication():
    parser = create_parser()

    source = """
    int main() {
        int x = 10 * 2;
    }
    """

    ast = parser.parse(source)

    expression = ast.functions[0].body.statements[0].initializer

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "*"


def test_parse_division():
    parser = create_parser()

    source = """
    int main() {
        int x = 10 / 2;
    }
    """

    ast = parser.parse(source)

    expression = ast.functions[0].body.statements[0].initializer

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "/"


def test_parse_modulo():
    parser = create_parser()

    source = """
    int main() {
        int x = 10 % 3;
    }
    """

    ast = parser.parse(source)

    expression = ast.functions[0].body.statements[0].initializer

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "%"


# ==========================================================
# Operator Precedence
# ==========================================================

def test_multiplication_has_higher_precedence_than_addition():
    parser = create_parser()

    source = """
    int main() {
        int x = 10 + 2 * 3;
    }
    """

    ast = parser.parse(source)

    expression = ast.functions[0].body.statements[0].initializer

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "+"

    assert isinstance(expression.left, Literal)
    assert expression.left.value == 10

    assert isinstance(expression.right, BinaryExpression)
    assert expression.right.operator == "*"

    assert expression.right.left.value == 2
    assert expression.right.right.value == 3


def test_parentheses_override_precedence():
    parser = create_parser()

    source = """
    int main() {
        int x = (10 + 2) * 3;
    }
    """

    ast = parser.parse(source)

    expression = ast.functions[0].body.statements[0].initializer

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "*"

    assert isinstance(expression.left, BinaryExpression)
    assert expression.left.operator == "+"

    assert expression.left.left.value == 10
    assert expression.left.right.value == 2

    assert isinstance(expression.right, Literal)
    assert expression.right.value == 3


# ==========================================================
# Unary Expressions
# ==========================================================

def test_parse_unary_minus():
    parser = create_parser()

    source = """
    int main() {
        int x = -10;
    }
    """

    ast = parser.parse(source)

    expression = ast.functions[0].body.statements[0].initializer

    assert isinstance(expression, UnaryExpression)
    assert expression.operator == "-"
    assert isinstance(expression.operand, Literal)
    assert expression.operand.value == 10


def test_parse_unary_plus():
    parser = create_parser()

    source = """
    int main() {
        int x = +10;
    }
    """

    ast = parser.parse(source)

    expression = ast.functions[0].body.statements[0].initializer

    assert isinstance(expression, UnaryExpression)
    assert expression.operator == "+"


def test_parse_logical_not():
    parser = create_parser()

    source = """
    int main() {
        bool value = !true;
    }
    """

    ast = parser.parse(source)

    expression = ast.functions[0].body.statements[0].initializer

    assert isinstance(expression, UnaryExpression)
    assert expression.operator == "!"

    assert isinstance(expression.operand, Literal)
    assert expression.operand.value is True


# ==========================================================
# Boolean Literals
# ==========================================================

def test_parse_true_literal():
    parser = create_parser()

    source = """
    int main() {
        bool value = true;
    }
    """

    ast = parser.parse(source)

    expression = ast.functions[0].body.statements[0].initializer

    assert isinstance(expression, Literal)
    assert expression.value is True
    assert expression.value_type == "bool"


def test_parse_false_literal():
    parser = create_parser()

    source = """
    int main() {
        bool value = false;
    }
    """

    ast = parser.parse(source)

    expression = ast.functions[0].body.statements[0].initializer

    assert isinstance(expression, Literal)
    assert expression.value is False
    assert expression.value_type == "bool"


# ==========================================================
# Comparison Expressions
# ==========================================================

def test_parse_comparison_expression():
    parser = create_parser()

    source = """
    int main() {
        bool result = x < 10;
    }
    """

    ast = parser.parse(source)

    expression = ast.functions[0].body.statements[0].initializer

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "<"

    assert isinstance(expression.left, Identifier)
    assert expression.left.name == "x"

    assert isinstance(expression.right, Literal)
    assert expression.right.value == 10


def test_parse_equality_expression():
    parser = create_parser()

    source = """
    int main() {
        bool result = x == 10;
    }
    """

    ast = parser.parse(source)

    expression = ast.functions[0].body.statements[0].initializer

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "=="


# ==========================================================
# Logical Expressions
# ==========================================================

def test_parse_logical_and():
    parser = create_parser()

    source = """
    int main() {
        bool result = x < 10 && y > 5;
    }
    """

    ast = parser.parse(source)

    expression = ast.functions[0].body.statements[0].initializer

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "&&"


def test_parse_logical_or():
    parser = create_parser()

    source = """
    int main() {
        bool result = x < 10 || y > 5;
    }
    """

    ast = parser.parse(source)

    expression = ast.functions[0].body.statements[0].initializer

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "||"


# ==========================================================
# Return Statements
# ==========================================================

def test_parse_empty_return():
    parser = create_parser()

    source = """
    int main() {
        return;
    }
    """

    ast = parser.parse(source)

    statement = ast.functions[0].body.statements[0]

    assert isinstance(statement, ReturnStatement)
    assert statement.expression is None


def test_parse_return_expression():
    parser = create_parser()

    source = """
    int main() {
        return 42;
    }
    """

    ast = parser.parse(source)

    statement = ast.functions[0].body.statements[0]

    assert isinstance(statement, ReturnStatement)
    assert isinstance(statement.expression, Literal)

    assert statement.expression.value == 42
    assert statement.expression.value_type == "int"


# ==========================================================
# Complete Program
# ==========================================================

def test_parse_complete_program():
    parser = create_parser()

    source = """
    int main() {
        int x = 10;
        float y = 2.5;
        x = x + 1;
        return x;
    }
    """

    ast = parser.parse(source)

    assert isinstance(ast, Program)
    assert len(ast.functions) == 1

    function = ast.functions[0]

    assert isinstance(function, Function)
    assert function.name == "main"
    assert function.return_type == "int"

    assert isinstance(function.body, Block)

    statements = function.body.statements

    assert len(statements) == 4

    assert isinstance(
        statements[0],
        VariableDeclaration,
    )

    assert isinstance(
        statements[1],
        VariableDeclaration,
    )

    assert isinstance(
        statements[2],
        Assignment,
    )

    assert isinstance(
        statements[3],
        ReturnStatement,
    )