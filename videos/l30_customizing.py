from plots import *


class L30Customizing(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 30, "matplotlib-customizing", "Customizing and saving", "Matplotlib"

    def construct(self):
        self.intro("Lesson thirty: customizing and saving figures. Defaults get you a plot; a few targeted changes "
                   "get you a figure you'd put in a report.", r"styles, ticks, scales, style sheets, saving, pandas")
        self.styling()
        self.scales()
        self.layout()
        self.styles()
        self.saving()
        self.outro([r"Line style: \texttt{color}, \texttt{linewidth}, \texttt{linestyle}, \texttt{marker}.",
                    r"\texttt{set\_xticks}, \texttt{set\_xscale('log')}, \texttt{grid}, \texttt{sharey=True}.",
                    r"\texttt{plt.style.context(...)} and \texttt{rcParams} change the defaults.",
                    r"Save vectors (PDF, SVG) for documents, PNG at \texttt{dpi=200} for screens."],
                   "Style the lines, choose ticks and scales that suit the data, set defaults with style sheets, "
                   "save in the right format, and let pandas create the plot when your data is already a DataFrame.")

    def styling(self):
        h = self.heading("Styling lines and ticks")
        ax = mini_axes(w=6.0, h=3.6, x_range=(0, 10, 5), y_range=(0, 100, 25)).move_to(LEFT * 2.6 + DOWN * 0.4)
        plain = ax.plot(lambda x: x * x, x_range=[0.1, 10], color=GREY_B, stroke_width=2)
        styled = DashedVMobject(ax.plot(lambda x: x * x, x_range=[0.1, 10], color=C_BLUE, stroke_width=4), num_dashes=30)
        marks = VGroup(*[Dot(ax.c2p(x, x * x), radius=0.05, color=C_BLUE) for x in np.linspace(0.1, 10, 25)])
        grid = VGroup(*[DashedLine(ax.c2p(0, y), ax.c2p(10, y), color=GREY_D, stroke_width=1) for y in (25, 50, 75, 100)])
        ticks = VGroup(*[mono(t, 18, color=C_GOLD).next_to(ax.c2p(x, 0), DOWN, buff=0.15) for x, t in [(0, "start"), (5, "mid"), (10, "end")]])
        code = code_panel('ax.plot(x, x**2, color="tab:blue",\n        linewidth=2, linestyle="--",\n        marker="o", markersize=3)\n'
                          'ax.grid(alpha=0.3)\nax.set_xticks([0, 5, 10],\n              ["start", "mid", "end"])',
                          font_size=20).to_edge(RIGHT, buff=0.4)
        mk = Marker(code)
        with self.say("Every plot call accepts styling keywords: color, line width, line style and markers. A light "
                      "grid helps reading values, and set x ticks chooses where the ticks go and what they say."):
            self.play(Create(ax), Create(plain), FadeIn(code))
            self.play(mk.to(0, 2), ReplacementTransform(plain, styled), FadeIn(marks))
            self.play(mk.to(3), Create(grid))
            self.play(mk.to(4, 5), FadeIn(ticks))
        self.clear(keep=[h])
        self.h = h

    def scales(self):
        h = self.swap_heading(self.h, "Scales and shared axes")
        ax1 = mini_axes(w=5.0, h=3.2, x_range=(0, 10, 5), y_range=(0, 100, 50)).move_to(LEFT * 3.3 + DOWN * 0.3)
        ax2 = Axes(x_range=[-1, 1, 1], y_range=[0, 100, 50], x_length=5.0, y_length=3.2,
                   axis_config={"color": GREY_B, "stroke_width": 2, "include_tip": False, "tick_size": 0.04}).move_to(RIGHT * 3.3 + DOWN * 0.3)
        c1 = ax1.plot(lambda x: x * x, x_range=[0.1, 10], color=C_BLUE, stroke_width=3)
        c2 = ax2.plot(lambda u: (10 ** u) ** 2, x_range=[-1, 1], color=C_GOLD, stroke_width=3)
        lab2 = VGroup(*[mono(t, 18, color=GREY_B).next_to(ax2.c2p(u, 0), DOWN, buff=0.12) for u, t in [(-1, "0.1"), (0, "1"), (1, "10")]])
        t1 = mono("linear x", 22, color=C_BLUE).next_to(ax1, DOWN, buff=0.5)
        t2 = mono('ax2.set_xscale("log")', 22, color=C_GOLD).next_to(ax2, DOWN, buff=0.5)
        shared = Line(ax1.c2p(0, 100), ax2.c2p(-1, 100), color=C_YELLOW, stroke_width=2).set_opacity(0.6)
        sl = mono("sharey=True", 22, color=C_YELLOW).next_to(shared, UP, buff=0.1)
        with self.say("A log scale spreads out small values and compresses large ones, so the same data can look "
                      "completely different. With sharey, two panels use one y range, which makes side-by-side "
                      "comparisons honest."):
            self.play(Create(ax1), Create(ax2), FadeIn(t1), FadeIn(t2))
            self.play(Create(c1), Create(c2), FadeIn(lab2))
            self.play(Create(shared), FadeIn(sl))
        self.clear(keep=[h])
        self.h = h

    def styles(self):
        h = self.swap_heading(self.h, "Style sheets and defaults")
        code = code_panel('with plt.style.context("ggplot"):\n    fig, ax = plt.subplots()\n    ax.plot(x, np.sin(x))\n\n'
                          'plt.rcParams["font.size"] = 11', font_size=24).to_edge(LEFT, buff=0.5)

        def panel(bg, gridc, linec):
            r = Rectangle(width=4.6, height=3.0, stroke_width=0, fill_color=bg, fill_opacity=1)
            ax = mini_axes(w=3.8, h=2.2, x_range=(0, 10, 2), y_range=(-1, 1, 1)).move_to(r)
            gl = VGroup(*[Line(ax.c2p(0, y), ax.c2p(10, y), color=gridc, stroke_width=1.5) for y in (-1, 0, 1)])
            return VGroup(r, gl, ax, ax.plot(np.sin, x_range=[0, 10], color=linec, stroke_width=3))
        p1 = panel("#14161d", "#14161d", C_BLUE).move_to(RIGHT * 3.6 + UP * 0.5)
        p2 = panel("#e5e5e5", "#ffffff", "#E24A33").move_to(p1)
        p2[2].set_color(GREY_D)
        with self.say("Style sheets change many defaults at once: colors, grid, fonts. Use one temporarily with a "
                      "with block, or globally with plt dot style dot use. Individual defaults live in the rc params "
                      "dictionary."):
            self.play(FadeIn(code), FadeIn(p1))
            self.play(ReplacementTransform(p1, p2), run_time=1.5)
            lab = mono('"ggplot"', 24, color=C_YELLOW).next_to(p2, DOWN, buff=0.3)
            self.play(FadeIn(lab))
        self.clear(keep=[h])
        self.h = h

    def layout(self):
        h = self.swap_heading(self.h, "Figure size and layout")
        code = code_panel('fig, axs = plt.subplots(1, 2, figsize=(8, 3),\n                        layout="constrained")\n'
                          'fig.suptitle("Two panels")', font_size=24).to_edge(UP, buff=1.0)

        def fig(w, hgt, tight):
            r = Rectangle(width=w, height=hgt, stroke_color=C_FIG, stroke_width=2, fill_color="#14161d", fill_opacity=1)
            pad = 0.35 if tight else 0.05
            aw = (w - 3 * pad - (0.4 if tight else 0)) / 2
            axs = VGroup(*[Rectangle(width=aw, height=hgt - 2 * pad - (0.35 if tight else 0), stroke_color=C_AX, stroke_width=2)
                           for _ in range(2)]).arrange(RIGHT, buff=pad + (0.4 if tight else 0))
            axs.move_to(r).shift(DOWN * (0.15 if tight else 0))
            labs = VGroup(*[mono("y label", 16, color=GREY_B).rotate(PI / 2).next_to(a, LEFT, buff=0.08) for a in axs])
            return VGroup(r, axs, labs)
        f1 = fig(4.0, 3.0, False).move_to(DOWN * 1.0)
        f2 = fig(8.0, 3.0, True).move_to(DOWN * 1.0)
        title = mono("Two panels", 20, weight=BOLD).next_to(f2[0].get_top(), DOWN, buff=0.12)
        with self.say("figsize sets the canvas size in inches, which also fixes the aspect ratio. Without help, "
                      "labels can collide or get clipped; layout constrained makes room for titles, labels and "
                      "colorbars automatically. suptitle puts one title over the whole figure."):
            self.play(FadeIn(code), FadeIn(f1))
            self.play(Circumscribe(f1[2][1], color=C_BAD))
            self.play(ReplacementTransform(f1, f2), run_time=1.5)
            self.play(FadeIn(title))
        self.clear(keep=[h])
        self.h = h

    def saving(self):
        h = self.swap_heading(self.h, "Saving, and plotting from pandas")
        rows = [["format", "kind", "use for"], ["PDF / SVG", "vector", "papers, slides"], ["PNG", "raster", "web, screens"]]
        t = table_grid(rows, [2.2, 1.6, 2.6], row_h=0.6, size=24).move_to(LEFT * 3.0 + UP * 0.6)
        code = mono('fig.savefig("plot.png", dpi=200,\n            bbox_inches="tight")', 22, color=C_YELLOW).next_to(t, DOWN, buff=0.5)
        with self.say("savefig picks the format from the file name. Vector formats like PDF and SVG stay sharp at "
                      "any zoom; PNG is pixels, so raise the d p i. bbox inches tight trims extra white space."):
            self.play(FadeIn(t))
            self.play(FadeIn(code))
        ax = mini_axes(w=4.6, h=3.0, x_range=(0, 3, 1), y_range=(0, 150, 50)).move_to(RIGHT * 3.6 + DOWN * 0.2)
        vals = [(120, 80), (95, 70), (140, 90)]
        bars = VGroup()
        for k, (s, c) in enumerate(vals):
            for j, (v, col) in enumerate([(s, C_BLUE), (c, C_GOLD)]):
                b = Rectangle(width=0.3, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=col, fill_opacity=0.85)
                bars.add(b.move_to(ax.c2p(k + 0.5 + (j - 0.5) * 0.32, 0), aligned_edge=DOWN))
        ml = VGroup(*[mono(m, 18, color=GREY_B).next_to(ax.c2p(k + 0.5, 0), DOWN, buff=0.1) for k, m in enumerate(["Jan", "Feb", "Mar"])])
        pc = mono('df.plot(x="month", y=["sales", "costs"],\n        kind="bar")', 20, color=C_GREY).next_to(ax, UP, buff=0.3)
        with self.say("And when your data is already in a DataFrame, its plot method builds the Matplotlib chart for "
                      "you, with labels and a legend, and returns the Axes for further tweaks."):
            self.play(FadeIn(pc), Create(ax), FadeIn(ml))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15))
        self.clear()
