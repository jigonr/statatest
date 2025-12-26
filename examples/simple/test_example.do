// test_example.do - Simple example test file
//
// Run with: statatest examples/simple/
//
// @marker: unit

clear all

// Test 1: Basic data generation
program define test_data_generation
    clear
    set obs 100
    gen x = _n
    gen y = x * 2

    assert_obs_count 100
    assert_var_exists x
    assert_var_exists y
    assert_true _N == 100
end

// Test 2: Summary statistics
program define test_summary_stats
    sysuse auto, clear

    summarize price
    assert_true r(N) > 0
    assert_true r(mean) > 0
    assert_in_range r(mean), min(1000) max(20000)
end

// Test 3: Regression
program define test_regression
    sysuse auto, clear

    regress price mpg
    assert_true e(N) > 0
    assert_true e(r2) >= 0
    assert_true e(r2) <= 1
end

// Run all tests
test_data_generation
test_summary_stats
test_regression

display "All tests passed!"
