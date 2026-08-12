"""
CompileDoctor Diagnostic Formatter
==================================

Formats structured Diagnostic objects into readable text.

This module is responsible only for presentation-oriented
text formatting.

It does not:
- perform lexical analysis
- parse source code
- perform semantic analysis
- generate explanations
- modify compiler errors
"""

from backend.diagnostics.error_formatter import Diagnostic


def format_diagnostic(diagnostic):
    """
    Format one Diagnostic as readable text.

    Args:
        diagnostic: Diagnostic object.

    Returns:
        Human-readable string.
    """

    if not isinstance(diagnostic, Diagnostic):
        raise TypeError(
            "format_diagnostic expects a Diagnostic object."
        )

    lines = [
        f"Error: {diagnostic.title}",
        "",
        f"What happened: {diagnostic.what_happened}",
        "",
        f"Why: {diagnostic.why}",
        "",
        f"Possible fix: {diagnostic.possible_fix}",
    ]

    if diagnostic.example:
        lines.extend(
            [
                "",
                "Example:",
                diagnostic.example,
            ]
        )

    return "\n".join(lines)


def format_diagnostics(diagnostics):
    """
    Format multiple diagnostics.

    Args:
        diagnostics: Iterable of Diagnostic objects.

    Returns:
        A single readable string containing all diagnostics.
    """

    diagnostics = list(diagnostics)

    if not diagnostics:
        return "No errors detected."

    formatted = [
        format_diagnostic(diagnostic)
        for diagnostic in diagnostics
    ]

    return "\n\n".join(formatted)