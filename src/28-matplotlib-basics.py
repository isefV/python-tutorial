"""
28 - Matplotlib: the object model
=================================

A **Figure** is the canvas, an **Axes** is one plot inside it, and
everything drawn is an **Artist**. Use the explicit `fig, ax = plt.subplots()`
interface for anything beyond a quick look.

Run the whole file:  uv run python src/28-matplotlib-basics.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## The explicit (object-oriented) interface

# %%
# NumPy for data
import numpy as np
# pyplot creates figures
import matplotlib.pyplot as plt

# 200 points between 0 and 10
x = np.linspace(0, 10, 200)
# One figure with one Axes
fig, ax = plt.subplots(figsize=(6, 3.5))
# Draw two lines; label= feeds the legend
ax.plot(x, np.exp(-x / 3) * np.sin(2 * x), label="damped")
# A dashed line
ax.plot(x, np.exp(-x / 3), "--", label="envelope")
# Set labels, title and limits in one call
ax.set(xlabel="time [s]", ylabel="amplitude", title="Damped oscillation", xlim=(0, 10))
# An arrow pointing at the first peak
ax.annotate("peak", xy=(0.7, 0.78), xytext=(2.5, 0.85), arrowprops=dict(arrowstyle="->"))
# Show the legend
ax.legend()
# Display the figure (opens a window when run as a script)
plt.show()

# %% [markdown]
# ## The implicit pyplot interface
# Fine for a quick look; it always draws on the "current" Axes.

# %%
# NumPy for data
import numpy as np
# pyplot
import matplotlib.pyplot as plt

# Some data
x = np.linspace(0, 2 * np.pi, 100)
# plt.plot draws on the current Axes (created automatically)
plt.plot(x, np.sin(x))
# Functions mirror the Axes methods with slightly different names
plt.title("Quick look")
# Show it
plt.show()

# %% [markdown]
# ## Figure, Axes and Artists

# %%
# pyplot
import matplotlib.pyplot as plt

# A figure with two Axes side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 3))
# plot() returns a list of Line2D artists
lines = ax1.plot([1, 3, 2], marker="o")
# Artists can be modified after creation
lines[0].set_color("tab:orange")
# A bar chart returns a container of Rectangle artists
bars = ax2.bar(["a", "b", "c"], [3, 1, 2])
# Change one bar
bars[1].set_color("tab:green")
# Inspect the structure
print(type(fig).__name__, len(fig.axes), type(lines[0]).__name__, len(bars))
# Show the figure
plt.show()
