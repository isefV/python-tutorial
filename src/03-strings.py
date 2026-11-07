"""
03 - Strings
============

Strings are immutable sequences of Unicode characters. Indexing and
slicing work like on every other sequence; f-strings are the way to format.

Run the whole file:  uv run python src/03-strings.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Indexing and slicing
# `s[start:stop:step]` - `stop` is exclusive, negative indices count from the end.

# %%
# ' and " are equivalent
s = "Hello, Python"
# First and last character -> H n
print(s[0], s[-1])
# From index 7 to the end -> Python
print(s[7:])
# Every second character -> Hlo yhn
print(s[::2])
# A negative step reverses -> nohtyP ,olleH
print(s[::-1])
# len() counts characters (code points)
print(len(s))

# %% [markdown]
# ## Common methods
# Every method returns a **new** string.

# %%
# A sample string
s = "Hello, Python"
# Case conversion
print(s.upper(), s.lower())
# split() breaks a string into a list
print(s.split(", "))
# join() is the inverse: glue a list together with a separator
print("-".join(["a", "b", "c"]))
# strip() removes surrounding whitespace
print(repr("  hi  ".strip()))
# replace() substitutes substrings
print("abc".replace("b", "B"))
# Searching
print(s.startswith("He"), s.find("P"), "py" in s.lower())
# Character tests
print("42".isdigit(), "abc".isalpha())

# %% [markdown]
# ## f-strings
# Expressions inside `{}` are evaluated; a format spec follows a colon.

# %%
# Values to format
name, pi = "Ada", 3.14159
# Two decimals, thousands separator, percentage
print(f"{pi:.2f} | {1234567:,} | {0.25:.0%}")
# !r uses repr(); >6 right-aligns in 6 characters
print(f"[{name!r:>6}]")
# Zero-padding and hexadecimal
print(f"{7:03d} {255:x} {255:#b}")
# {expr=} prints the expression and its value (debugging)
print(f"{pi=}")
# Any expression works inside the braces
print(f"{name.upper()} has {len(name)} letters")

# %% [markdown]
# ## Other literals
# Raw strings keep backslashes, triple quotes span lines, `bytes` hold binary
# data.

# %%
# Raw string: backslashes are not escape characters
print(r"C:\new\table")
# A normal string with escape sequences: newline and tab
print("line1\n\tline2")
# Triple quotes span several lines
text = """first line
second line"""
# Split it back into lines
print(text.splitlines())
# encode() turns str into bytes; decode() reverses it
data = "café".encode("utf-8")
# bytes are not str; é takes two bytes in UTF-8
print(data, len(data), data.decode("utf-8"))

# %% [markdown]
# ## Strings are immutable

# %%
# A sample string
s = "Hello"
# Item assignment is not allowed
try:
    # This raises TypeError
    s[0] = "J"
# Show the error
except TypeError as err:
    # Print the message
    print("TypeError:", err)
# Build a new string instead
s = "J" + s[1:]
# Prints Jello
print(s)
