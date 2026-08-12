"""
CompileDoctor Abstract Syntax Tree Nodes
========================================

This module defines the Abstract Syntax Tree (AST) nodes used by
the CompileDoctor compiler front-end.

The AST represents the syntactic structure of a source program
in a form that can be processed by later compiler phases.

Current supported concepts:
- Program
- Function
- Block
- Variable declaration
- Assignment
- Return statement
- Identifier
- Literal
- Binary expression
- Unary expression
"""


class ASTNode:
    """
    Base class for all AST nodes.

    The base class provides a common interface for converting
    nodes into readable representations during development and
    testing.
    """

    def __repr__(self):
        return self.__class__.__name__


class Program(ASTNode):
    """
    Root node representing an entire source program.
    """

    def __init__(self, functions=None):
        self.functions = functions or []

    def __repr__(self):
        return f"Program(functions={self.functions!r})"


class Function(ASTNode):
    """
    Represents a function definition.

    Example:

        int main() {
            return 0;
        }
    """

    def __init__(self, return_type, name, body):
        self.return_type = return_type
        self.name = name
        self.body = body

    def __repr__(self):
        return (
            f"Function("
            f"return_type={self.return_type!r}, "
            f"name={self.name!r}, "
            f"body={self.body!r}"
            f")"
        )


class Block(ASTNode):
    """
    Represents a compound statement or block.

    Example:

        {
            int x = 10;
            return x;
        }
    """

    def __init__(self, statements=None):
        self.statements = statements or []

    def __repr__(self):
        return f"Block(statements={self.statements!r})"


class VariableDeclaration(ASTNode):
    """
    Represents a variable declaration.

    Example:

        int x = 10;
    """

    def __init__(self, variable_type, name, initializer=None):
        self.variable_type = variable_type
        self.name = name
        self.initializer = initializer

    def __repr__(self):
        return (
            f"VariableDeclaration("
            f"variable_type={self.variable_type!r}, "
            f"name={self.name!r}, "
            f"initializer={self.initializer!r}"
            f")"
        )


class Assignment(ASTNode):
    """
    Represents assignment to an existing variable.

    Example:

        x = x + 1;
    """

    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __repr__(self):
        return (
            f"Assignment("
            f"name={self.name!r}, "
            f"expression={self.expression!r}"
            f")"
        )


class ReturnStatement(ASTNode):
    """
    Represents a return statement.

    Example:

        return 0;
    """

    def __init__(self, expression=None):
        self.expression = expression

    def __repr__(self):
        return (
            f"ReturnStatement("
            f"expression={self.expression!r}"
            f")"
        )


class Identifier(ASTNode):
    """
    Represents a variable or function identifier.
    """

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier(name={self.name!r})"


class Literal(ASTNode):
    """
    Represents a literal value.

    Examples:

        10
        3.14
        true
        false
    """

    def __init__(self, value, value_type=None):
        self.value = value
        self.value_type = value_type

    def __repr__(self):
        return (
            f"Literal("
            f"value={self.value!r}, "
            f"value_type={self.value_type!r}"
            f")"
        )


class BinaryExpression(ASTNode):
    """
    Represents a binary operation.

    Example:

        x + 10

    Structure:

        left  -> x
        op    -> +
        right -> 10
    """

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return (
            f"BinaryExpression("
            f"left={self.left!r}, "
            f"operator={self.operator!r}, "
            f"right={self.right!r}"
            f")"
        )


class UnaryExpression(ASTNode):
    """
    Represents a unary operation.

    Examples:

        -x
        !condition
    """

    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return (
            f"UnaryExpression("
            f"operator={self.operator!r}, "
            f"operand={self.operand!r}"
            f")"
        )