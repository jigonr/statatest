# Network Data Use Cases

How to use statatest fixtures for testing network analysis with modern Stata
tools.

## Prerequisites

```stata
ssc install reghdfe
ssc install ftools
ssc install gtools
ssc install ppmlhdfe
```

## Production Networks (Directed)

### Testing Supply Chain Metrics

```stata
program define test_network_metrics
    // Create directed network
    fixture_directed_network, n_firms(200) n_edges(1000) seed(42)

    // Compute in-degree (number of suppliers)
    gegen n_suppliers = count(seller), by(buyer)

    // Compute out-degree (number of customers)
    gegen n_customers = count(buyer), by(seller)

    // Compute weighted degree
    gegen total_purchases = total(weight), by(buyer)
    gegen total_sales = total(weight), by(seller)

    // Verify network properties
    assert_no_missing n_suppliers n_customers
    assert_positive total_purchases
    assert_positive total_sales

    // Check degree distribution (power law approximation)
    summarize n_suppliers
    assert_true r(max) > 3 * r(mean)  // Fat tail
end
```

### Testing Network Regressions

```stata
program define test_network_regression
    fixture_directed_network, n_firms(100) n_edges(500) temporal

    // Generate firm characteristics
    preserve
    keep seller
    duplicates drop
    gen seller_size = exp(rnormal())
    tempfile sellers
    save `sellers'
    restore

    merge m:1 seller using `sellers', nogen

    // Gravity-style regression on network
    gen log_weight = log(weight)
    gen log_size = log(seller_size)

    reghdfe log_weight log_size, absorb(buyer year) vce(cluster seller)

    assert_true e(N) > 0
    assert_true _b[log_size] != 0
end
```

## Trade Networks (Gravity Models)

### Testing PPML Gravity Estimation

```stata
program define test_ppml_gravity
    // Bilateral trade network
    fixture_directed_network, n_firms(50) n_edges(500) temporal

    // Rename for trade context
    rename seller exporter
    rename buyer importer
    rename weight trade_value

    // Generate gravity variables
    preserve
    keep exporter
    duplicates drop
    gen exporter_gdp = exp(2 + rnormal())
    tempfile exp_data
    save `exp_data'
    restore

    merge m:1 exporter using `exp_data', nogen

    preserve
    keep importer
    duplicates drop
    gen importer_gdp = exp(2 + rnormal())
    tempfile imp_data
    save `imp_data'
    restore

    merge m:1 importer using `imp_data', nogen

    // PPML with exporter-year and importer-year FE
    ppmlhdfe trade_value exporter_gdp importer_gdp, ///
        absorb(exporter#year importer#year) d

    assert_true e(converged) == 1
    assert_true e(N) > 100
end
```

### Testing Zero Trade Flows

```stata
program define test_zero_flows
    fixture_directed_network, n_firms(30) n_edges(200)

    // Expand to full matrix (including zeros)
    preserve
    keep seller
    duplicates drop
    rename seller i
    cross using (keep buyer, duplicates drop, rename buyer j)
    tempfile full_matrix
    save `full_matrix'
    restore

    rename seller i
    rename buyer j
    merge 1:1 i j using `full_matrix'
    replace weight = 0 if _merge == 2
    drop _merge

    // Count zeros
    count if weight == 0
    local n_zeros = r(N)
    count if weight > 0
    local n_positive = r(N)

    // Sparse network: many zeros
    assert_true `n_zeros' > `n_positive'

    // PPML handles zeros
    ppmlhdfe weight, absorb(i j)
    assert_true e(N) == _N  // Uses all obs including zeros
end
```

## Employer-Employee Networks (AKM)

### Testing AKM Data Structure

```stata
program define test_akm_structure
    fixture_bipartite_network, n_workers(1000) n_firms(100) ///
        n_periods(5) mobility(0.2) seed(42)

    // Verify bipartite structure
    assert_unique worker_id year
    assert_no_missing worker_id firm_id year wage

    // Check mobility (needed for identification)
    bysort worker_id (year): gen switched = firm_id != firm_id[_n-1] if _n > 1
    gegen ever_switched = max(switched), by(worker_id)

    summarize ever_switched
    assert_true r(mean) > 0.1, message("Need mobility for AKM identification")

    // Verify wage structure
    gen log_wage = log(wage)
    assert_no_missing log_wage
    assert_positive wage, strict
end
```

### Testing AKM Estimation with reghdfe

```stata
program define test_akm_estimation
    fixture_bipartite_network, n_workers(500) n_firms(50) ///
        n_periods(5) mobility(0.25)

    gen log_wage = log(wage)

    // AKM: log(wage) = worker_FE + firm_FE + Xb + e
    // Generate experience
    bysort worker_id (year): gen experience = _n - 1
    gen exp_sq = experience^2

    // Estimate AKM
    reghdfe log_wage experience exp_sq, ///
        absorb(worker_fe=worker_id firm_fe=firm_id) ///
        vce(cluster firm_id)

    // Check estimation
    assert_true e(N) > 0
    assert_true e(df_a) > 50  // Absorbed many FE

    // Experience should have positive return
    assert_true _b[experience] > 0

    // Verify FE were estimated
    assert_var_exists worker_fe
    assert_var_exists firm_fe
end
```

### Testing Connected Set

```stata
program define test_connected_set
    fixture_bipartite_network, n_workers(500) n_firms(50) n_periods(5)

    // Find largest connected set
    // (Workers connected if they share a firm)

    // Create worker-firm incidence
    preserve
    keep worker_id firm_id
    duplicates drop

    // Simple connectivity check via firm
    gegen n_workers_per_firm = count(worker_id), by(firm_id)
    gegen n_firms_per_worker = count(firm_id), by(worker_id)

    // Most workers should be in firms with multiple workers
    summarize n_workers_per_firm
    assert_true r(mean) > 5, message("Firms too small for AKM")

    restore
end
```

## Matching Markets (Bipartite)

### Testing Two-Sided Market

```stata
program define test_matching_market
    fixture_bipartite_network, n_workers(200) n_firms(50) ///
        n_periods(1) mobility(0)

    // One period = static matching
    // Rename for market context
    rename worker_id buyer_id
    rename firm_id seller_id
    rename wage price

    // Market concentration
    gegen seller_share = count(buyer_id), by(seller_id)
    replace seller_share = seller_share / _N

    // HHI calculation
    gen seller_share_sq = seller_share^2
    gegen hhi = total(seller_share_sq)

    // Check market structure
    summarize hhi
    assert_in_range r(mean), min(0) max(1)
end
```

## Network Formation

### Testing Link Prediction Setup

```stata
program define test_link_data
    fixture_directed_network, n_firms(100) n_edges(300)

    // Create potential links (dyadic data)
    preserve
    keep seller
    duplicates drop
    gen i = seller
    cross using (keep buyer, duplicates drop, rename buyer j)
    drop if i == j  // No self-loops
    tempfile dyads
    save `dyads'
    restore

    // Merge actual links
    gen i = seller
    gen j = buyer
    gen linked = 1

    merge 1:1 i j using `dyads'
    replace linked = 0 if _merge == 2
    drop _merge seller buyer

    // Verify dyadic structure
    assert_unique i j

    // Check link density
    summarize linked
    local density = r(mean)
    assert_in_range `density', min(0.01) max(0.5)
end
```

## Common Pitfalls

### 1. Confusing Directed vs Bipartite

```stata
// DIRECTED: Same node type, asymmetric edges
// Firm A sells to Firm B (A→B ≠ B→A)
fixture_directed_network  // seller → buyer

// BIPARTITE: Two node types, edges between types only
// Worker employed at Firm (workers never employ workers)
fixture_bipartite_network  // worker ↔ firm
```

### 2. Self-Loops in Network Data

```stata
program define test_no_self_loops
    fixture_directed_network, n_firms(50) n_edges(200)

    // Verify no firm trades with itself
    assert_true seller != buyer
end
```

### 3. Duplicate Edges

```stata
program define test_no_duplicate_edges
    fixture_directed_network, n_firms(50) n_edges(200)

    // Check uniqueness
    assert_unique seller buyer
end
```

### 4. Ignoring Network Sparsity

```stata
program define test_sparsity
    fixture_directed_network, n_firms(100) n_edges(500)

    // Potential edges: 100 * 99 = 9900
    // Actual edges: 500
    // Density: ~5%

    local n_firms = 100
    local potential = `n_firms' * (`n_firms' - 1)
    local density = _N / `potential'

    display "Network density: " %5.3f `density'
    assert_true `density' < 0.1, message("Network too dense")
end
```

## See Also

- [Fixtures Reference](../reference/fixtures.md)
- [Panel Data Use Cases](panel-data.md)
- [reghdfe documentation](http://scorreia.com/software/reghdfe/)
- [ppmlhdfe documentation](http://scorreia.com/software/ppmlhdfe/)
