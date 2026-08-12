from graphviz import Digraph
import pytest

from backend.ast_nodes.nodes import (
    Assignment,
    BinaryExpression,
    Block,
    Function,
    Identifier,
    Literal,
    Program,
    ReturnStatement,
    UnaryExpression,
    VariableDeclaration,
)

from backend.utils.graphviz_renderer import (
    ASTGraphvizRenderer,
    render_ast,
)


def create_sample_ast():
    return Program(
        functions=[
            Function(
                return_type="int",
                name="main",
                body=Block(
                    statements=[
                        VariableDeclaration(
                            variable_type="int",
                            name="x",
                            initializer=Literal(
                                value=10,
                                value_type="int",
                            ),
                        ),
                        Assignment(
                            name="x",
                            expression=BinaryExpression(
                                left=Identifier("x"),
                                operator="+",
                                right=Literal(
                                    value=1,
                                    value_type="int",
                                ),
                            ),
                        ),
                        ReturnStatement(
                            expression=Identifier("x"),
                        ),
                    ]
                ),
            )
        ]
    )


def test_renderer_can_be_created():
    renderer = ASTGraphvizRenderer()

    assert renderer is not None


def test_render_returns_graphviz_graph():
    renderer = ASTGraphvizRenderer()
    ast = create_sample_ast()

    graph = renderer.render(ast)

    assert isinstance(graph, Digraph)


def test_render_contains_program():
    renderer = ASTGraphvizRenderer()
    ast = create_sample_ast()

    graph = renderer.render(ast)

    assert "Program" in graph.source


def test_render_contains_function():
    renderer = ASTGraphvizRenderer()
    ast = create_sample_ast()

    graph = renderer.render(ast)

    assert "Function" in graph.source
    assert "main" in graph.source
    assert "return type: int" in graph.source


def test_render_contains_variable_declaration():
    renderer = ASTGraphvizRenderer()
    ast = create_sample_ast()

    graph = renderer.render(ast)

    assert "VariableDeclaration" in graph.source
    assert "name: x" in graph.source


def test_render_contains_binary_expression():
    renderer = ASTGraphvizRenderer()
    ast = create_sample_ast()

    graph = renderer.render(ast)

    assert "BinaryExpression" in graph.source
    assert "operator: +" in graph.source


def test_render_contains_return_statement():
    renderer = ASTGraphvizRenderer()
    ast = create_sample_ast()

    graph = renderer.render(ast)

    assert "ReturnStatement" in graph.source


def test_renderer_rejects_non_program_root():
    renderer = ASTGraphvizRenderer()

    with pytest.raises(TypeError):
        renderer.render(
            Literal(
                value=10,
                value_type="int",
            )
        )


def test_convenience_render_function():
    ast = create_sample_ast()

    graph = render_ast(ast)

    assert isinstance(graph, Digraph)


def test_renderer_can_be_reused():
    renderer = ASTGraphvizRenderer()

    ast = create_sample_ast()

    first_graph = renderer.render(ast)
    second_graph = renderer.render(ast)

    assert isinstance(first_graph, Digraph)
    assert isinstance(second_graph, Digraph)
    assert "Program" in second_graph.source