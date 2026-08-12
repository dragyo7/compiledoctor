"""
Tests for the CompileDoctor error-recovery layer.
"""

from types import SimpleNamespace

from backend.recovery.recovery import (
    ErrorRecovery,
    RecoveryError,
)


def make_token(token_type, value=None):
    """
    Create a lightweight token-like object for testing.
    """

    return SimpleNamespace(
        type=token_type,
        value=value,
    )


def test_create_recovery_error():
    error = RecoveryError(
        message="Missing semicolon.",
        line=4,
        column=10,
        token_type="IDENTIFIER",
        token_value="x",
    )

    assert error.message == "Missing semicolon."
    assert error.line == 4
    assert error.column == 10
    assert error.token_type == "IDENTIFIER"
    assert error.token_value == "x"


def test_recovery_error_to_dict():
    error = RecoveryError(
        message="Unexpected token.",
        line=5,
        column=3,
        token_type="RBRACE",
        token_value="}",
    )

    result = error.to_dict()

    assert result == {
        "message": "Unexpected token.",
        "line": 5,
        "column": 3,
        "token_type": "RBRACE",
        "token_value": "}",
    }


def test_recovery_starts_without_errors():
    recovery = ErrorRecovery()

    assert not recovery.has_errors()
    assert recovery.error_count() == 0
    assert recovery.get_errors() == []


def test_record_error():
    recovery = ErrorRecovery()

    error = recovery.record_error(
        message="Missing semicolon.",
        line=3,
        column=12,
        token_type="RETURN",
        token_value="return",
    )

    assert isinstance(error, RecoveryError)
    assert recovery.has_errors()
    assert recovery.error_count() == 1


def test_multiple_errors_are_recorded():
    recovery = ErrorRecovery()

    recovery.record_error(
        "Missing semicolon.",
        line=3,
    )

    recovery.record_error(
        "Unexpected token.",
        line=5,
    )

    assert recovery.error_count() == 2


def test_get_errors_returns_recorded_errors():
    recovery = ErrorRecovery()

    recovery.record_error(
        "First error.",
        line=2,
    )

    errors = recovery.get_errors()

    assert len(errors) == 1
    assert errors[0].message == "First error."


def test_get_errors_returns_copy():
    recovery = ErrorRecovery()

    recovery.record_error(
        "Test error.",
    )

    errors = recovery.get_errors()
    errors.clear()

    assert recovery.error_count() == 1


def test_clear_errors():
    recovery = ErrorRecovery()

    recovery.record_error(
        "Test error.",
    )

    assert recovery.has_errors()

    recovery.clear()

    assert not recovery.has_errors()
    assert recovery.error_count() == 0


def test_semicolon_is_synchronization_token():
    recovery = ErrorRecovery()

    token = make_token(
        "SEMICOLON",
        ";",
    )

    assert recovery.is_synchronization_token(token)


def test_right_brace_is_synchronization_token():
    recovery = ErrorRecovery()

    token = make_token(
        "RBRACE",
        "}",
    )

    assert recovery.is_synchronization_token(token)


def test_left_brace_is_synchronization_token():
    recovery = ErrorRecovery()

    token = make_token(
        "LBRACE",
        "{",
    )

    assert recovery.is_synchronization_token(token)


def test_identifier_is_not_synchronization_token():
    recovery = ErrorRecovery()

    token = make_token(
        "IDENTIFIER",
        "x",
    )

    assert not recovery.is_synchronization_token(token)


def test_none_is_not_synchronization_token():
    recovery = ErrorRecovery()

    assert not recovery.is_synchronization_token(None)


def test_synchronize_finds_semicolon():
    recovery = ErrorRecovery()

    tokens = [
        make_token("IDENTIFIER", "x"),
        make_token("ASSIGN", "="),
        make_token("INTEGER", 10),
        make_token("SEMICOLON", ";"),
        make_token("RETURN", "return"),
    ]

    result = recovery.synchronize(tokens)

    assert result is not None
    assert result.type == "SEMICOLON"


def test_synchronize_finds_right_brace():
    recovery = ErrorRecovery()

    tokens = [
        make_token("IDENTIFIER", "x"),
        make_token("PLUS", "+"),
        make_token("INTEGER", 1),
        make_token("RBRACE", "}"),
    ]

    result = recovery.synchronize(tokens)

    assert result is not None
    assert result.type == "RBRACE"


def test_synchronize_returns_none_at_end():
    recovery = ErrorRecovery()

    tokens = [
        make_token("IDENTIFIER", "x"),
        make_token("INTEGER", 10),
    ]

    result = recovery.synchronize(tokens)

    assert result is None


def test_custom_synchronization_tokens():
    recovery = ErrorRecovery(
        synchronization_tokens={
            "SEMICOLON",
        }
    )

    assert recovery.is_synchronization_token(
        make_token("SEMICOLON")
    )

    assert not recovery.is_synchronization_token(
        make_token("RBRACE")
    )


def test_recovery_to_dict():
    recovery = ErrorRecovery()

    recovery.record_error(
        "Missing semicolon.",
        line=4,
        column=8,
    )

    result = recovery.to_dict()

    assert result["error_count"] == 1
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Missing semicolon."
    )