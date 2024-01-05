"""
Module for testing Python garbage collection with DEBUG_LEAK
"""
import gc


# set gc to debug leak mode
# see here for more info:
# https://docs.python.org/3/library/gc.html#gc.DEBUG_LEAK
gc.set_debug(gc.DEBUG_LEAK)


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
