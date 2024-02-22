"""
Module for testing Python garbage collection with customized callbacks.
"""
import gc

# pylint: disable=R0801


def info_callback(phase, info):
    """
    Leverage gc.callbacks to show collection start and stop along with info
    see: https://docs.python.org/3/library/gc.html#gc.callbacks
    """
    if phase == "start":
        print("Garbage collection started. Info: ", info, sep="\n", end="\n\n")

    elif phase == "stop":
        print("Garbage collection stopped. Info: ", info, sep="\n", end="\n\n")


# append the callback for use by gc
gc.callbacks.append(info_callback)


def multiply(a, b):
    """
    Basic python function
    """
    return a * b


print(f"Function output: {multiply(5, 9)}")

# collect garbage
# see here for more info:
# https://docs.python.org/3/library/gc.html#gc.collect
COLLECTED = gc.collect()

# print the unreachable objects
print(COLLECTED)
assert COLLECTED == 0

# print the len of gc garbage to reference unreachable objects
GC_LEN = len(gc.garbage)
print(GC_LEN)
assert GC_LEN == 0
