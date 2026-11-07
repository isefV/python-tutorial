"""
21 - NumPy: vectorization & broadcasting
========================================

Write **array expressions**, not loops. Broadcasting lets arrays of
different shapes combine: shapes are compared right to left, and two dimensions
fit when they are equal or one of them is 1.

Run the whole file:  uv run python src/21-numpy-broadcasting.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Element-wise operations and ufuncs

# %%
# NumPy
import numpy as np

# A small array
x = np.array([1, 2, 3])
# Operators work element by element -> [10 40 90]
print(x * np.array([10, 20, 30]))
# Scalars are broadcast to every element -> [3 5 7]
print(x * 2 + 1)
# Universal functions (ufuncs) apply math element-wise
print(np.sqrt(x).round(3), np.exp(x).round(2))
# Comparisons are element-wise too
print(x > 1)

# %% [markdown]
# ## Aggregations along an axis
# `axis=0` collapses the rows (one result per column), `axis=1` collapses the
# columns (one result per row).

# %%
# NumPy
import numpy as np

# A 3x4 example array
a = np.arange(12).reshape(3, 4)
# Sum of everything -> 66
print(a.sum())
# Per column -> [12 15 18 21]
print(a.sum(axis=0))
# Per row -> [1.5 5.5 9.5]
print(a.mean(axis=1))
# Max, index of the max (in the flattened array), standard deviation
print(a.max(), a.argmax(), a.std().round(3))
# Cumulative sums along each row
print(a.cumsum(axis=1))

# %% [markdown]
# ## Broadcasting

# %%
# NumPy
import numpy as np

# Shape (3, 4)
a = np.arange(12).reshape(3, 4)
# Shape (3, 1): one value per row
col = np.array([[10], [20], [30]])
# (3, 4) + (3, 1) -> (3, 4): the column is stretched across
print(a + col)
# Shape (4,): one value per column, broadcast down every row
row = np.array([100, 200, 300, 400])
# (3, 4) + (4,) -> (3, 4)
print(a + row)
# Incompatible shapes raise an error
try:
    # (3, 4) + (3,) does not line up from the right
    a + np.array([1, 2, 3])
# Show the error
except ValueError as err:
    # Print the message
    print("ValueError:", err)

# %% [markdown]
# ## A practical example: standardize columns
# Subtract each column's mean and divide by its standard deviation, without a
# single loop.

# %%
# NumPy
import numpy as np

# 5 samples (rows) x 3 features (columns) on very different scales
X = np.random.default_rng(1).normal([10, 200, 3000], [1, 20, 300], size=(5, 3))
# Column means and standard deviations, shape (3,)
mean, std = X.mean(axis=0), X.std(axis=0)
# Broadcasting applies them to every row
Z = (X - mean) / std
# Each column now has mean 0 and std 1
print(Z.mean(axis=0).round(6), Z.std(axis=0).round(6))
