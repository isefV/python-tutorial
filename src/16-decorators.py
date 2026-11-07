"""
16 - Decorators
===============

A decorator is a function that takes a function and returns a new one.
`@decorator` above a `def` is shorthand for `func = decorator(func)`.

Run the whole file:  uv run python src/16-decorators.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Functions are objects

# %%
# A plain function
def shout(text: str) -> str:
    # Return the upper-case text
    return text.upper()


# Bind a second name to the same function object
yell = shout
# Call through the new name
print(yell("hi"))
# Functions have attributes
print(shout.__name__)
# Functions can be passed to other functions
print(list(map(shout, ["a", "b"])))

# %% [markdown]
# ## A timing decorator

# %%
# functools.wraps copies the name and docstring to the wrapper
import functools
# time.perf_counter() is a precise clock
import time


# The decorator takes the function to wrap
def timed(func):
    # Preserve func.__name__, __doc__, ...
    @functools.wraps(func)
    # The wrapper accepts any arguments and forwards them
    def wrapper(*args, **kwargs):
        # Remember the start time
        start = time.perf_counter()
        # Call the original function
        result = func(*args, **kwargs)
        # Measure the elapsed time
        elapsed = time.perf_counter() - start
        # Report it
        print(f"{func.__name__} took {elapsed:.4f}s")
        # Return the original result
        return result

    # The decorator returns the wrapper
    return wrapper


# Same as: slow_sum = timed(slow_sum)
@timed
def slow_sum(n: int) -> int:
    # Some work
    return sum(range(n))


# Calling the function now also prints the timing
print(slow_sum(1_000_000))
# Thanks to wraps(), the name is preserved
print(slow_sum.__name__)

# %% [markdown]
# ## Memoization with `functools.cache`

# %%
# cache stores results by argument
import functools


# Without the cache this recursion would take forever for n = 100
@functools.cache
def fib(n: int) -> int:
    # Base case and recursive case in one expression
    return n if n < 2 else fib(n - 1) + fib(n - 2)


# Instant thanks to the cache -> 354224848179261915075
print(fib(100))
# The cache keeps statistics
print(fib.cache_info())

# %% [markdown]
# ## Decorators with arguments
# A decorator *factory* takes the arguments and returns the actual decorator.

# %%
# For wraps()
import functools


# The outer function receives the decorator's arguments
def repeat(times: int):
    # The real decorator
    def decorator(func):
        # Preserve the metadata
        @functools.wraps(func)
        # The wrapper calls func several times
        def wrapper(*args, **kwargs):
            # Collect each result
            return [func(*args, **kwargs) for _ in range(times)]

        # Return the wrapper from the decorator
        return wrapper

    # Return the decorator from the factory
    return decorator


# Same as: greet = repeat(3)(greet)
@repeat(3)
def greet(name: str) -> str:
    # Build a greeting
    return f"hi {name}"


# Prints ['hi Ada', 'hi Ada', 'hi Ada']
print(greet("Ada"))

# %% [markdown]
# ## Registration decorators
# A decorator does not have to wrap anything; it can just record the function.
# Web frameworks use this for routes (`@app.get("/")`).

# %%
# A registry of command handlers
COMMANDS = {}


# Register the decorated function under a name
def command(name: str):
    # The decorator stores and returns the function unchanged
    def decorator(func):
        # Record it
        COMMANDS[name] = func
        # Return the original function
        return func

    # Return the decorator
    return decorator


# Register a handler
@command("hello")
def say_hello() -> str:
    # The handler's work
    return "Hello!"


# Register another handler
@command("bye")
def say_bye() -> str:
    # The handler's work
    return "Goodbye!"


# Dispatch by name
for name in ["hello", "bye"]:
    # Look up and call the registered function
    print(name, "->", COMMANDS[name]())
