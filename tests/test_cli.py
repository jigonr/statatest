"""Tests for CLI module."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from statatest import __version__
from statatest.cli import main


class TestCLIVersion:
    """Tests for --version flag."""

    def test_version_flag(self):
        """Test --version shows version and exits."""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])

        assert result.exit_code == 0
        assert f"statatest version {__version__}" in result.output


class TestCLIInit:
    """Tests for --init flag."""

    def test_init_creates_config(self):
        """Test --init creates statatest.toml template."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(main, ["--init"])

            assert result.exit_code == 0
            assert "Created statatest.toml" in result.output
            assert Path("statatest.toml").exists()

            # Verify content
            content = Path("statatest.toml").read_text()
            assert "[tool.statatest]" in content
            assert 'testpaths = ["tests"]' in content

    def test_init_skips_if_exists(self):
        """Test --init skips if statatest.toml already exists."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Create existing file
            Path("statatest.toml").write_text("existing content")

            result = runner.invoke(main, ["--init"])

            assert result.exit_code == 0
            assert "already exists" in result.output

            # Content should be unchanged
            assert Path("statatest.toml").read_text() == "existing content"


class TestCLINoPath:
    """Tests for CLI without path argument."""

    def test_no_path_shows_usage(self):
        """Test that no path shows usage message."""
        runner = CliRunner()
        result = runner.invoke(main, [])

        assert result.exit_code == 1
        assert "Usage: statatest <path>" in result.output


class TestCLINoTestsFound:
    """Tests for CLI when no tests are found."""

    def test_no_tests_found(self):
        """Test that empty directory shows no tests message."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Create empty tests directory
            Path("tests").mkdir()

            result = runner.invoke(main, ["tests"])

            assert result.exit_code == 0
            assert "No tests found" in result.output


class TestCLITestExecution:
    """Tests for CLI test execution."""

    @patch("statatest.cli.run_tests")
    @patch("statatest.cli.discover_tests")
    def test_runs_discovered_tests(self, mock_discover, mock_run):
        """Test that discovered tests are executed."""
        runner = CliRunner()

        # Mock test discovery
        mock_test = MagicMock()
        mock_test.relative_path = "test_example.do"
        mock_discover.return_value = [mock_test]

        # Mock test results
        mock_result = MagicMock()
        mock_result.passed = True
        mock_result.duration = 0.1
        mock_run.return_value = [mock_result]

        with runner.isolated_filesystem():
            Path("tests").mkdir()
            Path("tests/test_example.do").write_text("// test")

            result = runner.invoke(main, ["tests"])

            assert result.exit_code == 0
            mock_discover.assert_called_once()
            mock_run.assert_called_once()

    @patch("statatest.cli.run_tests")
    @patch("statatest.cli.discover_tests")
    def test_exits_with_failure_code(self, mock_discover, mock_run):
        """Test that failed tests result in exit code 1."""
        runner = CliRunner()

        mock_test = MagicMock()
        mock_test.relative_path = "test_example.do"
        mock_discover.return_value = [mock_test]

        # Mock failed test result
        mock_result = MagicMock()
        mock_result.passed = False
        mock_result.duration = 0.1
        mock_result.error_message = "assertion failed"
        mock_run.return_value = [mock_result]

        with runner.isolated_filesystem():
            Path("tests").mkdir()
            Path("tests/test_example.do").write_text("// test")

            result = runner.invoke(main, ["tests"])

            assert result.exit_code == 1


class TestCLIJUnitXML:
    """Tests for --junit-xml option."""

    @patch("statatest.cli.run_tests")
    @patch("statatest.cli.discover_tests")
    @patch("statatest.cli.write_junit_xml")
    def test_generates_junit_xml(self, mock_write_xml, mock_discover, mock_run):
        """Test that --junit-xml generates JUnit XML report."""
        runner = CliRunner()

        mock_test = MagicMock()
        mock_test.relative_path = "test_example.do"
        mock_discover.return_value = [mock_test]

        mock_result = MagicMock()
        mock_result.passed = True
        mock_result.duration = 0.1
        mock_run.return_value = [mock_result]

        with runner.isolated_filesystem():
            Path("tests").mkdir()
            Path("tests/test_example.do").write_text("// test")

            result = runner.invoke(main, ["--junit-xml", "junit.xml", "tests"])

            assert result.exit_code == 0
            mock_write_xml.assert_called_once()
            assert "JUnit XML written to" in result.output


class TestCLICoverage:
    """Tests for --coverage option."""

    @patch("statatest.cli.run_tests")
    @patch("statatest.cli.discover_tests")
    def test_coverage_without_source_shows_warning(self, mock_discover, mock_run):
        """Test that --coverage without source config shows warning."""
        runner = CliRunner()

        mock_test = MagicMock()
        mock_test.relative_path = "test_example.do"
        mock_discover.return_value = [mock_test]

        mock_result = MagicMock()
        mock_result.passed = True
        mock_result.duration = 0.1
        mock_run.return_value = [mock_result]

        with runner.isolated_filesystem():
            Path("tests").mkdir()
            Path("tests/test_example.do").write_text("// test")

            result = runner.invoke(main, ["--coverage", "tests"])

            assert result.exit_code == 0
            assert "no coverage.source configured" in result.output

    @patch("statatest.cli.cleanup_instrumented_environment")
    @patch("statatest.cli.setup_instrumented_environment")
    @patch("statatest.cli.run_tests")
    @patch("statatest.cli.discover_tests")
    def test_coverage_with_source_instruments_files(
        self, mock_discover, mock_run, mock_setup, mock_cleanup
    ):
        """Test that --coverage with source config instruments files."""
        runner = CliRunner()

        mock_test = MagicMock()
        mock_test.relative_path = "test_example.do"
        mock_discover.return_value = [mock_test]

        mock_result = MagicMock()
        mock_result.passed = True
        mock_result.duration = 0.1
        mock_run.return_value = [mock_result]

        # Mock instrumentation
        mock_setup.return_value = (Path(".statatest/instrumented"), {"file.ado": {}})

        with runner.isolated_filesystem():
            Path("tests").mkdir()
            Path("tests/test_example.do").write_text("// test")
            Path("code").mkdir()

            # Create config with coverage source
            Path("statatest.toml").write_text("""
[tool.statatest]
testpaths = ["tests"]

[tool.statatest.coverage]
source = ["code"]
""")

            result = runner.invoke(main, ["--coverage", "tests"])

            assert result.exit_code == 0
            mock_setup.assert_called_once()
            mock_cleanup.assert_called_once()


class TestCLIVerbose:
    """Tests for --verbose option."""

    @patch("statatest.cli.run_tests")
    @patch("statatest.cli.discover_tests")
    def test_verbose_shows_more_output(self, mock_discover, mock_run):
        """Test that --verbose shows additional output."""
        runner = CliRunner()

        mock_test = MagicMock()
        mock_test.relative_path = "test_example.do"
        mock_discover.return_value = [mock_test]

        mock_result = MagicMock()
        mock_result.passed = True
        mock_result.duration = 0.1
        mock_run.return_value = [mock_result]

        with runner.isolated_filesystem():
            Path("tests").mkdir()
            Path("tests/test_example.do").write_text("// test")

            result = runner.invoke(main, ["-v", "tests"])

            assert result.exit_code == 0


class TestCLIFilters:
    """Tests for -m/--marker and -k/--keyword options."""

    @patch("statatest.cli.run_tests")
    @patch("statatest.cli.discover_tests")
    def test_marker_filter_passed_to_discovery(self, mock_discover, mock_run):
        """Test that -m marker is passed to discover_tests."""
        runner = CliRunner()

        mock_discover.return_value = []

        with runner.isolated_filesystem():
            Path("tests").mkdir()

            result = runner.invoke(main, ["-m", "slow", "tests"])

            assert result.exit_code == 0
            # Check marker was passed
            call_args = mock_discover.call_args
            assert call_args.kwargs.get("marker") == "slow"

    @patch("statatest.cli.run_tests")
    @patch("statatest.cli.discover_tests")
    def test_keyword_filter_passed_to_discovery(self, mock_discover, mock_run):
        """Test that -k keyword is passed to discover_tests."""
        runner = CliRunner()

        mock_discover.return_value = []

        with runner.isolated_filesystem():
            Path("tests").mkdir()

            result = runner.invoke(main, ["-k", "integration", "tests"])

            assert result.exit_code == 0
            # Check keyword was passed
            call_args = mock_discover.call_args
            assert call_args.kwargs.get("keyword") == "integration"
