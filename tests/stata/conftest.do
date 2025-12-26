// conftest.do
// Fixtures for Stata integration tests

// ============================================================================
// Fixture: sample_data
// Creates a simple dataset for testing
// ============================================================================

program define fixture_sample_data
    clear
    set obs 100
    gen id = _n
    gen group = mod(_n, 4) + 1
    gen value = rnormal(50, 10)
    gen str10 category = cond(group <= 2, "A", "B")
end

program define fixture_sample_data_teardown
    clear
end

// ============================================================================
// Fixture: panel_data
// Creates a simple panel dataset
// ============================================================================

program define fixture_panel_data
    clear
    set obs 200
    gen id = ceil(_n / 10)
    gen year = 2010 + mod(_n - 1, 10)
    gen value = rnormal(100, 20)
    xtset id year
end

program define fixture_panel_data_teardown
    clear
end

// ============================================================================
// Fixture: deterministic_seed
// Sets a reproducible random seed
// ============================================================================

program define fixture_deterministic_seed
    set seed 12345
end
