"""Shared building blocks for the four tutorial videos."""
from manim import *
from style3b1b import *

MONO = "Cascadia Mono"
CODE_BG = "#1a1c24"

# concept colours, fixed across all four videos
C_NAME = C_YELLOW     # a Python name / label
C_OBJ = C_BLUE        # an object in memory
C_NEW = C_GREEN       # something newly created
C_BAD = C_RED         # surprise / bug / removed


def mono(s: str, size: float = 26, color=WHITE, **kw) -> Text:
    return Text(s, font=MONO, font_size=size, color=color, **kw)


def code_panel(src: str, font_size: float = 22) -> Code:
    code = Code(
        code_string=src.strip("\n"), language="python", formatter_style="monokai",
        add_line_numbers=False, background="rectangle",
        background_config={"fill_color": CODE_BG, "fill_opacity": 1,
                           "stroke_color": GREY_D, "stroke_width": 1, "buff": 0.25},
        paragraph_config={"font": MONO, "font_size": font_size},
    )
    return code


def line_marker(code: Code, i: int, color=C_YELLOW, j: int | None = None) -> VGroup:
    """Tinted bar across lines i..j (inclusive) of a Code panel (use Transform to move it)."""
    bg = code.submobjects[0]
    j = i if j is None else j
    lines = [code.code_lines[k] for k in range(i, j + 1) if len(code.code_lines[k])]
    pad = code.code_lines[0].height * 0.35
    top = max(l.get_top()[1] for l in lines) + pad
    bot = min(l.get_bottom()[1] for l in lines) - pad
    h = top - bot
    bar = Rectangle(width=bg.width - 0.08, height=h, stroke_width=0,
                    fill_color=color, fill_opacity=0.16)
    bar.move_to([bg.get_center()[0], (top + bot) / 2, 0])
    tick = Rectangle(width=0.06, height=h, stroke_width=0, fill_color=color, fill_opacity=1)
    tick.next_to(bar, LEFT, buff=0).shift(RIGHT * 0.06)
    return VGroup(bar, tick)


def type_code(scene: Scene, code: Code, lines=None, run_time_per_line=0.6):
    """Reveal code lines one at a time (background first)."""
    lines = range(len(code.code_lines)) if lines is None else lines
    for i in lines:
        if len(code.code_lines[i]):
            scene.play(FadeIn(code.code_lines[i], shift=0.15 * RIGHT), run_time=run_time_per_line)


def chapter(scene: Scene, text: str, corner_only: bool = False) -> Tex:
    """Big centred chapter heading that shrinks into the top-left corner; returns it.
    corner_only: write it straight into the corner (when the stage isn't empty)."""
    head = Tex(rf"\textbf{{{text}}}", font_size=52)
    if corner_only:
        head.scale(0.6).to_corner(UL, buff=0.35).set_color(C_GREY)
        scene.play(Write(head))
        return head
    scene.play(Write(head), run_time=1)
    scene.wait(0.4)
    scene.play(head.animate.scale(0.6).to_corner(UL, buff=0.35).set_color(C_GREY))
    return head


# ---------------------------------------------------------------- memory model
def name_tag(name: str, color=C_NAME) -> VGroup:
    t = mono(name, 32, color=BLACK, weight=BOLD)
    box = RoundedRectangle(corner_radius=0.08, width=max(0.7, t.width + 0.35), height=0.62,
                           stroke_width=0, fill_color=color, fill_opacity=1)
    t.move_to(box)
    return VGroup(box, t)


def cell(value, w=0.8, h=0.8, color=C_OBJ, size=32, fill_opacity=0.15) -> VGroup:
    sq = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5,
                   fill_color=color, fill_opacity=fill_opacity)
    txt = mono(str(value), size).move_to(sq)
    return VGroup(sq, txt)


def list_obj(values, color=C_OBJ, w=0.8, label="list", direction=RIGHT) -> VGroup:
    """A list object: row (or column) of cells plus a small type label above. [0] = cells VGroup."""
    cells = VGroup(*[cell(v, w=w, h=w, color=color) for v in values]).arrange(direction, buff=0)
    lab = mono(label, 20, color=color).next_to(cells, UP, buff=0.08, aligned_edge=LEFT)
    return VGroup(cells, lab)


def pointer(start_mob: Mobject, end_mob: Mobject, color=C_NAME, **kw) -> Arrow:
    return Arrow(start_mob.get_right(), end_mob.get_left(), buff=0.12, color=color,
                 stroke_width=4, max_tip_length_to_length_ratio=0.25, **kw)


# ---------------------------------------------------------------- tables
def table_grid(rows, col_widths, row_h=0.5, size=22, header_color=C_GREY,
               index=None, index_w=0.5) -> VGroup:
    """Simple data table. rows[0] is the header. Returns VGroup(*row VGroups);
    each row VGroup holds cell VGroups (rect, text). Index column (if given) is cell 0."""
    out = VGroup()
    for r, row in enumerate(rows):
        g = VGroup()
        vals = ([("" if r == 0 else index[r - 1])] if index is not None else []) + list(row)
        widths = ([index_w] if index is not None else []) + list(col_widths)
        for c, (v, w) in enumerate(zip(vals, widths)):
            is_idx = index is not None and c == 0
            rect = Rectangle(width=w, height=row_h, stroke_width=1, stroke_color=GREY_D,
                             fill_color=CODE_BG if r else "#262a36", fill_opacity=1)
            col = header_color if r == 0 else (C_GREY if is_idx else WHITE)
            if v in ("NaN",):
                col = C_BAD
            txt = mono(str(v), size, color=col, weight=BOLD if r == 0 else NORMAL)
            txt.move_to(rect)
            g.add(VGroup(rect, txt))
        g.arrange(RIGHT, buff=0)
        out.add(g)
    out.arrange(DOWN, buff=0)
    return out


def end_card(scene: Scene, lines: list[str], title="Take-aways"):
    head = Tex(rf"\textbf{{{title}}}", font_size=48, color=C_YELLOW)
    items = VGroup(*[Tex(rf"$\blacktriangleright$\ \ {l}", font_size=34) for l in lines])
    items.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
    VGroup(head, items).arrange(DOWN, buff=0.6)
    scene.play(Write(head))
    scene.play(LaggedStart(*[FadeIn(i, shift=0.3 * RIGHT) for i in items], lag_ratio=0.5), run_time=2.5)
    scene.wait(3)
    fade_out_all(scene)
