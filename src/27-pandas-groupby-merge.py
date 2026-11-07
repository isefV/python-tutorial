"""
27 - pandas: group, aggregate, reshape, join
============================================

Split-apply-combine with `groupby`, reshaping with `pivot_table` and
`melt`, and SQL-style joins with `merge`.

| SQL | pandas |
|---|---|
| `WHERE` | `df[mask]`, `df.query(...)` |
| `GROUP BY` | `df.groupby(...).agg(...)` |
| `JOIN` | `df.merge(other, on=...)` |
| `ORDER BY` | `df.sort_values(...)` |
| `LIMIT n` | `df.head(n)` |
| `UNION ALL` | `pd.concat([...])` |

Run the whole file:  uv run python src/27-pandas-groupby-merge.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## groupby and agg

# %%
# pandas
import pandas as pd

# The sample data
df = pd.DataFrame({
    "city":  ["Tehran", "Berlin", "Tehran", "Tokyo", "Berlin", "Tokyo"],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Jan"],
    "sales": [120, 95, 140, 80, 110, None],
})
# Several aggregations of one column per group; NaN is skipped
print(df.groupby("city")["sales"].agg(["sum", "mean", "count"]))
# Named aggregations give the result columns clear names
print(df.groupby("city").agg(total=("sales", "sum"), months=("month", "nunique")))
# as_index=False keeps the group key as a normal column
print(df.groupby("city", as_index=False)["sales"].sum().sort_values("sales", ascending=False))

# %% [markdown]
# ## transform: group statistics on every row

# %%
# pandas
import pandas as pd

# The sample data
df = pd.DataFrame({
    "city":  ["Tehran", "Berlin", "Tehran", "Tokyo", "Berlin", "Tokyo"],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Jan"],
    "sales": [120, 95, 140, 80, 110, None],
})
# transform() returns one value per original row
df["city_total"] = df.groupby("city")["sales"].transform("sum")
# Each row's share of its city's total
df["share"] = (df["sales"] / df["city_total"]).round(2)
# Print the result
print(df)

# %% [markdown]
# ## Reshaping: pivot_table and melt

# %%
# pandas
import pandas as pd

# The sample data
df = pd.DataFrame({
    "city":  ["Tehran", "Berlin", "Tehran", "Tokyo", "Berlin", "Tokyo"],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Jan"],
    "sales": [120, 95, 140, 80, 110, None],
})
# Long -> wide: cities as rows, months as columns
wide = df.pivot_table(index="city", columns="month", values="sales", aggfunc="sum")
# Print the wide table
print(wide)
# Wide -> long again
long = wide.reset_index().melt(id_vars="city", var_name="month", value_name="sales")
# Print the long table
print(long)

# %% [markdown]
# ## Joining and concatenating

# %%
# pandas
import pandas as pd

# The sample data
df = pd.DataFrame({
    "city":  ["Tehran", "Berlin", "Tehran", "Tokyo", "Berlin", "Tokyo"],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Jan"],
    "sales": [120, 95, 140, 80, 110, None],
})
# A lookup table
countries = pd.DataFrame({
    "city": ["Tehran", "Berlin", "Paris"],
    "country": ["IR", "DE", "FR"],
})
# Left join: keep every row of df; Tokyo has no match -> NaN
print(df.merge(countries, on="city", how="left"))
# Inner join: only matching rows
print(df.merge(countries, on="city", how="inner").shape)
# Stack two frames on top of each other (UNION ALL)
print(pd.concat([df.head(2), df.tail(2)], ignore_index=True))
