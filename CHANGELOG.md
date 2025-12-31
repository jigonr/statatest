# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1](https://github.com/jigonr/statatest/compare/statatest-v0.1.0...statatest-v0.1.1) (2025-12-31)


### Features

* add GitHub Action for zero-install testing ([#26](https://github.com/jigonr/statatest/issues/26)) ([c9e3742](https://github.com/jigonr/statatest/commit/c9e37424cfd4ac48a54e5a54b64dacd2e11b7772))
* **ado:** add verbose option to all assertions and fixtures ([#54](https://github.com/jigonr/statatest/issues/54)) ([f64545f](https://github.com/jigonr/statatest/commit/f64545f31c5600d35c68d2a4ca1259cb1e83afbf)), closes [#36](https://github.com/jigonr/statatest/issues/36)
* **assertions:** add assert_count, assert_var_type, assert_label_exists ([#53](https://github.com/jigonr/statatest/issues/53)) ([e5f8624](https://github.com/jigonr/statatest/commit/e5f8624f498a66c12b3441d7790f8f97a07a9e1d))
* **coverage:** add instrumentation and pre-commit hooks ([#3](https://github.com/jigonr/statatest/issues/3)) ([98b4691](https://github.com/jigonr/statatest/commit/98b46914a078bc59863d6483594c6d8dac88a11a))
* **econ:** add economic fixtures and assertions as optional extra ([#12](https://github.com/jigonr/statatest/issues/12)) ([3b5e4a8](https://github.com/jigonr/statatest/commit/3b5e4a86898997aea1b9f6b240acaf03ba484594))
* **econ:** add panel fixtures and economic assertions ([#14](https://github.com/jigonr/statatest/issues/14)) ([21011fe](https://github.com/jigonr/statatest/commit/21011fe06e840e1d288bc7fd943fc0554c9de532))
* **fixtures:** add pytest-like fixture system ([#1](https://github.com/jigonr/statatest/issues/1)) ([2e0aa21](https://github.com/jigonr/statatest/commit/2e0aa21d1d6d7fa5e310de75e4d2fe9dff2fa201))
* initial release of statatest v0.1.0 ([94cc7fe](https://github.com/jigonr/statatest/commit/94cc7fefc2ea3038798aaeee5dc6352072c758c4))


### Bug Fixes

* **ci:** remove unsupported changelog-type from release-please ([f72b8b4](https://github.com/jigonr/statatest/commit/f72b8b41ae347d77beccc4154e7da5bca24ce852))
* **ci:** update codecov action and add id-token permission ([750ed32](https://github.com/jigonr/statatest/commit/750ed32280711eb8f5a26223f9daa06159cdc7b3))
* **ci:** use simple version tags without component prefix ([c583dfc](https://github.com/jigonr/statatest/commit/c583dfc75d0f990a4b7331e59476c1eb9da342d7))
* **coverage:** fix instrumentation to capture COV markers ([#52](https://github.com/jigonr/statatest/issues/52)) ([d24cf59](https://github.com/jigonr/statatest/commit/d24cf597ebd41575a0a7e692750267b071234b1a))
* **coverage:** instrument all lines in /// continuations ([c47d821](https://github.com/jigonr/statatest/commit/c47d821c85c15315c5c4db272784a5c42fb9eab2))
* **coverage:** wire up instrumentation in CLI ([#22](https://github.com/jigonr/statatest/issues/22)) ([f206c78](https://github.com/jigonr/statatest/commit/f206c78d5be873afa1da1d9bed0ee0326b2a17e0))
* **docs:** add migration.md to mkdocs navigation ([4ece2d4](https://github.com/jigonr/statatest/commit/4ece2d4b6133680cb8d176d7a4b1324a2a05e427))
* **docs:** remove docs/README.md conflicting with index.md ([dd185b4](https://github.com/jigonr/statatest/commit/dd185b4011d3a8e2090e8a5d4dd9ad72d349b42c))
* **econ:** correct network terminology and add AKM bipartite fixture ([#13](https://github.com/jigonr/statatest/issues/13)) ([4b3bfa5](https://github.com/jigonr/statatest/commit/4b3bfa539e27afae543f18b943ac95ef566e455b))
* **executor:** improve Stata invocation to match documented usage ([#50](https://github.com/jigonr/statatest/issues/50)) ([01974d7](https://github.com/jigonr/statatest/commit/01974d7af2136c079506d660467c1728604d49be))
* **lint:** move imports to top-level (PLC0415) ([e0dcd79](https://github.com/jigonr/statatest/commit/e0dcd79cb3740593143a9926526f37c97da93b87))
* **lint:** use list.extend in report.py for PERF401 ([433f1f3](https://github.com/jigonr/statatest/commit/433f1f32a99576466128b19168a2937de2539f04))


### Documentation

* add comprehensive troubleshooting guide ([#10](https://github.com/jigonr/statatest/issues/10)) ([93d86af](https://github.com/jigonr/statatest/commit/93d86af553a503d19c45ed91e711f38adbe75e41))
* add Docker integration guide ([#25](https://github.com/jigonr/statatest/issues/25)) ([326cf6f](https://github.com/jigonr/statatest/commit/326cf6fa69d7f02c71f61dc73a705e91e205f177)), closes [#21](https://github.com/jigonr/statatest/issues/21)
* add econ extension documentation and update CHANGELOG ([#15](https://github.com/jigonr/statatest/issues/15)) ([af481b6](https://github.com/jigonr/statatest/commit/af481b62023329dc7d98e8301302046a1cda1047))
* add language specifiers to code blocks (MD040) ([4a8d1da](https://github.com/jigonr/statatest/commit/4a8d1daeae424279b15986ec81ea5b275b32cffb))
* add MkDocs documentation website ([9d43b31](https://github.com/jigonr/statatest/commit/9d43b31dff12959d769754191521fdda94da3c6d))
* add MkDocs documentation website ([#4](https://github.com/jigonr/statatest/issues/4)) ([9d43b31](https://github.com/jigonr/statatest/commit/9d43b31dff12959d769754191521fdda94da3c6d))
* **codecov:** expand integration guide with multi-CI support ([#9](https://github.com/jigonr/statatest/issues/9)) ([507c2b9](https://github.com/jigonr/statatest/commit/507c2b9e52ed885e50311b995a04b10aacd75eb5))
* comprehensive documentation update ([#55](https://github.com/jigonr/statatest/issues/55)) ([08f1746](https://github.com/jigonr/statatest/commit/08f1746042e37d071a5a69490fce24886c1c7ea7))
* **executor:** remove outdated adopath settings comment ([#49](https://github.com/jigonr/statatest/issues/49)) ([d3f1f09](https://github.com/jigonr/statatest/commit/d3f1f0959cd37209246aab0c0d570b261c510d8a))
* recommend uv over pip for installation ([dd823fb](https://github.com/jigonr/statatest/commit/dd823fb0f1e09bc4f471dbf8b1aa9717ac54c76f))
* remove project-specific references from documentation ([#5](https://github.com/jigonr/statatest/issues/5)) ([9335845](https://github.com/jigonr/statatest/commit/9335845c911e1b3ed02e7ff3fdebce0593c42391))
* update badges and documentation url ([1006787](https://github.com/jigonr/statatest/commit/1006787db926ebd0f3bfd4ee80449e00c80c7c23))

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
