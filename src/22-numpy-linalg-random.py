"""
22 - NumPy: linear algebra, random & toolbox
============================================

Matrix operations with `@` and `np.linalg`, random sampling, and the most
useful helper functions.

Run the whole file:  uv run python src/22-numpy-linalg-random.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Linear algebra
# `*` is element-wise; `@` is matrix multiplication.

# %%
# NumPy
import numpy as np

# A 2x2 matrix and a vector
A = np.array([[2, 1], [1, 3]])
# Right-hand side
b = np.array([3, 5])
# Matrix product
print(A @ A)
# Element-wise product (different!)
print(A * A)
# Solve the system Ax = b -> [0.8 1.4]
print(np.linalg.solve(A, b))
# Inverse and determinant
print(np.linalg.inv(A).round(2), round(np.linalg.det(A), 6))
# Eigenvalues and eigenvectors; eigh() is for symmetric matrices like A
values, vectors = np.linalg.eigh(A)
# Show the eigenvalues -> [1.382 3.618]
print(values.round(3))
# Vector length (Euclidean norm)
print(np.linalg.norm(b).round(3))

# %% [markdown]
# ## Random sampling

# %%
# NumPy
import numpy as np

# A seeded generator for reproducible results
rng = np.random.default_rng(seed=42)
# Integers in [0, 10) -> [0 7 6 4 4]
print(rng.integers(0, 10, size=5))
# 1000 normal samples; their mean and std are close to 0 and 1
samples = rng.normal(loc=0, scale=1, size=1000)
# Summary of the sample
print(samples.mean().round(2), samples.std().round(2))
# Pick random elements
print(rng.choice(["a", "b", "c"], size=4))
# A random permutation of 0..9
print(rng.permutation(10))

# %% [markdown]
# ## Combining, sorting and missing values

# %%
# NumPy
import numpy as np

# Two small arrays
a, b = np.array([3, 1, 2]), np.array([9, 8, 7])
# Join end to end
print(np.concatenate([a, b]))
# Stack as rows of a new 2-D array
print(np.stack([a, b]))
# Sorted copy, sorting indices, unique values
print(np.sort(a), np.argsort(a), np.unique([3, 1, 3, 2]))
# NaN marks missing values in float arrays
x = np.array([1.0, np.nan, 3.0])
# Normal functions propagate NaN; nan-functions ignore it
print(np.mean(x), np.nanmean(x), np.isnan(x))
# Clip values into a range
print(np.clip([-5, 0, 5, 10], 0, 6))
# Compare floats with a tolerance
print(np.allclose([0.1 + 0.2], [0.3]))

# %% [markdown]
# ## Saving and loading arrays

# %%
# NumPy
import numpy as np
# A temporary folder for the files
import tempfile
# Path handling
from pathlib import Path

# A small array
a = np.arange(6).reshape(2, 3)
# Work in a scratch folder
with tempfile.TemporaryDirectory() as tmp:
    # .npy is NumPy's fast binary format
    np.save(Path(tmp) / "a.npy", a)
    # Load it back
    print(np.load(Path(tmp) / "a.npy"))
    # Plain-text formats are also available
    np.savetxt(Path(tmp) / "a.csv", a, delimiter=",", fmt="%d")
    # Read the text back
    print((Path(tmp) / "a.csv").read_text())
