"""Shared pieces for the Matplotlib lessons."""
from lesson import *

C_FIG = GREY_B
C_AX = C_BLUE
C_ART = C_GOLD          # artists
CITY_COL = {"Tehran": C_GOLD, "Berlin": C_TEAL, "Tokyo": C_PURPLE}


def tag(text, color, size=20) -> VGroup:
    t = mono(text, size, color=BLACK, weight=BOLD)
    r = RoundedRectangle(corner_radius=0.06, width=t.width + 0.25, height=t.height + 0.18, stroke_width=0,
                         fill_color=color, fill_opacity=1)
    return VGroup(r, t.move_to(r))


def mini_axes(w=2.9, h=1.45, x_range=(0, 10, 2), y_range=(-1, 1, 1)) -> Axes:
    return Axes(x_range=list(x_range), y_range=list(y_range), x_length=w, y_length=h,
                axis_config={"color": GREY_B, "stroke_width": 2, "include_tip": False, "tick_size": 0.04})


def bars_on(ax: Axes, values, color, width=0.5, x0=0.5) -> VGroup:
    out = VGroup()
    for k, v in enumerate(values):
        b = Rectangle(width=width, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.001), stroke_width=0,
                      fill_color=color, fill_opacity=0.85)
        out.add(b.move_to(ax.c2p(k + x0, 0), aligned_edge=DOWN))
    return out


def hist_on(ax: Axes, samples, bins, rng_, color) -> VGroup:
    counts, edges = np.histogram(samples, bins=bins, range=rng_)
    out = VGroup()
    for cnt, e0, e1 in zip(counts, edges[:-1], edges[1:]):
        if cnt == 0:
            continue
        p0, p1 = ax.c2p(e0, 0), ax.c2p(e1, cnt)
        out.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_color=BG, stroke_width=1,
                          fill_color=color, fill_opacity=0.9).move_to(p0, aligned_edge=DL))
    return out
