"""Video 3 - pandas: tables that know their labels.
Render: manim -qh v3_pandas.py PandasTables"""
from manim import *
from common import *

CITY = {"Tehran": C_GOLD, "Berlin": C_TEAL, "Tokyo": C_PURPLE}
C_IDX = C_GREY
C_VAL = C_BLUE

DF = [  # index, city, month, sales  (the DataFrame from the slides)
    (0, "Tehran", "Jan", "120.0"),
    (1, "Berlin", "Jan", "95.0"),
    (2, "Tehran", "Feb", "140.0"),
    (3, "Tokyo", "Feb", "80.0"),
    (4, "Berlin", "Feb", "110.0"),
    (5, "Tokyo", "Jan", "NaN"),
]


def series_col(index, values, color=C_VAL, w_idx=0.6, w_val=1.0, h=0.6, size=26):
    """Vertical Series: rows of (index cell, value cell)."""
    rows = VGroup()
    for i, v in zip(index, values):
        ic = cell(i, w=w_idx, h=h, color=C_IDX, size=size, fill_opacity=0.05)
        vc = cell(v, w=w_val, h=h, color=C_BAD if v == "NaN" else color, size=size)
        rows.add(VGroup(ic, vc).arrange(RIGHT, buff=0))
    return rows.arrange(DOWN, buff=0)


class PandasTables(Scene):
    def construct(self):
        title_card(self, "Tables that know their labels",
                   r"Python for Programmers \textperiodcentered{} Part 3: pandas")
        self.series()
        self.alignment()
        self.dataframe()
        self.filtering()
        self.groupby()
        end_card(self, [
            r"\texttt{Series} = NumPy array + index; \texttt{DataFrame} = columns sharing one index.",
            r"Arithmetic and joins \emph{align on labels}, not positions.",
            r"Filter with boolean masks: \texttt{df.loc[mask, cols]}, combine with \texttt{\&} \texttt{|} \texttt{\textasciitilde}.",
            r"\texttt{groupby} = split $\rightarrow$ apply $\rightarrow$ combine.",
        ])

    # ------------------------------------------------------------------ 1
    def series(self):
        self.next_section("series")
        head = chapter(self, "A Series is an array with labels")
        arr = VGroup(*[cell(v, w=1.4, h=0.9, color=C_VAL, size=36) for v in [10, 20, 30]]).arrange(DOWN, buff=0)
        arr.move_to(LEFT * 2.6 + DOWN * 0.3)
        arr_lab = Tex("NumPy array", font_size=34, color=C_VAL).next_to(arr, UP, buff=0.3)
        self.play(FadeIn(arr), FadeIn(arr_lab))
        idx = VGroup(*[cell(i, w=0.9, h=0.9, color=C_IDX, size=36, fill_opacity=0.05) for i in "abc"])
        idx.arrange(DOWN, buff=0).next_to(arr, LEFT, buff=0)
        idx_lab = Tex("index", font_size=34, color=C_IDX).next_to(idx, LEFT, buff=0.3)
        self.play(FadeIn(idx, shift=RIGHT * 0.6), FadeIn(idx_lab))
        code = code_panel('s = pd.Series([10, 20, 30],\n              index=["a", "b", "c"])', font_size=22)
        code.move_to(RIGHT * 3.4 + UP * 1.8)
        self.play(FadeIn(code))

        def ask(src, target, result, color):
            c = code_panel(src, font_size=26).next_to(code, DOWN, buff=0.5, aligned_edge=LEFT)
            box = SurroundingRectangle(target, color=color, buff=0.04, stroke_width=5)
            r = mono(result, 26, color=color).next_to(c, RIGHT, buff=0.3)
            self.play(FadeIn(c), Create(box))
            self.play(Write(r))
            self.wait(1)
            return VGroup(c, box, r)

        g1 = ask('s["b"]', VGroup(idx[1], arr[1]), "-> 20  by label", C_YELLOW)
        self.play(FadeOut(g1))
        g2 = ask("s.iloc[0]", arr[0], "-> 10  by position", C_GREEN)
        self.wait(0.5)
        fade_out_all(self)

    # ------------------------------------------------------------------ 2
    def alignment(self):
        self.next_section("alignment")
        head = chapter(self, "Arithmetic aligns on labels")
        s1 = series_col("abc", [1, 2, 3]).move_to(LEFT * 4.6 + DOWN * 0.3)
        s2 = series_col("bcd", [10, 20, 30], color=C_GOLD).move_to(LEFT * 1.0 + DOWN * 0.9)
        l1 = mono("s1", 26, color=C_VAL).next_to(s1, UP, buff=0.25)
        l2 = mono("s2", 26, color=C_GOLD).next_to(s2, UP, buff=0.25)
        # '+' on row 'a' (which has no partner), so it never sits on a link line
        plus = MathTex("+", font_size=56).move_to([(s1.get_right()[0] + s2.get_left()[0]) / 2,
                                                   s1[0].get_center()[1], 0])
        self.play(FadeIn(s1), FadeIn(l1), FadeIn(s2), FadeIn(l2), Write(plus))
        trap = Tex(r"Position by position? No: by \emph{label}.", font_size=30, color=C_GREY)
        trap.to_edge(UP, buff=1.0)
        self.play(FadeIn(trap))
        # link matching labels
        links = VGroup(
            DashedLine(s1[1].get_right(), s2[0].get_left(), color=C_YELLOW),
            DashedLine(s1[2].get_right(), s2[1].get_left(), color=C_YELLOW),
        )
        self.play(Create(links), Indicate(VGroup(s1[1][0], s1[2][0], s2[0][0], s2[1][0])))
        self.wait(0.6)
        res = series_col("abcd", ["NaN", 12, 23, "NaN"], color=C_TEAL)
        res.move_to(RIGHT * 4.3 + DOWN * 0.6)
        lr = mono("s1 + s2", 26, color=C_TEAL).next_to(res, UP, buff=0.25)
        eq = MathTex("=", font_size=56).move_to((s2.get_right() + res.get_left()) / 2 + UP * 0.2)
        self.play(Write(eq), FadeIn(lr))
        self.play(FadeIn(res[0][0]), FadeIn(res[3][0]))
        self.play(TransformFromCopy(VGroup(s1[1][1], s2[0][1]), res[1][1]),
                  TransformFromCopy(VGroup(s1[2][1], s2[1][1]), res[2][1]),
                  FadeIn(res[1][0]), FadeIn(res[2][0]), run_time=1.5)
        self.play(FadeIn(res[0][1]), FadeIn(res[3][1]))
        cap = caption(r"Labels found in only one Series have no partner, so the result is \texttt{NaN}")
        self.play(FadeIn(cap))
        self.wait(2.5)
        fade_out_all(self)

    # ------------------------------------------------------------------ 3
    def dataframe(self):
        self.next_section("dataframe")
        head = chapter(self, "A DataFrame: columns sharing one index")
        rows = [("city", "month", "sales")] + [r[1:] for r in DF]
        t = table_grid(rows, [1.7, 1.3, 1.4], row_h=0.55, size=24, index=[r[0] for r in DF], index_w=0.6)
        t.move_to(LEFT * 2.2 + DOWN * 0.3)
        ncols = len(t[0])
        col = lambda c: VGroup(*[t[r][c] for r in range(len(t))])
        self.play(FadeIn(col(0), shift=RIGHT * 0.3))
        for c in range(1, ncols):
            self.play(FadeIn(col(c), shift=UP * 0.4), run_time=0.8)
        dtypes = ["str", "str", "float64"]
        dt = VGroup(*[mono(d, 22, color=GREY_B).next_to(t[-1][c + 1], DOWN, buff=0.15) for c, d in enumerate(dtypes)])
        self.play(FadeIn(dt))
        # each column is a Series
        box = SurroundingRectangle(VGroup(col(0), col(3)), color=C_VAL, buff=0.02, stroke_width=4)
        note = Tex(r'\texttt{df["sales"]} is a Series:\\the shared index + one column', font_size=32)
        note.move_to(RIGHT * 4.2 + UP * 1.0)
        self.play(Create(box), FadeIn(note))
        self.wait(1)
        nan = t[6][3]
        nbox = SurroundingRectangle(nan, color=C_BAD, buff=0.03, stroke_width=4)
        nnote = Tex(r"\texttt{None} became \texttt{NaN},\\so \texttt{sales} is \texttt{float64}",
                    font_size=32, color=C_BAD).move_to(RIGHT * 4.2 + DOWN * 1.2)
        self.play(Create(nbox), FadeIn(nnote))
        self.wait(2)
        self.play(FadeOut(VGroup(box, note, nbox, nnote, dt)), FadeOut(head))
        self.table = t

    # ------------------------------------------------------------------ 4
    def filtering(self):
        self.next_section("filtering")
        t = self.table
        self.play(t.animate.move_to(LEFT * 3.4 + DOWN * 0.4))
        head = chapter(self, "Filtering with a mask", corner_only=True)
        code = code_panel('mask = df["sales"] > 100\ndf.loc[mask, ["city", "sales"]]', font_size=22)
        code.move_to(RIGHT * 3.3 + UP * 2.2)
        mk = line_marker(code, 0)
        self.play(FadeIn(code), FadeIn(mk))
        mask_vals = [True, False, True, False, True, False]
        mcol = VGroup(cell("mask", w=1.1, h=0.55, color=C_GREY, size=20, fill_opacity=0.05))
        for m in mask_vals:
            mcol.add(cell(str(m), w=1.1, h=0.55, color=C_GREEN if m else C_BAD, size=20,
                          fill_opacity=0.3))
        mcol.arrange(DOWN, buff=0).next_to(t, RIGHT, buff=0.25)
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in mcol], lag_ratio=0.12), run_time=1.5)
        self.wait(0.6)
        self.play(Transform(mk, line_marker(code, 1)))
        keep = [0] + [i + 1 for i, m in enumerate(mask_vals) if m]
        drop = [i + 1 for i, m in enumerate(mask_vals) if not m]
        self.play(*[t[r].animate.set_opacity(0.15) for r in drop],
                  *[mcol[r].animate.set_opacity(0.15) for r in drop], run_time=1)
        # result: rows 0,2,4 with columns city, sales; index labels are kept
        res_rows = [("city", "sales")] + [(DF[r - 1][1], DF[r - 1][3]) for r in keep[1:]]
        res = table_grid(res_rows, [1.7, 1.4], row_h=0.55, size=24,
                         index=[DF[r - 1][0] for r in keep[1:]], index_w=0.6)
        res.move_to(RIGHT * 3.6 + DOWN * 0.6)
        anims = []
        for k, r in enumerate(keep):
            src = VGroup(t[r][0], t[r][1], t[r][3])
            anims.append(TransformFromCopy(src, res[k]))
        self.play(LaggedStart(*anims, lag_ratio=0.2), run_time=2)
        idx_box = SurroundingRectangle(VGroup(*[res[k][0] for k in range(1, 4)]), color=C_YELLOW, buff=0.03)
        cap = caption(r"Rows keep their labels \texttt{0, 2, 4}: the index travels with the data")
        self.play(Create(idx_box), FadeIn(cap))
        self.wait(2.5)
        fade_out_all(self)

    # ------------------------------------------------------------------ 5
    def groupby(self):
        self.next_section("groupby")
        head = chapter(self, "Group by: split, apply, combine")
        code = code_panel('df.groupby("city")["sales"].sum()', font_size=24).to_edge(UP, buff=0.9)
        self.play(FadeIn(code))
        rows = [("city", "sales")] + [(r[1], r[3]) for r in DF]
        t = table_grid(rows, [1.6, 1.25], row_h=0.5, size=22, index=[r[0] for r in DF], index_w=0.5)
        t.move_to(LEFT * 4.6 + DOWN * 0.6)
        self.play(FadeIn(t))
        # colour every row by its city
        self.play(*[t[i + 1][1][0].animate.set_fill(CITY[DF[i][1]], opacity=0.45) for i in range(6)])

        labels = VGroup(*[Tex(s, font_size=34, color=C_YELLOW) for s in ["split", "apply", "combine"]])
        for lab, x in zip(labels, [-0.4, 2.4, 5.0]):
            lab.move_to([x, 1.75, 0])

        # ---- split
        self.play(Write(labels[0]))
        order = {"Berlin": [1, 4], "Tehran": [0, 2], "Tokyo": [3, 5]}  # sorted keys, like pandas
        groups = {}
        y = 0.9
        moves = []
        for city, idxs in order.items():
            g = VGroup()
            for i in idxs:
                tgt = t[i + 1].copy().move_to([-0.4, y, 0])
                y -= 0.5
                moves.append(Transform(t[i + 1], tgt))
                g.add(t[i + 1])
            groups[city] = g
            y -= 0.35
        self.play(LaggedStart(*moves, lag_ratio=0.12), FadeOut(t[0]), run_time=2.2)
        self.wait(0.5)

        # ---- apply
        self.play(Write(labels[1]))
        sums = {"Berlin": "205.0", "Tehran": "260.0", "Tokyo": "80.0"}
        sum_cells = {}
        for city, g in groups.items():
            sc = cell(sums[city], w=1.25, h=0.6, color=CITY[city], size=24, fill_opacity=0.3)
            sc.move_to([2.4, g.get_center()[1], 0])
            sum_cells[city] = sc
        anims = [ReplacementTransform(VGroup(*[r[2].copy() for r in g]), sum_cells[c]) for c, g in groups.items()]
        self.play(LaggedStart(*anims, lag_ratio=0.3), run_time=2)
        nan_note = Tex(r"\texttt{NaN} is skipped", font_size=24, color=C_BAD)
        nan_note.next_to(sum_cells["Tokyo"], DOWN, buff=0.3)
        self.play(FadeIn(nan_note), Indicate(groups["Tokyo"][1][2], color=C_BAD))
        self.wait(0.6)

        # ---- combine
        self.play(Write(labels[2]))
        res = table_grid([("sales",)] + [(sums[c],) for c in order], [1.3], row_h=0.55, size=24,
                         index=list(order), index_w=1.5)
        res.move_to([5.0, -0.1, 0])
        city_lab = mono("city", 20, color=C_GREY).move_to(res[0][0])
        anims = []
        for k, city in enumerate(order, start=1):
            res[k][0][0].set_fill(CITY[city], opacity=0.35)
            anims.append(TransformFromCopy(sum_cells[city], res[k][1]))
            anims.append(FadeIn(res[k][0]))
        self.play(FadeIn(res[0]), FadeIn(city_lab), *anims, run_time=1.8)
        cap = caption(r"One line of code: split the rows by key, aggregate each group, glue the results")
        self.play(FadeIn(cap))
        self.wait(3)
        fade_out_all(self)
