*! assert_error v1.0.0  statatest  2025-12-26
*! Author: Jose Ignacio Gonzalez Rojas
*!
*! Assert that a command produces an error.
*!
*! Syntax:
*!   assert_error "command" [, rc(integer) message(string)]
*!
*! Example:
*!   assert_error "use nonexistent_file.dta"
*!   assert_error "gen x = invalid", rc(198)

program define assert_error, rclass
    version 16

    syntax anything(name=command) [, RC(integer 0) Message(string)]

    // Execute the command and capture the return code
    capture `command'
    local actual_rc = _rc

    if `actual_rc' == 0 {
        display as error "ASSERTION FAILED: assert_error"
        display as error "  Command:  `command'"
        display as error "  Expected: error"
        display as error "  Actual:   no error (rc=0)"
        if `"`message'"' != "" {
            display as error "  Message:  `message'"
        }
        // Emit failure marker
        noisily display "_STATATEST_FAIL_:assert_error_:command did not fail_END_"
        exit 9
    }

    // If specific rc requested, check it
    if `rc' != 0 & `actual_rc' != `rc' {
        display as error "ASSERTION FAILED: assert_error"
        display as error "  Command:  `command'"
        display as error "  Expected: rc=`rc'"
        display as error "  Actual:   rc=`actual_rc'"
        if `"`message'"' != "" {
            display as error "  Message:  `message'"
        }
        // Emit failure marker
        noisily display "_STATATEST_FAIL_:assert_error_:wrong rc `actual_rc' != `rc'_END_"
        exit 9
    }

    // Emit success marker
    noisily display "_STATATEST_PASS_:assert_error_"

    return local passed "1"
    return local rc "`actual_rc'"
end
