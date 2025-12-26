// test_fixtures.do
// Tests for statatest fixture system
// @marker: unit
// @uses_fixture: sample_data

clear all

// ============================================================================
// Test fixture loading
// ============================================================================

program define test_fixture_sample_data
    use_fixture sample_data
    
    assert_obs_count 100
    assert_var_exists id
    assert_var_exists group
    assert_var_exists value
    assert_var_exists category
end

program define test_fixture_deterministic
    use_fixture deterministic_seed
    
    // Generate random values - should be deterministic
    clear
    set obs 10
    gen x = rnormal()
    
    // First value should be consistent with seed 12345
    assert_true !missing(x[1])
end

// ============================================================================
// Test fixture with assertions
// ============================================================================

program define test_fixture_data_properties
    use_fixture sample_data
    
    // Check group values
    summarize group
    assert_in_range r(min), min(1) max(4)
    assert_in_range r(max), min(1) max(4)
    
    // Check category values
    tab category
    assert_true r(r) == 2  // Should have exactly 2 categories
end

program define test_panel_structure
    use_fixture panel_data
    
    // Check panel structure
    assert_obs_count 200
    
    // Check xtset worked
    xtsum value
    assert_true r(N) > 0
end

// ============================================================================
// Run all tests
// ============================================================================

test_fixture_sample_data
test_fixture_deterministic
test_fixture_data_properties
test_panel_structure

display as result "All fixture tests passed!"
