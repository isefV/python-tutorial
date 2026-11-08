from lesson import *


class L22NumpyLinalg(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 22, "numpy-linalg-random", "Linear algebra, random and toolbox", "NumPy"

    def construct(self):
        self.intro("Lesson twenty-two: linear algebra, random numbers, and the everyday NumPy toolbox. "
                   "This is the last NumPy lesson before we move on to pandas.",
                   r"\texttt{@}, \texttt{np.linalg}, \texttt{default\_rng}, sorting, NaN, saving")
        self.matmul()
        self.solve()
        self.random_()
        self.toolbox()
        self.outro([r"\texttt{A @ B} is the matrix product; \texttt{A * B} is element-wise.",
                    r"\texttt{np.linalg.solve(A, b)} solves $Ax = b$; also \texttt{inv}, \texttt{det}, \texttt{eigh}.",
                    r"\texttt{rng = np.random.default\_rng(seed)} for reproducible samples.",
                    r"\texttt{concatenate}, \texttt{sort}, \texttt{unique}, \texttt{nanmean}, \texttt{np.save}."],
                   "The at operator multiplies matrices, linalg solves systems, a seeded generator makes randomness "
                   "reproducible, and a handful of helpers cover joining, sorting and missing values.")

    def matmul(self):
        h = self.heading("Matrix product versus element-wise")
        A = grid_of([2, 1, 1, 3], 2, 2, w=0.8, color=C_BLUE)
        B = grid_of([2, 1, 1, 3], 2, 2, w=0.8, color=C_GOLD)
        R = grid_of([5, 5, 5, 10], 2, 2, w=0.8, color=C_TEAL)
        row = VGroup(A, mono("@", 44), B, MathTex("=", font_size=56), R).arrange(RIGHT, buff=0.45).move_to(UP * 1.2)
        with self.say("For matrices, the at operator is the true matrix product: each result entry is a row of the "
                      "left times a column of the right, summed. Row one, two times column one, two: two times two "
                      "plus one times one, five."):
            self.play(FadeIn(A), FadeIn(row[1]), FadeIn(B))
            r0 = SurroundingRectangle(VGroup(A[0], A[1]), color=C_YELLOW, buff=0.04)
            c0 = SurroundingRectangle(VGroup(B[0], B[2]), color=C_YELLOW, buff=0.04)
            self.play(Create(r0), Create(c0))
            calc = MathTex(r"2\cdot 2 + 1\cdot 1 = 5", font_size=40, color=C_YELLOW).next_to(row, DOWN, buff=0.5)
            self.play(Write(calc), FadeIn(row[3]))
            self.play(TransformFromCopy(VGroup(A[0], A[1], B[0], B[2]), R[0]))
            self.play(FadeIn(VGroup(R[1], R[2], R[3])), FadeOut(r0), FadeOut(c0))
        with self.say("A star A is something else: element-wise multiplication, which squares each entry. "
                      "Mixing the two up is a classic bug."):
            el = mono("A * A  -> [[4 1]\n           [1 9]]", 30, color=C_GREY).move_to(DOWN * 2.0)
            self.play(FadeIn(el, shift=0.2 * UP))
        self.clear(keep=[h])
        self.h = h

    def solve(self):
        h = self.swap_heading(self.h, "Solving a linear system")
        code = code_panel("A = np.array([[2, 1], [1, 3]])\nb = np.array([3, 5])\nnp.linalg.solve(A, b)  # [0.8 1.4]",
                          font_size=24).to_edge(LEFT, buff=0.4).shift(UP * 1.6)
        ax = Axes(x_range=[-1, 3, 1], y_range=[-1, 3, 1], x_length=5.0, y_length=5.0,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 20}).move_to(RIGHT * 3.3 + DOWN * 0.2)
        l1 = ax.plot(lambda x: 3 - 2 * x, x_range=[0, 2], color=C_BLUE)
        l2 = ax.plot(lambda x: (5 - x) / 3, x_range=[-1, 3], color=C_GOLD)
        e1 = MathTex("2x + y = 3", color=C_BLUE, font_size=34)
        e2 = MathTex("x + 3y = 5", color=C_GOLD, font_size=34)
        eqs = VGroup(e1, e2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(code, DOWN, buff=0.6, aligned_edge=LEFT)
        with self.say("np dot linalg has the standard toolkit. solve finds x in A x equals b. Each row is a line, "
                      "and the solution is where the lines meet: x point eight, y one point four."):
            self.play(FadeIn(code), Create(ax))
            self.play(Write(e1), Create(l1))
            self.play(Write(e2), Create(l2))
            p = Dot(ax.c2p(0.8, 1.4), color=C_YELLOW, radius=0.1)
            pl = MathTex("(0.8,\\ 1.4)", font_size=32, color=C_YELLOW).next_to(p, UR, buff=0.1)
            self.play(FadeIn(p, scale=3), Write(pl))
        with self.say("The same module gives you the inverse, the determinant, eigenvalues and norms. Prefer solve "
                      "over multiplying by the inverse: it's faster and more accurate."):
            more = mono("inv(A)  det(A) -> 5.0\neigh(A)  norm(b)", 24, color=C_GREY).next_to(eqs, DOWN, buff=0.6, aligned_edge=LEFT)
            self.play(FadeIn(more))
        self.clear(keep=[h])
        self.h = h

    def random_(self):
        h = self.swap_heading(self.h, "Random sampling")
        code = code_panel("rng = np.random.default_rng(seed=42)\nsamples = rng.normal(0, 1, size=1000)\n"
                          "samples.mean(), samples.std()   # ~0, ~1", font_size=24).to_edge(UP, buff=1.0)
        ax = Axes(x_range=[-4, 4, 1], y_range=[0, 140, 40], x_length=8, y_length=3.4,
                  axis_config={"color": GREY_B, "include_tip": False}, x_axis_config={"include_numbers": True, "font_size": 20})
        ax.move_to(DOWN * 1.4)
        rng = np.random.default_rng(42)
        s = rng.normal(0, 1, 1000)
        counts, edges = np.histogram(s, bins=24, range=(-4, 4))
        bars = VGroup(*[Rectangle(width=ax.x_length / 24 * 0.92, height=max(ax.y_axis.unit_size * c, 0.001), stroke_width=0,
                                  fill_color=C_TEAL, fill_opacity=0.85).move_to(ax.c2p((edges[i] + edges[i + 1]) / 2, 0), aligned_edge=DOWN)
                        for i, c in enumerate(counts)])
        with self.say("Random numbers come from a generator object. Create it once with a seed, and every run "
                      "produces the same samples, which makes results reproducible. A thousand normal samples "
                      "pile up into the familiar bell curve."):
            self.play(FadeIn(code), Create(ax))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), run_time=2.5)
        with self.say("The generator also draws integers, picks random choices, and shuffles with permutation."):
            more = mono("rng.integers(0, 10, size=5)   rng.choice(['a', 'b', 'c'])   rng.permutation(10)", 20,
                        color=C_GREY).next_to(code, DOWN, buff=0.35)
            self.play(FadeIn(more))
        self.clear(keep=[h])
        self.h = h

    def toolbox(self):
        h = self.swap_heading(self.h, "The everyday toolbox")
        rows = [("np.concatenate([a, b])", "[3 1 2 9 8 7]"), ("np.stack([a, b])", "shape (2, 3)"),
                ("np.sort(a), np.argsort(a)", "[1 2 3]  [1 2 0]"), ("np.unique([3, 1, 3, 2])", "[1 2 3]"),
                ("np.mean([1, nan, 3])", "nan"), ("np.nanmean([1, nan, 3])", "2.0"),
                ("np.clip([-5, 0, 5, 10], 0, 6)", "[0 0 5 6]"), ("np.save('a.npy', a); np.load(...)", "round trip")]
        g = VGroup(*[VGroup(mono(a, 24), mono(b, 24, color=C_YELLOW)) for a, b in rows])
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(LEFT * 1.4 + DOWN * 0.2)
        for r in g:
            r[1].set_x(3.0, LEFT)
        g[4][1].set_color(C_RED)
        with self.say("Finally the helpers you'll use daily: concatenate and stack to join arrays, sort and argsort, "
                      "unique. Note that NaN poisons ordinary aggregations, so use the nan-aware versions like nan "
                      "mean. Clip limits a range, and save and load store arrays in NumPy's own fast binary format."):
            self.play(LaggedStart(*[FadeIn(r, shift=0.2 * RIGHT) for r in g], lag_ratio=0.3), run_time=4)
            self.play(Indicate(g[5], color=C_GREEN))
        self.clear()
