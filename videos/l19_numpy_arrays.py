from lesson import *

C_SLOW, C_FAST = C_RED, C_GREEN


class L19NumpyArrays(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 19, "numpy-arrays", "The ndarray", "NumPy"

    def construct(self):
        self.intro("Lesson nineteen starts the NumPy part. Its core object is the n-d array: an N-dimensional "
                   "grid of numbers of a single type, stored in one block of memory. That one design decision is "
                   "why NumPy is fast.", r"creating arrays, shape, dtype, reshape, speed")
        self.race()
        self.memory()
        self.create()
        self.shape()
        self.outro([r"An \texttt{ndarray} holds one \texttt{dtype} in contiguous memory.",
                    r"Create with \texttt{array}, \texttt{zeros}, \texttt{arange}, \texttt{linspace}, \texttt{default\_rng}.",
                    r"\texttt{shape}, \texttt{ndim}, \texttt{dtype}; \texttt{reshape(2, -1)} infers a dimension.",
                    r"Whole-array operations run as compiled loops: tens of times faster."],
                   "One type, one block of memory, and compiled loops over it: that's the n-d array. Create "
                   "arrays with the factory functions, and reshape them freely, since the data never moves.")

    def race(self):
        h = self.heading("Why NumPy?")
        q = tex(r"Sum of squares of one million floats", 40).to_edge(UP, buff=1.0)
        py = code_panel("sum(v * v for v in xs)", font_size=26).move_to(LEFT * 3.6 + UP * 0.9)
        npc = code_panel("(x * x).sum()", font_size=26).move_to(LEFT * 3.6 + DOWN * 1.1)
        py_lab = tex("pure Python", 32, C_SLOW).next_to(py, UP, buff=0.15, aligned_edge=LEFT)
        np_lab = tex("NumPy", 32, C_FAST).next_to(npc, UP, buff=0.15, aligned_edge=LEFT)
        t = ValueTracker(0)
        x0, scale = -0.6, 6.4 / 87

        def bar(ms, y, color):
            w = max(min(t.get_value(), ms) * scale, 0.001)
            r = Rectangle(width=w, height=0.6, stroke_width=0, fill_color=color, fill_opacity=0.9)
            r.move_to([x0 + w / 2, y, 0])
            n = DecimalNumber(min(t.get_value(), ms), num_decimal_places=0, unit=r"\,\text{ms}", font_size=34,
                              color=color).next_to(r, RIGHT, buff=0.2)
            return VGroup(r, n)
        with self.say("Here's the motivation. Squaring and summing a million floats with a generator takes "
                      "around ninety milliseconds. The same computation as a NumPy expression takes about three. "
                      "Same machine, same result, roughly thirty times faster."):
            self.play(Write(q))
            self.play(FadeIn(py), FadeIn(py_lab), FadeIn(npc), FadeIn(np_lab))
            b_py = always_redraw(lambda: bar(87, py.get_center()[1], C_SLOW))
            b_np = always_redraw(lambda: bar(3, npc.get_center()[1], C_FAST))
            self.add(b_py, b_np)
            self.play(t.animate.set_value(87), run_time=4, rate_func=linear)
            ratio = MathTex(r"\approx 30\times", r"\text{ faster}", font_size=56, color=C_FAST).move_to(DOWN * 2.8)
            self.play(Write(ratio))
        b_py.clear_updaters()
        b_np.clear_updaters()
        self.clear(keep=[h])
        self.h = h

    def memory(self):
        h = self.swap_heading(self.h, "Two ways to store numbers")
        lt = tex(r"Python \texttt{list}", 36, C_SLOW).move_to(LEFT * 3.6 + UP * 2.3)
        slots = VGroup(*[cell("", w=0.7, h=0.7, color=C_SLOW) for _ in range(5)]).arrange(RIGHT, buff=0).next_to(lt, DOWN, buff=0.4)
        dots = VGroup(*[Dot(s.get_center(), radius=0.07) for s in slots])
        vals = ["0.5", "1.2", "3.7", "2.0", "0.9"]
        spots = [np.array(p + (0,)) for p in [(-6.1, -1.2), (-3.0, -2.7), (-2.0, -1.1), (-5.3, -2.7), (-4.1, -1.5)]]
        boxes = VGroup()
        for v, p in zip(vals, spots):
            r = RoundedRectangle(corner_radius=0.08, width=1.25, height=0.85, stroke_color=GREY_B, stroke_width=1.5,
                                 fill_color=CODE_BG, fill_opacity=1)
            t1, t2 = mono("float", 16, color=C_GREY), mono(v, 24)
            VGroup(t1, t2).arrange(DOWN, buff=0.06).move_to(r)
            boxes.add(VGroup(r, t1, t2).move_to(p))
        arrows = VGroup(*[Arrow(d.get_center(), b.get_top(), buff=0.05, stroke_width=2.5, color=GREY_A,
                                max_tip_length_to_length_ratio=0.12) for d, b in zip(dots, boxes)])
        with self.say("A Python list stores pointers. Each number is a full Python object somewhere else in memory, "
                      "with its own type information, so every step of a loop has to follow a pointer and check a type."):
            self.play(FadeIn(lt), FadeIn(slots), FadeIn(dots))
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(b)) for a, b in zip(arrows, boxes)],
                                  lag_ratio=0.25), run_time=2)
        rt = tex(r"NumPy \texttt{ndarray}", 36, C_FAST).move_to(RIGHT * 3.6 + UP * 2.3)
        block = VGroup(*[cell(v, w=0.95, h=0.75, color=C_FAST, size=24) for v in vals]).arrange(RIGHT, buff=0).next_to(rt, DOWN, buff=0.4)
        dt = mono("dtype=float64", 22, color=C_FAST).next_to(block, DOWN, buff=0.35)
        br = Brace(block[0], DOWN, color=GREY_B).next_to(dt, DOWN, buff=0.25).align_to(block[0], LEFT)
        brt = tex("8 bytes", 28, GREY_B).next_to(br, DOWN, buff=0.1)
        with self.say("An n-d array stores the raw numbers side by side, all of one d-type, eight bytes each for "
                      "float sixty-four. A single compiled loop can walk straight through them, and that is where "
                      "the speed comes from."):
            self.play(FadeIn(rt), LaggedStart(*[FadeIn(c, shift=0.2 * DOWN) for c in block], lag_ratio=0.15))
            self.play(FadeIn(dt), GrowFromCenter(br), FadeIn(brt))
            sweep = SurroundingRectangle(block[0], color=C_YELLOW, buff=0.03)
            self.play(Create(sweep))
            for c in block[1:]:
                self.play(sweep.animate.move_to(c), run_time=0.18, rate_func=linear)
            self.play(FadeOut(sweep))
        self.clear(keep=[h])
        self.h = h

    def create(self):
        h = self.swap_heading(self.h, "Creating arrays")
        code = code_panel("np.array([1, 2, 3])\nnp.array([1, 2.5]).dtype\nnp.zeros((2, 3))\nnp.arange(0, 10, 2)\n"
                          "np.linspace(0, 1, 5)\nrng = np.random.default_rng(42)\nrng.integers(0, 10, size=5)",
                          font_size=24).to_edge(LEFT, buff=0.5)
        mk = Marker(code)
        con = Console(width=5.4, height=4.6, font_size=22).to_edge(RIGHT, buff=0.5)
        outs = ["[1 2 3]   int64", "float64", "[[0. 0. 0.]\n [0. 0. 0.]]", "[0 2 4 6 8]",
                "[0.   0.25 0.5  0.75 1.  ]", "", "[0 7 6 4 4]"]
        with self.say("np dot array converts a list, and picks one d-type for everything: mix ints and floats and "
                      "you get floats. zeros, ones and full build arrays of a given shape. arange is range for arrays, "
                      "and linspace gives a fixed number of evenly spaced points, endpoints included. For random "
                      "numbers, create a generator with a seed so results are reproducible."):
            self.play(FadeIn(code), FadeIn(con))
            for i, o in enumerate(outs):
                self.play(mk.to(i), run_time=0.45)
                if o:
                    self.play(con.print(o, color=C_YELLOW), run_time=0.5)
        self.clear(keep=[h])
        self.h = h

    def shape(self):
        h = self.swap_heading(self.h, "Shape, dtype and reshaping")
        code = code_panel("a = np.arange(12)", font_size=26).to_edge(UP, buff=1.0)
        flat = VGroup(*[cell(i, w=0.75, h=0.75, size=26) for i in range(12)]).arrange(RIGHT, buff=0)
        sh = mono("shape (12,)", 26, color=C_GREY).next_to(flat, DOWN, buff=0.4)
        with self.say("arange of twelve is a flat array with shape twelve. reshape of three by four views the same "
                      "twelve numbers as a grid of three rows and four columns. No data moves; only the shape changes."):
            self.play(FadeIn(code))
            self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in flat], lag_ratio=0.06), FadeIn(sh), run_time=1.5)
            code2 = code_panel("a = np.arange(12).reshape(3, 4)", font_size=26).move_to(code)
            grid = flat.copy().arrange_in_grid(3, 4, buff=0).scale(1.1).move_to(LEFT * 2.0 + DOWN * 0.4)
            sh2 = mono("shape (3, 4)", 26, color=C_GREY).next_to(grid, DOWN, buff=0.4)
            self.play(ReplacementTransform(code, code2))
            self.play(Transform(flat, grid), Transform(sh, sh2), run_time=2)
        info = VGroup(mono("a.ndim   -> 2", 26), mono("a.size   -> 12", 26), mono("a.dtype  -> int64", 26),
                      mono("a.reshape(2, -1).shape -> (2, 6)", 24, color=C_GOLD), mono("a.T.shape -> (4, 3)", 24, color=C_GOLD))
        info.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 3.6 + DOWN * 0.4)
        with self.say("Every array knows its number of dimensions, its size and its d-type. Pass minus one to "
                      "reshape and NumPy works out that dimension for you. dot T transposes, again without copying."):
            self.play(LaggedStart(*[FadeIn(i, shift=0.2 * LEFT) for i in info], lag_ratio=0.3), run_time=2.5)
        self.clear()
