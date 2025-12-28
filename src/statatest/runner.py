"""Test runner for statatest - executes Stata tests via subprocess.

Architecture follows I/O separation principle:
- _prepare_test_environment(): I/O (file creation)
- _execute_stata(): I/O (subprocess call)
- _parse_test_output(): Computation (result parsing)
"""

from __future__ import annotations

import contextlib
import importlib.resources
import re
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console

from statatest.config import Config
from statatest.constants import ERROR_MESSAGE_MAX_LENGTH
from statatest.models import TestFile, TestResult

console = Console()

# =============================================================================
# Regex Patterns (compiled once at module load)
# =============================================================================

# Pattern to extract coverage markers from SMCL logs
# Format: {* COV:filename:lineno }
COVERAGE_PATTERN = re.compile(r"\{\*\s*COV:([^:]+):(\d+)\s*\}")

# Pattern to extract test markers from output
PASS_PATTERN = re.compile(r"_STATATEST_PASS_:(\w+)_")
FAIL_PATTERN = re.compile(r"_STATATEST_FAIL_:(\w+)_:(.+?)_END_")

# Stata error patterns for message extraction
ERROR_PATTERNS = [
    re.compile(r"r\((\d+)\);"),  # Stata return codes
    re.compile(r"assertion is false", re.IGNORECASE),  # Assert failures
    re.compile(r"^error:?\s*(.+)$", re.MULTILINE | re.IGNORECASE),  # Generic errors
]


# =============================================================================
# Data Classes for Internal State
# =============================================================================


@dataclass
class TestEnvironment:
    """Temporary files created for test execution."""

    wrapper_path: Path
    log_path: Path


@dataclass
class StataOutput:
    """Raw output from Stata subprocess."""

    returncode: int
    log_content: str
    stderr: str
    duration: float


# =============================================================================
# Path Discovery
# =============================================================================


def _get_ado_paths() -> dict[str, Path]:
    """Get paths to Stata .ado directories (assertions and fixtures).

    Uses importlib.resources to find package data, which works for both
    development installs (editable) and installed packages.

    Returns:
        Dictionary with 'assertions' and 'fixtures' paths
    """
    paths: dict[str, Path] = {}

    # Use importlib.resources to find the package's ado files
    try:
        files = importlib.resources.files("statatest")
        ado_base = Path(str(files.joinpath("ado")))
        if ado_base.exists():
            for subdir in ["assertions", "fixtures"]:
                subpath = ado_base / subdir
                if subpath.exists():
                    paths[subdir] = subpath
            if paths:
                return paths
    except (TypeError, AttributeError):
        pass

    # Fallback: look relative to this module (works in development)
    module_dir = Path(__file__).parent
    ado_base = module_dir / "ado"
    if ado_base.exists():
        for subdir in ["assertions", "fixtures"]:
            subpath = ado_base / subdir
            if subpath.exists():
                paths[subdir] = subpath

    return paths


def run_tests(
    tests: list[TestFile],
    config: Config,
    coverage: bool = False,
    verbose: bool = False,
    instrumented_dir: Path | None = None,
) -> list[TestResult]:
    """Run all discovered tests.

    Args:
        tests: List of test files to execute.
        config: Configuration object.
        coverage: Whether to collect coverage data.
        verbose: Whether to show verbose output.
        instrumented_dir: Path to instrumented source files (for coverage).

    Returns:
        List of TestResult objects.
    """
    results: list[TestResult] = []

    for test in tests:
        if verbose:
            console.print(f"Running: {test.relative_path}", end=" ")

        result = _run_single_test(test, config, coverage, instrumented_dir)
        results.append(result)

        if verbose:
            if result.passed:
                console.print("[green]PASSED[/green]", end="")
            else:
                console.print("[red]FAILED[/red]", end="")
            console.print(f" ({result.duration:.2f}s)")
        # Compact output
        elif result.passed:
            console.print("[green].[/green]", end="")
        else:
            console.print("[red]F[/red]", end="")

    if not verbose:
        console.print()  # Newline after dots

    return results


def _run_single_test(
    test: TestFile,
    config: Config,
    coverage: bool = False,
    instrumented_dir: Path | None = None,
) -> TestResult:
    """Execute a single test file.

    This function orchestrates three phases:
    1. Prepare environment (I/O) - create wrapper files
    2. Execute Stata (I/O) - run subprocess
    3. Parse results (computation) - analyze output

    Args:
        test: TestFile to execute.
        config: Configuration object.
        coverage: Whether to collect coverage data.
        instrumented_dir: Path to instrumented source files (for coverage).

    Returns:
        TestResult with execution details.
    """
    # Phase 1: Prepare environment (I/O)
    env = _prepare_test_environment(test, config, coverage, instrumented_dir)

    try:
        # Phase 2: Execute Stata (I/O)
        output = _execute_stata(test, config, env, coverage)

        # Phase 3: Parse results (computation)
        return _parse_test_output(test, output, coverage)

    except subprocess.TimeoutExpired:
        return TestResult(
            test_file=test.relative_path,
            passed=False,
            duration=0.0,
            rc=-1,
            error_message=f"Test timed out after {config.timeout} seconds",
        )

    except FileNotFoundError:
        return TestResult(
            test_file=test.relative_path,
            passed=False,
            duration=0.0,
            rc=-1,
            error_message=f"Stata executable not found: {config.stata_executable}",
        )

    finally:
        # Clean up temporary files
        _cleanup_environment(env)


def _prepare_test_environment(
    test: TestFile,
    config: Config,
    coverage: bool,
    instrumented_dir: Path | None,
) -> TestEnvironment:
    """Prepare temporary files for test execution (I/O phase).

    Args:
        test: TestFile to execute.
        config: Configuration object with adopath settings.
        coverage: Whether coverage collection is enabled.
        instrumented_dir: Path to instrumented source files.

    Returns:
        TestEnvironment with paths to temporary files.
    """
    # Get paths to .ado files based on adopath_mode
    ado_paths = _get_ado_paths_for_mode(config)

    # Find conftest.do files in directory hierarchy
    from statatest.fixtures import discover_conftest

    conftest_files = discover_conftest(test.path.parent)

    # Create wrapper .do file
    wrapper_content = _create_wrapper_do(
        test_path=test.path,
        ado_paths=ado_paths,
        conftest_files=conftest_files,
        instrumented_dir=instrumented_dir,
        setup_do=config.setup_do,
    )

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".do", delete=False
    ) as wrapper_file:
        wrapper_file.write(wrapper_content)
        wrapper_path = Path(wrapper_file.name)

    # Create log file
    log_suffix = ".smcl" if coverage else ".log"
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=log_suffix, delete=False
    ) as log_file:
        log_path = Path(log_file.name)

    return TestEnvironment(wrapper_path=wrapper_path, log_path=log_path)


def _get_ado_paths_for_mode(config: Config) -> dict[str, Path]:
    """Get ado paths based on configuration mode.

    Args:
        config: Configuration with adopath_mode and adopath settings.

    Returns:
        Dictionary of ado paths to add. Empty dict if user manages paths.
    """
    if config.adopath_mode == "none":
        # User manages adopath - don't inject anything
        return {}

    if config.adopath_mode == "custom":
        # Only use paths from config, not statatest internal paths
        return {f"custom_{i}": Path(p) for i, p in enumerate(config.adopath)}

    # Default "auto" mode: add statatest paths + any custom paths
    paths = _get_ado_paths()

    # Add any user-specified custom paths
    for i, custom_path in enumerate(config.adopath):
        paths[f"custom_{i}"] = Path(custom_path)

    return paths


def _execute_stata(
    test: TestFile,
    config: Config,
    env: TestEnvironment,
    coverage: bool,
) -> StataOutput:
    """Execute Stata subprocess (I/O phase).

    Args:
        test: TestFile being executed.
        config: Configuration object.
        env: Test environment with temporary file paths.
        coverage: Whether coverage collection is enabled.

    Returns:
        StataOutput with raw subprocess results.

    Raises:
        subprocess.TimeoutExpired: If test exceeds timeout.
        FileNotFoundError: If Stata executable not found.
    """
    start_time = time.time()

    # Use -s for SMCL log (coverage), -b for plain text log
    log_flag = "-s" if coverage else "-b"

    cmd = [
        config.stata_executable,
        log_flag,
        "-q",  # Quiet mode (suppress logo)
        "do",
        str(env.wrapper_path),
    ]

    process = subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
        timeout=config.timeout,
        cwd=test.path.parent,
    )

    duration = time.time() - start_time

    # Read log file
    try:
        log_content = env.log_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        log_content = ""

    return StataOutput(
        returncode=process.returncode,
        log_content=log_content,
        stderr=process.stderr,
        duration=duration,
    )


def _parse_test_output(
    test: TestFile,
    output: StataOutput,
    coverage: bool,
) -> TestResult:
    """Parse Stata output into TestResult (computation phase).

    This is a pure function with no I/O - only string parsing.

    Args:
        test: TestFile that was executed.
        output: Raw output from Stata subprocess.
        coverage: Whether to parse coverage markers.

    Returns:
        TestResult with parsed execution details.
    """
    # Check return code
    passed = output.returncode == 0

    # Count assertion markers
    assertions_passed = len(PASS_PATTERN.findall(output.log_content))
    assertions_failed = len(FAIL_PATTERN.findall(output.log_content))

    if assertions_failed > 0:
        passed = False

    # Extract error message if failed
    error_message = ""
    if not passed:
        error_message = _extract_error_message(output.log_content, output.stderr)

    # Parse coverage markers
    coverage_hits: dict[str, set[int]] = {}
    if coverage:
        coverage_hits = _parse_coverage_markers(output.log_content)

    return TestResult(
        test_file=test.relative_path,
        passed=passed,
        duration=output.duration,
        rc=output.returncode,
        stdout=output.log_content,
        stderr=output.stderr,
        error_message=error_message,
        assertions_passed=assertions_passed,
        assertions_failed=assertions_failed,
        coverage_hits=coverage_hits,
    )


def _cleanup_environment(env: TestEnvironment) -> None:
    """Clean up temporary files (I/O phase).

    Args:
        env: Test environment with paths to clean up.
    """
    for path in [env.log_path, env.wrapper_path]:
        with contextlib.suppress(FileNotFoundError):
            path.unlink()


def _create_wrapper_do(
    test_path: Path,
    ado_paths: dict[str, Path],
    conftest_files: list[Path],
    instrumented_dir: Path | None = None,
    setup_do: str | None = None,
) -> str:
    """Create a wrapper .do file that sets up the environment and runs the test.

    The wrapper executes in this order:
    1. Clear and set Stata options
    2. Add instrumented directory (for coverage) - highest priority
    3. Add ado paths (if adopath_mode is not "none")
    4. Run setup_do (if configured)
    5. Load conftest.do files (fixtures and shared setup)
    6. Run the actual test

    Args:
        test_path: Path to the test file.
        ado_paths: Dictionary of ado paths to add. May be empty if user manages paths.
        conftest_files: List of conftest.do files to load (in order).
        instrumented_dir: Path to instrumented source files (for coverage).
        setup_do: Optional path to a setup.do file for custom initialization.

    Returns:
        Contents of the wrapper .do file.
    """
    lines = [
        "// Auto-generated wrapper by statatest",
        "// Test environment setup and execution",
        "",
        "clear all",
        "set more off",
        "",
    ]

    # Add instrumented directory FIRST (highest priority for coverage)
    if instrumented_dir:
        lines.append("// Instrumented source files for coverage (highest priority)")
        lines.append(f'adopath + "{instrumented_dir}"')
        lines.append("")

    # Add ado paths (may be empty if adopath_mode is "none")
    if ado_paths:
        lines.append("// Additional ado paths")
        for name, path in ado_paths.items():
            # Skip internal naming, just add the path with a clean comment
            comment = name.replace("_", " ").replace("custom ", "user: ")
            lines.append(f"// {comment}")
            lines.append(f'adopath + "{path}"')
        lines.append("")

    # Run user's setup.do if configured (before conftest)
    if setup_do:
        lines.append("// User-defined setup script")
        lines.append(f'do "{setup_do}"')
        lines.append("")

    # Load conftest.do files (root first, then closer to test)
    if conftest_files:
        lines.append("// Conftest files (fixtures and shared setup)")
        lines.extend(f'do "{conftest}"' for conftest in conftest_files)
        lines.append("")

    # Run the actual test
    lines.extend(
        [
            "// Execute test",
            f'do "{test_path}"',
            "",
        ]
    )

    return "\n".join(lines)


def _extract_error_message(log_content: str, stderr: str) -> str:
    """Extract error message from Stata output (computation).

    This is a pure function - only string processing, no I/O.

    Args:
        log_content: Stata log file content.
        stderr: Standard error output.

    Returns:
        Human-readable error message.
    """
    # Try each error pattern
    for pattern in ERROR_PATTERNS:
        match = pattern.search(log_content)
        if match:
            return match.group(0)

    # Fall back to stderr (truncated)
    if stderr.strip():
        return stderr.strip()[:ERROR_MESSAGE_MAX_LENGTH]

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
