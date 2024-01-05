"""
Module for testing Python garbage collection.
"""
import gc

# pylint: disable=R0801


def multiply(a, b):
    """
    Basic python function
    """
    return a * b


print(multiply(5, 9))

# collect garbage
# see here for more info:
# https://docs.python.org/3/library/gc.html#gc.collect
collected = gc.collect()

# print the unreachable objects
print(collected)

# print the len of gc garbage to reference unreachable objects
print(len(gc.garbage))
