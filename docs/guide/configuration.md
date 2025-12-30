# Configuration

statatest uses a TOML configuration file for project settings.

## Configuration File

Create `statatest.toml` in your project root:

```toml
[tool.statatest]
# Test discovery
testpaths = ["tests"]
test_files = ["test_*.do"]

# Stata executable (auto-detected if not set)
stata_executable = "stata-mp"

[tool.statatest.coverage]
# Source directories to instrument
source = ["code/functions"]

# Files/patterns to exclude from coverage
omit = ["tests/*", "*_test.ado"]

[tool.statatest.reporting]
# JUnit XML output for CI
junit_xml = "junit.xml"

# LCOV output for Codecov
lcov = "coverage.lcov"
```

## Initialize Configuration

Generate a configuration file with defaults:

```bash
statatest --init
```

## Configuration Options

### Test Discovery

| Option             | Type   | Default         | Description                     |
| ------------------ | ------ | --------------- | ------------------------------- |
| `testpaths`        | list   | `["tests"]`     | Directories to search for tests |
| `test_files`       | list   | `["test_*.do"]` | Glob patterns for test files    |
| `stata_executable` | string | auto            | Path to Stata executable        |

### Coverage Settings

| Option   | Type | Default | Description                                       |
| -------- | ---- | ------- | ------------------------------------------------- |
| `source` | list | `[]`    | Directories containing `.ado` files to instrument |
| `omit`   | list | `[]`    | Patterns to exclude from coverage                 |

### Reporting

| Option      | Type   | Default | Description                   |
| ----------- | ------ | ------- | ----------------------------- |
| `junit_xml` | string | `null`  | Path for JUnit XML output     |
| `lcov`      | string | `null`  | Path for LCOV coverage output |

## Auto-Detection

statatest automatically detects the Stata executable:

1. Checks `stata_executable` in config
2. Looks for `stata-mp`, `stata-se`, `stata` in PATH
3. Checks common installation paths

## Environment Variables

| Variable           | Description                                     |
| ------------------ | ----------------------------------------------- |
| `STATA_PATH`       | Override Stata executable path                  |
| `STATATEST_CONFIG` | Path to config file (default: `statatest.toml`) |

## Example Configurations

### Minimal

```toml
[tool.statatest]
testpaths = ["tests"]
```

### Full Project

```toml
[tool.statatest]
testpaths = ["tests/unit", "tests/integration"]
test_files = ["test_*.do"]
stata_executable = "/usr/local/bin/stata-mp"

[tool.statatest.coverage]
source = ["code/functions", "code/lib"]
omit = ["tests/*", "examples/*"]

[tool.statatest.reporting]
junit_xml = "junit.xml"
lcov = "coverage.lcov"
```

### CI Environment

```toml
[tool.statatest]
testpaths = ["tests"]
stata_executable = "stata-mp"

[tool.statatest.coverage]
source = ["src"]

[tool.statatest.reporting]
junit_xml = "results/junit.xml"
lcov = "results/coverage.lcov"
```
