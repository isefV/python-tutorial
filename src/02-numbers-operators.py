"""
02 - Numbers, booleans & operators
==================================

Integer and float arithmetic, comparisons, truthiness and the operators
that differ from C-family languages.

Run the whole file:  uv run python src/02-numbers-operators.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Integer arithmetic
# Python ints have arbitrary precision. `/` always returns a float; `//` is floor
# division.

# %%
# Ints never overflow
print(2 ** 100)
# True division always returns a float -> 3.5
print(7 / 2)
# Floor division -> 3
print(7 // 2)
# Floor division rounds toward negative infinity -> -4
print(-7 // 2)
# The sign of % follows the divisor -> 2
print(-7 % 3)
# divmod() returns quotient and remainder together -> (3, 2)
print(divmod(17, 5))

# %% [markdown]
# ## Floats and complex numbers

# %%
# Import math for isclose()
import math

# Floats are IEEE 754 doubles, so this is False
print(0.1 + 0.2 == 0.3)
# Compare floats with a tolerance instead -> True
print(math.isclose(0.1 + 0.2, 0.3))
# Complex numbers are built in; j marks the imaginary part
z = 3 + 4j
# Real part, imaginary part and magnitude -> 3.0 4.0 5.0
print(z.real, z.imag, abs(z))
# Underscores make long literals readable
print(1_000_000)

# %% [markdown]
# ## Comparisons and identity
# `==` compares **values**, `is` compares **identity** (same object). Use `is`
# only for `None` (and other singletons).

# %%
# A sample value
x = 5
# Chained comparison, same as (1 < x) and (x <= 10)
print(1 < x <= 10)
# Two different list objects with equal content
a, b = [1, 2], [1, 2]
# Equal values, but not the same object -> True False
print(a == b, a is b)
# A variable that holds None
value = None
# The idiomatic None check -> True
print(value is None)

# %% [markdown]
# ## Truthiness
# Empty containers, zero, `None` and `""` are *falsy*; almost everything else is
# *truthy*. Write `if items:` rather than `if len(items) > 0:`.

# %%
# Check how different values behave in a boolean context
for value in [0, 0.0, "", [], {}, set(), None, "text", [0]]:
    # bool() shows what an if-statement would see
    print(f"{value!r:8} -> {bool(value)}")

# %% [markdown]
# ## `and` / `or` return operands; the walrus operator

# %%
# `or` returns the first truthy operand (handy for defaults)
name = "" or "default"
# Prints default
print(name)
# `and` stops at the first falsy operand, so 1 / 0 is never evaluated
print(0 and 1 / 0)
# Sample data
data = [1, 2, 3, 4]
# := assigns inside an expression (here: inside the if-condition)
if (n := len(data)) > 3:
    # n is available inside the block
    print(f"list is long ({n} items)")

# %% [markdown]
# ## Bitwise operators and augmented assignment
# There is no `++`/`--`; use `+=`/`-=`.

# %%
# Binary literals with the 0b prefix
a, b = 0b1100, 0b1010
# AND, OR, XOR shown as binary strings
print(bin(a & b), bin(a | b), bin(a ^ b))
# Shift left by 2 multiplies by 4 -> 48
print(a << 2)
# bool is a subclass of int -> 2
print(True + True)
# Start a counter
counter = 0
# Same as counter = counter + 1
counter += 1
# Prints 1
print(counter)
