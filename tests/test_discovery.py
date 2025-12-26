"""Tests for test discovery module."""

from pathlib import Path
import tempfile

import pytest

from statatest.config import Config
from statatest.discovery import discover_tests, _parse_test_file


@pytest.fixture
def temp_test_dir():
    """Create a temporary directory with test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create test files
        (tmppath / "test_foo.do").write_text(
            """
// test_foo.do
// @marker: unit
// @marker: fast

program define test_something
    assert 1 == 1
end
"""
        )

        (tmppath / "test_bar.do").write_text(
            """
// test_bar.do
// @marker: integration

program define test_other
    assert 2 == 2
end
"""
        )

        (tmppath / "not_a_test.do").write_text("// Not a test file")

        yield tmppath


def test_discover_tests_finds_test_files(temp_test_dir: Path):
    """Test that discover_tests finds test_*.do files."""
    config = Config()
    tests = discover_tests(temp_test_dir, config)

    assert len(tests) == 2
    names = {t.name for t in tests}
    assert "test_foo" in names
    assert "test_bar" in names


def test_discover_tests_respects_marker_filter(temp_test_dir: Path):
    """Test that marker filtering works."""
    config = Config()

    # Filter by 'unit' marker
    tests = discover_tests(temp_test_dir, config, marker="unit")
    assert len(tests) == 1
    assert tests[0].name == "test_foo"

    # Filter by 'integration' marker
    tests = discover_tests(temp_test_dir, config, marker="integration")
    assert len(tests) == 1
    assert tests[0].name == "test_bar"


def test_discover_tests_respects_keyword_filter(temp_test_dir: Path):
    """Test that keyword filtering works."""
    config = Config()

    # Filter by 'foo' keyword
    tests = discover_tests(temp_test_dir, config, keyword="foo")
    assert len(tests) == 1
    assert tests[0].name == "test_foo"


def test_parse_test_file_extracts_markers(temp_test_dir: Path):
    """Test that markers are correctly extracted."""
    test_file = _parse_test_file(temp_test_dir / "test_foo.do")

    assert "unit" in test_file.markers
    assert "fast" in test_file.markers


def test_parse_test_file_extracts_programs(temp_test_dir: Path):
    """Test that program definitions are extracted."""
    test_file = _parse_test_file(temp_test_dir / "test_foo.do")

    assert "test_something" in test_file.programs
