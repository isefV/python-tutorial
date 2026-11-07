"""Video 2 - NumPy: think in whole arrays.
Render: manim -qh v2_numpy.py NumpyArrays"""
from manim import *
from common import *

C_ARR = C_BLUE      # the array a
C_COL = C_GOLD      # the (3,1) column being broadcast
C_RES = C_TEAL      # results
C_SLOW = C_RED
C_FAST = C_GREEN


def grid_of(values, rows, cols, w=0.8, color=C_ARR, size=28) -> VGroup:
    g = VGroup(*[cell(v, w=w, h=w, color=color, size=size) for v in values])
    return g.arrange_in_grid(rows, cols, buff=0)


class NumpyArrays(Scene):
    def construct(self):
        title_card(self, "Think in whole arrays",
                   r"Python for Programmers \textperiodcentered{} Part 2: NumPy")
        self.race()
        self.memory()
        self.reshape_axes()
        self.indexing()
        self.broadcasting()
        end_card(self, [
            r"An \texttt{ndarray} is one \texttt{dtype} in contiguous memory, looped over in C.",
            r"Index with \texttt{[row, col]}; slices are \emph{views}, masks are copies.",
            r"\texttt{axis=0} collapses rows (down), \texttt{axis=1} collapses columns (across).",
            r"Broadcasting: compare shapes right to left; sizes must match or be 1.",
            r"A Python \texttt{for} over an array is usually a missed vectorization.",
        ])

    # ------------------------------------------------------------------ 1
    def race(self):
        self.next_section("race")
        q = Tex(r"Sum of squares of $10^6$ floats", font_size=44).to_edge(UP, buff=0.8)
        self.play(Write(q))
        py = code_panel("sum(v * v for v in xs)", font_size=24)
        npc = code_panel("(x * x).sum()", font_size=24)
        py.move_to(LEFT * 3.6 + UP * 1.2)
        npc.move_to(LEFT * 3.6 + DOWN * 0.8)
        py_lab = Tex("pure Python", font_size=30, color=C_SLOW).next_to(py, UP, buff=0.15, aligned_edge=LEFT)
        np_lab = Tex("NumPy", font_size=30, color=C_FAST).next_to(npc, UP, buff=0.15, aligned_edge=LEFT)
        self.play(FadeIn(py), FadeIn(py_lab), FadeIn(npc), FadeIn(np_lab))

        t = ValueTracker(0)
        x0 = -0.6
        scale = 6.6 / 87  # units per ms

        def bar(ms, y, color):
            w = max(min(t.get_value(), ms) * scale, 0.001)
            r = Rectangle(width=w, height=0.6, stroke_width=0, fill_color=color, fill_opacity=0.9)
            r.move_to([x0 + w / 2, y, 0])
            n = DecimalNumber(min(t.get_value(), ms), num_decimal_places=0, unit=r"\,\text{ms}",
                              font_size=34, color=color).next_to(r, RIGHT, buff=0.2)
            return VGroup(r, n)

        b_py = always_redraw(lambda: bar(87, py.get_center()[1], C_SLOW))
        b_np = always_redraw(lambda: bar(3, npc.get_center()[1], C_FAST))
        self.add(b_py, b_np)
        self.play(t.animate.set_value(87), run_time=5, rate_func=linear)
        self.wait(0.3)
        ratio = MathTex(r"\approx 30\times", r"\text{ faster}", font_size=56, color=C_FAST)
        ratio.move_to(DOWN * 2.6)
        self.play(Write(ratio))
        self.wait(1)
        why = Tex("Why?", font_size=48).next_to(ratio, RIGHT, buff=1)
        self.play(FadeIn(why, shift=LEFT * 0.3))
        self.wait(0.8)
        b_py.clear_updaters(); b_np.clear_updaters()
        fade_out_all(self)

    # ------------------------------------------------------------------ 2
    def memory(self):
        self.next_section("memory")
        head = chapter(self, "Two ways to store numbers")
        # Python list: slots of pointers to scattered boxed floats
        lt = Tex(r"Python \texttt{list}", font_size=36, color=C_SLOW).move_to(LEFT * 3.6 + UP * 2.3)
        slots = VGroup(*[cell("", w=0.7, h=0.7, color=C_SLOW) for _ in range(5)]).arrange(RIGHT, buff=0)
        slots.next_to(lt, DOWN, buff=0.4)
        dots = VGroup(*[Dot(s.get_center(), radius=0.07) for s in slots])
        vals = ["0.5", "1.2", "3.7", "2.0", "0.9"]
        # scattered but non-overlapping (boxes are 1.25 x 0.85)
        spots = [np.array(p + (0,)) for p in [(-6.1, -1.2), (-3.0, -2.7), (-2.0, -1.1),
                                               (-5.3, -2.7), (-4.1, -1.5)]]
        boxes = VGroup()
        for v, p in zip(vals, spots):
            r = RoundedRectangle(corner_radius=0.08, width=1.25, height=0.85, stroke_color=GREY_B,
                                 stroke_width=1.5, fill_color=CODE_BG, fill_opacity=1)
            t1 = mono("float", 16, color=C_GREY)
            t2 = mono(v, 24)
            VGroup(t1, t2).arrange(DOWN, buff=0.06).move_to(r)
            boxes.add(VGroup(r, t1, t2).move_to(p))
        arrows = VGroup(*[Arrow(d.get_center(), b.get_top(), buff=0.05, stroke_width=2.5, color=GREY_A,
                                max_tip_length_to_length_ratio=0.12) for d, b in zip(dots, boxes)])
        self.play(FadeIn(lt), FadeIn(slots), FadeIn(dots))
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(b)) for a, b in zip(arrows, boxes)],
                              lag_ratio=0.25), run_time=2)
        lnote = Tex(r"each item: a pointer to a full\\Python object, scattered in memory",
                    font_size=26, color=C_GREY).next_to(slots, RIGHT, buff=0.3).shift(UP * 0.0)
        lnote.move_to(LEFT * 3.6 + DOWN * 3.65)

        # ndarray: one contiguous typed block
        rt = Tex(r"NumPy \texttt{ndarray}", font_size=36, color=C_FAST).move_to(RIGHT * 3.6 + UP * 2.3)
        block = VGroup(*[cell(v, w=0.95, h=0.75, color=C_FAST, size=24) for v in vals]).arrange(RIGHT, buff=0)
        block.next_to(rt, DOWN, buff=0.4)
        dt = mono("dtype=float64", 22, color=C_FAST).next_to(block, DOWN, buff=0.35)
        br = Brace(block[0], DOWN, color=GREY_B).next_to(dt, DOWN, buff=0.25).align_to(block[0], LEFT)
        brt = Tex("8 bytes", font_size=26, color=GREY_B).next_to(br, DOWN, buff=0.1)
        self.play(FadeIn(rt), LaggedStart(*[FadeIn(c, shift=0.2 * DOWN) for c in block], lag_ratio=0.15))
        self.play(FadeIn(dt), GrowFromCenter(br), FadeIn(brt))
        rnote = Tex(r"raw numbers side by side: one C loop\\walks straight through them",
                    font_size=26, color=C_GREY).move_to(RIGHT * 3.6 + DOWN * 2.6)
        self.play(FadeIn(rnote), FadeIn(lnote))
        # a "C loop" sweeping across the block
        sweep = SurroundingRectangle(block[0], color=C_YELLOW, buff=0.03)
        self.play(Create(sweep))
        for c in block[1:]:
            self.play(sweep.animate.move_to(c), run_time=0.18, rate_func=linear)
        self.play(FadeOut(sweep))
        self.wait(1.5)
        fade_out_all(self)

    # ------------------------------------------------------------------ 3
    def reshape_axes(self):
        self.next_section("reshape")
        head = chapter(self, "Shape and axes")
        code = code_panel("a = np.arange(12)", font_size=26).to_edge(UP, buff=1.0)
        self.play(FadeIn(code))
        flat = VGroup(*[cell(i, w=0.75, h=0.75, size=26) for i in range(12)]).arrange(RIGHT, buff=0)
        self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in flat], lag_ratio=0.08), run_time=1.5)
        shape = mono("shape (12,)", 26, color=C_GREY).next_to(flat, DOWN, buff=0.4)
        self.play(FadeIn(shape))
        self.wait(0.5)

        code2 = code_panel("a = np.arange(12).reshape(3, 4)", font_size=26).move_to(code)
        grid = flat.copy().arrange_in_grid(3, 4, buff=0).scale(1.1).move_to(LEFT * 1.5 + DOWN * 0.3)
        shape2 = mono("shape (3, 4)", 26, color=C_GREY).next_to(grid, DOWN, buff=0.4)
        self.play(ReplacementTransform(code, code2))
        self.play(Transform(flat, grid), Transform(shape, shape2), run_time=2)
        self.wait(0.4)

        a0 = Arrow(grid.get_corner(UL) + LEFT * 0.4, grid.get_corner(DL) + LEFT * 0.4, buff=0,
                   color=C_RED, stroke_width=5)
        a1 = Arrow(grid.get_corner(UL) + UP * 0.35, grid.get_corner(UR) + UP * 0.35, buff=0,
                   color=C_GREEN, stroke_width=5)
        l0 = MathTex(r"\text{axis } 0", color=C_RED, font_size=32).next_to(a0, LEFT, buff=0.15)
        l1 = MathTex(r"\text{axis } 1", color=C_GREEN, font_size=32).next_to(a1, UP, buff=0.1)
        self.play(GrowArrow(a0), Write(l0))
        self.play(GrowArrow(a1), Write(l1))
        self.wait(0.6)

        # sum(axis=0): each column collapses downward
        code3 = code_panel("a.sum(axis=0)", font_size=26).move_to(RIGHT * 4.3 + UP * 1.0)
        self.play(FadeIn(code3), Indicate(l0, color=C_RED))
        sums = VGroup(*[cell(s, w=0.825, h=0.825, color=C_RES, size=28) for s in [12, 15, 18, 21]])
        sums.arrange(RIGHT, buff=0).next_to(grid, DOWN, buff=0.4).align_to(grid, LEFT)
        self.play(FadeOut(shape))
        self.play(LaggedStart(*[
            ReplacementTransform(VGroup(*[flat[r * 4 + j].copy() for r in range(3)]), sums[j])
            for j in range(4)], lag_ratio=0.25), run_time=2.2)
        out = mono("-> [12 15 18 21]", 26, color=C_RES).next_to(code3, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(Write(out))
        cap = caption(r"\texttt{axis=0} runs \emph{down} the rows, so each column becomes one number")
        self.play(FadeIn(cap))
        self.wait(2.5)
        self.play(FadeOut(VGroup(sums, code3, out, cap, a0, a1, l0, l1, code2)))
        self.grid = flat
        self.head = head

    # ------------------------------------------------------------------ 4
    def indexing(self):
        self.next_section("indexing")
        grid = self.grid
        self.play(FadeOut(self.head), grid.animate.move_to(LEFT * 3 + DOWN * 0.2))
        head = chapter(self, "Indexing and masks", corner_only=True)

        def show(src, target, color=C_YELLOW, result=None):
            c = code_panel(src, font_size=28).move_to(RIGHT * 3.3 + UP * 1.6)
            box = SurroundingRectangle(target, color=color, buff=0.04, stroke_width=5)
            self.play(FadeIn(c), Create(box))
            r = None
            if result:
                r = mono(result, 28, color=color).next_to(c, DOWN, buff=0.4)
                self.play(Write(r))
            self.wait(1.2)
            self.play(FadeOut(c), FadeOut(box), *([FadeOut(r)] if r else []))

        show("a[1, 2]", grid[6], result="-> 6")
        show("a[1]", VGroup(*grid[4:8]), result="-> [4 5 6 7]")
        show("a[:, 2]", VGroup(grid[2], grid[6], grid[10]), result="-> [ 2  6 10]")

        # boolean mask
        c = code_panel("mask = a % 2 == 0\na[mask]", font_size=28).move_to(RIGHT * 3.3 + UP * 1.6)
        mk = line_marker(c, 0)
        self.play(FadeIn(c), FadeIn(mk))
        overlays = VGroup()
        for i, g in enumerate(grid):
            even = i % 2 == 0
            o = Rectangle(width=g.width, height=g.height, stroke_width=0, fill_opacity=0.55,
                          fill_color=C_FAST if even else C_SLOW).move_to(g)
            lab = mono("True" if even else "False", 15, color=WHITE).move_to(g).shift(DOWN * 0.27)
            overlays.add(VGroup(o, lab))
        self.play(LaggedStart(*[FadeIn(o) for o in overlays], lag_ratio=0.05), run_time=1.5)
        self.wait(0.6)
        self.play(Transform(mk, line_marker(c, 1)))
        picked = VGroup(*[cell(i, w=0.75, h=0.75, color=C_FAST, size=26) for i in range(0, 12, 2)])
        picked.arrange(RIGHT, buff=0).move_to(RIGHT * 3.3 + DOWN * 0.6)
        self.play(LaggedStart(*[TransformFromCopy(grid[i], picked[i // 2]) for i in range(0, 12, 2)],
                              lag_ratio=0.15), run_time=2)
        note = Tex(r"a mask keeps the \texttt{True} cells and returns a 1-D \emph{copy}",
                   font_size=28, color=C_GREY).next_to(picked, DOWN, buff=0.5)
        self.play(FadeIn(note))
        self.wait(2)
        fade_out_all(self)

    # ------------------------------------------------------------------ 5
    def broadcasting(self):
        self.next_section("broadcasting")
        head = chapter(self, "Broadcasting")
        code = code_panel("col = np.array([[10], [20], [30]])\na + col", font_size=24)
        code.to_edge(UP, buff=0.9)
        self.play(FadeIn(code))
        w = 0.72
        a = grid_of(range(12), 3, 4, w=w, color=C_ARR, size=24)
        col = grid_of([10, 20, 30], 3, 1, w=w, color=C_COL, size=24)
        res_vals = [i + 10 * (i // 4 + 1) for i in range(12)]
        res = grid_of(res_vals, 3, 4, w=w, color=C_RES, size=24)
        plus = MathTex("+", font_size=56)
        eq = MathTex("=", font_size=56)
        # reserve room for the stretched column: 4 columns wide
        col_slot = Rectangle(width=4 * w, height=3 * w, stroke_width=0)
        row = VGroup(a, plus, col_slot, eq, res).arrange(RIGHT, buff=0.45).shift(DOWN * 0.5)
        col.move_to(col_slot, aligned_edge=LEFT)
        sh_a = mono("(3, 4)", 24, color=C_ARR).next_to(a, DOWN, buff=0.3)
        sh_c = mono("(3, 1)", 24, color=C_COL).next_to(col_slot, DOWN, buff=0.3)
        sh_r = mono("(3, 4)", 24, color=C_RES).next_to(res, DOWN, buff=0.3)
        self.play(FadeIn(a), FadeIn(sh_a), Write(plus), FadeIn(col), FadeIn(sh_c))
        self.wait(0.6)

        # stretch the column (no data is copied in reality)
        ghosts = VGroup()
        for k in range(1, 4):
            gk = col.copy().set_opacity(0.45).shift(RIGHT * k * w)
            for c in gk:
                c[0].set_stroke(opacity=0.8)
            ghosts.add(gk)
        sh_c2 = mono("(3, 1) -> (3, 4)", 24, color=C_COL).move_to(sh_c)
        self.play(LaggedStart(*[TransformFromCopy(col, g) for g in ghosts], lag_ratio=0.3),
                  Transform(sh_c, sh_c2), run_time=2)
        self.wait(0.6)
        self.play(Write(eq))
        stretched = VGroup(*[VGroup(*[(col if k == 0 else ghosts[k - 1])[r] for k in range(4)]) for r in range(3)])
        anims = []
        for i in range(12):
            r, cidx = divmod(i, 4)
            anims.append(TransformFromCopy(VGroup(a[i], stretched[r][cidx]), res[i]))
        self.play(LaggedStart(*anims, lag_ratio=0.08), FadeIn(sh_r), run_time=3)
        self.wait(1)

        rule = VGroup(
            Tex(r"Compare shapes \emph{right to left}:", font_size=32),
            Tex(r"each pair must be \textbf{equal}, or one of them \textbf{1}", font_size=32),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        rule.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)
        self.play(FadeIn(rule))
        self.wait(3)
        fade_out_all(self)
