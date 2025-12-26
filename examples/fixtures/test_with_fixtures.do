// test_with_fixtures.do - Example test using fixtures
//
// Run with: statatest examples/fixtures/
//
// @marker: unit
// @uses_fixture: sample_panel

clear all

// Test 1: Sample panel has expected structure
program define test_panel_structure
    // Load the fixture
    use_fixture sample_panel

    // Check observations
    assert_obs_count 100

    // Check variables exist
    assert_var_exists firm_id
    assert_var_exists year
    assert_var_exists revenue
    assert_var_exists employees
    assert_var_exists capital
end

// Test 2: Panel has 10 firms
program define test_firm_count
    use_fixture sample_panel

    // Count unique firms
    quietly distinct firm_id
    assert_equal "`r(ndistinct)'", expected("10") message("Should have 10 firms")
end

// Test 3: Each firm has 10 years
program define test_years_per_firm
    use_fixture sample_panel

    // Check balanced panel
    bysort firm_id: gen n_years = _N
    assert_true n_years[1] == 10
end

// Test 4: Variables are positive
program define test_positive_values
    use_fixture sample_panel

    // All values should be positive
    assert_true revenue > 0
    assert_true employees > 0
    assert_true capital > 0
end

// Test 5: Use built-in seed fixture for reproducibility
program define test_with_seed
    // Use seed fixture for reproducible random numbers
    fixture_seed, seed(42)

    clear
    set obs 10
    gen x = rnormal()

    // First value should be consistent with seed 42
    assert_true _N == 10
end

// Run all tests
test_panel_structure
test_firm_count
test_years_per_firm
test_positive_values
test_with_seed

display "All fixture tests passed!"
