"""
30 - Matplotlib: customizing & saving
=====================================

Styles, colors, ticks, scales, shared axes, saving to files and plotting
directly from pandas.

Run the whole file:  uv run python src/30-matplotlib-customizing.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Styling lines, ticks and scales

# %%
# NumPy for data
import numpy as np
# pyplot
import matplotlib.pyplot as plt

# Data
x = np.linspace(0.1, 10, 50)
# Two panels sharing the y-axis
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(8, 3), layout="constrained")
# Color, width, marker and line style
ax1.plot(x, x ** 2, color="tab:blue", linewidth=2, marker="o", markersize=3, linestyle="--")
# A light grid
ax1.grid(alpha=0.3)
# Custom tick positions and labels
ax1.set_xticks([0, 5, 10], ["start", "mid", "end"])
# A log scale on the second panel
ax2.plot(x, x ** 2)
# Logarithmic x-axis
ax2.set_xscale("log")
# A title for the whole figure
fig.suptitle("Two panels, shared y-axis")
# Display
plt.show()

# %% [markdown]
# ## Style sheets and global defaults

# %%
# NumPy for data
import numpy as np
# pyplot
import matplotlib.pyplot as plt

# List a few of the available styles
print(plt.style.available[:5])
# Apply a style only inside this block
with plt.style.context("ggplot"):
    # Some data
    x = np.linspace(0, 10, 100)
    # A figure in the ggplot style
    fig, ax = plt.subplots(figsize=(5, 3))
    # Draw a line
    ax.plot(x, np.sin(x))
    # Title
    ax.set_title("ggplot style")
    # Display
    plt.show()
# rcParams changes defaults globally, e.g. plt.rcParams["font.size"] = 11
print(plt.rcParams["font.size"])

# %% [markdown]
# ## Saving figures
# Vector formats (`pdf`, `svg`) for documents, raster (`png`) with a `dpi` for
# screens.

# %%
# A temporary folder for the files
import tempfile
# Path handling
from pathlib import Path
# pyplot
import matplotlib.pyplot as plt

# A simple figure
fig, ax = plt.subplots(figsize=(4, 3))
# Some bars
ax.bar(["a", "b", "c"], [3, 1, 2])
# Save into a scratch folder
with tempfile.TemporaryDirectory() as tmp:
    # Vector output
    fig.savefig(Path(tmp) / "plot.pdf", bbox_inches="tight")
    # Raster output at 200 dots per inch
    fig.savefig(Path(tmp) / "plot.png", dpi=200, bbox_inches="tight")
    # List what was written
    print(sorted(p.name for p in Path(tmp).iterdir()))
# Close the figure to free memory (useful in loops)
plt.close(fig)

# %% [markdown]
# ## Plotting from pandas
# `df.plot(...)` returns an ordinary Matplotlib `Axes`, so all the customization
# above still applies.

# %%
# pandas
import pandas as pd
# pyplot
import matplotlib.pyplot as plt

# A small table
df = pd.DataFrame({"month": ["Jan", "Feb", "Mar"], "sales": [120, 95, 140], "costs": [80, 70, 90]})
# A grouped bar chart straight from the DataFrame
ax = df.plot(x="month", y=["sales", "costs"], kind="bar", rot=0, figsize=(5, 3))
# Customize the returned Axes like any other
ax.set_ylabel("amount")
# Title
ax.set_title("pandas -> Matplotlib")
# Display
plt.show()
