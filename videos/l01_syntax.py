from lesson import *


class L01SyntaxBasics(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 1, "syntax-basics", "Syntax basics", "Python"

    def construct(self):
        self.intro("Lesson one: syntax basics. If you already write C, Java or JavaScript, Python will look "
                   "familiar, but it rests on a few different ideas. Let's see how a Python program is laid out.",
                   r"names, indentation, inspecting objects")
        self.names()
        self.swap()
        self.blocks()
        self.inspect()
        self.outro([r"A variable is a \emph{name} bound to an object; only objects have types.",
                    r"\texttt{a, b = b, a} packs a tuple, then unpacks it.",
                    r"A colon opens a block; indentation (4 spaces) closes it.",
                    r"\texttt{type}, \texttt{isinstance}, \texttt{dir} and \texttt{help} inspect anything."],
                   "To recap: names are labels on typed objects, tuples make swapping trivial, "
                   "indentation is the block structure, and the built-ins let you inspect any object.")

    def names(self):
        h = self.heading("Names are bound to objects")
        code = code_panel('x = 42\nx = "now a string"\nprint(x, type(x))', font_size=28)
        code.to_edge(LEFT, buff=0.6).shift(UP * 0.6)
        mk = Marker(code)
        with self.say("There are no declarations. Writing x equals 42 creates an integer object, "
                      "and binds the name x to it."):
            self.play(FadeIn(code))
            self.play(mk.to(0))
            obj = obj_circle(42, label="int").move_to(RIGHT * 4 + UP * 1.2)
            tag = name_tag("x").move_to(RIGHT * 1.2 + UP * 0.2)
            arr = pointer(tag, obj[0])
            self.play(FadeIn(obj, scale=0.6))
            self.play(FadeIn(tag, shift=0.3 * RIGHT), GrowArrow(arr))
        with self.say("Assigning a string to the same name doesn't convert anything. "
                      "A new string object is created and the label simply moves to it. "
                      "The name has no type; the object does."):
            self.play(mk.to(1))
            s = RoundedRectangle(corner_radius=0.15, width=3.6, height=0.9, stroke_color=C_NEW,
                                 fill_color=C_NEW, fill_opacity=0.15, stroke_width=3)
            sobj = VGroup(s, mono('"now a string"', 24).move_to(s),
                          mono("str", 18, color=C_NEW).next_to(s, UP, buff=0.08))
            sobj.move_to(RIGHT * 4 + DOWN * 1.2)
            self.play(FadeIn(sobj, scale=0.6))
            self.play(Transform(arr, pointer(tag, sobj[0], color=C_NAME)), run_time=1.2)
            self.play(obj.animate.set_opacity(0.25))
        with self.say("type of x asks the object it currently points to."):
            self.play(mk.to(2))
            out = mono("now a string <class 'str'>", 24, color=C_YELLOW).next_to(code, DOWN, buff=0.4,
                                                                              aligned_edge=LEFT)
            self.play(Write(out))
        self.clear(keep=[h])
        self.h = h

    def swap(self):
        h = self.swap_heading(self.h, "Multiple assignment and swapping")
        code = code_panel("a, b = 1, 2\na, b = b, a\nprint(a, b)", font_size=28)
        code.to_edge(LEFT, buff=0.6).shift(UP * 0.6)
        mk = Marker(code)
        one = obj_circle(1, label="int").move_to(RIGHT * 4.3 + UP * 1.2)
        two = obj_circle(2, label="int").move_to(RIGHT * 4.3 + DOWN * 1.2)
        ta = name_tag("a").move_to(RIGHT * 1.2 + UP * 1.2)
        tb = name_tag("b").move_to(RIGHT * 1.2 + DOWN * 1.2)
        aa, ab = pointer(ta, one[0]), pointer(tb, two[0])
        with self.say("One statement can bind several names. On the right, one comma two builds a tuple; "
                      "the left side unpacks it, item by item."):
            self.play(FadeIn(code), mk.to(0))
            tup = mono("(1, 2)", 30, color=C_GREY).move_to(RIGHT * 2.7)
            self.play(FadeIn(tup, shift=0.2 * UP))
            self.play(FadeIn(one), FadeIn(two), FadeOut(tup))
            self.play(FadeIn(ta), FadeIn(tb), GrowArrow(aa), GrowArrow(ab))
        with self.say("That gives us the classic swap with no temporary variable. "
                      "b comma a is evaluated first, into a tuple of the two objects, "
                      "and only then are the names rebound."):
            self.play(mk.to(1))
            tup = mono("(2, 1)", 30, color=C_YELLOW).move_to(RIGHT * 2.7 + UP * 2.6)
            self.play(FadeIn(tup, shift=0.2 * DOWN))
            na = Arrow(ta.get_right(), two[0].get_left(), buff=0.12, color=C_NAME, stroke_width=4,
                       max_tip_length_to_length_ratio=0.12)
            nb = Arrow(tb.get_right(), one[0].get_left(), buff=0.12, color=C_NAME, stroke_width=4,
                       max_tip_length_to_length_ratio=0.12)
            self.play(Transform(aa, na), Transform(ab, nb), run_time=1.5)
            self.play(mk.to(2))
            out = mono("2 1", 28, color=C_YELLOW).next_to(code, DOWN, buff=0.4, aligned_edge=LEFT)
            self.play(Write(out), FadeOut(tup))
        self.clear(keep=[h])
        self.h = h

    def blocks(self):
        h = self.swap_heading(self.h, "Indentation defines blocks")
        src = '''import math

def area(r):
    """Area of a circle of radius r."""
    if r < 0:
        raise ValueError("negative radius")
    return math.pi * r ** 2

print(f"{area(2):.2f}")      # 12.57'''
        code = code_panel(src, font_size=24).to_edge(LEFT, buff=0.6)
        with self.say("Python has no braces. A colon opens a block, and the lines indented beneath it "
                      "are the block's body. The block ends where the indentation ends."):
            self.play(FadeIn(code))
            lines = code.code_lines

            def band(i, j, color, indent):
                top = lines[i].get_top()[1] + 0.08
                bot = lines[j].get_bottom()[1] - 0.08
                x0 = code.submobjects[0].get_left()[0] + 0.15 + indent
                return Rectangle(width=0.08, height=top - bot, stroke_width=0, fill_color=color,
                                 fill_opacity=1).move_to([x0, (top + bot) / 2, 0])
            ind = lines[3].get_left()[0] - lines[2].get_left()[0]
            b1 = band(3, 6, C_BLUE, 0.0)
            b2 = band(5, 5, C_GOLD, ind)
            l1 = tex(r"\texttt{def} body", 34, C_BLUE).next_to(code, RIGHT, buff=0.5).align_to(lines[3], UP)
            l2 = tex(r"\texttt{if} body", 34, C_GOLD).next_to(l1, DOWN, buff=0.4)
            self.play(Indicate(lines[2][-1], color=C_YELLOW), Indicate(lines[4][-1], color=C_YELLOW))
            self.play(GrowFromEdge(b1, UP), FadeIn(l1))
            self.play(GrowFromEdge(b2, UP), FadeIn(l2))
        with self.say("The convention is four spaces per level. Inside parentheses, brackets or braces, "
                      "a long statement may also continue on the next line without a backslash."):
            pep = tex(r"PEP 8: four spaces per level", 32, C_GREY).next_to(l2, DOWN, buff=0.6,
                                                                           aligned_edge=LEFT)
            self.play(FadeIn(pep))
            cont = code_panel("total = (1 + 2 +\n         3 + 4)", font_size=24)
            cont.next_to(pep, DOWN, buff=0.5, aligned_edge=LEFT)
            self.play(FadeIn(cont, shift=0.2 * UP))
        self.clear(keep=[h])
        self.h = h

    def inspect(self):
        h = self.swap_heading(self.h, "Inspecting objects and printing")
        src = '''isinstance(3, int)
type(3.0)
[n for n in dir("text")
   if not n.startswith("_")][:4]
print("a", "b", "c", sep=", ")
print("no newline", end=" | ")
print("done")'''
        code = code_panel(src, font_size=24).to_edge(LEFT, buff=0.4).shift(UP * 0.2)
        con = Console(width=5.6, height=4.0).to_edge(RIGHT, buff=0.5).shift(UP * 0.2)
        mk = Marker(code)
        with self.say("Every value carries its type, and you can ask about it at runtime. "
                      "isinstance is the preferred type test, type returns the exact class, "
                      "and dir lists an object's attributes. help shows its documentation."):
            self.play(FadeIn(code), FadeIn(con))
            self.play(mk.to(0))
            self.play(con.print("True"))
            self.play(mk.to(1))
            self.play(con.print("<class 'float'>"))
            self.play(mk.to(2, 3))
            self.play(con.print("['capitalize', 'casefold',"))
            self.play(con.print(" 'center', 'count']"))
        with self.say("print takes any number of values. sep sets the separator between them, "
                      "and end replaces the trailing newline, so the next print continues the same line."):
            self.play(mk.to(4))
            self.play(con.print("a, b, c", color=C_YELLOW))
            self.play(mk.to(5))
            self.play(con.print("no newline | ", color=C_YELLOW))
            self.play(mk.to(6))
            last = con.rows[-1]
            done = mono("done", con.font_size, color=C_GREEN).next_to(last, RIGHT, buff=0.1)
            self.play(FadeIn(done, shift=0.15 * LEFT))
        self.clear()
