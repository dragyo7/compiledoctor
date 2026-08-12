"""
Tests for the CompileDoctor Diagnostics layer.

The diagnostics pipeline converts internal compiler errors into
structured, beginner-friendly explanations and readable output.
"""

import pytest

from backend.diagnostics.error_formatter import (
    Diagnostic,
    format_error,
    format_errors,
)
from backend.diagnostics.explanations import (
    get_explanation,
    has_explanation,
)
from backend.diagnostics.formatter import (
    format_diagnostic,
    format_diagnostics,
)
from backend.semantic.analyzer import SemanticError


# ==========================================================
# Helpers
# ==========================================================


def make_error(error_type, message):
    """
    Create a SemanticError for diagnostics testing.
    """

    return SemanticError(
        error_type=error_type,
        message=message,
    )


# ==========================================================
# Explanation Tests
# ==========================================================


def test_known_explanation_exists():
    explanation = get_explanation(
        "undeclared_identifier"
    )

    assert explanation is not None
    assert explanation["title"] == "Undeclared Identifier"
    assert explanation["what_happened"]
    assert explanation["why"]
    assert explanation["possible_fix"]
    assert explanation["example"]


def test_has_explanation():
    assert has_explanation(
        "undeclared_identifier"
    )

    assert not has_explanation(
        "unknown_error"
    )


def test_all_current_semantic_errors_have_explanations():
    error_types = [
        "duplicate_declaration",
        "undeclared_identifier",
        "type_mismatch",
        "return_type_mismatch",
        "invalid_operand_type",
        "invalid_logical_operand",
        "incompatible_comparison",
    ]

    for error_type in error_types:
        assert has_explanation(error_type)


# ==========================================================
# Diagnostic Model Tests
# ==========================================================


def test_diagnostic_to_dict():
    diagnostic = Diagnostic(
        error_type="test_error",
        title="Test Error",
        message="Test message.",
        what_happened="Something happened.",
        why="Because this is a test.",
        possible_fix="Fix the test.",
        example="int x = 10;",
    )

    result = diagnostic.to_dict()

    assert result == {
        "error_type": "test_error",
        "title": "Test Error",
        "message": "Test message.",
        "what_happened": "Something happened.",
        "why": "Because this is a test.",
        "possible_fix": "Fix the test.",
        "example": "int x = 10;",
    }


# ==========================================================
# Error Formatter Tests
# ==========================================================


def test_format_undeclared_identifier():
    error = make_error(
        "undeclared_identifier",
        "Variable 'x' has not been declared.",
    )

    diagnostic = format_error(error)

    assert isinstance(diagnostic, Diagnostic)

    assert (
        diagnostic.error_type
        == "undeclared_identifier"
    )

    assert (
        diagnostic.title
        == "Undeclared Identifier"
    )

    assert (
        diagnostic.message
        == "Variable 'x' has not been declared."
    )

    assert diagnostic.what_happened
    assert diagnostic.why
    assert diagnostic.possible_fix
    assert diagnostic.example


def test_format_duplicate_declaration():
    error = make_error(
        "duplicate_declaration",
        "Variable 'x' has already been declared.",
    )

    diagnostic = format_error(error)

    assert (
        diagnostic.error_type
        == "duplicate_declaration"
    )

    assert (
        diagnostic.title
        == "Duplicate Variable Declaration"
    )


def test_format_type_mismatch():
    error = make_error(
        "type_mismatch",
        "Cannot assign value of type 'bool' "
        "to variable 'x' of type 'int'.",
    )

    diagnostic = format_error(error)

    assert diagnostic.error_type == "type_mismatch"
    assert diagnostic.title == "Type Mismatch"
    assert diagnostic.possible_fix


def test_format_return_type_mismatch():
    error = make_error(
        "return_type_mismatch",
        "Function expects return type 'int' "
        "but received 'float'.",
    )

    diagnostic = format_error(error)

    assert (
        diagnostic.error_type
        == "return_type_mismatch"
    )

    assert (
        diagnostic.title
        == "Return Type Mismatch"
    )


def test_format_invalid_operand_type():
    error = make_error(
        "invalid_operand_type",
        "Operator '+' cannot be applied to type 'bool'.",
    )

    diagnostic = format_error(error)

    assert (
        diagnostic.error_type
        == "invalid_operand_type"
    )

    assert (
        diagnostic.title
        == "Invalid Operand Type"
    )


def test_format_invalid_logical_operand():
    error = make_error(
        "invalid_logical_operand",
        "Logical operator requires boolean operands.",
    )

    diagnostic = format_error(error)

    assert (
        diagnostic.error_type
        == "invalid_logical_operand"
    )

    assert (
        diagnostic.title
        == "Invalid Logical Operand"
    )


def test_format_incompatible_comparison():
    error = make_error(
        "incompatible_comparison",
        "Cannot compare incompatible values.",
    )

    diagnostic = format_error(error)

    assert (
        diagnostic.error_type
        == "incompatible_comparison"
    )

    assert (
        diagnostic.title
        == "Incompatible Comparison"
    )


def test_unknown_error_uses_fallback():
    error = make_error(
        "future_error",
        "Something unexpected happened.",
    )

    diagnostic = format_error(error)

    assert diagnostic.error_type == "future_error"
    assert diagnostic.title == "Compiler Error"

    assert (
        diagnostic.message
        == "Something unexpected happened."
    )

    assert diagnostic.what_happened
    assert diagnostic.why
    assert diagnostic.possible_fix
    assert diagnostic.example is None


def test_format_multiple_errors():
    errors = [
        make_error(
            "undeclared_identifier",
            "Variable 'x' has not been declared.",
        ),
        make_error(
            "duplicate_declaration",
            "Variable 'y' has already been declared.",
        ),
    ]

    diagnostics = format_errors(errors)

    assert len(diagnostics) == 2

    assert (
        diagnostics[0].error_type
        == "undeclared_identifier"
    )

    assert (
        diagnostics[1].error_type
        == "duplicate_declaration"
    )


def test_format_empty_error_list():
    diagnostics = format_errors([])

    assert diagnostics == []


# ==========================================================
# Text Formatter Tests
# ==========================================================


def test_format_diagnostic_as_text():
    error = make_error(
        "undeclared_identifier",
        "Variable 'x' has not been declared.",
    )

    diagnostic = format_error(error)

    result = format_diagnostic(diagnostic)

    assert "Error: Undeclared Identifier" in result
    assert "What happened:" in result
    assert "Why:" in result
    assert "Possible fix:" in result
    assert "Example:" in result


def test_formatted_text_contains_example():
    error = make_error(
        "undeclared_identifier",
        "Variable 'x' has not been declared.",
    )

    diagnostic = format_error(error)

    result = format_diagnostic(diagnostic)

    assert "int x = 10;" in result


def test_format_diagnostic_without_example():
    error = make_error(
        "future_error",
        "Unknown problem.",
    )

    diagnostic = format_error(error)

    result = format_diagnostic(diagnostic)

    assert "Error: Compiler Error" in result
    assert "Example:" not in result


def test_format_multiple_diagnostics_as_text():
    errors = [
        make_error(
            "undeclared_identifier",
            "Variable 'x' has not been declared.",
        ),
        make_error(
            "duplicate_declaration",
            "Variable 'y' has already been declared.",
        ),
    ]

    diagnostics = format_errors(errors)

    result = format_diagnostics(diagnostics)

    assert "Undeclared Identifier" in result
    assert "Duplicate Variable Declaration" in result


def test_format_empty_diagnostics():
    result = format_diagnostics([])

    assert result == "No errors detected."


def test_formatter_rejects_invalid_object():
    with pytest.raises(TypeError):
        format_diagnostic(
            "this is not a Diagnostic"
        )


# ==========================================================
# Semantic Analysis → Diagnostics Integration
# ==========================================================


def test_semantic_error_can_become_diagnostic():
    error = SemanticError(
        error_type="undeclared_identifier",
        message="Variable 'score' has not been declared.",
    )

    diagnostic = format_error(error)

    assert (
        diagnostic.error_type
        == "undeclared_identifier"
    )

    assert "score" in diagnostic.message
    assert diagnostic.title == "Undeclared Identifier"


def test_semantic_errors_can_be_formatted_for_display():
    errors = [
        SemanticError(
            error_type="undeclared_identifier",
            message="Variable 'x' has not been declared.",
        ),
        SemanticError(
            error_type="type_mismatch",
            message="Invalid assignment.",
        ),
    ]

    diagnostics = format_errors(errors)
    output = format_diagnostics(diagnostics)

    assert "Undeclared Identifier" in output
    assert "Type Mismatch" in output