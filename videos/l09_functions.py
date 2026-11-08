from lesson import *


class L09Functions(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 9, "functions", "Functions", "Python"

    def construct(self):
        self.intro("Lesson nine: functions. def creates a function; arguments can be passed by position or "
                   "by name, and Python gives you precise control over which is allowed.",
                   r"defaults, keywords, parameter kinds, \texttt{*args}, \texttt{**kwargs}")
        self.basics()
        self.kinds()
        self.varargs()
        self.returns()
        self.outro([r"Defaults and keyword arguments make calls readable.",
                    r"\texttt{/} ends positional-only, \texttt{*} starts keyword-only.",
                    r"\texttt{*args} is a tuple, \texttt{**kwargs} a dict; \texttt{*}/\texttt{**} also unpack.",
                    r"Return a tuple for several values; type hints are not enforced."],
                   "Give parameters defaults, pass arguments by name when it helps, use slash and star to "
                   "control how a function may be called, and return tuples for several results.")

    def basics(self):
        h = self.heading("Defaults, keywords and docstrings")
        code = code_panel('def greet(name: str, greeting: str = "Hello") -> str:\n    """Return a greeting for `name`."""\n'
                          '    return f"{greeting}, {name}!"\n\ngreet("Ada")\ngreet(greeting="Hi", name="Ada")',
                          font_size=26).to_edge(UP, buff=1.1)
        mk = Marker(code)
        con = Console(width=6.0, height=1.5).next_to(code, DOWN, buff=0.4)
        with self.say("A parameter can have a default value, so callers may leave it out. The string right "
                      "under def is the docstring; help shows it. The annotations are documentation only."):
            self.play(FadeIn(code), mk.to(0))
            self.play(Circumscribe(code.code_lines[0], color=C_GOLD))
            self.play(mk.to(1))
        with self.say("At the call site, arguments can be passed by position or by name. Named arguments "
                      "can come in any order, and they make the call read like a sentence."):
            self.play(FadeIn(con), mk.to(4))
            self.play(con.print("Hello, Ada!", color=C_YELLOW))
            self.play(mk.to(5))
            self.play(con.print("Hi, Ada!", color=C_YELLOW))
        self.clear(keep=[h])
        self.h = h

    def kinds(self):
        h = self.swap_heading(self.h, "Parameter kinds")
        sig = mono("def f(a, b, /, c, *, d=1, **kw):", 40).move_to(UP * 2.0)
        with self.say("The full signature can mix five kinds of parameters. Everything before a slash is "
                      "positional-only. Between slash and star, a parameter may be passed either way. After "
                      "the star, parameters are keyword-only, and double star kw collects any extra keywords."):
            self.play(Write(sig))
            zones = [(sig[5:8], C_BLUE, "positional\nonly"), (sig[11:12], C_GREEN, "either"),
                     (sig[15:18], C_GOLD, "keyword\nonly"), (sig[19:23], C_PURPLE, "extra\nkeywords")]
            labs = VGroup()
            for mob, col, txt in zones:
                r = SurroundingRectangle(mob, color=col, buff=0.07)
                t = Text(txt, font_size=22, color=col, line_spacing=0.8).next_to(r, DOWN, buff=0.2)
                labs.add(VGroup(r, t))
                self.play(Create(r), FadeIn(t), run_time=0.7)
        call = mono("f(1, 2, 3, d=4, e=5)", 34).move_to(DOWN * 1.0)
        res = mono("-> (1, 2, 3, 4, {'e': 5})", 30, color=C_YELLOW).next_to(call, DOWN, buff=0.35)
        bad = mono("f(a=1, b=2, c=3)  -> TypeError", 30, color=C_BAD).next_to(res, DOWN, buff=0.35)
        with self.say("So f of one, two, three, d equals four, e equals five works, and e lands in the kw "
                      "dict. But passing a by name is a type error: it's positional-only. Library authors use "
                      "this to keep the freedom to rename parameters."):
            self.play(FadeIn(call))
            self.play(FadeIn(res, shift=0.2 * DOWN))
            self.play(FadeIn(bad, shift=0.2 * DOWN))
        self.clear(keep=[h])
        self.h = h

    def varargs(self):
        h = self.swap_heading(self.h, "*args and **kwargs")
        code = code_panel('def log(*args, **kwargs):\n    print(args, kwargs)\n\nlog(1, 2, level="info")\n'
                          'log(*[1, 2], **{"level": "info"})', font_size=28).to_edge(LEFT, buff=0.5).shift(UP * 0.8)
        mk = Marker(code)
        with self.say("A star parameter packs any extra positional arguments into a tuple, and a double-star "
                      "parameter packs extra keyword arguments into a dict."):
            self.play(FadeIn(code), mk.to(3))
            a1, a2 = mono("1", 34), mono("2", 34)
            kw = mono('level="info"', 30)
            src = VGroup(a1, a2, kw).arrange(RIGHT, buff=0.5).move_to(RIGHT * 4.4 + UP * 2.4)
            self.play(FadeIn(src))
            t = list_obj([1, 2], w=0.8, label="args: tuple", color=C_BLUE).move_to(RIGHT * 3.4 + UP * 0.6)
            d = VGroup(pill('"level"', C_GOLD, 22), mono(": 'info'", 24)).arrange(RIGHT, buff=0.1)
            dbox = SurroundingRectangle(d, color=C_GOLD, buff=0.2)
            dl = mono("kwargs: dict", 20, color=C_GOLD).next_to(dbox, UP, buff=0.08, aligned_edge=LEFT)
            dg = VGroup(dbox, d, dl).move_to(RIGHT * 4.6 + DOWN * 1.2)
            self.play(TransformFromCopy(VGroup(a1, a2), t[0]), FadeIn(t[1]))
            self.play(TransformFromCopy(kw, d), Create(dbox), FadeIn(dl))
        with self.say("The same stars work in reverse at a call site: star unpacks a list into positional "
                      "arguments, and double star unpacks a dict into keyword arguments."):
            self.play(mk.to(4))
            self.play(Indicate(code.code_lines[4], color=C_YELLOW, scale_factor=1.05))
            same = tex(r"same call as above", 30, C_GREY).next_to(code, DOWN, buff=0.4, aligned_edge=LEFT)
            self.play(FadeIn(same))
        self.clear(keep=[h])
        self.h = h

    def returns(self):
        h = self.swap_heading(self.h, "Returning values, hints and recursion")
        code = code_panel("def min_max(xs):\n    return min(xs), max(xs)\n\nlo, hi = min_max([3, 1, 4])\n\n"
                          'def double(x: int) -> int:\n    return x * 2\ndouble("ab")   # \'abab\'',
                          font_size=24).to_edge(LEFT, buff=0.5)
        mk = Marker(code)
        with self.say("To return several values, return a tuple and unpack it at the call. A function without "
                      "a return statement returns None. Type hints are not checked at runtime: doubling a string "
                      "happily returns a b a b. Tools like mypy check them before you run."):
            self.play(FadeIn(code), mk.to(0, 1))
            tup = mono("(1, 4)", 32, color=C_YELLOW).move_to(RIGHT * 3.6 + UP * 1.6)
            self.play(FadeIn(tup))
            self.play(mk.to(3))
            lo = VGroup(name_tag("lo"), name_tag("hi")).arrange(RIGHT, buff=0.6).next_to(tup, DOWN, buff=0.5)
            self.play(FadeIn(lo, shift=0.2 * UP))
            self.play(mk.to(5, 7, color=C_GOLD))
        with self.say("Recursion works as you'd expect, but Python doesn't optimise tail calls, and the default "
                      "depth limit is about a thousand frames, so prefer loops for deep iteration."):
            stack = VGroup(*[Rectangle(width=3.2, height=0.5, stroke_color=C_BLUE, fill_color=C_BLUE,
                                       fill_opacity=0.12 + 0.05 * i) for i in range(5)]).arrange(UP, buff=0.06)
            stack.move_to(RIGHT * 3.6 + DOWN * 2.1)
            labs = VGroup(*[mono(f"factorial({5 - i})", 20).move_to(s) for i, s in enumerate(stack)])
            self.play(LaggedStart(*[AnimationGroup(FadeIn(s, shift=0.2 * DOWN), FadeIn(l)) for s, l in zip(stack, labs)],
                                  lag_ratio=0.3), run_time=2)
            lim = mono("sys.getrecursionlimit() -> 1000", 22, color=C_GREY).next_to(stack, UP, buff=0.25)
            self.play(FadeIn(lim))
        self.clear()
