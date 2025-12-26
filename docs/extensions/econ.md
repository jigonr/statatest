# statatest[econ]

Economic data fixtures and assertions for panel data, networks, and accounting identities.

## Installation

```bash
pip install statatest[econ]
```

## Features

- **Panel Fixtures**: Balanced, unbalanced, and multilevel panels
- **Network Fixtures**: Production networks and bipartite employer-employee data
- **Economic Assertions**: Panel structure, uniqueness, accounting identities
- **gtools Integration**: Uses gisid, hashsort for performance on large datasets

---

## Panel Fixtures

### fixture_balanced_panel

Creates a balanced panel dataset (all units observed in all periods).

```stata
fixture_balanced_panel [, n_units(#) n_periods(#) start_year(#) seed(#)]
```

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `n_units` | 10 | Number of panel units |
| `n_periods` | 5 | Number of time periods |
| `start_year` | 2015 | Starting year |
| `seed` | 12345 | Random seed |

**Creates:** `id`, `year`, `value`

**Example:**

```stata
fixture_balanced_panel, n_units(100) n_periods(10)
assert_panel_structure id year, balanced
```

**Alias:** `fixture_firm_panel`

---

### fixture_unbalanced_panel

Creates an unbalanced panel with entry, exit, and gaps.

```stata
fixture_unbalanced_panel [, n_units(#) n_periods(#) start_year(#) ///
                            attrition(#) entry(#) seed(#)]
```

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `attrition` | 0.1 | Annual attrition rate (0-1) |
| `entry` | 0.05 | Annual entry rate (0-1) |

**Creates:** `id`, `year`, `value` (with gaps)

**Alias:** `fixture_unbalanced_firm_panel`

---

### fixture_multilevel_panel

Creates a hierarchical panel (e.g., country × firm × year).

```stata
fixture_multilevel_panel [, n_groups(#) n_units(#) n_periods(#) ///
                            start_year(#) seed(#)]
```

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `n_groups` | 5 | Number of top-level groups |
| `n_units` | 10 | Units per group |

**Creates:** `group_id`, `unit_id`, `year`, `panel_id`, `value`

**Aliases:** `fixture_country_firm_panel`, `fixture_industry_firm_panel`

---

## Network Fixtures

### fixture_production_network

Creates a sparse directed weighted network following Bernard & Zi (2022).

```stata
fixture_production_network [, n_firms(#) n_edges(#) temporal seed(#)]
```

**Structure:**

- ~31% only buyers, ~13% only sellers, ~56% both
- Log-normal transaction weights
- Directed edges (seller → buyer)

**Creates:** `seller`, `buyer`, `weight`, `year` (if temporal)

**Aliases:** `fixture_trade_network`, `fixture_supply_chain`

!!! note "Not Bipartite"
    Production networks are NOT bipartite—firms can be both buyers and sellers.

---

### fixture_bipartite_network

Creates a bipartite employer-employee network following AKM structure.

```stata
fixture_bipartite_network [, n_workers(#) n_firms(#) n_periods(#) ///
                             start_year(#) mobility(#) seed(#)]
```

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `n_workers` | 500 | Number of workers |
| `n_firms` | 50 | Number of firms |
| `mobility` | 0.15 | Job switching rate (0-1) |

**Structure:**

- Two distinct node types (workers ↔ firms)
- AKM wage decomposition: `log(wage) = worker_effect + firm_effect + residual`

**Creates:** `worker_id`, `firm_id`, `year`, `wage`

**Aliases:** `fixture_employer_employee`, `fixture_matched_panel`

---

## Assertions

### assert_unique

Check that variable combination uniquely identifies observations.

```stata
assert_unique varlist [if] [, by(varlist) message(string)]
```

Uses `gisid` internally for performance.

**Example:**

```stata
assert_unique id year
assert_unique seller buyer, by(year)
```

---

### assert_no_missing

Check that variables have no missing values.

```stata
assert_no_missing varlist [if] [, message(string)]
```

---

### assert_positive

Check that all values are positive.

```stata
assert_positive varname [if] [, strict message(string)]
```

**Options:**

- `strict`: Require `> 0` (default is `>= 0`)

---

### assert_sorted

Check that data is sorted by specified variables.

```stata
assert_sorted varlist [, message(string)]
```

Uses `hashsort` for verification if available.

---

### assert_panel_structure

Check that data has valid panel structure.

```stata
assert_panel_structure [panelvar timevar] [, balanced message(string)]
```

**Options:**

- `balanced`: Require all units have all periods

**Example:**

```stata
// Check current xtset
assert_panel_structure

// Check specific variables
assert_panel_structure id year, balanced
```

---

### assert_sum_equals

Check that sum equals expected value.

```stata
assert_sum_equals varname [if], expected(#) [tol(#) by(varlist) message(string)]
```

**Example:**

```stata
// Shares sum to 1
assert_sum_equals share, expected(1)

// Sum by group
assert_sum_equals weight, expected(100) by(group)
```

---

### assert_identity

Check accounting identity (row-wise equality).

```stata
assert_identity exp1 == exp2 [if] [, tol(#) message(string)]
```

**Example:**

```stata
assert_identity assets == liabilities + equity
assert_identity fob + freight + insurance == cif, tol(0.01)
```

---

## Full Example

```stata
// Create test data
fixture_balanced_panel, n_units(100) n_periods(5)

// Validate structure
assert_panel_structure id year, balanced
assert_unique id year
assert_sorted id year
assert_no_missing id year value
assert_positive value, strict

// Add derived variables
gen double share = value / 100
bysort year: egen double total = total(share)

// Check accounting
assert_sum_equals share, expected(1) by(year) tol(0.01)
```

---

## See Also

- [Econ Assertions Reference](../reference/econ-assertions.md)
- [Econ Fixtures Reference](../reference/econ-fixtures.md)
- [Core Assertions](../guide/assertions.md)
