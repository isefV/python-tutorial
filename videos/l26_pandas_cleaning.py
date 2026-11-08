from tables import *


class L26PandasCleaning(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 26, "pandas-cleaning", "Cleaning and transforming", "pandas"

    def construct(self):
        self.intro("Lesson twenty-six: cleaning and transforming. Real data is messy. This lesson covers missing "
                   "values, new columns, text and date columns, and a clean style for chaining it all together.",
                   r"\texttt{fillna}, \texttt{assign}, \texttt{.str}, \texttt{.dt}, method chains, Copy-on-Write")
        self.missing()
        self.new_cols()
        self.accessors()
        self.chain()
        self.cow()
        self.outro([r"\texttt{dropna} removes, \texttt{fillna} replaces missing values.",
                    r"New columns from vectorized expressions; \texttt{astype}, \texttt{rename}.",
                    r"\texttt{.str} and \texttt{.dt} apply string and date methods to whole columns.",
                    r"Chain methods; assign with \texttt{df.loc[mask, col] = ...}, never chained."],
                   "Decide what missing means, build columns with vectorized expressions, use the str and dt "
                   "accessors, write transformations as one readable chain, and assign through loc.")

    def missing(self):
        h = self.heading("Missing values")
        s = series_col(range(6), [r[3] for r in DF], w_val=1.2).move_to(LEFT * 4.5 + DOWN * 0.4)
        sl = mono('df["sales"]', 24, color=C_VAL).next_to(s, UP, buff=0.25)
        drop = series_col(range(5), [r[3] for r in DF[:5]], w_val=1.2, color=C_TEAL).move_to(LEFT * 0.6 + DOWN * 0.1)
        dl = mono(".dropna()", 24, color=C_TEAL).next_to(drop, UP, buff=0.25)
        fill = series_col(range(6), [r[3] for r in DF[:5]] + ["109.0"], w_val=1.2, color=C_GOLD).move_to(RIGHT * 3.6 + DOWN * 0.4)
        fl = mono(".fillna(mean)", 24, color=C_GOLD).next_to(fill, UP, buff=0.25)
        with self.say("You have two basic options for missing values. dropna removes the rows that contain them. "
                      "fillna replaces them, with zero, or with something smarter like the column mean. Which one is "
                      "right depends on what missing means in your data."):
            self.play(FadeIn(s), FadeIn(sl))
            self.play(Indicate(s[5], color=C_BAD))
            self.play(TransformFromCopy(VGroup(*s[:5]), drop), FadeIn(dl))
            self.play(TransformFromCopy(s, fill), FadeIn(fl))
            self.play(Circumscribe(fill[5], color=C_GOLD))
        self.clear(keep=[h])
        self.h = h

    def new_cols(self):
        h = self.swap_heading(self.h, "New columns and types")
        code = code_panel('df["sales"] = df["sales"].fillna(0)\ndf["tax"] = df["sales"] * 0.1\ndf["big"] = df["sales"] > 100\n'
                          'df = df.astype({"sales": "int64"})\ndf = df.rename(columns={"sales": "revenue"})',
                          font_size=24).to_edge(UP, buff=1.0)
        mk = Marker(code)
        rows = [("revenue", "tax", "big")] + [(v, t, b) for v, t, b in
                                              [("120", "12.0", "True"), ("95", "9.5", "False"), ("140", "14.0", "True"),
                                               ("80", "8.0", "False"), ("110", "11.0", "True"), ("0", "0.0", "False")]]
        t = table_grid(rows, [1.5, 1.3, 1.3], row_h=0.48, size=22, index=list(range(6)), index_w=0.6).next_to(code, DOWN, buff=0.4)
        with self.say("Assigning to a new column name creates it. The right side is a whole-column expression, so "
                      "there's no loop: tax is ten percent of sales, big is a boolean column. astype converts types, "
                      "and rename changes labels."):
            self.play(FadeIn(code))
            self.play(mk.to(0), FadeIn(column(t, 0)), FadeIn(column(t, 1)))
            self.play(mk.to(1), FadeIn(column(t, 2), shift=0.2 * LEFT))
            self.play(mk.to(2), FadeIn(column(t, 3), shift=0.2 * LEFT))
            self.play(mk.to(3, 4), Indicate(t[0][1], color=C_GOLD))
        self.clear(keep=[h])
        self.h = h

    def accessors(self):
        h = self.swap_heading(self.h, "String and date accessors")
        before = VGroup(mono('" ada lovelace"', 26, color=C_GREY), mono('"Alan Turing "', 26, color=C_GREY),
                        mono('"grace HOPPER"', 26, color=C_GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        after = VGroup(mono('"Ada Lovelace"', 26, color=C_GREEN), mono('"Alan Turing"', 26, color=C_GREEN),
                       mono('"Grace Hopper"', 26, color=C_GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        VGroup(before, after).arrange(RIGHT, buff=2.8).move_to(UP * 0.6)
        arr = Arrow(before.get_right(), after.get_left(), buff=0.3, color=C_YELLOW)
        lab = mono(".str.strip().str.title()", 24, color=C_YELLOW).next_to(VGroup(before, after), UP, buff=0.5)
        with self.say("Text columns have a str accessor that applies string methods to every value: strip "
                      "whitespace, fix capitalization, split into parts. No loop, and missing values are handled "
                      "for you."):
            self.play(FadeIn(before))
            self.play(GrowArrow(arr), FadeIn(lab))
            self.play(TransformFromCopy(before, after))
        with self.say("Dates work the same way. Convert with to datetime, then the dt accessor gives you the year, "
                      "month, weekday and more."):
            d = VGroup(mono('pd.to_datetime(df["joined"])', 26), mono('df["joined"].dt.year  -> 2024, 2024, 2025', 26, color=C_TEAL))
            d.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 1.9)
            self.play(FadeIn(d, shift=0.2 * UP))
        self.clear(keep=[h])
        self.h = h

    def chain(self):
        h = self.swap_heading(self.h, "Method chaining")
        code = code_panel('clean = (\n    df.dropna(subset=["sales"])\n      .assign(tax=lambda d: d["sales"] * 0.1)\n'
                          '      .sort_values("sales", ascending=False)\n      .reset_index(drop=True)\n)',
                          font_size=26).to_edge(LEFT, buff=0.5)
        mk = Marker(code)
        steps = VGroup(*[pill(s, c, 22) for s, c in [("6 rows", C_GREY), ("5 rows", C_BLUE), ("+ tax", C_GOLD),
                                                       ("sorted", C_TEAL), ("index 0..4", C_GREEN)]]).arrange(DOWN, buff=0.45)
        steps.to_edge(RIGHT, buff=1.2)
        arrows = VGroup(*[Arrow(steps[i].get_bottom(), steps[i + 1].get_top(), buff=0.05, color=GREY_B) for i in range(4)])
        with self.say("Most pandas methods return a new DataFrame, so you can chain them. Wrap the chain in "
                      "parentheses and put one step per line: it reads top to bottom like a recipe, with no "
                      "half-finished temporary variables. assign adds columns inside the chain."):
            self.play(FadeIn(code), FadeIn(steps[0]))
            for i in range(4):
                self.play(mk.to(1 + i), GrowArrow(arrows[i]), FadeIn(steps[i + 1], shift=0.2 * DOWN), run_time=0.9)
        self.clear(keep=[h])
        self.h = h

    def cow(self):
        h = self.swap_heading(self.h, "No chained assignment; vectorize")
        bad = code_panel('df[df["sales"] > 100]["tax"] = 0     # does nothing', font_size=26)
        good = code_panel('df.loc[df["sales"] > 100, "tax"] = 0', font_size=26)
        VGroup(bad, good).arrange(DOWN, buff=0.6).move_to(UP * 0.9)
        with self.say("One trap. Indexing twice and then assigning modifies a temporary copy, so the original never "
                      "changes; with Copy-on-Write in modern pandas it simply has no effect. Do it in one step with loc."):
            self.play(FadeIn(bad))
            self.play(Create(SurroundingRectangle(bad, color=C_BAD, buff=0.06)))
            self.play(FadeIn(good))
            self.play(Create(SurroundingRectangle(good, color=C_GREEN, buff=0.06)))
        with self.say("And avoid apply with a Python function per row when a vectorized version exists: np dot where "
                      "does the same job many times faster."):
            v = VGroup(mono('df.apply(lambda row: ..., axis=1)    slow', 24, color=C_BAD),
                       mono('np.where(df["sales"] > 100, "big", "small")', 24, color=C_GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            v.move_to(DOWN * 2.0)
            self.play(FadeIn(v, shift=0.2 * UP))
        self.clear()
