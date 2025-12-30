# Codecov Integration

Upload Stata code coverage to Codecov for PR comments and coverage tracking.

## Quick Start

1. Sign up at [codecov.io](https://codecov.io) with GitHub
2. Add your repository token as `CODECOV_TOKEN` secret
3. Add the Codecov action to your workflow

```yaml
- run: statatest tests/ --coverage --cov-report=lcov
- uses: codecov/codecov-action@v5
  with:
    files: coverage.lcov
    token: ${{ secrets.CODECOV_TOKEN }}
```

---

## Setup Options

### Option 1: GitHub Actions (Recommended)

#### Step 1: Generate Coverage Report

Add to your workflow:

```yaml
- name: Run tests with coverage
  run: statatest tests/ --coverage --cov-report=lcov
```

This generates `coverage.lcov` in LCOV format.

#### Step 2: Get Upload Token

1. Go to [codecov.io](https://codecov.io) and log in with GitHub
2. Navigate to your repository
3. Copy the **Repository Upload Token**

!!! tip "Organization vs Repository Token" - **Repository token**: Works for a
single repository - **Organization token**: Works for all repositories in an
organization

#### Step 3: Add Token to GitHub Secrets

**For repository secret:**

1. Go to repository Settings > Secrets and variables > Actions
2. Click "New repository secret"
3. Name: `CODECOV_TOKEN`
4. Value: Paste your token

**For organization secret:**

1. Go to organization Settings > Secrets and variables > Actions
2. Click "New organization secret"
3. Name: `CODECOV_TOKEN`
4. Value: Paste your token
5. Select repository access

#### Step 4: Add Upload Step

```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v5
  with:
    files: coverage.lcov
    token: ${{ secrets.CODECOV_TOKEN }}
    fail_ci_if_error: false # Optional: don't fail CI if upload fails
```

#### Complete Workflow Example

```yaml
# .github/workflows/tests.yml
name: Tests

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
        uses: astral-sh/setup-uv@v5

      - name: Set up Stata license
        run: |
          echo "${{ secrets.STATA_LIC_B64 }}" | base64 -d > /usr/local/stata/stata.lic

      - name: Run tests with coverage
        run: |
          uvx statatest tests/ \
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

---

### Option 2: CircleCI

```yaml
# .circleci/config.yml
version: 2.1

orbs:
  codecov: codecov/codecov@4

jobs:
  test:
    docker:
      - image: dataeditors/stata18:latest
    steps:
      - checkout
      - run:
          name: Install uv
          command: curl -LsSf https://astral.sh/uv/install.sh | sh
      - run:
          name: Run tests with coverage
          command: uvx statatest tests/ --coverage --cov-report=lcov
      - codecov/upload:
          file: coverage.lcov

workflows:
  test:
    jobs:
      - test
```

Add `CODECOV_TOKEN` to CircleCI project environment variables.

---

### Option 3: Codecov CLI

For local testing or custom CI systems:

```bash
# Install Codecov CLI
pip install codecov-cli

# Generate coverage
statatest tests/ --coverage --cov-report=lcov

# Upload coverage
codecovcli upload-process \
  --token=$CODECOV_TOKEN \
  --file=coverage.lcov
```

---

## Codecov Configuration

Create `codecov.yml` in your repository root:

```yaml
# codecov.yml
codecov:
  require_ci_to_pass: true

coverage:
  precision: 2
  round: down
  range: "70...100"

  status:
    project:
      default:
        target: auto # Target = previous coverage
        threshold: 1% # Allow 1% drop

    patch:
      default:
        target: 80% # New code must have 80% coverage

comment:
  layout: "reach,diff,flags,files"
  behavior: default
  require_changes: false
```

---

## PR Comments

Codecov automatically adds comments to pull requests showing:

- Coverage diff (lines added/removed)
- Coverage percentage change
- Uncovered lines in the patch
- File-by-file breakdown

Example PR comment:

```markdown
## Coverage Report

| Coverage | Status           |
| -------- | ---------------- |
| Project  | 85.3% (+0.5%) ✅ |
| Patch    | 92.1% ✅         |

### Files Changed

| File           | Coverage | Lines |
| -------------- | -------- | ----- |
| myfunction.ado | 90%      | 18/20 |
| helper.ado     | 75%      | 15/20 |
```

---

## Coverage Flags

Use flags to track different coverage types:

```yaml
# codecov.yml
flags:
  unit:
    paths:
      - tests/unit/
    carryforward: true

  integration:
    paths:
      - tests/integration/
    carryforward: true
```

```yaml
# .github/workflows/tests.yml
- uses: codecov/codecov-action@v5
  with:
    files: coverage.lcov
    flags: unit
    token: ${{ secrets.CODECOV_TOKEN }}
```

---

## Coverage Targets

Set minimum coverage requirements:

```yaml
# codecov.yml
coverage:
  status:
    project:
      default:
        target: 80% # Fail if below 80%
        threshold: 2% # Allow 2% drop

    patch:
      default:
        target: 90% # New code must have 90% coverage
```

---

## Badges

Add a coverage badge to your README:

```{markdown}
[![codecov](https://codecov.io/gh/username/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/username/repo)
```

Replace `username/repo` with your repository path.

---

## LCOV Format

statatest generates LCOV format coverage:

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

- `TN`: Test name
- `SF`: Source file
- `DA:line,hits`: Line coverage data (line number, execution count)
- `LF`: Lines found (total)
- `LH`: Lines hit (covered)

---

## Troubleshooting

### Coverage Not Uploading

1. **Check token is correctly set**

   ```bash
   # Verify secret exists in GitHub Actions
   echo "Token length: ${#CODECOV_TOKEN}"
   ```

2. **Verify LCOV file exists**

   ```bash
   ls -la coverage.lcov
   cat coverage.lcov | head -20
   ```

3. **Check Codecov action logs** for specific error messages

4. **Test upload manually**

   ```bash
   curl -Os https://cli.codecov.io/latest/linux/codecov
   chmod +x codecov
   ./codecov upload-process -t $CODECOV_TOKEN -f coverage.lcov
   ```

### Coverage Shows 0% or Empty

1. **Verify source paths** are correctly configured in `statatest.toml`:

   ```toml
   [tool.statatest.coverage]
   source = ["code/functions"]  # Must point to your .ado files
   ```

2. **Check SMCL logging is enabled**
   - Tests must run with SMCL output for coverage collection
   - Coverage markers are invisible `{* COV:file:line }` comments

3. **Verify files are being instrumented**

   ```bash
   ls -la .statatest/instrumented/
   ```

### Coverage Too Low

1. Add more tests covering edge cases
2. Use coverage HTML report to identify uncovered lines:

   ```bash
   statatest tests/ --coverage --cov-report=html
   open htmlcov/index.html
   ```

3. Focus on testing error paths and boundary conditions

### Flaky Coverage

If coverage varies between runs:

1. **Ensure tests are deterministic** (use `fixture_seed`)
2. **Check for conditional code paths** that depend on random values
3. **Use `carryforward: true`** in flags to preserve coverage from previous runs

### Token Issues

| Error              | Solution                        |
| ------------------ | ------------------------------- |
| `401 Unauthorized` | Token is invalid or expired     |
| `404 Not Found`    | Repository not found in Codecov |
| `No coverage data` | LCOV file is empty or malformed |

---

## See Also

- [GitHub Actions Integration](github-actions.md)
- [Coverage Configuration](../guide/coverage.md)
- [Codecov Documentation](https://docs.codecov.io/)
