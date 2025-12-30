# Panel Data Use Cases

How to use statatest fixtures for testing panel data analysis.

## Firm-Year Panels (Economics)

### Setup

```stata
// Create test data
fixture_balanced_panel, n_units(100) n_periods(10)

// Verify structure
assert_panel_structure id year, balanced
assert_count, expected(1000)
```

### Testing Regressions

```stata
program define test_fe_regression
    // Setup
    fixture_balanced_panel, n_units(50) n_periods(5) seed(42)
    
    // Generate dependent variable
    gen y = 0.5 * value + rnormal()
    
    // Run your estimation code
    xtreg y value, fe
    
    // Assertions
    assert_true e(N) == 250
    assert_in_range _b[value], min(0.4) max(0.6)
end
```

## Patient-Visit Panels (Healthcare)

### Unbalanced Panel with Attrition

```stata
program define test_patient_data
    // Healthcare data often has dropout
    fixture_unbalanced_panel, n_units(500) attrition(0.2) entry(0.05)
    
    // Rename for domain clarity
    rename id patient_id
    rename year visit_date
    
    // Test your analysis handles missingness
    assert_no_missing patient_id visit_date
    
    // Test panel operations work
    xtset patient_id visit_date
    gen lag_value = L.value
    assert_true !missing(lag_value) if _n > 1 & patient_id == patient_id[_n-1]
end
```

## User-Session Panels (Tech)

### Multilevel Structure

```stata
program define test_user_sessions
    // Users nested in companies
    fixture_multilevel_panel, n_groups(20) n_units(50) n_periods(12)
    
    // Rename for domain
    rename group_id company_id
    rename unit_id user_id
    rename year month
    
    // Verify hierarchy
    bysort company_id user_id: gen user_obs = _N
    assert_true user_obs == 12  // All users have 12 months
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

### 2. Not Testing Edge Cases

```stata
program define test_edge_cases
    // Test with minimal data
    fixture_balanced_panel, n_units(2) n_periods(2)
    
    // Your code should still work
    your_estimation_command
    assert_noerror "your_estimation_command"
end
```

### 3. Hardcoding Observation Counts

```stata
// BAD: Brittle test
assert _N == 1000

// GOOD: Use fixture parameters
fixture_balanced_panel, n_units(10) n_periods(5)
assert_count, expected(50)  // 10 * 5 = 50
```

## See Also

- [Fixtures Reference](../reference/fixtures.md)
- [Network Data Use Cases](network-data.md)
