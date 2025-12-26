"""Coverage collection and report generation for statatest."""

from __future__ import annotations

from pathlib import Path

from statatest.models import TestResult
from statatest.report import generate_lcov as _generate_lcov


def generate_lcov(results: list[TestResult], output_path: Path) -> None:
    """Generate LCOV coverage report.

    Wrapper around report.generate_lcov for API consistency.
    """
    _generate_lcov(results, output_path)


def generate_html(results: list[TestResult], output_dir: Path) -> None:
    """Generate HTML coverage report.

    Wrapper around report.generate_html for API consistency.
    """
    from statatest.report import generate_html as _generate_html
    _generate_html(results, output_dir)
