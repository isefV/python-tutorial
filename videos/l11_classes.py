from lesson import *


def obj_box(title, rows, color, width=3.6, size=22):
    """An object drawn as a titled box with attribute rows."""
    lines = VGroup(*[mono(r, size) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    box = RoundedRectangle(corner_radius=0.15, width=width, height=lines.height + 0.9, stroke_color=color,
                           fill_color=color, fill_opacity=0.08)
    t = mono(title, 20, color=color).next_to(box, UP, buff=0.08, aligned_edge=LEFT)
    lines.move_to(box).shift(DOWN * 0.05)
    lines.align_to(box, LEFT).shift(RIGHT * 0.3)
    return VGroup(box, t, lines)


class L11Classes(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 11, "classes", "Classes", "Python"

    def construct(self):
        self.intro("Lesson eleven: classes. Python's object model is simple and open: self is the explicit "
                   "this, attributes live in dictionaries, and properties let you add logic without changing "
                   "how callers use your class.", r"instances, properties, classmethod, staticmethod")
        self.account()
        self.lookup()
        self.properties()
        self.ctors()
        self.outro([r"\texttt{\_\_init\_\_} sets up a new instance; \texttt{self} is passed explicitly.",
                    r"Attribute lookup: the instance first, then its class.",
                    r"\texttt{@property} turns a method into a validated attribute.",
                    r"\texttt{@classmethod} builds alternative constructors."],
                   "init sets up each instance, self is just the first argument, lookups fall back from "
                   "instance to class, and properties add logic behind plain attribute syntax.")

    def account(self):
        h = self.heading("A small class")
        code = code_panel('class Account:\n    bank = "PyBank"\n\n    def __init__(self, owner, balance=0):\n'
                          '        self.owner = owner\n        self._balance = balance\n\n    def deposit(self, amount):\n'
                          '        self._balance += amount\n\nacc = Account("Ada", 100)\nacc.deposit(50)',
                          font_size=22).to_edge(LEFT, buff=0.4)
        mk = Marker(code)
        with self.say("class creates a new type. The double-underscore init method runs right after a new "
                      "instance is created, and stores attributes on self. self is simply the instance, passed "
                      "explicitly as the first parameter."):
            self.play(FadeIn(code), mk.to(3, 5))
            self.play(mk.to(10))
            inst = obj_box("acc: Account", ["owner = 'Ada'", "_balance = 100"], C_BLUE).move_to(RIGHT * 3.6 + DOWN * 0.6)
            self.play(FadeIn(inst, shift=0.2 * UP))
        with self.say("Calling acc dot deposit of fifty is really Account dot deposit of acc and fifty: the method "
                      "is found on the class, and the instance is passed in as self."):
            self.play(mk.to(11))
            eq = mono("Account.deposit(acc, 50)", 26, color=C_YELLOW).move_to(RIGHT * 3.6 + UP * 2.2)
            self.play(FadeIn(eq))
            nv = mono("_balance = 150", 22, color=C_YELLOW).move_to(inst[2][1], aligned_edge=LEFT)
            self.play(Transform(inst[2][1], nv))
        self.inst = inst
        self.clear(keep=[h])
        self.h = h

    def lookup(self):
        h = self.swap_heading(self.h, "Instance and class attributes")
        cls = obj_box("class Account", ["bank = 'PyBank'", "__init__()", "deposit()"], C_PURPLE).move_to(RIGHT * 3.2 + UP * 0.6)
        inst = obj_box("acc", ["owner = 'Ada'", "_balance = 150"], C_BLUE).move_to(LEFT * 3.2 + UP * 0.6)
        link = Arrow(inst[0].get_right(), cls[0].get_left(), buff=0.15, color=GREY_B)
        lk = mono("__class__", 20, color=GREY_B).next_to(link, UP, buff=0.1)
        with self.say("Attributes assigned in init belong to each instance. Attributes in the class body, like "
                      "bank, belong to the class and are shared by all instances."):
            self.play(FadeIn(inst), FadeIn(cls))
            self.play(GrowArrow(link), FadeIn(lk))
        with self.say("When you read acc dot bank, Python looks in the instance first. It's not there, so it "
                      "follows the link to the class and finds it. Methods are found the same way."):
            q = mono("acc.bank", 32, color=C_YELLOW).move_to(DOWN * 2.3)
            self.play(FadeIn(q))
            dot = Dot(color=C_YELLOW, radius=0.12).move_to(inst[0].get_center())
            self.play(FadeIn(dot, scale=2), Indicate(inst[0], color=C_GREY))
            self.play(MoveAlongPath(dot, Line(inst[0].get_center(), cls[2][0].get_left() + LEFT * 0.15)), run_time=1.2)
            self.play(Circumscribe(cls[2][0], color=C_YELLOW))
            ans = mono("-> 'PyBank'", 32, color=C_YELLOW).next_to(q, RIGHT, buff=0.4)
            self.play(FadeIn(ans))
        self.clear(keep=[h])
        self.h = h

    def properties(self):
        h = self.swap_heading(self.h, "Properties")
        code = code_panel('class Temperature:\n    @property\n    def celsius(self):\n        return self._celsius\n\n'
                          '    @celsius.setter\n    def celsius(self, value):\n        if value < -273.15:\n'
                          '            raise ValueError("too cold")\n        self._celsius = value',
                          font_size=20).to_edge(LEFT, buff=0.4)
        mk = Marker(code)
        con = Console(width=5.3, height=2.2, font_size=20).to_edge(RIGHT, buff=0.35)
        with self.say("Python has no getters and setters by habit. Start with a plain attribute. If you later "
                      "need logic, turn it into a property: callers still write t dot celsius, but now a method "
                      "runs behind the scenes."):
            self.play(FadeIn(code), FadeIn(con), mk.to(1, 3))
            self.play(con.print("t.celsius        # reads"))
        with self.say("The setter can validate. Assigning minus three hundred is rejected with a value error. "
                      "A property without a setter, like fahrenheit, is read-only and computed on demand."):
            self.play(mk.to(5, 9, color=C_GOLD))
            self.play(con.print("t.celsius = -300", color=C_GOLD))
            self.play(con.print("ValueError: too cold", color=C_BAD))
            self.play(con.print("t.fahrenheit     # 77.0", color=C_GREEN))
        self.clear(keep=[h])
        self.h = h

    def ctors(self):
        h = self.swap_heading(self.h, "classmethod, staticmethod, privacy")
        code = code_panel('class Person:\n    @classmethod\n    def from_string(cls, text):\n        name, year = text.split(",")\n'
                          '        return cls(name, int(year))\n\n    @staticmethod\n    def is_adult(age):\n        return age >= 18\n\n'
                          'p = Person.from_string("Ada,1990")', font_size=20).to_edge(LEFT, buff=0.4)
        mk = Marker(code)
        with self.say("A classmethod receives the class instead of an instance, which makes it perfect for "
                      "alternative constructors like from string. A staticmethod receives neither; it's just a "
                      "function that lives in the class's namespace."):
            self.play(FadeIn(code), mk.to(1, 4))
            self.play(mk.to(10))
            self.play(mk.to(6, 8, color=C_TEAL))
        with self.say("There are no access modifiers. A leading underscore means internal, by convention. "
                      "Two underscores trigger name mangling, which avoids clashes in subclasses but hides nothing."):
            rows = VGroup(mono("self._internal  # by convention", 20, color=C_GREY),
                          mono("self.__hidden   # -> _Box__hidden", 20, color=C_GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            rows.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.2)
            self.play(LaggedStart(*[FadeIn(r, shift=0.2 * LEFT) for r in rows], lag_ratio=0.4))
        self.clear()
