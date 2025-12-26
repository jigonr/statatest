"""Test discovery for statatest."""

from __future__ import annotations

import re
from fnmatch import fnmatch
from pathlib import Path

from statatest.config import Config
from statatest.models import TestFile


def discover_tests(
    path: Path,
    config: Config,
    marker: str | None = None,
    keyword: str | None = None,
) -> list[TestFile]:
    """Discover test files matching configuration patterns.

    Args:
        path: Path to search for tests (file or directory).
        config: Configuration object with test file patterns.
        marker: Optional marker to filter tests (e.g., "unit", "integration").
        keyword: Optional keyword to filter test files by name.

    Returns:
        List of TestFile objects representing discovered tests.
    """
    test_files: list[TestFile] = []

    if path.is_file():
        # Single file specified
        if _is_test_file(path, config.test_files):
            test_file = _parse_test_file(path)
            if _matches_filters(test_file, marker, keyword):
                test_files.append(test_file)
    else:
        # Directory - search recursively
        for pattern in config.test_files:
            for file_path in path.rglob(pattern):
                if file_path.is_file():
                    test_file = _parse_test_file(file_path)
                    if _matches_filters(test_file, marker, keyword):
                        test_files.append(test_file)

    # Sort by path for consistent ordering
    test_files.sort(key=lambda t: t.path)

    return test_files


def _is_test_file(path: Path, patterns: list[str]) -> bool:
    """Check if path matches any test file pattern."""
    return any(fnmatch(path.name, pattern) for pattern in patterns)


def _parse_test_file(path: Path) -> TestFile:
    """Parse a test file to extract markers and program definitions.

    Markers are extracted from comments like:
        // @marker: unit
        // @marker: slow

    Programs are extracted from:
        program define test_something
    """
    markers: list[str] = []
    programs: list[str] = []

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = path.read_text(encoding="latin-1")

    # Extract markers
    marker_pattern = re.compile(r"//\s*@marker:\s*(\w+)", re.IGNORECASE)
    for match in marker_pattern.finditer(content):
        markers.append(match.group(1).lower())

    # Extract program definitions
    program_pattern = re.compile(
        r"^\s*program\s+(?:define\s+)?(\w+)", re.MULTILINE | re.IGNORECASE
    )
    for match in program_pattern.finditer(content):
        name = match.group(1)
        if name.startswith("test_"):
            programs.append(name)

    return TestFile(path=path, markers=markers, programs=programs)


def _matches_filters(
    test_file: TestFile, marker: str | None, keyword: str | None
) -> bool:
    """Check if test file matches the specified filters."""
    if marker and marker.lower() not in test_file.markers:
        return False

    if keyword and keyword.lower() not in test_file.name.lower():
        return False

    return True
