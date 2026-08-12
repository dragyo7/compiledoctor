"""
CompileDoctor Semantic Analyzer
================================

Performs semantic analysis on the Abstract Syntax Tree (AST).

Responsibilities:
- Build and use the symbol table.
- Detect duplicate declarations.
- Detect undeclared identifiers.
- Check basic assignment compatibility.
- Check expression types.
- Check return types.

The semantic analyzer does not:
- Parse source code.
- Generate AST nodes.
- Format user-facing diagnostics.
- Perform error recovery.

Those responsibilities belong to other compiler phases.
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

from backend.semantic.symbol_table import SymbolTable


class SemanticError:
    """
    Represents a semantic error detected during analysis.

    Attributes:
        error_type:
            Short category describing the error.

        message:
            Human-readable description of the problem.
    """

    def __init__(self, error_type, message):
        self.error_type = error_type
        self.message = message

    def __repr__(self):
        return (
            f"SemanticError("
            f"error_type='{self.error_type}', "
            f"message='{self.message}'"
            f")"
        )

    def to_dict(self):
        """
        Convert the semantic error into a serializable dictionary.

        Returns:
            Dictionary containing the error category and message.
        """

        return {
            "error_type": self.error_type,
            "message": self.message,
        }


class SemanticAnalyzer:
    """
    Performs semantic analysis over the CompileDoctor AST.
    """

    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.current_function_return_type = None

    # ==========================================================
    # Public API
    # ==========================================================

    def analyze(self, ast):
        """
        Analyze a complete AST.

        Args:
            ast: Program AST node.

        Returns:
            List of SemanticError objects.
        """

        self.symbol_table.clear()
        self.errors = []
        self.current_function_return_type = None

        if not isinstance(ast, Program):
            self._add_error(
                "invalid_program",
                "Semantic analysis requires a Program AST node.",
            )
            return self.errors

        for function in ast.functions:
            self._analyze_function(function)

        return self.errors

    # ==========================================================
    # Function Analysis
    # ==========================================================

    def _analyze_function(self, function):
        """
        Analyze a single function.
        """

        if not isinstance(function, Function):
            self._add_error(
                "invalid_function",
                "Invalid function node encountered during analysis.",
            )
            return

        self.current_function_return_type = function.return_type

        # Each function currently has its own symbol-table scope.
        self.symbol_table.clear()

        self._analyze_block(function.body)

        self.current_function_return_type = None

    # ==========================================================
    # Block Analysis
    # ==========================================================

    def _analyze_block(self, block):
        """
        Analyze every statement inside a block.
        """

        if not isinstance(block, Block):
            self._add_error(
                "invalid_block",
                "Invalid block node encountered during analysis.",
            )
            return

        for statement in block.statements:
            self._analyze_statement(statement)

    # ==========================================================
    # Statement Analysis
    # ==========================================================

    def _analyze_statement(self, statement):
        """
        Dispatch semantic analysis based on statement type.
        """

        if isinstance(statement, VariableDeclaration):
            self._analyze_variable_declaration(statement)

        elif isinstance(statement, Assignment):
            self._analyze_assignment(statement)

        elif isinstance(statement, ReturnStatement):
            self._analyze_return(statement)

        elif isinstance(statement, Block):
            self._analyze_block(statement)

        elif isinstance(statement, BinaryExpression):
            self._analyze_binary_expression(statement)

        elif isinstance(statement, UnaryExpression):
            self._analyze_unary_expression(statement)

        elif isinstance(statement, Identifier):
            self._resolve_identifier(statement)

        elif isinstance(statement, Literal):
            return

    # ==========================================================
    # Variable Declaration
    # ==========================================================

    def _analyze_variable_declaration(self, declaration):
        """
        Analyze a variable declaration.
        """

        declared = self.symbol_table.declare(
            declaration.name,
            declaration.variable_type,
        )

        if not declared:
            self._add_error(
                "duplicate_declaration",
                (
                    f"Variable '{declaration.name}' "
                    f"has already been declared."
                ),
            )

            # The declaration itself is already invalid.
            # Still analyze the initializer so independent
            # errors inside it can be detected.
            if declaration.initializer is not None:
                self._infer_expression_type(
                    declaration.initializer
                )

            return

        if declaration.initializer is not None:
            initializer_type = self._infer_expression_type(
                declaration.initializer
            )

            # If expression analysis already reported an error,
            # do not create a secondary type-mismatch diagnostic.
            if initializer_type is None:
                return

            if not self._is_type_compatible(
                declaration.variable_type,
                initializer_type,
            ):
                self._add_error(
                    "type_mismatch",
                    (
                        f"Cannot initialize variable "
                        f"'{declaration.name}' of type "
                        f"'{declaration.variable_type}' "
                        f"with value of type "
                        f"'{initializer_type}'."
                    ),
                )

    # ==========================================================
    # Assignment
    # ==========================================================

    def _analyze_assignment(self, assignment):
        """
        Analyze an assignment statement.
        """

        symbol = self.symbol_table.lookup(
            assignment.name
        )

        if symbol is None:
            self._add_error(
                "undeclared_identifier",
                (
                    f"Variable '{assignment.name}' "
                    f"has not been declared."
                ),
            )

            # Analyze the right-hand side for independent errors.
            self._infer_expression_type(
                assignment.expression
            )

            return

        expression_type = self._infer_expression_type(
            assignment.expression
        )

        # Do not create a secondary type mismatch if expression
        # analysis has already failed.
        if expression_type is None:
            return

        if not self._is_type_compatible(
            symbol.symbol_type,
            expression_type,
        ):
            self._add_error(
                "type_mismatch",
                (
                    f"Cannot assign value of type "
                    f"'{expression_type}' to variable "
                    f"'{assignment.name}' of type "
                    f"'{symbol.symbol_type}'."
                ),
            )

    # ==========================================================
    # Return Statement
    # ==========================================================

    def _analyze_return(self, statement):
        """
        Analyze a return statement against the current
        function return type.
        """

        if self.current_function_return_type is None:
            return

        if statement.expression is None:
            return

        expression_type = self._infer_expression_type(
            statement.expression
        )

        # If expression analysis already produced an error,
        # avoid a cascading return-type diagnostic.
        if expression_type is None:
            return

        if not self._is_type_compatible(
            self.current_function_return_type,
            expression_type,
        ):
            self._add_error(
                "return_type_mismatch",
                (
                    f"Function expects return type "
                    f"'{self.current_function_return_type}' "
                    f"but received '{expression_type}'."
                ),
            )

    # ==========================================================
    # Expression Type Inference
    # ==========================================================

    def _infer_expression_type(self, expression):
        """
        Determine the semantic type of an expression.

        Returns:
            Type name such as 'int', 'float', 'bool',
            or None when the expression contains an
            unresolved or invalid semantic construct.
        """

        if isinstance(expression, Literal):
            return expression.value_type

        if isinstance(expression, Identifier):
            return self._resolve_identifier(expression)

        if isinstance(expression, BinaryExpression):
            return self._analyze_binary_expression(
                expression
            )

        if isinstance(expression, UnaryExpression):
            return self._analyze_unary_expression(
                expression
            )

        return None

    # ==========================================================
    # Identifier Resolution
    # ==========================================================

    def _resolve_identifier(self, identifier):
        """
        Resolve an identifier through the symbol table.

        Returns:
            The identifier's type if declared.
            None if the identifier is undeclared.
        """

        symbol = self.symbol_table.lookup(
            identifier.name
        )

        if symbol is None:
            self._add_error(
                "undeclared_identifier",
                (
                    f"Variable '{identifier.name}' "
                    f"has not been declared."
                ),
            )

            return None

        return symbol.symbol_type

    # ==========================================================
    # Binary Expression Analysis
    # ==========================================================

    def _analyze_binary_expression(self, expression):
        """
        Analyze a binary expression and determine its type.
        """

        left_type = self._infer_expression_type(
            expression.left
        )

        right_type = self._infer_expression_type(
            expression.right
        )

        operator = expression.operator

        # If either operand cannot be resolved, do not produce
        # another cascading error for the parent expression.
        if left_type is None or right_type is None:
            return None

        # ------------------------------------------------------
        # Arithmetic operators
        # ------------------------------------------------------

        if operator in {
            "+",
            "-",
            "*",
            "/",
            "%",
        }:
            if not self._is_numeric_type(left_type):
                self._add_error(
                    "invalid_operand_type",
                    (
                        f"Operator '{operator}' cannot be "
                        f"applied to type '{left_type}'."
                    ),
                )
                return None

            if not self._is_numeric_type(right_type):
                self._add_error(
                    "invalid_operand_type",
                    (
                        f"Operator '{operator}' cannot be "
                        f"applied to type '{right_type}'."
                    ),
                )
                return None

            if (
                left_type == "float"
                or right_type == "float"
            ):
                return "float"

            return "int"

        # ------------------------------------------------------
        # Comparison operators
        # ------------------------------------------------------

        if operator in {
            "==",
            "!=",
            "<",
            "<=",
            ">",
            ">=",
        }:
            if not self._are_comparable(
                left_type,
                right_type,
            ):
                self._add_error(
                    "incompatible_comparison",
                    (
                        f"Cannot compare values of type "
                        f"'{left_type}' and "
                        f"'{right_type}'."
                    ),
                )

                return None

            return "bool"

        # ------------------------------------------------------
        # Logical operators
        # ------------------------------------------------------

        if operator in {
            "&&",
            "||",
        }:
            if left_type != "bool":
                self._add_error(
                    "invalid_logical_operand",
                    (
                        f"Logical operator '{operator}' "
                        f"requires boolean operands, "
                        f"but received '{left_type}'."
                    ),
                )

                return None

            if right_type != "bool":
                self._add_error(
                    "invalid_logical_operand",
                    (
                        f"Logical operator '{operator}' "
                        f"requires boolean operands, "
                        f"but received '{right_type}'."
                    ),
                )

                return None

            return "bool"

        return None

    # ==========================================================
    # Unary Expression Analysis
    # ==========================================================

    def _analyze_unary_expression(self, expression):
        """
        Analyze a unary expression.
        """

        operand_type = self._infer_expression_type(
            expression.operand
        )

        # An unresolved operand should not generate a
        # second diagnostic at the unary-expression level.
        if operand_type is None:
            return None

        if expression.operator in {
            "+",
            "-",
        }:
            if not self._is_numeric_type(
                operand_type
            ):
                self._add_error(
                    "invalid_operand_type",
                    (
                        f"Unary operator "
                        f"'{expression.operator}' "
                        f"requires a numeric operand, "
                        f"but received '{operand_type}'."
                    ),
                )

                return None

            return operand_type

        if expression.operator == "!":
            if operand_type != "bool":
                self._add_error(
                    "invalid_logical_operand",
                    (
                        "Logical NOT requires a boolean "
                        f"operand, but received "
                        f"'{operand_type}'."
                    ),
                )

                return None

            return "bool"

        return None

    # ==========================================================
    # Type Utilities
    # ==========================================================

    def _is_numeric_type(self, symbol_type):
        """
        Return True for numeric types.
        """

        return symbol_type in {
            "int",
            "float",
        }

    def _are_comparable(self, left_type, right_type):
        """
        Determine whether two types can be compared.
        """

        if left_type == right_type:
            return True

        if (
            self._is_numeric_type(left_type)
            and self._is_numeric_type(right_type)
        ):
            return True

        return False

    def _is_type_compatible(
        self,
        expected_type,
        actual_type,
    ):
        """
        Determine whether a value can be used where
        another type is expected.

        For this educational compiler:
        - identical types are compatible
        - int can be used where float is expected
        """

        if actual_type is None:
            return False

        if expected_type == actual_type:
            return True

        if (
            expected_type == "float"
            and actual_type == "int"
        ):
            return True

        return False

    # ==========================================================
    # Error Handling
    # ==========================================================

    def _add_error(self, error_type, message):
        """
        Add a semantic error to the result list.
        """

        self.errors.append(
            SemanticError(
                error_type=error_type,
                message=message,
            )
        )