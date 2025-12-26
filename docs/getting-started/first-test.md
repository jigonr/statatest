# Writing Your First Test

## Test File Structure

A statatest test file is a regular Stata `.do` file with some conventions:

```stata
// tests/test_myfunction.do

// Markers for filtering (optional)
// @marker: unit

// Clear state
clear all

// Define test programs
program define test_something
    // Setup
    clear
    set obs 100
    gen x = rnormal()

    // Action
    myfunction x, gen(y)

    // Assert
    assert_var_exists y
    assert_obs_count 100
end

// Run the test
test_something

display "All tests passed!"
```

## Test Naming Convention

- Test files: `test_*.do`
- Test programs: `test_*` (optional but recommended)

## Basic Assertions

```stata
// Value equality
assert_equal "`r(result)'", expected("expected_value")

// Boolean assertions
assert_true _N > 0
assert_false missing(x)

// Variable checks
assert_var_exists myvar
assert_obs_count 100

// Numeric comparisons
assert_approx_equal r(mean), expected(0.5) tol(0.01)
assert_in_range r(sd), min(0) max(10)

// Command behavior
assert_error "invalid_command"
assert_noerror "summarize x"

// File checks
assert_file_exists "data/output.dta"
```

## Using Markers

Markers help organize and filter tests:

```stata
// @marker: unit
// @marker: slow
// @marker: integration
```

Run only specific markers:

```bash
statatest tests/ -m unit
statatest tests/ -m "not slow"
```

## Using Fixtures

For reusable setup, use `conftest.do`:

```stata
// tests/conftest.do

program define fixture_sample_data
    clear
    set obs 100
    gen x = rnormal()
    gen y = x * 2 + rnormal()
end
```

```stata
// tests/test_analysis.do
// @uses_fixture: sample_data

program define test_correlation
    use_fixture sample_data
    correlate x y
    assert_true r(rho) > 0.5
end
```

## Running Tests

```bash
# Run all tests
statatest tests/

# Run specific file
statatest tests/test_myfunction.do

# Run with keyword filter
statatest tests/ -k "regression"

# Verbose output
statatest tests/ --verbose
```
