# Installation

## Requirements

- **Python**: 3.11 or higher
- **Stata**: 16 or higher

## Using uv (Recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package manager.

```bash
# Install globally
uv tool install statatest

# Or run directly without installing
uvx statatest tests/
```

## Using pip

```bash
pip install statatest
```

## Development Installation

For contributing or development:

```bash
git clone https://github.com/jigonr/statatest.git
cd statatest
uv sync --dev
```

## Verify Installation

```bash
statatest --version
```

Should output:

```console
statatest version 0.1.0
```

## Stata Configuration

statatest needs to find your Stata executable. By default, it looks for
`stata-mp`. You can configure this in `statatest.toml`:

```toml
[tool.statatest]
stata_executable = "stata-se"  # or "stata", "stata-mp"
```

Or via environment variable:

```bash
export STATA_EXECUTABLE=stata-se
```
