from lesson import *


class L17Modules(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 17, "modules-stdlib", "Modules and the standard library", "Python"

    def construct(self):
        self.intro("Lesson seventeen: modules and the standard library. Every Python file is a module, a folder "
                   "of modules is a package, and the standard library covers a surprising amount before you need "
                   "anything from PyPI.", r"imports, \texttt{\_\_main\_\_}, dates, regex, CLI tools")
        self.imports()
        self.main_guard()
        self.regex()
        self.tour()
        self.outro([r"A file is a module, a folder of modules is a package.",
                    r"Guard script code with \texttt{if \_\_name\_\_ == '\_\_main\_\_':}",
                    r"\texttt{datetime}, \texttt{re}, \texttt{statistics}, \texttt{pathlib}, \texttt{json}: batteries included.",
                    r"\texttt{argparse}, \texttt{logging}, \texttt{subprocess} for real command-line tools."],
                   "Modules are files, packages are folders, the main guard separates script from library, and "
                   "the standard library already has dates, regular expressions, statistics and command-line tools.")

    def imports(self):
        h = self.heading("Import forms")
        tree = VGroup(mono("project/", 26, color=C_GOLD), mono("  main.py", 26), mono("  shop/", 26, color=C_GOLD),
                      mono("    __init__.py", 26, color=C_GREY), mono("    cart.py", 26), mono("    prices.py", 26))
        tree.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(LEFT, buff=1.0).shift(DOWN * 0.2)
        forms = VGroup(mono("import math", 28), mono("import statistics as stats", 28),
                       mono("from pathlib import Path", 28), mono("from shop.cart import Cart", 28, color=C_GOLD))
        forms.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(RIGHT * 2.6 + DOWN * 0.2)
        with self.say("A module is just a py file, and a package is a folder of them. import binds the module "
                      "name; as gives it an alias; from import pulls names out of it. Prefer explicit imports over "
                      "star imports, so readers can see where every name comes from."):
            self.play(LaggedStart(*[FadeIn(t, shift=0.2 * RIGHT) for t in tree], lag_ratio=0.15))
            self.play(LaggedStart(*[FadeIn(f, shift=0.2 * LEFT) for f in forms], lag_ratio=0.35), run_time=2.5)
            self.play(Indicate(tree[4], color=C_GOLD), Indicate(forms[3], color=C_GOLD))
        self.clear(keep=[h])
        self.h = h

    def main_guard(self):
        h = self.swap_heading(self.h, r"The \_\_main\_\_ guard")
        code = code_panel('def main():\n    print("running main()")\n\nif __name__ == "__main__":\n    main()',
                          font_size=30).to_edge(LEFT, buff=0.6)
        run = VGroup(mono("python tool.py", 26, color=C_GREEN), mono('__name__ == "__main__"', 24),
                     mono("-> main() runs", 24, color=C_GREEN)).arrange(DOWN, buff=0.2)
        imp = VGroup(mono("import tool", 26, color=C_BLUE), mono('__name__ == "tool"', 24),
                     mono("-> nothing runs", 24, color=C_GREY)).arrange(DOWN, buff=0.2)
        VGroup(run, imp).arrange(DOWN, buff=0.9).move_to(RIGHT * 3.6)
        with self.say("Each module has a dunder name. When a file is run as a script, its name is the string "
                      "dunder main; when it's imported, it's the module's own name. So code under this guard runs "
                      "only when the file is executed directly, and importing it has no side effects."):
            self.play(FadeIn(code))
            self.play(FadeIn(run, shift=0.2 * LEFT))
            self.play(FadeIn(imp, shift=0.2 * LEFT))
        self.clear(keep=[h])
        self.h = h

    def regex(self):
        h = self.swap_heading(self.h, "Dates and regular expressions")
        txt = "Order 42 shipped on 2025-01-31, order 7 on 2025-02-02"
        t = mono(txt, 28).move_to(UP * 1.6)
        pat = mono(r're.findall(r"\d{4}-\d{2}-\d{2}", text)', 28, color=C_GOLD).move_to(UP * 0.4)
        with self.say("The re module handles regular expressions. findall returns every match: here, both dates. "
                      "Use raw strings for patterns, so backslashes reach the regex engine untouched."):
            self.play(FadeIn(t))
            self.play(FadeIn(pat))
            start1 = len("Order42shippedon")
            d1 = t[start1:start1 + 10]
            start2 = len("Order42shippedon2025-01-31,order7on")
            d2 = t[start2:start2 + 10]
            self.play(Create(SurroundingRectangle(d1, color=C_GOLD, buff=0.05)),
                      Create(SurroundingRectangle(d2, color=C_GOLD, buff=0.05)))
            res = mono("['2025-01-31', '2025-02-02']", 28, color=C_YELLOW).next_to(pat, DOWN, buff=0.3)
            self.play(FadeIn(res))
        with self.say("datetime parses and formats dates with strptime and strftime, and timedelta does date "
                      "arithmetic, like adding thirty days."):
            dt = VGroup(mono("date(2025, 10, 7) + timedelta(days=30)  -> 2025-11-06", 24),
                        mono('datetime.strptime("2025-01-31 14:05", "%Y-%m-%d %H:%M")', 24, color=C_GREY))
            dt.arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.8)
            self.play(FadeIn(dt, shift=0.2 * UP))
        self.clear(keep=[h])
        self.h = h

    def tour(self):
        h = self.swap_heading(self.h, "Batteries included")
        mods = [("statistics", "mean, median, pstdev"), ("random", "Random(42).randint(1, 6)"),
                ("functools", "partial(int, base=2)"), ("argparse", "parse command-line options"),
                ("logging", "levels, formats, handlers"), ("subprocess", "run other programs"),
                ("json / csv", "data formats"), ("collections", "Counter, deque, ...")]
        cards = VGroup()
        for m, d in mods:
            r = RoundedRectangle(corner_radius=0.12, width=5.6, height=0.95, stroke_color=C_BLUE, fill_color=C_BLUE,
                                 fill_opacity=0.08)
            g = VGroup(mono(m, 24, color=C_BLUE), mono(d, 18, color=C_GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            g.move_to(r).align_to(r, LEFT).shift(RIGHT * 0.25)
            cards.add(VGroup(r, g))
        cards.arrange_in_grid(rows=4, cols=2, buff=(0.4, 0.25), flow_order="dr").move_to(DOWN * 0.3)
        with self.say("A quick tour of what's in the box: statistics for basic stats, random with a seeded "
                      "generator for reproducibility, functools for partial and caching, argparse for command-line "
                      "options, logging instead of print, and subprocess to run other programs."):
            self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in cards], lag_ratio=0.2), run_time=3)
        self.clear()
