from lesson import *


class L05References(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 5, "references-mutability", "References and mutability", "Python"

    def construct(self):
        self.intro("Lesson five: references and mutability. One rule explains almost every "
                   "why-did-my-list-change surprise in Python: assignment never copies.",
                   r"aliasing, copies, default arguments, passing by sharing")
        self.aliasing()
        self.copies()
        self.defaults()
        self.sharing()
        self.outro([r"Assignment binds a name; it never copies the object.",
                    r"\texttt{.copy()} is shallow: inner objects are still shared.",
                    r"Defaults are evaluated once: use \texttt{None}, then create inside.",
                    r"Functions can mutate your object, but rebinding a parameter is local."],
                   "Assignment never copies, a shallow copy shares its insides, a mutable default is created "
                   "only once, and a function can change your object but never your names.")

    def aliasing(self):
        h = self.heading("Aliasing")
        code = code_panel("a = [1, 2, 3]\nb = a\nb.append(4)\nprint(a, a is b)", font_size=30)
        code.to_edge(LEFT, buff=0.6).shift(UP * 0.8)
        mk = Marker(code)
        obj = list_obj([1, 2, 3]).move_to(RIGHT * 3.8 + UP * 0.2)
        ta = name_tag("a").move_to(RIGHT * 0.9 + UP * 1.0)
        tb = name_tag("b").move_to(RIGHT * 0.9 + DOWN * 0.6)
        with self.say("a equals a list binds the name a to a new list object. b equals a does not copy "
                      "that list; it attaches a second label to the very same object."):
            self.play(FadeIn(code), mk.to(0))
            self.play(FadeIn(obj), FadeIn(ta), GrowArrow(pa := pointer(ta, obj[0])))
            self.play(mk.to(1))
            self.play(FadeIn(tb), GrowArrow(pb := pointer(tb, obj[0])))
        with self.say("So appending through b changes the one object, and a sees the change. "
                      "a is b is true: two names, one list."):
            self.play(mk.to(2))
            new = cell(4, color=C_NEW).next_to(obj[0], RIGHT, buff=0)
            self.play(Indicate(tb), GrowFromEdge(new, LEFT))
            obj[0].add(new)
            self.play(mk.to(3))
            out = mono("[1, 2, 3, 4] True", 28, color=C_YELLOW).next_to(code, DOWN, buff=0.4, aligned_edge=LEFT)
            self.play(ShowPassingFlash(pa.copy().set_color(WHITE), time_width=0.6), Write(out))
        self.clear(keep=[h])
        self.h = h

    def copies(self):
        h = self.swap_heading(self.h, "Shallow versus deep copies")
        code = code_panel("nested = [[1, 2], [3, 4]]\nshallow = nested.copy()\ndeep = copy.deepcopy(nested)\n"
                          "nested[0].append(99)", font_size=24).to_edge(UP, buff=1.0).to_edge(LEFT, buff=0.5)
        mk = Marker(code)

        def outer(color, label):
            o = list_obj(["", ""], color=color, w=0.6, label=label, direction=DOWN)
            return o
        inner1 = list_obj([1, 2], w=0.6).move_to(RIGHT * 4.6 + UP * 0.4)
        inner2 = list_obj([3, 4], w=0.6).move_to(RIGHT * 4.6 + DOWN * 1.0)
        on = outer(C_OBJ, "nested").move_to(RIGHT * 1.5 + DOWN * 0.3)
        os = outer(C_GREEN, "shallow").move_to(LEFT * 1.4 + DOWN * 0.3)

        def links(o, targets, color=WHITE):
            return VGroup(*[Arrow(c.get_center(), t[0].get_left(), buff=0.06, color=color, stroke_width=2.5,
                                  max_tip_length_to_length_ratio=0.08) for c, t in zip(o[0], targets)])
        with self.say("Copying is explicit. A shallow copy, like dot copy, makes a new outer list, "
                      "but its slots point at the same inner lists."):
            self.play(FadeIn(code), mk.to(0))
            self.play(FadeIn(on), FadeIn(inner1), FadeIn(inner2), Create(ln := links(on, [inner1, inner2])))
            self.play(mk.to(1))
            self.play(FadeIn(os, shift=0.3 * RIGHT))
            ls = VGroup(*[CurvedArrow(c.get_center(), t[0].get_corner(DL) + DOWN * 0.02, angle=-0.6,
                                      color=C_GREEN, stroke_width=2.5, tip_length=0.15)
                          for c, t in zip(os[0], [inner1, inner2])])
            self.play(Create(ls))
        with self.say("deepcopy copies recursively, so it shares nothing. Now append to the first inner "
                      "list: the shallow copy sees ninety-nine, the deep copy does not."):
            self.play(mk.to(2))
            deep = VGroup(list_obj([1, 2], w=0.5, color=C_GOLD, label="deep"), list_obj([3, 4], w=0.5, color=C_GOLD, label=""))
            deep.arrange(RIGHT, buff=0.3).move_to(LEFT * 4.5 + DOWN * 2.6)
            self.play(FadeIn(deep, shift=0.3 * UP))
            self.play(mk.to(3))
            c99 = cell(99, w=0.6, h=0.6, color=C_BAD, size=26).next_to(inner1[0], RIGHT, buff=0)
            self.play(GrowFromEdge(c99, LEFT))
            self.play(Indicate(os, color=C_BAD), Circumscribe(deep, color=C_GOLD))
        self.clear(keep=[h])
        self.h = h

    def defaults(self):
        h = self.swap_heading(self.h, "Mutable default arguments")
        code = code_panel("def add_bad(x, lst=[]):\n    lst.append(x)\n    return lst\n\n"
                          "add_bad(1)   # [1]\nadd_bad(2)   # [1, 2] !", font_size=26).to_edge(LEFT, buff=0.6)
        mk = Marker(code, color=C_BAD)
        fobj = RoundedRectangle(corner_radius=0.15, width=3.4, height=2.6, stroke_color=C_PURPLE,
                                fill_color=C_PURPLE, fill_opacity=0.08).move_to(RIGHT * 3.6 + UP * 0.3)
        flab = mono("function add_bad", 20, color=C_PURPLE).next_to(fobj, UP, buff=0.1)
        dl = mono("defaults:", 20, color=C_GREY).move_to(fobj.get_top() + DOWN * 0.45)
        empty = Rectangle(width=0.6, height=0.6, stroke_color=C_BAD, stroke_width=2).move_to(fobj.get_center() + DOWN * 0.2 + LEFT * 0.6)
        with self.say("A default value is evaluated once, when def runs, and stored on the function object. "
                      "A list default is therefore one list shared by every call."):
            self.play(FadeIn(code), mk.to(0))
            self.play(FadeIn(fobj), FadeIn(flab), FadeIn(dl), Create(empty))
        with self.say("The first call appends one to it. The second call gets the same list back and "
                      "appends two: the result is one, two. The fix is to default to None and create a "
                      "fresh list inside the function."):
            self.play(mk.to(4))
            c1 = cell(1, w=0.6, h=0.6, color=C_BAD, size=26).move_to(empty)
            self.play(FadeIn(c1))
            self.play(mk.to(5))
            c2 = cell(2, w=0.6, h=0.6, color=C_BAD, size=26).next_to(c1, RIGHT, buff=0)
            self.play(GrowFromEdge(c2, LEFT), Flash(c2, color=C_BAD))
            fix = code_panel("def add_good(x, lst=None):\n    lst = [] if lst is None else lst",
                             font_size=22).next_to(fobj, DOWN, buff=0.5)
            self.play(FadeIn(fix, shift=0.2 * UP))
            self.play(Create(SurroundingRectangle(fix, color=C_GREEN, buff=0.05)))
        self.clear(keep=[h])
        self.h = h

    def sharing(self):
        h = self.swap_heading(self.h, "Arguments are passed by sharing")
        code = code_panel('def mutate(items):\n    items.append("added")\n\ndef rebind(items):\n'
                          '    items = ["new list"]\n\ndata = ["original"]\nmutate(data); rebind(data)',
                          font_size=24).to_edge(LEFT, buff=0.5)
        mk = Marker(code)
        obj = list_obj(['"original"'], w=2.4, h=0.8, size=26).move_to(RIGHT * 4.1 + UP * 0.8)
        td = name_tag("data").move_to(RIGHT * 0.9 + UP * 1.6)
        ti = name_tag("items", color=C_TEAL).move_to(RIGHT * 0.9 + DOWN * 0.2)
        with self.say("A function receives a reference to the caller's object. Inside mutate, items and data "
                      "are two labels on one list, so appending is visible outside."):
            self.play(FadeIn(code), mk.to(6))
            self.play(FadeIn(obj), FadeIn(td), GrowArrow(pointer(td, obj[0])))
            self.play(mk.to(0, 1))
            pi = pointer(ti, obj[0], color=C_TEAL)
            self.play(FadeIn(ti), GrowArrow(pi))
            add = cell('"added"', w=1.9, h=0.8, color=C_NEW, size=26).next_to(obj[0], RIGHT, buff=0)
            self.play(GrowFromEdge(add, LEFT))
        with self.say("Rebinding the parameter is different: it only moves the local label to a new object. "
                      "The caller's list is untouched."):
            self.play(mk.to(3, 4))
            nl = list_obj(['"new list"'], w=2.4, h=0.8, size=26, color=C_TEAL).move_to(RIGHT * 4.1 + DOWN * 1.6)
            self.play(FadeIn(nl))
            self.play(Transform(pi, pointer(ti, nl[0], color=C_TEAL)))
            self.play(Circumscribe(VGroup(obj, add), color=C_YELLOW))
        self.clear()
