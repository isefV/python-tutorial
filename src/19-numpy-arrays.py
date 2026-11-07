"""
19 - NumPy: the ndarray
=======================

An `ndarray` is an N-dimensional array of **one dtype** stored in contiguous
memory. Operations run as compiled loops, which is why NumPy is fast.

Run the whole file:  uv run python src/19-numpy-arrays.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Creating arrays

# %%
# NumPy is imported as np by convention
import numpy as np

# From a Python list; NumPy picks the dtype (int64 here)
a = np.array([1, 2, 3])
# Show the array and its dtype
print(a, a.dtype)
# Mixing ints and floats upcasts everything to float64
print(np.array([1, 2.5]).dtype)
# Arrays filled with zeros / ones / a constant
print(np.zeros((2, 3)), np.ones(4), np.full((2, 2), 7), sep="\n")
# Like range(), but returns an array -> [0 2 4 6 8]
print(np.arange(0, 10, 2))
# N evenly spaced values including both ends
print(np.linspace(0, 1, 5))
# The identity matrix
print(np.eye(3))

# %% [markdown]
# ## Shape, dtype and reshaping

# %%
# NumPy
import numpy as np

# 12 numbers reshaped into 3 rows and 4 columns
a = np.arange(12).reshape(3, 4)
# Print the 2-D array
print(a)
# Dimensions, number of axes, number of elements, element type
print(a.shape, a.ndim, a.size, a.dtype)
# Bytes per element and in total
print(a.itemsize, a.nbytes)
# -1 lets NumPy infer one dimension -> shape (2, 6)
print(a.reshape(2, -1).shape)
# Transpose swaps the axes -> (4, 3)
print(a.T.shape)
# Flatten to 1-D
print(a.ravel())
# astype() converts to another dtype (makes a copy)
print(a.astype(np.float32).dtype)
# Back to nested Python lists
print(a.tolist())

# %% [markdown]
# ## Random arrays
# Use a `Generator` from `default_rng()`; pass a seed for reproducible results.

# %%
# NumPy
import numpy as np

# A seeded random generator
rng = np.random.default_rng(42)
# Uniform floats in [0, 1)
print(rng.random(3))
# Integers in [0, 10)
print(rng.integers(0, 10, size=5))
# A 2x3 matrix of normally distributed values (mean 0, std 1)
print(rng.normal(0, 1, size=(2, 3)).round(2))

# %% [markdown]
# ## Why it is fast
# The same computation as a Python loop and as one vectorized expression.

# %%
# NumPy
import numpy as np
# timeit measures small snippets
import timeit

# One million random floats
x = np.random.default_rng(0).random(1_000_000)
# The same numbers as a Python list
xs = x.tolist()
# Pure Python: a generator expression over a list
t_python = timeit.timeit(lambda: sum(v * v for v in xs), number=3) / 3
# NumPy: one expression, executed in compiled code
t_numpy = timeit.timeit(lambda: (x * x).sum(), number=3) / 3
# Compare the timings
print(f"python {t_python * 1000:.1f} ms | numpy {t_numpy * 1000:.1f} ms | {t_python / t_numpy:.0f}x faster")
