# Tests

Python test suite for statatest.

## Structure

```plaintext
tests/
├── conftest.py         # Shared pytest fixtures
├── test_cli.py         # CLI tests
├── test_config.py      # Configuration tests
├── test_coverage.py    # Coverage module tests
├── test_discovery.py   # Discovery module tests
├── test_fixtures.py    # Fixtures module tests
├── test_instrument.py  # Instrumentation tests
├── test_report.py      # Reporting tests
└── test_runner.py      # Execution tests
```

## Running Tests

```bash
# All tests
uv run pytest tests/ -v

# Specific file
uv run pytest tests/test_runner.py -v

# By keyword
uv run pytest tests/ -k "coverage" -v

# With coverage
uv run pytest tests/ --cov=src/statatest --cov-report=term-missing
```

## Test Categories

### Unit Tests

Most tests are unit tests that mock Stata execution:

```python
def test_parse_result():
    output = "_STATATEST_PASS_:assert_true_"
    result = parse_output(output)
    assert result.passed
```

### Integration Tests

Tests marked with `@pytest.mark.requires_stata` need Stata installed:

```python
@pytest.mark.requires_stata
def test_run_actual_test():
    # Runs real Stata subprocess
    ...
```

## Writing Tests

Follow these patterns:

```python
class TestFeatureName:
    """Tests for feature_name."""

    def test_basic_case(self):
        """Test the happy path."""
        ...

    def test_edge_case(self):
        """Test edge case."""
        ...

    def test_error_case(self):
        """Test error handling."""
        ...
```

## Coverage Target

Maintain **90%+ test coverage**.
