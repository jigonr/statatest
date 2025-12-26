# Core Assertions Reference

Built-in assertions available in the base statatest package.

## assert_equal

Check that two values are equal.

```stata
assert_equal value, expected(expected_value) [message(string)]
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `value` | Yes | Actual value to test |
| `expected()` | Yes | Expected value |
| `message()` | No | Custom error message |

**Example:**

```stata
local result = "success"
assert_equal "`result'", expected("success")
```

---

## assert_true

Check that expression evaluates to true (non-zero).

```stata
assert_true expression [, message(string)]
```

**Example:**

```stata
assert_true 1 == 1
assert_true `r(N)' > 0
```

---

## assert_false

Check that expression evaluates to false (zero).

```stata
assert_false expression [, message(string)]
```

**Example:**

```stata
assert_false 1 == 0
assert_false missing(`r(mean)')
```

---

## assert_error

Check that a command produces an error.

```stata
assert_error "command_string"
```

**Example:**

```stata
assert_error "drop nonexistent_variable"
```

---

## assert_noerror

Check that a command executes without error.

```stata
assert_noerror "command_string"
```

**Example:**

```stata
assert_noerror "summarize x"
```

---

## assert_var_exists

Check that a variable exists in the dataset.

```stata
assert_var_exists varname [, message(string)]
```

**Example:**

```stata
assert_var_exists id
assert_var_exists wage, message("Wage variable required")
```

---

## assert_file_exists

Check that a file exists on disk.

```stata
assert_file_exists "filepath" [, message(string)]
```

**Example:**

```stata
assert_file_exists "data/input.dta"
```

---

## assert_approx_equal

Check that two numeric values are approximately equal.

```stata
assert_approx_equal value, expected(#) [tol(#) message(string)]
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `tol()` | 1e-6 | Tolerance for comparison |

**Example:**

```stata
assert_approx_equal `r(mean)', expected(0.5) tol(0.01)
```

---

## assert_obs_count

Check that observation count matches expected.

```stata
assert_obs_count # [if] [, message(string)]
```

**Example:**

```stata
assert_obs_count 100
assert_obs_count 50 if group == 1
```

---

## assert_in_range

Check that value is within specified range.

```stata
assert_in_range value, min(#) max(#) [message(string)]
```

**Example:**

```stata
assert_in_range `r(r2)', min(0) max(1)
```

---

## See Also

- [Assertions Guide](../guide/assertions.md)
- [Econ Assertions](econ-assertions.md) (requires `[econ]` extension)
