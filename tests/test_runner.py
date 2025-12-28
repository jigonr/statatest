"""Tests for runner module."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from statatest.core.config import Config
from statatest.core.models import TestFile
from statatest.execution import run_tests
from statatest.execution.executor import _get_ado_paths
from statatest.execution.parser import (
    extract_error_message as _extract_error_message,
    parse_coverage_markers as _parse_coverage_markers,
)
from statatest.execution.wrapper import create_wrapper_do as _create_wrapper_do


class TestGetAdoPaths:
    """Tests for _get_ado_paths function."""

    def test_returns_dict_with_paths(self):
        """Test that ado paths are returned."""
        paths = _get_ado_paths()

        # Should return a dict (may be empty if paths don't exist)
        assert isinstance(paths, dict)

    def test_paths_exist_when_returned(self):
        """Test that returned paths actually exist."""
        paths = _get_ado_paths()

        for name, path in paths.items():
            assert path.exists(), f"Path {name} does not exist: {path}"


class TestCreateWrapperDo:
    """Tests for _create_wrapper_do function."""

    def test_creates_basic_wrapper(self):
        """Test basic wrapper creation."""
        test_path = Path("/project/tests/test_example.do")
        ado_paths = {}
        conftest_files = []

        wrapper = _create_wrapper_do(test_path, ado_paths, conftest_files)

        assert "// Auto-generated wrapper by statatest" in wrapper
        assert "clear all" in wrapper
        assert "set more off" in wrapper
        assert 'do "/project/tests/test_example.do"' in wrapper

    def test_includes_ado_paths(self):
        """Test that ado paths are added to adopath."""
        test_path = Path("/project/tests/test_example.do")
        ado_paths = {"assertions": Path("/pkg/ado/assertions")}
        conftest_files = []

        wrapper = _create_wrapper_do(test_path, ado_paths, conftest_files)

        assert 'adopath + "/pkg/ado/assertions"' in wrapper
        assert "// Additional ado paths" in wrapper

    def test_includes_conftest_files(self):
        """Test that conftest.do files are loaded."""
        test_path = Path("/project/tests/test_example.do")
        ado_paths = {}
        conftest_files = [
            Path("/project/conftest.do"),
            Path("/project/tests/conftest.do"),
        ]

        wrapper = _create_wrapper_do(test_path, ado_paths, conftest_files)

        assert 'do "/project/conftest.do"' in wrapper
        assert 'do "/project/tests/conftest.do"' in wrapper

    def test_includes_instrumented_dir(self):
        """Test that instrumented directory is added first (highest priority)."""
        test_path = Path("/project/tests/test_example.do")
        ado_paths = {"assertions": Path("/pkg/ado/assertions")}
        conftest_files = []
        instrumented_dir = Path("/project/.statatest/instrumented")

        wrapper = _create_wrapper_do(
            test_path, ado_paths, conftest_files, instrumented_dir
        )

        # Instrumented dir should be added first with coverage comment
        assert "// Instrumented source files for coverage" in wrapper
        assert 'adopath + "/project/.statatest/instrumented"' in wrapper

        # And should appear before other ado paths
        instr_pos = wrapper.find("instrumented")
        assertions_pos = wrapper.find("assertions")
        assert instr_pos < assertions_pos


class TestParseCoverageMarkers:
    """Tests for _parse_coverage_markers function."""

    def test_parses_single_marker(self):
        """Test parsing a single coverage marker."""
        smcl = "some output {* COV:myfile.ado:10 } more output"

        hits = _parse_coverage_markers(smcl)

        assert "myfile.ado" in hits
        assert 10 in hits["myfile.ado"]

    def test_parses_multiple_markers_same_file(self):
        """Test parsing multiple markers for same file."""
        smcl = "{* COV:file.ado:1 } {* COV:file.ado:5 } {* COV:file.ado:10 }"

        hits = _parse_coverage_markers(smcl)

        assert hits["file.ado"] == {1, 5, 10}

    def test_parses_multiple_files(self):
        """Test parsing markers for multiple files."""
        smcl = "{* COV:a.ado:1 } {* COV:b.ado:2 } {* COV:a.ado:3 }"

        hits = _parse_coverage_markers(smcl)

        assert hits["a.ado"] == {1, 3}
        assert hits["b.ado"] == {2}

    def test_returns_empty_when_no_markers(self):
        """Test that empty dict is returned when no markers found."""
        smcl = "regular stata output without markers"

        hits = _parse_coverage_markers(smcl)

        assert hits == {}


class TestExtractErrorMessage:
    """Tests for _extract_error_message function."""

    def test_extracts_return_code(self):
        """Test extraction of Stata return code errors."""
        log = "some command\nr(198);\nmore output"

        msg = _extract_error_message(log, "")

        assert "r(198)" in msg

    def test_extracts_assertion_failure(self):
        """Test extraction of assertion failure message."""
        log = "assert x == y\nassertion is false\n"

        msg = _extract_error_message(log, "")

        assert "assertion is false" in msg

    def test_uses_stderr_as_fallback(self):
        """Test that stderr is used when no error in log."""
        log = "clean log output"
        stderr = "error from stata"

        msg = _extract_error_message(log, stderr)

        assert "error from stata" in msg

    def test_returns_generic_message_when_no_error_found(self):
        """Test generic message when no specific error found."""
        log = "clean output"
        stderr = ""

        msg = _extract_error_message(log, stderr)

        assert "Test failed" in msg


class TestRunTests:
    """Tests for run_tests function."""

    @patch("statatest.execution.executor._run_single_test")
    def test_runs_all_tests(self, mock_run_single):
        """Test that all tests are executed."""
        config = Config()
        tests = [
            TestFile(path=Path("/t1.do")),
            TestFile(path=Path("/t2.do")),
        ]

        mock_result = MagicMock()
        mock_result.passed = True
        mock_result.duration = 0.1
        mock_run_single.return_value = mock_result

        results = run_tests(tests, config)

        assert len(results) == 2
        assert mock_run_single.call_count == 2

    @patch("statatest.execution.executor._run_single_test")
    def test_passes_coverage_flag(self, mock_run_single):
        """Test that coverage flag is passed to single test runner."""
        config = Config()
        tests = [TestFile(path=Path("/t.do"))]

        mock_result = MagicMock()
        mock_result.passed = True
        mock_result.duration = 0.1
        mock_run_single.return_value = mock_result

        run_tests(tests, config, coverage=True)

        # Check coverage was passed
        call_args = mock_run_single.call_args
        assert call_args[0][2] is True  # coverage arg

    @patch("statatest.execution.executor._run_single_test")
    def test_passes_instrumented_dir(self, mock_run_single):
        """Test that instrumented_dir is passed to single test runner."""
        config = Config()
        tests = [TestFile(path=Path("/t.do"))]
        instr_dir = Path("/project/.statatest/instrumented")

        mock_result = MagicMock()
        mock_result.passed = True
        mock_result.duration = 0.1
        mock_run_single.return_value = mock_result

        run_tests(tests, config, instrumented_dir=instr_dir)

        # Check instrumented_dir was passed
        call_args = mock_run_single.call_args
        assert call_args[0][3] == instr_dir  # instrumented_dir arg


class TestRunSingleTest:
    """Tests for _run_single_test function."""

    @patch("statatest.execution.executor.subprocess.run")
    @patch("statatest.execution.executor._get_ado_paths")
    @patch("statatest.fixtures.discover_conftest")
    def test_handles_timeout(self, mock_conftest, mock_ado, mock_subprocess):
        """Test handling of subprocess timeout."""
        import subprocess

        from statatest.execution.executor import _run_single_test

        mock_ado.return_value = {}
        mock_conftest.return_value = []
        mock_subprocess.side_effect = subprocess.TimeoutExpired(
            cmd="stata", timeout=300
        )

        config = Config()

        with tempfile.TemporaryDirectory() as tmpdir:
            test_path = Path(tmpdir) / "test.do"
            test_path.write_text("// test")
            test = TestFile(path=test_path)

            result = _run_single_test(test, config)

        assert result.passed is False
        assert "timed out" in result.error_message.lower()

    @patch("statatest.execution.executor.subprocess.run")
    @patch("statatest.execution.executor._get_ado_paths")
    @patch("statatest.fixtures.discover_conftest")
    def test_handles_file_not_found(self, mock_conftest, mock_ado, mock_subprocess):
        """Test handling when Stata executable is not found."""
        from statatest.execution.executor import _run_single_test

        mock_ado.return_value = {}
        mock_conftest.return_value = []
        mock_subprocess.side_effect = FileNotFoundError()

        config = Config()

        with tempfile.TemporaryDirectory() as tmpdir:
            test_path = Path(tmpdir) / "test.do"
            test_path.write_text("// test")
            test = TestFile(path=test_path)

            result = _run_single_test(test, config)

        assert result.passed is False
        assert "not found" in result.error_message.lower()
