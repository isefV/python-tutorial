from plots import *


class L31EndToEnd(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 31, "end-to-end", "Putting it together", "Matplotlib"

    def construct(self):
        self.intro("Lesson thirty-one, the last one, puts everything together: NumPy generates a year of raw data, "
                   "pandas turns it into a monthly table, and Matplotlib draws the result.",
                   r"NumPy $\rightarrow$ pandas $\rightarrow$ Matplotlib")
        self.pipeline()
        self.outro([r"NumPy: fast arrays and reproducible random data.",
                    r"pandas: label-aware tables; group, reshape, aggregate.",
                    r"Matplotlib: Figure, Axes and Artists, driven explicitly.",
                    r"Each step is a few lines because each library does one job well."],
                   "That's the full toolkit: Python for the logic, NumPy for numbers, pandas for tables and "
                   "Matplotlib for pictures. Thanks for watching, and happy coding.")

    def pipeline(self):
        rng = np.random.default_rng(42)
        cities = ["Tehran", "Berlin", "Tokyo"]
        n = 365
        city = rng.choice(cities, size=n)
        sales = rng.normal(100, 20, size=n).round(1)
        month = np.repeat(np.arange(12), [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
        order = ["Berlin", "Tehran", "Tokyo"]
        monthly = np.array([[sales[(month == m) & (city == c)].sum() for c in order] for m in range(12)])
        zone_x = [-4.9, -0.6, 3.9]
        titles = VGroup(tex(r"\textbf{NumPy}: 365 raw rows", 30), tex(r"\textbf{pandas}: $12 \times 3$ table", 30),
                        tex(r"\textbf{Matplotlib}: 3 lines", 30))
        for t, x in zip(titles, zone_x):
            t.move_to([x, 2.55, 0])
        cols, sq = 19, 0.17
        days = VGroup(*[Square(sq, stroke_width=0, fill_color=CITY_COL[c], fill_opacity=0.9) for c in city])
        days.arrange_in_grid(rows=int(np.ceil(n / cols)), cols=cols, buff=0.025).move_to([zone_x[0], -0.45, 0])
        code1 = mono('rng.choice(cities, size=365)\nrng.normal(100, 20, size=365)', 15, color=C_GREY).next_to(days, DOWN, buff=0.25)
        legend = VGroup(*[VGroup(Square(0.18, stroke_width=0, fill_color=CITY_COL[c], fill_opacity=1), Text(c, font_size=16)).arrange(RIGHT, buff=0.1)
                          for c in order]).arrange(RIGHT, buff=0.35).next_to(titles[0], DOWN, buff=0.2)
        with self.say("Step one, NumPy. A seeded generator draws a city and a sales figure for each of the three "
                      "hundred sixty-five days of a year. Each little square is one day, coloured by its city. "
                      "These go into a DataFrame with a date column."):
            self.play(Write(titles[0]))
            self.play(LaggedStart(*[FadeIn(d) for d in days], lag_ratio=0.004), FadeIn(code1), run_time=2)
            self.play(FadeIn(legend))
        counts = {c: int((city == c).sum()) for c in order}
        check = VGroup(mono("df.head()", 20, color=C_YELLOW),
                       mono("        date    city  sales\n0 2025-01-01  Tokyo  ...\n1 2025-01-02  Berlin ...", 16, color=GREY_B),
                       mono('df["city"].value_counts()', 20, color=C_YELLOW),
                       mono("\n".join(f"{c:7s} {n}" for c, n in counts.items()), 18)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        check.move_to([2.0, -0.3, 0])
        with self.say("Before aggregating anything, look at the data. head shows the columns came out as intended, "
                      "and value counts confirms roughly a third of the days for each city. Two seconds of checking "
                      "saves an hour of debugging."):
            self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in check], lag_ratio=0.3), run_time=2)
        self.play(FadeOut(check))
        mnames ="Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
        rows = [tuple(order)] + [tuple(f"{v:.0f}" for v in monthly[m]) for m in range(12)]
        table = table_grid(rows, [0.95, 0.95, 0.95], row_h=0.34, size=15, index=mnames, index_w=0.6).move_to([zone_x[1], -0.55, 0])
        for k, c in enumerate(order):
            table[0][k + 1][1].set_color(CITY_COL[c])
        code2 = mono('groupby([Grouper(freq="ME"), "city"])\n  ["sales"].sum().unstack("city")', 14, color=C_GREY).next_to(table, DOWN, buff=0.15)
        with self.say("Step two, pandas. One chain groups the rows by month and by city, sums the sales in each "
                      "group, and unstacks the cities into columns. Three hundred sixty-five rows become a "
                      "twelve by three table."):
            self.play(Write(titles[1]), FadeIn(table[0]), FadeIn(code2))
            anims = []
            for m in range(12):
                for k, c in enumerate(order):
                    sel = [d for d, mm, cc in zip(days, month, city) if mm == m and cc == c]
                    anims.append(ReplacementTransform(VGroup(*sel), table[m + 1][k + 1]))
                anims.append(FadeIn(table[m + 1][0]))
            self.play(LaggedStart(*anims, lag_ratio=0.02), run_time=4)
        ax = Axes(x_range=[0, 11, 1], y_range=[400, 1600, 400], x_length=4.3, y_length=3.6,
                  axis_config={"color": GREY_B, "stroke_width": 2, "include_tip": False, "tick_size": 0.04},
                  y_axis_config={"include_numbers": True, "font_size": 16}).move_to([zone_x[2] + 0.2, -0.5, 0])
        mlab = VGroup(*[Text(mnames[m][0], font_size=13, color=GREY_B).next_to(ax.c2p(m, 400), DOWN, buff=0.1) for m in range(12)])
        with self.say("Step three, Matplotlib. Calling plot on the table draws one line per column: each city's "
                      "monthly total becomes a line with a marker per month. The legend comes from the column "
                      "names, for free."):
            self.play(Write(titles[2]), Create(ax), FadeIn(mlab))
            for k, c in enumerate(order):
                colcells = VGroup(*[table[m + 1][k + 1] for m in range(12)])
                pts = [ax.c2p(m, monthly[m, k]) for m in range(12)]
                line = VMobject(color=CITY_COL[c], stroke_width=3).set_points_as_corners(pts)
                dots = VGroup(*[Dot(p, radius=0.045, color=CITY_COL[c]) for p in pts])
                self.play(Circumscribe(colcells, color=CITY_COL[c], buff=0.03), run_time=0.6)
                self.play(TransformFromCopy(VGroup(*[c_[1] for c_ in colcells]), dots), run_time=0.9)
                self.play(Create(line), run_time=0.7)
            code3 = mono('monthly.plot(marker="o")', 15, color=C_GREY).next_to(ax, DOWN, buff=0.45)
            self.play(FadeIn(code3))
        with self.say("Then the finishing touches from the last lessons: a y label and a title with ax dot set, a light "
                      "grid, and savefig to write the file."):
            grid = VGroup(*[DashedLine(ax.c2p(0, y), ax.c2p(11, y), color=GREY_D, stroke_width=1) for y in (800, 1200, 1600)])
            ttl = Text("Monthly sales by city", font_size=16, weight=BOLD).next_to(ax, UP, buff=0.12)
            yl = Text("monthly sales", font_size=13, color=GREY_B).rotate(PI / 2).next_to(ax, LEFT, buff=0.45)
            self.play(Create(grid), FadeIn(ttl), FadeIn(yl))
            sv = mono('fig.savefig("sales.png", dpi=200)', 15, color=C_GREEN).next_to(code3, DOWN, buff=0.1)
            self.play(FadeIn(sv))
        with self.say("About fifteen lines of code in total, because each library does one job well and they "
                      "all speak NumPy arrays underneath."):
            cap = caption(r"365 rows $\rightarrow$ one chain of pandas calls $\rightarrow$ one plot call")
            self.play(FadeOut(sv), FadeIn(cap))
        fade_out_all(self)
