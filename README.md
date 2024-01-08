# Demonstrating Python Memory Allocator Reference Counting (and Related)

Demonstrating Python memory allocator reference counting and debug.
The goal of this repository is to help demonstrate Python memory allocation using source controlled code.
Work for this project was originally inspired by [cytomining/CytoTable#75](https://github.com/cytomining/CytoTable/issues/75) which explores related topics.

## Project outline

```mermaid
---
title: Project Overview
---
flowchart LR

pyproject["pyproject.toml"]
poeworkflow["poethepoet\nworkflows"]
dockerfile["Dockerfile"]
subgraph test_container["test container"]
    subgraph tests
        test_env["Python environment\n(for tests)"]
        test_modules["Test module(s)"]
    end
end
subgraph runner
    runner_env["Python environment\n(for runner)"]
    runner_cli["Runner CLI\n(Python Fire)"]
    pipeline["Container pipeline\n(through Dagger)"]
end


pyproject --> |defines| test_env
pyproject --> |defines| runner_env

test_env --> |runs| test_modules
test_modules -.-> |display\nresults through| pipeline
runner_env --> |enables| runner_cli
runner_cli --> |runs| pipeline

dockerfile -.-> |defines\ncontainer for| pipeline

pipeline --> |executes| test_container

pyproject --> poeworkflow
poeworkflow -.-> |declarative\nworkflows for| runner
```

See above for a quick overview of project components and their relationship.
[Poetry](https://python-poetry.org/docs/) is used to define Python environment dependencies within [dependency groups](https://python-poetry.org/docs/master/managing-dependencies/#dependency-groups) in a `pyproject.toml` file.
Declarative [Poe the Poet tasks](https://poethepoet.natn.io/index.html) may also be found in the same `pyproject.toml` file to help define reproducible workflows.
A "runner" command-line interface (CLI) is provided through [Python Fire](https://github.com/google/python-fire) to help enable the use of the container-based pipelines.
Container-based pipelines are provided through [Dagger's Python SDK](https://docs.dagger.io/sdk/python/) to help isolate potential OS-specific distinctions for memory allocation work in Python.
Testing workflows are designed to run "locally" within a developer's environment (for example, leveraging [pyenv](https://github.com/pyenv/pyenv), [poetry](https://python-poetry.org/docs/), and [Docker Desktop](https://www.docker.com/products/docker-desktop/)) or within [GitHub Actions images](https://github.com/actions/runner-images) (`dagger-io` installs the necessary dependencies).

## Development

The following are suggested steps to get started with development for this project.

1. Install Python from [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)
1. [Install Poetry](https://python-poetry.org/docs/#installation)
1. [Install Poe the Poet](https://poethepoet.natn.io/installation.html)
1. [Install Docker Desktop](https://www.docker.com/products/docker-desktop/)
1. Run Poe the Poet workflow(s): e.g. `poetry poe run_all_tests`
