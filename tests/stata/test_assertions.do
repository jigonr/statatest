// test_assertions.do
// Tests for statatest assertion functions
// @marker: unit

clear all

// ============================================================================
// Test assert_equal
// ============================================================================

program define test_assert_equal_string
    local result = "success"
    assert_equal "`result'", expected("success")
end

program define test_assert_equal_numeric
    local value = 42
    assert_equal `value', expected(42)
end

program define test_assert_equal_with_message
    local status = "active"
    assert_equal "`status'", expected("active") message("Status should be active")
end

// ============================================================================
// Test assert_true and assert_false
// ============================================================================

program define test_assert_true_basic
    assert_true 1 == 1
    assert_true 5 > 3
    assert_true 10 >= 10
end

program define test_assert_false_basic
    assert_false 1 == 0
    assert_false 3 > 5
    assert_false 1 > 10
end

// ============================================================================
// Test assert_var_exists
// ============================================================================

program define test_assert_var_exists_basic
    clear
    set obs 10
    gen x = _n
    gen str10 name = "test"
    
    assert_var_exists x
    assert_var_exists name
end

// ============================================================================
// Test assert_obs_count
// ============================================================================

program define test_assert_obs_count_basic
    clear
    set obs 100
    gen x = _n
    
    assert_obs_count 100
end

program define test_assert_obs_count_with_if
    clear
    set obs 100
    gen x = _n
    gen group = mod(_n, 2)
    
    assert_obs_count 50 if group == 0
    assert_obs_count 50 if group == 1
end

// ============================================================================
// Test assert_approx_equal
// ============================================================================

program define test_assert_approx_equal_basic
    local pi = 3.14159
    assert_approx_equal `pi', expected(3.14) tol(0.01)
end

program define test_assert_approx_equal_regression
    clear
    set seed 12345
    set obs 100
    gen x = rnormal()
    gen y = 2*x + rnormal()
    
    regress y x
    
    // Coefficient should be approximately 2
    assert_approx_equal _b[x], expected(2) tol(0.5)
end

// ============================================================================
// Test assert_in_range
// ============================================================================

program define test_assert_in_range_basic
    local value = 50
    assert_in_range `value', min(0) max(100)
end

program define test_assert_in_range_r2
    clear
    set seed 12345
    set obs 100
    gen x = rnormal()
    gen y = 2*x + rnormal()
    
    regress y x
    
    // R-squared should be between 0 and 1
    assert_in_range e(r2), min(0) max(1)
end

// ============================================================================
// Test assert_error and assert_noerror
// ============================================================================

program define test_assert_error_basic
    // This command should fail (dropping non-existent variable)
    assert_error "drop nonexistent_variable_xyz"
end

program define test_assert_noerror_basic
    clear
    set obs 10
    gen x = _n
    
    // This command should succeed
    assert_noerror "summarize x"
end

// ============================================================================
// Test assert_file_exists
// ============================================================================

program define test_assert_file_exists_temp
    tempfile tf
    
    clear
    set obs 10
    gen x = _n
    save "`tf'", replace
    
    assert_file_exists "`tf'"
end

// ============================================================================
// Run all tests
// ============================================================================

test_assert_equal_string
test_assert_equal_numeric
test_assert_equal_with_message

test_assert_true_basic
test_assert_false_basic

test_assert_var_exists_basic

test_assert_obs_count_basic
test_assert_obs_count_with_if

test_assert_approx_equal_basic
test_assert_approx_equal_regression

test_assert_in_range_basic
test_assert_in_range_r2

test_assert_error_basic
test_assert_noerror_basic

test_assert_file_exists_temp

display as result "All assertion tests passed!"
