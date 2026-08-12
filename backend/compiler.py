"""
CompileDoctor Compiler Pipeline.

Coordinates the compiler front-end phases:

    Source Code
        ↓
      Parser
        ↓
       AST
        ↓
    Semantic Analysis
        ↓
     Diagnostics

Syntax/recovery errors are maintained separately by
the parser's ErrorRecovery manager.

This module is responsible for orchestration only.
"""

from dataclasses import dataclass
from typing import Any, List, Optional

from backend.diagnostics.error_formatter import format_errors
from backend.parser.parser import CompileDoctorParser
from backend.semantic.analyzer import SemanticAnalyzer


@dataclass
class CompilationResult:
    """
    Result of a CompileDoctor compilation.

    Attributes:
        source_code:
            Original source code.

        ast:
            Abstract Syntax Tree produced by the parser.

        semantic_errors:
            Errors produced during semantic analysis.

        recovery_errors:
            Syntax errors recorded by the recovery layer.

        success:
            True when no compilation errors occurred.
    """

    source_code: str
    ast: Optional[Any]
    semantic_errors: List[Any]
    recovery_errors: List[Any]
    success: bool

    def to_dict(self):
        """Return a JSON-safe dictionary representation."""

        return {
            "source_code": self.source_code,
            "success": self.success,
            "ast": self._convert_value(self.ast),
            "semantic_errors": [
                self._convert_value(error)
                for error in self.semantic_errors
            ],
            "recovery_errors": [
                self._convert_value(error)
                for error in self.recovery_errors
            ],
        }

    @staticmethod
    def _convert_value(value):
        """
        Convert compiler objects recursively into
        JSON-safe Python values.
        """

        if value is None:
            return None

        if hasattr(value, "to_dict"):
            return value.to_dict()

        if isinstance(value, list):
            return [
                CompilationResult._convert_value(item)
                for item in value
            ]

        if isinstance(value, tuple):
            return [
                CompilationResult._convert_value(item)
                for item in value
            ]

        if isinstance(value, dict):
            return {
                key: CompilationResult._convert_value(item)
                for key, item in value.items()
            }

        # AST nodes currently expose their data through
        # instance attributes rather than to_dict().
        #
        # Convert those attributes recursively so the AST
        # can safely cross the API boundary.
        if hasattr(value, "__dict__"):
            return {
                key: CompilationResult._convert_value(item)
                for key, item in value.__dict__.items()
            }

        return value


class CompileDoctorCompiler:
    """
    Main compiler front-end coordinator.

    Connects the already implemented compiler components
    without duplicating their responsibilities.
    """

    def __init__(self):
        """Initialize the parser and its recovery manager."""

        self.parser = CompileDoctorParser()
        self.parser.build()

    def compile(self, source_code: str) -> CompilationResult:
        """
        Run the compiler front-end pipeline.

        Pipeline:

            1. Parse source code.
            2. Collect syntax/recovery errors.
            3. Run semantic analysis when parsing succeeds.
            4. Return a CompilationResult.
        """

        if not isinstance(source_code, str):
            raise TypeError(
                "source_code must be a string."
            )

        # Start every compilation with a clean
        # recovery state.
        self.parser.recovery.clear()

        # -----------------------------------------
        # Phase 1: Parsing
        # -----------------------------------------

        ast = self.parser.parse(source_code)

        recovery_errors = self.parser.recovery.get_errors()

        # -----------------------------------------
        # Phase 2: Semantic Analysis
        # -----------------------------------------

        semantic_errors = []

        if ast is not None and not recovery_errors:
            analyzer = SemanticAnalyzer()
            semantic_errors = analyzer.analyze(ast)

        # -----------------------------------------
        # Final Status
        # -----------------------------------------

        success = (
            ast is not None
            and not recovery_errors
            and not semantic_errors
        )

        return CompilationResult(
            source_code=source_code,
            ast=ast,
            semantic_errors=semantic_errors,
            recovery_errors=recovery_errors,
            success=success,
        )

    def analyze(self, source_code: str):
        """
        Compile source code and return a frontend/API-friendly
        structured result including educational diagnostics.

        The compiler is executed only once.
        """

        result = self.compile(source_code)

        diagnostics = format_errors(
            result.semantic_errors
        )

        response = result.to_dict()

        response["diagnostics"] = [
            diagnostic.to_dict()
            for diagnostic in diagnostics
        ]

        return response