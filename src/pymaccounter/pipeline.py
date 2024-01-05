"""
Dagger pipelines using the Python SDK for pymaccounter
"""

# referenced with modifications from:
# https://docs.dagger.io/sdk/python/628797/get-started

import sys
from typing import List, Union

import anyio
import dagger


async def test(test_to_run: Union[str, List[str]]):
    """
    Dagger pipeline for running reproducible tests in python.
    """
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # get reference to the local project
        dockerfile_dir = client.host().directory(".")

        async def test_version(test_to_run: str):
            # build a python container based on Dockerfile
            python = (
                client.container()
                .build(
                    context=dockerfile_dir,
                    dockerfile="./build/docker/Dockerfile",
                )
                .with_exec(["poetry", "run", "python", test_to_run])
            )

            print(f"Starting test for {test_to_run}")

            # execute
            await python.sync()

            print(f"Tests for {test_to_run} succeeded!")

        # when this block exits, all tasks will be awaited (i.e., executed)
        async with anyio.create_task_group() as tg:
            tg.start_soon(test_version, test_to_run)

    print("All tests have finished")
