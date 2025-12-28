"""Configuration management for statatest.

This module provides:
- Config: Dataclass holding all configuration options
- load_config: Function to load configuration from TOML files
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from statatest.core.constants import (
    DEFAULT_STATA_EXECUTABLE,
    DEFAULT_TEST_FILE_PATTERNS,
    DEFAULT_TEST_PATHS,
    DEFAULT_TIMEOUT_SECONDS,
)


@dataclass
class Config:
    """Configuration for statatest.

    Attributes:
        testpaths: Directories to search for test files.
        test_files: Glob patterns for test file names.
        stata_executable: Path or name of Stata executable.
        timeout: Timeout in seconds for each test file.
        verbose: Whether to show verbose output.
        adopath_mode: How to handle ado path setup:
            - "auto": Add statatest assertions/fixtures to adopath (default)
            - "none": User manages adopath (packages already installed)
            - "custom": Use only paths from adopath list
        adopath: Additional paths to add to Stata's adopath.
        setup_do: Path to a setup.do file to run before each test.
        coverage_source: Directories containing source files for coverage.
        coverage_omit: Patterns for files to exclude from coverage.
        reporting: Reporting configuration (junit_xml, lcov paths).
    """

    testpaths: list[str] = field(default_factory=list)
    test_files: list[str] = field(default_factory=list)
    stata_executable: str = DEFAULT_STATA_EXECUTABLE
    timeout: int = DEFAULT_TIMEOUT_SECONDS
    verbose: bool = False
    adopath_mode: str = "auto"
    adopath: list[str] = field(default_factory=list)
    setup_do: str | None = None
    coverage_source: list[str] = field(default_factory=list)
    coverage_omit: list[str] = field(default_factory=list)
    reporting: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Apply default values for empty lists.

        This method is called after dataclass __init__ completes.
        It sets default values from constants when lists are empty.
        """
        if not self.testpaths:
            self.testpaths = list(DEFAULT_TEST_PATHS)
        if not self.test_files:
            self.test_files = list(DEFAULT_TEST_FILE_PATTERNS)


def load_config(project_root: Path) -> Config:
    """Load configuration from statatest.toml or pyproject.toml.

    Config file precedence (first found wins):
    1. statatest.toml
    2. pyproject.toml [tool.statatest]

    Args:
        project_root: Root directory of the project.

    Returns:
        Config object with merged settings.
    """
    config = Config()

    # Try statatest.toml first
    statatest_toml = project_root / "statatest.toml"
    if statatest_toml.exists():
        data = _load_toml(statatest_toml)
        settings = data.get("tool", {}).get("statatest", data)
        _apply_settings(config, settings)
        return config

    # Fall back to pyproject.toml
    pyproject_toml = project_root / "pyproject.toml"
    if pyproject_toml.exists():
        data = _load_toml(pyproject_toml)
        settings = data.get("tool", {}).get("statatest", {})
        if settings:
            _apply_settings(config, settings)
            return config

    return config


def _load_toml(path: Path) -> dict[str, Any]:
    """Load and parse a TOML file.

    Args:
        path: Path to the TOML file.

    Returns:
        Parsed TOML content as dictionary.
    """
    with path.open("rb") as f:
        return tomllib.load(f)


def _apply_settings(config: Config, settings: dict[str, Any]) -> None:
    """Apply settings dictionary to config object.

    Args:
        config: Config object to modify.
        settings: Dictionary of settings from TOML file.
    """
    _apply_core_settings(config, settings)
    _apply_adopath_settings(config, settings)
    _apply_coverage_settings(config, settings)
    config.reporting = settings.get("reporting", {})


def _apply_core_settings(config: Config, settings: dict[str, Any]) -> None:
    """Apply core settings (testpaths, executable, timeout, verbose).

    Args:
        config: Config object to modify.
        settings: Dictionary of settings from TOML file.
    """
    if "testpaths" in settings:
        config.testpaths = settings["testpaths"]
    if "test_files" in settings:
        config.test_files = settings["test_files"]
    if "stata_executable" in settings:
        config.stata_executable = settings["stata_executable"]
    if "timeout" in settings:
        config.timeout = settings["timeout"]
    if "verbose" in settings:
        config.verbose = settings["verbose"]


def _apply_adopath_settings(config: Config, settings: dict[str, Any]) -> None:
    """Apply adopath settings (mode, custom paths, setup_do).

    Args:
        config: Config object to modify.
        settings: Dictionary of settings from TOML file.
    """
    if "adopath_mode" in settings:
        config.adopath_mode = settings["adopath_mode"]
    if "adopath" in settings:
        config.adopath = settings["adopath"]
    if "setup_do" in settings:
        config.setup_do = settings["setup_do"]


def _apply_coverage_settings(config: Config, settings: dict[str, Any]) -> None:
    """Apply coverage settings (source, omit).

    Args:
        config: Config object to modify.
        settings: Dictionary of settings from TOML file.
    """
    coverage = settings.get("coverage", {})
    if "source" in coverage:
        config.coverage_source = coverage["source"]
    if "omit" in coverage:
        config.coverage_omit = coverage["omit"]
