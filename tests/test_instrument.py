"""Tests for source code instrumentation module."""

import tempfile
from pathlib import Path

from statatest.coverage.instrument import (
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

    def test_skip_continuation_lines(self):
        """Continuation lines should not be instrumented."""
        assert not should_instrument_line("///")
        assert not should_instrument_line("    /// continuation")


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
