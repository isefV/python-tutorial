"""Narrated-lesson framework: one ~2 minute Scene per tutorial lesson.

Every beat of a lesson is wrapped in ``with self.say("..."):``. The block's
animations play, then the scene waits until the beat has lasted at least as long
as its narration takes to speak (WPM words per minute). When the scene finishes,
the narration is written to ``narration/<NN>-<slug>.txt`` with a timestamp per
beat, so the script always matches the rendered video.
"""
import re
from contextlib import contextmanager
from pathlib import Path

from manim import *
from common import *

HERE = Path(__file__).resolve().parent
NARRATION_DIR = HERE / "narration"
WPM = 150                      # speaking pace used to time every beat

CATEGORY_COLOR = {"Python": C_BLUE, "NumPy": C_TEAL, "pandas": C_PURPLE, "Matplotlib": C_GOLD}


def fmt_t(t: float) -> str:
    m, s = divmod(int(round(t)), 60)
    return f"{m:02d}:{s:02d}"


class Marker:
    """Tinted bar that walks over the lines of a Code panel.
    ``mk.to(i, j)`` returns an animation (FadeIn the first time, Transform after)."""

    def __init__(self, code: Code, color=C_YELLOW):
        self.code, self.color, self.mob = code, color, None

    def to(self, i: int, j: int | None = None, color=None):
        new = line_marker(self.code, i, color=color or self.color, j=j)
        if self.mob is None:
            self.mob = new
            return FadeIn(new)
        return Transform(self.mob, new)


class Console(VGroup):
    """A small terminal panel; ``scene.play(console.print("text"))`` appends a line."""

    def __init__(self, width=5.6, height=3.0, title="output", font_size=24):
        super().__init__()
        self.font_size = font_size
        self.bg = RoundedRectangle(corner_radius=0.1, width=width, height=height,
                                   fill_color="#0a0b0f", fill_opacity=1,
                                   stroke_color=GREY_D, stroke_width=1.5)
        self.head = mono(title, 16, color=C_GREY).move_to(self.bg.get_corner(UL) + [0.2, -0.22, 0],
                                                          aligned_edge=UL)
        self.rows = VGroup()
        self.add(self.bg, self.head, self.rows)

    def print(self, text: str, color=WHITE, size=None, run_time=0.6):
        t = mono(text, size or self.font_size, color=color)
        if len(self.rows):
            t.next_to(self.rows[-1], DOWN, buff=0.16, aligned_edge=LEFT)
        else:
            t.next_to(self.head, DOWN, buff=0.22, aligned_edge=LEFT)
        self.rows.add(t)
        return FadeIn(t, shift=0.15 * UP, run_time=run_time)

    def clear(self):
        anim = FadeOut(self.rows.copy())
        old = list(self.rows)
        self.rows.remove(*old)
        return anim, old


class Lesson(Scene):
    NUM = 0
    SLUG = ""
    TITLE = ""
    CATEGORY = "Python"

    def setup(self):
        self._beats: list[tuple[float, str]] = []

    # ------------------------------------------------------------ narration
    @contextmanager
    def say(self, text: str, gap: float = 0.6):
        text = " ".join(text.split())
        t0 = self.renderer.time
        yield
        need = len(text.split()) * 60 / WPM + gap
        spent = self.renderer.time - t0
        if need - spent > 1 / 30:
            self.wait(need - spent)
        self._beats.append((t0, text))

    def tear_down(self):
        if not self._beats:
            return
        NARRATION_DIR.mkdir(exist_ok=True)
        total = self.renderer.time
        words = sum(len(t.split()) for _, t in self._beats)
        name = f"{self.NUM:02d}-{self.SLUG}"
        head = [f"Lesson {self.NUM:02d} - {self.TITLE}",
                f"Category: {self.CATEGORY}",
                f"Video: {name}.mp4   Length: {fmt_t(total)}   Narration: {words} words at ~{WPM} wpm",
                "Each paragraph starts at the timestamp shown; the picture waits for the voice.",
                ""]
        body = [f"[{fmt_t(t)}] {text}\n" for t, text in self._beats]
        (NARRATION_DIR / f"{name}.txt").write_text("\n".join(head + body), encoding="utf-8")

    # ------------------------------------------------------------ bookends
    def intro(self, narration: str, subtitle: str | None = None):
        col = CATEGORY_COLOR[self.CATEGORY]
        with self.say(narration):
            kicker = Tex(rf"Lesson {self.NUM:02d} \textperiodcentered{{}} {self.CATEGORY}",
                         font_size=32, color=col)
            title = Tex(rf"\textbf{{{self.TITLE}}}", font_size=62)
            line = Underline(title, color=col, buff=0.15)
            g = VGroup(kicker, title, line)
            kicker.next_to(title, UP, buff=0.45)
            if subtitle:
                g.add(Tex(subtitle, font_size=32, color=C_GREY).next_to(line, DOWN, buff=0.4))
            self.play(FadeIn(kicker, shift=0.2 * DOWN), Write(title), run_time=1.5)
            self.play(*[FadeIn(m, shift=0.2 * UP) for m in g[2:]])
        self.play(FadeOut(g, shift=UP))

    def outro(self, lines: list[str], narration: str):
        with self.say(narration, gap=1.5):
            head = Tex(r"\textbf{Take-aways}", font_size=46, color=C_YELLOW)
            items = VGroup(*[Tex(rf"$\blacktriangleright$\ \ {l}", font_size=32) for l in lines])
            items.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
            VGroup(head, items).arrange(DOWN, buff=0.55)
            if items.width > 13:
                items.scale_to_fit_width(13)
            self.play(Write(head))
            self.play(LaggedStart(*[FadeIn(i, shift=0.3 * RIGHT) for i in items], lag_ratio=0.5),
                      run_time=2.5)
        fade_out_all(self)

    # ------------------------------------------------------------ small helpers
    def heading(self, text: str) -> Tex:
        """Write a section heading straight into the top-left corner."""
        text = re.sub(r"(?<!\\)_", r"\\_", text)
        h = Tex(rf"\textbf{{{text}}}", font_size=34, color=C_GREY).to_corner(UL, buff=0.35)
        self.play(FadeIn(h, shift=0.2 * RIGHT))
        return h

    def swap_heading(self, old: Tex, text: str) -> Tex:
        text = re.sub(r"(?<!\\)_", r"\\_", text)
        h = Tex(rf"\textbf{{{text}}}", font_size=34, color=C_GREY).to_corner(UL, buff=0.35)
        self.play(ReplacementTransform(old, h))
        return h

    def clear(self, keep=()):
        mobs = [m for m in self.mobjects if m not in keep]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs])


def obj_circle(value, color=C_OBJ, r=0.5, size=30, label=None) -> VGroup:
    """A scalar object in memory: a circle with its value (and an optional type label)."""
    c = Circle(r, stroke_color=color, fill_color=color, fill_opacity=0.15, stroke_width=3)
    g = VGroup(c, mono(str(value), size).move_to(c))
    if label:
        g.add(mono(label, 18, color=color).next_to(c, UP, buff=0.08))
    return g


def pill(text: str, color, size=20) -> VGroup:
    t = mono(text, size, color=BLACK, weight=BOLD)
    r = RoundedRectangle(corner_radius=0.08, width=t.width + 0.3, height=t.height + 0.22,
                         stroke_width=0, fill_color=color, fill_opacity=1)
    return VGroup(r, t.move_to(r))


def tex(s: str, size=30, color=WHITE, **kw) -> Tex:
    return Tex(s, font_size=size, color=color, **kw)


def grid_of(values, rows, cols, w=0.8, color=C_OBJ, size=28) -> VGroup:
    """A rows x cols block of cells (row-major), e.g. a 2-D array."""
    g = VGroup(*[cell(v, w=w, h=w, color=color, size=size) for v in values])
    return g.arrange_in_grid(rows, cols, buff=0)
