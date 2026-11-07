"""
23 - pandas: Series and DataFrame
=================================

A **Series** is a 1-D labeled array; a **DataFrame** is a table of columns,
each column a Series with its own dtype. Both carry an **index** (row labels).

Run the whole file:  uv run python src/23-pandas-dataframe.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Series

# %%
# pandas is imported as pd by convention
import pandas as pd

# A Series: values plus an index of labels
s = pd.Series([10, 20, 30], index=["a", "b", "c"])
# Print it
print(s)
# Access by label and by position -> 20 10
print(s["b"], s.iloc[0])
# Vectorized arithmetic, like NumPy
print((s * 2).tolist())
# The underlying NumPy array
print(s.to_numpy())

# %% [markdown]
# ## Index alignment
# Arithmetic between Series matches **labels**, not positions. Labels missing on
# one side produce `NaN`.

# %%
# pandas
import pandas as pd

# Two Series with partly overlapping labels
a = pd.Series([1, 2, 3], index=["x", "y", "z"])
# A second Series in a different order
b = pd.Series([10, 20, 30], index=["z", "y", "w"])
# Values are added by label; w and x have no partner -> NaN
print(a + b)

# %% [markdown]
# ## Creating a DataFrame

# %%
# pandas
import pandas as pd

# From a dict of columns
df = pd.DataFrame({
    "city":  ["Tehran", "Berlin", "Tehran", "Tokyo", "Berlin", "Tokyo"],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Jan"],
    "sales": [120, 95, 140, 80, 110, None],
})
# Print the table; None became NaN and `sales` became float64
print(df)
# The dtype of each column (pandas 3 has a dedicated str dtype)
print(df.dtypes)
# Every column is a Series
print(type(df["city"]))
# From a list of row dicts
rows = pd.DataFrame([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
# Print it
print(rows)

# %% [markdown]
# ## Index, columns and shape

# %%
# pandas
import pandas as pd

# The sample data
df = pd.DataFrame({
    "city":  ["Tehran", "Berlin", "Tehran", "Tokyo", "Berlin", "Tokyo"],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Jan"],
    "sales": [120, 95, 140, 80, 110, None],
})
# Rows and columns
print(df.shape)
# Column labels and the row index
print(df.columns.tolist(), df.index)
# Use a column as the index
by_city = df.set_index("city")
# Rows can now be selected by city name
print(by_city.loc["Berlin"])
# reset_index() turns the index back into a column
print(by_city.reset_index().columns.tolist())
