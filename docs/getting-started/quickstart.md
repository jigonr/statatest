# Quick Start

## Create Your First Test

Create a test file `tests/test_example.do`:

```stata
// tests/test_example.do
// @marker: unit

clear all

program define test_basic_math
    assert_equal 2 + 2, expected(4)
    assert_true 5 > 3
    assert_false 1 > 2
end

test_basic_math
display "Test passed!"
```

## Run Tests

```bash
statatest tests/
```

Output:

```console
statatest v0.1.0
Collecting tests from: tests
Found 1 test file(s)

.

============================================================
1 passed in 0.25s
```

## Run with Verbose Output

```bash
statatest tests/ --verbose
```

Output:

```console
statatest v0.1.0
Collecting tests from: tests
Found 1 test file(s)

Running: tests/test_example.do PASSED (0.25s)

============================================================
1 passed in 0.25s
```

## Generate JUnit XML for CI

```bash
statatest tests/ --junit-xml=junit.xml
```

## Enable Coverage

```bash
statatest tests/ --coverage --cov-report=lcov
```

## Create Configuration

```bash
statatest --init
```

Creates `statatest.toml` with default settings.
