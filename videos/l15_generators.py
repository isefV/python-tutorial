from lesson import *


class L15Generators(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 15, "iterators-generators", "Iterators and generators", "Python"

    def construct(self):
        self.intro("Lesson fifteen: iterators and generators. Every for loop runs on a tiny protocol of two "
                   "functions. Once you see it, generators, lazy pipelines and itertools all fall into place.",
                   r"\texttt{iter}, \texttt{next}, \texttt{yield}, lazy pipelines, \texttt{itertools}")
        self.protocol()
        self.generator()
        self.pipeline()
        self.itertools_()
        self.outro([r"\texttt{for} calls \texttt{iter()} once, then \texttt{next()} until \texttt{StopIteration}.",
                    r"A function with \texttt{yield} returns a generator that pauses between values.",
                    r"Chained generators process data one item at a time, in constant memory.",
                    r"A generator is consumed once; \texttt{itertools} has the building blocks."],
                   "A for loop is iter plus repeated next, yield turns a function into a pausable generator, "
                   "chained generators stream data, and itertools supplies the plumbing.")

    def protocol(self):
        h = self.heading("The iteration protocol")
        code = code_panel("it = iter([10, 20, 30])\nnext(it)   # 10\nnext(it)   # 20\nnext(it)   # 30\n"
                          "next(it)   # StopIteration", font_size=28).to_edge(LEFT, buff=0.6)
        mk = Marker(code)
        row = list_obj([10, 20, 30], w=1.0).move_to(RIGHT * 3.6 + UP * 0.8)
        with self.say("Behind every for loop: iter asks the iterable for an iterator, an object that remembers a "
                      "position. Each call to next returns the following item and advances."):
            self.play(FadeIn(code), FadeIn(row), mk.to(0))
            cur = Triangle(color=C_YELLOW, fill_opacity=1).scale(0.15).rotate(PI).next_to(row[0][0], UP, buff=0.12)
            self.play(FadeIn(cur))
            for i in range(3):
                self.play(mk.to(1 + i), run_time=0.5)
                out = mono(str((i + 1) * 10), 30, color=C_YELLOW).move_to(RIGHT * (2.6 + i) + DOWN * 1.2)
                self.play(TransformFromCopy(row[0][i], out), run_time=0.6)
                if i < 2:
                    self.play(cur.animate.next_to(row[0][i + 1], UP, buff=0.12), run_time=0.4)
        with self.say("When nothing is left, next raises StopIteration, and the for loop takes that as its "
                      "signal to stop. Write dunder iter and dunder next, and your own class works in a for loop."):
            self.play(mk.to(4, color=C_BAD), cur.animate.next_to(row[0][2], RIGHT, buff=0.2).set_color(C_BAD))
            stop = mono("StopIteration", 30, color=C_BAD).move_to(RIGHT * 3.6 + DOWN * 2.3)
            self.play(FadeIn(stop, shift=0.2 * UP))
        self.clear(keep=[h])
        self.h = h

    def generator(self):
        h = self.swap_heading(self.h, "Generator functions")
        code = code_panel("def fib():\n    a, b = 0, 1\n    while True:\n        yield a\n        a, b = b, a + b\n\n"
                          "g = fib()\nnext(g), next(g), next(g)", font_size=26).to_edge(LEFT, buff=0.6)
        mk = Marker(code)
        with self.say("Writing iterator classes by hand is tedious. A function that contains yield becomes a "
                      "generator instead. Calling it runs nothing yet; it returns a generator object."):
            self.play(FadeIn(code), mk.to(0, 4))
            self.play(mk.to(6))
            gen = RoundedRectangle(corner_radius=0.2, width=3.6, height=1.9, stroke_color=C_TEAL, fill_color=C_TEAL,
                                   fill_opacity=0.08).move_to(RIGHT * 3.8 + UP * 1.2)
            gl = mono("g: paused", 22, color=C_TEAL).next_to(gen, UP, buff=0.1)
            st = mono("a = 0, b = 1", 26).move_to(gen)
            self.play(Create(gen), FadeIn(gl), FadeIn(st))
        with self.say("Each next runs the body until the next yield, hands out that value, and freezes, keeping "
                      "all its local variables. This one is infinite, and that's fine: values only exist when "
                      "someone asks for them."):
            self.play(mk.to(7))
            outs = VGroup()
            for k, (v, a, b) in enumerate([(0, 1, 1), (1, 1, 2), (1, 2, 3)]):
                self.play(mk.to(3, color=C_GREEN), run_time=0.4)
                o = mono(str(v), 34, color=C_GOLD).move_to(gen)
                self.play(FadeIn(o, scale=0.5), st.animate.set_opacity(0.2), run_time=0.4)
                self.play(o.animate.move_to(RIGHT * (2.6 + 1.2 * k) + DOWN * 1.2), run_time=0.5)
                self.play(Transform(st, mono(f"a = {a}, b = {b}", 26).move_to(gen)), run_time=0.5)
                outs.add(o)
            self.play(mk.to(7))
        self.clear(keep=[h])
        self.h = h

    def pipeline(self):
        h = self.swap_heading(self.h, "Lazy pipelines")
        code = code_panel('rows = read_rows(big_file)\niran = (r for r in rows if r[0] == "IR")\n'
                          'amounts = (int(r[1]) for r in iran)\nsum(amounts)   # 260', font_size=26).to_edge(UP, buff=1.0)

        def stage(t, c, x):
            r = RoundedRectangle(corner_radius=0.15, width=2.5, height=1.0, stroke_color=c, fill_color=c, fill_opacity=0.1)
            return VGroup(r, mono(t, 22, color=c).move_to(r)).move_to([x, -1.2, 0])
        stages = VGroup(stage("read_rows", C_BLUE, -4.5), stage('if "IR"', C_GOLD, -1.5), stage("int(r[1])", C_TEAL, 1.5),
                        stage("sum", C_GREEN, 4.5))
        links = VGroup(*[Arrow(stages[i].get_right(), stages[i + 1].get_left(), buff=0.1, color=GREY_B) for i in range(3)])
        with self.say("Chain generators and you get a pipeline. Each stage pulls one item from the stage before it, "
                      "so a row travels all the way through before the next is even read. The file could be "
                      "gigabytes; memory use stays tiny."):
            self.play(FadeIn(code))
            self.play(LaggedStart(*[FadeIn(s) for s in stages], lag_ratio=0.2), Create(links))
            total = mono("0", 28, color=C_GREEN).next_to(stages[3], DOWN, buff=0.4)
            self.play(FadeIn(total))
            acc = 0
            for row in [("IR", 120), ("DE", 95), ("IR", 140)]:
                tok = pill(f"{row[0]},{row[1]}", C_BLUE, 20).next_to(stages[0], DOWN, buff=0.4)
                self.play(FadeIn(tok), run_time=0.3)
                self.play(tok.animate.next_to(stages[1], DOWN, buff=0.4), run_time=0.5)
                if row[0] != "IR":
                    self.play(tok.animate.set_opacity(0).shift(DOWN * 0.5), run_time=0.4)
                    continue
                num = pill(str(row[1]), C_TEAL, 20).next_to(stages[2], DOWN, buff=0.4)
                self.play(ReplacementTransform(tok, num), run_time=0.5)
                acc += row[1]
                self.play(FadeOut(num, target_position=total), Transform(total, mono(str(acc), 28, color=C_GREEN).move_to(total)),
                          run_time=0.5)
        with self.say("One catch: a generator can be consumed only once. Iterate it a second time and it's simply "
                      "empty."):
            once = mono("list(squares) -> [0, 1, 4, 9]\nlist(squares) -> []", 26, color=C_GREY).to_edge(DOWN, buff=0.5)
            self.play(FadeIn(once))
        self.clear(keep=[h])
        self.h = h

    def itertools_(self):
        h = self.swap_heading(self.h, "itertools highlights")
        rows = [("chain([1, 2], (3, 4))", "1 2 3 4"), ("islice(count(10, 5), 3)", "10 15 20"),
                ("accumulate([1, 2, 3, 4])", "1 3 6 10"), ("pairwise('abc')", "ab bc"),
                ("product('ab', [0, 1])", "a0 a1 b0 b1"), ("combinations('abc', 2)", "ab ac bc"),
                ("groupby('aaabccd')", "a:3 b:1 c:2 d:1")]
        g = VGroup(*[VGroup(mono(a, 26), mono(b, 26, color=C_YELLOW)) for a, b in rows])
        for r in g:
            r[1].move_to([2.2, 0, 0], aligned_edge=LEFT)
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(DOWN * 0.2)
        for r in g:
            r[1].set_x(2.0, LEFT)
        with self.say("The itertools module is a toolbox of lazy building blocks: chain joins iterables, islice "
                      "slices any iterator, accumulate gives running totals, pairwise yields neighbours, product and "
                      "combinations enumerate choices, and groupby groups consecutive equal items."):
            self.play(LaggedStart(*[FadeIn(r, shift=0.2 * RIGHT) for r in g], lag_ratio=0.3), run_time=3.5)
        self.clear()
