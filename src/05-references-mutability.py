"""
05 - References & mutability
============================

Assignment never copies. Knowing which objects are mutable explains most
"why did my list change?" surprises.

* **Mutable**: `list`, `dict`, `set`, most user-defined objects
* **Immutable**: `int`, `float`, `str`, `tuple`, `bytes`, `frozenset`

Run the whole file:  uv run python src/05-references-mutability.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Aliasing

# %%
# Create a list and bind the name `a` to it
a = [1, 2, 3]
# `b` is bound to the SAME object; nothing is copied
b = a
# Mutating through `b`...
b.append(4)
# ...is visible through `a` -> [1, 2, 3, 4] True
print(a, a is b)

# %% [markdown]
# ## Shallow vs deep copies

# %%
# copy.deepcopy() lives in the copy module
import copy

# A nested list: the inner lists are separate objects
nested = [[1, 2], [3, 4]]
# A shallow copy: new outer list, SHARED inner lists
shallow = nested.copy()
# A deep copy: inner lists are copied too
deep = copy.deepcopy(nested)
# Mutate an inner list of the original
nested[0].append(99)
# The shallow copy sees the change, the deep copy does not
print(shallow, deep)

# %% [markdown]
# ## The repeated-list trap

# %%
# [[0] * 3] * 3 repeats a reference to ONE inner list
grid = [[0] * 3] * 3
# Changing one "row" changes all three
grid[0][0] = 1
# Prints [[1, 0, 0], [1, 0, 0], [1, 0, 0]]
print(grid)
# A comprehension builds three independent rows
grid = [[0] * 3 for _ in range(3)]
# Now only the first row changes
grid[0][0] = 1
# Prints [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
print(grid)

# %% [markdown]
# ## Mutable default arguments
# A default value is evaluated **once**, when the function is defined.

# %%
# The default list is created once and shared by all calls
def add_bad(x, lst=[]):
    # Every call without `lst` mutates the same list
    lst.append(x)
    # Return the shared list
    return lst


# Both calls return the same list object -> [1, 2] [1, 2]
print(add_bad(1), add_bad(2))


# The idiom: use None as the default and create the list inside
def add_good(x, lst=None):
    # Create a fresh list on every call that did not pass one
    lst = [] if lst is None else lst
    # Append to the fresh list
    lst.append(x)
    # Return it
    return lst


# Each call gets its own list -> [1] [2]
print(add_good(1), add_good(2))

# %% [markdown]
# ## Arguments are passed by "sharing"
# A function receives a reference to the caller's object: *mutating* it is
# visible outside, *rebinding* the parameter is not.

# %%
# Mutating the argument changes the caller's object
def mutate(items):
    # append() modifies the list object itself
    items.append("added")


# Rebinding the parameter only changes the local name
def rebind(items):
    # The caller's list is untouched
    items = ["new list"]


# Start with a list
data = ["original"]
# This changes `data`
mutate(data)
# This does not
rebind(data)
# Prints ['original', 'added']
print(data)

# %% [markdown]
# ## Immutable objects are replaced, not changed

# %%
# A tuple is immutable
t = (1, 2)
# Remember the identity of the original object
before = id(t)
# += creates a NEW tuple and rebinds t
t += (3,)
# New content, different object -> (1, 2, 3) False
print(t, id(t) == before)
