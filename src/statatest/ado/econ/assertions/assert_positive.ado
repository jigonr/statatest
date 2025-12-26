*! assert_positive.ado
*! Version 1.0.0
*! Assert that all values of a variable are positive
*!
*! Syntax:
*!   assert_positive varname [if] [, strict message(string)]
*!
*! Options:
*!   strict        - Require strictly positive (> 0), not just non-negative
*!   message(str)  - Custom error message
*!
*! Examples:
*!   assert_positive sales
*!   assert_positive wage, strict message("Wages must be positive")
*!   assert_positive revenue if year >= 2015

program define assert_positive
    version 16
    
    syntax varname [if] [, strict message(string)]
    
    marksample touse
    
    // Check for missing values first
    quietly count if missing(`varlist') & `touse'
    if r(N) > 0 {
        display as error ""
        display as error "ASSERTION FAILED: assert_positive"
        display as error "  Variable: `varlist'"
        display as error "  Found `r(N)' missing values"
        if "`message'" != "" {
            display as error "  Message: `message'"
        }
        exit 9
    }
    
    // Check for non-positive values
    if "`strict'" != "" {
        // Strictly positive: > 0
        quietly count if `varlist' <= 0 & `touse'
        local condition "<= 0"
    }
    else {
        // Non-negative by default: >= 0
        quietly count if `varlist' < 0 & `touse'
        local condition "< 0"
    }
    
    if r(N) > 0 {
        display as error ""
        display as error "ASSERTION FAILED: assert_positive"
        display as error "  Variable: `varlist'"
        display as error "  Found `r(N)' values `condition'"
        if "`message'" != "" {
            display as error "  Message: `message'"
        }
        
        // Show summary of problematic values
        display as error ""
        display as error "  Summary of non-positive values:"
        if "`strict'" != "" {
            summarize `varlist' if `varlist' <= 0 & `touse', detail
        }
        else {
            summarize `varlist' if `varlist' < 0 & `touse', detail
        }
        
        exit 9
    }
end
