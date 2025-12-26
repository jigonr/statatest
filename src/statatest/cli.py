"""Command-line interface for statatest."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

import click
from rich.console import Console

from statatest import __version__
from statatest.config import Config, load_config
from statatest.discovery import discover_tests
from statatest.runner import run_tests
from statatest.report import write_junit_xml

if TYPE_CHECKING:
    from statatest.models import TestResult

console = Console()


@click.group(invoke_without_command=True)
@click.argument("path", type=click.Path(exists=True), required=False)
@click.option("--coverage", is_flag=True, help="Enable coverage collection")
@click.option("--cov-report", type=str, help="Coverage report format (lcov, html)")
@click.option("--junit-xml", type=click.Path(), help="Output JUnit XML to this path")
@click.option("-m", "--marker", type=str, help="Only run tests with this marker")
@click.option("-k", "--keyword", type=str, help="Only run tests matching keyword")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
@click.option("--version", is_flag=True, help="Show version and exit")
@click.option("--init", is_flag=True, help="Create statatest.toml template")
@click.pass_context
def main(
    ctx: click.Context,
    path: str | None,
    coverage: bool,
    cov_report: str | None,
    junit_xml: str | None,
    marker: str | None,
    keyword: str | None,
    verbose: bool,
    version: bool,
    init: bool,
) -> None:
    """statatest - Pytest-inspired testing framework for Stata.

    Run tests:
        statatest tests/

    Run with coverage:
        statatest tests/ --coverage --cov-report=lcov
    """
    if version:
        console.print(f"statatest version {__version__}")
        sys.exit(0)

    if init:
        _create_config_template()
        sys.exit(0)

    if ctx.invoked_subcommand is None and path is None:
        console.print("[yellow]Usage: statatest <path> [OPTIONS][/yellow]")
        console.print("Run 'statatest --help' for more information.")
        sys.exit(1)

    if path is None:
        return

    # Load configuration
    config = load_config(Path.cwd())
    if verbose:
        config.verbose = True

    # Discover tests
    test_path = Path(path)
    console.print(f"[bold blue]statatest[/bold blue] v{__version__}")
    console.print(f"Collecting tests from: {test_path}")

    tests = discover_tests(test_path, config, marker=marker, keyword=keyword)

    if not tests:
        console.print("[yellow]No tests found.[/yellow]")
        sys.exit(0)

    console.print(f"Found {len(tests)} test file(s)\n")

    # Run tests
    results = run_tests(tests, config, coverage=coverage, verbose=verbose)

    # Generate reports
    if junit_xml:
        write_junit_xml(results, Path(junit_xml))
        console.print(f"\nJUnit XML written to: {junit_xml}")

    if coverage and cov_report:
        _generate_coverage_report(results, cov_report, config)

    # Print summary
    _print_summary(results)

    # Exit with appropriate code
    failed = sum(1 for r in results if not r.passed)
    sys.exit(1 if failed > 0 else 0)


def _create_config_template() -> None:
    """Create a statatest.toml template in the current directory."""
    template = '''[tool.statatest]
testpaths = ["tests"]
test_files = ["test_*.do"]
stata_executable = "stata-mp"

[tool.statatest.coverage]
source = ["code/functions"]
omit = ["tests/*"]

[tool.statatest.reporting]
junit_xml = "junit.xml"
lcov = "coverage.lcov"
'''
    config_path = Path.cwd() / "statatest.toml"
    if config_path.exists():
        console.print("[yellow]statatest.toml already exists.[/yellow]")
        return

    config_path.write_text(template)
    console.print(f"[green]Created statatest.toml[/green]")


def _generate_coverage_report(
    results: list[TestResult], report_format: str, config: Config
) -> None:
    """Generate coverage report in the specified format."""
    from statatest.coverage import generate_lcov, generate_html

    match report_format.lower():
        case "lcov":
            lcov_path = Path(config.reporting.get("lcov", "coverage.lcov"))
            generate_lcov(results, lcov_path)
            console.print(f"LCOV coverage written to: {lcov_path}")
        case "html":
            html_dir = Path(config.reporting.get("htmlcov", "htmlcov"))
            generate_html(results, html_dir)
            console.print(f"HTML coverage written to: {html_dir}")
        case _:
            console.print(f"[yellow]Unknown coverage format: {report_format}[/yellow]")


def _print_summary(results: list[TestResult]) -> None:
    """Print test results summary."""
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    total = len(results)
    total_time = sum(r.duration for r in results)

    console.print()
    console.print("=" * 60)

    if failed == 0:
        console.print(
            f"[bold green]{passed} passed[/bold green] in {total_time:.2f}s"
        )
    else:
        console.print(
            f"[bold red]{failed} failed[/bold red], "
            f"[green]{passed} passed[/green] in {total_time:.2f}s"
        )

        # Show failed tests
        console.print("\n[bold red]FAILURES:[/bold red]")
        for result in results:
            if not result.passed:
                console.print(f"  - {result.test_file}: {result.error_message}")


if __name__ == "__main__":
    main()
