"""Video 4 - Matplotlib: anatomy of a figure, plot types, and the full pipeline.
Render: manim -qh v4_matplotlib.py MatplotlibAnatomy"""
from manim import *
from common import *

C_FIG = GREY_B
C_AX = C_BLUE
C_ART = C_GOLD          # artists
CITY_COL = {"Tehran": C_GOLD, "Berlin": C_TEAL, "Tokyo": C_PURPLE}

SRC = '''
x = np.linspace(0, 10, 200)
fig, ax = plt.subplots()
ax.plot(x, np.exp(-x/3) * np.sin(2*x),
        label="damped")
ax.plot(x, np.exp(-x/3), "--",
        label="envelope")
ax.set(xlabel="time [s]",
       ylabel="amplitude",
       title="Damped oscillation")
ax.annotate("peak", xy=(0.7, 0.78),
            xytext=(2.8, 0.85))
ax.legend()
fig.savefig("damped.pdf")
'''


def tag(text, color, size=20):
    t = mono(text, size, color=BLACK, weight=BOLD)
    r = RoundedRectangle(corner_radius=0.06, width=t.width + 0.25, height=t.height + 0.18,
                         stroke_width=0, fill_color=color, fill_opacity=1)
    return VGroup(r, t.move_to(r))


def mini_axes(w=2.9, h=1.45, x_range=(0, 10, 2), y_range=(-1, 1, 1)):
    return Axes(x_range=list(x_range), y_range=list(y_range), x_length=w, y_length=h,
                axis_config={"color": GREY_B, "stroke_width": 2, "include_tip": False,
                             "tick_size": 0.04})


class MatplotlibAnatomy(Scene):
    def construct(self):
        title_card(self, "Anatomy of a figure",
                   r"Python for Programmers \textperiodcentered{} Part 4: Matplotlib")
        self.anatomy()
        self.plot_types()
        self.pipeline()
        end_card(self, [
            r"\textbf{Figure} = the canvas, \textbf{Axes} = one plot, \textbf{Artists} = everything drawn.",
            r"Use the explicit interface: \texttt{fig, ax = plt.subplots()}, then \texttt{ax.*} calls.",
            r"\texttt{plot}, \texttt{scatter}, \texttt{bar}, \texttt{hist}: same Axes, different artists.",
            r"NumPy makes the data, pandas shapes it, Matplotlib draws it.",
        ])

    # ------------------------------------------------------------------ 1
    def anatomy(self):
        self.next_section("anatomy")
        head = chapter(self, "Figure, Axes, Artists")
        code = code_panel(SRC, font_size=20).to_edge(LEFT, buff=0.35).shift(DOWN * 0.3)
        self.play(FadeIn(code))
        mk = line_marker(code, 0)
        self.play(FadeIn(mk))
        self.wait(0.4)

        # line 1: Figure + Axes
        self.play(Transform(mk, line_marker(code, 1)))
        fig_rect = Rectangle(width=6.6, height=5.6, stroke_color=C_FIG, stroke_width=2,
                             fill_color="#14161d", fill_opacity=1).move_to(RIGHT * 3.5 + DOWN * 0.3)
        fig_tag = tag("Figure", C_FIG).next_to(fig_rect, UP, buff=0.08, aligned_edge=LEFT)
        self.play(FadeIn(fig_rect), FadeIn(fig_tag))
        ax = Axes(x_range=[0, 10, 2], y_range=[-0.6, 1.0, 0.5], x_length=5.0, y_length=3.4,
                  axis_config={"color": GREY_B, "stroke_width": 2, "include_tip": False,
                               "include_numbers": True, "font_size": 18, "decimal_number_config": {"num_decimal_places": 1}},
                  x_axis_config={"decimal_number_config": {"num_decimal_places": 0}})
        ax.move_to(fig_rect.get_center() + RIGHT * 0.25 + DOWN * 0.1)
        ax_box = SurroundingRectangle(ax, color=C_AX, buff=0.12, stroke_width=2)
        ax_tag = tag("Axes", C_AX).next_to(ax_box, UP, buff=0.06, aligned_edge=RIGHT)
        self.play(Create(ax), Create(ax_box), FadeIn(ax_tag), run_time=1.5)
        self.wait(0.4)

        # lines 2-3: damped curve
        self.play(Transform(mk, line_marker(code, 2, j=3)))
        f = lambda x: np.exp(-x / 3) * np.sin(2 * x)
        damped = ax.plot(f, x_range=[0, 10, 0.05], color=C_BLUE, stroke_width=3)
        self.play(Create(damped), run_time=2)
        # lines 4-5: envelope
        self.play(Transform(mk, line_marker(code, 4, j=5)))
        env = DashedVMobject(ax.plot(lambda x: np.exp(-x / 3), x_range=[0, 10, 0.05]),
                             num_dashes=40).set_color(C_GOLD).set_stroke(width=3)
        self.play(Create(env), run_time=1.5)
        # lines 6-8: labels and title
        self.play(Transform(mk, line_marker(code, 6, j=8)))
        xl = Text("time [s]", font_size=18).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = Text("amplitude", font_size=18).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.45)
        tt = Text("Damped oscillation", font_size=22, weight=BOLD).next_to(ax, UP, buff=0.3)
        self.play(Write(xl), Write(yl), Write(tt))
        # lines 9-10: annotation
        self.play(Transform(mk, line_marker(code, 9, j=10)))
        peak_t = Text("peak", font_size=18).move_to(ax.c2p(2.8, 0.85), aligned_edge=LEFT)
        peak_a = Arrow(peak_t.get_left(), ax.c2p(0.75, 0.78), buff=0.08, stroke_width=2.5,
                       color=WHITE, max_tip_length_to_length_ratio=0.15)
        self.play(FadeIn(peak_t), GrowArrow(peak_a))
        # line 11: legend
        self.play(Transform(mk, line_marker(code, 11)))
        leg_items = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.45, color=C_BLUE, stroke_width=3), Text("damped", font_size=15)).arrange(RIGHT, buff=0.12),
            VGroup(DashedLine(ORIGIN, RIGHT * 0.45, color=C_GOLD, stroke_width=3, dash_length=0.08),
                   Text("envelope", font_size=15)).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        leg_box = SurroundingRectangle(leg_items, color=GREY_C, buff=0.1, stroke_width=1.5,
                                       fill_color="#14161d", fill_opacity=0.9, corner_radius=0.05)
        legend = VGroup(leg_box, leg_items).move_to(ax.c2p(8.0, 0.75))
        self.play(FadeIn(legend))
        # line 12: save
        self.play(Transform(mk, line_marker(code, 12)))
        saved = Tex(r"$\rightarrow$ \texttt{damped.pdf}", font_size=26, color=C_GREEN)
        saved.next_to(fig_rect, DOWN, buff=0.1, aligned_edge=RIGHT)
        self.play(FadeIn(saved, shift=0.2 * RIGHT))
        self.wait(0.8)

        # everything drawn is an Artist
        self.play(FadeOut(mk), FadeOut(saved))
        arts = [(damped, "Line2D", ax.c2p(5.3, 0.4), UP),
                (tt, "Text", tt.get_left(), LEFT),
                (legend, "Legend", legend.get_bottom(), DOWN),
                (peak_t, "Annotation", peak_t.get_bottom(), DOWN),
                (ax.x_axis, "XAxis", ax.c2p(8.6, -0.6), DOWN)]
        tags = VGroup()
        for mob, name, p, d in arts:
            tg = tag(name, C_ART, size=16).next_to(p, d, buff=0.08)
            tags.add(tg)
        self.play(LaggedStart(*[FadeIn(tg, scale=0.6) for tg in tags], lag_ratio=0.2),
                  LaggedStart(*[Indicate(m, color=C_ART, scale_factor=1.05) for m, *_ in arts], lag_ratio=0.2),
                  run_time=2.5)
        cap = caption(r"Everything you see is an \emph{Artist}, owned by an Axes, owned by the Figure")
        self.play(FadeIn(cap))
        self.wait(3)
        fade_out_all(self)

    # ------------------------------------------------------------------ 2
    def plot_types(self):
        self.next_section("plot-types")
        head = chapter(self, "Four Axes, four kinds of plot")
        code = code_panel('fig, axs = plt.subplots(2, 2, layout="constrained")', font_size=20)
        code.to_edge(UP, buff=0.85)
        self.play(FadeIn(code))
        panels = VGroup(*[Rectangle(width=5.6, height=2.5, stroke_color=GREY_D, stroke_width=1.5)
                          for _ in range(4)]).arrange_in_grid(2, 2, buff=(0.4, 0.25))
        panels.next_to(code, DOWN, buff=0.3)
        idx = ["axs[0, 0]", "axs[0, 1]", "axs[1, 0]", "axs[1, 1]"]
        idx_t = VGroup(*[mono(s, 15, color=C_AX).next_to(p.get_corner(UL), DR, buff=0.08) for s, p in zip(idx, panels)])
        self.play(LaggedStart(*[Create(p) for p in panels], lag_ratio=0.2), FadeIn(idx_t))

        def place(axes, p):
            return axes.move_to(p.get_center() + UP * 0.1 + RIGHT * 0.1)

        rng = np.random.default_rng(42)
        # line
        a1 = place(mini_axes(x_range=(0, 10, 2), y_range=(-1, 1, 1)), panels[0])
        l_sin = a1.plot(np.sin, x_range=[0, 10, 0.05], color=C_BLUE, stroke_width=3)
        l_cos = a1.plot(np.cos, x_range=[0, 10, 0.05], color=C_GOLD, stroke_width=3)
        c1 = mono("ax.plot(x, np.sin(x))", 15, color=C_GREY)
        # scatter
        a2 = place(mini_axes(x_range=(-3, 3, 1), y_range=(-3, 3, 1)), panels[1])
        xs = rng.normal(size=120); ys = 0.6 * xs + rng.normal(scale=0.6, size=120)
        pts = VGroup(*[Dot(a2.c2p(x, y), radius=0.035, color=C_TEAL, fill_opacity=0.75)
                       for x, y in zip(xs, ys) if abs(x) < 3 and abs(y) < 3])
        c2 = mono("ax.scatter(xs, ys)", 15, color=C_GREY)
        # bar
        a3 = place(mini_axes(x_range=(0, 4, 1), y_range=(0, 45, 15)), panels[2])
        vals = [42, 27, 31, 18]
        bars = VGroup()
        for k, v in enumerate(vals):
            b = Rectangle(width=0.5, height=a3.c2p(0, v)[1] - a3.c2p(0, 0)[1], stroke_width=0,
                          fill_color=C_GREEN, fill_opacity=0.85)
            b.move_to(a3.c2p(k + 0.5, 0), aligned_edge=DOWN)
            bars.add(b)
        blabels = VGroup(*[mono(s, 14, color=GREY_B).next_to(a3.c2p(k + 0.5, 0), DOWN, buff=0.08)
                           for k, s in enumerate("ABCD")])
        c3 = mono('ax.bar(["A","B","C","D"], vals)', 15, color=C_GREY)
        # hist
        a4 = place(mini_axes(x_range=(-4, 4, 2), y_range=(0, 120, 40)), panels[3])
        samples = rng.normal(size=1000)
        counts, edges = np.histogram(samples, bins=30, range=(-4, 4))
        hist = VGroup()
        for cnt, e0, e1 in zip(counts, edges[:-1], edges[1:]):
            if cnt == 0:
                continue
            p0, p1 = a4.c2p(e0, 0), a4.c2p(e1, cnt)
            hist.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_color=BG,
                               stroke_width=1, fill_color=C_PURPLE, fill_opacity=0.9).move_to(p0, aligned_edge=DL))
        c4 = mono("ax.hist(samples, bins=30)", 15, color=C_GREY)

        titles = ["Line", "Scatter", "Bar", "Histogram"]
        for c, p in zip([c1, c2, c3, c4], panels):
            c.next_to(p.get_bottom(), UP, buff=0.07)
        for k, (axes, draw, c) in enumerate([
            (a1, [Create(l_sin), Create(l_cos)], c1),
            (a2, [LaggedStart(*[FadeIn(d, scale=0.3) for d in pts], lag_ratio=0.01)], c2),
            (a3, [LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), FadeIn(blabels)], c3),
            (a4, [LaggedStart(*[GrowFromEdge(b, DOWN) for b in hist], lag_ratio=0.04)], c4),
        ]):
            tt = Tex(rf"\textbf{{{titles[k]}}}", font_size=26).next_to(panels[k].get_top(), DOWN, buff=0.08)
            self.play(Create(axes), FadeIn(c), FadeIn(tt), run_time=0.8)
            self.play(*draw, run_time=1.6)
        self.wait(1)
        cap = caption(r"Each panel is its own Axes object: \texttt{for ax in axs.flat: ...}")
        self.play(FadeIn(cap))
        self.wait(2.5)
        fade_out_all(self)

    # ------------------------------------------------------------------ 3
    def pipeline(self):
        self.next_section("pipeline")
        head = chapter(self, r"NumPy $\rightarrow$ pandas $\rightarrow$ Matplotlib")
        # same synthetic data as the slides (numpy only, to avoid a pandas dependency here)
        rng = np.random.default_rng(42)
        cities = ["Tehran", "Berlin", "Tokyo"]
        n = 365
        city = rng.choice(cities, size=n)
        sales = rng.normal(100, 20, size=n).round(1)
        month = np.repeat(np.arange(12), [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
        order = ["Berlin", "Tehran", "Tokyo"]  # unstack sorts column labels
        monthly = np.array([[sales[(month == m) & (city == c)].sum() for c in order] for m in range(12)])

        zone_x = [-4.9, -0.6, 3.9]
        titles = VGroup(
            Tex(r"\textbf{NumPy}: 365 raw rows", font_size=28),
            Tex(r"\textbf{pandas}: $12 \times 3$ table", font_size=28),
            Tex(r"\textbf{Matplotlib}: 3 lines", font_size=28),
        )
        for t, x in zip(titles, zone_x):
            t.move_to([x, 2.55, 0])

        # zone 1: one tiny square per day, coloured by city
        cols, sq = 19, 0.17
        days = VGroup(*[Square(sq, stroke_width=0, fill_color=CITY_COL[c], fill_opacity=0.9) for c in city])
        days.arrange_in_grid(rows=int(np.ceil(n / cols)), cols=cols, buff=0.025)
        days.move_to([zone_x[0], -0.45, 0])
        code1 = mono("rng.normal(100, 20, size=365)", 15, color=C_GREY).next_to(days, DOWN, buff=0.25)
        self.play(Write(titles[0]))
        self.play(LaggedStart(*[FadeIn(d) for d in days], lag_ratio=0.004), FadeIn(code1), run_time=2)
        legend = VGroup(*[VGroup(Square(0.18, stroke_width=0, fill_color=CITY_COL[c], fill_opacity=1),
                                 Text(c, font_size=16)).arrange(RIGHT, buff=0.1) for c in order])
        legend.arrange(RIGHT, buff=0.35).next_to(titles[0], DOWN, buff=0.2)
        self.play(FadeIn(legend))
        self.wait(0.5)

        # zone 2: the monthly table
        mnames = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
        rows = [tuple(order)] + [tuple(f"{v:.0f}" for v in monthly[m]) for m in range(12)]
        table = table_grid(rows, [0.95, 0.95, 0.95], row_h=0.34, size=15, index=mnames, index_w=0.6)
        table.move_to([zone_x[1], -0.55, 0])
        for k, c in enumerate(order):
            table[0][k + 1][1].set_color(CITY_COL[c])
        code2 = mono('groupby([month, "city"]).sum().unstack()', 14, color=C_GREY)
        code2.next_to(table, DOWN, buff=0.15)
        self.play(Write(titles[1]), FadeIn(table[0]), FadeIn(code2))
        anims = []
        for m in range(12):
            for k, c in enumerate(order):
                sel = [d for d, mm, cc in zip(days, month, city) if mm == m and cc == c]
                anims.append(ReplacementTransform(VGroup(*sel), table[m + 1][k + 1]))
            anims.append(FadeIn(table[m + 1][0]))
        self.play(LaggedStart(*anims, lag_ratio=0.02), run_time=4)
        self.wait(0.6)

        # zone 3: lines
        ax = Axes(x_range=[0, 11, 1], y_range=[400, 1600, 400], x_length=4.3, y_length=3.6,
                  axis_config={"color": GREY_B, "stroke_width": 2, "include_tip": False, "tick_size": 0.04},
                  y_axis_config={"include_numbers": True, "font_size": 16})
        ax.move_to([zone_x[2] + 0.2, -0.5, 0])
        mlab = VGroup(*[Text(mnames[m][0], font_size=13, color=GREY_B).next_to(ax.c2p(m, 400), DOWN, buff=0.1)
                        for m in range(12)])
        self.play(Write(titles[2]), Create(ax), FadeIn(mlab))
        for k, c in enumerate(order):
            colcells = VGroup(*[table[m + 1][k + 1] for m in range(12)])
            pts = [ax.c2p(m, monthly[m, k]) for m in range(12)]
            line = VMobject(color=CITY_COL[c], stroke_width=3).set_points_as_corners(pts)
            dots = VGroup(*[Dot(p, radius=0.045, color=CITY_COL[c]) for p in pts])
            self.play(Circumscribe(colcells, color=CITY_COL[c], buff=0.03), run_time=0.8)
            self.play(TransformFromCopy(VGroup(*[c_[1] for c_ in colcells]), dots), run_time=1.2)
            self.play(Create(line), run_time=1)
        code3 = mono('monthly.plot(marker="o")', 15, color=C_GREY).next_to(ax, DOWN, buff=0.45)
        self.play(FadeIn(code3))
        cap = caption(r"365 rows $\rightarrow$ one chain of pandas calls $\rightarrow$ one plot call")
        self.play(FadeIn(cap))
        self.wait(3)
        fade_out_all(self)
