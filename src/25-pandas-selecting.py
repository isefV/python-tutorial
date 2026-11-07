"""
25 - pandas: selecting & filtering
==================================

`.loc` selects by **label** (slice end inclusive), `.iloc` by **position**
(slice end exclusive). Boolean masks filter rows.

Run the whole file:  uv run python src/25-pandas-selecting.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Columns

# %%
# pandas
import pandas as pd

# The sample data
df = pd.DataFrame({
    "city":  ["Tehran", "Berlin", "Tehran", "Tokyo", "Berlin", "Tokyo"],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Jan"],
    "sales": [120, 95, 140, 80, 110, None],
})
# One column -> Series
print(df["sales"])
# A list of columns -> DataFrame
print(df[["city", "sales"]])

# %% [markdown]
# ## loc and iloc

# %%
# pandas
import pandas as pd

# The sample data
df = pd.DataFrame({
    "city":  ["Tehran", "Berlin", "Tehran", "Tokyo", "Berlin", "Tokyo"],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Jan"],
    "sales": [120, 95, 140, 80, 110, None],
})
# One cell by row label and column label -> Tehran
print(df.loc[0, "city"])
# Label slices INCLUDE the end: rows 0, 1 and 2
print(df.loc[0:2, ["city", "sales"]])
# Position slices EXCLUDE the end: rows 0 and 1, columns 0 and 1
print(df.iloc[0:2, 0:2])
# Last row by position
print(df.iloc[-1])

# %% [markdown]
# ## Boolean filtering
# Use `&`, `|`, `~` (not `and`/`or`/`not`) and wrap each condition in parentheses.

# %%
# pandas
import pandas as pd

# The sample data
df = pd.DataFrame({
    "city":  ["Tehran", "Berlin", "Tehran", "Tokyo", "Berlin", "Tokyo"],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Jan"],
    "sales": [120, 95, 140, 80, 110, None],
})
# Rows where sales > 100, only two columns
print(df.loc[df["sales"] > 100, ["city", "sales"]])
# Two conditions combined with &
print(df[(df["sales"] > 90) & (df["month"] == "Jan")])
# isin() tests membership in a list
print(df[df["city"].isin(["Berlin", "Tokyo"])])
# ~ negates a mask: rows that are NOT missing
print(df[~df["sales"].isna()])

# %% [markdown]
# ## query() and between()

# %%
# pandas
import pandas as pd

# The sample data
df = pd.DataFrame({
    "city":  ["Tehran", "Berlin", "Tehran", "Tokyo", "Berlin", "Tokyo"],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Jan"],
    "sales": [120, 95, 140, 80, 110, None],
})
# query() takes an expression as a string
print(df.query("city == 'Berlin' and sales > 100"))
# @name refers to a Python variable
limit = 100
# Use the variable inside the query
print(df.query("sales >= @limit"))
# between() is inclusive on both ends
print(df[df["sales"].between(90, 120)])
