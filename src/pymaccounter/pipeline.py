"""
Dagger pipelines using the Python SDK for pymaccounter
"""

# referenced with modifications from:
# https://docs.dagger.io/sdk/python/628797/get-started

import shutil
import sys
from typing import List

import anyio
import dagger


async def pipeline_run_tests(
    tests_to_run: List[str],
    test_dir: str = "src/pymaccounter/tests",
    debug: bool = False,
) -> None:
    """
    Dagger pipeline for running reproducible tests in python.
    """

    # create dagger conf based on debug arg
    dagger_conf = dagger.Config(log_output=sys.stderr) if debug else dagger.Config()

    async with dagger.Connection(dagger_conf) as client:
        # get reference to the local project
        dockerfile_dir = client.host().directory(".")

        async def run_test(test_to_run: str, test_dir: str):
            """
            Run a test in a container via dagger
            """
            full_test_to_run = f"{test_dir}/{test_to_run}"

            # gather the terminal width for result display purposes
            terminal_width, _ = shutil.get_terminal_size()

            # build a python container based on Dockerfile and run test
            python = (
                client.container(
                    # explicitly set the container to be a certain platform type
                    platform=dagger.Platform("linux/amd64")
                ).build(
                    context=dockerfile_dir,
                    # uses a dockerfile to create the container
                    dockerfile="./src/pymaccounter/Dockerfile",
                )
                # run the python test through a poetry environment
                .with_exec(["poetry", "run", "python", full_test_to_run])
            )

            # execute and show the results of the last executed command
            results = await python.stdout()

            # surround the output with terminal-width lines for reading clarity
            print("_" * terminal_width)
            print(f"Test results for {full_test_to_run}:\n{results}")

        # when this block exits, all tasks will be awaited (i.e., executed)
        async with anyio.create_task_group() as tg:
            # run each test provided individually
            for test_to_run in tests_to_run:
                tg.start_soon(run_test, test_to_run, test_dir)

    print("All tests have finished")
