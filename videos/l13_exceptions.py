from lesson import *


class L13Exceptions(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 13, "exceptions", "Exceptions", "Python"

    def construct(self):
        self.intro("Lesson thirteen: exceptions. Python reports errors by raising exceptions, and it uses them "
                   "freely, even for ordinary situations like a missing key. Handling them well is everyday Python.",
                   r"\texttt{try} / \texttt{except} / \texttt{else} / \texttt{finally}, \texttt{raise from}, EAFP")
        self.flow()
        self.custom()
        self.eafp()
        self.builtins()
        self.outro([r"\texttt{except} handles, \texttt{else} runs on success, \texttt{finally} always runs.",
                    r"Subclass a built-in exception; chain causes with \texttt{raise ... from err}.",
                    r"Catch specific types, several at once with a tuple.",
                    r"EAFP: try it and handle the failure, rather than checking first."],
                   "Put only the risky line in try, handle specific exceptions, use else for the success path and "
                   "finally for cleanup, and chain your own exceptions to the original cause.")

    def flow(self):
        h = self.heading("try / except / else / finally")
        code = code_panel('def to_int(text):\n    try:\n        value = int(text)\n    except ValueError as err:\n'
                          '        print("bad input:", err)\n        return None\n    else:\n        print("parsed", value)\n'
                          '        return value\n    finally:\n        print("finally runs")', font_size=22).to_edge(LEFT, buff=0.4)

        def blk(t, c):
            r = RoundedRectangle(corner_radius=0.12, width=2.6, height=0.75, stroke_color=c, fill_color=c, fill_opacity=0.12)
            return VGroup(r, mono(t, 26, color=c).move_to(r))
        b_try = blk("try", C_BLUE).move_to(RIGHT * 3.6 + UP * 2.2)
        b_exc = blk("except", C_BAD).move_to(RIGHT * 2.0 + UP * 0.4)
        b_els = blk("else", C_GREEN).move_to(RIGHT * 5.2 + UP * 0.4)
        b_fin = blk("finally", C_GOLD).move_to(RIGHT * 3.6 + DOWN * 1.4)
        arrows = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.1, color=GREY_B, stroke_width=3)
                          for a, b in [(b_try, b_exc), (b_try, b_els), (b_exc, b_fin), (b_els, b_fin)]])
        lbl = VGroup(mono("raised", 18, color=C_BAD).next_to(arrows[0], LEFT, buff=0.05),
                     mono("no error", 18, color=C_GREEN).next_to(arrows[1], RIGHT, buff=0.05))
        with self.say("Put the risky operation in the try block. If it raises, the matching except block handles "
                      "it. If nothing was raised, the else block runs. And finally runs in every case, even after "
                      "a return, which makes it the place for cleanup."):
            self.play(FadeIn(code))
            self.play(LaggedStart(*[FadeIn(b) for b in [b_try, b_exc, b_els, b_fin]], lag_ratio=0.2),
                      Create(arrows), FadeIn(lbl), run_time=2)
        mk = Marker(code)
        with self.say("Calling with forty-two: int succeeds, so else prints parsed, then finally runs. "
                      "With a b c, int raises a value error, so except prints bad input, and finally still runs."):
            for arg, path, lines, col in [('"42"', [b_try, b_els, b_fin], [(1, 2), (6, 8), (9, 10)], C_GREEN),
                                          ('"abc"', [b_try, b_exc, b_fin], [(1, 2), (3, 5), (9, 10)], C_BAD)]:
                inp = mono(f"to_int({arg})", 28, color=C_YELLOW).move_to(RIGHT * 3.6 + DOWN * 2.8)
                self.play(FadeIn(inp))
                dot = Dot(color=col, radius=0.13).move_to(path[0])
                self.play(FadeIn(dot, scale=2), mk.to(*lines[0]))
                for b, ln in zip(path[1:], lines[1:]):
                    self.play(dot.animate.move_to(b), mk.to(*ln), run_time=0.9)
                self.wait(0.4)
                self.play(FadeOut(dot), FadeOut(inp))
        self.clear(keep=[h])
        self.h = h

    def custom(self):
        h = self.swap_heading(self.h, "Custom exceptions and raise from")
        code = code_panel('class InvalidAge(ValueError):\n    """Age is not a valid non-negative int."""\n\n'
                          'def parse_age(text):\n    try:\n        age = int(text)\n    except ValueError as err:\n'
                          '        raise InvalidAge(f"bad age: {text!r}") from err', font_size=20).to_edge(LEFT, buff=0.4).shift(UP * 0.5)
        mk = Marker(code)
        with self.say("Define your own exception by subclassing a built-in one. Callers can catch InvalidAge "
                      "specifically, or catch any ValueError."):
            self.play(FadeIn(code), mk.to(0, 1))
            tree = VGroup(pill("Exception", C_GREY, 22), pill("ValueError", C_BAD, 22), pill("InvalidAge", C_GOLD, 22))
            tree.arrange(DOWN, buff=0.5).move_to(RIGHT * 4.6 + UP * 1.4)
            links = VGroup(*[Arrow(tree[i + 1].get_top(), tree[i].get_bottom(), buff=0.06, color=GREY_B, stroke_width=3)
                             for i in range(2)])
            self.play(FadeIn(tree), Create(links))
        with self.say("When you translate one error into another, raise the new one from the original. The "
                      "traceback then shows both, and the original is kept as the cause."):
            self.play(mk.to(6, 7, color=C_GOLD))
            e1 = pill("InvalidAge: bad age: 'abc'", C_GOLD, 20).move_to(RIGHT * 3.0 + DOWN * 2.0)
            e2 = pill("ValueError: invalid literal", C_BAD, 20).next_to(e1, DOWN, buff=0.6)
            cause = Arrow(e1.get_bottom(), e2.get_top(), buff=0.08, color=GREY_B)
            cl = mono("__cause__", 20, color=GREY_B).next_to(cause, RIGHT, buff=0.1)
            self.play(FadeIn(e1))
            self.play(GrowArrow(cause), FadeIn(cl), FadeIn(e2))
        self.clear(keep=[h])
        self.h = h

    def eafp(self):
        h = self.swap_heading(self.h, "EAFP versus LBYL")
        lbyl = code_panel("if key not in cache:\n    cache[key] = compute(key)\nreturn cache[key]", font_size=26)
        eafp = code_panel("try:\n    return cache[key]\nexcept KeyError:\n    value = cache[key] = compute(key)\n"
                          "    return value", font_size=26)
        tl = tex(r"Look before you leap", 34, C_GREY)
        te = tex(r"Easier to ask forgiveness than permission", 34, C_GREEN)
        left = VGroup(tl, lbyl).arrange(DOWN, buff=0.4)
        right = VGroup(te, eafp).arrange(DOWN, buff=0.4)
        VGroup(left, right).arrange(DOWN, buff=0.7).move_to(DOWN * 0.2)
        with self.say("Other languages often check first, then act: look before you leap. Python style usually "
                      "just tries the operation and handles the failure: it's easier to ask forgiveness than "
                      "permission. It avoids a double lookup and race conditions between the check and the use."):
            self.play(FadeIn(left))
            self.play(FadeIn(right, shift=0.2 * UP))
        with self.say("Whatever you catch, be specific. A tuple catches several types at once: except key error "
                      "or value error. A bare except hides real bugs."):
            multi = mono("except (KeyError, ValueError) as err:", 28, color=C_YELLOW)
            self.play(FadeOut(left), right.animate.to_edge(UP, buff=1.1))
            multi.next_to(right, DOWN, buff=0.7)
            self.play(FadeIn(multi, shift=0.2 * UP))
        self.clear(keep=[h])
        self.h = h

    def builtins(self):
        h = self.swap_heading(self.h, "Common built-in exceptions")
        rows = [["expression", "raises"], ["int('x')", "ValueError"], ["[1][5]", "IndexError"], ["{}['k']", "KeyError"],
                ["None.upper()", "AttributeError"], ["1 / 0", "ZeroDivisionError"], ["'a' + 1", "TypeError"]]
        t = table_grid(rows, [3.4, 4.2], row_h=0.62, size=26).move_to(DOWN * 0.2)
        for r in t[1:]:
            r[1][1].set_color(C_BAD)
        with self.say("You'll meet these six constantly. Learn to read them: the exception's name usually tells "
                      "you exactly what went wrong."):
            self.play(FadeIn(t[0]))
            self.play(LaggedStart(*[FadeIn(r, shift=0.2 * RIGHT) for r in t[1:]], lag_ratio=0.25), run_time=2.5)
        self.clear()
