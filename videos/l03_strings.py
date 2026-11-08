from lesson import *


def char_row(s: str, w=0.62, color=C_OBJ):
    cells = VGroup(*[cell(ch if ch != " " else "␣", w=w, h=w * 1.15, color=color, size=28) for ch in s])
    cells.arrange(RIGHT, buff=0)
    pos = VGroup(*[mono(str(i), 18, color=C_GREY).next_to(c, UP, buff=0.1) for i, c in enumerate(cells)])
    neg = VGroup(*[mono(str(i - len(s)), 16, color=C_GREY).next_to(c, DOWN, buff=0.1)
                   for i, c in enumerate(cells)])
    return cells, pos, neg


class L03Strings(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 3, "strings", "Strings", "Python"

    def construct(self):
        self.intro("Lesson three: strings. A Python string is an immutable sequence of Unicode characters. "
                   "Indexing and slicing work exactly like on every other sequence, and f-strings handle "
                   "formatting.", r"slicing, methods, f-strings, immutability")
        self.slicing()
        self.methods()
        self.fstrings()
        self.immutable()
        self.outro([r"\texttt{s[start:stop:step]}: stop is exclusive, negatives count from the end.",
                    r"String methods never modify; they return a \emph{new} string.",
                    r"f-strings: any expression in braces, a format spec after the colon.",
                    r"\texttt{str} is text, \texttt{bytes} is binary; convert with encode / decode."],
                   "Remember: slices exclude the stop index, methods return new strings, f-strings do all "
                   "the formatting, and text only becomes bytes when you encode it.")

    def slicing(self):
        h = self.heading("Indexing and slicing")
        s = "Hello, Python"
        cells, pos, neg = char_row(s)
        g = VGroup(cells, pos, neg).move_to(UP * 1.4)
        expr = mono('s = "Hello, Python"', 30).to_edge(LEFT, buff=0.8).shift(DOWN * 0.8)
        with self.say("A string is a row of characters. Indices start at zero, and negative indices count "
                      "from the end, so s of minus one is the last character."):
            self.play(FadeIn(expr), LaggedStart(*[FadeIn(c, shift=0.2 * DOWN) for c in cells], lag_ratio=0.05))
            self.play(FadeIn(pos))
            self.play(FadeIn(neg))
            hl = SurroundingRectangle(cells[0], color=C_YELLOW, buff=0.03)
            hl2 = SurroundingRectangle(cells[-1], color=C_YELLOW, buff=0.03)
            r = mono("s[0], s[-1]  ->  H n", 30, color=C_YELLOW).next_to(expr, DOWN, buff=0.4, aligned_edge=LEFT)
            self.play(Create(hl), Create(hl2), FadeIn(r))
        with self.say("A slice takes start, stop and step. The stop index is excluded. "
                      "s from seven to the end gives Python; a step of two takes every second character; "
                      "and a step of minus one walks backwards, reversing the string."):
            self.play(FadeOut(hl), FadeOut(hl2))
            sel = SurroundingRectangle(cells[7:], color=C_GREEN, buff=0.04)
            r2 = mono("s[7:]    ->  Python", 30, color=C_GREEN).move_to(r, aligned_edge=LEFT)
            self.play(Create(sel), ReplacementTransform(r, r2))
            self.wait(0.6)
            marks = VGroup(*[SurroundingRectangle(cells[i], color=C_GOLD, buff=0.03) for i in range(0, len(s), 2)])
            r3 = mono("s[::2]   ->  Hlo yhn", 30, color=C_GOLD).move_to(r2, aligned_edge=LEFT)
            self.play(FadeOut(sel), LaggedStart(*[Create(m) for m in marks], lag_ratio=0.1),
                      ReplacementTransform(r2, r3))
            self.wait(0.6)
            rev = cells.copy()
            r4 = mono("s[::-1]  ->  nohtyP ,olleH", 30, color=C_TEAL).move_to(r3, aligned_edge=LEFT)
            self.play(FadeOut(marks), ReplacementTransform(r3, r4))
            target = VGroup(*reversed([c.copy() for c in cells])).arrange(RIGHT, buff=0).next_to(r4, DOWN, buff=0.5)
            target.align_to(r4, LEFT).set_color(C_TEAL)
            self.play(LaggedStart(*[c.animate.move_to(t).set_color(C_TEAL) for c, t in zip(rev[::-1], target)],
                                  lag_ratio=0.05), run_time=2)
        self.clear(keep=[h])
        self.h = h

    def methods(self):
        h = self.swap_heading(self.h, "Methods return new strings")
        code = code_panel('s.upper()\ns.split(", ")\n"-".join(["a", "b", "c"])\n"  hi  ".strip()\n'
                          '"abc".replace("b", "B")\n"py" in s.lower()', font_size=26)
        code.to_edge(LEFT, buff=0.6)
        con = Console(width=5.4, height=3.9).to_edge(RIGHT, buff=0.6)
        mk = Marker(code)
        outs = ["'HELLO, PYTHON'", "['Hello', 'Python']", "'a-b-c'", "'hi'", "'aBc'", "True"]
        with self.say("Strings come with a rich set of methods: change case, split into a list, join a list "
                      "back together, strip whitespace, replace, search. Every one of them returns a new string; "
                      "the original is never touched. Join is called on the separator, not on the list."):
            self.play(FadeIn(code), FadeIn(con))
            for i, o in enumerate(outs):
                self.play(mk.to(i), run_time=0.4)
                self.play(con.print(o, color=C_YELLOW), run_time=0.5)
            self.play(Circumscribe(code.code_lines[2], color=C_GOLD))
        self.clear(keep=[h])
        self.h = h

    def fstrings(self):
        h = self.swap_heading(self.h, "f-strings")
        big = mono('f"{pi:.2f}"', 56).move_to(UP * 1.5)
        with self.say("An f-string evaluates any expression inside its braces. After a colon comes a format "
                      "spec: point two f means two decimal places."):
            self.play(Write(big))
            expr = SurroundingRectangle(big[3:5], color=C_BLUE, buff=0.06)
            spec = SurroundingRectangle(big[6:9], color=C_GOLD, buff=0.06)
            le = tex("expression", 32, C_BLUE).next_to(expr, DOWN, buff=0.35)
            ls = tex("format spec", 32, C_GOLD).next_to(spec, DOWN, buff=0.35).shift(RIGHT * 0.6)
            self.play(Create(expr), FadeIn(le))
            self.play(Create(spec), FadeIn(ls))
            res = mono("->  3.14", 44, color=C_YELLOW).next_to(big, RIGHT, buff=0.5)
            self.play(FadeIn(res, shift=0.2 * LEFT))
        rows = [('f"{1234567:,}"', "1,234,567"), ('f"{0.25:.0%}"', "25%"), ('f"{7:03d}"', "007"),
                ('f"{255:x}"', "ff"), ('f"{pi=}"', "pi=3.14159")]
        tbl = VGroup(*[VGroup(mono(a, 28), mono(b, 28, color=C_YELLOW)).arrange(RIGHT, buff=0.8) for a, b in rows])
        for r in tbl:
            r[1].move_to([2.2, 0, 0], aligned_edge=LEFT).match_y(r[0])
        tbl.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(DOWN * 1.6)
        for r in tbl:
            r[1].set_x(2.6, LEFT)
        with self.say("The same mini-language gives thousands separators, percentages, zero padding and hex. "
                      "And the equals sign prints the expression next to its value, which is perfect for "
                      "quick debugging."):
            self.play(LaggedStart(*[FadeIn(r, shift=0.2 * UP) for r in tbl], lag_ratio=0.3), run_time=2.5)
        self.clear(keep=[h])
        self.h = h

    def immutable(self):
        h = self.swap_heading(self.h, "Strings are immutable")
        code = code_panel('s = "Hello"\ns[0] = "J"         # TypeError\ns = "J" + s[1:]', font_size=28)
        code.to_edge(LEFT, buff=0.6).shift(UP * 1.2)
        mk = Marker(code)
        old = list_obj(list("Hello"), label="str").move_to(RIGHT * 3.5 + UP * 1.4)
        tag = name_tag("s").move_to(RIGHT * 0.6 + UP * 0.4)
        arr = pointer(tag, old[0])
        with self.say("You can't change a string in place. Assigning to an index raises a type error."):
            self.play(FadeIn(code), mk.to(0))
            self.play(FadeIn(old), FadeIn(tag), GrowArrow(arr))
            self.play(mk.to(1, color=C_BAD))
            cross = Cross(old[0][0], stroke_color=C_BAD)
            self.play(Create(cross))
        with self.say("Instead, build a new string from pieces and rebind the name. The old object is "
                      "untouched. Text becomes bytes only when you encode it: café in UTF-8 is five bytes."):
            self.play(FadeOut(cross), mk.to(2, color=C_GREEN))
            new = list_obj(list("Jello"), label="str", color=C_NEW).move_to(RIGHT * 3.5 + DOWN * 0.8)
            self.play(TransformFromCopy(old[0][1:], new[0][1:]), FadeIn(new[0][0]), FadeIn(new[1]))
            self.play(Transform(arr, pointer(tag, new[0], color=C_NAME)), old.animate.set_opacity(0.3))
            enc = mono('"café".encode("utf-8")  ->  b\'caf\\xc3\\xa9\'', 26, color=C_GREY)
            enc.to_edge(DOWN, buff=0.8)
            self.play(FadeIn(enc))
        self.clear()
