"""
Defines runner convenience functions for pymaccounter.
"""

import anyio

from typing import Union, List
from pymaccounter.pipeline import test

import fire


def run_test(tests_to_run: Union[str, List[str]]) -> None:
    """
    Helper function to run dagger testing pipeline
    """
    anyio.run(test, tests_to_run)


if __name__ == "__main__":
    fire.Fire(run_test)
