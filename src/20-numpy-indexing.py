"""
20 - NumPy: indexing, slicing & masks
=====================================

Index with `[row, column]`. Basic slices are **views** of the same memory;
boolean masks and fancy indexing return **copies**.

Run the whole file:  uv run python src/20-numpy-indexing.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Basic indexing and slicing

# %%
# NumPy
import numpy as np

# A 3x4 example array
a = np.arange(12).reshape(3, 4)
# Print it
print(a)
# One element: row 1, column 2 -> 6 (prefer this over a[1][2])
print(a[1, 2])
# A whole row -> [4 5 6 7]
print(a[1])
# A whole column -> [ 2  6 10]
print(a[:, 2])
# Rows 1.., every second column
print(a[1:, ::2])
# Negative indices count from the end -> 11
print(a[-1, -1])

# %% [markdown]
# ## Boolean masks

# %%
# NumPy
import numpy as np

# A 3x4 example array
a = np.arange(12).reshape(3, 4)
# A comparison gives an array of booleans
mask = a % 2 == 0
# Print the mask
print(mask)
# Indexing with the mask selects matching elements (1-D result)
print(a[mask])
# Combine masks with & | ~ and wrap each condition in parentheses
print(a[(a > 2) & (a < 6)])
# np.where(cond, x, y) is an element-wise if/else
print(np.where(a > 5, a, 0))
# Masked assignment changes the selected elements in place
a[a > 9] = -1
# Print the modified array
print(a)

# %% [markdown]
# ## Fancy indexing

# %%
# NumPy
import numpy as np

# A 3x4 example array
a = np.arange(12).reshape(3, 4)
# A list of indices selects rows 0 and 2
print(a[[0, 2]])
# Pairs of (row, column) indices -> [ 1 11]
print(a[[0, 2], [1, 3]])
# argsort() returns the indices that would sort an array
values = np.array([30, 10, 20])
# Use them to reorder -> [10 20 30]
print(values[np.argsort(values)])

# %% [markdown]
# ## Views vs copies

# %%
# NumPy
import numpy as np

# A 3x4 example array
a = np.arange(12).reshape(3, 4)
# A basic slice is a VIEW of the same memory
row = a[0]
# Writing through the view...
row[0] = 99
# ...changes the original -> 99
print(a[0, 0])
# .copy() gives independent data
safe = a[1].copy()
# Change the copy
safe[0] = -5
# The original is untouched -> 4
print(a[1, 0])
# Masks return copies too
picked = a[a > 5]
# Changing the copy does not affect `a`
picked[:] = 0
# Still contains values > 5
print(a.max())
