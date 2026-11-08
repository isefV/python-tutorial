from plots import *

SRC = '''x = np.linspace(0, 10, 200)
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
fig.savefig("damped.pdf")'''


class L28MatplotlibBasics(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 28, "matplotlib-basics", "The Matplotlib object model", "Matplotlib"

    def construct(self):
        self.intro("Lesson twenty-eight starts Matplotlib, Python's standard plotting library. Once you understand "
                   "its three objects, figure, axes and artists, the huge API becomes predictable.",
                   r"Figure, Axes, Artists; explicit vs.\ \texttt{pyplot} interface")
        self.anatomy()
        self.interfaces()
        self.outro([r"\textbf{Figure} = the canvas, \textbf{Axes} = one plot, \textbf{Artists} = everything drawn.",
                    r"Prefer the explicit interface: \texttt{fig, ax = plt.subplots()}, then \texttt{ax.*}.",
                    r"\texttt{plt.plot(...)} is fine for a quick look in a notebook.",
                    r"Plot calls return artists you can restyle later."],
                   "A figure holds axes, axes hold artists, and every call on ax adds or changes an artist. Use "
                   "the explicit interface for anything you'll keep.")

    def anatomy(self):
        h = self.heading("Figure, Axes, Artists")
        code = code_panel(SRC, font_size=20).to_edge(LEFT, buff=0.35).shift(DOWN * 0.3)
        mk = Marker(code)
        fig_rect = Rectangle(width=6.6, height=5.6, stroke_color=C_FIG, stroke_width=2, fill_color="#14161d",
                             fill_opacity=1).move_to(RIGHT * 3.5 + DOWN * 0.3)
        fig_tag = tag("Figure", C_FIG).next_to(fig_rect, UP, buff=0.08, aligned_edge=LEFT)
        ax = Axes(x_range=[0, 10, 2], y_range=[-0.6, 1.0, 0.5], x_length=5.0, y_length=3.4,
                  axis_config={"color": GREY_B, "stroke_width": 2, "include_tip": False, "include_numbers": True,
                               "font_size": 18, "decimal_number_config": {"num_decimal_places": 1}},
                  x_axis_config={"decimal_number_config": {"num_decimal_places": 0}})
        ax.move_to(fig_rect.get_center() + RIGHT * 0.25 + DOWN * 0.1)
        ax_box = SurroundingRectangle(ax, color=C_AX, buff=0.12, stroke_width=2)
        ax_tag = tag("Axes", C_AX).next_to(ax_box, UP, buff=0.06, aligned_edge=RIGHT)
        with self.say("plt dot subplots creates two objects. The Figure is the whole canvas, the thing you save to a "
                      "file. The Axes is one plot inside it, with its own coordinate system, ticks and labels."):
            self.play(FadeIn(code), mk.to(0))
            self.play(mk.to(1), FadeIn(fig_rect), FadeIn(fig_tag))
            self.play(Create(ax), Create(ax_box), FadeIn(ax_tag), run_time=1.5)
        f = lambda x: np.exp(-x / 3) * np.sin(2 * x)
        damped = ax.plot(f, x_range=[0, 10, 0.05], color=C_BLUE, stroke_width=3)
        env = DashedVMobject(ax.plot(lambda x: np.exp(-x / 3), x_range=[0, 10, 0.05]), num_dashes=40).set_color(C_GOLD).set_stroke(width=3)
        xl = Text("time [s]", font_size=18).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = Text("amplitude", font_size=18).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.45)
        tt = Text("Damped oscillation", font_size=22, weight=BOLD).next_to(ax, UP, buff=0.3)
        with self.say("Then every call on ax adds something. plot draws a line from the x and y arrays; a format "
                      "string like dash dash makes it dashed. set adds the axis labels and the title in one call."):
            self.play(mk.to(2, 3))
            self.play(Create(damped), run_time=1.5)
            self.play(mk.to(4, 5))
            self.play(Create(env), run_time=1.2)
            self.play(mk.to(6, 8))
            self.play(Write(xl), Write(yl), Write(tt))
        peak_t = Text("peak", font_size=18).move_to(ax.c2p(2.8, 0.85), aligned_edge=LEFT)
        peak_a = Arrow(peak_t.get_left(), ax.c2p(0.75, 0.78), buff=0.08, stroke_width=2.5, color=WHITE,
                       max_tip_length_to_length_ratio=0.15)
        leg_items = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.45, color=C_BLUE, stroke_width=3), Text("damped", font_size=15)).arrange(RIGHT, buff=0.12),
                           VGroup(DashedLine(ORIGIN, RIGHT * 0.45, color=C_GOLD, stroke_width=3, dash_length=0.08),
                                  Text("envelope", font_size=15)).arrange(RIGHT, buff=0.12)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        leg_box = SurroundingRectangle(leg_items, color=GREY_C, buff=0.1, stroke_width=1.5, fill_color="#14161d",
                                       fill_opacity=0.9, corner_radius=0.05)
        legend = VGroup(leg_box, leg_items).move_to(ax.c2p(8.0, 0.75))
        with self.say("annotate places text with an arrow pointing at a data coordinate. legend collects the labels "
                      "you passed to plot. And fig dot savefig writes the figure; the file extension picks the format."):
            self.play(mk.to(9, 10))
            self.play(FadeIn(peak_t), GrowArrow(peak_a))
            self.play(mk.to(11))
            self.play(FadeIn(legend))
            self.play(mk.to(12))
            saved = tex(r"$\rightarrow$ \texttt{damped.pdf}", 28, C_GREEN).next_to(fig_rect, DOWN, buff=0.1, aligned_edge=RIGHT)
            self.play(FadeIn(saved, shift=0.2 * RIGHT))
        arts = [(damped, "Line2D", ax.c2p(5.3, 0.4), UP), (tt, "Text", tt.get_left(), LEFT),
                (legend, "Legend", legend.get_bottom(), DOWN), (peak_t, "Annotation", peak_t.get_bottom(), DOWN),
                (ax.x_axis, "XAxis", ax.c2p(8.6, -0.6), DOWN)]
        with self.say("Everything you see is an Artist: lines, text, the legend, even the axis itself. Artists are "
                      "owned by an Axes, and the Axes is owned by the Figure. That hierarchy is the whole model."):
            self.play(FadeOut(mk.mob), FadeOut(saved))
            tags = VGroup(*[tag(name, C_ART, size=16).next_to(p, d, buff=0.08) for _, name, p, d in arts])
            self.play(LaggedStart(*[FadeIn(tg, scale=0.6) for tg in tags], lag_ratio=0.2),
                      LaggedStart(*[Indicate(m, color=C_ART, scale_factor=1.05) for m, *_ in arts], lag_ratio=0.2), run_time=2.5)
        self.clear(keep=[h])
        self.h = h

    def interfaces(self):
        h = self.swap_heading(self.h, "Two interfaces")
        imp = code_panel('plt.plot(x, np.sin(x))\nplt.title("Quick look")\nplt.show()', font_size=26)
        exp = code_panel('fig, ax = plt.subplots()\nax.plot(x, np.sin(x))\nax.set_title("Report")\nfig.savefig("sin.png")', font_size=26)
        il = tex(r"implicit \texttt{pyplot}: acts on the \emph{current} Axes", 30, C_GREY)
        el = tex(r"explicit: you hold the objects", 30, C_GREEN)
        left = VGroup(il, imp).arrange(DOWN, buff=0.3)
        right = VGroup(el, exp).arrange(DOWN, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to(UP * 0.6)
        with self.say("There are two ways to drive Matplotlib. The pyplot functions act on an invisible current axes, "
                      "which is handy for a quick look. The explicit style keeps the figure and axes in variables, "
                      "so it stays clear with several plots, functions and saved files. Prefer it."):
            self.play(FadeIn(left))
            self.play(FadeIn(right))
            self.play(Circumscribe(exp, color=C_GREEN))
        with self.say("Plot calls also return their artists. Keep them, and you can restyle a line or a single "
                      "bar after the fact."):
            a = mono('lines = ax1.plot([1, 3, 2]);  lines[0].set_color("tab:orange")', 22, color=C_YELLOW)
            b = mono('bars = ax2.bar(["a", "b", "c"], [3, 1, 2]);  bars[1].set_color("tab:green")', 22, color=C_YELLOW)
            VGroup(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.7)
            self.play(FadeIn(a), FadeIn(b))
        self.clear()
