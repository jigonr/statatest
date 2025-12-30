# Assertions Reference

All assertions available in statatest. All assertions support `verbose` option for detailed output.

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

## assert_count

Check that dataset has expected number of observations.

```stata
assert_count, expected(#) [if] [message(string) verbose]
```

**Example:**

```stata
assert_count, expected(100)
assert_count if group == 1, expected(50)
```

---

## assert_var_type

Check that variable has expected type.

```stata
assert_var_type varname, type(string) [message(string) verbose]
```

**Type options:** `numeric`, `string`, `byte`, `int`, `long`, `float`, `double`, `str#`

**Example:**

```stata
assert_var_type price, type("numeric")
assert_var_type name, type("string")
```

---

## assert_label_exists

Check that variable has value labels attached.

```stata
assert_label_exists varname [, message(string) verbose]
```

**Example:**

```stata
assert_label_exists foreign
```

---

## assert_unique

Check that variable combination uniquely identifies observations.

```stata
assert_unique varlist [if] [, by(varlist) message(string) verbose]
```

**Example:**

```stata
assert_unique id year
assert_unique seller buyer, by(year)
```

---

## assert_no_missing

Check that variables have no missing values.

```stata
assert_no_missing varlist [if] [, message(string) verbose]
```

**Example:**

```stata
assert_no_missing id year value
assert_no_missing wage if year >= 2015
```

---

## assert_positive

Check that all values are positive.

```stata
assert_positive varname [if] [, strict message(string) verbose]
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `strict` | off | If specified, requires `> 0`; otherwise `>= 0` |

**Example:**

```stata
assert_positive sales
assert_positive wage, strict
```

---

## assert_sorted

Check that data is sorted by specified variables.

```stata
assert_sorted varlist [, message(string) verbose]
```

**Example:**

```stata
assert_sorted id year
```

---

## assert_panel_structure

Check that data has valid panel structure.

```stata
assert_panel_structure [panelvar timevar] [, balanced message(string) verbose]
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `panelvar timevar` | No | If omitted, checks current xtset |
| `balanced` | No | Require all units have all periods |

**Example:**

```stata
xtset id year
assert_panel_structure
assert_panel_structure id year, balanced
```

---

## assert_sum_equals

Check that sum of variable equals expected value.

```stata
assert_sum_equals varname [if], expected(#) [tol(#) by(varlist) message(string) verbose]
```

**Example:**

```stata
assert_sum_equals share, expected(1)
assert_sum_equals market_share, expected(1) by(industry year)
```

---

## assert_identity

Check accounting identity (row-wise equality).

```stata
assert_identity exp1 == exp2 [if] [, tol(#) message(string) verbose]
```

**Example:**

```stata
assert_identity assets == liabilities + equity
assert_identity revenue - costs == profit
```

---

## See Also

- [Assertions Guide](../guide/assertions.md)
- [Fixtures Reference](fixtures.md)
