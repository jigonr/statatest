# Panel Data Use Cases

How to use statatest fixtures for testing panel data analysis with modern Stata
tools.

## Prerequisites

These examples use high-performance packages. Install via:

```stata
ssc install reghdfe
ssc install ftools
ssc install gtools
ssc install ivreghdfe
ssc install ppmlhdfe
```

## Fixed Effects Estimation with reghdfe

### Testing Two-Way Fixed Effects

```stata
program define test_twoway_fe
    // Setup balanced panel
    fixture_balanced_panel, n_units(100) n_periods(10) seed(42)

    // Generate outcome with unit and time effects
    gen unit_fe = id * 0.1
    gen time_fe = year * 0.05
    gen y = 0.5 * value + unit_fe + time_fe + rnormal() * 0.1

    // Run reghdfe (absorbs high-dimensional FE)
    reghdfe y value, absorb(id year) vce(cluster id)

    // Assertions
    assert_true e(N) == 1000
    assert_in_range _b[value], min(0.45) max(0.55)
    assert_true e(df_a) > 100  // Many absorbed FE
end
```

### Testing Multiway Clustering

```stata
program define test_multiway_clustering
    fixture_multilevel_panel, n_groups(20) n_units(50) n_periods(5)

    // Generate outcome
    gen y = value + rnormal()

    // Two-way clustered standard errors
    reghdfe y value, absorb(unit_id year) vce(cluster group_id unit_id)

    // SE should be larger with two-way clustering
    local se_twoway = _se[value]

    reghdfe y value, absorb(unit_id year) vce(cluster unit_id)
    local se_oneway = _se[value]

    assert_true `se_twoway' >= `se_oneway'
end
```

## High-Performance Operations with gtools

### Testing Large Panel Operations

```stata
program define test_gtools_performance
    // Large panel for performance testing
    fixture_balanced_panel, n_units(1000) n_periods(20) seed(123)

    // Use gtools for fast operations
    gegen mean_value = mean(value), by(id)
    gegen sd_value = sd(value), by(id)
    gegen n_obs = count(value), by(id)

    // Verify aggregations
    assert_no_missing mean_value sd_value n_obs
    assert_true n_obs == 20  // All units have 20 periods

    // Fast sorting
    hashsort id year
    assert_sorted id year
end
```

### Testing Panel Lags with gtools

```stata
program define test_panel_lags
    fixture_balanced_panel, n_units(100) n_periods(10)

    // Fast panel operations
    xtset id year
    gegen lag_value = shift(value), by(id) shiftby(-1)
    gegen lead_value = shift(value), by(id) shiftby(1)
    gegen diff_value = diff(value), by(id)

    // Verify lag structure
    assert_true missing(lag_value) if year == 2015
    assert_true !missing(lag_value) if year > 2015
end
```

## Instrumental Variables with ivreghdfe

### Testing IV Estimation

```stata
program define test_iv_estimation
    fixture_balanced_panel, n_units(200) n_periods(5) seed(42)

    // Generate endogenous variable and instrument
    gen z = rnormal()  // Instrument
    gen x = 0.7 * z + 0.3 * rnormal()  // Endogenous
    gen y = 0.5 * x + value * 0.1 + rnormal()

    // IV regression with fixed effects
    ivreghdfe y value (x = z), absorb(id year) first

    // Check first stage F-statistic (weak instruments)
    assert_true e(widstat) > 10, message("Weak instrument: F < 10")

    // Check coefficient is in expected range
    assert_in_range _b[x], min(0.3) max(0.7)
end
```

## Gravity Models with ppmlhdfe

### Testing Trade Flow Estimation

```stata
program define test_gravity_model
    // Create bilateral panel (origin-destination-year)
    fixture_multilevel_panel, n_groups(30) n_units(30) n_periods(5)

    // Rename for gravity context
    rename group_id origin
    rename unit_id destination

    // Generate trade flows (count data with zeros)
    gen trade = exp(2 + 0.5 * value + rnormal()) * (runiform() > 0.3)
    replace trade = round(trade)

    // PPML with high-dimensional FE
    ppmlhdfe trade value, absorb(origin#year destination#year) d

    // Verify estimation
    assert_true e(N) > 0
    assert_true e(converged) == 1
end
```

## Unbalanced Panels

### Testing with Entry and Exit

```stata
program define test_unbalanced_estimation
    fixture_unbalanced_panel, n_units(200) n_periods(10) ///
        attrition(0.15) entry(0.08)

    // Verify unbalanced structure
    bysort id: gen n_periods = _N
    summarize n_periods
    assert_true r(min) < r(max)  // Different coverage

    // Estimation should handle gaps
    gen y = 0.5 * value + rnormal()
    reghdfe y value, absorb(id year) vce(cluster id)

    assert_true e(N) < 2000  // Less than balanced
    assert_true e(N) > 1000  // But substantial
end
```

### Testing Selection Correction

```stata
program define test_selection
    fixture_unbalanced_panel, n_units(300) n_periods(8) attrition(0.2)

    // Selection indicator
    gen observed = 1

    // Test for selection on observables
    gegen mean_value_first = mean(value) if year == 2010, by(id)
    gegen mean_value_first_all = max(mean_value_first), by(id)

    bysort id (year): gen exits = year == year[_N] & year < 2017

    // Exiters vs stayers comparison
    // (In real test, would run selection model)
    assert_var_exists mean_value_first_all
end
```

## Common Pitfalls

### 1. Forgetting to Set Panel Structure

```stata
// BAD: Operations fail silently
gen lag = L.value  // Returns missing!

// GOOD: Verify panel is set
xtset id year
assert_panel_structure
gen lag = L.value
```

### 2. Singleton Observations

```stata
program define test_handles_singletons
    fixture_unbalanced_panel, n_units(100) n_periods(5) attrition(0.3)

    // reghdfe drops singletons automatically
    gen y = value + rnormal()
    reghdfe y value, absorb(id year)

    // Check how many dropped
    assert_true e(N) <= _N
    display "Dropped " (_N - e(N)) " singletons"
end
```

### 3. Not Testing Clustered SEs

```stata
program define test_clustering_matters
    fixture_balanced_panel, n_units(50) n_periods(20)

    // Generate serially correlated errors
    gen e = 0
    bysort id (year): replace e = 0.8 * e[_n-1] + rnormal() if _n > 1
    gen y = value + e

    // Unclustered SE (wrong)
    reghdfe y value, absorb(id) vce(robust)
    local se_robust = _se[value]

    // Clustered SE (correct)
    reghdfe y value, absorb(id) vce(cluster id)
    local se_cluster = _se[value]

    // Clustered should be larger with serial correlation
    assert_true `se_cluster' > `se_robust'
end
```

## See Also

- [Fixtures Reference](../reference/fixtures.md)
- [Network Data Use Cases](network-data.md)
- [reghdfe documentation](http://scorreia.com/software/reghdfe/)
- [gtools documentation](https://gtools.readthedocs.io/)
