"""Tests for source code instrumentation module."""

import tempfile
from pathlib import Path

from statatest.coverage.instrument import (
    _ends_with_continuation,
    cleanup_instrumented_environment,
    get_total_lines,
    instrument_directory,
    instrument_file,
    setup_instrumented_environment,
    should_instrument_line,
)


class TestShouldInstrumentLine:
    """Tests for should_instrument_line function."""

    def test_instrument_regular_code(self):
        """Regular code lines should be instrumented."""
        assert should_instrument_line("    gen x = 1")
        assert should_instrument_line("local foo = 42")
        assert should_instrument_line("    regress y x")

    def test_skip_empty_lines(self):
        """Empty lines should not be instrumented."""
        assert not should_instrument_line("")
        assert not should_instrument_line("   ")
        assert not should_instrument_line("\t")

    def test_skip_comment_lines(self):
        """Comment lines should not be instrumented."""
        assert not should_instrument_line("* This is a comment")
        assert not should_instrument_line("// Another comment")
        assert not should_instrument_line("/* Block comment start")
        assert not should_instrument_line("*/ Block comment end")

    def test_skip_program_structure(self):
        """Program structure lines should not be instrumented."""
        assert not should_instrument_line("program define myprogram")
        assert not should_instrument_line("program drop myprogram")
        assert not should_instrument_line("end")
        assert not should_instrument_line("    end")

    def test_skip_syntax_related(self):
        """Syntax-related lines should not be instrumented."""
        assert not should_instrument_line("version 16")
        assert not should_instrument_line("    syntax anything")
        assert not should_instrument_line("    args x y z")
        assert not should_instrument_line("    marksample touse")

    def test_skip_continuation_start_lines(self):
        """Lines that only contain /// should not be instrumented."""
        # Lines that are ONLY continuation markers (start with ///) are skipped
        assert not should_instrument_line("///")
        assert not should_instrument_line("    /// continuation comment")

    def test_continuation_context_instruments_all_lines(self):
        """Lines inside continuation context should be instrumented."""
        # When in_continuation=True, all lines are instrumented
        # (they're part of a multi-line command)
        assert should_instrument_line("    , absorb(id)", in_continuation=True)
        assert should_instrument_line("    vce(cluster id)", in_continuation=True)
        # Even comment-like content is instrumented in continuation
        assert should_instrument_line("    /// comment", in_continuation=True)


class TestInstrumentFile:
    """Tests for instrument_file function."""

    def test_instrument_simple_file(self):
        """Test instrumenting a simple .ado file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            source_content = """\
*! myfunction v1.0
program define myfunction
    version 16
    syntax anything
    gen x = 1
    gen y = 2
end
"""
            source_path = tmppath / "myfunction.ado"
            source_path.write_text(source_content)

            dest_path = tmppath / "instrumented" / "myfunction.ado"
            line_map = instrument_file(source_path, dest_path)

            # Check file was created
            assert dest_path.exists()

            # Check instrumented content
            instrumented = dest_path.read_text()
            assert "{* COV:myfunction.ado:5 }" in instrumented
            assert "{* COV:myfunction.ado:6 }" in instrumented

            # Check line map
            assert 5 in line_map.values()
            assert 6 in line_map.values()

    def test_instrument_preserves_structure(self):
        """Test that instrumentation preserves program structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            source_content = """\
program define test
    version 16
    local x = 1
    if `x' == 1 {
        display "yes"
    }
end
"""
            source_path = tmppath / "test.ado"
            source_path.write_text(source_content)

            dest_path = tmppath / "instrumented" / "test.ado"
            instrument_file(source_path, dest_path)

            instrumented = dest_path.read_text()

            # Program structure should be preserved
            assert "program define test" in instrumented
            assert "version 16" in instrumented
            assert "end" in instrumented


class TestInstrumentDirectory:
    """Tests for instrument_directory function."""

    def test_instrument_multiple_files(self):
        """Test instrumenting multiple files in a directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            source_dir = tmppath / "source"
            source_dir.mkdir()

            # Create multiple .ado files
            (source_dir / "func1.ado").write_text(
                "program define func1\n    gen x = 1\nend\n"
            )
            (source_dir / "func2.ado").write_text(
                "program define func2\n    gen y = 2\nend\n"
            )
            (source_dir / "notado.txt").write_text("not an ado file")

            dest_dir = tmppath / "instrumented"
            all_maps = instrument_directory(source_dir, dest_dir)

            # Check both .ado files were instrumented
            assert "func1.ado" in all_maps
            assert "func2.ado" in all_maps

            # Check .txt file was not instrumented
            assert not (dest_dir / "notado.txt").exists()


class TestSetupInstrumentedEnvironment:
    """Tests for setup_instrumented_environment function."""

    def test_setup_creates_directory(self):
        """Test that setup creates .statatest/instrumented directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            source_dir = tmppath / "source"
            source_dir.mkdir()
            (source_dir / "test.ado").write_text(
                "program define test\n    gen x = 1\nend\n"
            )

            instrumented_dir, maps = setup_instrumented_environment(
                [source_dir], tmppath
            )

            assert instrumented_dir.exists()
            assert instrumented_dir == tmppath / ".statatest" / "instrumented"
            assert (instrumented_dir / "test.ado").exists()


class TestCleanupInstrumentedEnvironment:
    """Tests for cleanup_instrumented_environment function."""

    def test_cleanup_removes_directory(self):
        """Test that cleanup removes .statatest directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create .statatest directory
            statatest_dir = tmppath / ".statatest"
            statatest_dir.mkdir()
            (statatest_dir / "instrumented").mkdir()
            (statatest_dir / "instrumented" / "test.ado").write_text("content")

            cleanup_instrumented_environment(tmppath)

            assert not statatest_dir.exists()


class TestGetTotalLines:
    """Tests for get_total_lines function."""

    def test_get_total_lines(self):
        """Test getting total instrumentable lines."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            source_content = """\
*! comment
program define test
    version 16
    gen x = 1
    gen y = 2
    gen z = 3
end
"""
            source_path = tmppath / "test.ado"
            source_path.write_text(source_content)

            total_lines = get_total_lines(source_path)

            # Lines 4, 5, 6 should be instrumentable (gen statements)
            assert 4 in total_lines
            assert 5 in total_lines
            assert 6 in total_lines

            # Lines 1, 2, 3, 7 should not be instrumentable
            assert 1 not in total_lines  # comment
            assert 2 not in total_lines  # program define
            assert 3 not in total_lines  # version
            assert 7 not in total_lines  # end


class TestContinuationLines:
    """Tests for Stata continuation line (///) handling.

    In Stata, /// at the end of a line continues the command to the next line.
    All lines of a multi-line command should be instrumented for coverage.
    """

    def test_ends_with_continuation_basic(self):
        """Test _ends_with_continuation detects /// at end of line."""
        assert _ends_with_continuation("reghdfe y x ///")
        assert _ends_with_continuation("    , absorb(id) ///")
        assert not _ends_with_continuation("reghdfe y x")
        assert not _ends_with_continuation("// comment with /// inside")

    def test_ends_with_continuation_whitespace(self):
        """Test _ends_with_continuation handles trailing whitespace."""
        # Trailing whitespace after /// should still be detected
        assert _ends_with_continuation("reghdfe y x ///  ")
        assert _ends_with_continuation("reghdfe y x ///\t")

    def test_instrument_file_continuation_all_lines(self):
        """Test that all lines in a continuation are instrumented."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Stata command spanning 3 lines with ///
            source_content = """\
program define test_regression
    version 16
    reghdfe y x ///
        , absorb(id) ///
        vce(cluster id)
    display "done"
end
"""
            source_path = tmppath / "test_regression.ado"
            source_path.write_text(source_content)

            dest_path = tmppath / "instrumented" / "test_regression.ado"
            line_map = instrument_file(source_path, dest_path)

            instrumented = dest_path.read_text()

            # Line 3 (reghdfe y x ///) - starts the command
            assert "{* COV:test_regression.ado:3 }" in instrumented
            # Line 4 (, absorb(id) ///) - continuation
            assert "{* COV:test_regression.ado:4 }" in instrumented
            # Line 5 (vce(cluster id)) - final line of continuation
            assert "{* COV:test_regression.ado:5 }" in instrumented
            # Line 6 (display "done") - next command
            assert "{* COV:test_regression.ado:6 }" in instrumented

            # All 4 lines should be in the line map
            assert 3 in line_map.values()
            assert 4 in line_map.values()
            assert 5 in line_map.values()
            assert 6 in line_map.values()

    def test_get_total_lines_continuation(self):
        """Test that get_total_lines includes all continuation lines."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            source_content = """\
program define mytest
    version 16
    reghdfe y x ///
        , absorb(id) ///
        vce(cluster id)
end
"""
            source_path = tmppath / "mytest.ado"
            source_path.write_text(source_content)

            total_lines = get_total_lines(source_path)

            # Lines 3, 4, 5 should all be instrumentable
            assert 3 in total_lines  # reghdfe y x ///
            assert 4 in total_lines  # , absorb(id) ///
            assert 5 in total_lines  # vce(cluster id)

    def test_multiple_continuation_blocks(self):
        """Test multiple separate continuation blocks in one file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            source_content = """\
program define mytest
    version 16
    * First multi-line command
    gen x = 1 + ///
        2 + ///
        3
    * Second multi-line command
    gen y = 4 + ///
        5
end
"""
            source_path = tmppath / "mytest.ado"
            source_path.write_text(source_content)

            total_lines = get_total_lines(source_path)

            # First block: lines 4, 5, 6
            assert 4 in total_lines
            assert 5 in total_lines
            assert 6 in total_lines

            # Second block: lines 8, 9
            assert 8 in total_lines
            assert 9 in total_lines
