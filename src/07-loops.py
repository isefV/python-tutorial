"""
07 - Loops
==========

Python has no C-style `for(;;)`: a `for` loop iterates **over the items** of
any iterable. `enumerate`, `zip` and `range` cover the index-based cases.

Run the whole file:  uv run python src/07-loops.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## for and range

# %%
# for iterates over the items of any iterable
for x in [10, 20, 30]:
    # x takes each value in turn
    print(x)
# range(stop) and range(start, stop, step); stop is exclusive
print(list(range(5)), list(range(10, 0, -3)))

# %% [markdown]
# ## enumerate, zip and dict.items

# %%
# Two parallel lists
names = ["ann", "bob", "cy"]
# Ages matching the names by position
ages = [31, 25, 19]
# enumerate() yields (index, item); start= sets the first index
for i, name in enumerate(names, start=1):
    # A numbered list
    print(i, name)
# zip() walks several iterables in parallel and stops at the shortest
for name, age in zip(names, ages):
    # Name and age together
    print(name, age)
# A dict to iterate over
config = {"debug": True, "level": 3}
# .items() yields (key, value) pairs
for key, value in config.items():
    # One setting per line
    print(key, "=", value)

# %% [markdown]
# ## while, break and continue

# %%
# A list used as a queue of work items
queue = ["a", None, "b", "STOP", "c"]
# Reverse it so pop() returns the items in their original order
queue.reverse()
# Loop while the list is non-empty (truthy)
while queue:
    # Take the next item
    item = queue.pop()
    # Skip None values
    if item is None:
        # continue jumps to the next iteration
        continue
    # Stop at the sentinel
    if item == "STOP":
        # break leaves the loop; "c" is never processed
        break
    # Process the item
    print("processing", item)

# %% [markdown]
# ## `else` on a loop
# The `else` block runs only when the loop finished **without** `break`.

# %%
# Report the first even number, or that there is none
def first_even(numbers):
    # Look at each number
    for n in numbers:
        # Is it even?
        if n % 2 == 0:
            # Report it
            print("found", n)
            # break also skips the else clause
            break
    # Runs only if the loop did not break
    else:
        # Nothing found
        print("no even number")


# A list with an even number -> found 8
first_even([3, 5, 8, 9])
# A list without one -> no even number
first_even([3, 5, 7])

# %% [markdown]
# ## Reversed iteration and safe filtering
# Don't add or remove items of a list while looping over it; build a new list.

# %%
# Iterate backwards without copying
for ch in reversed("abc"):
    # Prints c b a on one line
    print(ch, end=" ")
# Finish the line
print()
# A list to filter
nums = [1, 2, 3, 4, 5, 6]
# Build a new list with only the odd numbers
nums = [n for n in nums if n % 2]
# Prints [1, 3, 5]
print(nums)
