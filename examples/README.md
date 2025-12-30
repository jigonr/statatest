# Examples

Example projects demonstrating statatest usage.

## Available Examples

### simple/

Basic example showing minimal test setup:

```
simple/
├── src/
│   └── myprogram.ado    # Code to test
├── tests/
│   └── test_basic.do    # Test file
└── statatest.toml       # Configuration
```

Run with:

```bash
cd examples/simple
statatest tests/
```

### fixtures/

Example using fixtures for test data:

```
fixtures/
├── tests/
│   ├── conftest.do         # Shared fixtures
│   └── test_fixtures.do    # Tests using fixtures
└── statatest.toml
```

## Creating Your Own Example

1. Create a directory with your example name
2. Add a `statatest.toml` configuration
3. Add `src/` with code to test
4. Add `tests/` with test files
5. Document in this README

## Running All Examples

```bash
for dir in examples/*/; do
    echo "=== Running $dir ==="
    (cd "$dir" && statatest tests/)
done
```
