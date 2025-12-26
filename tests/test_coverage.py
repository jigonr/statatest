"""Tests for coverage collection module."""

import tempfile
from pathlib import Path

from statatest.coverage import (
    CoverageReport,
    FileCoverage,
    aggregate_coverage,
    generate_html,
    generate_lcov,
    parse_smcl_log,
)
from statatest.models import TestResult


class TestFileCoverage:
    """Tests for FileCoverage dataclass."""

    def test_coverage_percent_full(self):
        """Test coverage percentage when all lines are covered."""
        cov = FileCoverage(
            filepath="test.ado",
            lines_hit={1, 2, 3},
            lines_total={1, 2, 3},
        )
        assert cov.coverage_percent == 100.0

    def test_coverage_percent_partial(self):
        """Test coverage percentage with partial coverage."""
        cov = FileCoverage(
            filepath="test.ado",
            lines_hit={1, 2},
            lines_total={1, 2, 3, 4},
        )
        assert cov.coverage_percent == 50.0

    def test_coverage_percent_empty_total(self):
        """Test coverage percentage when no lines are expected."""
        cov = FileCoverage(filepath="test.ado")
        assert cov.coverage_percent == 100.0

    def test_lines_covered_and_missed(self):
        """Test lines covered and missed properties."""
        cov = FileCoverage(
            filepath="test.ado",
            lines_hit={1, 2, 5},
            lines_total={1, 2, 3, 4, 5},
        )
        assert cov.lines_covered == 3
        assert cov.lines_missed == 2


class TestCoverageReport:
    """Tests for CoverageReport dataclass."""

    def test_add_hit(self):
        """Test adding coverage hits."""
        report = CoverageReport()
        report.add_hit("test.ado", 1)
        report.add_hit("test.ado", 2)
        report.add_hit("other.ado", 5)

        assert "test.ado" in report.files
        assert 1 in report.files["test.ado"].lines_hit
        assert 2 in report.files["test.ado"].lines_hit
        assert 5 in report.files["other.ado"].lines_hit

    def test_set_total_lines(self):
        """Test setting total lines for a file."""
        report = CoverageReport()
        report.set_total_lines("test.ado", {1, 2, 3, 4, 5})

        assert report.files["test.ado"].lines_total == {1, 2, 3, 4, 5}

    def test_overall_coverage(self):
        """Test overall coverage calculation."""
        report = CoverageReport()
        report.add_hit("test.ado", 1)
        report.add_hit("test.ado", 2)
        report.set_total_lines("test.ado", {1, 2, 3, 4})

        assert report.total_lines == 4
        assert report.covered_lines == 2
        assert report.coverage_percent == 50.0


class TestParseSMCLLog:
    """Tests for parse_smcl_log function."""

    def test_parse_single_marker(self):
        """Test parsing a single coverage marker."""
        smcl = """
{smcl}
{txt}
{* COV:test.ado:5 }
{res}some output
"""
        hits = parse_smcl_log(smcl)

        assert "test.ado" in hits
        assert 5 in hits["test.ado"]

    def test_parse_multiple_markers(self):
        """Test parsing multiple coverage markers."""
        smcl = """
{* COV:test.ado:1 }
{* COV:test.ado:2 }
{* COV:other.ado:10 }
"""
        hits = parse_smcl_log(smcl)

        assert hits["test.ado"] == {1, 2}
        assert hits["other.ado"] == {10}

    def test_parse_no_markers(self):
        """Test parsing content without markers."""
        smcl = """
{smcl}
just regular output
"""
        hits = parse_smcl_log(smcl)

        assert hits == {}


class TestAggregateCoverage:
    """Tests for aggregate_coverage function."""

    def test_aggregate_single_result(self):
        """Test aggregating coverage from a single result."""
        results = [
            TestResult(
                test_file="test.do",
                passed=True,
                duration=1.0,
                coverage_hits={"test.ado": {1, 2, 3}},
            ),
        ]

        report = aggregate_coverage(results)

        assert "test.ado" in report.files
        assert report.files["test.ado"].lines_hit == {1, 2, 3}

    def test_aggregate_multiple_results(self):
        """Test aggregating coverage from multiple results."""
        results = [
            TestResult(
                test_file="test1.do",
                passed=True,
                duration=1.0,
                coverage_hits={"test.ado": {1, 2}},
            ),
            TestResult(
                test_file="test2.do",
                passed=True,
                duration=1.0,
                coverage_hits={"test.ado": {2, 3, 4}},
            ),
        ]

        report = aggregate_coverage(results)

        # Union of all hits
        assert report.files["test.ado"].lines_hit == {1, 2, 3, 4}


class TestGenerateLCOV:
    """Tests for generate_lcov function."""

    def test_generate_lcov_format(self):
        """Test LCOV output format."""
        results = [
            TestResult(
                test_file="test.do",
                passed=True,
                duration=1.0,
                coverage_hits={"test.ado": {1, 2, 5}},
            ),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "coverage.lcov"
            generate_lcov(results, output_path)

            content = output_path.read_text()

            assert "TN:statatest" in content
            assert "SF:test.ado" in content
            assert "DA:1,1" in content
            assert "DA:2,1" in content
            assert "DA:5,1" in content
            assert "end_of_record" in content


class TestGenerateHTML:
    """Tests for generate_html function."""

    def test_generate_html_creates_index(self):
        """Test HTML report generation."""
        results = [
            TestResult(
                test_file="test.do",
                passed=True,
                duration=1.0,
                coverage_hits={"test.ado": {1, 2, 3}},
            ),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "htmlcov"
            generate_html(results, output_dir)

            index_path = output_dir / "index.html"
            assert index_path.exists()

            content = index_path.read_text()
            assert "statatest Coverage Report" in content
            assert "test.ado" in content
