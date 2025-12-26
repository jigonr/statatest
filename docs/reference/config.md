# Configuration Reference

Complete reference for `statatest.toml` configuration options.

## File Location

statatest looks for configuration in:

1. `statatest.toml` in current directory
2. `pyproject.toml` under `[tool.statatest]`
3. Path specified by `--config` option
4. Path specified by `STATATEST_CONFIG` environment variable

## Schema

```toml
[tool.statatest]
# Test discovery
testpaths = ["tests"]
test_files = ["test_*.do"]
stata_executable = "stata-mp"

[tool.statatest.coverage]
source = ["code/functions"]
omit = ["tests/*"]

[tool.statatest.reporting]
junit_xml = "junit.xml"
lcov = "coverage.lcov"
```

## Options Reference

### `[tool.statatest]`

#### `testpaths`

Directories to search for test files.

- **Type:** `list[str]`
- **Default:** `["tests"]`

```toml
testpaths = ["tests/unit", "tests/integration"]
```

#### `test_files`

Glob patterns for test file discovery.

- **Type:** `list[str]`
- **Default:** `["test_*.do"]`

```toml
test_files = ["test_*.do", "*_test.do"]
```

#### `stata_executable`

Path to Stata executable.

- **Type:** `str`
- **Default:** Auto-detected

```toml
stata_executable = "/usr/local/bin/stata-mp"
```

Auto-detection order:

1. `stata-mp`
2. `stata-se`
3. `stata`
4. Common installation paths

### `[tool.statatest.coverage]`

#### `source`

Directories containing `.ado` files to instrument.

- **Type:** `list[str]`
- **Default:** `[]`

```toml
[tool.statatest.coverage]
source = ["code/functions", "code/lib"]
```

#### `omit`

Patterns to exclude from coverage.

- **Type:** `list[str]`
- **Default:** `[]`

```toml
[tool.statatest.coverage]
omit = ["tests/*", "*_test.ado", "examples/*"]
```

### `[tool.statatest.reporting]`

#### `junit_xml`

Path for JUnit XML test results.

- **Type:** `str | null`
- **Default:** `null`

```toml
[tool.statatest.reporting]
junit_xml = "results/junit.xml"
```

#### `lcov`

Path for LCOV coverage report.

- **Type:** `str | null`
- **Default:** `null`

```toml
[tool.statatest.reporting]
lcov = "results/coverage.lcov"
```

## Example Configurations

### Minimal

```toml
[tool.statatest]
testpaths = ["tests"]
```

### Research Project

```toml
[tool.statatest]
testpaths = ["tests/unit", "tests/integration"]
test_files = ["test_*.do"]
stata_executable = "stata-mp"

[tool.statatest.coverage]
source = ["code/functions"]
omit = ["tests/*", "examples/*"]

[tool.statatest.reporting]
junit_xml = "junit.xml"
lcov = "coverage.lcov"
```

### Monorepo

```toml
[tool.statatest]
testpaths = [
  "packages/core/tests",
  "packages/utils/tests",
  "packages/analysis/tests"
]

[tool.statatest.coverage]
source = [
  "packages/core/src",
  "packages/utils/src",
  "packages/analysis/src"
]
```

### CI-Optimized

```toml
[tool.statatest]
testpaths = ["tests"]
stata_executable = "stata-mp"

[tool.statatest.reporting]
junit_xml = "test-results/junit.xml"
lcov = "test-results/coverage.lcov"
```

## pyproject.toml Integration

Configuration can also be placed in `pyproject.toml`:

```toml
# pyproject.toml
[project]
name = "my-stata-project"
version = "1.0.0"

[tool.statatest]
testpaths = ["tests"]

[tool.statatest.coverage]
source = ["code/functions"]
```

## Validation

statatest validates configuration on startup:

```bash
$ statatest tests/
Error: Invalid configuration in statatest.toml
  - testpaths[0]: Directory 'tests' does not exist
```

## Precedence

Configuration sources are merged in order (later overrides earlier):

1. Built-in defaults
2. `pyproject.toml` `[tool.statatest]`
3. `statatest.toml`
4. `--config` file
5. Command-line options
