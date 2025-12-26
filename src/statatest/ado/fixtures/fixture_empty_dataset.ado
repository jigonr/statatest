*! fixture_empty_dataset v1.0.0  statatest  2025-12-26
*! Author: Jose Ignacio Gonzalez Rojas
*!
*! Built-in fixture: Creates an empty dataset with specified observations.
*!
*! Syntax:
*!   fixture_empty_dataset [, scope(string) obs(integer)]
*!
*! Example:
*!   use_fixture empty_dataset
*!   // Now have empty dataset with 0 observations
*!
*!   fixture_empty_dataset, obs(100)
*!   // Now have empty dataset with 100 observations

program define fixture_empty_dataset, rclass
    version 16

    syntax [, Scope(string) OBS(integer 0)]

    // Clear current data
    clear

    // Set observations if specified
    if `obs' > 0 {
        quietly set obs `obs'
    }

    return local obs "`obs'"
end

program define fixture_empty_dataset_teardown
    // Clear data
    clear

    // Clear fixture marker
    capture scalar drop _FIXTURE_empty_dataset

    // Emit marker
    noisily display "_STATATEST_FIXTURE_:teardown_:empty_dataset_END_"
end
