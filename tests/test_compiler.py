from backend.compiler import (
    CompilationResult,
    CompileDoctorCompiler,
)


def test_compiler_can_be_created():
    compiler = CompileDoctorCompiler()

    assert compiler is not None
    assert compiler.parser is not None


def test_valid_program_compiles_successfully():
    source = """
    int main() {
        int x = 10;
        return x;
    }
    """

    compiler = CompileDoctorCompiler()
    result = compiler.compile(source)

    assert isinstance(result, CompilationResult)
    assert result.success is True
    assert result.ast is not None
    assert result.semantic_errors == []
    assert result.recovery_errors == []


def test_valid_program_produces_ast():
    source = """
    int main() {
        int x = 10;
        return x;
    }
    """

    compiler = CompileDoctorCompiler()
    result = compiler.compile(source)

    assert result.ast is not None
    assert len(result.ast.functions) == 1
    assert result.ast.functions[0].name == "main"


def test_undeclared_variable_fails_semantic_analysis():
    source = """
    int main() {
        return x;
    }
    """

    compiler = CompileDoctorCompiler()
    result = compiler.compile(source)

    assert result.success is False
    assert result.ast is not None
    assert result.recovery_errors == []

    assert len(result.semantic_errors) == 1

    assert (
        result.semantic_errors[0].error_type
        == "undeclared_identifier"
    )


def test_syntax_error_is_recorded_by_recovery():
    source = """
    int main() {
        int x = 10
    }
    """

    compiler = CompileDoctorCompiler()
    result = compiler.compile(source)

    assert result.success is False
    assert len(result.recovery_errors) >= 1
    assert result.semantic_errors == []


def test_analyze_formats_semantic_errors():
    source = """
    int main() {
        return x;
    }
    """

    compiler = CompileDoctorCompiler()
    result = compiler.analyze(source)

    assert result["success"] is False
    assert len(result["semantic_errors"]) == 1
    assert len(result["diagnostics"]) == 1

    diagnostic = result["diagnostics"][0]

    assert diagnostic["error_type"] == "undeclared_identifier"
    assert diagnostic["title"] == "Undeclared Identifier"
    assert diagnostic["message"]


def test_analyze_valid_program_has_no_diagnostics():
    source = """
    int main() {
        int x = 10;
        return x;
    }
    """

    compiler = CompileDoctorCompiler()
    result = compiler.analyze(source)

    assert result["success"] is True
    assert result["semantic_errors"] == []
    assert result["recovery_errors"] == []
    assert result["diagnostics"] == []


def test_compilation_result_to_dict():
    source = """
    int main() {
        int x = 10;
        return x;
    }
    """

    compiler = CompileDoctorCompiler()
    result = compiler.compile(source)

    data = result.to_dict()

    assert data["success"] is True
    assert data["semantic_errors"] == []
    assert data["recovery_errors"] == []


def test_compiler_rejects_non_string_source():
    compiler = CompileDoctorCompiler()

    try:
        compiler.compile(None)
        assert False, "Expected TypeError"
    except TypeError:
        pass