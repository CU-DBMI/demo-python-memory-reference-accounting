"""
Defines runner convenience functions for pymaccounter.
"""

import anyio

from pymaccounter.pipeline import test


def run_test(test_to_run: str):
    """
    Helper function to run dagger testing pipeline
    """
    anyio.run(test, test_to_run)
