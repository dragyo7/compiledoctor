"""
Graphviz renderer for the CompileDoctor Abstract Syntax Tree.

Responsibilities:

- Accept a Program AST.
- Convert AST nodes into a Graphviz directed graph.
- Represent compiler structure visually.
- Support rendering the graph in memory.
- Support rendering the graph to a file.

This module does not:

- perform lexical analysis
- perform parsing
- perform semantic analysis
- modify the AST
- generate compiler diagnostics
- perform source-code repair
"""

from graphviz import Digraph

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


class ASTGraphvizRenderer:
    """
    Convert a CompileDoctor AST into a Graphviz directed graph.

    The renderer creates one Graphviz node for every AST node
    and connects parent nodes to their children.
    """

    def __init__(self):
        """
        Initialize the renderer.
        """

        self.graph = None
        self._node_counter = 0

    # ==========================================================
    # Internal State
    # ==========================================================

    def _reset(self):
        """
        Reset renderer state so the renderer can be reused.
        """

        self.graph = Digraph(
            name="CompileDoctorAST",
            comment="CompileDoctor Abstract Syntax Tree",
        )

        self.graph.attr(
            rankdir="TB",
        )

        self.graph.attr(
            "node",
            shape="box",
        )

        self._node_counter = 0

    def _new_node_id(self):
        """
        Generate a unique Graphviz node identifier.
        """

        node_id = f"node_{self._node_counter}"
        self._node_counter += 1

        return node_id

    def _add_node(self, label):
        """
        Add a node to the Graphviz graph.

        Returns:
            The generated Graphviz node identifier.
        """

        node_id = self._new_node_id()

        self.graph.node(
            node_id,
            label=label,
        )

        return node_id

    def _add_edge(self, parent_id, child_id):
        """
        Connect a parent AST node to a child AST node.
        """

        self.graph.edge(
            parent_id,
            child_id,
        )

    # ==========================================================
    # AST Rendering
    # ==========================================================

    def render(self, program):
        """
        Render a Program AST into a Graphviz Digraph.

        Args:
            program:
                CompileDoctor Program AST.

        Returns:
            graphviz.Digraph

        Raises:
            TypeError:
                If the supplied root is not a Program.
        """

        if not isinstance(program, Program):
            raise TypeError(
                "AST root must be a Program instance."
            )

        self._reset()

        self._render_program(program)

        return self.graph

    def _render_program(self, program):
        """
        Render the Program node.
        """

        program_id = self._add_node("Program")

        for function in program.functions:
            function_id = self._render_function(function)
            self._add_edge(program_id, function_id)

    def _render_function(self, function):
        """
        Render a Function node.
        """

        label = (
            "Function\n"
            f"return type: {function.return_type}\n"
            f"name: {function.name}"
)

        function_id = self._add_node(label)

        body_id = self._render_block(function.body)

        self._add_edge(
            function_id,
            body_id,
        )

        return function_id

    def _render_block(self, block):
        """
        Render a Block node.
        """

        block_id = self._add_node("Block")

        for statement in block.statements:
            statement_id = self._render_node(statement)

            if statement_id is not None:
                self._add_edge(
                    block_id,
                    statement_id,
                )

        return block_id

    # ==========================================================
    # Statement Rendering
    # ==========================================================

    def _render_node(self, node):
        """
        Dispatch rendering according to AST node type.

        Returns:
            Graphviz node identifier.
        """

        if isinstance(node, VariableDeclaration):
            return self._render_variable_declaration(node)

        if isinstance(node, Assignment):
            return self._render_assignment(node)

        if isinstance(node, ReturnStatement):
            return self._render_return_statement(node)

        if isinstance(node, BinaryExpression):
            return self._render_binary_expression(node)

        if isinstance(node, UnaryExpression):
            return self._render_unary_expression(node)

        if isinstance(node, Identifier):
            return self._render_identifier(node)

        if isinstance(node, Literal):
            return self._render_literal(node)

        if isinstance(node, Block):
            return self._render_block(node)

        raise TypeError(
            f"Unsupported AST node type: "
            f"{type(node).__name__}"
        )

    def _render_variable_declaration(self, declaration):
        """
        Render a variable declaration.
        """

        label = (
            "VariableDeclaration\n"
            f"type: {declaration.variable_type}\n"
            f"name: {declaration.name}"
        )

        declaration_id = self._add_node(label)

        if declaration.initializer is not None:
            initializer_id = self._render_node(
                declaration.initializer
            )

            self._add_edge(
                declaration_id,
                initializer_id,
            )

        return declaration_id

    def _render_assignment(self, assignment):
        """
        Render an assignment.
        """

        label = (
            "Assignment\n"
            f"name: {assignment.name}"
        )

        assignment_id = self._add_node(label)

        expression_id = self._render_node(
            assignment.expression
        )

        self._add_edge(
            assignment_id,
            expression_id,
        )

        return assignment_id

    def _render_return_statement(self, statement):
        """
        Render a return statement.
        """

        return_id = self._add_node(
            "ReturnStatement"
        )

        if statement.expression is not None:
            expression_id = self._render_node(
                statement.expression
            )

            self._add_edge(
                return_id,
                expression_id,
            )

        return return_id

    # ==========================================================
    # Expression Rendering
    # ==========================================================

    def _render_binary_expression(self, expression):
        """
        Render a binary expression.
        """

        label = (
            "BinaryExpression\n"
            f"operator: {expression.operator}"
        )

        expression_id = self._add_node(label)

        left_id = self._render_node(
            expression.left
        )

        right_id = self._render_node(
            expression.right
        )

        self._add_edge(
            expression_id,
            left_id,
        )

        self._add_edge(
            expression_id,
            right_id,
        )

        return expression_id

    def _render_unary_expression(self, expression):
        """
        Render a unary expression.
        """

        label = (
            "UnaryExpression\n"
            f"operator: {expression.operator}"
        )

        expression_id = self._add_node(label)

        operand_id = self._render_node(
            expression.operand
        )

        self._add_edge(
            expression_id,
            operand_id,
        )

        return expression_id

    def _render_identifier(self, identifier):
        """
        Render an identifier.
        """

        return self._add_node(
            f"Identifier\n"
            f"name: {identifier.name}"
        )

    def _render_literal(self, literal):
        """
        Render a literal.
        """

        label = (
            "Literal\n"
            f"value: {literal.value}\n"
            f"type: {literal.value_type}"
        )

        return self._add_node(label)

    # ==========================================================
    # File Rendering
    # ==========================================================

    def render_to_file(
        self,
        program,
        filename,
        format="png",
        cleanup=True,
    ):
        """
        Render an AST directly to a file.

        Args:
            program:
                CompileDoctor Program AST.

            filename:
                Output filename without requiring an extension.

            format:
                Graphviz output format, such as png, pdf,
                svg, or dot.

            cleanup:
                Remove Graphviz intermediate files when possible.

        Returns:
            Path returned by Graphviz.
        """

        graph = self.render(program)

        return graph.render(
            filename=filename,
            format=format,
            cleanup=cleanup,
        )


# ==============================================================
# Convenience Function
# ==============================================================

def render_ast(program):
    """
    Convenience function for rendering a Program AST.

    Args:
        program:
            CompileDoctor Program AST.

    Returns:
        graphviz.Digraph
    """

    renderer = ASTGraphvizRenderer()

    return renderer.render(program)