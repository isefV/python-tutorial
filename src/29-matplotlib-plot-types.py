"""
29 - Matplotlib: common plot types
==================================

Line, scatter, bar and histogram cover most needs. Others: `barh`,
`errorbar`, `fill_between`, `boxplot`, `violinplot`, `imshow`, `contour`,
`stackplot`, `pie`.

Run the whole file:  uv run python src/29-matplotlib-plot-types.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Four basic plot types in a 2x2 grid

# %%
# NumPy for data
import numpy as np
# pyplot
import matplotlib.pyplot as plt

# Reproducible random data
rng = np.random.default_rng(0)
# x values for the line plot
x = np.linspace(0, 2 * np.pi, 100)
# A 2x2 grid; constrained layout avoids overlapping labels
fig, axs = plt.subplots(2, 2, figsize=(8, 5), layout="constrained")
# Line plot with two series
axs[0, 0].plot(x, np.sin(x), label="sin")
# Second series
axs[0, 0].plot(x, np.cos(x), label="cos")
# Legend for the line plot
axs[0, 0].legend()
# Scatter plot of correlated random points
xs = rng.normal(size=200)
# s = marker size, alpha = transparency
axs[0, 1].scatter(xs, xs + rng.normal(scale=0.5, size=200), s=10, alpha=0.7)
# Bar chart of categories
axs[1, 0].bar(["A", "B", "C", "D"], [42, 27, 31, 18])
# Histogram of 1000 normal samples
axs[1, 1].hist(rng.normal(size=1000), bins=30)
# Give every Axes a title
for ax, title in zip(axs.flat, ["Line", "Scatter", "Bar", "Histogram"]):
    # set_title on each Axes
    ax.set_title(title)
# Display
plt.show()

# %% [markdown]
# ## Uncertainty: fill_between and errorbar

# %%
# NumPy for data
import numpy as np
# pyplot
import matplotlib.pyplot as plt

# x positions
x = np.arange(10)
# A mean curve
mean = np.sqrt(x)
# Two Axes side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3), layout="constrained")
# Draw the mean
ax1.plot(x, mean)
# Shade a band of +/- 0.3 around it
ax1.fill_between(x, mean - 0.3, mean + 0.3, alpha=0.3)
# Title
ax1.set_title("fill_between")
# Error bars with caps
ax2.errorbar(x, mean, yerr=0.3, fmt="o", capsize=3)
# Title
ax2.set_title("errorbar")
# Display
plt.show()

# %% [markdown]
# ## Distributions: boxplot and violinplot

# %%
# NumPy for data
import numpy as np
# pyplot
import matplotlib.pyplot as plt

# Three groups with different spreads
rng = np.random.default_rng(1)
# One array per group
groups = [rng.normal(0, s, 200) for s in (1, 2, 3)]
# Two Axes side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3), layout="constrained")
# Box plot: median, quartiles, outliers
ax1.boxplot(groups, tick_labels=["a", "b", "c"])
# Title
ax1.set_title("boxplot")
# Violin plot: the full distribution shape
ax2.violinplot(groups)
# Title
ax2.set_title("violinplot")
# Display
plt.show()

# %% [markdown]
# ## Images and heatmaps: imshow

# %%
# NumPy for data
import numpy as np
# pyplot
import matplotlib.pyplot as plt

# A 2-D grid of values
y, x = np.mgrid[-2:2:100j, -2:2:100j]
# A function of two variables
z = np.exp(-(x ** 2 + y ** 2))
# One Axes
fig, ax = plt.subplots(figsize=(4, 3.5))
# imshow draws a 2-D array as an image; extent sets the axis ranges
image = ax.imshow(z, extent=(-2, 2, -2, 2), origin="lower", cmap="viridis")
# A colorbar explains the color scale
fig.colorbar(image, ax=ax)
# Title
ax.set_title("imshow")
# Display
plt.show()
