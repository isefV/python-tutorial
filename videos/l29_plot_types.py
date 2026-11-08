from plots import *


class L29PlotTypes(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 29, "matplotlib-plot-types", "Common plot types", "Matplotlib"

    def construct(self):
        self.intro("Lesson twenty-nine: the common plot types. Line, scatter, bar and histogram cover most needs; "
                   "a few more handle uncertainty, distributions and images.",
                   r"\texttt{plot}, \texttt{scatter}, \texttt{bar}, \texttt{hist}, \texttt{fill\_between}, \texttt{boxplot}, \texttt{imshow}")
        self.grid()
        self.uncertainty()
        self.distributions()
        self.image()
        self.outro([r"\texttt{plot} for trends, \texttt{scatter} for relations, \texttt{bar} for categories.",
                    r"\texttt{hist}, \texttt{boxplot}, \texttt{violinplot} show distributions.",
                    r"\texttt{fill\_between} and \texttt{errorbar} show uncertainty.",
                    r"\texttt{imshow} draws a 2-D array as an image; add a \texttt{colorbar}."],
                   "Pick the plot for the question: lines for trends, scatter for relationships, bars for "
                   "categories, histograms and box plots for distributions, and images for grids of values.")

    def grid(self):
        h = self.heading("Four basic plot types")
        code = code_panel('fig, axs = plt.subplots(2, 2, layout="constrained")', font_size=22).to_edge(UP, buff=0.9)
        panels = VGroup(*[Rectangle(width=5.6, height=2.5, stroke_color=GREY_D, stroke_width=1.5) for _ in range(4)])
        panels.arrange_in_grid(2, 2, buff=(0.4, 0.25)).next_to(code, DOWN, buff=0.3)

        def place(axes, p):
            return axes.move_to(p.get_center() + UP * 0.1 + RIGHT * 0.1)
        rng = np.random.default_rng(42)
        a1 = place(mini_axes(), panels[0])
        draw1 = [Create(a1.plot(np.sin, x_range=[0, 10, 0.05], color=C_BLUE, stroke_width=3)),
                 Create(a1.plot(np.cos, x_range=[0, 10, 0.05], color=C_GOLD, stroke_width=3))]
        a2 = place(mini_axes(x_range=(-3, 3, 1), y_range=(-3, 3, 1)), panels[1])
        xs = rng.normal(size=120)
        ys = 0.6 * xs + rng.normal(scale=0.6, size=120)
        pts = VGroup(*[Dot(a2.c2p(x, y), radius=0.035, color=C_TEAL, fill_opacity=0.75) for x, y in zip(xs, ys) if abs(x) < 3 and abs(y) < 3])
        a3 = place(mini_axes(x_range=(0, 4, 1), y_range=(0, 45, 15)), panels[2])
        bars = bars_on(a3, [42, 27, 31, 18], C_GREEN)
        a4 = place(mini_axes(x_range=(-4, 4, 2), y_range=(0, 120, 40)), panels[3])
        hist = hist_on(a4, rng.normal(size=1000), 30, (-4, 4), C_PURPLE)
        codes = ["ax.plot(x, np.sin(x))", "ax.scatter(xs, ys)", 'ax.bar(["A","B","C","D"], vals)', "ax.hist(samples, bins=30)"]
        titles = ["Line", "Scatter", "Bar", "Histogram"]
        steps = [(a1, draw1), (a2, [LaggedStart(*[FadeIn(d, scale=0.3) for d in pts], lag_ratio=0.01)]),
                 (a3, [LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2)]),
                 (a4, [LaggedStart(*[GrowFromEdge(b, DOWN) for b in hist], lag_ratio=0.04)])]
        narr = ["subplots with two rows and two columns gives a grid of four Axes. A line plot connects points in "
                "order: the natural choice for a trend over time.",
                "A scatter plot draws one marker per pair of values, to show how two variables relate.",
                "Bars compare a value across categories.",
                "And a histogram counts how many values fall into each bin, which shows the shape of a distribution."]
        for k, ((axes, draw), n) in enumerate(zip(steps, narr)):
            with self.say(n):
                if k == 0:
                    self.play(FadeIn(code), LaggedStart(*[Create(p) for p in panels], lag_ratio=0.2))
                tt = tex(rf"\textbf{{{titles[k]}}}", 28).next_to(panels[k].get_top(), DOWN, buff=0.08)
                c = mono(codes[k], 15, color=C_GREY).next_to(panels[k].get_bottom(), UP, buff=0.07)
                self.play(Create(axes), FadeIn(c), FadeIn(tt), run_time=0.8)
                self.play(*draw, run_time=1.6)
        self.clear(keep=[h])
        self.h = h

    def uncertainty(self):
        h = self.swap_heading(self.h, "Uncertainty: fill_between and errorbar")
        ax1 = mini_axes(w=5.2, h=3.0, x_range=(0, 9, 3), y_range=(0, 3.5, 1)).move_to(LEFT * 3.4 + DOWN * 0.4)
        ax2 = mini_axes(w=5.2, h=3.0, x_range=(0, 9, 3), y_range=(0, 3.5, 1)).move_to(RIGHT * 3.4 + DOWN * 0.4)
        f = np.sqrt
        band = ax1.get_area(ax1.plot(lambda x: f(x) + 0.3, x_range=[0, 9]), x_range=[0, 9],
                            bounded_graph=ax1.plot(lambda x: max(f(x) - 0.3, 0), x_range=[0, 9]), color=C_BLUE, opacity=0.3)
        line = ax1.plot(f, x_range=[0, 9], color=C_BLUE, stroke_width=3)
        dots = VGroup()
        for x in range(10):
            p = ax2.c2p(x, f(x))
            bar = Line(ax2.c2p(x, f(x) - 0.3), ax2.c2p(x, f(x) + 0.3), color=C_GOLD, stroke_width=2)
            caps = VGroup(*[Line(LEFT * 0.06, RIGHT * 0.06, color=C_GOLD, stroke_width=2).move_to(ax2.c2p(x, f(x) + s)) for s in (-0.3, 0.3)])
            dots.add(VGroup(bar, caps, Dot(p, radius=0.06, color=C_GOLD)))
        l1 = mono("ax.fill_between(x, lo, hi, alpha=0.3)", 20, color=C_GREY).next_to(ax1, DOWN, buff=0.3)
        l2 = mono("ax.errorbar(x, mean, yerr=0.3, capsize=3)", 20, color=C_GREY).next_to(ax2, DOWN, buff=0.3)
        with self.say("Real measurements come with uncertainty. fill between shades a band between a lower and an "
                      "upper curve, good for continuous data. errorbar puts a bar on each individual point."):
            self.play(Create(ax1), Create(ax2))
            self.play(Create(line), FadeIn(band), FadeIn(l1))
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.1), FadeIn(l2))
        self.clear(keep=[h])
        self.h = h

    def distributions(self):
        h = self.swap_heading(self.h, "Distributions: boxplot and violinplot")
        ax = mini_axes(w=6.0, h=4.0, x_range=(0, 4, 1), y_range=(-8, 8, 4)).move_to(LEFT * 2.4 + DOWN * 0.3)
        rng = np.random.default_rng(1)
        groups = [rng.normal(0, s, 200) for s in (1, 2, 3)]
        boxes = VGroup()
        for k, g in enumerate(groups, start=1):
            q1, med, q3 = np.percentile(g, [25, 50, 75])
            iqr = q3 - q1
            lo, hi = max(g.min(), q1 - 1.5 * iqr), min(g.max(), q3 + 1.5 * iqr)
            col = [C_BLUE, C_GOLD, C_TEAL][k - 1]
            body = Rectangle(width=0.7, height=ax.c2p(0, q3)[1] - ax.c2p(0, q1)[1], stroke_color=col, fill_color=col,
                             fill_opacity=0.25).move_to(ax.c2p(k, (q1 + q3) / 2))
            mline = Line(ax.c2p(k - 0.35, med), ax.c2p(k + 0.35, med), color=WHITE, stroke_width=3)
            wh = VGroup(Line(ax.c2p(k, q3), ax.c2p(k, hi), color=col), Line(ax.c2p(k, q1), ax.c2p(k, lo), color=col),
                        Line(ax.c2p(k - 0.15, hi), ax.c2p(k + 0.15, hi), color=col), Line(ax.c2p(k - 0.15, lo), ax.c2p(k + 0.15, lo), color=col))
            boxes.add(VGroup(body, mline, wh))
        labels = VGroup(tex("median", 28, WHITE), tex("middle 50\\%", 28, C_GOLD), tex("whiskers", 28, C_GOLD))
        labels.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 4.2 + UP * 0.6)
        with self.say("A box plot summarizes each group in five numbers: the box spans the middle half of the data, "
                      "the line is the median, and the whiskers reach the bulk of the rest. Three groups with growing "
                      "spread show up instantly. A violin plot draws the full estimated shape instead."):
            self.play(Create(ax))
            self.play(LaggedStart(*[FadeIn(b, shift=0.2 * UP) for b in boxes], lag_ratio=0.3), run_time=2)
            self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.3))
            code = mono('ax.boxplot(groups, tick_labels=["a", "b", "c"])\nax.violinplot(groups)', 20, color=C_GREY)
            code.next_to(ax, DOWN, buff=0.35)
            self.play(FadeIn(code))
        self.clear(keep=[h])
        self.h = h

    def image(self):
        h = self.swap_heading(self.h, "Images and heatmaps: imshow")
        n = 24
        y, x = np.mgrid[-2:2:n * 1j, -2:2:n * 1j]
        z = np.exp(-(x ** 2 + y ** 2))
        cmap = [ManimColor("#440154"), ManimColor("#3b528b"), ManimColor("#21918c"), ManimColor("#5ec962"), ManimColor("#fde725")]

        grad = color_gradient(cmap, 101)

        def col(v):
            return grad[int(round(min(max(v, 0), 1) * 100))]
        sq = 4.2 / n
        img = VGroup(*[Square(sq, stroke_width=0, fill_color=col(float(z[i, j])), fill_opacity=1)
                       for i in range(n - 1, -1, -1) for j in range(n)]).arrange_in_grid(n, n, buff=0).move_to(LEFT * 1.5 + DOWN * 0.3)
        bar = VGroup(*[Rectangle(width=0.35, height=4.2 / 50, stroke_width=0, fill_color=col(k / 49), fill_opacity=1) for k in range(50)])
        bar.arrange(UP, buff=0).next_to(img, RIGHT, buff=0.4)
        bl = VGroup(mono("1.0", 18).next_to(bar, RIGHT, buff=0.1).align_to(bar, UP), mono("0.0", 18).next_to(bar, RIGHT, buff=0.1).align_to(bar, DOWN))
        code = mono('ax.imshow(z, origin="lower", cmap="viridis")\nfig.colorbar(image, ax=ax)', 22, color=C_GREY).next_to(img, DOWN, buff=0.4)
        with self.say("imshow draws a two-dimensional array as an image, mapping each value to a color through a "
                      "colormap. Here a two-dimensional Gaussian bump. Always add a colorbar so readers can turn "
                      "colors back into numbers."):
            self.play(LaggedStart(*[FadeIn(s) for s in img], lag_ratio=0.002), run_time=2)
            self.play(FadeIn(bar), FadeIn(bl), FadeIn(code))
        self.clear()
