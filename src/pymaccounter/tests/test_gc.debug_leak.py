"""
Module for testing pure Python garbage collection.
"""
import gc
import sys

import pandas as pd

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

# list of elements which could not be collected in garbage
# see here for more info:
# https://docs.python.org/3/library/gc.html#gc.garbage
if gc.garbage:
    print(f"Memory leak detected: {len(gc.garbage)} objects")
    df = pd.DataFrame(
        [
            {
                "id": id(obj),
                "type": type(obj),
                "refcount": sys.getrefcount(obj),
                "repr": repr(obj),
                "size": sys.getsizeof(obj),
            }
            for obj in gc.garbage
        ]
    )

    print(df.head())
    # df.to_csv("experiment_control_gc.csv")

# else print that there was nothing to analyze
else:
    print("No uncollected garbage to analyze.")
