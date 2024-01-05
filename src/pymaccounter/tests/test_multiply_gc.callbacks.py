"""
Module for testing Python garbage collection with customized callbacks.
"""
import gc


# leverage gc.callbacks to show collection start and stop along with info
# see: https://docs.python.org/3/library/gc.html#gc.callbacks
def info_callback(phase, info):
    if phase == "start":
        print("Garbage collection started. Info: ", info, sep="\n", end="\n\n")

    elif phase == "stop":
        print("Garbage collection stopped. Info: ", info, sep="\n", end="\n\n")


# append the callback for use by gc
gc.callbacks.append(info_callback)


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
