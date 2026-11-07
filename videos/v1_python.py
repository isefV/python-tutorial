"""Video 1 - The Language: names are labels, not boxes.
Render: manim -qh v1_python.py PythonNames"""
from manim import *
from common import *


class PythonNames(Scene):
    def construct(self):
        title_card(self, "Names are labels, not boxes",
                   r"Python for Programmers \textperiodcentered{} Part 1: the language")
        self.hook()
        self.labels_model()
        self.immutable()
        self.grid_trap()
        end_card(self, [
            r"Assignment never copies; it attaches a \emph{name} to an \emph{object}.",
            r"Mutating an object is visible through \emph{every} name bound to it.",
            r"Immutable objects (\texttt{int}, \texttt{str}, \texttt{tuple}) are never changed in place.",
            r"Need a separate object? Ask for one: \texttt{.copy()}, a comprehension.",
        ])

    # ------------------------------------------------------------------ 1
    def hook(self):
        self.next_section("hook")
        code = code_panel("""
a = [1, 2, 3]
b = a
b.append(4)
print(a)
""", font_size=30)
        self.play(FadeIn(code.submobjects[0]))
        type_code(self, code)
        out = mono("[1, 2, 3, 4]", 32, color=C_YELLOW).next_to(code, DOWN, buff=0.5)
        q = mono("?", 40, color=C_GREY).move_to(out)
        self.play(FadeIn(q))
        self.wait(0.8)
        self.play(ReplacementTransform(q, out))
        why = Tex(r"We only changed \texttt{b}\ldots{} so why did \texttt{a} change?", font_size=36)
        why.next_to(out, DOWN, buff=0.5)
        self.play(Write(why))
        self.wait(1.5)
        self.play(FadeOut(why), FadeOut(out))
        self.code = code

    # ------------------------------------------------------------------ 2
    def labels_model(self):
        self.next_section("boxes-vs-labels")
        code = self.code
        self.play(code.animate.scale(0.8).to_edge(LEFT, buff=0.5).shift(UP * 1.5))

        # the C mental model: variables are boxes holding values
        def box(name):
            r = Square(1.6, stroke_color=C_GREY, stroke_width=2)
            v = mono("[1,2,3]", 22).move_to(r)
            n = mono(name, 26, color=C_GREY).next_to(r, DOWN, buff=0.15)
            return VGroup(r, v, n)
        boxes = VGroup(box("a"), box("b")).arrange(RIGHT, buff=1).move_to(RIGHT * 3)
        head = Tex(r"C mental model: a variable is a \emph{box}", font_size=32, color=C_GREY)
        head.next_to(boxes, UP, buff=0.6)
        self.play(FadeIn(head), LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.4))
        cross = Cross(VGroup(head, boxes), stroke_color=C_BAD, stroke_width=6)
        self.play(Create(cross))
        self.wait(0.6)
        self.play(FadeOut(VGroup(head, boxes, cross)))

        # the Python model
        head = Tex(r"Python: a name is a \emph{label} on an object", font_size=32)
        head.move_to(RIGHT * 3 + UP * 3)
        self.play(FadeIn(head))

        marker = line_marker(code, 0)
        obj = list_obj([1, 2, 3]).move_to(RIGHT * 3.6 + UP * 0.6)
        tag_a = name_tag("a").move_to(RIGHT * 0.9 + UP * 1.2)
        arr_a = pointer(tag_a, obj[0])
        self.play(FadeIn(marker))
        self.play(FadeIn(obj, shift=0.3 * UP))
        self.play(FadeIn(tag_a, shift=0.3 * RIGHT), GrowArrow(arr_a))
        self.wait(0.6)

        tag_b = name_tag("b").move_to(RIGHT * 0.9 + DOWN * 0.1)
        arr_b = pointer(tag_b, obj[0])
        self.play(Transform(marker, line_marker(code, 1)))
        self.play(FadeIn(tag_b, shift=0.3 * RIGHT), GrowArrow(arr_b))
        note = Tex(r"same object, two labels", font_size=28, color=C_GREY).next_to(obj, DOWN, buff=0.9)
        self.play(FadeIn(note))
        self.wait(0.8)

        self.play(Transform(marker, line_marker(code, 2)), FadeOut(note))
        new = cell(4, color=C_NEW).next_to(obj[0], RIGHT, buff=0)
        self.play(Indicate(tag_b), arr_b.animate.set_color(WHITE), run_time=0.8)
        self.play(GrowFromEdge(new, LEFT), arr_b.animate.set_color(C_NAME))
        obj[0].add(new)
        self.wait(0.4)

        self.play(Transform(marker, line_marker(code, 3)))
        self.play(Indicate(tag_a), ShowPassingFlash(arr_a.copy().set_color(WHITE), time_width=0.6))
        self.play(Circumscribe(obj[0], color=C_YELLOW))
        out = mono("[1, 2, 3, 4]", 26, color=C_YELLOW).next_to(code, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(TransformFromCopy(obj[0], out))
        self.wait(1)

        # copy() makes a new object
        self.next_section("copy")
        extra = code_panel("c = a.copy()\nc.append(5)", font_size=24)
        extra.next_to(out, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(FadeIn(extra))
        m2 = line_marker(extra, 0, color=C_NEW)
        self.play(FadeOut(marker), FadeIn(m2))
        obj_c = list_obj([1, 2, 3, 4], color=C_NEW).move_to(RIGHT * 3.6 + DOWN * 2.2)
        tag_c = name_tag("c", color=C_NEW).move_to(RIGHT * 0.9 + DOWN * 2.2)
        self.play(TransformFromCopy(obj, obj_c), run_time=1.5)
        arr_c = pointer(tag_c, obj_c[0], color=C_NEW)
        self.play(FadeIn(tag_c, shift=0.3 * RIGHT), GrowArrow(arr_c))
        self.play(Transform(m2, line_marker(extra, 1, color=C_NEW)))
        five = cell(5, color=C_NEW).next_to(obj_c[0], RIGHT, buff=0)
        self.play(GrowFromEdge(five, LEFT))
        cap = caption(r"\texttt{a} and \texttt{b} are untouched: \texttt{c} is a different object")
        self.play(FadeIn(cap))
        self.wait(2)
        fade_out_all(self)

    # ------------------------------------------------------------------ 3
    def immutable(self):
        self.next_section("immutable")
        head = chapter(self, "What about numbers?")
        code = code_panel("x = 5\ny = x\nx += 1\nprint(x, y)", font_size=28)
        code.to_edge(LEFT, buff=0.8)
        self.play(FadeIn(code))

        def int_obj(v, color=C_OBJ):
            c = Circle(0.5, stroke_color=color, fill_color=color, fill_opacity=0.15, stroke_width=3)
            return VGroup(c, mono(str(v), 32).move_to(c))

        # x on top, y below; 5 sits low and the new 6 appears high, so arrows never cross
        five = int_obj(5).move_to(RIGHT * 4.2 + DOWN * 0.9)
        lab = mono("int", 20, color=C_OBJ).next_to(five, UP, buff=0.08)
        tx = name_tag("x").move_to(RIGHT * 0.9 + UP * 0.9)
        ty = name_tag("y").move_to(RIGHT * 0.9 + DOWN * 0.9)
        mk = line_marker(code, 0)
        self.play(FadeIn(mk), FadeIn(five), FadeIn(lab), FadeIn(tx))
        ax = pointer(tx, five)
        self.play(GrowArrow(ax))
        self.play(Transform(mk, line_marker(code, 1)), FadeIn(ty))
        ay = pointer(ty, five)
        self.play(GrowArrow(ay))
        self.wait(0.5)

        self.play(Transform(mk, line_marker(code, 2)))
        six = int_obj(6, color=C_NEW).move_to(RIGHT * 4.2 + UP * 1.6)
        lab6 = mono("int", 20, color=C_NEW).next_to(six, UP, buff=0.08)
        self.play(FadeIn(six, scale=0.5), FadeIn(lab6))
        self.play(Transform(ax, pointer(tx, six)), run_time=1.2)
        self.play(Transform(mk, line_marker(code, 3)))
        out = mono("6 5", 28, color=C_YELLOW).next_to(code, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(Write(out))
        cap = caption(r"\texttt{5} can't change, so \texttt{x += 1} builds a new object and moves the label")
        self.play(FadeIn(cap))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not head])
        self.play(FadeOut(head))

    # ------------------------------------------------------------------ 4
    def grid_trap(self):
        self.next_section("grid-trap")
        head = chapter(self, "The classic trap")
        code = code_panel("grid = [[0] * 3] * 3\ngrid[0][0] = 1\nprint(grid)", font_size=26)
        code.to_corner(UL, buff=0.5).shift(DOWN * 0.7)
        self.play(FadeIn(code))
        mk = line_marker(code, 0)
        self.play(FadeIn(mk))

        outer = list_obj(["", "", ""], color=C_OBJ, direction=DOWN).move_to(LEFT * 2.2 + DOWN * 1.35)
        tag = name_tag("grid").next_to(outer, LEFT, buff=0.9)
        row = list_obj([0, 0, 0]).move_to(RIGHT * 3.2 + DOWN * 1.35)
        self.play(FadeIn(tag), FadeIn(outer), GrowArrow(pointer(tag, outer[0])))
        self.play(FadeIn(row))
        dots = VGroup(*[Dot(c.get_center(), radius=0.08) for c in outer[0]])
        arrows = VGroup(*[Arrow(c.get_center(), row[0].get_left(), buff=0.08, color=WHITE,
                                stroke_width=3, max_tip_length_to_length_ratio=0.08)
                          for c in outer[0]])
        self.play(FadeIn(dots), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), run_time=1.5)
        note = Tex(r"three references to \emph{one} row", font_size=32, color=C_BAD).next_to(row, UP, buff=0.5)
        self.play(FadeIn(note))
        self.wait(0.8)

        self.play(Transform(mk, line_marker(code, 1)))
        one = cell(1, color=C_BAD, fill_opacity=0.35).move_to(row[0][0])
        self.play(Transform(row[0][0], one), Flash(row[0][0], color=C_BAD))
        self.play(Transform(mk, line_marker(code, 2)))
        out = mono("[[1, 0, 0], [1, 0, 0], [1, 0, 0]]", 26, color=C_BAD)
        out.next_to(code, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(out))
        self.wait(1.5)

        # the fix
        self.next_section("grid-fix")
        fix = code_panel("grid = [[0] * 3 for _ in range(3)]\ngrid[0][0] = 1\nprint(grid)", font_size=26)
        fix.move_to(code, aligned_edge=LEFT)
        self.play(FadeOut(mk), FadeOut(out), FadeOut(note), FadeOut(arrows), FadeOut(row),
                  ReplacementTransform(code, fix))
        mk = line_marker(fix, 0, color=C_NEW)
        self.play(FadeIn(mk))
        rows = VGroup()
        for c in outer[0]:  # one row level with each slot -> three parallel arrows
            r = list_obj([0, 0, 0], color=C_NEW, w=0.62)
            r[1].set_opacity(0)  # drop the 'list' labels, they'd collide
            r.move_to([3.2, c.get_center()[1], 0])
            rows.add(r)
        arrows = VGroup(*[Arrow(c.get_center(), r[0].get_left(), buff=0.08, color=WHITE,
                                stroke_width=3, max_tip_length_to_length_ratio=0.08)
                          for c, r in zip(outer[0], rows)])
        self.play(LaggedStart(*[FadeIn(r, shift=0.3 * LEFT) for r in rows], lag_ratio=0.3),
                  LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), run_time=1.8)
        self.play(Transform(mk, line_marker(fix, 1, color=C_NEW)))
        one = cell(1, w=0.62, h=0.62, color=C_NEW, fill_opacity=0.4).move_to(rows[0][0][0])
        self.play(Transform(rows[0][0][0], one))
        self.play(Transform(mk, line_marker(fix, 2, color=C_NEW)))
        out = mono("[[1, 0, 0], [0, 0, 0], [0, 0, 0]]", 26, color=C_NEW).next_to(fix, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(out))
        cap = caption(r"The comprehension runs \texttt{[0] * 3} three times: three separate rows")
        self.play(FadeIn(cap))
        self.wait(2.5)
        fade_out_all(self)
