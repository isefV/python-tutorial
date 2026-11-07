"""
13 - Exceptions
===============

`try` / `except` / `else` / `finally`, raising and chaining exceptions,
custom exception classes and the EAFP style.

Run the whole file:  uv run python src/13-exceptions.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## try / except / else / finally

# %%
# Convert text to an int, reporting each stage
def to_int(text: str) -> int | None:
    # Code that may fail goes into try
    try:
        # int() raises ValueError for non-numeric text
        value = int(text)
    # Handle one specific exception type
    except ValueError as err:
        # The exception object carries the message
        print("bad input:", err)
        # Return a sentinel value
        return None
    # else runs only if the try block raised nothing
    else:
        # The success path
        print("parsed", value)
        # Return the parsed number
        return value
    # finally always runs: after success, after an error, even after return
    finally:
        # A typical place for cleanup
        print("finally runs for", repr(text))


# A valid input
to_int("42")
# An invalid input
to_int("abc")

# %% [markdown]
# ## Custom exceptions and `raise ... from`

# %%
# Custom exceptions are just subclasses of Exception (or a subclass of it)
class InvalidAge(ValueError):
    # A docstring is enough as the class body
    """Raised when an age is not a valid non-negative integer."""


# Translate low-level errors into a domain-specific error
def parse_age(text: str) -> int:
    # Attempt the conversion
    try:
        # May raise ValueError
        age = int(text)
    # Catch the low-level error
    except ValueError as err:
        # `from err` keeps the original exception as the cause
        raise InvalidAge(f"bad age: {text!r}") from err
    # Validate the range
    if age < 0:
        # raise creates and throws the exception
        raise InvalidAge("age must be >= 0")
    # A valid result
    return age


# Try several inputs
for text in ["30", "abc", "-5"]:
    # Attempt to parse each one
    try:
        # Print the parsed age
        print(parse_age(text))
    # Catch our custom type
    except InvalidAge as err:
        # __cause__ holds the chained original exception (or None)
        print("error:", err, "| cause:", repr(err.__cause__))

# %% [markdown]
# ## Catching several exception types

# %%
# A price table
prices = {"apple": 1.5}
# Inputs that fail in different ways
for key, qty in [("apple", "3"), ("pear", "1"), ("apple", "x")]:
    # Attempt the computation
    try:
        # KeyError if the key is missing, ValueError if qty is not a number
        total = prices[key] * int(qty)
        # Show the result
        print(key, total)
    # One handler for several types
    except (KeyError, ValueError) as err:
        # The class name tells which error happened
        print("skipped:", type(err).__name__, err)

# %% [markdown]
# ## EAFP vs LBYL
# *Easier to Ask Forgiveness than Permission* is the idiomatic Python style;
# *Look Before You Leap* is the C-style alternative.

# %%
# A cache for expensive results
cache = {}


# Pretend this is expensive
def compute(key: str) -> int:
    # Some work
    return len(key) * 10


# EAFP: just try, and handle the failure
def get_eafp(key: str) -> int:
    # The fast path when the key is present
    try:
        # May raise KeyError
        return cache[key]
    # The slow path when it is missing
    except KeyError:
        # Compute, store and keep the value
        value = cache[key] = compute(key)
        # Return the new value
        return value


# LBYL: check first, then act
def get_lbyl(key: str) -> int:
    # Explicit membership test
    if key not in cache:
        # Compute when missing
        cache[key] = compute(key)
    # Then read
    return cache[key]


# Both styles give the same results
print(get_eafp("abc"), get_lbyl("hello"), cache)

# %% [markdown]
# ## Common built-in exceptions

# %%
# Pairs of (description, function that fails)
examples = [
    ("int('x')", lambda: int("x")),
    ("[1][5]", lambda: [1][5]),
    ("{}['k']", lambda: {}["k"]),
    ("None.upper()", lambda: None.upper()),
    ("1 / 0", lambda: 1 / 0),
    ("'a' + 1", lambda: "a" + 1),
]
# Run each one and report which exception it raises
for label, func in examples:
    # Attempt the call
    try:
        # Each of these raises
        func()
    # Exception is the base class of all ordinary exceptions
    except Exception as err:
        # Show the type name next to the expression
        print(f"{label:14} -> {type(err).__name__}")
