# statatest GitHub Action

Run Stata tests in CI with zero local installation required.

## Usage

### Basic Example

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

### With Coverage

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

### Filter Tests

```yaml
      - uses: jigonr/statatest/action@v1
        with:
          tests: tests/
          stata-license: ${{ secrets.STATA_LIC_B64 }}
          marker: slow        # Only tests marked @slow
          keyword: regression # Only tests matching "regression"
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `tests` | Path to test files or directory | No | `tests/` |
| `stata-license` | Base64-encoded Stata license | **Yes** | - |
| `coverage` | Enable coverage collection | No | `false` |
| `cov-report` | Coverage report format (lcov, html) | No | `lcov` |
| `junit-xml` | Path for JUnit XML output | No | - |
| `marker` | Only run tests with this marker | No | - |
| `keyword` | Only run tests matching keyword | No | - |
| `verbose` | Enable verbose output | No | `false` |
| `statatest-version` | Version of statatest to install | No | latest |

## Outputs

| Output | Description |
|--------|-------------|
| `passed` | Number of tests passed |
| `failed` | Number of tests failed |
| `total` | Total number of tests |

## License Setup

1. Encode your Stata license:
   ```bash
   base64 -i stata.lic -o stata_lic_b64.txt
   ```

2. Add to GitHub Secrets as `STATA_LIC_B64`

3. Reference in workflow: `${{ secrets.STATA_LIC_B64 }}`

## Container Images

This action is designed to run inside AEA Data Editor's Stata containers:

| Image | Stata Version |
|-------|---------------|
| `dataeditors/stata18_5-mp:2025-02-26` | 18.5 MP |
| `dataeditors/stata18_5-se:2025-02-26` | 18.5 SE |
| `dataeditors/stata19_5-mp:2025-12-19` | 19.5 MP |

Always use pinned date tags, never `latest`.

## Requirements

- GitHub Actions runner with Docker support
- Valid Stata license
- AEA Data Editor's Stata Docker image
