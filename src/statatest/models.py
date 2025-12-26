"""Data models for statatest."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestFile:
    """Represents a test file to be executed."""

    path: Path
    markers: list[str] = field(default_factory=list)
    programs: list[str] = field(default_factory=list)

    @property
    def name(self) -> str:
        """Return the file name without extension."""
        return self.path.stem

    @property
    def relative_path(self) -> str:
        """Return path relative to current working directory."""
        try:
            return str(self.path.relative_to(Path.cwd()))
        except ValueError:
            return str(self.path)


@dataclass
class TestResult:
    """Result of running a single test file."""

    test_file: str
    passed: bool
    duration: float
    rc: int = 0
    stdout: str = ""
    stderr: str = ""
    error_message: str = ""
    assertions_passed: int = 0
    assertions_failed: int = 0
    coverage_hits: dict[str, set[int]] = field(default_factory=dict)


@dataclass
class CoverageData:
    """Coverage data for a source file."""

    file_path: str
    lines_hit: set[int] = field(default_factory=set)
    lines_total: set[int] = field(default_factory=set)

    @property
    def coverage_percent(self) -> float:
        """Calculate coverage percentage."""
        if not self.lines_total:
            return 100.0
        return len(self.lines_hit) / len(self.lines_total) * 100


@dataclass
class TestSuite:
    """Collection of test results for a suite."""

    name: str
    tests: list[TestResult] = field(default_factory=list)

    @property
    def total(self) -> int:
        """Total number of tests."""
        return len(self.tests)

    @property
    def passed(self) -> int:
        """Number of passed tests."""
        return sum(1 for t in self.tests if t.passed)

    @property
    def failed(self) -> int:
        """Number of failed tests."""
        return sum(1 for t in self.tests if not t.passed)

    @property
    def total_time(self) -> float:
        """Total execution time."""
        return sum(t.duration for t in self.tests)
