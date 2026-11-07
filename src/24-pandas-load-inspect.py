"""
24 - pandas: load & inspect
===========================

Reading data (`read_csv`, `read_excel`, `read_parquet`, `read_sql`, ...)
and the first commands you run on a new dataset. The CSV here lives in memory
so the example runs anywhere.

Run the whole file:  uv run python src/24-pandas-load-inspect.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Reading CSV

# %%
# In-memory text file
import io
# pandas
import pandas as pd

# CSV text; normally this would be a file path
csv_text = """city,month,sales
Tehran,Jan,120
Berlin,Jan,95
Tehran,Feb,140
Tokyo,Feb,80
Berlin,Feb,110
Tokyo,Jan,
"""
# read_csv() accepts a path, a URL or a file-like object
df = pd.read_csv(io.StringIO(csv_text))
# First rows
print(df.head(3))
# Last rows
print(df.tail(2))

# %% [markdown]
# ## Structure and summary statistics

# %%
# pandas
import pandas as pd

# The sample data
df = pd.DataFrame({
    "city":  ["Tehran", "Berlin", "Tehran", "Tokyo", "Berlin", "Tokyo"],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Jan"],
    "sales": [120, 95, 140, 80, 110, None],
})
# (rows, columns)
print(df.shape)
# Column types
print(df.dtypes)
# Columns, non-null counts and memory usage
df.info()
# Statistics of the numeric columns; count excludes NaN
print(df.describe())
# include="all" also summarizes text columns
print(df.describe(include="all"))

# %% [markdown]
# ## Values, counts and missing data

# %%
# pandas
import pandas as pd

# The sample data
df = pd.DataFrame({
    "city":  ["Tehran", "Berlin", "Tehran", "Tokyo", "Berlin", "Tokyo"],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Jan"],
    "sales": [120, 95, 140, 80, 110, None],
})
# Frequency of each value
print(df["city"].value_counts())
# Distinct values and how many there are
print(df["city"].unique(), df["city"].nunique())
# Missing values per column
print(df.isna().sum())
# Rows that contain any missing value
print(df[df.isna().any(axis=1)])

# %% [markdown]
# ## Writing data

# %%
# pandas
import pandas as pd

# The sample data
df = pd.DataFrame({
    "city":  ["Tehran", "Berlin", "Tehran", "Tokyo", "Berlin", "Tokyo"],
    "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Jan"],
    "sales": [120, 95, 140, 80, 110, None],
})
# to_csv() without a path returns the CSV text; index=False drops the index
print(df.to_csv(index=False))
# JSON, one object per row
print(df.head(2).to_json(orient="records"))
# Other writers: to_excel, to_parquet, to_sql, to_markdown, ...
