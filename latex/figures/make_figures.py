"""Generate the figures used in python-for-programmers.tex.

Run from anywhere:  python src/figures/make_figures.py
Needs: numpy, pandas, matplotlib
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent

# Validated categorical palette (first three slots are safe for any chart form)
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 6.5,
    "axes.prop_cycle": matplotlib.cycler(color=[BLUE, ORANGE, AQUA]),
    "axes.edgecolor": INK2,
    "axes.labelcolor": INK2,
    "axes.titlecolor": INK,
    "axes.titlesize": 7.5,
    "axes.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": GRID,
    "grid.linewidth": 0.5,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "axes.axisbelow": True,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "lines.linewidth": 1.3,
    "lines.markersize": 3,
    "legend.fontsize": 6.5,
    "legend.frameon": False,
    "figure.dpi": 150,
})


def plot_types():
    """2x2 grid: line, scatter, bar, histogram (matches the slide code)."""
    rng = np.random.default_rng(0)
    x = np.linspace(0, 2 * np.pi, 100)

    fig, axs = plt.subplots(2, 2, figsize=(3.3, 2.6), layout="constrained")

    axs[0, 0].plot(x, np.sin(x), label="sin")
    axs[0, 0].plot(x, np.cos(x), label="cos")
    axs[0, 0].set_title("Line")
    axs[0, 0].set_ylim(-1.7, 1.2)
    axs[0, 0].legend(loc="lower center", ncols=2)

    xs = rng.normal(size=200)
    axs[0, 1].scatter(xs, xs + rng.normal(scale=0.5, size=200),
                      s=6, alpha=0.7, edgecolors="white", linewidths=0.3)
    axs[0, 1].set_title("Scatter")

    axs[1, 0].bar(["A", "B", "C", "D"], [42, 27, 31, 18], width=0.6)
    axs[1, 0].set_title("Bar")
    axs[1, 0].grid(axis="x", visible=False)

    axs[1, 1].hist(rng.normal(size=1000), bins=30,
                   edgecolor="white", linewidth=0.5)
    axs[1, 1].set_title("Histogram")

    fig.savefig(OUT / "plot_types.pdf")
    plt.close(fig)


def oo_example():
    """Object-oriented API example with labels, annotation and limits."""
    x = np.linspace(0, 10, 200)
    fig, ax = plt.subplots(figsize=(2.7, 1.9), layout="constrained")
    ax.plot(x, np.exp(-x / 3) * np.sin(2 * x), label="damped")
    ax.plot(x, np.exp(-x / 3), "--", label="envelope")
    ax.set(xlabel="time [s]", ylabel="amplitude",
           title="Damped oscillation", xlim=(0, 10))
    ax.annotate("peak", xy=(0.7, 0.78), xytext=(2.8, 0.85),
                arrowprops=dict(arrowstyle="->", color=INK2), color=INK2)
    ax.legend()
    fig.savefig(OUT / "oo_example.pdf")
    plt.close(fig)


def pandas_pipeline():
    """End-to-end: synthetic daily sales -> monthly totals per city -> plot."""
    rng = np.random.default_rng(42)
    df = pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=365, freq="D"),
        "city": rng.choice(["Tehran", "Berlin", "Tokyo"], size=365),
        "sales": rng.normal(100, 20, size=365).round(1),
    })
    monthly = (
        df.groupby([pd.Grouper(key="date", freq="ME"), "city"])["sales"]
          .sum()
          .unstack("city")
    )
    monthly.index = monthly.index.strftime("%b")   # Jan, Feb, ...
    ax = monthly.plot(figsize=(2.9, 2.1), marker="o", markersize=2.5)
    ax.set(xlabel="", ylabel="monthly sales")
    ax.legend(title=None, ncols=3, loc="lower left",
              bbox_to_anchor=(0, 1.0), borderaxespad=0.2)
    ax.figure.savefig(OUT / "pandas_pipeline.pdf", bbox_inches="tight")
    plt.close(ax.figure)
    return monthly


if __name__ == "__main__":
    plot_types()
    oo_example()
    print(pandas_pipeline().round(0).head(3))
    print("figures written to", OUT)
