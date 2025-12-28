# statatest GitHub Action

The `jigonr/statatest/action` provides zero-install Stata testing in GitHub Actions.

## Quick Start

```yaml
name: Stata Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    container:
      image: dataeditors/stata18_5-mp:2025-02-26
      options: --user root

    steps:
      - uses: actions/checkout@v4

      - uses: jigonr/statatest/action@v1
        with:
          tests: tests/
          stata-license: ${{ secrets.STATA_LIC_B64 }}
```

## Features

- **Zero installation**: No need to install Python or statatest locally
- **Automatic setup**: Installs uv and statatest automatically
- **License handling**: Decodes and sets up Stata license from secrets
- **Full CLI support**: All statatest options available as inputs

## Inputs

### Required

| Input | Description |
|-------|-------------|
| `stata-license` | Base64-encoded Stata license from `secrets.STATA_LIC_B64` |

### Optional

| Input | Description | Default |
|-------|-------------|---------|
| `tests` | Path to test files or directory | `tests/` |
| `coverage` | Enable coverage collection | `false` |
| `cov-report` | Coverage report format (lcov, html) | `lcov` |
| `junit-xml` | Path for JUnit XML output | - |
| `marker` | Only run tests with this marker (-m) | - |
| `keyword` | Only run tests matching keyword (-k) | - |
| `verbose` | Enable verbose output | `false` |
| `statatest-version` | Specific version to install | latest |

## Examples

### Basic Testing

```yaml
- uses: jigonr/statatest/action@v1
  with:
    tests: tests/
    stata-license: ${{ secrets.STATA_LIC_B64 }}
```

### With Coverage and Codecov

```yaml
- uses: jigonr/statatest/action@v1
  with:
    tests: tests/
    stata-license: ${{ secrets.STATA_LIC_B64 }}
    coverage: true
    cov-report: lcov
    junit-xml: junit.xml

- uses: codecov/codecov-action@v4
  with:
    files: coverage.lcov
    token: ${{ secrets.CODECOV_TOKEN }}
```

### Filter by Marker

Run only tests marked with `@slow`:

```yaml
- uses: jigonr/statatest/action@v1
  with:
    tests: tests/
    stata-license: ${{ secrets.STATA_LIC_B64 }}
    marker: slow
```

### Filter by Keyword

Run only tests with "regression" in the name:

```yaml
- uses: jigonr/statatest/action@v1
  with:
    tests: tests/
    stata-license: ${{ secrets.STATA_LIC_B64 }}
    keyword: regression
```

### Pin statatest Version

```yaml
- uses: jigonr/statatest/action@v1
  with:
    tests: tests/
    stata-license: ${{ secrets.STATA_LIC_B64 }}
    statatest-version: '0.1.0'
```

## Outputs

The action provides outputs for use in subsequent steps:

| Output | Description |
|--------|-------------|
| `passed` | Number of tests passed |
| `failed` | Number of tests failed |
| `total` | Total number of tests |

```yaml
- uses: jigonr/statatest/action@v1
  id: tests
  with:
    tests: tests/
    stata-license: ${{ secrets.STATA_LIC_B64 }}

- run: echo "Passed ${{ steps.tests.outputs.passed }} of ${{ steps.tests.outputs.total }} tests"
```

## Container Setup

The action must run inside a Stata Docker container:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    container:
      image: dataeditors/stata18_5-mp:2025-02-26
      options: --user root  # Required for package installation
```

See [Docker Integration](docker.md) for available images and version tags.

## License Setup

1. **Encode your license:**
   ```bash
   base64 -i stata.lic -o stata_lic_b64.txt
   cat stata_lic_b64.txt
   ```

2. **Add to GitHub Secrets:**
   - Go to repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `STATA_LIC_B64`
   - Value: Paste the base64 content

3. **Reference in workflow:**
   ```yaml
   stata-license: ${{ secrets.STATA_LIC_B64 }}
   ```

## Troubleshooting

### License Not Found

```
stata.lic not found
```

Ensure `STATA_LIC_B64` secret is set and the action has access to it.

### Permission Denied

```
Permission denied
```

Add `options: --user root` to the container configuration.

### statatest Not Found

```
statatest: command not found
```

The action installs statatest automatically. If this fails, check that the container has internet access.
