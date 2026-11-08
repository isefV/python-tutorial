from tables import *


class L23PandasDataFrame(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 23, "pandas-dataframe", "Series and DataFrame", "pandas"

    def construct(self):
        self.intro("Lesson twenty-three begins pandas, the library for tables. It's built on NumPy, but adds the "
                   "thing NumPy lacks: labels. Every row and every column has a name.",
                   r"\texttt{Series}, index alignment, \texttt{DataFrame}")
        self.series()
        self.alignment()
        self.dataframe()
        self.index_cols()
        self.outro([r"A \texttt{Series} is a 1-D array with an index of labels.",
                    r"Arithmetic aligns on labels; unmatched labels give \texttt{NaN}.",
                    r"A \texttt{DataFrame} is a set of columns (Series) sharing one index.",
                    r"\texttt{shape}, \texttt{columns}, \texttt{index}; \texttt{set\_index} promotes a column."],
                   "A Series is labelled values, a DataFrame is labelled columns sharing an index, and every "
                   "operation lines data up by label rather than by position.")

    def series(self):
        h = self.heading("Series")
        code = code_panel('s = pd.Series([10, 20, 30], index=["a", "b", "c"])\ns["b"]\ns.iloc[0]\ns * 2',
                          font_size=26).to_edge(UP, buff=1.0)
        mk = Marker(code)
        s = series_col("abc", [10, 20, 30], w_idx=0.8, w_val=1.2, h=0.7, size=28).move_to(LEFT * 2.5 + DOWN * 1.2)
        il = tex("index", 30, C_GREY).next_to(s, UP, buff=0.2).align_to(s, LEFT)
        vl = tex("values", 30, C_VAL).next_to(il, RIGHT, buff=0.35)
        with self.say("A Series is a one-dimensional array of values with an index: a label for every element. "
                      "By default the labels are zero, one, two, but they can be anything, like letters."):
            self.play(FadeIn(code), mk.to(0))
            self.play(LaggedStart(*[FadeIn(r, shift=0.2 * RIGHT) for r in s], lag_ratio=0.2), FadeIn(il), FadeIn(vl))
        with self.say("Square brackets look up by label, so s of b is twenty. iloc looks up by position. And "
                      "arithmetic works on all values at once, just like NumPy."):
            self.play(mk.to(1))
            b1 = SurroundingRectangle(s[1], color=C_YELLOW, buff=0.03)
            r1 = mono("-> 20", 30, color=C_YELLOW).move_to(RIGHT * 2.6 + DOWN * 0.5)
            self.play(Create(b1), FadeIn(r1))
            self.play(mk.to(2))
            b2 = SurroundingRectangle(s[0], color=C_GOLD, buff=0.03)
            r2 = mono("-> 10   (position 0)", 30, color=C_GOLD).move_to(RIGHT * 2.6 + DOWN * 1.2)
            self.play(Transform(b1, b2), FadeIn(r2))
            self.play(mk.to(3))
            r3 = mono("-> [20, 40, 60]", 30, color=C_TEAL).move_to(RIGHT * 2.6 + DOWN * 1.9)
            self.play(FadeIn(r3))
        self.clear(keep=[h])
        self.h = h

    def alignment(self):
        h = self.swap_heading(self.h, "Arithmetic aligns on labels")
        s1 = series_col("abc", [1, 2, 3]).move_to(LEFT * 4.6 + DOWN * 0.3)
        s2 = series_col("bcd", [10, 20, 30], color=C_GOLD).move_to(LEFT * 1.0 + DOWN * 0.9)
        l1 = mono("s1", 26, color=C_VAL).next_to(s1, UP, buff=0.25)
        l2 = mono("s2", 26, color=C_GOLD).next_to(s2, UP, buff=0.25)
        plus = MathTex("+", font_size=56).move_to([(s1.get_right()[0] + s2.get_left()[0]) / 2, s1[0].get_center()[1], 0])
        with self.say("Here's what makes pandas different. Adding two Series does not pair them by position. "
                      "It pairs them by label: b with b, c with c."):
            self.play(FadeIn(s1), FadeIn(l1), FadeIn(s2), FadeIn(l2), Write(plus))
            links = VGroup(DashedLine(s1[1].get_right(), s2[0].get_left(), color=C_YELLOW),
                           DashedLine(s1[2].get_right(), s2[1].get_left(), color=C_YELLOW))
            self.play(Create(links), Indicate(VGroup(s1[1][0], s1[2][0], s2[0][0], s2[1][0])))
        res = series_col("abcd", ["NaN", 12, 23, "NaN"], color=C_TEAL).move_to(RIGHT * 4.3 + DOWN * 0.6)
        lr = mono("s1 + s2", 26, color=C_TEAL).next_to(res, UP, buff=0.25)
        eq = MathTex("=", font_size=56).move_to((s2.get_right() + res.get_left()) / 2 + UP * 0.2)
        with self.say("Labels that appear in only one of them have no partner, so the result there is NaN, "
                      "not a number. Alignment is automatic, and it prevents a whole class of silent "
                      "off-by-one bugs."):
            self.play(Write(eq), FadeIn(lr))
            self.play(FadeIn(res[0][0]), FadeIn(res[3][0]))
            self.play(TransformFromCopy(VGroup(s1[1][1], s2[0][1]), res[1][1]),
                      TransformFromCopy(VGroup(s1[2][1], s2[1][1]), res[2][1]), FadeIn(res[1][0]), FadeIn(res[2][0]),
                      run_time=1.5)
            self.play(FadeIn(res[0][1]), FadeIn(res[3][1]))
        self.clear(keep=[h])
        self.h = h

    def dataframe(self):
        h = self.swap_heading(self.h, "A DataFrame")
        code = code_panel('df = pd.DataFrame({\n    "city":  ["Tehran", "Berlin", ...],\n    "month": ["Jan", "Jan", ...],\n'
                          '    "sales": [120, 95, ..., None],\n})', font_size=22).to_edge(LEFT, buff=0.4).shift(UP * 1.4)
        t = df_table().move_to(RIGHT * 2.8 + DOWN * 0.3)
        with self.say("A DataFrame is a table. The easiest way to build one is a dict of columns. Each column is "
                      "really a Series, and all of them share one index, the row labels on the left."):
            self.play(FadeIn(code))
            self.play(FadeIn(column(t, 0), shift=RIGHT * 0.3))
            for c in range(1, 4):
                self.play(FadeIn(column(t, c), shift=UP * 0.4), run_time=0.7)
            box = SurroundingRectangle(VGroup(column(t, 0), column(t, 3)), color=C_VAL, buff=0.02, stroke_width=4)
            note = tex(r'\texttt{df["sales"]} is a Series', 32, C_VAL).next_to(code, DOWN, buff=0.6, aligned_edge=LEFT)
            self.play(Create(box), FadeIn(note))
        with self.say("Every column has its own d-type. The missing sale became NaN, and since NaN is a float, the "
                      "whole sales column is float sixty-four."):
            dt = VGroup(*[mono(d, 20, color=GREY_B).next_to(t[-1][c + 1], DOWN, buff=0.15) for c, d in enumerate(["str", "str", "float64"])])
            self.play(FadeIn(dt))
            nb = SurroundingRectangle(t[6][3], color=C_BAD, buff=0.03, stroke_width=4)
            nn = tex(r"\texttt{None} $\to$ \texttt{NaN}", 32, C_BAD).next_to(note, DOWN, buff=0.4, aligned_edge=LEFT)
            self.play(Create(nb), FadeIn(nn))
        self.t = t
        self.clear(keep=[h])
        self.h = h

    def index_cols(self):
        h = self.swap_heading(self.h, "Index, columns and shape")
        t = df_table().move_to(LEFT * 3.0 + DOWN * 0.3)
        info = VGroup(mono("df.shape    -> (6, 3)", 26), mono("df.columns  -> city, month, sales", 26),
                      mono("df.index    -> RangeIndex(0..5)", 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        info.move_to(RIGHT * 3.4 + UP * 1.2)
        with self.say("shape gives rows and columns. columns and index are the two sets of labels."):
            self.play(FadeIn(t))
            self.play(LaggedStart(*[FadeIn(i, shift=0.2 * LEFT) for i in info], lag_ratio=0.3))
            self.play(Circumscribe(t[0], color=C_YELLOW), Circumscribe(column(t, 0), color=C_GREY))
        with self.say("Any column can become the index with set index, so you can look rows up by city. "
                      "reset index turns it back into a normal column."):
            c = mono('df.set_index("city").loc["Berlin"]', 26, color=C_GOLD).move_to(RIGHT * 3.2 + DOWN * 0.6)
            self.play(FadeIn(c))
            t2 = table_grid([("month", "sales")] + [(r[2], r[3]) for r in DF], [1.3, 1.4], row_h=0.55, size=24,
                            index=[r[1] for r in DF], index_w=1.7).move_to(t)
            for r, row in enumerate(DF, start=1):
                t2[r][0][1].set_color(CITY[row[1]])
            hdr = mono("city", 22, color=C_GREY).move_to(t2[0][0])
            t2[0][0].add(hdr)
            self.play(ReplacementTransform(t, t2))
            sel = VGroup(SurroundingRectangle(t2[2], color=C_TEAL, buff=0.02), SurroundingRectangle(t2[5], color=C_TEAL, buff=0.02))
            self.play(Create(sel))
            res = mono("-> the two Berlin rows", 24, color=C_TEAL).next_to(c, DOWN, buff=0.3)
            self.play(FadeIn(res))
        self.clear()
