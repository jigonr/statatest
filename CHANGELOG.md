# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.1.1 (2025-12-30)

## What's Changed
* feat(fixtures): add pytest-like fixture system by @jigonr in https://github.com/jigonr/statatest/pull/1
* chore(ci): add release-please for automatic changelog by @jigonr in https://github.com/jigonr/statatest/pull/2
* feat(coverage): add instrumentation and pre-commit hooks by @jigonr in https://github.com/jigonr/statatest/pull/3
* docs: add MkDocs documentation website by @jigonr in https://github.com/jigonr/statatest/pull/4
* docs: remove project-specific references from documentation by @jigonr in https://github.com/jigonr/statatest/pull/5
* docs(codecov): expand integration guide with multi-CI support by @jigonr in https://github.com/jigonr/statatest/pull/9
* docs: add comprehensive troubleshooting guide by @jigonr in https://github.com/jigonr/statatest/pull/10
* ci: add scheduled Stata integration tests by @jigonr in https://github.com/jigonr/statatest/pull/11
* feat(econ): add economic fixtures and assertions as optional extra by @jigonr in https://github.com/jigonr/statatest/pull/12
* fix(econ): correct network terminology and add AKM bipartite fixture by @jigonr in https://github.com/jigonr/statatest/pull/13
* feat(econ): add panel fixtures and economic assertions by @jigonr in https://github.com/jigonr/statatest/pull/14
* docs: add econ extension documentation and update CHANGELOG by @jigonr in https://github.com/jigonr/statatest/pull/15
* chore: remove release-please in favor of manual releases by @jigonr in https://github.com/jigonr/statatest/pull/17
* fix(coverage): wire up instrumentation in CLI by @jigonr in https://github.com/jigonr/statatest/pull/22
* test: improve Python test coverage to 90%+ by @jigonr in https://github.com/jigonr/statatest/pull/24
* docs: add Docker integration guide by @jigonr in https://github.com/jigonr/statatest/pull/25
* feat: add GitHub Action for zero-install testing by @jigonr in https://github.com/jigonr/statatest/pull/26
* refactor: code quality improvements (constants, logging, econ merge) by @jigonr in https://github.com/jigonr/statatest/pull/30
* refactor(config): replace lambdas with __post_init__ by @jigonr in https://github.com/jigonr/statatest/pull/44
* refactor(fixtures): move fixtures.py to fixtures/ module by @jigonr in https://github.com/jigonr/statatest/pull/45
* refactor(coverage): move instrument.py to coverage/ module by @jigonr in https://github.com/jigonr/statatest/pull/46
* refactor(fixtures): rename fixture_production_network to fixture_directed_network by @jigonr in https://github.com/jigonr/statatest/pull/47
* refactor(config): OOP redesign with classmethod factory + remove adopath_mode by @jigonr in https://github.com/jigonr/statatest/pull/48
* docs(executor): remove outdated adopath settings comment by @jigonr in https://github.com/jigonr/statatest/pull/49
* fix(executor): improve Stata invocation to match documented usage by @jigonr in https://github.com/jigonr/statatest/pull/50
* fix(coverage): fix instrumentation to capture COV markers by @jigonr in https://github.com/jigonr/statatest/pull/52
* feat(assertions): add assert_count, assert_var_type, assert_label_exists by @jigonr in https://github.com/jigonr/statatest/pull/53
* feat(ado): add verbose option to all assertions and fixtures by @jigonr in https://github.com/jigonr/statatest/pull/54
* docs: comprehensive documentation update by @jigonr in https://github.com/jigonr/statatest/pull/55
* release: prepare v0.1.0 infrastructure by @jigonr in https://github.com/jigonr/statatest/pull/57
* ci(deps): bump actions/download-artifact from 4 to 7 by @dependabot[bot] in https://github.com/jigonr/statatest/pull/62
* ci(deps): bump astral-sh/setup-uv from 4 to 7 by @dependabot[bot] in https://github.com/jigonr/statatest/pull/61
* ci(deps): bump actions/upload-pages-artifact from 3 to 4 by @dependabot[bot] in https://github.com/jigonr/statatest/pull/60
* ci(deps): bump actions/setup-python from 5 to 6 by @dependabot[bot] in https://github.com/jigonr/statatest/pull/59
* ci(deps): bump DavidAnson/markdownlint-cli2-action from 18 to 22 by @dependabot[bot] in https://github.com/jigonr/statatest/pull/58

## New Contributors
* @jigonr made their first contribution in https://github.com/jigonr/statatest/pull/1
* @dependabot[bot] made their first contribution in https://github.com/jigonr/statatest/pull/62

**Full Changelog**: https://github.com/jigonr/statatest/compare/v0.1.0...v0.1.1

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
