"""
Defines runner convenience functions for pymaccounting.
"""

import anyio

from pymaccounting.pipeline import test


def run_test(test_to_run: str):
    """
    Helper function to run dagger testing pipeline
    """
    anyio.run(test, test_to_run)
