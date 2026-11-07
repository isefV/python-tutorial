"""
12 - Inheritance, dunder methods & dataclasses
==============================================

Subclassing with `super()`, operator overloading through "dunder"
(double underscore) methods, `@dataclass` and duck typing with `Protocol`.

Run the whole file:  uv run python src/12-inheritance-dataclasses.py
Run cell by cell:   in VS Code click "Run Cell" above each "# %%" marker.
"""

# %% [markdown]
# ## Inheritance and polymorphism

# %%
# Base class
class Animal:
    # Store the name
    def __init__(self, name: str):
        # Instance attribute
        self.name = name

    # Meant to be overridden by subclasses
    def speak(self) -> str:
        # Generic sound
        return "..."

    # Calls speak(), which dispatches to the subclass implementation
    def introduce(self) -> str:
        # Polymorphism: depends on the actual class of self
        return f"{self.name} says {self.speak()}"


# A subclass lists its base class in parentheses
class Dog(Animal):
    # Extend the initializer
    def __init__(self, name: str, breed: str):
        # super() calls the parent's implementation
        super().__init__(name)
        # Add a new attribute
        self.breed = breed

    # Override the parent method
    def speak(self) -> str:
        # Dog-specific sound
        return "Woof"


# Create a dog
d = Dog("Rex", "collie")
# Uses Animal.introduce together with Dog.speak
print(d.introduce())
# A Dog is also an Animal -> True True
print(isinstance(d, Animal), issubclass(Dog, Animal))
# The method resolution order shows where attributes are looked up
print([cls.__name__ for cls in Dog.__mro__])

# %% [markdown]
# ## Dunder methods: plug into operators and built-ins
# | Define | To support |
# |---|---|
# | `__repr__`, `__str__` | `repr(o)`, `print(o)` |
# | `__eq__`, `__lt__` | `==`, `<`, sorting |
# | `__len__`, `__getitem__` | `len(o)`, `o[i]` |
# | `__iter__`, `__contains__` | `for x in o`, `x in o` |
# | `__add__`, `__mul__` | `o + p`, `o * k` |
# | `__call__` | `o()` |
# | `__enter__`, `__exit__` | `with o:` |

# %%
# A small vector class
class Vector:
    # Store the components as a tuple
    def __init__(self, *components: float):
        # Tuples are immutable
        self.components = tuple(components)

    # Used by repr() and print()
    def __repr__(self) -> str:
        # Show the components
        return f"Vector{self.components}"

    # Used by len()
    def __len__(self) -> int:
        # Number of components
        return len(self.components)

    # Used by v[i] and, as a fallback, by iteration
    def __getitem__(self, i: int) -> float:
        # Delegate to the tuple
        return self.components[i]

    # Used by ==
    def __eq__(self, other) -> bool:
        # Equal if the other object is a Vector with the same components
        return isinstance(other, Vector) and self.components == other.components

    # Used by +
    def __add__(self, other: "Vector") -> "Vector":
        # Add component by component
        return Vector(*(a + b for a, b in zip(self, other)))

    # Used by * with a number
    def __mul__(self, k: float) -> "Vector":
        # Scale every component
        return Vector(*(a * k for a in self))


# Two vectors
v, w = Vector(1, 2), Vector(3, 4)
# Operators call the dunder methods
print(v + w, v * 3, v == Vector(1, 2))
# len(), indexing and iteration work too
print(len(v), v[0], list(w))

# %% [markdown]
# ## dataclasses
# `@dataclass` generates `__init__`, `__repr__` and `__eq__` from the annotated
# fields.

# %%
# dataclass and field come from the dataclasses module
from dataclasses import dataclass, field


# frozen=True makes instances immutable (and hashable)
@dataclass(frozen=True)
class Point:
    # A required field
    x: float
    # A field with a default value
    y: float = 0.0

    # Normal methods work as usual
    def __add__(self, other: "Point") -> "Point":
        # Return a new Point because instances are immutable
        return Point(self.x + other.x, self.y + other.y)


# Generated __repr__ plus our __add__ -> Point(x=4, y=2.0)
print(Point(1, 2) + Point(3))
# Generated __eq__ compares field by field -> True
print(Point(1, 2) == Point(1, 2))


# Mutable defaults must use default_factory
@dataclass
class Order:
    # Customer name
    customer: str
    # A fresh list for each instance
    items: list[str] = field(default_factory=list)


# Create an order
order = Order("Ada")
# Add an item to its own list
order.items.append("book")
# Prints Order(customer='Ada', items=['book'])
print(order)

# %% [markdown]
# ## Duck typing and Protocol
# Python checks **behaviour**, not declared types. `typing.Protocol` describes that
# behaviour for static type checkers.

# %%
# io.StringIO is a file-like object in memory
import io
# Protocol describes a "shape" of an object
from typing import Protocol


# Anything with a read() -> str method fits this protocol
class Readable(Protocol):
    # Only the signature matters; the body is just ...
    def read(self) -> str: ...


# A class that never mentions Readable
class FakeFile:
    # It fits the protocol simply by having read()
    def read(self) -> str:
        # Return some text
        return "hello from FakeFile"


# The parameter is annotated with the protocol
def shout(source: Readable) -> str:
    # Call read() on whatever was passed
    return source.read().upper()


# Works with our class
print(shout(FakeFile()))
# And with a standard-library object
print(shout(io.StringIO("hello from StringIO")))
