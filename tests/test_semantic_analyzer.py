"""
Unit tests for the CompileDoctor Semantic Analyzer.
"""

from backend.parser.parser import CompileDoctorParser
from backend.semantic.analyzer import SemanticAnalyzer


def parse_source(source):
    """Parse source code into an AST."""

    parser = CompileDoctorParser()
    parser.build()

    return parser.parse(source)


def analyze_source(source):
    """Parse and semantically analyze source code."""

    ast = parse_source(source)

    analyzer = SemanticAnalyzer()

    errors = analyzer.analyze(ast)

    return errors


# ==========================================================
# Valid Programs
# ==========================================================

def test_valid_variable_declaration():
    source = """
    int main() {
        int x = 10;
        return x;
    }
    """

    errors = analyze_source(source)

    assert errors == []


def test_valid_float_declaration():
    source = """
    int main() {
        float value = 2.5;
        return 0;
    }
    """

    errors = analyze_source(source)

    assert errors == []


def test_integer_can_initialize_float():
    source = """
    int main() {
        float value = 10;
        return 0;
    }
    """

    errors = analyze_source(source)

    assert errors == []


def test_valid_assignment():
    source = """
    int main() {
        int x = 10;
        x = 20;
        return x;
    }
    """

    errors = analyze_source(source)

    assert errors == []


def test_valid_arithmetic_expression():
    source = """
    int main() {
        int x = 10;
        int y = 20;
        int result = x + y;
        return result;
    }
    """

    errors = analyze_source(source)

    assert errors == []


# ==========================================================
# Duplicate Declaration
# ==========================================================

def test_duplicate_declaration():
    source = """
    int main() {
        int x = 10;
        int x = 20;
        return x;
    }
    """

    errors = analyze_source(source)

    assert len(errors) == 1
    assert errors[0].error_type == "duplicate_declaration"
    assert "x" in errors[0].message


# ==========================================================
# Undeclared Identifier
# ==========================================================

def test_undeclared_assignment_variable():
    source = """
    int main() {
        x = 10;
        return 0;
    }
    """

    errors = analyze_source(source)

    assert len(errors) == 1
    assert errors[0].error_type == "undeclared_identifier"
    assert "x" in errors[0].message


def test_undeclared_identifier_in_return():
    source = """
    int main() {
        return x;
    }
    """

    errors = analyze_source(source)

    assert len(errors) == 1
    assert errors[0].error_type == "undeclared_identifier"
    assert "x" in errors[0].message


def test_undeclared_identifier_in_expression():
    source = """
    int main() {
        int x = y + 10;
        return x;
    }
    """

    errors = analyze_source(source)

    assert len(errors) == 1
    assert errors[0].error_type == "undeclared_identifier"
    assert "y" in errors[0].message


# ==========================================================
# Assignment Type Checking
# ==========================================================

def test_assignment_type_mismatch():
    source = """
    int main() {
        int x = 10;
        x = 2.5;
        return x;
    }
    """

    errors = analyze_source(source)

    assert len(errors) == 1
    assert errors[0].error_type == "type_mismatch"
    assert "x" in errors[0].message


def test_float_assignment_from_integer():
    source = """
    int main() {
        float value = 2.5;
        value = 10;
        return 0;
    }
    """

    errors = analyze_source(source)

    assert errors == []


# ==========================================================
# Expression Type Checking
# ==========================================================

def test_invalid_boolean_arithmetic():
    source = """
    int main() {
        bool flag = true;
        int result = flag + 10;
        return result;
    }
    """

    errors = analyze_source(source)

    assert any(
        error.error_type == "invalid_operand_type"
        for error in errors
    )


def test_valid_numeric_comparison():
    source = """
    int main() {
        int x = 10;
        bool result = x < 20;
        return 0;
    }
    """

    errors = analyze_source(source)

    assert errors == []


def test_valid_boolean_expression():
    source = """
    int main() {
        bool a = true;
        bool b = false;
        bool result = a && b;
        return 0;
    }
    """

    errors = analyze_source(source)

    assert errors == []


def test_invalid_logical_operand():
    source = """
    int main() {
        int x = 10;
        bool result = x && true;
        return 0;
    }
    """

    errors = analyze_source(source)

    assert any(
        error.error_type == "invalid_logical_operand"
        for error in errors
    )


# ==========================================================
# Unary Expressions
# ==========================================================

def test_valid_numeric_unary_expression():
    source = """
    int main() {
        int x = -10;
        return x;
    }
    """

    errors = analyze_source(source)

    assert errors == []


def test_invalid_numeric_unary_expression():
    source = """
    int main() {
        bool flag = true;
        int x = -flag;
        return x;
    }
    """

    errors = analyze_source(source)

    assert any(
        error.error_type == "invalid_operand_type"
        for error in errors
    )


def test_valid_boolean_not():
    source = """
    int main() {
        bool flag = true;
        bool result = !flag;
        return 0;
    }
    """

    errors = analyze_source(source)

    assert errors == []


# ==========================================================
# Return Type Checking
# ==========================================================

def test_valid_return_type():
    source = """
    int main() {
        int x = 10;
        return x;
    }
    """

    errors = analyze_source(source)

    assert errors == []


def test_return_type_mismatch():
    source = """
    int main() {
        return 2.5;
    }
    """

    errors = analyze_source(source)

    assert len(errors) == 1
    assert errors[0].error_type == "return_type_mismatch"


# ==========================================================
# Multiple Semantic Errors
# ==========================================================

def test_multiple_semantic_errors():
    source = """
    int main() {
        int x = 10;
        int x = 20;
        y = 30;
        return z;
    }
    """

    errors = analyze_source(source)

    error_types = [
        error.error_type
        for error in errors
    ]

    assert "duplicate_declaration" in error_types
    assert "undeclared_identifier" in error_types
    