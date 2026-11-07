"""
10 - Functions are objects: lambdas, closures, scope
====================================================

Functions can be stored, passed and returned like any other value. Name
lookup follows the **LEGB** rule: Local, Enclosing, Global, Built-in.

Run the whole file:  uv run python src/10-lambdas-closures-scope.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Functions as values and lambdas

# %%
# A lambda is a one-expression anonymous function
square = lambda x: x * x
# Call it like any function -> 9
print(square(3))
# Pass a function as an argument: key= decides how to sort
people = [("bob", 25), ("ann", 31), ("cy", 19)]
# Sort by the second tuple element (the age)
print(sorted(people, key=lambda p: p[1]))
# Built-in functions work as keys too
print(sorted(["banana", "Apple", "cherry"], key=str.lower))

# %% [markdown]
# ## Closures
# An inner function remembers the variables of the function that created it.

# %%
# A factory that returns a function
def make_counter():
    # A local variable of make_counter
    count = 0

    # The inner function "closes over" count
    def inc():
        # nonlocal lets us rebind the enclosing variable
        nonlocal count
        # Update the captured variable
        count += 1
        # Return the new value
        return count

    # Return the inner function itself (not a call)
    return inc


# Each counter has its own captured state
c1, c2 = make_counter(), make_counter()
# Call c1 twice
c1()
# The second call returns 2
print(c1(), c2())

# %% [markdown]
# ## global and nonlocal
# Reading an outer name needs nothing; **rebinding** it needs a declaration.

# %%
# A module-level (global) variable
counter = 0


# Reading a global needs no declaration
def read():
    # Found in the global scope
    return counter


# Rebinding a global requires the global statement
def increment():
    # Declare that counter refers to the global name
    global counter
    # Rebind the global
    counter += 1


# Increment twice
increment()
# Second increment
increment()
# Prints 2
print(read())

# %% [markdown]
# ## Blocks do not create a scope

# %%
# A simple loop
for i in range(3):
    # Nothing to do in the body
    pass
# The loop variable still exists afterwards and holds the last value -> 2
print(i)

# %% [markdown]
# ## Late binding in closures
# A lambda looks names up when it is **called**, not when it is created.

# %%
# All three lambdas share the same variable i
funcs = [lambda: i for i in range(3)]
# They all see its final value -> [2, 2, 2]
print([f() for f in funcs])
# Fix: freeze the current value as a default argument
funcs = [lambda i=i: i for i in range(3)]
# Now -> [0, 1, 2]
print([f() for f in funcs])

# %% [markdown]
# ## map, filter and reduce
# They exist, but comprehensions are usually clearer.

# %%
# reduce() moved to functools
from functools import reduce

# map() applies a function to every item (lazily)
print(list(map(str.upper, ["a", "b"])))
# filter() keeps items for which the function is truthy
print(list(filter(lambda n: n % 2, range(10))))
# reduce() folds a sequence into one value -> 24
print(reduce(lambda a, b: a * b, [1, 2, 3, 4]))
# The comprehension equivalent of the filter above
print([n for n in range(10) if n % 2])
