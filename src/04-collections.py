"""
04 - Built-in collections
=========================

`list`, `tuple`, `dict` and `set`, plus the `collections` module.

| Type | Literal | Mutable | Ordered |
|---|---|---|---|
| list | `[1, 2]` | yes | yes |
| tuple | `(1, 2)` | no | yes |
| dict | `{"k": 1}` | yes | insertion order |
| set | `{1, 2}` | yes | no |

Run the whole file:  uv run python src/04-collections.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## list: a dynamic array

# %%
# Create a list
xs = [3, 1, 4]
# Append one item at the end
xs.append(1)
# Extend with all items of another iterable
xs.extend([5, 9])
# Insert at a position
xs.insert(0, 2)
# Remove and return the last item
last = xs.pop()
# Remove the first occurrence of a value
xs.remove(4)
# Prints [2, 3, 1, 1, 5] 9
print(xs, last)

# %% [markdown]
# ## Sorting and slicing lists

# %%
# An unsorted list
xs = [2, 3, 1, 1, 5]
# sorted() returns a NEW list and leaves xs unchanged
print(sorted(xs, reverse=True))
# .sort() sorts in place and returns None
xs.sort()
# xs is now sorted
print(xs)
# Slicing works like on strings
print(xs[1:3], xs[::-1])
# Slice assignment replaces a range of items
xs[1:3] = [7, 7]
# Prints [1, 7, 7, 3, 5]
print(xs)

# %% [markdown]
# ## tuple and unpacking

# %%
# A tuple is an immutable sequence
point = (3, 4)
# Unpack it into two names
x, y = point
# Star-unpacking collects the rest into a list
first, *rest = [1, 2, 3, 4]
# A one-element tuple needs a trailing comma
single = (1,)
# Prints 3 4 1 [2, 3, 4] <class 'tuple'>
print(x, y, first, rest, type(single))
# Tuples are hashable, so they can be dict keys
distances = {(0, 0): 0.0, (3, 4): 5.0}
# Look up with a tuple key
print(distances[(3, 4)])

# %% [markdown]
# ## dict: a hash map
# Keys must be hashable (str, int, tuple, ...). Lookup is O(1) on average.

# %%
# A dict literal
d = {"a": 1}
# Insert or update a key
d["b"] = 2
# get() returns a default instead of raising KeyError
print(d.get("z", 0))
# setdefault() inserts a default if missing and returns the stored value
d.setdefault("c", []).append(1)
# Iterate over key/value pairs
for key, value in d.items():
    # Print each pair
    print(key, value)
# | merges into a new dict
print(d | {"e": 5})
# Delete a key
del d["a"]
# `in` tests keys -> False True
print("a" in d, "b" in d)

# %% [markdown]
# ## set: unique items

# %%
# Two sets
a = {1, 2, 3}
# A second set for set algebra
b = {2, 3, 4}
# Union, intersection, difference, symmetric difference
print(a | b, a & b, a - b, a ^ b)
# Remove duplicates from a list
print(set([1, 1, 2, 2, 3]))
# Membership tests on a set are O(1)
print(3 in a)
# {} is an empty DICT; use set() for an empty set
print(type({}), type(set()))

# %% [markdown]
# ## The `collections` module

# %%
# Specialised containers from the standard library
from collections import Counter, defaultdict, deque, namedtuple

# Counter counts hashable items -> [('i', 4), ('s', 4)]
print(Counter("mississippi").most_common(2))
# defaultdict creates missing values with a factory function
groups = defaultdict(list)
# Group words by their first letter
for word in ["apple", "avocado", "banana"]:
    # A missing key starts as an empty list automatically
    groups[word[0]].append(word)
# Convert to a plain dict for printing
print(dict(groups))
# deque has O(1) appends/pops at both ends; maxlen keeps the last N items
recent = deque(maxlen=3)
# Push five items
for i in range(5):
    # The oldest item is dropped when the deque is full
    recent.append(i)
# Prints deque([2, 3, 4], maxlen=3)
print(recent)
# namedtuple creates a small immutable record type
Point = namedtuple("Point", ["x", "y"])
# Fields are accessible by name
print(Point(1, 2).x)
