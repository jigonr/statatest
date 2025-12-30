# Documentation

statatest documentation built with MkDocs.

## Structure

```
docs/
├── index.md                    # Home page
├── getting-started/
│   ├── installation.md         # Installation guide
│   └── quickstart.md           # Quick start tutorial
├── guide/
│   ├── assertions.md           # Assertions guide
│   ├── fixtures.md             # Fixtures guide
│   ├── coverage.md             # Coverage guide
│   └── configuration.md        # Configuration reference
├── ci/
│   ├── github-actions.md       # GitHub Actions setup
│   └── docker.md               # Docker usage
├── reference/
│   ├── cli.md                  # CLI reference
│   ├── assertions.md           # Assertions API
│   └── fixtures.md             # Fixtures API
├── use-cases/
│   ├── panel-data.md           # Panel data examples
│   └── network-data.md         # Network data examples
└── contributing.md             # Contributing guide
```

## Building Docs

```bash
# Install docs dependencies
uv sync --all-extras

# Serve locally
uv run mkdocs serve

# Build static site
uv run mkdocs build
```

## Configuration

See `mkdocs.yml` in project root for:

- Navigation structure
- Theme settings
- Plugins (search, etc.)

## Writing Docs

Use Markdown with:

- Code blocks with syntax highlighting
- Admonitions (`!!! note`, `!!! warning`)
- Tables for reference content
