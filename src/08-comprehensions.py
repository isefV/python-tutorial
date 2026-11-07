"""
08 - Comprehensions
===================

`[expr for x in iterable if condition]` builds a list in one expression.
The same shape works for sets `{}`, dicts `{k: v}` and lazy generators `()`.

Run the whole file:  uv run python src/08-comprehensions.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## List, set and dict comprehensions

# %%
# Sample data
nums = [3, 1, 4, 1, 5, 9, 2, 6]
# Squares of the even numbers -> [16, 4, 36]
print([n * n for n in nums if n % 2 == 0])
# A set comprehension removes duplicates -> {0, 1, 2}
print({n % 3 for n in nums})
# A dict comprehension maps keys to values
print({word: len(word) for word in ["hi", "hey"]})

# %% [markdown]
# ## Generator expressions
# Parentheses instead of brackets produce values lazily; no list is built.
# Perfect as the argument of `sum`, `any`, `all`, `max`, ...

# %%
# Sample data
nums = [3, 1, 4, 1, 5, 9, 2, 6]
# Sum of squares without building a list -> 173
print(sum(n * n for n in nums))
# any() stops at the first True -> True
print(any(n > 8 for n in nums))
# all() stops at the first False -> False
print(all(n > 1 for n in nums))
# A generator expression is an object you can iterate later
squares = (n * n for n in nums)
# Take the first value from it
print(next(squares))

# %% [markdown]
# ## Conditional values and nested loops

# %%
# Sample data
nums = [1, 2, 3, 4]
# A conditional expression inside the comprehension (no filter)
print(["even" if n % 2 == 0 else "odd" for n in nums])
# Two for-clauses: read them left to right like nested loops
print([(x, y) for x in range(2) for y in "ab"])
# Flatten a list of lists
matrix = [[1, 2], [3, 4], [5, 6]]
# The outer loop comes first
print([value for row in matrix for value in row])

# %% [markdown]
# ## When to use a normal loop instead
# If the logic needs several statements, a loop is more readable.

# %%
# Sample records
orders = [("ann", 30), ("bob", -5), ("cy", 12)]
# Collect messages with a plain loop
messages = []
# Several steps per item are clearer in a loop
for name, amount in orders:
    # Skip invalid rows
    if amount < 0:
        # Move on to the next order
        continue
    # Compute a derived value
    tax = round(amount * 0.1, 2)
    # Store a formatted message
    messages.append(f"{name}: {amount} (+{tax} tax)")
# Show the result
print(messages)
