"""
11 - Classes
============

Defining classes, instance vs class attributes, properties, class methods
and static methods. `self` is the explicit `this`.

Run the whole file:  uv run python src/11-classes.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## A complete small class

# %%
# A class is a blueprint for objects
class Account:
    # Class attribute: shared by all instances
    bank = "PyBank"

    # __init__ initializes a new instance; self is that instance
    def __init__(self, owner: str, balance: float = 0):
        # Instance attribute: one per object
        self.owner = owner
        # A leading underscore means "internal" by convention
        self._balance = balance

    # A property is read like an attribute: acc.balance
    @property
    def balance(self) -> float:
        # Return the internal value
        return self._balance

    # A regular method
    def deposit(self, amount: float) -> None:
        # Validate the input
        if amount <= 0:
            # Signal invalid input with an exception
            raise ValueError("amount must be positive")
        # Update the internal state
        self._balance += amount

    # __repr__ controls how the object is displayed
    def __repr__(self) -> str:
        # !r puts quotes around the owner string
        return f"Account({self.owner!r}, {self._balance})"


# Create an instance: no `new` keyword
acc = Account("Ada", 100)
# Call a method
acc.deposit(50)
# Read the property (no parentheses) -> 150
print(acc.balance)
# print() falls back to __repr__ -> Account('Ada', 150)
print(acc)
# A class attribute is reachable through the class and the instances
print(Account.bank, acc.bank)

# %% [markdown]
# ## Properties with a setter
# Start with a plain attribute; switch to a property later without changing the
# callers. No `getX()` / `setX()` needed.

# %%
# A class with a validated attribute
class Temperature:
    # The assignment below goes through the property setter
    def __init__(self, celsius: float):
        # Calls the setter
        self.celsius = celsius

    # Getter: runs on t.celsius
    @property
    def celsius(self) -> float:
        # Return the stored value
        return self._celsius

    # Setter: runs on t.celsius = value
    @celsius.setter
    def celsius(self, value: float) -> None:
        # Reject impossible temperatures
        if value < -273.15:
            # Raise for invalid values
            raise ValueError("below absolute zero")
        # Store the validated value
        self._celsius = value

    # A computed, read-only property
    @property
    def fahrenheit(self) -> float:
        # Converted on every access
        return self.celsius * 9 / 5 + 32


# Create a temperature
t = Temperature(25)
# Prints 77.0
print(t.fahrenheit)
# Assignments go through the validation
try:
    # This raises ValueError
    t.celsius = -300
# Handle the error
except ValueError as err:
    # Print the message
    print("rejected:", err)

# %% [markdown]
# ## classmethod and staticmethod

# %%
# date is used to compute an age
from datetime import date


# A class with an alternative constructor and a helper
class Person:
    # The regular initializer
    def __init__(self, name: str, born: int):
        # Store the name
        self.name = name
        # Store the birth year
        self.born = born

    # A classmethod receives the class (cls): ideal for alternative constructors
    @classmethod
    def from_string(cls, text: str) -> "Person":
        # Parse "name,year"
        name, year = text.split(",")
        # cls(...) also does the right thing for subclasses
        return cls(name, int(year))

    # A staticmethod is a plain function in the class namespace
    @staticmethod
    def is_adult(age: int) -> bool:
        # Neither self nor cls is needed
        return age >= 18

    # A normal method that uses instance data
    def age(self) -> int:
        # Years since birth
        return date.today().year - self.born


# Build an object from a string
p = Person.from_string("Ada,1990")
# Use the instance method and the static method
print(p.name, Person.is_adult(p.age()))

# %% [markdown]
# ## No access modifiers
# `_x` is "internal" by convention only; `__x` is renamed (name-mangled) to avoid
# clashes in subclasses.

# %%
# A class with two "private-ish" attributes
class Box:
    # Set both attributes
    def __init__(self):
        # Internal by convention only
        self._internal = 1
        # Stored as _Box__hidden
        self.__hidden = 2


# Create a box
b = Box()
# _internal is still accessible -> 1
print(b._internal)
# __hidden is only reachable under its mangled name -> 2
print(b._Box__hidden)
# vars() shows the instance's attribute dictionary
print(vars(b))
