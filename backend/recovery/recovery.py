"""
CompileDoctor Error Recovery
============================

Provides lightweight error-recovery support for the compiler
front-end.

The recovery layer is intentionally simple and educational.

Its purpose is to:
- represent recoverable syntax errors
- record multiple errors
- identify useful synchronization tokens
- allow the parser to continue after selected errors

This module does not:
- modify source code
- perform semantic analysis
- generate explanations
- render diagnostics
"""

from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class RecoveryError:
    """
    Represents a syntax error encountered during parsing.

    Attributes:
        message:
            Human-readable description of the syntax error.

        line:
            Source-code line where the error occurred.

        column:
            Source-code column where the error occurred.

        token_type:
            Type of token involved in the error.

        token_value:
            Actual token value, when available.
    """

    message: str
    line: Optional[int] = None
    column: Optional[int] = None
    token_type: Optional[str] = None
    token_value: Optional[Any] = None

    def to_dict(self):
        """
        Convert the recovery error to a dictionary.
        """

        return {
            "message": self.message,
            "line": self.line,
            "column": self.column,
            "token_type": self.token_type,
            "token_value": self.token_value,
        }


class ErrorRecovery:
    """
    Manages recoverable parser errors.

    The class keeps recovery logic independent from the parser
    implementation so that the parser can use it without
    becoming responsible for diagnostic storage.
    """

    DEFAULT_SYNCHRONIZATION_TOKENS = {
        "SEMICOLON",
        "RBRACE",
        "LBRACE",
    }

    def __init__(self, synchronization_tokens=None):
        """
        Initialize the recovery manager.

        Args:
            synchronization_tokens:
                Optional collection of token types that can be
                used as synchronization points.
        """

        if synchronization_tokens is None:
            synchronization_tokens = (
                self.DEFAULT_SYNCHRONIZATION_TOKENS
            )

        self.synchronization_tokens = set(
            synchronization_tokens
        )

        self.errors: List[RecoveryError] = []

    def record_error(
        self,
        message,
        line=None,
        column=None,
        token_type=None,
        token_value=None,
    ):
        """
        Record a recoverable syntax error.

        Returns:
            The created RecoveryError.
        """

        error = RecoveryError(
            message=message,
            line=line,
            column=column,
            token_type=token_type,
            token_value=token_value,
        )

        self.errors.append(error)

        return error

    def has_errors(self):
        """
        Return True when at least one recovery error exists.
        """

        return bool(self.errors)

    def error_count(self):
        """
        Return the number of recorded recovery errors.
        """

        return len(self.errors)

    def clear(self):
        """
        Remove all recorded recovery errors.
        """

        self.errors.clear()

    def get_errors(self):
        """
        Return a copy of the recorded errors.

        Returning a copy prevents callers from accidentally
        modifying the internal error collection.
        """

        return list(self.errors)

    def is_synchronization_token(self, token):
        """
        Determine whether a token can be used as a synchronization
        point during parser recovery.

        Args:
            token:
                PLY token object or an object exposing a `type`
                attribute.

        Returns:
            True if the token is a synchronization token.
        """

        if token is None:
            return False

        token_type = getattr(token, "type", None)

        return token_type in self.synchronization_tokens

    def synchronize(self, token_stream):
        """
        Consume tokens until a synchronization token is found.

        This method works with an iterator or iterable of tokens.

        Args:
            token_stream:
                Iterable containing parser tokens.

        Returns:
            The first synchronization token found, or None if
            the stream ends.
        """

        for token in token_stream:
            if self.is_synchronization_token(token):
                return token

        return None

    def to_dict(self):
        """
        Convert the complete recovery state into a dictionary.
        """

        return {
            "error_count": self.error_count(),
            "errors": [
                error.to_dict()
                for error in self.errors
            ],
        }