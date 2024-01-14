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

## Definitions

### Computer Memory

Computer memory, also sometimes known as "RAM" or "random-access memory", is a type of resource used by computer software on a computer.
"Computer memory stores information, such as data and programs for immediate use in the computer. ... Main memory operates at a high speed compared to \[non-memory\] storage which is slower but less expensive and \[oftentimes\] higher in capacity. " ([Wikipedia: Computer memory](https://en.wikipedia.org/wiki/Computer_memory)).
Computer memory is generally organized as ___heaps___ which help describe chunks of the total memory available on a computer.
These heaps may be ___private___ (only available to a specific software process) or ___shared___ (available to one or many software processes).

#### Python and Computer Memory

Python is an interpreted "high-level" programming language ([Python: What is Python?](https://www.python.org/doc/essays/blurb/)).
Interpreted languages are those which include an "interpreter" which helps execute code written in a particular way ([Wikipedia: Interpreter (computing)](<https://en.wikipedia.org/wiki/Interpreter_(computing)>)).
High-level languages such as Python often remove the requirement for software developers to manually perform memory management ([Wikipedia: High-level programming language](https://en.wikipedia.org/wiki/High-level_programming_language)).
Python code is executed by a commonly pre-packaged and downloaded binary call the Python [interpreter](<https://en.wikipedia.org/wiki/Interpreter_(computing)>).
The Python interpreter reads Python code and performs memory management as the code is executed.

### Memory Allocator

Memory management is a concept which helps enable the shared use of computer memory to avoid challenges such as memory overuse (where all memory is in use and never shared to other software).
Computer memory management often occurs through the use of a ___memory allocator___ which controls how computer memory resources are used.
Computer software can be written to interact with memory allocators to use computer memory.
Memory allocators may be used manually (with specific directions provided on when and how to use memory resources) or automatically (with an algorithmic approach of some kind).
The memory allocator usually performs the following actions with memory:

- __"Allocation"__: computer memory resource reservation (taking memory). This is sometimes also known as "`malloc`", or "memory allocate".
- __"Deallocation"__: computer memory resource freeing (giving back memory for other uses). This is sometimes also known as "`free`", or "freeing memory from allocation".

#### Python's Memory Manager

Memory is managed for Python software processes automatically (when unspecified) or manually (when specified) through the Python interpreter.
The ___Python memory manager___ manages memory through a private heap for Python software processes through the Python interpreter and CPython ([Python: Memory Management](https://docs.python.org/3/c-api/memory.html)).
From a high-level perspective, we assume variables and other operations written in Python will automatically allocate memory through the Python interpreter when executed.

### Garbage Collection

"Garbage collection (GC)" is used to describe a type of automated memory management.
"The _garbage collector_ attempts to reclaim memory which was allocated by the program, but is no longer referenced; such memory is called _garbage_." ([Wikipedia: Garbage collection (computer science)](<https://en.wikipedia.org/wiki/Garbage_collection_(computer_science)>)).
A garbage collector often works in tandem with a memory allocator to help control computer memory resource usage in software development.

#### Python's Garbage Collection

Python by default uses an optional garbage collector to automatically deallocate garbage memory through the Python interpreter in CPython.
"The main garbage collection algorithm used by CPython is reference counting. The basic idea is that CPython counts how many different places there are that have a reference to an object. Such a place could be another object, or a global (or static) C variable, or a local variable in some C function. When an object’s reference count becomes zero, the object is deallocated." ([Python Developer's Guide: Garbage collector design](https://devguide.python.org/internals/garbage-collector/))
The [`gc` module](https://docs.python.org/3/library/gc.html) provides an interface to the Python garbage collector.
In addition, the [`sys` module](https://docs.python.org/3/library/sys.html) provides many functions which provide information about references and other details about Python objects as they are executed through the interpreter.

## Development

The following are suggested steps to get started with development for this project.

1. (Suggested) Install Python from [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation) (or another way).
1. [Install Poetry](https://python-poetry.org/docs/#installation)
1. [Install Docker Desktop](https://www.docker.com/products/docker-desktop/)
1. Run Poe the Poet workflow(s): e.g. `poetry run poe run_all_tests`
   _(Poe the Poet is installed as a Poetry env dependency for the `runner` group)_

## Test Modules

This project focuses on leveraging Python memory observability tools to illustrate what happens as code is executed.
See the `src/pymaccounter/tests` folder for a full list of test modules.
Each test module includes a description of what it tests and expects in a [docstring](https://docs.python.org/3/glossary.html#term-docstring) near the top of the file.

### Running Test Modules

Test modules may be executed individually or in groups.
Test modules are provided in a list to be run by containerized pipelines.
Each test provided in this way is run in an isolated container instance.

In addition to test module specification, a test module base directory and debug mode may also be specified.
The test module base directory is where the container pipeline will look for test modules listed by name in the list.
Debug mode may be used to view container pipeline debug log messages.

See the following examples for more details on the suggested way to run tests through this project.

- Individual test: `poetry run python src/pymaccounter/runner.py '["test_baseline.py"]'`
- Multiple tests: `poetry run python src/pymaccounter/runner.py '["test_baseline.py", "test_multiply_gc.collect.py"]'`
- Individual test with debug mode: `poetry run python src/pymaccounter/runner.py '["test_baseline.py"]' --debug True`
- Individual test with non-default base test directory specification: `poetry run python src/pymaccounter/runner.py '["test_baseline.py"]' --test_dir 'src/another_test_dir'`
