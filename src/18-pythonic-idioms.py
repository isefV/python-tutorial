"""
18 - Pythonic idioms
====================

Each cell shows the C-style way first and the idiomatic Python way second.
Both produce the same result.

Run the whole file:  uv run python src/18-pythonic-idioms.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Iterate over items, not indices

# %%
# Sample data
xs = ["a", "b", "c"]
# Instead of index-based looping...
for i in range(len(xs)):
    # ...indexing into the list
    print(i, xs[i])
# ...use enumerate()
for i, x in enumerate(xs):
    # Same output, no indexing
    print(i, x)

# %% [markdown]
# ## Truthiness and `is None`

# %%
# Sample values
xs, x = [], None
# Instead of: if len(xs) == 0
if not xs:
    # Empty containers are falsy
    print("empty")
# Instead of: if x == None
if x is None:
    # None is a singleton, compare by identity
    print("no value")
# Instead of: if type(x) == int (also accepts subclasses like bool)
print(isinstance(5, int))

# %% [markdown]
# ## Build strings with join, swap with tuples

# %%
# Pieces to concatenate
parts = ["a", "b", "c"]
# Instead of s += p in a loop (quadratic for long inputs)...
s = ""
# ...concatenate piece by piece
for p in parts:
    # Each += creates a new string
    s += p
# ...use join()
print(s, "".join(parts))
# Instead of a temporary variable, swap with tuple unpacking
a, b = 1, 2
# Swap
a, b = b, a
# Prints 2 1
print(a, b)

# %% [markdown]
# ## dict.get, comprehensions, chained comparisons

# %%
# A sample dict
d = {"apple": 3}
# Instead of: v = d[k] if k in d else 0
print(d.get("pear", 0))
# Instead of creating a list and appending in a loop
print([x * 2 for x in range(5)])
# Instead of: x > 0 and x < 10
x = 5
# Chained comparison
print(0 < x < 10)
# Instead of "%s is %d" % (name, age)
name, age = "Ada", 36
# f-strings
print(f"{name} is {age}")

# %% [markdown]
# ## Always use `with` for resources

# %%
# A temporary folder for the demo file
import tempfile
# Path handling
from pathlib import Path

# Create a scratch folder
with tempfile.TemporaryDirectory() as tmp:
    # A file path inside it
    path = Path(tmp) / "x.txt"
    # Write a file the idiomatic way
    path.write_text("data", encoding="utf-8")
    # Instead of f = open(p); data = f.read(); f.close()
    with open(path, encoding="utf-8") as f:
        # The file is closed even if read() raises
        data = f.read()
    # Prints data
    print(data)

# %% [markdown]
# ## The Zen of Python

# %%
# Importing `this` prints the guiding principles of the language
import this
