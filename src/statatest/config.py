"""Configuration management for statatest."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


@dataclass
class Config:
    """Configuration for statatest."""

    testpaths: list[str] = field(default_factory=lambda: ["tests"])
    test_files: list[str] = field(default_factory=lambda: ["test_*.do"])
    stata_executable: str = "stata-mp"
    verbose: bool = False
    coverage_source: list[str] = field(default_factory=list)
    coverage_omit: list[str] = field(default_factory=list)
    reporting: dict[str, str] = field(default_factory=dict)


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
    """Load TOML file."""
    with open(path, "rb") as f:
        return tomllib.load(f)


def _apply_settings(config: Config, settings: dict[str, Any]) -> None:
    """Apply settings dictionary to config object."""
    if "testpaths" in settings:
        config.testpaths = settings["testpaths"]
    if "test_files" in settings:
        config.test_files = settings["test_files"]
    if "stata_executable" in settings:
        config.stata_executable = settings["stata_executable"]
    if "verbose" in settings:
        config.verbose = settings["verbose"]

    # Coverage settings
    coverage = settings.get("coverage", {})
    if "source" in coverage:
        config.coverage_source = coverage["source"]
    if "omit" in coverage:
        config.coverage_omit = coverage["omit"]

    # Reporting settings
    config.reporting = settings.get("reporting", {})
