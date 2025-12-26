*! fixture_tempfile v1.0.0  statatest  2025-12-26
*! Author: Jose Ignacio Gonzalez Rojas
*!
*! Built-in fixture: Creates a temporary file path.
*!
*! After calling this fixture, the global $fixture_tempfile_path
*! contains the path to a temporary file that will be cleaned up
*! after the test.
*!
*! Syntax:
*!   fixture_tempfile [, scope(string) suffix(string)]
*!
*! Example:
*!   use_fixture tempfile
*!   save "$fixture_tempfile_path", replace

program define fixture_tempfile, rclass
    version 16

    syntax [, Scope(string) SUFfix(string)]

    // Default suffix is .dta
    if `"`suffix'"' == "" {
        local suffix ".dta"
    }

    // Generate temporary file path
    tempfile tmpfile
    local filepath "`tmpfile'`suffix'"

    // Store in global for access
    global fixture_tempfile_path "`filepath'"

    // Store for cleanup tracking
    global _FIXTURE_tempfile_cleanup "`filepath'"

    return local path "`filepath'"
end

program define fixture_tempfile_teardown
    // Clean up temporary file if it exists
    capture confirm file "$_FIXTURE_tempfile_cleanup"
    if _rc == 0 {
        erase "$_FIXTURE_tempfile_cleanup"
    }

    // Clear globals
    global fixture_tempfile_path
    global _FIXTURE_tempfile_cleanup

    // Clear fixture marker
    capture scalar drop _FIXTURE_tempfile

    // Emit marker
    noisily display "_STATATEST_FIXTURE_:teardown_:tempfile_END_"
end
