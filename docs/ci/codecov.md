# Codecov Integration

Upload Stata code coverage to Codecov for PR comments and coverage tracking.

## Setup

### 1. Enable Codecov

1. Go to [codecov.io](https://codecov.io)
2. Log in with GitHub
3. Add your repository

### 2. Add Codecov Token

1. Copy the upload token from Codecov
2. Go to repository Settings > Secrets > Actions
3. Create new secret: `CODECOV_TOKEN`

### 3. Configure GitHub Actions

```yaml
# .github/workflows/tests.yml
- name: Run tests with coverage
  run: statatest tests/ --coverage --cov-report=lcov

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v5
  with:
    files: coverage.lcov
    token: ${{ secrets.CODECOV_TOKEN }}
```

## Codecov Configuration

Create `codecov.yml` in your repository root:

```yaml
# codecov.yml
coverage:
  precision: 2
  round: down
  range: "70...100"

  status:
    project:
      default:
        target: auto
        threshold: 1%

    patch:
      default:
        target: 80%

comment:
  layout: "reach,diff,flags,files"
  behavior: default
  require_changes: false
```

## PR Comments

Codecov automatically adds comments to pull requests showing:

- Coverage diff (lines added/removed)
- Coverage percentage change
- Uncovered lines in the patch
- File-by-file breakdown

Example PR comment:

```
## Coverage Report

| Coverage | Status |
|----------|--------|
| Project  | 85.3% (+0.5%) ✅ |
| Patch    | 92.1% ✅ |

### Files Changed

| File | Coverage | Lines |
|------|----------|-------|
| myfunction.ado | 90% | 18/20 |
| helper.ado | 75% | 15/20 |
```

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

## Coverage Targets

Set minimum coverage requirements:

```yaml
# codecov.yml
coverage:
  status:
    project:
      default:
        target: 80%  # Fail if below 80%
        threshold: 2%  # Allow 2% drop

    patch:
      default:
        target: 90%  # New code must have 90% coverage
```

## Badges

Add a coverage badge to your README:

```markdown
[![codecov](https://codecov.io/gh/username/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/username/repo)
```

## LCOV Format

statatest generates LCOV format coverage:

```
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
- `DA:line,hits`: Line coverage data
- `LF`: Lines found (total)
- `LH`: Lines hit (covered)

## Troubleshooting

### Coverage Not Uploading

1. Check token is correctly set
2. Verify LCOV file exists: `ls -la coverage.lcov`
3. Check Codecov action logs for errors

### Coverage Too Low

1. Add more tests covering edge cases
2. Use coverage HTML report to identify uncovered lines:
   ```bash
   statatest tests/ --coverage --cov-report=html
   open htmlcov/index.html
   ```

### Flaky Coverage

If coverage varies between runs:

1. Ensure tests are deterministic (use `fixture_seed`)
2. Check for conditional code paths
3. Use `carryforward: true` in flags
