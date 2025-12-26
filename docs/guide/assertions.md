# Assertions

statatest provides a rich assertion library built on Stata's native `assert`
command, with detailed failure messages.

## Available Assertions

### assert_equal

Check that two values are equal.

```stata
assert_equal actual, expected(value) [message(str)]
```

**Example:**

```stata
summarize x
assert_equal "`r(N)'", expected("100")
assert_equal "`r(mean)'", expected("0.5") message("Mean should be 0.5")
```

### assert_true

Check that a condition is true.

```stata
assert_true condition
```

**Example:**

```stata
assert_true _N > 0
assert_true r(mean) > 0
assert_true inlist("`region'", "EU", "GB")
```

### assert_false

Check that a condition is false.

```stata
assert_false condition
```

**Example:**

```stata
assert_false _N == 0
assert_false missing(x)
```

### assert_var_exists

Check that a variable exists in the dataset.

```stata
assert_var_exists varname [, type(str)]
```

**Example:**

```stata
assert_var_exists x
assert_var_exists firm_id, type(numeric)
assert_var_exists name, type(string)
```

### assert_obs_count

Check the number of observations.

```stata
assert_obs_count expected [if] [, message(str)]
```

**Example:**

```stata
assert_obs_count 100
assert_obs_count 50 if foreign == 1
```

### assert_approx_equal

Check that two numbers are approximately equal (for floating point).

```stata
assert_approx_equal value, expected(num) [tol(num)] [message(str)]
```

**Example:**

```stata
assert_approx_equal r(mean), expected(0.5) tol(0.01)
assert_approx_equal e(r2), expected(0.85) tol(0.05)
```

### assert_in_range

Check that a value is within a range.

```stata
assert_in_range value, min(num) max(num) [message(str)]
```

**Example:**

```stata
assert_in_range r(mean), min(0) max(100)
assert_in_range e(r2), min(0) max(1)
```

### assert_error

Check that a command produces an error.

```stata
assert_error "command"
```

**Example:**

```stata
assert_error "drop nonexistent_var"
assert_error "regress y"  // Missing independent variables
```

### assert_noerror

Check that a command executes without error.

```stata
assert_noerror "command"
```

**Example:**

```stata
assert_noerror "summarize x"
assert_noerror "regress y x"
```

### assert_file_exists

Check that a file exists.

```stata
assert_file_exists "path/to/file"
```

**Example:**

```stata
assert_file_exists "data/output.dta"
assert_file_exists "$HOME/config.txt"
```

## Failure Messages

All assertions provide detailed failure messages:

```
ASSERTION FAILED: assert_equal
  Expected: 100
  Actual:   99
  Message:  Observation count mismatch
```

## Custom Messages

Add context to failures with the `message()` option:

```stata
assert_equal "`r(N)'", expected("100") message("Sample size after filtering")
assert_true e(r2) > 0.5, message("R-squared should be above 0.5")
```
