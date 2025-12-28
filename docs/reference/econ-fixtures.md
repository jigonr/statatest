# Econ Fixtures Reference

Fixtures for economic data structures. Requires `pip install statatest[econ]`.

## Panel Fixtures

### fixture_balanced_panel

Creates a balanced panel dataset.

```stata
fixture_balanced_panel [, n_units(#) n_periods(#) start_year(#) seed(#)]
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `n_units` | 10 | Number of panel units |
| `n_periods` | 5 | Number of time periods |
| `start_year` | 2015 | Starting year |
| `seed` | 12345 | Random seed for reproducibility |

**Creates:**

| Variable | Type | Description |
|----------|------|-------------|
| `id` | int | Panel unit identifier (1 to n_units) |
| `year` | int | Time period |
| `value` | double | Random normal (mean=100, sd=20) |

**Returns:**

- `r(n_units)` - Number of units
- `r(n_periods)` - Number of periods
- `r(n_obs)` - Total observations

**Side effects:** Sets `xtset id year`

**Alias:** `fixture_firm_panel`

---

### fixture_unbalanced_panel

Creates an unbalanced panel with entry, attrition, and gaps.

```stata
fixture_unbalanced_panel [, n_units(#) n_periods(#) start_year(#) ///
                            attrition(#) entry(#) seed(#)]
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `n_units` | 20 | Number of panel units |
| `n_periods` | 10 | Number of time periods |
| `start_year` | 2010 | Starting year |
| `attrition` | 0.1 | Annual attrition rate (0-1) |
| `entry` | 0.05 | Annual entry rate (0-1) |
| `seed` | 12345 | Random seed |

**Creates:** `id`, `year`, `value` (with gaps)

**Alias:** `fixture_unbalanced_firm_panel`

---

### fixture_multilevel_panel

Creates a hierarchical/multilevel panel.

```stata
fixture_multilevel_panel [, n_groups(#) n_units(#) n_periods(#) ///
                            start_year(#) seed(#)]
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `n_groups` | 5 | Number of top-level groups |
| `n_units` | 10 | Units per group |
| `n_periods` | 5 | Time periods |
| `start_year` | 2015 | Starting year |
| `seed` | 12345 | Random seed |

**Creates:**

| Variable | Type | Description |
|----------|------|-------------|
| `group_id` | int | Top-level group (e.g., country) |
| `unit_id` | int | Unit within group (e.g., firm) |
| `year` | int | Time period |
| `panel_id` | long | Unique panel identifier |
| `value` | double | Value with group and unit effects |

**Aliases:** `fixture_country_firm_panel`, `fixture_industry_firm_panel`

---

## Network Fixtures

### fixture_directed_network

Creates a sparse directed weighted network.

```stata
fixture_directed_network [, n_firms(#) n_edges(#) temporal seed(#)]
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `n_firms` | 100 | Total number of firms |
| `n_edges` | 500 | Number of edges |
| `temporal` | off | Add year dimension (2015-2019) |
| `seed` | 12345 | Random seed |

**Creates:**

| Variable | Type | Description |
|----------|------|-------------|
| `seller` | int | Seller firm ID (source node) |
| `buyer` | int | Buyer firm ID (target node) |
| `weight` | double | Transaction value (log-normal) |
| `year` | int | Year (if `temporal` specified) |

**Network Properties (Bernard & Zi 2022):**

- ~31% only buyers
- ~13% only sellers
- ~56% both buyers and sellers
- Directed: seller → buyer
- Weighted: log-normal transaction values
- **NOT bipartite**: firms can be both

**Aliases:** `fixture_trade_network`, `fixture_supply_chain`

---

### fixture_bipartite_network

Creates a bipartite employer-employee network (AKM structure).

```stata
fixture_bipartite_network [, n_workers(#) n_firms(#) n_periods(#) ///
                             start_year(#) mobility(#) seed(#)]
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `n_workers` | 500 | Number of workers |
| `n_firms` | 50 | Number of firms |
| `n_periods` | 5 | Time periods |
| `start_year` | 2015 | Starting year |
| `mobility` | 0.15 | Job switching probability (0-1) |
| `seed` | 12345 | Random seed |

**Creates:**

| Variable | Type | Description |
|----------|------|-------------|
| `worker_id` | int | Worker identifier |
| `firm_id` | int | Firm identifier |
| `year` | int | Year |
| `wage` | double | Wage (AKM structure) |

**AKM Structure:**

```
log(wage) = worker_effect + firm_effect + experience + residual
```

- Worker effects: N(0, 0.3)
- Firm effects: N(0, 0.2)
- Experience: 2% return per year
- Residual: N(0, 0.15)

**Bipartite Property:** Two distinct node types; edges only between workers and firms.

**Aliases:** `fixture_employer_employee`, `fixture_matched_panel`

---

## See Also

- [statatest[econ] Guide](../extensions/econ.md)
- [Econ Assertions Reference](econ-assertions.md)
- [Core Fixtures](../guide/fixtures.md)
