# Econ Assertions Reference

Assertions for economic data validation. Requires `pip install statatest[econ]`.

## assert_unique

Check that variable combination uniquely identifies observations.

```stata
assert_unique varlist [if] [, by(varlist) message(string)]
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `varlist` | Yes | Variables that should uniquely identify |
| `by()` | No | Check uniqueness within groups |
| `message()` | No | Custom error message |

**Performance:** Uses `gisid` if available.

**Examples:**

```stata
assert_unique id year
assert_unique seller buyer, by(year)
assert_unique worker_id firm_id year
```

---

## assert_no_missing

Check that variables have no missing values.

```stata
assert_no_missing varlist [if] [, message(string)]
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
assert_positive varname [if] [, strict message(string)]
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `strict` | off | If specified, requires `> 0`; otherwise `>= 0` |

**Examples:**

```stata
assert_positive sales
assert_positive wage, strict message("Wages must be positive")
```

---

## assert_sorted

Check that data is sorted by specified variables.

```stata
assert_sorted varlist [, message(string)]
```

**Performance:** Uses `hashsort` for verification if available.

**Example:**

```stata
assert_sorted id year
assert_sorted seller buyer year
```

---

## assert_panel_structure

Check that data has valid panel structure (xtset).

```stata
assert_panel_structure [panelvar timevar] [, balanced message(string)]
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `panelvar timevar` | No | If omitted, checks current xtset |
| `balanced` | No | Require all units have all periods |

**Checks:**

1. Data can be xtset with specified variables
2. No duplicate panel-time combinations
3. (If `balanced`) All units observed in all periods

**Examples:**

```stata
// Check current xtset
xtset id year
assert_panel_structure

// Check and set specific variables
assert_panel_structure id year

// Require balanced panel
assert_panel_structure id year, balanced
```

---

## assert_sum_equals

Check that sum of variable equals expected value.

```stata
assert_sum_equals varname [if], expected(#) [tol(#) by(varlist) message(string)]
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `expected()` | Required | Expected sum value |
| `tol()` | 1e-10 | Tolerance for comparison |
| `by()` | None | Check sum within each group |

**Examples:**

```stata
// Shares sum to 1
assert_sum_equals share, expected(1)

// With tolerance
assert_sum_equals weight, expected(100) tol(0.01)

// By group
assert_sum_equals market_share, expected(1) by(industry year)
```

---

## assert_identity

Check accounting identity (row-wise equality).

```stata
assert_identity exp1 == exp2 [if] [, tol(#) message(string)]
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `tol()` | 1e-10 | Tolerance for numeric comparison |

**Examples:**

```stata
// Balance sheet identity
assert_identity assets == liabilities + equity

// Trade costs
assert_identity fob + freight + insurance == cif, tol(0.01)

// Income statement
assert_identity revenue - costs == profit if year == 2020
```

---

## See Also

- [statatest[econ] Guide](../extensions/econ.md)
- [Econ Fixtures Reference](econ-fixtures.md)
- [Core Assertions](assertions.md)
