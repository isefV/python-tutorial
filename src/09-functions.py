"""
09 - Functions
==============

Defaults, keyword arguments, the five parameter kinds, variadic arguments
and type hints.

Run the whole file:  uv run python src/09-functions.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Defaults, keywords and docstrings

# %%
# Type hints document intent; the default makes `greeting` optional
def greet(name: str, greeting: str = "Hello") -> str:
    # The docstring is what help(greet) shows
    """Return a greeting for `name`."""
    # Build the result with an f-string
    return f"{greeting}, {name}!"


# Positional call
print(greet("Ada"))
# Keyword arguments can come in any order
print(greet(greeting="Hi", name="Ada"))
# The docstring is available at runtime
print(greet.__doc__)

# %% [markdown]
# ## Parameter kinds
# `/` ends positional-only parameters, `*` starts keyword-only parameters.

# %%
# a, b: positional-only | c: either | d: keyword-only | kw: extra keywords
def f(a, b, /, c, *, d=1, **kw):
    # Return everything so we can inspect it
    return a, b, c, d, kw


# Extra keyword arguments land in kw -> (1, 2, 3, 4, {'e': 5})
print(f(1, 2, 3, d=4, e=5))
# c may also be passed by keyword -> (1, 2, 3, 1, {})
print(f(1, 2, c=3))
# Passing a positional-only parameter by keyword fails
try:
    # This raises TypeError
    f(a=1, b=2, c=3)
# Show the error
except TypeError as err:
    # Print the message
    print("TypeError:", err)

# %% [markdown]
# ## *args and **kwargs

# %%
# *args collects extra positional arguments (tuple), **kwargs keywords (dict)
def log(*args, **kwargs):
    # Show what was collected
    print(args, kwargs)


# Mixed arguments -> (1, 2) {'level': 'info'}
log(1, 2, level="info")
# * and ** also UNPACK a sequence / dict at the call site
log(*[1, 2], **{"level": "info"})

# %% [markdown]
# ## Returning several values

# %%
# A function can return a tuple
def min_max(xs):
    # The comma builds a tuple
    return min(xs), max(xs)


# Unpack the tuple directly -> 1 4
lo, hi = min_max([3, 1, 4])
# Print both values
print(lo, hi)


# A function without a return statement returns None
def nothing():
    # An empty body
    pass


# Prints None
print(nothing())

# %% [markdown]
# ## Type hints are not enforced
# Hints are for readers, IDEs and type checkers (mypy, pyright). Python itself
# does not check them.

# %%
# The hints say int ...
def double(x: int) -> int:
    # ... but any type that supports * works
    return x * 2


# A str is accepted at runtime -> abab
print(double("ab"))
# The hints are stored as metadata
print(double.__annotations__)

# %% [markdown]
# ## Recursion
# Works, but there is no tail-call optimization and the depth is limited.

# %%
# The recursion limit lives in the sys module
import sys


# Classic recursive factorial
def factorial(n: int) -> int:
    # Base case
    if n <= 1:
        # Stop recursing
        return 1
    # Recursive case
    return n * factorial(n - 1)


# Prints 3628800
print(factorial(10))
# The default limit is about 1000 frames
print(sys.getrecursionlimit())
