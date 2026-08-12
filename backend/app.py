"""
CompileDoctor Flask application.

Provides the HTTP API boundary for the compiler pipeline.

Responsibilities:

- Accept source code through HTTP requests.
- Invoke the compiler pipeline.
- Return structured JSON responses.
- Expose a lightweight health endpoint.

This module does not:

- perform lexical analysis
- perform parsing
- perform semantic analysis
- implement diagnostics
- modify the AST
- contain compiler logic

Those responsibilities remain inside the compiler pipeline.
"""

from flask import Flask, jsonify, request

from backend.compiler import CompileDoctorCompiler
from backend.config import Config


def create_app(config_class=Config):
    """
    Create and configure the CompileDoctor Flask application.

    Using an application factory keeps the application easy
    to test and allows different configurations to be supplied.
    """

    app = Flask(__name__)
    app.config.from_object(config_class)

    compiler = CompileDoctorCompiler()

    @app.get("/api/health")
    def health():
        """Return basic API health information."""

        return jsonify(
            {
                "status": "ok",
                "service": "CompileDoctor",
            }
        )

    @app.post("/api/compile")
    def compile_source():
        """
        Compile source code submitted by the client.

        Expected JSON:

            {
                "source": "int main() { return 0; }"
            }
        """

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify(
                {
                    "success": False,
                    "error": "Request body must be a JSON object.",
                }
            ), 400

        source_code = data.get("source")

        if not isinstance(source_code, str):
            return jsonify(
                {
                    "success": False,
                    "error": "The 'source' field must be a string.",
                }
            ), 400

        try:
            result = compiler.analyze(source_code)

            return jsonify(result), 200

        except Exception as exc:
            return jsonify(
                {
                    "success": False,
                    "error": "Internal compiler error.",
                    "message": str(exc),
                }
            ), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=Config.DEBUG,
    )