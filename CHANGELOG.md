# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- New assertions:
  - `assert_count` - Check dataset observation count
  - `assert_var_type` - Check variable type (numeric, string, specific)
  - `assert_label_exists` - Check variable has value labels attached
- `verbose` option for all assertions and fixtures:
  - Default: Minimal one-line error messages
  - Verbose: Detailed multi-line diagnostic output
- Documentation:
  - `CONTRIBUTING.md` with contribution guidelines
  - README.md for all source modules (13 files)
  - Use case documentation (panel data, network data)
- Panel data fixtures (merged from econ extension):
  - `fixture_balanced_panel` - Balanced panel data
  - `fixture_unbalanced_panel` - Panel with attrition, entry, gaps
  - `fixture_multilevel_panel` - Hierarchical panel (group × unit × year)
- Network fixtures:
  - `fixture_production_network` - Sparse directed weighted network
  - `fixture_bipartite_network` - Two-mode network structure
- Data validation assertions:
  - `assert_unique` - ID uniqueness (uses gisid for performance)
  - `assert_no_missing` - No missing values
  - `assert_positive` - All values positive
  - `assert_sorted` - Sort order preserved (uses hashsort)
  - `assert_panel_structure` - Valid xtset with balanced option
  - `assert_sum_equals` - Sum equals expected with by-group support
  - `assert_identity` - Accounting identities (A + B == C)
- Fixture system with pytest-like `conftest.do` pattern
- Built-in fixtures:
  - `use_fixture` - Request a fixture by name
  - `fixture_tempfile` - Temporary file path
  - `fixture_empty_dataset` - Empty dataset with optional observation count
  - `fixture_seed` - Reproducible random seed
- Fixture scoping: function, module, session
- Automatic `conftest.do` discovery in directory hierarchy
- Coverage instrumentation module (`instrument.py`)
  - SMCL comment markers for invisible coverage tracking
  - Automatic instrumentation to `.statatest/instrumented/` directory
  - Line number mapping for accurate reporting
- Enhanced coverage module with `FileCoverage` and `CoverageReport` classes
- HTML coverage report generation
- Logging module (`core/logging.py`) with ANSI color support
- 90 Python tests passing

### Changed

- Reorganized package structure: moved ado files to `statatest/ado/`
- Centralized all constants in `core/constants.py`
- Replaced `rich` library with Python standard logging + ANSI colors
- Merged [econ] extension into main package (no separate install needed)
- Merged econ documentation into main reference (removed extensions section)
- Updated mkdocs navigation with Use Cases section
- Improved path handling with `importlib.resources`

### Removed

- `rich` dependency (replaced with standard library)
- `[econ]` optional extra (all features now included by default)

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
