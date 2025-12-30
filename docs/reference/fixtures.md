# Fixtures Reference

All fixtures available in statatest. All fixtures support `verbose` option for detailed output.

## Utility Fixtures

### fixture_seed

Sets a reproducible random seed.

```stata
fixture_seed [, seed(#) verbose]
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `seed` | 12345 | Random seed value |

**Example:**

```stata
fixture_seed, seed(42)
```

---

### fixture_tempfile

Creates a temporary file path.

```stata
fixture_tempfile, name(string) [verbose]
```

**Example:**

```stata
fixture_tempfile, name(mytemp)
// Now have `mytemp' containing temp file path
```

---

### fixture_empty_dataset

Creates an empty dataset with specified structure.

```stata
fixture_empty_dataset [, vars(string) verbose]
```

**Example:**

```stata
fixture_empty_dataset, vars("id year value")
```

---

### use_fixture

Load a fixture by name (convenience wrapper).

```stata
use_fixture fixture_name [, options]
```

**Example:**

```stata
use_fixture seed
use_fixture balanced_panel, n_units(100)
```

---

## Panel Fixtures

### fixture_balanced_panel

Creates a balanced panel dataset.

```stata
fixture_balanced_panel [, n_units(#) n_periods(#) start_year(#) seed(#) verbose]
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `n_units` | 10 | Number of panel units |
| `n_periods` | 5 | Number of time periods |
| `start_year` | 2015 | Starting year |
| `seed` | 12345 | Random seed |

**Creates:** `id`, `year`, `value`

**Side effects:** Sets `xtset id year`

**Example:**

```stata
fixture_balanced_panel, n_units(100) n_periods(10) verbose
assert_count, expected(1000)
```

---

### fixture_unbalanced_panel

Creates an unbalanced panel with entry, attrition, and gaps.

```stata
fixture_unbalanced_panel [, n_units(#) n_periods(#) start_year(#) ///
                            attrition(#) entry(#) seed(#) verbose]
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `n_units` | 20 | Number of panel units |
| `n_periods` | 10 | Number of time periods |
| `attrition` | 0.1 | Annual attrition rate (0-1) |
| `entry` | 0.05 | Annual entry rate (0-1) |

**Example:**

```stata
fixture_unbalanced_panel, n_units(50) attrition(0.15)
```

---

### fixture_multilevel_panel

Creates a hierarchical/multilevel panel.

```stata
fixture_multilevel_panel [, n_groups(#) n_units(#) n_periods(#) ///
                            start_year(#) seed(#) verbose]
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `n_groups` | 5 | Number of top-level groups |
| `n_units` | 10 | Units per group |
| `n_periods` | 5 | Time periods |

**Creates:** `group_id`, `unit_id`, `year`, `panel_id`, `value`

**Example:**

```stata
fixture_multilevel_panel, n_groups(10) n_units(20) n_periods(5)
// Creates 10 * 20 * 5 = 1000 observations
```

---

## Network Fixtures

### fixture_directed_network

Creates a sparse directed weighted network.

```stata
fixture_directed_network [, n_firms(#) n_edges(#) temporal seed(#) verbose]
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `n_firms` | 100 | Total number of firms |
| `n_edges` | 500 | Number of edges |
| `temporal` | off | Add year dimension |

**Creates:** `seller`, `buyer`, `weight` (and `year` if temporal)

**Example:**

```stata
fixture_directed_network, n_firms(200) n_edges(1000) temporal
```

---

### fixture_bipartite_network

Creates a bipartite employer-employee network.

```stata
fixture_bipartite_network [, n_workers(#) n_firms(#) n_periods(#) ///
                             start_year(#) mobility(#) seed(#) verbose]
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `n_workers` | 500 | Number of workers |
| `n_firms` | 50 | Number of firms |
| `n_periods` | 5 | Time periods |
| `mobility` | 0.15 | Job switching probability |

**Creates:** `worker_id`, `firm_id`, `year`, `wage`

**Example:**

```stata
fixture_bipartite_network, n_workers(1000) n_firms(100) mobility(0.2)
```

---

## See Also

- [Fixtures Guide](../guide/fixtures.md)
- [Assertions Reference](assertions.md)
- [Use Cases](../use-cases/panel-data.md)
