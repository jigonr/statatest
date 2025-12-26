# GitHub Actions

Run Stata tests in GitHub Actions CI/CD pipelines.

## Basic Workflow

```yaml
# .github/workflows/tests.yml
name: Stata Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    container:
      image: dataeditors/stata18:latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install statatest
        run: pip install statatest

      - name: Set up Stata license
        run: |
          echo "${{ secrets.STATA_LIC_B64 }}" | base64 -d > /usr/local/stata/stata.lic

      - name: Run tests
        run: statatest tests/ --junit-xml=junit.xml

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: junit.xml
```

## With Coverage

```yaml
# .github/workflows/tests.yml
name: Stata Tests with Coverage

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    container:
      image: dataeditors/stata18:latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install statatest
        run: pip install statatest

      - name: Set up Stata license
        run: |
          echo "${{ secrets.STATA_LIC_B64 }}" | base64 -d > /usr/local/stata/stata.lic

      - name: Run tests with coverage
        run: |
          statatest tests/ \
            --coverage \
            --cov-report=lcov \
            --junit-xml=junit.xml

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v5
        with:
          files: coverage.lcov
          token: ${{ secrets.CODECOV_TOKEN }}

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: |
            junit.xml
            coverage.lcov
```

## Stata License Setup

### 1. Encode your license

```bash
base64 -i stata.lic | pbcopy  # macOS
base64 stata.lic | xclip      # Linux
```

### 2. Add to GitHub Secrets

1. Go to repository Settings > Secrets > Actions
2. Create new secret: `STATA_LIC_B64`
3. Paste the base64-encoded license

## Docker Images

### dataeditors/stata18

Official Stata Docker image from AEA Data Editor:

```yaml
container:
  image: dataeditors/stata18:latest
```

License path: `/usr/local/stata/stata.lic`

### Custom Image

```dockerfile
FROM dataeditors/stata18:latest

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip

# Install statatest
RUN pip3 install statatest
```

## Matrix Testing

Test across multiple Stata versions:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        stata-version: ["17", "18"]
    container:
      image: dataeditors/stata${{ matrix.stata-version }}:latest

    steps:
      - uses: actions/checkout@v4
      # ... rest of steps
```

## Test Result Reporting

GitHub Actions can display test results in PR comments using JUnit XML:

```yaml
- name: Publish Test Results
  uses: EnricoMi/publish-unit-test-result-action@v2
  if: always()
  with:
    files: junit.xml
```

## Caching

Cache pip packages for faster builds:

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

## Troubleshooting

### License Issues

```
r(601): license not found
```

Check that:
1. `STATA_LIC_B64` secret is correctly set
2. License path matches Docker image location
3. Base64 encoding is correct

### Permission Denied

```
stata-mp: Permission denied
```

Ensure the container runs with appropriate permissions:

```yaml
container:
  image: dataeditors/stata18:latest
  options: --user root
```
