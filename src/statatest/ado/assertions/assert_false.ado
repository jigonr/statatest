*! assert_false v1.0.0  statatest  2025-12-26
*! Author: Jose Ignacio Gonzalez Rojas
*!
*! Assert that a condition evaluates to false.
*!
*! Syntax:
*!   assert_false condition [, message(string)]
*!
*! Example:
*!   assert_false missing(x)
*!   assert_false `x' < 0, message("x should not be negative")

program define assert_false, rclass
    version 16

    syntax anything(name=condition) [, Message(string)]

    // Use capture assert to test that condition is false (NOT condition is true)
    capture assert !(`condition')

    if _rc == 9 {
        display as error "ASSERTION FAILED: assert_false"
        display as error "  Condition: `condition'"
        display as error "  Evaluated: true (expected false)"
        if `"`message'"' != "" {
            display as error "  Message:   `message'"
        }
        // Emit failure marker
        noisily display "_STATATEST_FAIL_:assert_false_:`condition' is true_END_"
        exit 9
    }
    else if _rc != 0 {
        error _rc
    }

    // Emit success marker
    noisily display "_STATATEST_PASS_:assert_false_"

    return local passed "1"
end
