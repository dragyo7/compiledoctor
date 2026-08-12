"""
CompileDoctor Error Formatter
=============================

Converts internal compiler errors into structured,
educational diagnostic objects.

Responsibilities:
- Accept compiler error objects.
- Resolve their error type.
- Obtain educational explanations.
- Preserve the original compiler message.
- Produce a consistent diagnostic structure.

This module does not:
- perform lexical analysis
- perform parsing
- perform semantic analysis
- modify the AST
- render HTML
- print diagnostics

Presentation is handled by formatter.py.
"""

from dataclasses import dataclass
from typing import Optional

from backend.diagnostics.explanations import get_explanation


@dataclass
class Diagnostic:
    """
    Structured representation of a user-facing diagnostic.

    Attributes:
        error_type:
            Internal compiler error category.

        title:
            Short educational title.

        message:
            Original compiler-generated message.

        what_happened:
            Beginner-friendly explanation of the problem.

        why:
            Explanation of why the problem occurred.

        possible_fix:
            Suggested way to correct the problem.

        example:
            Example showing a possible correction.
    """

    error_type: str
    title: str
    message: str
    what_happened: str
    why: str
    possible_fix: str
    example: Optional[str] = None

    def to_dict(self):
        """
        Convert the diagnostic into a dictionary.

        Returns:
            Dictionary representation suitable for later
            frontend/API integration.
        """

        return {
            "error_type": self.error_type,
            "title": self.title,
            "message": self.message,
            "what_happened": self.what_happened,
            "why": self.why,
            "possible_fix": self.possible_fix,
            "example": self.example,
        }


def format_error(error):
    """
    Convert a compiler error into a structured Diagnostic.

    Args:
        error:
            An error object containing at least:
            - error_type
            - message

    Returns:
        Diagnostic object.
    """

    explanation = get_explanation(
        error.error_type
    )

    if explanation is None:
        return _create_unknown_diagnostic(error)

    return Diagnostic(
        error_type=error.error_type,
        title=explanation["title"],
        message=error.message,
        what_happened=explanation["what_happened"],
        why=explanation["why"],
        possible_fix=explanation["possible_fix"],
        example=explanation["example"],
    )


def format_errors(errors):
    """
    Convert multiple compiler errors into diagnostics.

    Args:
        errors:
            Iterable containing compiler error objects.

    Returns:
        List of Diagnostic objects.
    """

    return [
        format_error(error)
        for error in errors
    ]


def _create_unknown_diagnostic(error):
    """
    Create a fallback diagnostic for an error type that does
    not yet have a specialized educational explanation.

    This allows the compiler to remain usable even when a new
    error category has not yet been added to explanations.py.
    """

    return Diagnostic(
        error_type=error.error_type,
        title="Compiler Error",
        message=error.message,
        what_happened=error.message,
        why=(
            "CompileDoctor does not yet have a specialized "
            "educational explanation for this error."
        ),
        possible_fix=(
            "Review the compiler message and the surrounding "
            "source code."
        ),
        example=None,
    )