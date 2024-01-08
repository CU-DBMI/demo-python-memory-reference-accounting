"""
Defines runner convenience functions for pymaccounter.
"""

from typing import List

import anyio
import fire

from pymaccounter.pipeline import pipeline_run_tests


def run_tests(tests_to_run: List[str]) -> None:
    """
    Helper function to run dagger testing pipeline
    """

    anyio.run(pipeline_run_tests, tests_to_run)


if __name__ == "__main__":
    # creats a CLI through Python Fire for run_test
    fire.Fire(run_tests)
