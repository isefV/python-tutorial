from lesson import *


class L02NumbersOperators(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 2, "numbers-operators", "Numbers and operators", "Python"

    def construct(self):
        self.intro("Lesson two: numbers, booleans and operators. Most of it matches what you know from "
                   "C-like languages, but a handful of rules differ, and those are exactly the ones that bite.",
                   r"ints, floats, comparisons, truthiness")
        self.division()
        self.floats()
        self.identity()
        self.truthy()
        self.outro([r"Ints never overflow; \texttt{/} is true division, \texttt{//} floors.",
                    r"Floats are IEEE doubles: compare with \texttt{math.isclose}.",
                    r"\texttt{==} compares values, \texttt{is} compares identity (use it for \texttt{None}).",
                    r"Zero, empty and \texttt{None} are falsy; \texttt{and}/\texttt{or} return operands."],
                   "So: integers are unbounded, slash always gives a float, double slash floors, floats need "
                   "a tolerance, is means same object, and empty things are false.")

    def division(self):
        h = self.heading("Integer arithmetic")
        code = code_panel("2 ** 100\n7 / 2\n7 // 2\n-7 // 2\n-7 % 3", font_size=30)
        code.to_edge(LEFT, buff=0.6).shift(UP * 0.8)
        mk = Marker(code)
        con = Console(width=6.6, height=1.4).next_to(code, DOWN, buff=0.4, aligned_edge=LEFT)
        with self.say("Python integers have arbitrary precision. Two to the power one hundred simply works; "
                      "there is no overflow, the number just grows more digits."):
            self.play(FadeIn(code), FadeIn(con), mk.to(0))
            self.play(con.print("1267650600228229401496703205376", size=22, color=C_YELLOW))
        nl = NumberLine(x_range=[-5, 5, 1], length=6.4, include_numbers=True, font_size=26,
                        color=GREY_B).move_to(RIGHT * 3.3 + DOWN * 0.2)
        with self.say("A single slash is true division and always returns a float: seven over two is "
                      "three point five. Double slash is floor division."):
            self.play(mk.to(1), Create(nl))
            p = Dot(nl.n2p(3.5), color=C_BLUE, radius=0.09)
            lab = mono("3.5", 26, color=C_BLUE).next_to(p, UP, buff=0.75)
            self.play(FadeIn(p, scale=2), FadeIn(lab))
            self.play(mk.to(2))
            fl = Dot(nl.n2p(3), color=C_GREEN, radius=0.09)
            arc = CurvedArrow(nl.n2p(3.5) + UP * 0.15, nl.n2p(3) + UP * 0.15, color=C_GREEN, angle=TAU / 4)
            self.play(Create(arc), FadeIn(fl, scale=2))
        with self.say("Floor really means floor: it rounds toward minus infinity, not toward zero, so "
                      "minus seven floor-divided by two is minus four, not minus three as in C. "
                      "And the remainder takes the sign of the divisor."):
            self.play(mk.to(3))
            q = Dot(nl.n2p(-3.5), color=C_BLUE, radius=0.09)
            ql = mono("-3.5", 26, color=C_BLUE).next_to(q, UP, buff=0.75)
            self.play(FadeIn(q, scale=2), FadeIn(ql))
            fq = Dot(nl.n2p(-4), color=C_GREEN, radius=0.09)
            arc2 = CurvedArrow(nl.n2p(-3.5) + UP * 0.15, nl.n2p(-4) + UP * 0.15, color=C_GREEN, angle=TAU / 4)
            self.play(Create(arc2), FadeIn(fq, scale=2))
            c_way = VGroup(mono("C: -3", 24, color=C_BAD), mono("Python: -4", 24, color=C_GREEN))
            c_way.arrange(DOWN, aligned_edge=LEFT).next_to(nl, DOWN, buff=0.8)
            self.play(FadeIn(c_way))
            self.play(mk.to(4))
            self.play(con.print("-7 % 3  ->  2", color=C_YELLOW))
        self.clear(keep=[h])
        self.h = h

    def floats(self):
        h = self.swap_heading(self.h, "Floats are IEEE 754 doubles")
        code = code_panel("0.1 + 0.2 == 0.3\n0.1 + 0.2\nmath.isclose(0.1 + 0.2, 0.3)", font_size=30)
        code.to_edge(UP, buff=1.4)
        mk = Marker(code)
        con = Console(width=7, height=2.1).next_to(code, DOWN, buff=0.5)
        with self.say("Floats are ordinary double-precision numbers, so the usual surprise applies: "
                      "point one plus point two is not exactly point three."):
            self.play(FadeIn(code), FadeIn(con), mk.to(0))
            self.play(con.print("False", color=C_BAD))
            self.play(mk.to(1))
            self.play(con.print("0.30000000000000004", color=C_BAD))
        with self.say("Never compare floats with double equals. math dot isclose compares them with a "
                      "tolerance. Complex numbers are built in too, written with a j."):
            self.play(mk.to(2))
            self.play(con.print("True", color=C_GREEN))
            z = mono("z = 3 + 4j    abs(z) -> 5.0", 26, color=C_GREY).next_to(con, DOWN, buff=0.5)
            self.play(FadeIn(z))
        self.clear(keep=[h])
        self.h = h

    def identity(self):
        h = self.swap_heading(self.h, "Equality versus identity")
        code = code_panel("a, b = [1, 2], [1, 2]\na == b\na is b\nvalue is None", font_size=28)
        code.to_edge(LEFT, buff=0.6).shift(UP * 0.5)
        mk = Marker(code)
        la = list_obj([1, 2]).move_to(RIGHT * 4.3 + UP * 1.3)
        lb = list_obj([1, 2]).move_to(RIGHT * 4.3 + DOWN * 1.1)
        ta = name_tag("a").move_to(RIGHT * 1.6 + UP * 1.1)
        tb = name_tag("b").move_to(RIGHT * 1.6 + DOWN * 1.3)
        with self.say("Two different list objects can hold equal values. Double equals compares values, "
                      "so a equals b is true."):
            self.play(FadeIn(code), mk.to(0))
            self.play(FadeIn(la), FadeIn(lb), FadeIn(ta), FadeIn(tb),
                      GrowArrow(pointer(ta, la[0])), GrowArrow(pointer(tb, lb[0])))
            self.play(mk.to(1))
            eq = mono("True", 28, color=C_GREEN).next_to(code, DOWN, buff=0.4, aligned_edge=LEFT)
            self.play(Indicate(la[0][0][1]), Indicate(lb[0][0][1]), FadeIn(eq))
        with self.say("is compares identity: are these the same object? They are not. "
                      "Use is only for singletons, above all for checking is None."):
            self.play(mk.to(2))
            ne = mono("False", 28, color=C_BAD).next_to(eq, RIGHT, buff=0.6)
            self.play(Circumscribe(la), Circumscribe(lb), FadeIn(ne))
            self.play(mk.to(3))
        self.clear(keep=[h])
        self.h = h

    def truthy(self):
        h = self.swap_heading(self.h, "Truthiness")
        falsy = ["0", "0.0", '""', "[]", "{}", "set()", "None"]
        truthy = ['"text"', "[0]", "42", "-1"]
        with self.say("Any object can be tested in an if. Zero, empty strings, empty containers and None are "
                      "falsy; almost everything else is truthy. So write if items, not if len of items is "
                      "greater than zero."):
            fcol = VGroup(*[pill(v, C_BAD, 24) for v in falsy]).arrange(DOWN, buff=0.18)
            tcol = VGroup(*[pill(v, C_GREEN, 24) for v in truthy]).arrange(DOWN, buff=0.18)
            ft = tex(r"\textbf{falsy}", 36, C_BAD)
            tt = tex(r"\textbf{truthy}", 36, C_GREEN)
            left = VGroup(ft, fcol).arrange(DOWN, buff=0.4).move_to(LEFT * 3.5 + DOWN * 0.3)
            right = VGroup(tt, tcol).arrange(DOWN, buff=0.4).move_to(LEFT * 0.5 + DOWN * 0.3).align_to(left, UP)
            self.play(FadeIn(ft), FadeIn(tt))
            self.play(LaggedStart(*[FadeIn(p, shift=0.2 * DOWN) for p in fcol], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(p, shift=0.2 * DOWN) for p in tcol], lag_ratio=0.15), run_time=2)
        code = code_panel('name = "" or "default"\n0 and 1 / 0\nif (n := len(data)) > 3:\n    ...',
                          font_size=24).to_edge(RIGHT, buff=0.5).shift(UP * 0.4)
        with self.say("and and or don't return booleans; they return one of their operands. "
                      "or gives the first truthy one, which is handy for defaults, and and stops at the first "
                      "falsy one, so the division by zero never runs. The walrus operator assigns inside "
                      "an expression."):
            self.play(FadeIn(code))
            mk = Marker(code)
            self.play(mk.to(0))
            self.play(mk.to(1))
            self.play(mk.to(2, 3))
        self.clear()
