"""
31 - Putting it together: NumPy -> pandas -> Matplotlib
=======================================================

Generate synthetic data with NumPy, aggregate it with pandas and plot the
result with Matplotlib.

Run the whole file:  uv run python src/31-end-to-end.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Generate the raw data with NumPy

# %%
# NumPy for random data
import numpy as np
# pandas for the table
import pandas as pd

# A seeded generator for reproducible results
rng = np.random.default_rng(42)
# One row per day of 2025 and three cities
n, cities = 365, ["Tehran", "Berlin", "Tokyo"]
# Build the DataFrame from NumPy arrays
df = pd.DataFrame({
    "date": pd.date_range("2025-01-01", periods=n),
    "city": rng.choice(cities, size=n),
    "sales": rng.normal(100, 20, size=n).round(1),
})
# A first look
print(df.head())
# Rows per city
print(df["city"].value_counts())

# %% [markdown]
# ## Aggregate per month and city with pandas

# %%
# NumPy
import numpy as np
# pandas
import pandas as pd

# Re-create the raw data so this cell runs on its own
rng = np.random.default_rng(42)
# Same parameters as above
n, cities = 365, ["Tehran", "Berlin", "Tokyo"]
# The raw table
df = pd.DataFrame({
    "date": pd.date_range("2025-01-01", periods=n),
    "city": rng.choice(cities, size=n),
    "sales": rng.normal(100, 20, size=n).round(1),
})
# Group by month end ("ME") and city, sum, then move cities into columns
monthly = (
    df.groupby([pd.Grouper(key="date", freq="ME"), "city"])["sales"]
      .sum()
      .unstack("city")
)
# Use short month names as the index
monthly.index = monthly.index.strftime("%b")
# A 12 x 3 table
print(monthly.round(0))

# %% [markdown]
# ## Plot the result with Matplotlib

# %%
# NumPy
import numpy as np
# pandas
import pandas as pd
# pyplot
import matplotlib.pyplot as plt

# Re-create the raw data so this cell runs on its own
rng = np.random.default_rng(42)
# Same parameters as above
n, cities = 365, ["Tehran", "Berlin", "Tokyo"]
# The raw table
df = pd.DataFrame({
    "date": pd.date_range("2025-01-01", periods=n),
    "city": rng.choice(cities, size=n),
    "sales": rng.normal(100, 20, size=n).round(1),
})
# The monthly table from the previous step
monthly = df.groupby([pd.Grouper(key="date", freq="ME"), "city"])["sales"].sum().unstack("city")
# Short month names
monthly.index = monthly.index.strftime("%b")
# One line per city
ax = monthly.plot(marker="o", figsize=(7, 3.5))
# Labels and title
ax.set(xlabel="", ylabel="monthly sales", title="Monthly sales by city (synthetic data)")
# A light grid
ax.grid(alpha=0.3)
# Display
plt.show()
