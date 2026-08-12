"""
Syntax analyzer for the CompileDoctor educational compiler.

Responsibilities:

- Consume tokens produced by the lexer.
- Validate source code against the language grammar.
- Construct the Abstract Syntax Tree (AST).
- Apply operator precedence.
- Report syntax errors.
- Record recoverable syntax errors.

The parser does not perform:

- Semantic analysis
- Type checking
- Symbol-table validation
- Final diagnostic formatting
- Semantic diagnostic formatting
- Automatic source-code repair
"""

import ply.yacc as yacc

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
from backend.constants import TOKENS
from backend.lexer.lexer import CompileDoctorLexer
from backend.recovery.recovery import ErrorRecovery


class CompileDoctorParser:
    """
    Parser wrapper around PLY Yacc.

    Converts the token stream produced by the lexer
    into an Abstract Syntax Tree.
    """

    tokens = TOKENS

    # ==========================================================
    # Operator Precedence
    # ==========================================================

    precedence = (
        ("left", "OR"),
        ("left", "AND"),
        ("left", "EQUAL", "NOT_EQUAL"),
        (
            "left",
            "LESS_THAN",
            "LESS_EQUAL",
            "GREATER_THAN",
            "GREATER_EQUAL",
        ),
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE", "MODULO"),
        ("right", "NOT"),
        ("right", "UMINUS"),
        ("right", "UPLUS"),
    )

    # ==========================================================
    # Initialization
    # ==========================================================

    def __init__(self):
        """
        Initialize the lexer, parser, and recovery manager.
        """

        self.lexer = CompileDoctorLexer()
        self.lexer.build()

        self.parser = None

        # Stores syntax errors generated during parsing.
        self.recovery = ErrorRecovery()

    # ==========================================================
    # Type Specifier
    # ==========================================================

    def p_type_specifier(self, production):
        """
        type_specifier : INT
                       | FLOAT
                       | CHAR
                       | BOOL
                       | VOID
        """

        production[0] = production[1]

    # ==========================================================
    # Program
    # ==========================================================

    def p_program(self, production):
        """
        program : function_list
        """

        production[0] = Program(
            functions=production[1]
        )

    # ==========================================================
    # Function List
    # ==========================================================

    def p_function_list_multiple(self, production):
        """
        function_list : function_list function
        """

        production[0] = production[1] + [production[2]]

    def p_function_list_single(self, production):
        """
        function_list : function
        """

        production[0] = [production[1]]

    # ==========================================================
    # Function
    # ==========================================================

    def p_function(self, production):
        """
        function : type_specifier IDENTIFIER LPAREN RPAREN compound_statement
        """

        production[0] = Function(
            return_type=production[1],
            name=production[2],
            body=production[5],
        )

    # ==========================================================
    # Compound Statement
    # ==========================================================

    def p_compound_statement(self, production):
        """
        compound_statement : LBRACE statement_list RBRACE
                            | LBRACE RBRACE
        """

        if len(production) == 4:
            statements = production[2]
        else:
            statements = []

        production[0] = Block(
            statements=statements
        )

    # ==========================================================
    # Statement List
    # ==========================================================

    def p_statement_list_multiple(self, production):
        """
        statement_list : statement_list statement
        """

        production[0] = production[1] + [production[2]]

    def p_statement_list_single(self, production):
        """
        statement_list : statement
        """

        production[0] = [production[1]]

    # ==========================================================
    # Statements
    # ==========================================================

    def p_statement(self, production):
        """
        statement : variable_declaration
                  | assignment_statement
                  | return_statement
                  | expression_statement
        """

        production[0] = production[1]

    # ==========================================================
    # Variable Declaration
    # ==========================================================

    def p_variable_declaration_initialized(self, production):
        """
        variable_declaration : type_specifier IDENTIFIER ASSIGN expression SEMICOLON
        """

        production[0] = VariableDeclaration(
            variable_type=production[1],
            name=production[2],
            initializer=production[4],
        )

    def p_variable_declaration_uninitialized(self, production):
        """
        variable_declaration : type_specifier IDENTIFIER SEMICOLON
        """

        production[0] = VariableDeclaration(
            variable_type=production[1],
            name=production[2],
            initializer=None,
        )

    # ==========================================================
    # Assignment
    # ==========================================================

    def p_assignment_statement(self, production):
        """
        assignment_statement : IDENTIFIER ASSIGN expression SEMICOLON
        """

        production[0] = Assignment(
            name=production[1],
            expression=production[3],
        )

    # ==========================================================
    # Return Statement
    # ==========================================================

    def p_return_statement_expression(self, production):
        """
        return_statement : RETURN expression SEMICOLON
        """

        production[0] = ReturnStatement(
            expression=production[2]
        )

    def p_return_statement_empty(self, production):
        """
        return_statement : RETURN SEMICOLON
        """

        production[0] = ReturnStatement(
            expression=None
        )

    # ==========================================================
    # Expression Statement
    # ==========================================================

    def p_expression_statement(self, production):
        """
        expression_statement : expression SEMICOLON
        """

        production[0] = production[1]

    # ==========================================================
    # Expressions
    # ==========================================================

    def p_expression_binary(self, production):
        """
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression TIMES expression
                   | expression DIVIDE expression
                   | expression MODULO expression
                   | expression LESS_THAN expression
                   | expression LESS_EQUAL expression
                   | expression GREATER_THAN expression
                   | expression GREATER_EQUAL expression
                   | expression EQUAL expression
                   | expression NOT_EQUAL expression
                   | expression AND expression
                   | expression OR expression
        """

        production[0] = BinaryExpression(
            left=production[1],
            operator=production[2],
            right=production[3],
        )

    # ==========================================================
    # Unary Expressions
    # ==========================================================

    def p_expression_unary_minus(self, production):
        """
        expression : MINUS expression %prec UMINUS
        """

        production[0] = UnaryExpression(
            operator="-",
            operand=production[2],
        )

    def p_expression_unary_plus(self, production):
        """
        expression : PLUS expression %prec UPLUS
        """

        production[0] = UnaryExpression(
            operator="+",
            operand=production[2],
        )

    def p_expression_not(self, production):
        """
        expression : NOT expression
        """

        production[0] = UnaryExpression(
            operator="!",
            operand=production[2],
        )

    # ==========================================================
    # Parenthesized Expression
    # ==========================================================

    def p_expression_grouped(self, production):
        """
        expression : LPAREN expression RPAREN
        """

        production[0] = production[2]

    # ==========================================================
    # Identifier
    # ==========================================================

    def p_expression_identifier(self, production):
        """
        expression : IDENTIFIER
        """

        production[0] = Identifier(
            name=production[1]
        )

    # ==========================================================
    # Integer Literal
    # ==========================================================

    def p_expression_integer(self, production):
        """
        expression : INTEGER
        """

        production[0] = Literal(
            value=production[1],
            value_type="int",
        )

    # ==========================================================
    # Floating-Point Literal
    # ==========================================================

    def p_expression_float(self, production):
        """
        expression : FLOAT_NUMBER
        """

        production[0] = Literal(
            value=production[1],
            value_type="float",
        )

    # ==========================================================
    # Boolean Literals
    # ==========================================================

    def p_expression_true(self, production):
        """
        expression : TRUE
        """

        production[0] = Literal(
            value=True,
            value_type="bool",
        )

    def p_expression_false(self, production):
        """
        expression : FALSE
        """

        production[0] = Literal(
            value=False,
            value_type="bool",
        )

    # ==========================================================
    # Syntax Error Handler
    # ==========================================================

    def p_error(self, token):
        """
        Handle syntax errors detected by PLY.

        Syntax errors are recorded through the recovery layer.
        The parser does not modify the source code.
        """

        if token is None:
            self.recovery.record_error(
                message="Unexpected end of input.",
            )

            return

        column = self.find_column(token)

        self.recovery.record_error(
            message=f"Unexpected token '{token.value}'.",
            line=token.lineno,
            column=column,
            token_type=token.type,
            token_value=token.value,
        )

        # Tell PLY that the current syntax error has been handled.
        self.parser.errok()

    # ==========================================================
    # Column Calculation
    # ==========================================================

    def find_column(self, token):
        """
        Calculate the column position of a token.
        """

        source = self.lexer.source_code

        line_start = (
            source.rfind(
                "\n",
                0,
                token.lexpos,
            ) + 1
        )

        return token.lexpos - line_start + 1

    # ==========================================================
    # Build Parser
    # ==========================================================

    def build(self, **kwargs):
        """
        Build the PLY parser.
        """

        self.parser = yacc.yacc(
            module=self,
            start="program",
            **kwargs,
        )

    # ==========================================================
    # Parse Source Code
    # ==========================================================

    def parse(self, source_code):
        """
        Parse source code and return its AST.

        Syntax errors encountered during parsing are stored
        by the recovery manager.
        """

        if self.parser is None:
            raise RuntimeError(
                "Parser has not been built. "
                "Call build() first."
            )

        # Remove errors from any previous parse operation.
        self.recovery.clear()

        return self.parser.parse(
            source_code,
            lexer=self.lexer.lexer,
        )