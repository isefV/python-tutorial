from lesson import *


class L18Idioms(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 18, "pythonic-idioms", "Pythonic idioms", "Python"

    PAIRS = [
        ("Iterate over items, not indices",
         "for i in range(len(xs)):\n    print(i, xs[i])", "for i, x in enumerate(xs):\n    print(i, x)"),
        ("Truthiness and is None",
         "if len(xs) == 0: ...\nif x == None: ...", "if not xs: ...\nif x is None: ..."),
        ("Build strings with join",
         's = ""\nfor p in parts:\n    s += p', 's = "".join(parts)'),
        ("Swap with tuple unpacking",
         "tmp = a\na = b\nb = tmp", "a, b = b, a"),
        ("Comprehensions instead of append loops",
         "result = []\nfor x in range(5):\n    result.append(x * 2)", "result = [x * 2 for x in range(5)]"),
        ("dict.get with a default",
         'if "pear" in d:\n    n = d["pear"]\nelse:\n    n = 0', 'n = d.get("pear", 0)'),
        ("Chained comparisons and f-strings",
         'if x > 0 and x < 10:\n    msg = name + " is " + str(age)', 'if 0 < x < 10:\n    msg = f"{name} is {age}"'),
        ("Always use with for resources",
         'f = open(path)\ndata = f.read()\nf.close()', 'with open(path) as f:\n    data = f.read()'),
    ]
    NARR = [
        "Need the index too? Don't loop over range of len. enumerate gives you index and item together.",
        "Test emptiness by truthiness, and compare with None using is, never with double equals.",
        "Adding strings in a loop copies them again and again. join builds the result in one pass.",
        "Swapping needs no temporary variable: the right side is packed into a tuple, then unpacked.",
        "A loop that only appends is a comprehension waiting to happen: one line, and usually faster.",
        "dict dot get with a default replaces a whole if else block, and never raises a key error.",
        "Comparisons chain like in maths, and f-strings beat concatenation and str calls.",
        "And any resource that must be released belongs in a with block, so it closes even on errors.",
    ]

    def construct(self):
        self.intro("Lesson eighteen: Pythonic idioms. Code can be correct and still not read like Python. "
                   "Here are the habits that make the difference, each shown as the C-style version first, "
                   "then the idiomatic one.", r"the same result, written the Python way")
        h = None
        for (title, before, after), narr in zip(self.PAIRS, self.NARR):
            h = self.heading(title) if h is None else self.swap_heading(h, title)
            b = code_panel(before, font_size=26)
            a = code_panel(after, font_size=26)
            bl = tex(r"C-style", 36, C_BAD)
            al = tex(r"Pythonic", 36, C_GREEN)
            left = VGroup(bl, b).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            right = VGroup(al, a).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            VGroup(left, right).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to(DOWN * 0.2)
            if VGroup(left, right).width > 12.6:
                VGroup(left, right).scale_to_fit_width(12.6)
            arrow = Arrow(left.get_right(), right.get_left(), buff=0.15, color=C_YELLOW).match_y(VGroup(b, a))
            with self.say(narr):
                self.play(FadeIn(left))
                self.play(GrowArrow(arrow), FadeIn(right, shift=0.3 * LEFT))
                self.play(Circumscribe(a, color=C_GREEN))
            self.play(FadeOut(left), FadeOut(right), FadeOut(arrow))
        self.zen(h)
        self.outro([r"Loop over items; use \texttt{enumerate} and \texttt{zip} for indices and pairs.",
                    r"Rely on truthiness; test \texttt{None} with \texttt{is}.",
                    r"\texttt{join}, \texttt{get}, comprehensions, f-strings, chained comparisons.",
                    r"Resources always go in a \texttt{with} block."],
                   "None of these change what the code does. They change how fast another Python programmer "
                   "can read it, and that is what Pythonic really means.")

    def zen(self, h):
        h = self.swap_heading(h, "The Zen of Python")
        lines = ["Beautiful is better than ugly.", "Explicit is better than implicit.", "Simple is better than complex.",
                 "Readability counts.", "There should be one obvious way to do it."]
        cmd = mono(">>> import this", 30, color=C_GREEN).move_to(UP * 2.0)
        z = VGroup(*[tex(rf"\emph{{{l}}}", 38) for l in lines]).arrange(DOWN, buff=0.3).next_to(cmd, DOWN, buff=0.6)
        with self.say("Type import this in any Python shell to read the Zen of Python. A few lines sum up "
                      "everything in this lesson: explicit is better than implicit, simple is better than complex, "
                      "and readability counts."):
            self.play(FadeIn(cmd))
            self.play(LaggedStart(*[FadeIn(l, shift=0.2 * UP) for l in z], lag_ratio=0.4), run_time=3)
            self.play(Indicate(z[3], color=C_YELLOW))
        self.clear()
