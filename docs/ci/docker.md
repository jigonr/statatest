# Docker Integration

This guide covers using statatest with the
[AEA Data Editor's Docker images](https://hub.docker.com/u/dataeditors), which
provide Stata in containers for CI/CD.

## Available Images

The AEA Data Editor maintains Docker images for various Stata versions:

### Stata 18.5 (Recommended)

| Image                        | Description           | Size   |
| ---------------------------- | --------------------- | ------ |
| `dataeditors/stata18_5-mp`   | MP (multiprocessor)   | ~537MB |
| `dataeditors/stata18_5-mp-i` | MP + help files       | ~3.2GB |
| `dataeditors/stata18_5-mp-x` | MP + GUI (incomplete) | ~4.4GB |
| `dataeditors/stata18_5-se`   | SE (standard)         | ~2.6GB |
| `dataeditors/stata18_5-be`   | BE (basic)            | ~2.6GB |

### Stata 19.5 (Newest)

| Image                      | Description         |
| -------------------------- | ------------------- |
| `dataeditors/stata19_5-mp` | MP (multiprocessor) |
| `dataeditors/stata19_5-se` | SE (standard)       |
| `dataeditors/stata19_5-be` | BE (basic)          |

### Version Tags

!!! warning "Always use pinned version tags" Never use `latest` tag. Use
specific date tags for reproducibility.

**Available tags for `stata18_5-mp`:**

- `2025-02-26` (recommended)
- `2024-12-18`
- `2024-10-16`
- `2024-09-04`

```yaml
# Good - pinned version
image: dataeditors/stata18_5-mp:2025-02-26

# Bad - unpredictable
image: dataeditors/stata18_5-mp:latest
```

## Local Development Setup

### Step 1: Create a Dockerfile

Create a `Dockerfile.statatest` in your project root:

```dockerfile
# Use AEA Data Editor's Stata image
FROM dataeditors/stata18_5-mp:2025-02-26

# Switch to root for installation
USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        git \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install Python 3.11
RUN uv python install 3.11

# Add uv to PATH
ENV PATH="/root/.local/bin:$PATH"

# Install statatest
RUN uv tool install --python 3.11 statatest

# Set working directory
WORKDIR /project
```

### Step 2: Build the Image

```bash
docker build -t stata-statatest -f Dockerfile.statatest .
```

### Step 3: Run Tests

```bash
docker run --rm \
  -v "$PWD:/project" \
  -v "/path/to/stata.lic:/usr/local/stata/stata.lic:ro" \
  -w /project \
  stata-statatest \
  statatest tests/
```

## License Management

Stata requires a valid license to run. There are two approaches:

### Local Development

Mount your license file directly:

```bash
docker run --rm \
  -v "$PWD:/project" \
  -v "$HOME/stata.lic:/usr/local/stata/stata.lic:ro" \
  stata-statatest statatest tests/
```

### CI/CD (GitHub Actions)

Store the license as a base64-encoded secret:

1. **Encode your license:**

   ```bash
   base64 -i stata.lic -o stata_lic_b64.txt
   ```

2. **Add to GitHub Secrets:**
   - Go to Settings → Secrets and variables → Actions
   - Create `STATA_LIC_B64` with the base64 content

3. **Decode in workflow:**

   ```yaml
   - name: Decode Stata license
     run: echo "${{ secrets.STATA_LIC_B64 }}" | base64 -d > stata.lic
   ```

## GitHub Actions Integration

### Basic Workflow

```yaml
name: Stata Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    container:
      image: dataeditors/stata18_5-mp:2025-02-26
      options: --user root

    steps:
      - uses: actions/checkout@v4

      - name: Decode Stata license
        run:
          echo "${{ secrets.STATA_LIC_B64 }}" | base64 -d >
          /usr/local/stata/stata.lic

      - name: Install uv
        run: |
          apt-get update && apt-get install -y curl
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Install statatest
        run: uv tool install statatest

      - name: Run tests
        run: statatest tests/ --junit-xml junit.xml

      - name: Upload test results
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: junit.xml
```

### With Coverage

```yaml
- name: Run tests with coverage
  run: statatest tests/ --coverage --cov-report=lcov --junit-xml junit.xml

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    files: coverage.lcov
    token: ${{ secrets.CODECOV_TOKEN }}
```

## Installing Stata Packages

If your tests require additional Stata packages (gtools, estout, etc.), install
them in the Dockerfile:

```dockerfile
# Install Stata packages (no internet in CI)
COPY stata-packages/ /stata-packages/
RUN stata-mp -b do /stata-packages/install.do
```

Where `stata-packages/install.do` contains:

```stata
* Install packages from local files
net install gtools, from("/stata-packages/gtools")
net install estout, from("/stata-packages/estout")
```

!!! tip "Local Package Files" Download packages locally before CI runs to avoid
network dependencies. The AEA Data Editor has
[detailed instructions](https://github.com/AEADataEditor/replication-template/blob/master/template-README.md)
on reproducible package installation.

## Troubleshooting

### License Issues

**Error:** `stata.lic not found`

```bash
# Check license is mounted correctly
docker run --rm stata-statatest ls -la /usr/local/stata/stata.lic
```

### Permission Issues

**Error:** `Permission denied`

```bash
# Run as root
docker run --rm --user root ...
```

### Memory Issues

For large datasets, increase container memory:

```bash
docker run --rm --memory=4g ...
```

### Platform Issues (Apple Silicon)

For M1/M2 Macs, use platform flag:

```bash
docker run --rm --platform linux/amd64 ...
```

## Further Reading

- [AEA Data Editor Docker images](https://hub.docker.com/u/dataeditors)
- [GitHub Actions documentation](github-actions.md)
- [Codecov integration](codecov.md)
