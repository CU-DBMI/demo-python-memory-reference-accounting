"""
Defines runner convenience functions for pymaccounting. 
"""

import anyio


def run_test(test_to_run: str):
    anyio.run(test, test_to_run)
