# Fixtures

Fixtures provide reusable setup and teardown for tests, inspired by pytest.

## Basic Fixture

Define a fixture in `conftest.do`:

```stata
// tests/conftest.do

program define fixture_sample_panel
    clear
    set obs 100
    gen int firm_id = ceil(_n / 10)
    gen int year = 2010 + mod(_n, 10)
    gen double revenue = exp(rnormal(15, 2))
end

program define fixture_sample_panel_teardown
    clear
end
```

## Using Fixtures

Use fixtures in your tests:

```stata
// tests/test_analysis.do
// @uses_fixture: sample_panel

program define test_panel_structure
    use_fixture sample_panel

    assert_obs_count 100
    assert_var_exists firm_id
    assert_var_exists year
end
```

## Built-in Fixtures

statatest includes several built-in fixtures:

### fixture_tempfile

Creates a temporary file path.

```stata
use_fixture tempfile

save "$fixture_tempfile_path", replace
```

### fixture_empty_dataset

Creates an empty dataset with optional observations.

```stata
// Empty dataset
fixture_empty_dataset

// With 100 observations
fixture_empty_dataset, obs(100)
```

### fixture_seed

Sets a reproducible random seed.

```stata
// Default seed (12345)
fixture_seed

// Custom seed
fixture_seed, seed(42)
```

## Fixture Scopes

Fixtures support three scopes:

- **function** (default): Setup/teardown per test
- **module**: Setup once per test file
- **session**: Setup once per test run

```stata
use_fixture sample_panel, scope(module)
```

## Automatic Discovery

statatest automatically discovers `conftest.do` files:

```
tests/
├── conftest.do          # Root fixtures
├── unit/
│   ├── conftest.do      # Unit test fixtures
│   └── test_*.do
└── integration/
    ├── conftest.do      # Integration test fixtures
    └── test_*.do
```

Fixtures are loaded from root to leaf, so child directories can override parent
fixtures.

## Teardown

Define a teardown function with the `_teardown` suffix:

```stata
program define fixture_database
    // Setup: create temp database
    use "template.dta", clear
    save "$tempdb", replace
end

program define fixture_database_teardown
    // Cleanup: remove temp database
    capture erase "$tempdb"
end
```

Teardown is called automatically when the fixture scope ends.
