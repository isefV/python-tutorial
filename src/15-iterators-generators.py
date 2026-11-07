"""
15 - Iterators & generators
===========================

The iteration protocol behind every `for` loop, generator functions with
`yield`, and the `itertools` toolbox.

Run the whole file:  uv run python src/15-iterators-generators.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## The iteration protocol
# `for x in obj` calls `iter(obj)` and then `next()` until `StopIteration`.

# %%
# Get an iterator from any iterable
it = iter([10, 20, 30])
# next() returns the items one by one
print(next(it), next(it), next(it))
# When exhausted, next() raises StopIteration
try:
    # No items left
    next(it)
# A for-loop catches this for you
except StopIteration:
    # Report the end
    print("iterator exhausted")
# next() can return a default instead of raising
print(next(it, "default"))

# %% [markdown]
# ## A custom iterator class

# %%
# Counts down from a start value to 1
class Countdown:
    # Remember where to start
    def __init__(self, start: int):
        # The current value
        self.current = start

    # An iterator returns itself from __iter__
    def __iter__(self):
        # Return the iterator object
        return self

    # __next__ produces the next value or raises StopIteration
    def __next__(self) -> int:
        # Stop when we reach zero
        if self.current <= 0:
            # Signals the end of iteration
            raise StopIteration
        # Remember the value to return
        value = self.current
        # Move on
        self.current -= 1
        # Return it
        return value


# Works in a for-loop, list(), sum(), ... -> [3, 2, 1]
print(list(Countdown(3)))

# %% [markdown]
# ## Generator functions
# A function containing `yield` returns a generator: it pauses at each `yield`
# and resumes on the next `next()` call. Much shorter than an iterator class.

# %%
# islice() takes the first N items of any iterator
from itertools import islice


# An infinite generator of Fibonacci numbers
def fib():
    # Initial state
    a, b = 0, 1
    # Loop forever; values are produced only on demand
    while True:
        # Pause here and hand `a` to the caller
        yield a
        # Resume here on the next request
        a, b = b, a + b


# Take the first eight values -> [0, 1, 1, 2, 3, 5, 8, 13]
print(list(islice(fib(), 8)))
# A generator object can also be driven by hand
g = fib()
# -> 0 1 1
print(next(g), next(g), next(g))

# %% [markdown]
# ## Lazy pipelines
# Generators chain into pipelines that process one item at a time, with constant
# memory, no matter how large the input.

# %%
# io.StringIO simulates a large file in memory
import io

# Pretend this is a huge CSV file
big_file = io.StringIO("IR,120\nDE,95\nIR,140\nJP,80\n")


# Stage 1: read and split lines lazily
def read_rows(f):
    # One line at a time
    for line in f:
        # yield each parsed row
        yield line.rstrip().split(",")


# Stage 2: a generator expression filters lazily
iran = (row for row in read_rows(big_file) if row[0] == "IR")
# Stage 3: another one converts values
amounts = (int(row[1]) for row in iran)
# Nothing has been read yet; sum() pulls the items through -> 260
print(sum(amounts))

# %% [markdown]
# ## A generator can be consumed only once

# %%
# A generator expression
squares = (n * n for n in range(4))
# The first pass consumes it -> [0, 1, 4, 9]
print(list(squares))
# The second pass finds it empty -> []
print(list(squares))

# %% [markdown]
# ## itertools highlights

# %%
# Import a selection of tools
from itertools import accumulate, chain, combinations, count, groupby, islice, pairwise, product

# chain() concatenates iterables
print(list(chain([1, 2], (3, 4))))
# count() is infinite; islice() makes it finite
print(list(islice(count(10, 5), 3)))
# accumulate() gives running totals
print(list(accumulate([1, 2, 3, 4])))
# pairwise() yields neighbouring pairs
print(list(pairwise("abc")))
# product() is the cartesian product (nested loops)
print(list(product("ab", [0, 1])))
# combinations() picks without repetition
print(list(combinations("abc", 2)))
# groupby() groups CONSECUTIVE equal keys (sort first if needed)
for key, group in groupby("aaabccd"):
    # Each group is itself an iterator
    print(key, len(list(group)))
