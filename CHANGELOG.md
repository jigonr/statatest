# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-12-30

### Added

- **Core Testing Framework**
  - Test discovery for `test_*.do` files with automatic test collection
  - Test runner with subprocess Stata execution
  - Support for markers (`// @marker: unit`) for test categorization
  - Support for keyword filtering (`-k` option) to run specific tests
  - JUnit XML report generation for CI systems integration
  - LCOV coverage report generation for Codecov integration

- **Assertion Library**
  - Basic assertions:
    - `assert_equal` - Value equality comparison
    - `assert_true` - Boolean true assertion
    - `assert_false` - Boolean false assertion
    - `assert_error` - Command should fail
    - `assert_noerror` - Command should succeed
  - Data validation assertions:
    - `assert_var_exists` - Variable existence check
    - `assert_file_exists` - File existence check
    - `assert_approx_equal` - Float comparison with tolerance
    - `assert_obs_count` - Observation count check (deprecated, see `assert_count`)
    - `assert_in_range` - Value range validation
    - `assert_unique` - ID uniqueness validation (uses `gisid` for performance)
    - `assert_no_missing` - No missing values check
    - `assert_positive` - All values positive check
    - `assert_sorted` - Sort order preservation (uses `hashsort`)
    - `assert_count` - Dataset observation count check
    - `assert_var_type` - Variable type validation (numeric, string, specific)
    - `assert_label_exists` - Variable has value labels attached
  - Economic/panel data assertions:
    - `assert_panel_structure` - Valid xtset with balanced option
    - `assert_sum_equals` - Sum equals expected with by-group support
    - `assert_identity` - Accounting identities validation (A + B == C)
  - `verbose` option for all assertions:
    - Default: Minimal one-line error messages
    - Verbose: Detailed multi-line diagnostic output

- **Fixture System**
  - pytest-like `conftest.do` pattern for test setup
  - Automatic `conftest.do` discovery in directory hierarchy
  - Fixture scoping: function, module, session
  - Built-in fixtures:
    - `use_fixture` - Request a fixture by name
    - `fixture_tempfile` - Temporary file path
    - `fixture_empty_dataset` - Empty dataset with optional observation count
    - `fixture_seed` - Reproducible random seed
  - Panel data fixtures:
    - `fixture_balanced_panel` - Balanced panel data
    - `fixture_unbalanced_panel` - Panel with attrition, entry, gaps
    - `fixture_multilevel_panel` - Hierarchical panel (group × unit × year)
  - Network fixtures:
    - `fixture_directed_network` - Sparse directed weighted network (formerly `fixture_production_network`)
    - `fixture_bipartite_network` - Two-mode network structure (AKM-style)
  - `verbose` option for all fixtures

- **Coverage System**
  - Coverage instrumentation module with SMCL comment markers for invisible tracking
  - Automatic instrumentation to `.statatest/instrumented/` directory
  - Line number mapping for accurate coverage reporting
  - Enhanced coverage module with `FileCoverage` and `CoverageReport` classes
  - HTML coverage report generation

- **Configuration & CLI**
  - Configuration via `statatest.toml` or `pyproject.toml`
  - CLI with Click:
    - `statatest <path>` - Run tests
    - `statatest --coverage` - Enable coverage
    - `statatest --junit-xml=<path>` - Generate JUnit XML
    - `statatest --init` - Create config template
  - Configuration system with OOP design and classmethod factory

- **Documentation**
  - `CONTRIBUTING.md` with contribution guidelines
  - README.md for all source modules (13 files)
  - MkDocs documentation website
  - Docker integration guide
  - Comprehensive troubleshooting guide
  - Codecov integration guide with multi-CI support
  - Economic extensions documentation
  - Use case documentation (panel data, network data)

- **Development & CI/CD**
  - GitHub Actions CI/CD workflows
  - GitHub Action for zero-install testing
  - Scheduled Stata integration tests in CI
  - Pre-commit hooks
  - 90+ Python tests with 90%+ coverage
  - Logging module (`core/logging.py`) with ANSI color support

### Changed

- Package structure reorganization: moved ado files to `statatest/ado/`
- Centralized all constants in `core/constants.py`
- Replaced `rich` library with Python standard logging + ANSI colors for better compatibility
- Merged `[econ]` extension into main package (no separate install needed)
- Merged econ documentation into main reference (removed extensions section)
- Updated MkDocs navigation with Use Cases section
- Improved path handling with `importlib.resources`
- Configuration system: replaced lambdas with `__post_init__` for better maintainability
- Configuration system: OOP redesign with classmethod factory pattern
- Fixtures module: moved `fixtures.py` to `fixtures/` module for better organization
- Coverage module: moved `instrument.py` to `coverage/` module for better organization
- Executor: improved Stata invocation to match documented usage
- Network fixture: renamed `fixture_production_network` to `fixture_directed_network` for clarity
- Corrected network terminology in econ fixtures
- CI dependency updates:
  - `actions/download-artifact` from 4 to 7
  - `astral-sh/setup-uv` from 4 to 7
  - `actions/upload-pages-artifact` from 3 to 4
  - `actions/setup-python` from 5 to 6
  - `DavidAnson/markdownlint-cli2-action` from 18 to 22

### Fixed

- Coverage: wired up instrumentation in CLI to enable coverage tracking
- Coverage: fixed instrumentation to properly capture COV markers
- Executor: improved Stata invocation to match documented usage patterns
- Econ fixtures: correct network terminology and add AKM bipartite fixture

### Removed

- `rich` dependency (replaced with standard library for reduced dependencies)
- `[econ]` optional extra (all features now included by default)
- `adopath_mode` configuration option (simplified configuration)
- Outdated adopath settings comment in executor

[Unreleased]: https://github.com/jigonr/statatest/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/jigonr/statatest/releases/tag/v0.1.0
