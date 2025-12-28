"""Tests for configuration module."""

import tempfile
from pathlib import Path

from statatest.core.config import Config, load_config


def test_default_config():
    """Test default configuration values."""
    config = Config()

    assert config.testpaths == ["tests"]
    assert config.test_files == ["test_*.do"]
    assert config.stata_executable == "stata-mp"
    assert config.verbose is False


def test_load_config_from_statatest_toml():
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

        config = load_config(tmppath)

        assert config.testpaths == ["my_tests"]
        assert config.stata_executable == "stata-se"
        assert config.coverage_source == ["code"]
        assert config.coverage_omit == ["tests/*"]


def test_load_config_from_pyproject_toml():
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

        config = load_config(tmppath)

        assert config.testpaths == ["tests", "integration"]
        assert config.verbose is True


def test_load_config_statatest_toml_takes_precedence():
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

        config = load_config(tmppath)

        # statatest.toml should win
        assert config.stata_executable == "stata-mp"


def test_load_config_no_config_file():
    """Test that defaults are used when no config file exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = load_config(Path(tmpdir))

        # Should use defaults
        assert config.testpaths == ["tests"]
        assert config.stata_executable == "stata-mp"


def test_default_config_adopath_settings():
    """Test default adopath configuration values."""
    config = Config()

    assert config.adopath_mode == "auto"
    assert config.adopath == []
    assert config.setup_do is None
    assert config.timeout == 300


def test_load_config_adopath_none_mode():
    """Test loading config with adopath_mode = 'none'."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        (tmppath / "statatest.toml").write_text(
            """
[tool.statatest]
adopath_mode = "none"
"""
        )

        config = load_config(tmppath)
        assert config.adopath_mode == "none"


def test_load_config_custom_adopaths():
    """Test loading config with custom adopath entries."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        (tmppath / "statatest.toml").write_text(
            """
[tool.statatest]
adopath_mode = "custom"
adopath = ["./code/functions", "./lib/ado"]
"""
        )

        config = load_config(tmppath)
        assert config.adopath_mode == "custom"
        assert config.adopath == ["./code/functions", "./lib/ado"]


def test_load_config_setup_do():
    """Test loading config with setup_do option."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        (tmppath / "statatest.toml").write_text(
            """
[tool.statatest]
setup_do = "tests/setup.do"
"""
        )

        config = load_config(tmppath)
        assert config.setup_do == "tests/setup.do"


def test_load_config_timeout():
    """Test loading config with custom timeout."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        (tmppath / "statatest.toml").write_text(
            """
[tool.statatest]
timeout = 600
"""
        )

        config = load_config(tmppath)
        assert config.timeout == 600
