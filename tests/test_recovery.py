from backend.recovery.recovery import ErrorRecovery
from backend.recovery.recovery import RecoveryError


def test_create_recovery_manager():
    recovery = ErrorRecovery()

    assert recovery.errors == []
    assert recovery.error_count() == 0
    assert recovery.has_errors() is False


def test_create_recovery_error():
    error = RecoveryError(
        message="Missing semicolon.",
        line=3,
        column=12,
        token_type="RBRACE",
        token_value="}",
    )

    assert error.message == "Missing semicolon."
    assert error.line == 3
    assert error.column == 12
    assert error.token_type == "RBRACE"
    assert error.token_value == "}"


def test_recovery_error_to_dict():
    error = RecoveryError(
        message="Unexpected token.",
        line=5,
        column=7,
        token_type="PLUS",
        token_value="+",
    )

    result = error.to_dict()

    assert result == {
        "message": "Unexpected token.",
        "line": 5,
        "column": 7,
        "token_type": "PLUS",
        "token_value": "+",
    }


def test_record_error():
    recovery = ErrorRecovery()

    error = recovery.record_error(
        message="Missing semicolon.",
        line=3,
        column=10,
        token_type="RBRACE",
        token_value="}",
    )

    assert isinstance(error, RecoveryError)
    assert recovery.error_count() == 1
    assert recovery.has_errors() is True


def test_record_multiple_errors():
    recovery = ErrorRecovery()

    recovery.record_error(
        message="First error.",
        line=2,
        column=5,
        token_type="IDENTIFIER",
        token_value="x",
    )

    recovery.record_error(
        message="Second error.",
        line=4,
        column=8,
        token_type="RBRACE",
        token_value="}",
    )

    assert recovery.error_count() == 2
    assert len(recovery.get_errors()) == 2


def test_get_errors_returns_copy():
    recovery = ErrorRecovery()

    recovery.record_error(
        message="Test error.",
        line=1,
        column=1,
    )

    errors = recovery.get_errors()
    errors.clear()

    assert recovery.error_count() == 1


def test_synchronization_tokens():
    recovery = ErrorRecovery()

    assert "SEMICOLON" in recovery.synchronization_tokens
    assert "RBRACE" in recovery.synchronization_tokens
    assert "LBRACE" in recovery.synchronization_tokens


def test_custom_synchronization_tokens():
    recovery = ErrorRecovery(
        synchronization_tokens={"SEMICOLON", "RETURN"}
    )

    assert recovery.is_synchronization_token(
        type("Token", (), {"type": "SEMICOLON"})()
    )

    assert recovery.is_synchronization_token(
        type("Token", (), {"type": "RETURN"})()
    )

    assert not recovery.is_synchronization_token(
        type("Token", (), {"type": "PLUS"})()
    )


def test_is_synchronization_token():
    recovery = ErrorRecovery()

    semicolon_token = type(
        "Token",
        (),
        {"type": "SEMICOLON"},
    )()

    plus_token = type(
        "Token",
        (),
        {"type": "PLUS"},
    )()

    assert recovery.is_synchronization_token(
        semicolon_token
    )

    assert not recovery.is_synchronization_token(
        plus_token
    )


def test_none_is_not_synchronization_token():
    recovery = ErrorRecovery()

    assert recovery.is_synchronization_token(None) is False


def test_synchronize_finds_semicolon():
    recovery = ErrorRecovery()

    tokens = [
        type("Token", (), {"type": "IDENTIFIER"})(),
        type("Token", (), {"type": "PLUS"})(),
        type("Token", (), {"type": "SEMICOLON"})(),
        type("Token", (), {"type": "IDENTIFIER"})(),
    ]

    result = recovery.synchronize(tokens)

    assert result is not None
    assert result.type == "SEMICOLON"


def test_synchronize_finds_rbrace():
    recovery = ErrorRecovery()

    tokens = [
        type("Token", (), {"type": "IDENTIFIER"})(),
        type("Token", (), {"type": "PLUS"})(),
        type("Token", (), {"type": "RBRACE"})(),
    ]

    result = recovery.synchronize(tokens)

    assert result is not None
    assert result.type == "RBRACE"


def test_synchronize_returns_none_at_end():
    recovery = ErrorRecovery()

    tokens = [
        type("Token", (), {"type": "IDENTIFIER"})(),
        type("Token", (), {"type": "PLUS"})(),
    ]

    result = recovery.synchronize(tokens)

    assert result is None


def test_clear_errors():
    recovery = ErrorRecovery()

    recovery.record_error(
        message="First error.",
        line=1,
    )

    recovery.record_error(
        message="Second error.",
        line=2,
    )

    assert recovery.error_count() == 2

    recovery.clear()

    assert recovery.error_count() == 0
    assert recovery.has_errors() is False
    assert recovery.get_errors() == []


def test_recovery_to_dict():
    recovery = ErrorRecovery()

    recovery.record_error(
        message="Missing semicolon.",
        line=3,
        column=15,
        token_type="RBRACE",
        token_value="}",
    )

    recovery.record_error(
        message="Unexpected token.",
        line=5,
        column=4,
        token_type="PLUS",
        token_value="+",
    )

    result = recovery.to_dict()

    assert result["error_count"] == 2
    assert len(result["errors"]) == 2

    assert result["errors"][0]["message"] == (
        "Missing semicolon."
    )

    assert result["errors"][1]["token_type"] == "PLUS"