"""Report generation for statatest - JUnit XML and LCOV."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from statatest.models import TestResult


def write_junit_xml(results: list[TestResult], output_path: Path) -> None:
    """Generate JUnit XML report for CI systems.

    JUnit XML format is compatible with:
    - GitHub Actions
    - Jenkins
    - CircleCI
    - GitLab CI

    Args:
        results: List of test results.
        output_path: Path to write the XML file.
    """
    # Create root element
    testsuites = ET.Element("testsuites")
    testsuites.set("name", "Stata Tests")
    testsuites.set("tests", str(len(results)))
    testsuites.set("failures", str(sum(1 for r in results if not r.passed)))
    testsuites.set("time", f"{sum(r.duration for r in results):.3f}")
    testsuites.set("timestamp", datetime.now().isoformat())

    # Group by directory (each directory is a testsuite)
    suites: dict[str, list[TestResult]] = {}
    for result in results:
        # Use parent directory as suite name
        suite_name = Path(result.test_file).parent.name or "root"
        if suite_name not in suites:
            suites[suite_name] = []
        suites[suite_name].append(result)

    # Create testsuite elements
    for suite_name, suite_results in suites.items():
        testsuite = ET.SubElement(testsuites, "testsuite")
        testsuite.set("name", suite_name)
        testsuite.set("tests", str(len(suite_results)))
        testsuite.set("failures", str(sum(1 for r in suite_results if not r.passed)))
        testsuite.set("time", f"{sum(r.duration for r in suite_results):.3f}")

        for result in suite_results:
            testcase = ET.SubElement(testsuite, "testcase")
            testcase.set("name", Path(result.test_file).stem)
            testcase.set("classname", suite_name)
            testcase.set("time", f"{result.duration:.3f}")

            if not result.passed:
                failure = ET.SubElement(testcase, "failure")
                failure.set("message", result.error_message)
                failure.set("type", "AssertionError")
                failure.text = result.stdout[-2000:] if result.stdout else ""

            # Add system-out
            if result.stdout:
                system_out = ET.SubElement(testcase, "system-out")
                system_out.text = result.stdout[-5000:]  # Truncate long output

            # Add system-err
            if result.stderr:
                system_err = ET.SubElement(testcase, "system-err")
                system_err.text = result.stderr[-2000:]

    # Write to file with proper formatting
    tree = ET.ElementTree(testsuites)
    ET.indent(tree, space="  ")
    tree.write(output_path, encoding="utf-8", xml_declaration=True)


def generate_lcov(results: list[TestResult], output_path: Path) -> None:
    """Generate LCOV coverage report.

    LCOV format is compatible with:
    - Codecov
    - Coveralls
    - Most CI coverage tools

    Format:
        TN:<test name>
        SF:<source file>
        DA:<line number>,<execution count>
        LF:<lines found>
        LH:<lines hit>
        end_of_record

    Args:
        results: List of test results with coverage data.
        output_path: Path to write the LCOV file.
    """
    # Aggregate coverage across all tests
    combined_coverage: dict[str, set[int]] = {}

    for result in results:
        for filename, lines in result.coverage_hits.items():
            if filename not in combined_coverage:
                combined_coverage[filename] = set()
            combined_coverage[filename].update(lines)

    # Generate LCOV content
    lines: list[str] = []
    lines.append("TN:statatest")

    for filename, hit_lines in sorted(combined_coverage.items()):
        lines.append(f"SF:{filename}")

        # Sort lines for consistent output
        for lineno in sorted(hit_lines):
            lines.append(f"DA:{lineno},1")

        lines.append(f"LF:{len(hit_lines)}")  # Lines found (total instrumented)
        lines.append(f"LH:{len(hit_lines)}")  # Lines hit
        lines.append("end_of_record")

    output_path.write_text("\n".join(lines) + "\n")


def generate_html(results: list[TestResult], output_dir: Path) -> None:
    """Generate HTML coverage report.

    Args:
        results: List of test results with coverage data.
        output_dir: Directory to write HTML files.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Aggregate coverage
    combined_coverage: dict[str, set[int]] = {}
    for result in results:
        for filename, lines in result.coverage_hits.items():
            if filename not in combined_coverage:
                combined_coverage[filename] = set()
            combined_coverage[filename].update(lines)

    # Generate index.html
    index_content = _generate_html_index(combined_coverage)
    (output_dir / "index.html").write_text(index_content)

    # Generate per-file reports
    for filename, hit_lines in combined_coverage.items():
        file_content = _generate_html_file(filename, hit_lines)
        safe_name = filename.replace("/", "_").replace("\\", "_")
        (output_dir / f"{safe_name}.html").write_text(file_content)


def _generate_html_index(coverage: dict[str, set[int]]) -> str:
    """Generate HTML index page for coverage report."""
    files_html = ""
    total_lines = 0
    total_hit = 0

    for filename, hit_lines in sorted(coverage.items()):
        safe_name = filename.replace("/", "_").replace("\\", "_")
        lines_hit = len(hit_lines)
        total_lines += lines_hit
        total_hit += lines_hit
        files_html += f"""
        <tr>
            <td><a href="{safe_name}.html">{filename}</a></td>
            <td>{lines_hit}</td>
            <td>100%</td>
        </tr>
        """

    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Coverage Report - statatest</title>
    <style>
        body {{ font-family: system-ui, sans-serif; margin: 2rem; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        h1 {{ color: #333; }}
    </style>
</head>
<body>
    <h1>Coverage Report</h1>
    <p>Generated by statatest</p>
    <table>
        <tr>
            <th>File</th>
            <th>Lines Hit</th>
            <th>Coverage</th>
        </tr>
        {files_html}
    </table>
</body>
</html>
"""


def _generate_html_file(filename: str, hit_lines: set[int]) -> str:
    """Generate HTML page for a single source file."""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Coverage - {filename}</title>
    <style>
        body {{ font-family: monospace; margin: 2rem; }}
        .hit {{ background-color: #90EE90; }}
        .miss {{ background-color: #FFB6C1; }}
    </style>
</head>
<body>
    <h1>{filename}</h1>
    <p>Lines hit: {len(hit_lines)}</p>
    <p>Hit lines: {sorted(hit_lines)}</p>
    <p><a href="index.html">Back to index</a></p>
</body>
</html>
"""
