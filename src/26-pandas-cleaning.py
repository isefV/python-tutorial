"""
26 - pandas: cleaning & transforming
====================================

Handle missing values, derive new columns, use the `.str` and `.dt`
accessors, and chain methods. Avoid chained assignment: pandas 3 always uses
Copy-on-Write.

Run the whole file:  uv run python src/26-pandas-cleaning.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Missing values

# %%
# pandas
import pandas as pd

# The sample data
df = pd.DataFrame({
    "city":  ["Tehran", "Berlin", "Tehran", "Tokyo", "Berlin", "Tokyo"],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Jan"],
    "sales": [120, 95, 140, 80, 110, None],
})
# Drop rows with any missing value
print(df.dropna())
# Replace missing values with a constant (returns a new Series)
print(df["sales"].fillna(0).tolist())
# Or with a statistic of the column
print(df["sales"].fillna(df["sales"].mean()).tolist())

# %% [markdown]
# ## New columns and type conversion

# %%
# pandas
import pandas as pd

# The sample data
df = pd.DataFrame({
    "city":  ["Tehran", "Berlin", "Tehran", "Tokyo", "Berlin", "Tokyo"],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Jan"],
    "sales": [120, 95, 140, 80, 110, None],
})
# Assign the cleaned column back
df["sales"] = df["sales"].fillna(0)
# A vectorized derived column
df["tax"] = df["sales"] * 0.1
# A boolean column
df["big"] = df["sales"] > 100
# Convert a column's dtype
df = df.astype({"sales": "int64"})
# Rename columns
df = df.rename(columns={"sales": "revenue"})
# Print the result
print(df)

# %% [markdown]
# ## String and date accessors

# %%
# pandas
import pandas as pd

# A small table with text and dates
df = pd.DataFrame({
    "name": [" ada lovelace", "Alan Turing ", "grace HOPPER"],
    "joined": ["2024-01-15", "2024-03-02", "2025-07-30"],
})
# .str applies string methods to every value
df["name"] = df["name"].str.strip().str.title()
# Split into first and last name
df[["first", "last"]] = df["name"].str.split(" ", expand=True)
# Parse text into datetimes
df["joined"] = pd.to_datetime(df["joined"])
# .dt exposes date parts
df["year"] = df["joined"].dt.year
# Print the result
print(df)

# %% [markdown]
# ## Method chaining
# Each method returns a new DataFrame, so steps can be chained into one readable
# pipeline.

# %%
# pandas
import pandas as pd

# The sample data
df = pd.DataFrame({
    "city":  ["Tehran", "Berlin", "Tehran", "Tokyo", "Berlin", "Tokyo"],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Jan"],
    "sales": [120, 95, 140, 80, 110, None],
})
# A pipeline of transformations
clean = (
    df.dropna(subset=["sales"])
      .assign(tax=lambda d: d["sales"] * 0.1)
      .sort_values("sales", ascending=False)
      .reset_index(drop=True)
)
# Print the result
print(clean)

# %% [markdown]
# ## No chained assignment
# `df[mask]["col"] = value` modifies a temporary copy and leaves `df` unchanged
# (pandas 3 emits a `ChainedAssignmentError` warning). Use a single `.loc`.

# %%
# warnings lets us capture the warning for display
import warnings
# pandas
import pandas as pd

# The sample data
df = pd.DataFrame({
    "city":  ["Tehran", "Berlin", "Tehran", "Tokyo", "Berlin", "Tokyo"],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Jan"],
    "sales": [120, 95, 140, 80, 110, None],
})
# Add a column to modify
df["tax"] = 1.0
# Capture warnings instead of printing them to stderr
with warnings.catch_warnings(record=True) as caught:
    # Make sure the warning is recorded
    warnings.simplefilter("always")
    # WRONG: assigns into a temporary copy
    df[df["sales"] > 100]["tax"] = 0
# The warning name and the unchanged column
print([type(w.message).__name__ for w in caught], df["tax"].tolist())
# RIGHT: one .loc call with a row mask and a column label
df.loc[df["sales"] > 100, "tax"] = 0
# Now the matching rows are updated
print(df["tax"].tolist())

# %% [markdown]
# ## Vectorize instead of apply
# `apply` with `axis=1` runs a Python function per row; a column expression is
# much faster and usually shorter.

# %%
# NumPy for np.where
import numpy as np
# pandas
import pandas as pd

# The sample data
df = pd.DataFrame({
    "city":  ["Tehran", "Berlin", "Tehran", "Tokyo", "Berlin", "Tokyo"],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Jan"],
    "sales": [120, 95, 140, 80, 110, None],
})
# Slow style: a Python function called once per row
df["label_slow"] = df.apply(lambda row: "big" if row["sales"] > 100 else "small", axis=1)
# Fast style: one vectorized expression
df["label_fast"] = np.where(df["sales"] > 100, "big", "small")
# Same result
print(df[["sales", "label_slow", "label_fast"]])
