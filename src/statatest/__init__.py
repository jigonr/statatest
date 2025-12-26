"""statatest - Pytest-inspired testing and code coverage framework for Stata."""

__version__ = "0.1.0"
__author__ = "Jose Ignacio Gonzalez Rojas"
__email__ = "j.i.gonzalez-rojas@lse.ac.uk"

from statatest.config import Config
from statatest.discovery import discover_tests
from statatest.runner import run_tests

__all__ = ["Config", "discover_tests", "run_tests", "__version__"]
