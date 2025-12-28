"""Tests for configuration module."""

import tempfile
from pathlib import Path

from statatest.core.config import Config


def test_default_config() -> None:
    """Test default configuration values."""
    config = Config()

    assert config.testpaths == ["tests"]
    assert config.test_files == ["test_*.do"]
    assert config.stata_executable == "stata-mp"
    assert config.verbose is False
    assert config.setup_do is None
    assert config.timeout == 300


def test_from_project_statatest_toml() -> None:
    """Test loading config from statatest.toml."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create statatest.toml
        (tmppath / "statatest.toml").write_text(
            """
[tool.statatest]
testpaths = ["my_tests"]
stata_executable = "stata-se"

[tool.statatest.coverage]
source = ["code"]
omit = ["tests/*"]
"""
        )

        config = Config.from_project(tmppath)

        assert config.testpaths == ["my_tests"]
        assert config.stata_executable == "stata-se"
        assert config.coverage_source == ["code"]
        assert config.coverage_omit == ["tests/*"]


def test_from_project_pyproject_toml() -> None:
    """Test loading config from pyproject.toml."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create pyproject.toml
        (tmppath / "pyproject.toml").write_text(
            """
[project]
name = "my-project"

[tool.statatest]
testpaths = ["tests", "integration"]
verbose = true
"""
        )

        config = Config.from_project(tmppath)

        assert config.testpaths == ["tests", "integration"]
        assert config.verbose is True


def test_from_project_statatest_toml_takes_precedence() -> None:
    """Test that statatest.toml takes precedence over pyproject.toml."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create both files with different values
        (tmppath / "statatest.toml").write_text(
            """
[tool.statatest]
stata_executable = "stata-mp"
"""
        )

        (tmppath / "pyproject.toml").write_text(
            """
[tool.statatest]
stata_executable = "stata-se"
"""
        )

        config = Config.from_project(tmppath)

        # statatest.toml should win
        assert config.stata_executable == "stata-mp"


def test_from_project_no_config_file() -> None:
    """Test that defaults are used when no config file exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config.from_project(Path(tmpdir))

        # Should use defaults
        assert config.testpaths == ["tests"]
        assert config.stata_executable == "stata-mp"


def test_from_project_setup_do() -> None:
    """Test loading config with setup_do option."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        (tmppath / "statatest.toml").write_text(
            """
[tool.statatest]
setup_do = "tests/setup.do"
"""
        )

        config = Config.from_project(tmppath)
        assert config.setup_do == "tests/setup.do"


def test_from_project_timeout() -> None:
    """Test loading config with custom timeout."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        (tmppath / "statatest.toml").write_text(
            """
[tool.statatest]
timeout = 600
"""
        )

        config = Config.from_project(tmppath)
        assert config.timeout == 600
