# Extensions

statatest supports optional extensions that add domain-specific fixtures and assertions.

## Available Extensions

| Extension | Install Command | Description |
|-----------|-----------------|-------------|
| **[econ](econ.md)** | `pip install statatest[econ]` | Economic data fixtures and assertions |

## Installing Extensions

Extensions are installed as optional extras:

```bash
# Install with econ extension
pip install statatest[econ]

# Install with multiple extensions
pip install statatest[econ,other]

# Install all extensions
pip install statatest[all]
```

## Using Extensions

Extensions add .ado files that are automatically available when the extension is installed:

```stata
// Panel fixtures (from [econ])
fixture_balanced_panel, n_units(100) n_periods(10)

// Economic assertions (from [econ])
assert_panel_structure id year, balanced
assert_unique id year
```

## Creating Custom Extensions

Extensions are simply collections of .ado files in the `statatest/ado/` directory. To create a custom extension:

1. Add .ado files to `src/statatest/ado/<extension>/`
2. Register the extra in `pyproject.toml`
3. Document in `docs/extensions/`

See the [econ extension source](https://github.com/jigonr/statatest/tree/main/src/statatest/ado/econ) for reference.
