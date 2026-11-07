"""
01 - Syntax basics
==================

How Python code is laid out: names instead of declarations, indentation
instead of braces, and a few built-ins for inspecting objects.

Run the whole file:  uv run python src/01-syntax-basics.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Variables are names bound to objects
# There are no declarations. A variable is just a **name** that points to an
# object; the *object* has a type, the name does not.

# %%
# Bind the name `x` to an int object (no type declaration needed)
x = 42
# Rebind the same name to a str object: names have no type, objects do
x = "now a string"
# Print the value and the type of the object `x` currently refers to
print(x, type(x))

# %% [markdown]
# ## Multiple assignment and swapping

# %%
# Bind the same object to several names at once
a = b = 0
# Unpack a tuple into two names in one statement
a, b = 1, 2
# Swap two values without a temporary variable
a, b = b, a
# Prints 2 1
print(a, b)

# %% [markdown]
# ## Indentation defines blocks
# A colon starts a block; the indented lines below it form the block body.
# Use 4 spaces per level (PEP 8).

# %%
# Import the math module from the standard library
import math


# Define a function: the colon starts a block, indentation marks its body
def area(r):
    # A docstring documents the function; help(area) shows it
    """Return the area of a circle with radius r."""
    # An if-block nested inside the function body
    if r < 0:
        # This line belongs to the if-block because it is indented further
        raise ValueError("negative radius")
    # ** is the power operator
    return math.pi * r ** 2


# Call the function and format the result with 2 decimals -> 12.57
print(f"{area(2):.2f}")

# %% [markdown]
# ## Long lines
# Inside `()`, `[]` or `{}` a statement may continue on the next line without a
# backslash.

# %%
# The parentheses allow the expression to span two lines
total = (1 + 2 +
         3 + 4)
# Prints 10
print(total)

# %% [markdown]
# ## Inspecting objects

# %%
# isinstance() is the preferred way to test a type
print(isinstance(3, int))
# type() returns the exact class of an object
print(type(3.0))
# dir() lists an object's attributes; here the public str methods (first 5)
print([name for name in dir("text") if not name.startswith("_")][:5])
# The keyword module knows the reserved words of the language
import keyword
# These names cannot be used as variable names
print(keyword.kwlist)

# %% [markdown]
# ## Printing
# `print()` writes to stdout. (`input()` reads a line from stdin as a `str`; it
# is not used here so the file runs without interaction.)

# %%
# print() accepts several values and a custom separator
print("a", "b", "c", sep=", ")
# end= replaces the default newline
print("no newline here", end=" | ")
# The next print continues on the same line
print("done")
