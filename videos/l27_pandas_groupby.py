from tables import *


class L27PandasGroupby(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 27, "pandas-groupby-merge", "Group, reshape and join", "pandas"

    def construct(self):
        self.intro("Lesson twenty-seven: grouping, reshaping and joining. If you know SQL, this is GROUP BY, pivot "
                   "tables and JOIN, all on DataFrames.", r"\texttt{groupby}, \texttt{transform}, \texttt{pivot\_table}, "
                   r"\texttt{melt}, \texttt{merge}")
        self.groupby()
        self.transform()
        self.pivot()
        self.merge()
        self.outro([r"\texttt{groupby(key).agg(...)}: split, apply, combine.",
                    r"\texttt{transform} returns a group statistic on every original row.",
                    r"\texttt{pivot\_table} goes long $\to$ wide, \texttt{melt} wide $\to$ long.",
                    r"\texttt{merge(on=, how=)} joins like SQL; \texttt{concat} stacks."],
                   "Group by splits rows by key, aggregates each group and combines the results; transform keeps "
                   "the original shape; pivot and melt reshape; merge and concat join tables.")

    def groupby(self):
        h = self.heading("groupby: split, apply, combine")
        code = code_panel('df.groupby("city")["sales"].sum()', font_size=26).to_edge(UP, buff=1.0)
        rows = [("city", "sales")] + [(r[1], r[3]) for r in DF]
        t = table_grid(rows, [1.6, 1.25], row_h=0.5, size=22, index=[r[0] for r in DF], index_w=0.5).move_to(LEFT * 4.6 + DOWN * 0.6)
        labels = VGroup(*[tex(s, 36, C_YELLOW) for s in ["split", "apply", "combine"]])
        for lab, x in zip(labels, [-0.4, 2.4, 5.0]):
            lab.move_to([x, 1.75, 0])
        order = {"Berlin": [1, 4], "Tehran": [0, 2], "Tokyo": [3, 5]}
        with self.say("groupby works in three steps. Split: the rows are divided into groups by the key, here the "
                      "city."):
            self.play(FadeIn(code), FadeIn(t))
            self.play(*[t[i + 1][1][0].animate.set_fill(CITY[DF[i][1]], opacity=0.45) for i in range(6)])
            self.play(Write(labels[0]))
            groups, y, moves = {}, 0.9, []
            for city, idxs in order.items():
                g = VGroup()
                for i in idxs:
                    moves.append(Transform(t[i + 1], t[i + 1].copy().move_to([-0.4, y, 0])))
                    g.add(t[i + 1])
                    y -= 0.5
                groups[city] = g
                y -= 0.35
            self.play(LaggedStart(*moves, lag_ratio=0.12), FadeOut(t[0]), run_time=2)
        sums = {"Berlin": "205.0", "Tehran": "260.0", "Tokyo": "80.0"}
        with self.say("Apply: an aggregation runs on each group separately, here a sum. Missing values are skipped. "
                      "Combine: the results are glued into a new Series, indexed by the group keys."):
            self.play(Write(labels[1]))
            cells = {}
            for city, g in groups.items():
                cells[city] = cell(sums[city], w=1.25, h=0.6, color=CITY[city], size=24, fill_opacity=0.3).move_to([2.4, g.get_center()[1], 0])
            self.play(LaggedStart(*[ReplacementTransform(VGroup(*[r[2].copy() for r in g]), cells[c]) for c, g in groups.items()],
                                  lag_ratio=0.3), run_time=1.8)
            self.play(Write(labels[2]))
            res = table_grid([("sales",)] + [(sums[c],) for c in order], [1.3], row_h=0.55, size=24, index=list(order), index_w=1.5)
            res.move_to([5.0, -0.1, 0])
            anims = []
            for k, city in enumerate(order, start=1):
                res[k][0][0].set_fill(CITY[city], opacity=0.35)
                anims += [TransformFromCopy(cells[city], res[k][1]), FadeIn(res[k][0])]
            self.play(FadeIn(res[0]), *anims, run_time=1.6)
        with self.say("agg runs several aggregations at once, and named aggregations give the result columns "
                      "clear names."):
            more = mono('df.groupby("city").agg(total=("sales", "sum"), months=("month", "nunique"))', 20, color=C_GREY)
            more.to_edge(DOWN, buff=0.5)
            self.play(FadeIn(more))
        self.clear(keep=[h])
        self.h = h

    def transform(self):
        h = self.swap_heading(self.h, "transform: group statistics on every row")
        code = code_panel('df["city_total"] = df.groupby("city")["sales"].transform("sum")\n'
                          'df["share"] = df["sales"] / df["city_total"]', font_size=24).to_edge(UP, buff=1.0)
        totals = {"Tehran": "260.0", "Berlin": "205.0", "Tokyo": "80.0"}
        shares = ["0.46", "0.46", "0.54", "1.00", "0.54", "NaN"]
        rows = [("city", "sales", "city_total", "share")] + [(r[1], r[3], totals[r[1]], s) for r, s in zip(DF, shares)]
        t = table_grid(rows, [1.6, 1.3, 1.9, 1.3], row_h=0.5, size=22, index=[r[0] for r in DF], index_w=0.5).next_to(code, DOWN, buff=0.5)
        with self.say("Sometimes you want the group result back on every original row, for example each sale's share "
                      "of its city's total. transform does that: same aggregation, but the output has the original "
                      "shape, so it can become a new column."):
            self.play(FadeIn(code), FadeIn(column(t, 0)), FadeIn(column(t, 1)), FadeIn(column(t, 2)))
            for r in range(1, 7):
                t[r][1][0].set_fill(CITY[DF[r - 1][1]], opacity=0.35)
            self.play(LaggedStart(*[FadeIn(t[r][3], shift=0.2 * LEFT) for r in range(7)], lag_ratio=0.12))
            self.play(LaggedStart(*[FadeIn(t[r][4], shift=0.2 * LEFT) for r in range(7)], lag_ratio=0.12))
        self.clear(keep=[h])
        self.h = h

    def pivot(self):
        h = self.swap_heading(self.h, r"Reshaping: pivot_table and melt")
        long = table_grid([("city", "month", "sales")] + [(r[1], r[2], r[3]) for r in DF], [1.5, 1.1, 1.2], row_h=0.48, size=22)
        long.move_to(LEFT * 4.2 + DOWN * 0.4)
        wide = table_grid([("Feb", "Jan")] + [("110.0", "95.0"), ("140.0", "120.0"), ("80.0", "0.0")], [1.3, 1.3], row_h=0.55,
                          size=24, index=["Berlin", "Tehran", "Tokyo"], index_w=1.5).move_to(RIGHT * 3.7 + DOWN * 0.4)
        wl = mono('pivot_table(index="city", columns="month",\n            values="sales", aggfunc="sum")', 20, color=C_YELLOW)
        wl.to_edge(UP, buff=1.0)
        a1 = Arrow(long.get_right() + UP * 0.4, wide.get_left() + UP * 0.4, buff=0.3, color=C_YELLOW)
        a2 = Arrow(wide.get_left() + DOWN * 0.4, long.get_right() + DOWN * 0.4, buff=0.3, color=C_TEAL)
        ml = mono("melt", 22, color=C_TEAL).next_to(a2, DOWN, buff=0.1)
        with self.say("Long data has one row per observation. pivot table spreads it out: cities become rows, months "
                      "become columns, and an aggregation fills the cells. melt is the inverse, folding the columns "
                      "back into rows, which is the shape plotting libraries usually prefer."):
            self.play(FadeIn(long))
            self.play(GrowArrow(a1), FadeIn(wl), FadeIn(wide, shift=0.3 * RIGHT))
            self.play(GrowArrow(a2), FadeIn(ml))
        self.clear(keep=[h])
        self.h = h

    def merge(self):
        h = self.swap_heading(self.h, "Joining tables")
        left = table_grid([("city", "sales")] + [(r[1], r[3]) for r in DF[:4]], [1.5, 1.2], row_h=0.5, size=22).move_to(LEFT * 5.0 + DOWN * 0.3)
        right = table_grid([("city", "country")] + [("Tehran", "IR"), ("Berlin", "DE"), ("Paris", "FR")], [1.5, 1.3],
                           row_h=0.5, size=22).move_to(LEFT * 1.6 + DOWN * 0.3)
        res = table_grid([("city", "sales", "country")] + [(r[1], r[3], {"Tehran": "IR", "Berlin": "DE"}.get(r[1], "NaN")) for r in DF[:4]],
                         [1.5, 1.2, 1.4], row_h=0.5, size=22).move_to(RIGHT * 3.7 + DOWN * 0.3)
        code = mono('df.merge(countries, on="city", how="left")', 26, color=C_YELLOW).to_edge(UP, buff=1.0)
        with self.say("merge joins two tables on a key column, like SQL. A left join keeps every row of the left "
                      "table and attaches the matching country. Tokyo has no match, so it gets NaN, and Paris, "
                      "which matches nothing on the left, is dropped. concat simply stacks tables."):
            self.play(FadeIn(code), FadeIn(left), FadeIn(right))
            links = VGroup(*[DashedLine(left[i].get_right(), right[j].get_left(), color=C_YELLOW)
                             for i, j in [(1, 1), (2, 2), (3, 1)]])
            self.play(Create(links))
            self.play(FadeIn(res, shift=0.3 * RIGHT))
            self.play(Circumscribe(res[4], color=C_BAD), Indicate(right[3], color=C_GREY))
        self.clear()
