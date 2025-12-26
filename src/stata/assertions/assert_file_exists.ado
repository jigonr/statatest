*! assert_file_exists v1.0.0  statatest  2025-12-26
*! Author: Jose Ignacio Gonzalez Rojas
*!
*! Assert that a file exists at the specified path.
*!
*! Syntax:
*!   assert_file_exists "path" [, message(string)]
*!
*! Example:
*!   assert_file_exists "data/input.dta"
*!   assert_file_exists "`c(sysdir_plus)'ado/base/r/regress.ado"

program define assert_file_exists, rclass
    version 16

    syntax anything(name=filepath) [, Message(string)]

    // Remove quotes if present
    local filepath = subinstr(`"`filepath'"', `"""', "", .)

    // Check if file exists
    capture confirm file `"`filepath'"'

    if _rc != 0 {
        display as error "ASSERTION FAILED: assert_file_exists"
        display as error "  File:    `filepath'"
        display as error "  Status:  does not exist"
        if `"`message'"' != "" {
            display as error "  Message: `message'"
        }
        // Emit failure marker
        noisily display "_STATATEST_FAIL_:assert_file_exists_:`filepath' not found_END_"
        exit 601
    }

    // Emit success marker
    noisily display "_STATATEST_PASS_:assert_file_exists_"

    return local passed "1"
end
