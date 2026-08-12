"""
CompileDoctor server configuration.

Keeps application configuration separate from
the Flask application and compiler implementation.
"""

import os


class Config:
    """Base application configuration."""

    DEBUG = os.getenv("COMPILEDOC_DEBUG", "false").lower() == "true"

    JSON_SORT_KEYS = False

    MAX_CONTENT_LENGTH = 1024 * 1024  # 1 MB


class TestingConfig(Config):
    """Configuration used during automated tests."""

    TESTING = True
    DEBUG = False


class DevelopmentConfig(Config):
    """Configuration used during local development."""

    DEBUG = True