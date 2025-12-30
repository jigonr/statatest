# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please:

1. **Do not** open a public issue
2. Email security concerns to <j.i.gonzalez-rojas@lse.ac.uk>
3. Include steps to reproduce if possible
4. Allow up to 48 hours for initial response

We take security seriously and will address verified vulnerabilities promptly.

## Security Best Practices

When using statatest:

- Keep your Stata license secure
- Don't commit sensitive data in test fixtures
- Use environment variables for credentials in CI/CD
- Review coverage reports for accidentally exposed paths
