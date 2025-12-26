# statatest

**Pytest-inspired testing and coverage framework for Stata.**

[![PyPI version](https://img.shields.io/pypi/v/statatest.svg)](https://pypi.org/project/statatest/)
[![Python versions](https://img.shields.io/pypi/pyversions/statatest.svg)](https://pypi.org/project/statatest/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/jigonr/statatest/actions/workflows/ci.yml/badge.svg)](https://github.com/jigonr/statatest/actions/workflows/ci.yml)

## Features

- **Test Discovery**: Automatically find and run `test_*.do` files
- **Rich Assertions**: Built on Stata's native `assert` with detailed failure
  messages
- **Fixture System**: Reusable setup/teardown with pytest-like `conftest.do`
  pattern
- **Code Coverage**: Line-level coverage via SMCL comment instrumentation
- **CI Integration**: JUnit XML output for GitHub Actions, LCOV for Codecov
- **Backward Compatible**: Works with existing test patterns

## Quick Start

```bash
# Install
pip install statatest

# Run tests
statatest tests/

# Run with coverage
statatest tests/ --coverage --cov-report=lcov
```

## Example Test

```stata
// tests/test_myfunction.do

// @marker: unit
program define test_basic_functionality
    clear
    set obs 10
    gen x = _n

    myfunction x, gen(y)

    assert_var_exists y
    assert_equal _N, expected(10)
end
```

## Requirements

- **Python**: 3.11+
- **Stata**: 16+

## Getting Started

1. [Installation](getting-started/installation.md)
2. [Quick Start](getting-started/quickstart.md)
3. [Writing Your First Test](getting-started/first-test.md)

## License

MIT License - see [LICENSE](https://github.com/jigonr/statatest/blob/main/LICENSE)
for details.
