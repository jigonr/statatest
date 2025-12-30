# Contributing

See
[CONTRIBUTING.md](https://github.com/jigonr/statatest/blob/main/CONTRIBUTING.md)
in the repository root for complete contribution guidelines.

## Quick Start

```bash
# Clone
git clone https://github.com/jigonr/statatest.git
cd statatest

# Install
uv sync --all-extras

# Test
uv run pytest tests/ -v
uv run ruff check src/ tests/
uv run mypy src/ --strict
```

## Commit Format

```
<type>(<scope>): <description>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Code Quality

- **Coverage**: 90%+
- **Linting**: ruff (zero errors)
- **Types**: mypy --strict
