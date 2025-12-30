# Network Data Use Cases

How to use statatest fixtures for testing network analysis.

## Production Networks (Directed)

### Supply Chain Analysis

```stata
program define test_supply_chain
    // Create directed network (suppliers → buyers)
    fixture_directed_network, n_firms(200) n_edges(1000)
    
    // Verify structure
    assert_var_exists seller
    assert_var_exists buyer
    assert_var_exists weight
    
    // Test network is directed (not symmetric)
    gen edge_id = seller * 10000 + buyer
    gen reverse_id = buyer * 10000 + seller
    
    merge 1:1 edge_id using (network data), keep(1 3)
    // Some edges should NOT have reverse
    assert_true _merge == 1 in some observations
end
```

### Temporal Networks

```stata
program define test_temporal_network
    // Network over time
    fixture_directed_network, n_firms(100) n_edges(500) temporal
    
    // Has year dimension
    assert_var_exists year
    
    // Test panel operations on network
    bysort seller buyer (year): gen relationship_age = _n
    
    // First year of each relationship
    assert_true relationship_age == 1 if year == 2015
end
```

## Trade Networks (Weighted)

### International Trade

```stata
program define test_trade_flows
    // Directed weighted network
    fixture_directed_network, n_firms(50) n_edges(200)
    
    // Rename for trade context
    rename seller exporter
    rename buyer importer
    rename weight trade_value
    
    // Test gravity-style analysis
    gen log_trade = log(trade_value)
    assert_positive trade_value, strict
    
    // Compute network statistics
    bysort exporter: egen total_exports = total(trade_value)
    bysort importer: egen total_imports = total(trade_value)
end
```

## Employer-Employee Networks (Bipartite)

### AKM-Style Analysis

```stata
program define test_akm_data
    // Bipartite: workers ↔ firms
    fixture_bipartite_network, n_workers(1000) n_firms(100) mobility(0.2)
    
    // Verify bipartite structure
    assert_var_exists worker_id
    assert_var_exists firm_id
    assert_var_exists wage
    
    // Workers and firms are distinct
    assert_unique worker_id year
    
    // Test wage decomposition setup
    gen log_wage = log(wage)
    assert_no_missing log_wage
    
    // Verify some mobility (for identification)
    bysort worker_id (year): gen changed_firm = firm_id != firm_id[_n-1] if _n > 1
    summarize changed_firm
    assert_true r(mean) > 0.1  // At least 10% mobility
end
```

### Connected Sets

```stata
program define test_connected_set
    fixture_bipartite_network, n_workers(500) n_firms(50) n_periods(5)
    
    // Find largest connected set
    // (Your connected set algorithm here)
    
    // Test that connected workers share common firm
    bysort firm_id: gen firm_workers = _N
    assert_true firm_workers > 1  // Firms have multiple workers
end
```

## Buyer-Seller Matching

### Two-Sided Markets

```stata
program define test_matching
    // Bipartite matching market
    fixture_bipartite_network, n_workers(200) n_firms(50)
    
    // Rename for market context
    rename worker_id buyer_id
    rename firm_id seller_id
    
    // Test matching properties
    bysort buyer_id: gen n_sellers = _N
    bysort seller_id: gen n_buyers = _N
    
    // Market thickness
    assert_true n_sellers >= 1
    assert_true n_buyers >= 1
end
```

## Common Pitfalls

### 1. Confusing Directed vs Bipartite

```stata
// Directed: Same node type, edges have direction
// A can sell to B, B can sell to A
fixture_directed_network  // seller → buyer

// Bipartite: Two node types, edges between types only
// Workers at firms (workers can't employ workers)
fixture_bipartite_network  // worker ↔ firm
```

### 2. Not Testing Sparsity

```stata
// Real networks are sparse
fixture_directed_network, n_firms(1000) n_edges(2000)
// Only 0.2% of possible edges exist

// Test your code handles sparsity
assert_true _N < n_firms^2
```

### 3. Ignoring Self-Loops

```stata
// Check no firm trades with itself
assert_true seller != buyer
```

## See Also

- [Fixtures Reference](../reference/fixtures.md)
- [Panel Data Use Cases](panel-data.md)
