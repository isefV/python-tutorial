"""
14 - Files & context managers
=============================

Reading and writing files with `open()` and `pathlib`, the standard data
formats (JSON, CSV) and writing your own context managers. All examples work in
a temporary folder, so nothing is left on disk.

Run the whole file:  uv run python src/14-files-context-managers.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Writing and reading text files
# `with` closes the file automatically, even if an error occurs.
#
# | Mode | Meaning |
# |---|---|
# | `r` | read (default) |
# | `w` | write, truncates first |
# | `a` | append |
# | `x` | create, fail if it exists |
# | `b` | binary, e.g. `rb` |

# %%
# pathlib gives OS-independent paths
from pathlib import Path
# tempfile gives a scratch folder that is deleted afterwards
import tempfile

# Work inside a temporary directory
with tempfile.TemporaryDirectory() as tmp:
    # The / operator joins path parts
    path = Path(tmp) / "data" / "notes.txt"
    # Create the parent folder; no error if it already exists
    path.parent.mkdir(parents=True, exist_ok=True)
    # "w" opens for writing; always pass an explicit encoding for text
    with open(path, "w", encoding="utf-8") as f:
        # write() does not add a newline
        f.write("first line\n")
        # Write a second line
        f.write("second line\n")
    # "a" appends to the end of the file
    with open(path, "a", encoding="utf-8") as f:
        # Add a third line
        f.write("third line\n")
    # The default mode is "r" (read text)
    with open(path, encoding="utf-8") as f:
        # Iterating a file yields lines lazily (memory friendly)
        for number, line in enumerate(f, start=1):
            # rstrip() removes the trailing newline
            print(number, line.rstrip())

# %% [markdown]
# ## pathlib helpers

# %%
# Path for path handling
from pathlib import Path
# tempfile for a scratch folder
import tempfile

# Work inside a temporary directory
with tempfile.TemporaryDirectory() as tmp:
    # Build a file path
    path = Path(tmp) / "report.txt"
    # write_text() writes a whole file in one call
    path.write_text("hello\nworld\n", encoding="utf-8")
    # read_text() reads the whole file into one string
    print(path.read_text(encoding="utf-8").splitlines())
    # Parts of a path
    print(path.name, path.stem, path.suffix, path.exists())
    # Create a few empty files
    for name in ["a.csv", "b.csv", "c.txt"]:
        # touch() creates an empty file
        (Path(tmp) / name).touch()
    # glob() finds files by pattern
    print(sorted(p.name for p in Path(tmp).glob("*.csv")))

# %% [markdown]
# ## JSON and CSV

# %%
# CSV support
import csv
# In-memory text "files"
import io
# JSON support
import json

# A Python dict to serialize
config = {"name": "demo", "debug": True, "levels": [1, 2, 3]}
# dumps() converts Python objects to a JSON string (dump() writes to a file)
text = json.dumps(config, indent=2)
# Show the JSON text
print(text)
# loads() parses JSON back into Python objects (load() reads a file)
print(json.loads(text)["levels"])
# An in-memory file to write CSV into
buffer = io.StringIO()
# DictWriter writes dicts as rows
writer = csv.DictWriter(buffer, fieldnames=["city", "sales"])
# Header row
writer.writeheader()
# Two data rows
writer.writerows([{"city": "Tehran", "sales": 120}, {"city": "Berlin", "sales": 95}])
# Rewind to the beginning before reading
buffer.seek(0)
# DictReader yields every row as a dict
for row in csv.DictReader(buffer):
    # Note: CSV values are always strings
    print(row)

# %% [markdown]
# ## Writing a context manager with `@contextmanager`

# %%
# Measuring time
import time
# Turns a generator function into a context manager
from contextlib import contextmanager


# Code before `yield` runs on enter, code after it on exit
@contextmanager
def timer(label: str):
    # Enter: remember the start time
    start = time.perf_counter()
    # try/finally guarantees the exit code runs even on errors
    try:
        # Hand control to the body of the with-block
        yield
    # Exit: report the elapsed time
    finally:
        # Print the elapsed seconds
        print(f"{label}: {time.perf_counter() - start:.4f}s")


# Use it like any other context manager
with timer("sum of squares"):
    # The work being timed
    total = sum(i * i for i in range(100_000))
# The result is available after the block
print(total)

# %% [markdown]
# ## A class-based context manager
# Any object with `__enter__` and `__exit__` works with `with`.

# %%
# Track indentation for nested output
class Indent:
    # Shared nesting level
    level = 0

    # Runs when the with-block starts; the return value is bound by `as`
    def __enter__(self):
        # Go one level deeper
        Indent.level += 1
        # Return self so the block can call methods on it
        return self

    # Runs when the block ends, also after an exception
    def __exit__(self, exc_type, exc, tb):
        # Go back one level
        Indent.level -= 1
        # Returning False lets exceptions propagate
        return False

    # Print with the current indentation
    def say(self, text: str) -> None:
        # Two spaces per level
        print("  " * Indent.level + text)


# Nested with-blocks
with Indent() as outer:
    # Level one
    outer.say("level one")
    # Enter a nested block
    with Indent() as inner:
        # Level two
        inner.say("level two")
    # Back to level one
    outer.say("back to one")
