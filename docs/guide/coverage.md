# Code Coverage

statatest provides line-level code coverage for Stata `.ado` files.

## How It Works

Coverage is collected using invisible SMCL comment markers:

1. Source files are copied to `.statatest/instrumented/`
2. SMCL markers are injected: `{* COV:filename:lineno }`
3. Tests run with instrumented files
4. Markers are extracted from SMCL logs
5. Reports are generated with original file paths

The markers are invisible in Stata's output but preserved in raw `.smcl` logs.

## Enable Coverage

```bash
statatest tests/ --coverage
```

## Coverage Reports

### LCOV Format (for Codecov)

```bash
statatest tests/ --coverage --cov-report=lcov
```

Creates `coverage.lcov` in LCOV format:

```lcov
TN:statatest
SF:myfunction.ado
DA:5,1
DA:6,1
DA:10,0
LF:3
LH:2
end_of_record
```

### HTML Report

```bash
statatest tests/ --coverage --cov-report=html
```

Creates `htmlcov/index.html` with a visual coverage report.

## Configuration

Configure coverage in `statatest.toml`:

```toml
[tool.statatest.coverage]
# Source directories to instrument
source = ["code/functions"]

# Files/patterns to exclude
omit = ["tests/*", "*_test.ado"]
```

## Viewing Coverage

### Console Output

```console
============================================================
Coverage: 85.3%
  myfunction.ado: 90% (18/20 lines)
  helper.ado: 75% (15/20 lines)
============================================================
```

### HTML Report

Open `htmlcov/index.html` in a browser for detailed line-by-line coverage.

## Codecov Integration

Upload LCOV to Codecov for PR comments:

```yaml
# .github/workflows/tests.yml
- run: statatest tests/ --coverage --cov-report=lcov
- uses: codecov/codecov-action@v5
  with:
    files: coverage.lcov
```

See [Codecov Integration](../ci/codecov.md) for details.

## Limitations

- Coverage requires Stata to run with SMCL logging (`-s` flag)
- Only `.ado` files are instrumented (not `.do` files)
- Branch coverage is not yet supported (line coverage only)
