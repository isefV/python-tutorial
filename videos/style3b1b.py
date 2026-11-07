"""Shared 3Blue1Brown-flavoured style helpers. Copy next to your scene file and
`from style3b1b import *` (after `from manim import *`)."""
from manim import *

# ---- palette (close to 3b1b's) -------------------------------------------
BG = "#0f0f14"          # near-black, slightly blue
C_BLUE = "#58C4DD"      # primary curves / main object
C_YELLOW = "#FFFF00"    # highlight, "look here"
C_GREEN = "#83C167"     # positive / first basis / input
C_RED = "#FC6255"       # negative / second basis / output
C_TEAL = "#5CD0B3"
C_GOLD = "#F0AC5F"
C_PURPLE = "#9A72AC"
C_GREY = "#888888"      # de-emphasised context

config.background_color = BG


def title_card(scene: Scene, text: str, subtitle: str | None = None):
    """LaTeX-typeset title (Computer Modern look) with underline; fades out upward."""
    title = Tex(rf"\textbf{{{text}}}", font_size=60)
    group = VGroup(title, Underline(title, color=C_BLUE, buff=0.15))
    if subtitle:
        group.add(Tex(subtitle, font_size=36, color=C_GREY).next_to(group, DOWN, buff=0.4))
    scene.play(Write(title), run_time=1.5)
    scene.play(*[FadeIn(m, shift=0.2 * UP) for m in group[1:]])
    scene.wait(1)
    scene.play(FadeOut(group, shift=UP))


def caption(text: str, **kw) -> Tex:
    """Small explanatory line at the bottom of the frame with a dark backing."""
    t = Tex(text, font_size=kw.pop("font_size", 34), **kw).to_edge(DOWN, buff=0.4)
    t.add_background_rectangle(color=BG, opacity=0.85, buff=0.15)
    return t


def fade_out_all(scene: Scene, run_time: float = 1.0):
    if scene.mobjects:
        scene.play(*[FadeOut(m) for m in scene.mobjects], run_time=run_time)
