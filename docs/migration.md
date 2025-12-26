# Migration Guide

Migrate existing Stata test patterns to statatest.

## From Manual Testing

### Before

```stata
// test_analysis.do
clear all

// Test 1: Check data loading
use "data/sample.dta", clear
local test_pass = 1
if _N != 100 {
    display as error "FAIL: Expected 100 observations"
    local test_pass = 0
}
if "`test_pass'" == "1" {
    display as result "PASS: Data loading"
}

// Test 2: Check variable exists
capture confirm variable revenue
if _rc != 0 {
    display as error "FAIL: revenue variable missing"
}
```

### After

```stata
// tests/test_analysis.do
// @marker: unit

clear all

program define test_data_loading
    use "data/sample.dta", clear
    assert_obs_count 100
end

program define test_variable_exists
    use "data/sample.dta", clear
    assert_var_exists revenue
end

test_data_loading
test_variable_exists

display "All tests passed!"
```

## From Perfect Match Pattern

### Before (30+ lines per test)

```stata
// tests/unit/test_configure_region.do
local tests_run = 0
local tests_passed = 0
local tests_failed = 0
local all_test_results ""

// Test 1: EU region configuration
local tests_run = `tests_run' + 1
configure_region EU
local test_pass = 1
if "`r(region)'" != "EU" {
    display as error "  FAIL: r(region) = `r(region)', expected EU"
    local test_pass = 0
}
if "`r(deflator)'" != "IIPI" {
    display as error "  FAIL: r(deflator) = `r(deflator)', expected IIPI"
    local test_pass = 0
}
if `test_pass' == 1 {
    local tests_passed = `tests_passed' + 1
    local all_test_results "`all_test_results'P"
    display as result "  PASS"
}
else {
    local tests_failed = `tests_failed' + 1
    local all_test_results "`all_test_results'F"
}
```

### After (3-5 lines per test)

```stata
// tests/unit/test_configure_region.do
// @marker: unit

clear all

program define test_eu_region
    configure_region EU
    assert_equal "`r(region)'", expected("EU")
    assert_equal "`r(deflator)'", expected("IIPI")
end

program define test_gb_region
    configure_region GB
    assert_equal "`r(region)'", expected("GB")
    assert_equal "`r(deflator)'", expected("IIPI")
end

test_eu_region
test_gb_region

display "All tests passed!"
```

## Key Changes

### 1. Use Assertions

Replace manual checks with assertions:

| Before | After |
|--------|-------|
| `if _N != 100 { ... }` | `assert_obs_count 100` |
| `capture confirm variable x` | `assert_var_exists x` |
| `if r(mean) != 0.5 { ... }` | `assert_equal "`r(mean)'"`, expected("0.5")` |
| `if abs(r(mean) - 0.5) > 0.01 { ... }` | `assert_approx_equal r(mean), expected(0.5) tol(0.01)` |

### 2. Use Fixtures

Replace repeated setup with fixtures:

```stata
// tests/conftest.do
program define fixture_sample_panel
    clear
    set obs 100
    gen int firm_id = ceil(_n / 10)
    gen int year = 2010 + mod(_n, 10)
    gen double revenue = exp(rnormal(15, 2))
end
```

```stata
// tests/test_analysis.do
// @uses_fixture: sample_panel

program define test_panel_structure
    use_fixture sample_panel
    assert_obs_count 100
    assert_var_exists firm_id
end
```

### 3. Use Markers

Replace file organization with markers:

```stata
// @marker: unit
// @marker: slow
// @marker: integration
```

Run specific markers:

```bash
statatest tests/ -m "unit"
statatest tests/ -m "not slow"
```

### 4. Run from CLI

Replace manual execution:

```bash
# Before
stata-mp -b do tests/run_all_tests.do

# After
statatest tests/
```

## Migration Steps

### Step 1: Install statatest

```bash
pip install statatest
```

### Step 2: Create Configuration

```bash
statatest --init
```

### Step 3: Convert Test Files

1. Keep test file naming (`test_*.do`)
2. Replace manual checks with assertions
3. Add markers for organization
4. Extract common setup to fixtures

### Step 4: Create conftest.do

```stata
// tests/conftest.do
program define fixture_sample_data
    clear
    // Common setup code
end
```

### Step 5: Run Tests

```bash
statatest tests/ --verbose
```

### Step 6: Add Coverage

```bash
statatest tests/ --coverage --cov-report=lcov
```

### Step 7: Update CI

```yaml
# .github/workflows/tests.yml
- run: pip install statatest
- run: statatest tests/ --junit-xml=junit.xml --coverage --cov-report=lcov
```

## Compatibility

statatest maintains backward compatibility:

- Tests without assertions still work (pass if no error)
- Existing test file structure preserved
- Manual counting still possible alongside assertions

## Gradual Migration

Migrate incrementally:

1. Start with `statatest` CLI (no code changes)
2. Add assertions to new tests
3. Migrate existing tests file by file
4. Add fixtures as patterns emerge
5. Enable coverage
