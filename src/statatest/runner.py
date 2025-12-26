"""Test runner for statatest - executes Stata tests via subprocess."""

from __future__ import annotations

import re
import subprocess
import tempfile
import time
from pathlib import Path

from rich.console import Console

from statatest.config import Config
from statatest.models import TestFile, TestResult

console = Console()

# Pattern to extract coverage markers from SMCL logs
# Format: {* COV:filename:lineno }
COVERAGE_PATTERN = re.compile(r"\{\*\s*COV:([^:]+):(\d+)\s*\}")

# Pattern to extract test markers from output
PASS_PATTERN = re.compile(r"_STATATEST_PASS_:(\w+)_")
FAIL_PATTERN = re.compile(r"_STATATEST_FAIL_:(\w+)_:(.+?)_END_")


def run_tests(
    tests: list[TestFile],
    config: Config,
    coverage: bool = False,
    verbose: bool = False,
) -> list[TestResult]:
    """Run all discovered tests.

    Args:
        tests: List of test files to execute.
        config: Configuration object.
        coverage: Whether to collect coverage data.
        verbose: Whether to show verbose output.

    Returns:
        List of TestResult objects.
    """
    results: list[TestResult] = []

    for test in tests:
        if verbose:
            console.print(f"Running: {test.relative_path}", end=" ")

        result = _run_single_test(test, config, coverage)
        results.append(result)

        if verbose:
            if result.passed:
                console.print("[green]PASSED[/green]", end="")
            else:
                console.print("[red]FAILED[/red]", end="")
            console.print(f" ({result.duration:.2f}s)")
        else:
            # Compact output
            if result.passed:
                console.print("[green].[/green]", end="")
            else:
                console.print("[red]F[/red]", end="")

    if not verbose:
        console.print()  # Newline after dots

    return results


def _run_single_test(
    test: TestFile, config: Config, coverage: bool = False
) -> TestResult:
    """Execute a single test file.

    Args:
        test: TestFile to execute.
        config: Configuration object.
        coverage: Whether to collect coverage data.

    Returns:
        TestResult with execution details.
    """
    start_time = time.time()

    # Use SMCL log format for coverage marker parsing
    log_suffix = ".smcl" if coverage else ".log"

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=log_suffix, delete=False
    ) as log_file:
        log_path = Path(log_file.name)

    # Build Stata command
    # Use -s for SMCL log, -b for plain text log
    log_flag = "-s" if coverage else "-b"

    try:
        # Run Stata in batch mode
        cmd = [
            config.stata_executable,
            log_flag,
            "-q",  # Quiet mode (suppress logo)
            "do",
            str(test.path),
        ]

        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout per test
            cwd=test.path.parent,
        )

        duration = time.time() - start_time

        # Read log file
        try:
            log_content = log_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            log_content = ""

        # Parse results
        rc = process.returncode
        passed = rc == 0

        # Check for assertion failures in output
        assertions_passed = len(PASS_PATTERN.findall(log_content))
        assertions_failed = len(FAIL_PATTERN.findall(log_content))

        if assertions_failed > 0:
            passed = False

        # Extract error message
        error_message = ""
        if not passed:
            error_message = _extract_error_message(log_content, process.stderr)

        # Extract coverage data
        coverage_hits: dict[str, set[int]] = {}
        if coverage:
            coverage_hits = _parse_coverage_markers(log_content)

        return TestResult(
            test_file=test.relative_path,
            passed=passed,
            duration=duration,
            rc=rc,
            stdout=log_content,
            stderr=process.stderr,
            error_message=error_message,
            assertions_passed=assertions_passed,
            assertions_failed=assertions_failed,
            coverage_hits=coverage_hits,
        )

    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        return TestResult(
            test_file=test.relative_path,
            passed=False,
            duration=duration,
            rc=-1,
            error_message="Test timed out after 300 seconds",
        )

    except FileNotFoundError:
        duration = time.time() - start_time
        return TestResult(
            test_file=test.relative_path,
            passed=False,
            duration=duration,
            rc=-1,
            error_message=f"Stata executable not found: {config.stata_executable}",
        )

    finally:
        # Clean up log file
        try:
            log_path.unlink()
        except FileNotFoundError:
            pass


def _extract_error_message(log_content: str, stderr: str) -> str:
    """Extract error message from Stata output."""
    # Look for Stata error patterns
    error_patterns = [
        r"r\((\d+)\);",  # Stata return codes
        r"assertion is false",  # Assert failures
        r"^error:?\s*(.+)$",  # Generic error lines
    ]

    for pattern in error_patterns:
        match = re.search(pattern, log_content, re.MULTILINE | re.IGNORECASE)
        if match:
            if match.groups():
                return match.group(0)
            return match.group(0)

    # Check stderr
    if stderr.strip():
        return stderr.strip()[:200]

    # Generic failure message
    return "Test failed (check log for details)"


def _parse_coverage_markers(smcl_content: str) -> dict[str, set[int]]:
    """Extract coverage hits from SMCL log file.

    Coverage markers are invisible SMCL comments in the format:
        {* COV:filename.ado:lineno }

    Args:
        smcl_content: Raw SMCL log content.

    Returns:
        Dictionary mapping filenames to sets of line numbers hit.
    """
    hits: dict[str, set[int]] = {}

    for match in COVERAGE_PATTERN.finditer(smcl_content):
        filename, lineno = match.group(1), int(match.group(2))
        if filename not in hits:
            hits[filename] = set()
        hits[filename].add(lineno)

    return hits
