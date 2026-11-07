"""
06 - Control flow: if and match
===============================

`if`/`elif`/`else`, the conditional expression and structural pattern
matching (`match`, Python 3.10+).

Run the whole file:  uv run python src/06-control-flow.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## if / elif / else

# %%
# A sample score
score = 82
# No parentheses around the condition; a colon starts the block
if score >= 90:
    # Runs when the first condition is true
    grade = "A"
# elif means "else if"
elif score >= 75:
    # Runs when the second condition is true
    grade = "B"
# else catches everything else
else:
    # Fallback grade
    grade = "C"
# Prints B
print(grade)

# %% [markdown]
# ## Conditional expression and `pass`

# %%
# A sample age
age = 20
# <value if true> if <condition> else <value if false>
status = "adult" if age >= 18 else "minor"
# Prints adult
print(status)
# pass is an empty statement, a placeholder for an empty block
if age < 0:
    # Nothing to do yet
    pass

# %% [markdown]
# ## match: sequence patterns
# `match` destructures values. No fall-through and no `break` needed.

# %%
# Interpret a text command
def handle(command: str) -> str:
    # Split into words and match the resulting list
    match command.split():
        # Exactly two words starting with "go": capture the second one
        case ["go", direction]:
            # Use the captured value
            return f"moving {direction}"
        # | separates alternatives
        case ["quit" | "exit"]:
            # One-word quit command
            return "bye"
        # *words captures the rest; the guard adds a condition
        case ["say", *words] if words:
            # Join the captured words
            return " ".join(words)
        # _ is the wildcard and matches anything
        case _:
            # Default branch
            return "unknown command"


# Try a few commands
for cmd in ["go north", "exit", "say hello world", "dance"]:
    # Show command and result
    print(f"{cmd!r:18} -> {handle(cmd)}")

# %% [markdown]
# ## match: dict and class patterns

# %%
# A dataclass can be matched by its fields
from dataclasses import dataclass


# A simple 2-D point
@dataclass
class Point:
    # x coordinate
    x: float
    # y coordinate
    y: float


# Describe different kinds of values
def describe(event) -> str:
    # Match on the shape of the value
    match event:
        # Dict pattern with a nested tuple pattern
        case {"type": "click", "pos": (x, y)}:
            # x and y are bound from the tuple
            return f"click at {x},{y}"
        # Class pattern with literal sub-patterns
        case Point(x=0, y=0):
            # Exactly the origin
            return "origin"
        # Class pattern that captures the attributes
        case Point(x=x, y=y):
            # Any other point
            return f"point {x},{y}"
        # Anything else
        case _:
            # Fallback
            return "unknown"


# Try three different values
for event in [{"type": "click", "pos": (3, 4)}, Point(0, 0), Point(1, 2)]:
    # Print the description
    print(describe(event))
