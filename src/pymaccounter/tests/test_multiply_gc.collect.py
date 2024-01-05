"""
Module for testing pure Python garbage collection.
"""
import gc


# modified example from:
# https://parsl.readthedocs.io/en/stable/1-parsl-introduction.html#Python-Apps
def multiply(a, b):
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
