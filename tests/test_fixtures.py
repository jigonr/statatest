"""Tests for fixture module."""

import tempfile
from pathlib import Path

from statatest.fixtures import (
    Fixture,
    FixtureManager,
    discover_conftest,
    get_test_fixtures,
    parse_conftest,
)
from statatest.models import TestFile


def test_fixture_dataclass():
    """Test Fixture dataclass."""
    fixture = Fixture(
        name="sample_panel",
        scope="function",
        setup_program="fixture_sample_panel",
        teardown_program="fixture_sample_panel_teardown",
    )

    assert fixture.name == "sample_panel"
    assert fixture.scope == "function"
    assert fixture.setup_program == "fixture_sample_panel"
    assert fixture.teardown_program == "fixture_sample_panel_teardown"


def test_fixture_manager_register_and_get():
    """Test FixtureManager registration."""
    manager = FixtureManager()
    fixture = Fixture(name="test_fixture", setup_program="fixture_test_fixture")

    manager.register_fixture(fixture)

    assert manager.get_fixture("test_fixture") == fixture
    assert manager.get_fixture("nonexistent") is None


def test_fixture_manager_activation():
    """Test FixtureManager activation tracking."""
    manager = FixtureManager()

    assert not manager.is_active("sample_panel")

    manager.activate("sample_panel", "function")
    assert manager.is_active("sample_panel")

    manager.deactivate("sample_panel")
    assert not manager.is_active("sample_panel")


def test_fixture_manager_teardown_list():
    """Test FixtureManager teardown list by scope."""
    manager = FixtureManager()

    manager.activate("fixture1", "function")
    manager.activate("fixture2", "module")
    manager.activate("fixture3", "function")

    function_teardowns = manager.get_teardown_list("function")
    assert set(function_teardowns) == {"fixture1", "fixture3"}

    module_teardowns = manager.get_teardown_list("module")
    assert module_teardowns == ["fixture2"]


def test_discover_conftest():
    """Test conftest.do discovery."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir).resolve()

        # Create directory structure
        (tmppath / "tests").mkdir()
        (tmppath / "tests" / "unit").mkdir()

        # Create conftest files at different levels
        (tmppath / "conftest.do").write_text("// root conftest")
        (tmppath / "tests" / "conftest.do").write_text("// tests conftest")

        # Discover from tests/unit
        conftest_files = discover_conftest(tmppath / "tests" / "unit")

        assert len(conftest_files) == 2
        # Root comes first (use resolve() to normalize paths on macOS)
        assert conftest_files[0].resolve() == (tmppath / "conftest.do").resolve()
        assert (
            conftest_files[1].resolve() == (tmppath / "tests" / "conftest.do").resolve()
        )


def test_parse_conftest():
    """Test parsing fixture definitions from conftest.do."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        conftest_content = """
// Test conftest file

program define fixture_sample_panel
    clear
    set obs 100
end

program define fixture_sample_panel_teardown
    clear
end

program define fixture_empty_data
    clear
end

program define helper_function
    // This should not be detected as a fixture
end
"""
        conftest_path = tmppath / "conftest.do"
        conftest_path.write_text(conftest_content)

        fixtures = parse_conftest(conftest_path)

        assert len(fixtures) == 2

        # Check sample_panel fixture
        sample_panel = next(f for f in fixtures if f.name == "sample_panel")
        assert sample_panel.setup_program == "fixture_sample_panel"
        assert sample_panel.teardown_program == "fixture_sample_panel_teardown"

        # Check empty_data fixture (no teardown)
        empty_data = next(f for f in fixtures if f.name == "empty_data")
        assert empty_data.setup_program == "fixture_empty_data"
        assert empty_data.teardown_program == ""


def test_get_test_fixtures_from_comments():
    """Test extracting fixture requirements from test file comments."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        test_content = """
// test_example.do
//
// @uses_fixture: sample_panel
// @uses_fixture: seed

program define test_something
    assert_true 1 == 1
end
"""
        test_path = tmppath / "test_example.do"
        test_path.write_text(test_content)

        test_file = TestFile(
            path=test_path,
            markers=["unit"],
            programs=[],
        )

        fixtures = get_test_fixtures(test_file)

        assert set(fixtures) == {"sample_panel", "seed"}


def test_get_test_fixtures_from_calls():
    """Test extracting fixture requirements from use_fixture calls."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        test_content = """
program define test_something
    use_fixture sample_panel
    use_fixture empty_dataset
    assert_true _N > 0
end
"""
        test_path = tmppath / "test_example.do"
        test_path.write_text(test_content)

        test_file = TestFile(
            path=test_path,
            markers=[],
            programs=[],
        )

        fixtures = get_test_fixtures(test_file)

        assert set(fixtures) == {"sample_panel", "empty_dataset"}
