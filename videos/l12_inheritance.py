from lesson import *
from l11_classes import obj_box


class L12Inheritance(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 12, "inheritance-dataclasses", "Inheritance, dunders and dataclasses", "Python"

    def construct(self):
        self.intro("Lesson twelve: inheritance, dunder methods and dataclasses. These are the tools that let "
                   "your own classes behave like Python's built-in types.",
                   r"\texttt{super()}, operator overloading, \texttt{@dataclass}, \texttt{Protocol}")
        self.inherit()
        self.dunders()
        self.dataclasses()
        self.ducks()
        self.outro([r"A subclass overrides methods; \texttt{super()} calls the parent's version.",
                    r"Dunder methods plug your class into operators and built-ins.",
                    r"\texttt{@dataclass} writes \texttt{\_\_init\_\_}, \texttt{\_\_repr\_\_}, \texttt{\_\_eq\_\_} for you.",
                    r"Duck typing: what matters is the methods an object has."],
                   "Override methods and reach the parent with super, implement dunders to support operators, "
                   "let dataclass write the boilerplate, and rely on behaviour rather than inheritance.")

    def inherit(self):
        h = self.heading("Inheritance and polymorphism")
        animal = obj_box("class Animal", ["__init__(name)", "speak() -> '...'", "introduce()"], C_PURPLE, width=4.4)
        dog = obj_box("class Dog(Animal)", ["__init__(name, breed)", "speak() -> 'Woof'"], C_BLUE, width=4.4)
        inst = obj_box("d = Dog('Rex', 'collie')", ["name = 'Rex'", "breed = 'collie'"], C_GREEN, width=4.0)
        inst.move_to(LEFT * 4.3 + DOWN * 1.2)
        dog.move_to(RIGHT * 0.3 + DOWN * 1.2)
        animal.move_to(RIGHT * 4.5 + UP * 1.0)
        a1 = Arrow(inst[0].get_right(), dog[0].get_left(), buff=0.12, color=GREY_B)
        a2 = Arrow(dog[0].get_right(), animal[0].get_left() + DOWN * 0.3, buff=0.12, color=GREY_B)
        with self.say("Dog inherits from Animal. Its init calls super dot init to let the parent set the name, "
                      "then adds a breed. Dog overrides speak, but not introduce."):
            self.play(FadeIn(animal), FadeIn(dog), GrowArrow(a2))
            self.play(FadeIn(inst), GrowArrow(a1))
        with self.say("Now call d dot introduce. Lookup walks the method resolution order: the instance, Dog, "
                      "then Animal, where introduce is found. Inside it, self dot speak starts the search again "
                      "from the instance, and finds Dog's speak. That's polymorphism: Rex says Woof."):
            q = mono("d.introduce()", 30, color=C_YELLOW).to_edge(UP, buff=1.0).to_edge(LEFT, buff=0.8)
            self.play(FadeIn(q))
            dot = Dot(color=C_YELLOW, radius=0.12).move_to(inst[0])
            self.play(FadeIn(dot, scale=2))
            self.play(dot.animate.move_to(dog[0]), run_time=0.8)
            self.play(dot.animate.move_to(animal[2][2]), run_time=0.8)
            self.play(Circumscribe(animal[2][2], color=C_YELLOW))
            q2 = mono("self.speak()", 26, color=C_GOLD).next_to(q, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(FadeIn(q2))
            self.play(dot.animate.move_to(inst[0]), run_time=0.8)
            self.play(dot.animate.move_to(dog[2][1]), run_time=0.8)
            self.play(Circumscribe(dog[2][1], color=C_GOLD))
            out = mono("'Rex says Woof'", 30, color=C_GREEN).next_to(q, RIGHT, buff=0.6)
            self.play(FadeIn(out))
        self.clear(keep=[h])
        self.h = h

    def dunders(self):
        h = self.swap_heading(self.h, "Dunder methods")
        pairs = [("v + w", "v.__add__(w)"), ("v * 3", "v.__mul__(3)"), ("v == w", "v.__eq__(w)"),
                 ("len(v)", "v.__len__()"), ("v[0]", "v.__getitem__(0)"), ("print(v)", "v.__repr__()")]
        left = VGroup(*[mono(a, 30) for a, _ in pairs]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        right = VGroup(*[mono(b, 30, color=C_GOLD) for _, b in pairs])
        left.move_to(LEFT * 3.2 + DOWN * 0.2)
        for l, r in zip(left, right):
            r.move_to([1.0, l.get_y(), 0], aligned_edge=LEFT)
        arrows = VGroup(*[Arrow(l.get_right() + RIGHT * 0.1, [0.85, l.get_y(), 0], buff=0, color=GREY_B,
                                stroke_width=3, max_tip_length_to_length_ratio=0.15) for l in left])
        for a, l in zip(arrows, left):
            a.put_start_and_end_on([-1.2, l.get_y(), 0], [0.8, l.get_y(), 0])
        with self.say("Operators and built-ins are just syntax for special methods with double underscores. "
                      "v plus w calls v dot dunder add. len calls dunder len, square brackets call dunder getitem, "
                      "and printing uses dunder repr. Define them, and your class works with the syntax."):
            for l, a, r in zip(left, arrows, right):
                self.play(FadeIn(l), GrowArrow(a), FadeIn(r, shift=0.2 * LEFT), run_time=0.7)
            res = mono("Vector(1, 2) + Vector(3, 4)  ->  Vector(4, 6)", 26, color=C_YELLOW).to_edge(DOWN, buff=0.5)
            self.play(FadeIn(res))
        self.clear(keep=[h])
        self.h = h

    def dataclasses(self):
        h = self.swap_heading(self.h, "dataclasses")
        code = code_panel("@dataclass(frozen=True)\nclass Point:\n    x: float\n    y: float = 0.0\n\n"
                          "@dataclass\nclass Order:\n    customer: str\n    items: list[str] = field(default_factory=list)",
                          font_size=20).to_edge(LEFT, buff=0.5)
        gen = VGroup(*[pill(t, C_GREEN, 24) for t in ["__init__", "__repr__", "__eq__"]]).arrange(DOWN, buff=0.3)
        gen.move_to(RIGHT * 4.6 + UP * 0.6)
        with self.say("Most small classes just hold data. The dataclass decorator reads the annotated fields "
                      "and writes init, repr and equality for you. frozen makes instances immutable and hashable."):
            self.play(FadeIn(code))
            arr = Arrow(code.get_right() + UP * 0.8, gen.get_left(), color=C_GREEN, buff=0.2)
            self.play(GrowArrow(arr), LaggedStart(*[FadeIn(g, shift=0.2 * LEFT) for g in gen], lag_ratio=0.3))
        with self.say("For mutable defaults, use field with a default factory, so each order gets its own list, "
                      "avoiding the shared-default trap from lesson five."):
            hl = SurroundingRectangle(code.code_lines[8], color=C_GOLD, buff=0.05)
            ex = mono("Order(customer='Ada', items=['book'])", 24, color=C_YELLOW).to_edge(DOWN, buff=0.6)
            self.play(Create(hl), FadeIn(ex))
        self.clear(keep=[h])
        self.h = h

    def ducks(self):
        h = self.swap_heading(self.h, "Duck typing and Protocol")
        code = code_panel("class Readable(Protocol):\n    def read(self) -> str: ...\n\ndef shout(source: Readable):\n"
                          "    return source.read().upper()", font_size=26).to_edge(UP, buff=1.0)
        a = obj_box("FakeFile()", ["read()"], C_BLUE, width=3.0)
        b = obj_box("io.StringIO(...)", ["read()", "write()", "seek()"], C_TEAL, width=3.0)
        VGroup(a, b).arrange(RIGHT, buff=2.0, aligned_edge=UP).next_to(code, DOWN, buff=0.7)
        with self.say("If it walks like a duck... Python doesn't care about an object's class, only whether it "
                      "has the methods you call. A Protocol writes that expectation down for type checkers: "
                      "anything with a read method is readable, no inheritance required."):
            self.play(FadeIn(code))
            self.play(FadeIn(a), FadeIn(b))
            self.play(Circumscribe(a[2][0], color=C_GREEN), Circumscribe(b[2][0], color=C_GREEN))
        self.clear()
