# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-12-26

### Added

- Initial release
- Test discovery for `test_*.do` files
- Test runner with subprocess Stata execution
- Assertion library:
  - `assert_equal` - Value equality
  - `assert_true` - Boolean true
  - `assert_false` - Boolean false
  - `assert_error` - Command should fail
  - `assert_noerror` - Command should succeed
  - `assert_var_exists` - Variable existence
  - `assert_file_exists` - File existence
  - `assert_approx_equal` - Float comparison with tolerance
  - `assert_obs_count` - Observation count check
  - `assert_in_range` - Value range check
- JUnit XML report generation for CI systems
- LCOV coverage report generation for Codecov
- Configuration via `statatest.toml` or `pyproject.toml`
- CLI with Click:
  - `statatest <path>` - Run tests
  - `statatest --coverage` - Enable coverage
  - `statatest --junit-xml=<path>` - Generate JUnit XML
  - `statatest --init` - Create config template
- GitHub Actions CI/CD workflow
- Support for markers (`// @marker: unit`)
- Support for keyword filtering (`-k` option)

[Unreleased]: https://github.com/jigonr/statatest/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/jigonr/statatest/releases/tag/v0.1.0
