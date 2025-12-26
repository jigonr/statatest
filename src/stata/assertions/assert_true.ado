*! assert_true v1.0.0  statatest  2025-12-26
*! Author: Jose Ignacio Gonzalez Rojas
*!
*! Assert that a condition evaluates to true.
*!
*! Syntax:
*!   assert_true condition [, message(string)]
*!
*! Example:
*!   assert_true _N > 0
*!   assert_true `x' > 5, message("x should be greater than 5")

program define assert_true, rclass
    version 16

    syntax anything(name=condition) [, Message(string)]

    // Use capture assert to test condition
    capture assert `condition'

    if _rc == 9 {
        display as error "ASSERTION FAILED: assert_true"
        display as error "  Condition: `condition'"
        display as error "  Evaluated: false"
        if `"`message'"' != "" {
            display as error "  Message:   `message'"
        }
        // Emit failure marker
        noisily display "_STATATEST_FAIL_:assert_true_:`condition' is false_END_"
        exit 9
    }
    else if _rc != 0 {
        error _rc
    }

    // Emit success marker
    noisily display "_STATATEST_PASS_:assert_true_"

    return local passed "1"
end
