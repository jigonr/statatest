*! assert_equal v1.0.0  statatest  2025-12-26
*! Author: Jose Ignacio Gonzalez Rojas
*!
*! Assert that two values are equal.
*!
*! Syntax:
*!   assert_equal actual, expected(value) [message(string)]
*!
*! Example:
*!   assert_equal "`r(N)'", expected("100")
*!   assert_equal `x', expected(5) message("x should be 5")

program define assert_equal, rclass
    version 16

    syntax anything(name=actual), Expected(string) [Message(string)]

    // Use capture assert to test equality
    capture assert `"`actual'"' == `"`expected'"'

    if _rc == 9 {
        display as error "ASSERTION FAILED: assert_equal"
        display as error "  Expected: `expected'"
        display as error "  Actual:   `actual'"
        if `"`message'"' != "" {
            display as error "  Message:  `message'"
        }
        // Emit failure marker for Python to parse
        noisily display "_STATATEST_FAIL_:assert_equal_:`actual' != `expected'_END_"
        exit 9
    }
    else if _rc != 0 {
        error _rc  // Propagate unexpected errors
    }

    // Emit success marker for Python to parse
    noisily display "_STATATEST_PASS_:assert_equal_"

    return local passed "1"
end
