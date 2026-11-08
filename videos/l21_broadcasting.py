from lesson import *

C_ARR, C_COL, C_RES = C_BLUE, C_GOLD, C_TEAL


class L21Broadcasting(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 21, "numpy-broadcasting", "Vectorization and broadcasting", "NumPy"

    def construct(self):
        self.intro("Lesson twenty-one: vectorization and broadcasting. With NumPy you write array expressions "
                   "instead of loops, and broadcasting lets arrays of different shapes combine without copying.",
                   r"ufuncs, aggregations along axes, broadcasting rules")
        self.elementwise()
        self.axes_()
        self.broadcast()
        self.standardize()
        self.outro([r"Arithmetic, comparisons and ufuncs work element by element.",
                    r"\texttt{axis=0} collapses down the rows, \texttt{axis=1} across the columns.",
                    r"Broadcasting: compare shapes right to left; each pair equal or 1.",
                    r"A Python loop over an array is usually a missed vectorization."],
                   "Operators act element-wise, aggregations take an axis, broadcasting stretches size-one "
                   "dimensions, and together they replace almost every loop you'd otherwise write.")

    def elementwise(self):
        h = self.heading("Element-wise operations")
        x = grid_of([1, 2, 3], 1, 3, w=0.9, color=C_ARR)
        y = grid_of([10, 20, 30], 1, 3, w=0.9, color=C_COL)
        r = grid_of([10, 40, 90], 1, 3, w=0.9, color=C_RES)
        row = VGroup(x, MathTex(r"\times", font_size=56), y, MathTex("=", font_size=56), r).arrange(RIGHT, buff=0.4).move_to(UP * 1.2)
        with self.say("Arithmetic between arrays of the same shape works element by element: the first with the "
                      "first, the second with the second. No loop in sight, and it runs in compiled code."):
            self.play(FadeIn(x), FadeIn(row[1]), FadeIn(y))
            self.play(FadeIn(row[3]), LaggedStart(*[TransformFromCopy(VGroup(x[i], y[i]), r[i]) for i in range(3)],
                                                  lag_ratio=0.3), run_time=2)
        more = VGroup(mono("x * 2 + 1       -> [3 5 7]", 28), mono("np.sqrt(x)      -> [1.    1.414 1.732]", 28),
                      mono("x > 1           -> [False  True  True]", 28)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        more.move_to(DOWN * 1.6)
        with self.say("A plain number works too, applied to every element. Universal functions like square root and "
                      "exp do the same, and comparisons give boolean arrays."):
            self.play(LaggedStart(*[FadeIn(m, shift=0.2 * UP) for m in more], lag_ratio=0.4), run_time=2)
        self.clear(keep=[h])
        self.h = h

    def axes_(self):
        h = self.swap_heading(self.h, "Aggregations along an axis")
        grid = grid_of(range(12), 3, 4, w=0.85, size=26).move_to(LEFT * 2.2 + DOWN * 0.1)
        a0 = Arrow(grid.get_corner(UL) + LEFT * 0.4, grid.get_corner(DL) + LEFT * 0.4, buff=0, color=C_RED, stroke_width=5)
        a1 = Arrow(grid.get_corner(UL) + UP * 0.35, grid.get_corner(UR) + UP * 0.35, buff=0, color=C_GREEN, stroke_width=5)
        l0 = MathTex(r"\text{axis } 0", color=C_RED, font_size=32).next_to(a0, LEFT, buff=0.15)
        l1 = MathTex(r"\text{axis } 1", color=C_GREEN, font_size=32).next_to(a1, UP, buff=0.1)
        with self.say("sum, mean, max and friends reduce the whole array to one number, unless you give an axis. "
                      "Axis zero runs down the rows, axis one runs across the columns."):
            self.play(FadeIn(grid))
            self.play(GrowArrow(a0), Write(l0))
            self.play(GrowArrow(a1), Write(l1))
        with self.say("So sum with axis zero collapses each column into one number: four results. Mean with axis "
                      "one collapses each row: three results. The axis you name is the one that disappears."):
            c = code_panel("a.sum(axis=0)", font_size=28).move_to(RIGHT * 3.8 + UP * 1.4)
            self.play(FadeIn(c), Indicate(l0, color=C_RED))
            sums = VGroup(*[cell(s, w=0.85, h=0.85, color=C_RES, size=26) for s in [12, 15, 18, 21]]).arrange(RIGHT, buff=0)
            sums.next_to(grid, DOWN, buff=0.4)
            self.play(LaggedStart(*[ReplacementTransform(VGroup(*[grid[r * 4 + j].copy() for r in range(3)]), sums[j])
                                    for j in range(4)], lag_ratio=0.25), run_time=2)
            c2 = code_panel("a.mean(axis=1)", font_size=28).next_to(c, DOWN, buff=0.5)
            self.play(FadeIn(c2), Indicate(l1, color=C_GREEN))
            means = VGroup(*[cell(m, w=0.85, h=0.85, color=C_GOLD, size=24) for m in ["1.5", "5.5", "9.5"]]).arrange(DOWN, buff=0)
            means.next_to(grid, RIGHT, buff=0.4)
            self.play(LaggedStart(*[ReplacementTransform(VGroup(*[grid[r * 4 + j].copy() for j in range(4)]), means[r])
                                    for r in range(3)], lag_ratio=0.25), run_time=2)
        self.clear(keep=[h])
        self.h = h

    def broadcast(self):
        h = self.swap_heading(self.h, "Broadcasting")
        code = code_panel("col = np.array([[10], [20], [30]])\na + col", font_size=26).to_edge(UP, buff=1.0)
        w = 0.72
        a = grid_of(range(12), 3, 4, w=w, color=C_ARR, size=24)
        col = grid_of([10, 20, 30], 3, 1, w=w, color=C_COL, size=24)
        res = grid_of([i + 10 * (i // 4 + 1) for i in range(12)], 3, 4, w=w, color=C_RES, size=24)
        plus, eq = MathTex("+", font_size=56), MathTex("=", font_size=56)
        slot = Rectangle(width=4 * w, height=3 * w, stroke_width=0)
        VGroup(a, plus, slot, eq, res).arrange(RIGHT, buff=0.45).shift(DOWN * 0.4)
        col.move_to(slot, aligned_edge=LEFT)
        sh_a = mono("(3, 4)", 24, color=C_ARR).next_to(a, DOWN, buff=0.3)
        sh_c = mono("(3, 1)", 24, color=C_COL).next_to(slot, DOWN, buff=0.3)
        sh_r = mono("(3, 4)", 24, color=C_RES).next_to(res, DOWN, buff=0.3)
        with self.say("What if the shapes differ? Add a three-by-one column to a three-by-four array. NumPy "
                      "stretches the size-one dimension to match, as if the column were repeated four times, "
                      "without actually copying anything."):
            self.play(FadeIn(code))
            self.play(FadeIn(a), FadeIn(sh_a), Write(plus), FadeIn(col), FadeIn(sh_c))
            ghosts = VGroup()
            for k in range(1, 4):
                gk = col.copy().set_opacity(0.45).shift(RIGHT * k * w)
                ghosts.add(gk)
            self.play(LaggedStart(*[TransformFromCopy(col, gg) for gg in ghosts], lag_ratio=0.3),
                      Transform(sh_c, mono("(3, 1) -> (3, 4)", 24, color=C_COL).move_to(sh_c)), run_time=2)
            self.play(Write(eq))
            stretched = [[(col if k == 0 else ghosts[k - 1])[r] for k in range(4)] for r in range(3)]
            self.play(LaggedStart(*[TransformFromCopy(VGroup(a[i], stretched[i // 4][i % 4]), res[i]) for i in range(12)],
                                  lag_ratio=0.08), FadeIn(sh_r), run_time=2.5)
        rule = VGroup(tex(r"Compare shapes \emph{right to left}:", 34),
                      tex(r"each pair must be \textbf{equal}, or one of them \textbf{1}", 34)).arrange(DOWN, buff=0.15)
        rule.to_edge(DOWN, buff=0.35).add_background_rectangle(color=BG, opacity=0.9, buff=0.1)
        with self.say("The rule: line the shapes up from the right. Each pair of dimensions must be equal, or one "
                      "of them must be one. Three by four plus a plain four-element row works. Three by four plus "
                      "three elements fails, because four and three don't match."):
            self.play(FadeIn(rule))
            ok = mono("(3, 4) + (4,)  ok", 26, color=C_GREEN).move_to(LEFT * 3.5 + UP * 1.0)
            bad = mono("(3, 4) + (3,)  ValueError", 26, color=C_RED).move_to(RIGHT * 3.3 + UP * 1.0)
            self.play(FadeOut(code), FadeIn(ok))
            self.play(FadeIn(bad))
        self.clear(keep=[h])
        self.h = h

    def standardize(self):
        h = self.swap_heading(self.h, "Example: standardize columns")
        code = code_panel("mean, std = X.mean(axis=0), X.std(axis=0)\nZ = (X - mean) / std", font_size=28).to_edge(UP, buff=1.1)
        shapes = VGroup(mono("X     (5, 3)", 28, color=C_ARR), mono("mean  (3,)", 28, color=C_COL),
                        mono("std   (3,)", 28, color=C_COL), mono("Z     (5, 3)", 28, color=C_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        shapes.move_to(DOWN * 0.8)
        with self.say("Put together: to standardize every column of a data matrix, compute the mean and standard "
                      "deviation along axis zero, giving one number per column. Then subtract and divide. "
                      "Broadcasting lines the three-element rows up against every row of X. Two lines, no loop."):
            self.play(FadeIn(code))
            self.play(LaggedStart(*[FadeIn(s, shift=0.2 * RIGHT) for s in shapes], lag_ratio=0.3), run_time=2)
            res = mono("Z.mean(axis=0) -> [0. 0. 0.]   Z.std(axis=0) -> [1. 1. 1.]", 24, color=C_YELLOW).to_edge(DOWN, buff=0.7)
            self.play(FadeIn(res))
        self.clear()
