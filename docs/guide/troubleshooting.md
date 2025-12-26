# Troubleshooting

Common issues and solutions when using statatest.

## Installation Issues

### statatest command not found

**Symptom:**
```
bash: statatest: command not found
```

**Solutions:**

1. **Ensure pip/uv installed to PATH:**
   ```bash
   # Check if installed
   pip show statatest
   
   # Reinstall with pip
   pip install --user statatest
   
   # Or use uv
   uv tool install statatest
   ```

2. **Add Python user bin to PATH:**
   ```bash
   # macOS/Linux
   export PATH="$HOME/.local/bin:$PATH"
   
   # Add to ~/.bashrc or ~/.zshrc for persistence
   ```

3. **Run via Python module:**
   ```bash
   python -m statatest tests/
   ```

---

## Stata Configuration

### Stata executable not found

**Symptom:**
```
Error: Stata executable not found
```

**Solutions:**

1. **Check Stata is installed:**
   ```bash
   which stata-mp
   which stata-se
   which stata
   ```

2. **Configure in statatest.toml:**
   ```toml
   [tool.statatest]
   stata_executable = "/usr/local/bin/stata-mp"
   ```

3. **Set environment variable:**
   ```bash
   export STATA_PATH=/usr/local/bin/stata-mp
   ```

4. **Common Stata paths:**

   | OS | Path |
   |----|------|
   | macOS | `/usr/local/bin/stata-mp` |
   | Linux | `/usr/local/stata18/stata-mp` |
   | Windows | `C:\Program Files\Stata18\StataMP-64.exe` |

### Permission denied when running Stata

**Symptom:**
```
stata-mp: Permission denied
```

**Solutions:**

1. **Make Stata executable:**
   ```bash
   chmod +x /usr/local/bin/stata-mp
   ```

2. **Check file permissions:**
   ```bash
   ls -la /usr/local/bin/stata*
   ```

3. **In Docker/CI, run as root:**
   ```yaml
   container:
     image: dataeditors/stata18:latest
     options: --user root
   ```

### License issues in CI

**Symptom:**
```
r(601): license not found
```

**Solutions:**

1. **Encode license for secrets:**
   ```bash
   # macOS
   base64 -i stata.lic | pbcopy
   
   # Linux
   base64 stata.lic | xclip -selection clipboard
   ```

2. **Decode in workflow:**
   ```yaml
   - name: Set up Stata license
     run: |
       echo "${{ secrets.STATA_LIC_B64 }}" | base64 -d > /usr/local/stata/stata.lic
   ```

3. **Verify license path matches Docker image:**
   - `dataeditors/stata18`: `/usr/local/stata/stata.lic`

---

## Test Discovery

### No tests found

**Symptom:**
```
Found 0 test file(s)
```

**Solutions:**

1. **Check file naming convention:**
   - Test files must match `test_*.do` pattern
   - Example: `test_myfunction.do`, `test_analysis.do`

2. **Verify testpaths configuration:**
   ```toml
   [tool.statatest]
   testpaths = ["tests"]  # Must point to existing directory
   ```

3. **Check directory structure:**
   ```bash
   ls -la tests/
   find . -name "test_*.do"
   ```

4. **Use custom pattern:**
   ```toml
   [tool.statatest]
   test_files = ["test_*.do", "*_test.do"]
   ```

### Tests not running

**Symptom:** Tests are found but not executed.

**Solutions:**

1. **Check for syntax errors in test files:**
   ```bash
   stata-mp -b do tests/test_example.do
   cat tests/test_example.log
   ```

2. **Ensure test programs are called:**
   ```stata
   // Define test
   program define test_something
       // ...
   end
   
   // Must call the test!
   test_something
   ```

---

## Coverage Issues

### Coverage shows 0%

**Symptom:** Coverage report shows 0% even with tests passing.

**Solutions:**

1. **Configure source paths:**
   ```toml
   [tool.statatest.coverage]
   source = ["code/functions"]  # Point to your .ado files
   ```

2. **Verify .ado files exist:**
   ```bash
   ls -la code/functions/*.ado
   ```

3. **Check instrumentation directory:**
   ```bash
   ls -la .statatest/instrumented/
   ```

### Coverage not being collected

**Symptom:** LCOV file is empty or missing.

**Solutions:**

1. **Enable coverage explicitly:**
   ```bash
   statatest tests/ --coverage --cov-report=lcov
   ```

2. **Check SMCL logging:**
   - Coverage requires SMCL output
   - Verify `.smcl` logs are generated

3. **Check source file instrumentation:**
   ```bash
   # Instrumented files should have COV markers
   grep "COV:" .statatest/instrumented/*.ado
   ```

### Coverage varies between runs

**Solutions:**

1. **Use deterministic random seed:**
   ```stata
   fixture_seed, seed(12345)
   ```

2. **Check for conditional code paths:**
   - Random values may cause different branches to execute

3. **Use carryforward in Codecov:**
   ```yaml
   # codecov.yml
   flags:
     unit:
       carryforward: true
   ```

---

## Assertion Errors

### assert_equal fails with matching values

**Symptom:** Values look equal but assertion fails.

**Solutions:**

1. **Check for trailing spaces:**
   ```stata
   // Bad
   assert_equal "`r(result)' ", expected("value")
   
   // Good
   assert_equal "`r(result)'", expected("value")
   ```

2. **Use strtrim() for string comparison:**
   ```stata
   assert_equal strtrim("`r(result)'"), expected("value")
   ```

3. **Check numeric precision:**
   ```stata
   // Use assert_approx_equal for floats
   assert_approx_equal `r(mean)', expected(0.5) tol(0.001)
   ```

### assert_approx_equal fails

**Symptom:** Numeric comparison fails despite values being close.

**Solutions:**

1. **Increase tolerance:**
   ```stata
   // Default tolerance may be too strict
   assert_approx_equal `r(mean)', expected(0.5) tol(0.01)
   ```

2. **Check for missing values:**
   ```stata
   // Missing values will fail comparison
   assert_true !missing(`r(mean)')
   assert_approx_equal `r(mean)', expected(0.5) tol(0.01)
   ```

---

## Fixture Issues

### Fixture not found

**Symptom:**
```
Error: Fixture 'sample_data' not found
```

**Solutions:**

1. **Check conftest.do exists:**
   ```bash
   ls -la tests/conftest.do
   ```

2. **Verify fixture program name:**
   ```stata
   // In conftest.do
   program define fixture_sample_data  // Must start with fixture_
       // ...
   end
   ```

3. **Check fixture is in scope:**
   - Fixtures in parent directories are available to child directories
   - Check the directory hierarchy

### Fixture scope errors

**Symptom:** Fixture runs multiple times or not at all.

**Solutions:**

1. **Specify scope explicitly:**
   ```stata
   use_fixture sample_data, scope(module)
   ```

2. **Understand scope behavior:**

   | Scope | Behavior |
   |-------|----------|
   | `function` | Runs for each test (default) |
   | `module` | Runs once per test file |
   | `session` | Runs once per test run |

---

## CI/CD Issues

### GitHub Actions workflow fails

**Common causes and solutions:**

1. **Python version mismatch:**
   ```yaml
   - uses: actions/setup-python@v5
     with:
       python-version: "3.12"  # Ensure 3.11+
   ```

2. **Missing dependencies:**
   ```yaml
   - run: pip install statatest
   ```

3. **Stata license not set:**
   - Ad XMLd `STATA_LIC_B64` to repository secrets
   - Check secret name matches workflow

### JUnit not generated

**Symptom:** CI fails to find `junit.xml`.

**Solutions:**

1. **Specify output path:**
   ```bash
   statatest tests/ --junit-xml=junit.xml
   ```

2. **Check file is created:**
   ```yaml
   - run: |
       statatest tests/ --junit-xml=junit.xml
       ls -la junit.xml
   ```

3. **Upload as artifact:**
   ```yaml
   - uses: actions/upload-artifact@v4
     if: always()
     with:
       name: test-results
       path: junit.xml
   ```

---

## Performance Issues

### Tests run slowly

**Solutions:**

1. **Use module/session scope for expensive fixtures:**
   ```stata
   use_fixture large_dataset, scope(session)
   ```

2. **Parallelize tests (future feature):**
   - Currently tests run sequentially
   - Split into multiple test files for parallel CI jobs

3. **Profile Stata execution:**
   ```bash
   time statatest tests/ --verbose
   ```

### Out of memory errors

**Solutions:**

1. **Clear data between tests:**
   ```stata
   program define fixture_cleanup_teardown
       clear all
       macro drop _all
   end
   ```

2. **Use smaller test datasets:**
   ```stata
   // Instead of 1M observations
   set obs 1000
   ```

3. **Increase Stata memory:**
   ```stata
   set maxvar 10000
   set matsize 5000
   ```

---

## Getting Help

If you can't resolve your issue:

1. **Check existing issues:** [GitHub Issues](https://github.com/jigonr/statatest/issues)
2. **Search discussions:** [GitHub Discussions](https://github.com/jigonr/statatest/discussions)
3. **Open a new issue** with:
   - statatest version (`statatest --version`)
   - Stata version
   - Operating system
   - Minimal reproducible example
   - Full error message

---

## See Also

- [Configuration Reference](../reference/config.md)
- [CLI Reference](../reference/cli.md)
- [GitHub Actions Integration](../ci/github-actions.md)
