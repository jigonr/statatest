*! assert_panel_structure.ado
*! Version 1.0.0
*! Assert that data has valid panel structure (xtset)
*!
*! Syntax:
*!   assert_panel_structure [panelvar timevar] [, balanced message(string)]
*!
*! Options:
*!   balanced      - Require balanced panel (all units have all periods)
*!   message(str)  - Custom error message
*!
*! If panelvar and timevar not specified, checks current xtset.
*!
*! Examples:
*!   assert_panel_structure                    // Check current xtset
*!   assert_panel_structure id year            // Check specific variables
*!   assert_panel_structure id year, balanced  // Require balanced panel

program define assert_panel_structure
    version 16
    
    syntax [varlist(min=0 max=2)] [, balanced message(string)]
    
    local nvars : word count `varlist'
    
    if `nvars' == 0 {
        // Check current xtset
        capture xtset
        if _rc != 0 {
            display as error ""
            display as error "ASSERTION FAILED: assert_panel_structure"
            display as error "  Data is not xtset"
            if "`message'" != "" {
                display as error "  Message: `message'"
            }
            exit 9
        }
        local panelvar = r(panelvar)
        local timevar = r(timevar)
    }
    else if `nvars' == 1 {
        display as error "Must specify both panelvar and timevar, or neither"
        exit 198
    }
    else {
        local panelvar : word 1 of `varlist'
        local timevar : word 2 of `varlist'
        
        // Try to xtset with these variables
        capture xtset `panelvar' `timevar'
        if _rc != 0 {
            display as error ""
            display as error "ASSERTION FAILED: assert_panel_structure"
            display as error "  Cannot xtset with: `panelvar' `timevar'"
            display as error "  Error code: `=_rc'"
            if "`message'" != "" {
                display as error "  Message: `message'"
            }
            exit 9
        }
    }
    
    // Check for uniqueness using gisid if available
    capture which gisid
    if _rc == 0 {
        capture gisid `panelvar' `timevar'
    }
    else {
        capture isid `panelvar' `timevar'
    }
    
    if _rc != 0 {
        display as error ""
        display as error "ASSERTION FAILED: assert_panel_structure"
        display as error "  Panel variables: `panelvar' `timevar'"
        display as error "  Not uniquely identified (duplicates exist)"
        if "`message'" != "" {
            display as error "  Message: `message'"
        }
        exit 9
    }
    
    // Check for balanced panel if requested
    if "`balanced'" != "" {
        quietly xtset
        local panel_id = r(panelvar)
        local time_id = r(timevar)
        
        // Count observations per panel unit
        tempvar n_periods_per_unit
        bysort `panel_id': gen `n_periods_per_unit' = _N
        
        // Get expected number of periods
        quietly summarize `time_id'
        local expected_periods = r(max) - r(min) + 1
        
        // Check if all units have same number of periods
        quietly summarize `n_periods_per_unit'
        if r(min) != r(max) | r(min) != `expected_periods' {
            display as error ""
            display as error "ASSERTION FAILED: assert_panel_structure"
            display as error "  Panel is NOT balanced"
            display as error "  Expected periods per unit: `expected_periods'"
            display as error "  Actual range: `=r(min)' to `=r(max)'"
            if "`message'" != "" {
                display as error "  Message: `message'"
            }
            exit 9
        }
    }
end
