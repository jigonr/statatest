"""Coverage module - coverage collection, aggregation, and reporting.

This module provides coverage functionality:
- models: FileCoverage and CoverageReport data classes
- aggregator: Aggregate coverage from test results
- reporter: Generate LCOV and HTML reports
"""

from statatest.coverage.aggregator import aggregate_coverage
from statatest.coverage.models import CoverageReport, FileCoverage
from statatest.coverage.reporter import generate_html, generate_lcov

__all__ = [
    "CoverageReport",
    "FileCoverage",
    "aggregate_coverage",
    "generate_html",
    "generate_lcov",
]
