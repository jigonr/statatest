# Contributing to statatest

Thank you for your interest in contributing to statatest! This document provides
guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person

## How to Submit Issues

Before submitting an issue:

1. **Search existing issues** to avoid duplicates
2. **Use issue templates** when available
3. **Provide complete information**:
   - statatest version (`pip show statatest`)
   - Python version (`python --version`)
   - Stata version (`stata -v`)
   - Operating system
   - Minimal reproducible example

### Issue Types

| Label         | Use For                    |
| ------------- | -------------------------- |
| `bug`         | Something isn't working    |
| `enhancement` | New feature requests       |
| `docs`        | Documentation improvements |
| `question`    | Usage questions            |

**Note**: Discussing your idea in an issue first increases the likelihood of
your PR being accepted.

## How to Submit Pull Requests

### Fork Workflow

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/statatest.git
cd statatest

# 3. Add upstream remote
git remote add upstream https://github.com/jigonr/statatest.git

# 4. Create a feature branch
git checkout -b feat/your-feature-name

# 5. Make changes, commit, push
git push origin feat/your-feature-name

# 6. Open PR on GitHub
```

### Branch Naming

| Prefix      | Use For          |
| ----------- | ---------------- |
| `feat/`     | New features     |
| `fix/`      | Bug fixes        |
| `docs/`     | Documentation    |
| `refactor/` | Code refactoring |
| `test/`     | Test additions   |

### PR Checklist

- [ ] All tests pass (`uv run pytest tests/`)
- [ ] Linting passes (`uv run ruff check src/ tests/`)
- [ ] Type checking passes (`uv run mypy src/ --strict`)
- [ ] Coverage maintained at 90%+
- [ ] Commit messages follow Conventional Commits
- [ ] Documentation updated if needed

## Development Setup

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Stata 16+ (for integration tests)

### Installation

```bash
# Clone the repository
git clone https://github.com/jigonr/statatest.git
cd statatest

# Install dependencies
uv sync --all-extras

# Run tests
uv run pytest tests/ -v

# Run linting
uv run ruff check src/ tests/

# Run type checking
uv run mypy src/ --strict
```

### Running Specific Tests

```bash
# Run a specific test file
uv run pytest tests/test_runner.py -v

# Run tests matching a pattern
uv run pytest tests/ -k "coverage" -v

# Run with coverage report
uv run pytest tests/ --cov=src/statatest --cov-report=term-missing
```

## Code Style Guidelines

### Python

- **Formatter**: ruff format
- **Linter**: ruff check
- **Type checker**: mypy --strict
- **Docstrings**: Google style

```python
def function_name(arg1: str, arg2: int = 0) -> bool:
    """Short summary (one line).

    Longer description if needed.

    Args:
        arg1: Description of arg1.
        arg2: Description of arg2. Defaults to 0.

    Returns:
        Description of return value.

    Raises:
        ValueError: When arg1 is empty.
    """
```

### Stata (.ado files)

```stata
*! command_name v1.0.0  statatest  YYYY-MM-DD
*!
*! Brief description.
*!
*! Syntax:
*!   command_name varlist [if] [in], required(type) [optional(type)]
*!
*! Example:
*!   command_name myvar, required("value")

program define command_name, rclass
    version 16
    syntax ...
    // Implementation
end
```

## Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```plaintext
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type       | Description                     |
| ---------- | ------------------------------- |
| `feat`     | New feature                     |
| `fix`      | Bug fix                         |
| `docs`     | Documentation only              |
| `style`    | Formatting, no code change      |
| `refactor` | Code change without feature/fix |
| `test`     | Adding tests                    |
| `chore`    | Maintenance tasks               |

### Examples

```bash
# Feature
feat(assertions): add assert_count for observation counting

# Bug fix
fix(coverage): correct adopath priority for instrumented files

# Documentation
docs(readme): add installation instructions

# With scope
feat(cli): add --verbose flag for detailed output

# Breaking change
feat(api)!: rename TestResult to ExecutionResult

BREAKING CHANGE: TestResult class renamed to ExecutionResult
```

## Testing Requirements

### Coverage

- Maintain **90%+ test coverage**
- Add tests for all new features
- Add regression tests for bug fixes

### Test Organization

```plaintext
tests/
├── test_cli.py          # CLI tests
├── test_coverage.py     # Coverage module tests
├── test_discovery.py    # Discovery module tests
├── test_runner.py       # Execution tests
└── conftest.py          # Shared fixtures
```

### Writing Tests

```python
class TestFeatureName:
    """Tests for feature_name functionality."""

    def test_basic_usage(self):
        """Test the basic happy path."""
        result = feature_name("input")
        assert result == "expected"

    def test_edge_case(self):
        """Test edge case with empty input."""
        result = feature_name("")
        assert result is None
```

## Questions?

- Open a [GitHub issue](https://github.com/jigonr/statatest/issues)
- Check existing [discussions](https://github.com/jigonr/statatest/discussions)
