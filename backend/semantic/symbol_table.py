"""
CompileDoctor Symbol Table
==========================

Provides a simple symbol table for semantic analysis.

The symbol table stores information about identifiers declared
in the source program.

Current responsibilities:
- Store variable declarations.
- Detect duplicate declarations.
- Look up declared identifiers.
- Check whether an identifier exists.

Scope handling is intentionally simple at this stage.
The implementation can be extended when function/block scope
is integrated into semantic analysis.
"""


class Symbol:
    """
    Represents a declared identifier.

    Attributes:
        name: Identifier name.
        symbol_type: Declared data type.
    """

    def __init__(self, name, symbol_type):
        self.name = name
        self.symbol_type = symbol_type

    def __repr__(self):
        return (
            f"Symbol("
            f"name='{self.name}', "
            f"symbol_type='{self.symbol_type}'"
            f")"
        )


class SymbolTable:
    """
    Stores symbols declared in a program scope.
    """

    def __init__(self):
        self.symbols = {}

    def declare(self, name, symbol_type):
        """
        Declare a new identifier.

        Returns:
            True if the declaration succeeds.
            False if the identifier already exists.
        """

        if name in self.symbols:
            return False

        self.symbols[name] = Symbol(
            name=name,
            symbol_type=symbol_type,
        )

        return True

    def lookup(self, name):
        """
        Look up an identifier.

        Returns:
            Symbol object if found.
            None if the identifier does not exist.
        """

        return self.symbols.get(name)

    def exists(self, name):
        """
        Check whether an identifier exists.
        """

        return name in self.symbols

    def get_type(self, name):
        """
        Return the type of an identifier.

        Returns:
            The declared type if found.
            None otherwise.
        """

        symbol = self.lookup(name)

        if symbol is None:
            return None

        return symbol.symbol_type

    def clear(self):
        """
        Remove all symbols from the table.
        """

        self.symbols.clear()

    def __len__(self):
        """
        Return the number of symbols.
        """

        return len(self.symbols)

    def __repr__(self):
        return f"SymbolTable(symbols={self.symbols!r})"