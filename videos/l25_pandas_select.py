from tables import *


class L25PandasSelect(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 25, "pandas-selecting", "Selecting and filtering", "pandas"

    def construct(self):
        self.intro("Lesson twenty-five: selecting and filtering. pandas has two indexers, loc for labels and iloc "
                   "for positions, plus boolean masks for picking rows by condition.",
                   r"columns, \texttt{loc}, \texttt{iloc}, masks, \texttt{query}")
        self.t = df_table().move_to(LEFT * 3.2 + DOWN * 0.4)
        self.columns_()
        self.loc_iloc()
        self.filtering()
        self.query()
        self.outro([r'\texttt{df["col"]} gives a Series, \texttt{df[["a", "b"]]} a DataFrame.',
                    r"\texttt{.loc[rows, cols]} by label (end \emph{included}); \texttt{.iloc} by position.",
                    r"Filter with masks: \texttt{\&}, \texttt{|}, \texttt{\~}, \texttt{isin}, \texttt{between}.",
                    r"\texttt{query()} for readable conditions; \texttt{@name} uses a variable."],
                   "Brackets pick columns, loc and iloc pick rows and columns by label or position, and masks filter "
                   "rows by any condition you can express as a boolean Series.")

    def box(self, mobs, color=C_YELLOW):
        return VGroup(*[SurroundingRectangle(m, color=color, buff=0.02, stroke_width=4) for m in mobs])

    def columns_(self):
        h = self.heading("Selecting columns")
        t = self.t
        with self.say("Square brackets with one column name return that column as a Series. With a list of names "
                      "you get a smaller DataFrame. Note the double brackets: the outer pair indexes, the inner pair "
                      "is a Python list."):
            self.play(FadeIn(t))
            c1 = mono('df["sales"]', 30, color=C_YELLOW).move_to(RIGHT * 3.6 + UP * 1.2)
            b = self.box([column(t, 3)])
            self.play(FadeIn(c1), Create(b))
            self.wait(0.6)
            c2 = mono('df[["city", "sales"]]', 30, color=C_GOLD).move_to(RIGHT * 3.6 + DOWN * 0.2)
            b2 = self.box([column(t, 1), column(t, 3)], C_GOLD)
            self.play(FadeIn(c2), ReplacementTransform(b, b2))
            self.wait(0.6)
            self.play(FadeOut(b2), FadeOut(c1), FadeOut(c2))
        self.h = h

    def loc_iloc(self):
        h = self.swap_heading(self.h, "loc by label, iloc by position")
        t = self.t
        with self.say("loc takes row labels and column labels. loc of zero to two, city and sales, includes row two: "
                      "label slices include their end."):
            c = mono('df.loc[0:2, ["city", "sales"]]', 28, color=C_YELLOW).move_to(RIGHT * 3.4 + UP * 1.6)
            sel = self.box([VGroup(t[r][1]) for r in range(1, 4)] + [VGroup(t[r][3]) for r in range(1, 4)])
            self.play(FadeIn(c), Create(sel))
            n = mono("rows 0, 1, 2", 26, color=C_YELLOW).next_to(c, DOWN, buff=0.3)
            self.play(FadeIn(n))
        with self.say("iloc counts positions like a Python list, so iloc of zero to two, zero to two stops before "
                      "position two. And iloc of minus one is the last row."):
            c2 = mono("df.iloc[0:2, 0:2]", 28, color=C_GOLD).move_to(RIGHT * 3.4 + DOWN * 0.2)
            sel2 = self.box([VGroup(t[r][1], t[r][2]) for r in range(1, 3)], C_GOLD)
            self.play(FadeIn(c2), ReplacementTransform(sel, sel2))
            n2 = mono("rows 0, 1 only", 26, color=C_GOLD).next_to(c2, DOWN, buff=0.3)
            self.play(FadeIn(n2))
            self.wait(0.5)
            self.play(FadeOut(VGroup(c, n, c2, n2, sel2)))
        self.h = h

    def filtering(self):
        h = self.swap_heading(self.h, "Boolean filtering")
        t = self.t
        code = code_panel('mask = df["sales"] > 100\ndf.loc[mask, ["city", "sales"]]', font_size=24).move_to(RIGHT * 3.4 + UP * 2.2)
        mk = Marker(code)
        mask_vals = [True, False, True, False, True, False]
        mcol = VGroup(cell("mask", w=1.1, h=0.55, color=C_GREY, size=20, fill_opacity=0.05))
        for m in mask_vals:
            mcol.add(cell(str(m), w=1.1, h=0.55, color=C_GREEN if m else C_BAD, size=20, fill_opacity=0.3))
        mcol.arrange(DOWN, buff=0).next_to(t, RIGHT, buff=0.25)
        with self.say("A comparison on a column gives a boolean Series, one True or False per row. That's a mask. "
                      "NaN compares as False."):
            self.play(FadeIn(code), mk.to(0))
            self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in mcol], lag_ratio=0.12), run_time=1.5)
        keep = [1, 3, 5]
        with self.say("Pass the mask to loc to keep only the True rows. The surviving rows keep their original "
                      "labels: zero, two and four. The index travels with the data."):
            self.play(mk.to(1))
            self.play(*[t[r].animate.set_opacity(0.15) for r in (2, 4, 6)], *[mcol[r].animate.set_opacity(0.15) for r in (2, 4, 6)])
            res = table_grid([("city", "sales")] + [(DF[r - 1][1], DF[r - 1][3]) for r in keep], [1.7, 1.4], row_h=0.55,
                             size=24, index=[DF[r - 1][0] for r in keep], index_w=0.6).move_to(RIGHT * 4.3 + DOWN * 1.0)
            self.play(LaggedStart(*[TransformFromCopy(VGroup(t[r][0], t[r][1], t[r][3]), res[k])
                                    for k, r in enumerate([0] + keep)], lag_ratio=0.2), run_time=2)
            self.play(Create(SurroundingRectangle(VGroup(*[res[k][0] for k in range(1, 4)]), color=C_YELLOW, buff=0.03)))
        self.clear(keep=[h])
        self.h = h

    def query(self):
        h = self.swap_heading(self.h, "Combining conditions, query and between")
        rows = VGroup(mono('df[(df["sales"] > 90) & (df["month"] == "Jan")]', 26),
                      mono('df[df["city"].isin(["Berlin", "Tokyo"])]', 26),
                      mono('df[~df["sales"].isna()]', 26),
                      mono("df.query(\"city == 'Berlin' and sales > 100\")", 26, color=C_GOLD),
                      mono('df.query("sales >= @limit")', 26, color=C_GOLD),
                      mono('df[df["sales"].between(90, 120)]', 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        rows.move_to(DOWN * 0.2)
        with self.say("Combine masks with ampersand, bar and tilde for and, or and not, with parentheses around each "
                      "comparison. isin tests membership in a list. query takes the condition as a readable string, "
                      "where at name refers to a Python variable. between checks a range, inclusive."):
            self.play(LaggedStart(*[FadeIn(r, shift=0.2 * RIGHT) for r in rows], lag_ratio=0.35), run_time=4)
        self.clear()
