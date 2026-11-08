from lesson import *


class L16Decorators(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 16, "decorators", "Decorators", "Python"

    def construct(self):
        self.intro("Lesson sixteen: decorators. A decorator is a function that takes a function and returns a new "
                   "one. The at sign above a def is just shorthand for that.",
                   r"wrappers, \texttt{functools.wraps}, \texttt{cache}, arguments, registration")
        self.shorthand()
        self.wrapper()
        self.cache()
        self.with_args()
        self.outro([r"\texttt{@d} above \texttt{def f} means \texttt{f = d(f)}.",
                    r"A wrapper runs code around each call; \texttt{wraps} keeps the name.",
                    r"\texttt{@functools.cache} memoizes a pure function in one line.",
                    r"Decorators with arguments are factories: one extra level of nesting."],
                   "The at sign means rebind the name to the decorator's result, wrappers add behaviour around "
                   "calls, cache memoizes, and a decorator with arguments is a function that builds a decorator.")

    def shorthand(self):
        h = self.heading("@ is shorthand")
        a = code_panel("@timed\ndef slow_sum(n):\n    return sum(range(n))", font_size=26)
        b = code_panel("def slow_sum(n):\n    return sum(range(n))\nslow_sum = timed(slow_sum)", font_size=26)
        VGroup(a, b).arrange(RIGHT, buff=1.2).move_to(UP * 0.3)
        eq = mono("=", 50, color=C_YELLOW).move_to((a.get_right() + b.get_left()) / 2)
        with self.say("Functions are objects, so they can be passed to other functions. Writing at timed above a "
                      "function definition is exactly the same as defining it, then rebinding its name to timed "
                      "of the function."):
            self.play(FadeIn(a))
            self.play(FadeIn(eq), FadeIn(b))
            self.play(Circumscribe(b.code_lines[2], color=C_YELLOW))
        self.clear(keep=[h])
        self.h = h

    def wrapper(self):
        h = self.swap_heading(self.h, "A timing decorator")
        code = code_panel('def timed(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n'
                          '        start = time.perf_counter()\n        result = func(*args, **kwargs)\n'
                          '        print(f"{func.__name__} took ...")\n        return result\n    return wrapper',
                          font_size=22).to_edge(LEFT, buff=0.4)
        mk = Marker(code)
        outer = RoundedRectangle(corner_radius=0.2, width=4.6, height=3.6, stroke_color=C_GOLD, fill_color=C_GOLD,
                                 fill_opacity=0.06).move_to(RIGHT * 3.8 + DOWN * 0.1)
        ol = mono("wrapper", 22, color=C_GOLD).next_to(outer, UP, buff=0.1, aligned_edge=LEFT)
        inner = RoundedRectangle(corner_radius=0.15, width=2.8, height=1.0, stroke_color=C_BLUE, fill_color=C_BLUE,
                                 fill_opacity=0.15).move_to(outer)
        il = mono("slow_sum", 24, color=C_BLUE).move_to(inner)
        before = mono("start timer", 20, color=C_GOLD).next_to(inner, UP, buff=0.35)
        after = mono("print elapsed", 20, color=C_GOLD).next_to(inner, DOWN, buff=0.35)
        with self.say("Here's a real one. timed defines an inner wrapper that accepts any arguments, starts a "
                      "timer, calls the original function, prints the elapsed time and passes the result back. "
                      "timed returns the wrapper, and that's what the name now points to."):
            self.play(FadeIn(code), mk.to(0))
            self.play(FadeIn(inner), FadeIn(il))
            self.play(mk.to(2), Create(outer), FadeIn(ol))
            self.play(mk.to(3), FadeIn(before))
            self.play(mk.to(4), Indicate(inner, color=C_BLUE))
            self.play(mk.to(5, 6), FadeIn(after))
            self.play(mk.to(7))
            call = mono("slow_sum(1_000_000)", 24, color=C_YELLOW).next_to(outer, DOWN, buff=0.3)
            dot = Dot(color=C_YELLOW, radius=0.11).move_to(outer.get_top())
            self.play(FadeIn(call), FadeIn(dot))
            self.play(MoveAlongPath(dot, Line(outer.get_top(), outer.get_bottom())), run_time=1.5)
        with self.say("functools dot wraps copies the original's name and docstring onto the wrapper, so "
                      "debugging and help still show slow sum instead of wrapper."):
            self.play(mk.to(1, color=C_GREEN), FadeOut(dot))
            nm = mono("slow_sum.__name__ -> 'slow_sum'", 22, color=C_GREEN).next_to(code, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(FadeIn(nm))
        self.clear(keep=[h])
        self.h = h

    def cache(self):
        h = self.swap_heading(self.h, "Memoization with functools.cache")
        code = code_panel("@functools.cache\ndef fib(n):\n    return n if n < 2 else fib(n - 1) + fib(n - 2)\n\n"
                          "fib(100)   # 354224848179261915075", font_size=24).to_edge(UP, buff=1.0)
        with self.say("The standard library ships useful decorators. cache remembers every result by its "
                      "arguments. The naive recursive Fibonacci would take forever for a hundred; with one line of "
                      "decoration, each value is computed once and fib of one hundred is instant."):
            self.play(FadeIn(code))
            table = VGroup(*[VGroup(mono(f"fib({i})", 22), mono(str(v), 22, color=C_YELLOW)).arrange(RIGHT, buff=0.3)
                             for i, v in enumerate([0, 1, 1, 2, 3, 5, 8, 13])])
            table.arrange_in_grid(rows=2, buff=(0.7, 0.35)).next_to(code, DOWN, buff=0.8)
            box = SurroundingRectangle(table, color=C_TEAL, buff=0.25)
            bl = mono("cache", 22, color=C_TEAL).next_to(box, UP, buff=0.08, aligned_edge=LEFT)
            self.play(Create(box), FadeIn(bl))
            self.play(LaggedStart(*[FadeIn(t, shift=0.2 * UP) for t in table], lag_ratio=0.2), run_time=2)
        self.clear(keep=[h])
        self.h = h

    def with_args(self):
        h = self.h = self.swap_heading(self.h, "Decorators with arguments")
        code = code_panel("def repeat(times):\n    def decorator(func):\n        def wrapper(*a, **kw):\n"
                          "            return [func(*a, **kw) for _ in range(times)]\n        return wrapper\n"
                          '    return decorator\n\n@repeat(3)\ndef greet(name): return f"hi {name}"',
                          font_size=20).to_edge(LEFT, buff=0.4)
        bands = [(0, 5, C_PURPLE, "factory\ntakes times"), (1, 4, C_GOLD, "decorator\ntakes func"),
                 (2, 3, C_BLUE, "wrapper\nruns per call")]
        with self.say("To pass arguments to a decorator, add one more level. repeat of three is called first and "
                      "returns the actual decorator, which then receives the function and returns the wrapper."):
            self.play(FadeIn(code))
            labs = VGroup()
            for k, (i, j, c, t) in enumerate(bands):
                bar = Rectangle(width=0.08, height=code.code_lines[i].get_top()[1] - code.code_lines[j].get_bottom()[1] + 0.1,
                                stroke_width=0, fill_color=c, fill_opacity=1)
                bar.move_to([code.get_left()[0] + 0.12 + 0.12 * k, (code.code_lines[i].get_top()[1] + code.code_lines[j].get_bottom()[1]) / 2, 0])
                lab = Text(t, font_size=24, color=c, line_spacing=0.8).move_to(RIGHT * 5.0 + UP * (1.6 - 1.2 * k))
                labs.add(lab)
                self.play(GrowFromEdge(bar, UP), FadeIn(lab), run_time=0.8)
            out = mono("greet('Ada') -> ['hi Ada', 'hi Ada', 'hi Ada']", 22, color=C_YELLOW).next_to(code, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(FadeIn(out))
        with self.say("Decorators don't have to wrap at all. A registration decorator just records the function, "
                      "say in a dict of commands, and returns it unchanged. Web frameworks route URLs this way."):
            self.clear(keep=[self.h])
            reg = code_panel('COMMANDS = {}\n\ndef command(name):\n    def decorator(func):\n        COMMANDS[name] = func\n'
                             '        return func\n    return decorator\n\n@command("hello")\ndef say_hello(): return "Hello!"',
                             font_size=24)
            self.play(FadeIn(reg))
            self.play(Circumscribe(reg.code_lines[4], color=C_GOLD))
        self.clear()
