// conftest.do - Shared fixtures for test examples
//
// This file defines fixtures that can be used across multiple tests.
// Fixtures are loaded automatically before tests run.

// Custom fixture: Creates a sample panel dataset
program define fixture_sample_panel
    syntax [, scope(string)]

    clear
    set obs 100

    // Generate panel structure
    gen int firm_id = ceil(_n / 10)
    bysort firm_id: gen int year = 2010 + _n - 1

    // Generate variables
    gen double revenue = exp(rnormal(15, 2))
    gen double employees = exp(rnormal(3, 1))
    gen double capital = exp(rnormal(10, 2))

    // Label variables
    label variable firm_id "Firm identifier"
    label variable year "Year"
    label variable revenue "Revenue (nominal)"
    label variable employees "Number of employees"
    label variable capital "Capital stock"
end

program define fixture_sample_panel_teardown
    clear
    capture scalar drop _FIXTURE_sample_panel
    noisily display "_STATATEST_FIXTURE_:teardown_:sample_panel_END_"
end
