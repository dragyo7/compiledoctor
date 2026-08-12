"""
CompileDoctor Diagnostic Explanations
=====================================

Contains the educational explanations used by the Diagnostics
layer.

This module is intentionally independent of:
- the lexer
- the parser
- the AST
- semantic analysis
- Flask
- frontend presentation

Its responsibility is to explain compiler error categories
in beginner-friendly language.
"""


EXPLANATIONS = {
    "duplicate_declaration": {
        "title": "Duplicate Variable Declaration",
        "what_happened": (
            "A variable with the same name has already been "
            "declared in the current scope."
        ),
        "why": (
            "A variable name cannot be declared more than once "
            "within the same scope."
        ),
        "possible_fix": (
            "Use a different variable name or remove the "
            "duplicate declaration."
        ),
        "example": (
            "int x = 10;\n"
            "int y = 20;"
        ),
    },

    "undeclared_identifier": {
        "title": "Undeclared Identifier",
        "what_happened": (
            "The program uses a variable that has not been "
            "declared."
        ),
        "why": (
            "The compiler could not find a declaration for "
            "the variable in the current scope."
        ),
        "possible_fix": (
            "Declare the variable before using it."
        ),
        "example": (
            "int x = 10;\n"
            "x = x + 1;"
        ),
    },

    "type_mismatch": {
        "title": "Type Mismatch",
        "what_happened": (
            "A value is being used where a different data type "
            "is expected."
        ),
        "why": (
            "The type of the value is not compatible with the "
            "type required by the variable or operation."
        ),
        "possible_fix": (
            "Use a compatible value or change the declaration "
            "to use the appropriate type."
        ),
        "example": (
            "int x = 10;\n"
            "float y = 2.5;"
        ),
    },

    "return_type_mismatch": {
        "title": "Return Type Mismatch",
        "what_happened": (
            "The value returned by a function does not match "
            "the function's declared return type."
        ),
        "why": (
            "A function's return expression must be compatible "
            "with the return type specified in its declaration."
        ),
        "possible_fix": (
            "Return a value compatible with the function's "
            "declared return type."
        ),
        "example": (
            "int main() {\n"
            "    return 0;\n"
            "}"
        ),
    },

    "invalid_operand_type": {
        "title": "Invalid Operand Type",
        "what_happened": (
            "An operator is being used with a data type that "
            "the operator does not support."
        ),
        "why": (
            "Different operators require compatible operand "
            "types. Arithmetic operators require numeric values."
        ),
        "possible_fix": (
            "Use compatible operand types with the operator."
        ),
        "example": (
            "int x = 10;\n"
            "int y = x + 5;"
        ),
    },

    "invalid_logical_operand": {
        "title": "Invalid Logical Operand",
        "what_happened": (
            "A logical operator is being used with a value that "
            "is not boolean."
        ),
        "why": (
            "Logical operators such as &&, ||, and ! operate "
            "on boolean expressions."
        ),
        "possible_fix": (
            "Use boolean expressions with logical operators."
        ),
        "example": (
            "bool a = true;\n"
            "bool b = false;\n"
            "bool result = a && b;"
        ),
    },

    "incompatible_comparison": {
        "title": "Incompatible Comparison",
        "what_happened": (
            "The program attempts to compare values with "
            "incompatible types."
        ),
        "why": (
            "Comparison operators require values that can be "
            "meaningfully compared."
        ),
        "possible_fix": (
            "Compare values with compatible data types."
        ),
        "example": (
            "int x = 10;\n"
            "int y = 20;\n"
            "bool result = x < y;"
        ),
    },
}


def get_explanation(error_type):
    """
    Return the educational explanation for an error type.

    Args:
        error_type: Internal compiler error category.

    Returns:
        A dictionary containing the explanation fields, or
        None when the error type is not recognized.
    """

    return EXPLANATIONS.get(error_type)


def has_explanation(error_type):
    """
    Check whether an educational explanation exists.

    Args:
        error_type: Internal compiler error category.

    Returns:
        True if an explanation exists, otherwise False.
    """

    return error_type in EXPLANATIONS