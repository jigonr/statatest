# CLI Reference

Complete command-line interface reference for statatest.

## Usage

```bash
statatest [OPTIONS] [PATH]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `PATH` | Test directory or file (default: `tests/`) |

## Options

### General

| Option | Short | Description |
|--------|-------|-------------|
| `--help` | `-h` | Show help message |
| `--version` | `-V` | Show version |
| `--verbose` | `-v` | Verbose output |
| `--quiet` | `-q` | Minimal output |

### Test Selection

| Option | Short | Description |
|--------|-------|-------------|
| `--keyword` | `-k` | Filter tests by keyword |
| `--marker` | `-m` | Filter tests by marker |

### Coverage

| Option | Description |
|--------|-------------|
| `--coverage` | Enable coverage collection |
| `--cov-report=TYPE` | Coverage report type: `lcov`, `html`, `term` |
| `--cov-fail-under=N` | Fail if coverage below N% |

### Reporting

| Option | Description |
|--------|-------------|
| `--junit-xml=PATH` | Generate JUnit XML report |

### Configuration

| Option | Description |
|--------|-------------|
| `--init` | Create default configuration file |
| `--config=PATH` | Specify config file path |

## Examples

### Basic Usage

```bash
# Run all tests
statatest tests/

# Run specific file
statatest tests/test_myfunction.do

# Run with verbose output
statatest --verbose tests/
```

### Filtering Tests

```bash
# Filter by keyword
statatest tests/ -k "regression"

# Filter by marker
statatest tests/ -m "unit"

# Exclude markers
statatest tests/ -m "not slow"

# Combine filters
statatest tests/ -k "regression" -m "unit"
```

### Coverage

```bash
# Enable coverage
statatest tests/ --coverage

# Generate LCOV report
statatest tests/ --coverage --cov-report=lcov

# Generate HTML report
statatest tests/ --coverage --cov-report=html

# Fail if coverage below threshold
statatest tests/ --coverage --cov-fail-under=80
```

### CI Integration

```bash
# Full CI command
statatest tests/ \
  --verbose \
  --coverage \
  --cov-report=lcov \
  --junit-xml=junit.xml
```

### Configuration

```bash
# Create config file
statatest --init

# Use specific config
statatest tests/ --config=myconfig.toml
```

## Exit Codes

| Code | Description |
|------|-------------|
| 0 | All tests passed |
| 1 | Some tests failed |
| 2 | Configuration error |
| 3 | No tests found |
| 4 | Coverage below threshold |

## Output Formats

### Default

```
statatest v0.1.0
Collecting tests from: tests
Found 5 test file(s)

.....

============================================================
5 passed in 2.34s
```

### Verbose

```
statatest v0.1.0
Collecting tests from: tests
Found 5 test file(s)

Running: tests/test_equal.do PASSED (0.25s)
Running: tests/test_true.do PASSED (0.18s)
Running: tests/test_false.do PASSED (0.22s)
Running: tests/test_var.do PASSED (0.31s)
Running: tests/test_file.do PASSED (0.28s)

============================================================
5 passed in 2.34s
```

### With Coverage

```
statatest v0.1.0
Collecting tests from: tests
Found 5 test file(s)

.....

============================================================
5 passed in 2.34s
============================================================
Coverage: 85.3%
  myfunction.ado: 90% (18/20 lines)
  helper.ado: 75% (15/20 lines)
============================================================
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `STATA_PATH` | Override Stata executable |
| `STATATEST_CONFIG` | Config file path |
| `NO_COLOR` | Disable colored output |
