"""
Defines runner convenience functions and interface for pymaccounter.
"""

from typing import List

import anyio
import fire

from pymaccounter.pipeline import pipeline_run_tests


def run_tests(
    tests_to_run: List[str],
    test_dir: str = "src/pymaccounter/tests",
    debug: bool = False,
) -> None:
    """
    Helper function to run dagger testing pipeline
    """

    anyio.run(pipeline_run_tests, tests_to_run, test_dir, debug)


if __name__ == "__main__":
    # creates a CLI through Python Fire for run_test
    fire.Fire(run_tests)
