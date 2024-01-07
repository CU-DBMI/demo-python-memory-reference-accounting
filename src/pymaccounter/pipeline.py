"""
Dagger pipelines using the Python SDK for pymaccounter
"""

# referenced with modifications from:
# https://docs.dagger.io/sdk/python/628797/get-started

import sys
from typing import List, Union

import anyio
import dagger


async def test(
    tests_to_run: List[str], test_dir: str = "src/pymaccounter/tests"
) -> None:
    """
    Dagger pipeline for running reproducible tests in python.
    """
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # get reference to the local project
        dockerfile_dir = client.host().directory(".")

        async def test_version(test_to_run: str, test_dir: str):
            full_test_to_run = f"{test_dir}/{test_to_run}"

            # build a python container based on Dockerfile and run test
            python = (
                client.container()
                .build(
                    context=dockerfile_dir,
                    dockerfile="./src/pymaccounter/Dockerfile",
                )
                .with_exec(["poetry", "run", "python", full_test_to_run])
            )

            print(f"Starting test for {full_test_to_run}")

            # execute and show the results of the last executed command
            print(await python.stdout())

            print(f"Tests for {full_test_to_run} succeeded!")

        # when this block exits, all tasks will be awaited (i.e., executed)
        async with anyio.create_task_group() as tg:
            for test_to_run in tests_to_run:
                tg.start_soon(test_version, test_to_run, test_dir)

    print("All tests have finished")
