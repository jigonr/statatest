"""Pytest configuration and fixtures for statatest tests."""


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "requires_stata: mark test as requiring Stata installation"
    )
