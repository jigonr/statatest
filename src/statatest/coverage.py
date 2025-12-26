"""Coverage collection and report generation for statatest.

This module handles:
1. Setting up instrumented source files
2. Collecting coverage from SMCL logs
3. Aggregating coverage across test runs
4. Generating reports (LCOV, HTML)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from statatest.models import TestResult

# Pattern to extract coverage markers from SMCL logs
# Format: {* COV:filename:lineno }
COVERAGE_PATTERN = re.compile(r"\{\*\s*COV:([^:]+):(\d+)\s*\}")


@dataclass
class FileCoverage:
    """Coverage data for a single source file."""

    filepath: str
    lines_hit: set[int] = field(default_factory=set)
    lines_total: set[int] = field(default_factory=set)

    @property
    def coverage_percent(self) -> float:
        """Calculate coverage percentage."""
        if not self.lines_total:
            return 100.0
        return len(self.lines_hit & self.lines_total) / len(self.lines_total) * 100

    @property
    def lines_covered(self) -> int:
        """Number of lines covered."""
        return len(self.lines_hit & self.lines_total)

    @property
    def lines_missed(self) -> int:
        """Number of lines not covered."""
        return len(self.lines_total - self.lines_hit)


@dataclass
class CoverageReport:
    """Aggregated coverage report across all files."""

    files: dict[str, FileCoverage] = field(default_factory=dict)

    def add_hit(self, filename: str, lineno: int) -> None:
        """Record a coverage hit."""
        if filename not in self.files:
            self.files[filename] = FileCoverage(filepath=filename)
        self.files[filename].lines_hit.add(lineno)

    def set_total_lines(self, filename: str, lines: set[int]) -> None:
        """Set the total instrumentable lines for a file."""
        if filename not in self.files:
            self.files[filename] = FileCoverage(filepath=filename)
        self.files[filename].lines_total = lines

    @property
    def total_lines(self) -> int:
        """Total number of instrumentable lines."""
        return sum(len(f.lines_total) for f in self.files.values())

    @property
    def covered_lines(self) -> int:
        """Total number of covered lines."""
        return sum(f.lines_covered for f in self.files.values())

    @property
    def coverage_percent(self) -> float:
        """Overall coverage percentage."""
        if self.total_lines == 0:
            return 100.0
        return self.covered_lines / self.total_lines * 100


def parse_smcl_log(smcl_content: str) -> dict[str, set[int]]:
    """Extract coverage hits from SMCL log content.

    Args:
        smcl_content: Raw SMCL log content

    Returns:
        Dictionary mapping filenames to sets of line numbers hit
    """
    hits: dict[str, set[int]] = {}

    for match in COVERAGE_PATTERN.finditer(smcl_content):
        filename, lineno = match.group(1), int(match.group(2))
        if filename not in hits:
            hits[filename] = set()
        hits[filename].add(lineno)

    return hits


def aggregate_coverage(results: list[TestResult]) -> CoverageReport:
    """Aggregate coverage data from multiple test results.

    Args:
        results: List of TestResult objects

    Returns:
        Aggregated CoverageReport
    """
    report = CoverageReport()

    for result in results:
        for filename, lines in result.coverage_hits.items():
            for lineno in lines:
                report.add_hit(filename, lineno)

    return report


def generate_lcov(results: list[TestResult], output_path: Path) -> None:
    """Generate LCOV coverage report.

    Args:
        results: List of TestResult objects with coverage data
        output_path: Path to write the LCOV file
    """
    # Aggregate coverage
    coverage = aggregate_coverage(results)

    lines: list[str] = []
    lines.append("TN:statatest")

    for filename, file_cov in sorted(coverage.files.items()):
        lines.append(f"SF:{filename}")

        # Write all hit lines
        for lineno in sorted(file_cov.lines_hit):
            lines.append(f"DA:{lineno},1")

        # Summary
        lines.append(f"LF:{len(file_cov.lines_total) or len(file_cov.lines_hit)}")
        lines.append(f"LH:{len(file_cov.lines_hit)}")
        lines.append("end_of_record")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def generate_html(results: list[TestResult], output_dir: Path) -> None:
    """Generate HTML coverage report.

    Args:
        results: List of TestResult objects with coverage data
        output_dir: Directory to write HTML files
    """
    # Aggregate coverage
    coverage = aggregate_coverage(results)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate index.html
    html_lines = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "<title>statatest Coverage Report</title>",
        "<style>",
        "body { font-family: sans-serif; margin: 20px; }",
        "table { border-collapse: collapse; width: 100%; }",
        "th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
        "th { background-color: #4CAF50; color: white; }",
        "tr:nth-child(even) { background-color: #f2f2f2; }",
        ".high { color: green; }",
        ".medium { color: orange; }",
        ".low { color: red; }",
        "</style>",
        "</head>",
        "<body>",
        f"<h1>statatest Coverage Report</h1>",
        f"<p>Overall coverage: <strong>{coverage.coverage_percent:.1f}%</strong></p>",
        "<table>",
        "<tr><th>File</th><th>Lines</th><th>Covered</th><th>Coverage</th></tr>",
    ]

    for filename, file_cov in sorted(coverage.files.items()):
        pct = file_cov.coverage_percent
        css_class = "high" if pct >= 80 else "medium" if pct >= 50 else "low"
        total = len(file_cov.lines_total) or len(file_cov.lines_hit)
        covered = len(file_cov.lines_hit)
        html_lines.append(
            f"<tr><td>{filename}</td><td>{total}</td><td>{covered}</td>"
            f"<td class='{css_class}'>{pct:.1f}%</td></tr>"
        )

    html_lines.extend([
        "</table>",
        "</body>",
        "</html>",
    ])

    index_path = output_dir / "index.html"
    index_path.write_text("\n".join(html_lines), encoding="utf-8")
