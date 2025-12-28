"""Tests for report generation module."""

import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from statatest.models import TestResult
from statatest.report import generate_html, generate_lcov, write_junit_xml


@pytest.fixture
def sample_results():
    """Create sample test results."""
    return [
        TestResult(
            test_file="tests/unit/test_foo.do",
            passed=True,
            duration=1.5,
            assertions_passed=3,
        ),
        TestResult(
            test_file="tests/unit/test_bar.do",
            passed=False,
            duration=0.8,
            error_message="assertion is false",
            assertions_failed=1,
        ),
        TestResult(
            test_file="tests/integration/test_workflow.do",
            passed=True,
            duration=5.2,
            assertions_passed=10,
        ),
    ]


def test_write_junit_xml(sample_results):
    """Test JUnit XML generation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "junit.xml"
        write_junit_xml(sample_results, output_path)

        # Parse and verify XML
        tree = ET.parse(output_path)
        root = tree.getroot()

        assert root.tag == "testsuites"
        assert root.get("tests") == "3"
        assert root.get("failures") == "1"

        # Check testsuites
        testsuites = root.findall("testsuite")
        assert len(testsuites) == 2  # unit and integration

        # Find unit suite
        unit_suite = next(ts for ts in testsuites if ts.get("name") == "unit")
        assert unit_suite.get("tests") == "2"
        assert unit_suite.get("failures") == "1"


def test_write_junit_xml_failure_details(sample_results):
    """Test that failure details are included in JUnit XML."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "junit.xml"
        write_junit_xml(sample_results, output_path)

        tree = ET.parse(output_path)
        root = tree.getroot()

        # Find the failure element
        failures = root.findall(".//failure")
        assert len(failures) == 1
        assert "assertion is false" in failures[0].get("message")


def test_generate_lcov():
    """Test LCOV coverage report generation."""
    results = [
        TestResult(
            test_file="test.do",
            passed=True,
            duration=1.0,
            coverage_hits={
                "myfunction.ado": {1, 2, 3, 5, 7},
                "other.ado": {10, 20},
            },
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "coverage.lcov"
        generate_lcov(results, output_path)

        content = output_path.read_text()

        # Check LCOV format
        assert "TN:statatest" in content
        assert "SF:myfunction.ado" in content
        assert "SF:other.ado" in content
        assert "DA:1,1" in content
        assert "DA:2,1" in content
        assert "end_of_record" in content


def test_generate_lcov_aggregates_coverage():
    """Test that coverage is aggregated across multiple test results."""
    results = [
        TestResult(
            test_file="test1.do",
            passed=True,
            duration=1.0,
            coverage_hits={"myfunction.ado": {1, 2, 3}},
        ),
        TestResult(
            test_file="test2.do",
            passed=True,
            duration=1.0,
            coverage_hits={"myfunction.ado": {3, 4, 5}},
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "coverage.lcov"
        generate_lcov(results, output_path)

        content = output_path.read_text()

        # Lines 1-5 should all be covered (union of both test results)
        for line in range(1, 6):
            assert f"DA:{line},1" in content


def test_write_junit_xml_with_stdout():
    """Test that stdout is included in JUnit XML."""
    results = [
        TestResult(
            test_file="tests/test_example.do",
            passed=True,
            duration=1.0,
            stdout="This is stdout output from the test",
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "junit.xml"
        write_junit_xml(results, output_path)

        content = output_path.read_text()
        assert "<system-out>" in content
        assert "This is stdout output" in content


def test_write_junit_xml_with_stderr():
    """Test that stderr is included in JUnit XML."""
    results = [
        TestResult(
            test_file="tests/test_example.do",
            passed=False,
            duration=1.0,
            error_message="Test failed",
            stderr="This is stderr output from the test",
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "junit.xml"
        write_junit_xml(results, output_path)

        content = output_path.read_text()
        assert "<system-err>" in content
        assert "This is stderr output" in content


def test_generate_html_creates_index():
    """Test that generate_html creates index.html."""
    results = [
        TestResult(
            test_file="test.do",
            passed=True,
            duration=1.0,
            coverage_hits={"myfunction.ado": {1, 2, 3}},
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "htmlcov"
        generate_html(results, output_dir)

        index_path = output_dir / "index.html"
        assert index_path.exists()

        content = index_path.read_text()
        assert "Coverage Report" in content
        assert "myfunction.ado" in content


def test_generate_html_creates_file_reports():
    """Test that generate_html creates per-file HTML reports."""
    results = [
        TestResult(
            test_file="test.do",
            passed=True,
            duration=1.0,
            coverage_hits={
                "myfunction.ado": {1, 2, 3},
                "helper/utils.ado": {10, 20},
            },
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "htmlcov"
        generate_html(results, output_dir)

        # Check per-file reports exist (slashes replaced with underscores)
        assert (output_dir / "myfunction.ado.html").exists()
        assert (output_dir / "helper_utils.ado.html").exists()

        # Check content
        file_content = (output_dir / "myfunction.ado.html").read_text()
        assert "myfunction.ado" in file_content
        assert "Lines hit: 3" in file_content


def test_generate_html_multiple_results():
    """Test that coverage is aggregated across results in HTML report."""
    results = [
        TestResult(
            test_file="test1.do",
            passed=True,
            duration=1.0,
            coverage_hits={"file.ado": {1, 2}},
        ),
        TestResult(
            test_file="test2.do",
            passed=True,
            duration=1.0,
            coverage_hits={"file.ado": {2, 3}},
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "htmlcov"
        generate_html(results, output_dir)

        file_content = (output_dir / "file.ado.html").read_text()
        # Should have lines 1, 2, 3 (union)
        assert "Lines hit: 3" in file_content
