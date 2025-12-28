"""Constants and configuration defaults for statatest.

This module centralizes all magic numbers and default values to:
1. Make them easy to find and modify
2. Prevent duplication across modules
3. Enable configuration override in the future
"""

from __future__ import annotations

# =============================================================================
# Test Execution
# =============================================================================

#: Default timeout for a single test file (seconds)
DEFAULT_TIMEOUT_SECONDS: int = 300

#: Default Stata executable name
DEFAULT_STATA_EXECUTABLE: str = "stata-mp"

# =============================================================================
# Coverage Thresholds
# =============================================================================

#: Coverage percentage considered "high" (green in reports)
COVERAGE_HIGH_THRESHOLD: int = 80

#: Coverage percentage considered "medium" (yellow in reports)
COVERAGE_MEDIUM_THRESHOLD: int = 50

# =============================================================================
# Test Discovery
# =============================================================================

#: Default paths to search for tests
DEFAULT_TEST_PATHS: list[str] = ["tests"]

#: Default patterns for test file names
DEFAULT_TEST_FILE_PATTERNS: list[str] = ["test_*.do"]

# =============================================================================
# Output Markers (for parsing test results)
# =============================================================================

#: Marker pattern for passed assertions in Stata output
ASSERTION_PASSED_PREFIX: str = "_STATATEST_PASS_:"
ASSERTION_PASSED_SUFFIX: str = "_"

#: Marker pattern for failed assertions in Stata output
ASSERTION_FAILED_PREFIX: str = "_STATATEST_FAIL_:"
ASSERTION_FAILED_SUFFIX: str = "_END_"

# =============================================================================
# Coverage Markers (for SMCL log parsing)
# =============================================================================

#: SMCL comment format for coverage markers
#: Format: {* COV:filename:lineno }
COVERAGE_MARKER_FORMAT: str = "{{* COV:{filename}:{lineno} }}"

# =============================================================================
# Report Defaults
# =============================================================================

#: Default LCOV output filename
DEFAULT_LCOV_FILENAME: str = "coverage.lcov"

#: Default HTML coverage output directory
DEFAULT_HTML_COV_DIR: str = "htmlcov"

#: Default JUnit XML output filename
DEFAULT_JUNIT_FILENAME: str = "junit.xml"

# =============================================================================
# Error Message Truncation
# =============================================================================

#: Maximum length for error messages (characters)
ERROR_MESSAGE_MAX_LENGTH: int = 200
