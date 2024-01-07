"""
Defines runner convenience functions for pymaccounter.
"""

from typing import List

import anyio
import fire

from pymaccounter.pipeline import test


def run_test(tests_to_run: List[str]) -> None:
    """
    Helper function to run dagger testing pipeline
    """
    print(tests_to_run)
    anyio.run(test, tests_to_run)


if __name__ == "__main__":
    fire.Fire(run_test)
