"""
17 - Modules, packages & the standard library
=============================================

Every `.py` file is a module; a folder of modules is a package. The
standard library covers a lot before you need anything from PyPI.

Run the whole file:  uv run python src/17-modules-stdlib.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Import forms

# %%
# Import a whole module and use it with a prefix
import math
# Import a module under an alias (the community convention for some libs)
import statistics as stats
# Import selected names into the current namespace
from pathlib import Path, PurePosixPath

# Use the module prefix
print(math.sqrt(2))
# Use the alias
print(stats.mean([1, 2, 3, 4]))
# Use the imported names directly
print(Path("a") / "b", PurePosixPath("x/y").name)
# Avoid `from module import *`: it hides where names come from

# %% [markdown]
# ## The `__main__` guard
# A module's top-level code runs on import. Put the program's entry point behind
# `if __name__ == "__main__":` so it runs only when the file is executed directly.

# %%
# The entry point of a script
def main() -> None:
    # The real work would go here
    print("running main()")


# __name__ is "__main__" when run directly, the module name when imported
if __name__ == "__main__":
    # Call the entry point
    main()

# %% [markdown]
# ## Dates and times

# %%
# datetime types
from datetime import date, datetime, timedelta

# A fixed date
release = date(2025, 10, 7)
# Date arithmetic with timedelta
print(release + timedelta(days=30))
# Parse a string into a datetime
stamp = datetime.strptime("2025-01-31 14:05", "%Y-%m-%d %H:%M")
# Format it back into text
print(stamp.strftime("%d %b %Y, %H:%M"))
# ISO format is the safe interchange format
print(stamp.isoformat())

# %% [markdown]
# ## Regular expressions

# %%
# The re module
import re

# Some text to search
text = "Order 42 shipped on 2025-01-31, order 7 on 2025-02-02"
# findall() returns all matches of a pattern
print(re.findall(r"\d{4}-\d{2}-\d{2}", text))
# Groups capture parts of a match
for match in re.finditer(r"[Oo]rder (\d+)", text):
    # group(1) is the first captured group
    print("order id:", match.group(1))
# sub() replaces matches
print(re.sub(r"\d+", "#", "a1b22c333"))

# %% [markdown]
# ## Randomness, statistics and functools.partial

# %%
# Pseudo-random numbers
import random
# Basic statistics
import statistics
# partial() pre-fills some arguments
from functools import partial

# A seeded generator gives reproducible results
rng = random.Random(42)
# Random integers in [1, 6]
print([rng.randint(1, 6) for _ in range(5)])
# Pick and shuffle
print(rng.choice(["red", "green", "blue"]))
# Statistics on a list
data = [2, 4, 4, 4, 5, 5, 7, 9]
# Mean, median and population standard deviation
print(statistics.mean(data), statistics.median(data), statistics.pstdev(data))
# A new function with base=2 fixed
parse_binary = partial(int, base=2)
# -> 5
print(parse_binary("101"))

# %% [markdown]
# ## Command-line arguments, logging and subprocesses

# %%
# Command-line parsing
import argparse
# Structured logging
import logging
# Running other programs
import subprocess
# sys.executable is the path of the running Python
import sys

# Define the arguments a script accepts
parser = argparse.ArgumentParser(description="demo tool")
# A positional argument
parser.add_argument("name")
# An optional flag with a type and a default
parser.add_argument("--count", type=int, default=1)
# Parse an explicit list (normally it reads sys.argv)
args = parser.parse_args(["Ada", "--count", "2"])
# Access the values as attributes
print(args.name, args.count)
# Configure logging once at program start
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s", force=True)
# Log a message
logging.info("processing %s", args.name)
# Run another program and capture its output
result = subprocess.run([sys.executable, "-c", "print(6 * 7)"], capture_output=True, text=True)
# Prints 42
print(result.stdout.strip())
