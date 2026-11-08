from lesson import *


class L08Comprehensions(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 8, "comprehensions", "Comprehensions", "Python"

    def construct(self):
        self.intro("Lesson eight: comprehensions. A comprehension builds a whole list, set or dict in a "
                   "single expression. Once you can read their shape, you'll see them everywhere.",
                   r"list, set, dict and generator comprehensions")
        self.anatomy()
        self.flavours()
        self.generators()
        self.nested()
        self.outro([r"\texttt{[expr for x in it if cond]}: map and filter in one expression.",
                    r"Same shape: \texttt{\{...\}} for sets, \texttt{\{k: v ...\}} for dicts.",
                    r"\texttt{( ... )} is lazy: a generator that yields one value at a time.",
                    r"\texttt{a if c else b} chooses values; a trailing \texttt{if} filters items."],
                   "Read a comprehension as: this expression, for each item, if the condition holds. "
                   "Brackets make a list, braces a set or dict, and parentheses a lazy generator.")

    def anatomy(self):
        h = self.heading("Anatomy of a list comprehension")
        e = mono("[n * n  for n in nums  if n % 2 == 0]", 40).move_to(UP * 2.2)
        with self.say("Read it in three parts: the expression to produce, n times n; the loop, for n in nums; "
                      "and an optional filter, if n is even."):
            self.play(Write(e))
            parts = [(e[1:4], C_GOLD, "expression"), (e[4:14], C_BLUE, "loop"), (e[14:-1], C_GREEN, "filter")]
            labs = VGroup()
            for mob, col, txt in parts:
                br = Brace(mob, DOWN, color=col, buff=0.1)
                labs.add(VGroup(br, tex(txt, 32, col).next_to(br, DOWN, buff=0.1)))
                self.play(FadeIn(labs[-1], shift=0.2 * UP), run_time=0.8)
        nums = [3, 1, 4, 1, 5, 9, 2, 6]
        row = list_obj(nums, w=0.75, label="nums").move_to(DOWN * 0.6)
        with self.say("Watch it run over the list. Odd numbers fail the filter and are dropped. "
                      "Each survivor goes through the expression, and the results are collected into a new list."):
            self.play(FadeIn(row))
            keep = [i for i, v in enumerate(nums) if v % 2 == 0]
            self.play(*[row[0][i].animate.set_opacity(0.2) for i in range(len(nums)) if i not in keep],
                      *[Indicate(row[0][i], color=C_GREEN) for i in keep], run_time=1.2)
            out = list_obj([nums[i] ** 2 for i in keep], w=0.85, color=C_GOLD, label="result").move_to(DOWN * 2.5)
            for k, i in enumerate(keep):
                self.play(TransformFromCopy(row[0][i], out[0][k]), run_time=0.6)
            self.play(FadeIn(out[1]))
        self.clear(keep=[h])
        self.h = h

    def flavours(self):
        h = self.swap_heading(self.h, "Sets and dicts too")
        rows = VGroup(
            VGroup(mono("[n * n for n in nums]", 30), mono("list", 26, color=C_BLUE)),
            VGroup(mono("{n % 3 for n in nums}", 30), mono("set  -> {0, 1, 2}", 26, color=C_GREEN)),
            VGroup(mono('{w: len(w) for w in ["hi", "hey"]}', 30), mono("dict -> {'hi': 2, 'hey': 3}", 26, color=C_GOLD)),
        )
        for r in rows:
            r.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to(DOWN * 0.1)
        with self.say("The same shape works with other brackets. Curly braces with a single expression "
                      "build a set, so duplicates vanish. Curly braces with key colon value build a dict."):
            self.play(LaggedStart(*[FadeIn(r, shift=0.3 * RIGHT) for r in rows], lag_ratio=0.5), run_time=3)
        self.clear(keep=[h])
        self.h = h

    def generators(self):
        h = self.swap_heading(self.h, "Generator expressions are lazy")
        code = code_panel("sum(n * n for n in nums)\nany(n > 8 for n in nums)\n\nsquares = (n * n for n in nums)\n"
                          "next(squares)   # 9\nnext(squares)   # 1", font_size=26).to_edge(LEFT, buff=0.5)
        mk = Marker(code)
        with self.say("With parentheses you get a generator expression. No list is built at all; values are "
                      "produced one at a time, as they're asked for. That makes them ideal to feed straight "
                      "into sum, any or all, which can even stop early."):
            self.play(FadeIn(code), mk.to(0))
            self.play(mk.to(1))
        box = RoundedRectangle(corner_radius=0.2, width=3.0, height=1.6, stroke_color=C_TEAL,
                               fill_color=C_TEAL, fill_opacity=0.1).move_to(RIGHT * 3.4 + UP * 0.6)
        lab = mono("generator", 22, color=C_TEAL).next_to(box, UP, buff=0.1)
        with self.say("Think of it as a little machine with a cursor into the data. Each call to next "
                      "pulls exactly one value through it. Nothing is computed in advance."):
            self.play(mk.to(3), Create(box), FadeIn(lab))
            outs = VGroup()
            for k, v in enumerate([9, 1]):
                self.play(mk.to(4 + k))
                o = mono(str(v), 34, color=C_GOLD).move_to(box)
                self.play(FadeIn(o, scale=0.5), run_time=0.5)
                self.play(o.animate.move_to(RIGHT * (2.6 + 1.0 * k) + DOWN * 1.6), run_time=0.7)
                outs.add(o)
            wait = tex(r"the rest is not computed yet", 32, C_GREY).next_to(outs, DOWN, buff=0.5)
            wait.set_x(3.4)
            self.play(FadeIn(wait))
        self.clear(keep=[h])
        self.h = h

    def nested(self):
        h = self.swap_heading(self.h, "Conditional values and nesting")
        a = mono('["even" if n % 2 == 0 else "odd" for n in nums]', 28).move_to(UP * 1.8)
        a_out = mono("['odd', 'even', 'odd', 'even']", 26, color=C_YELLOW).next_to(a, DOWN, buff=0.3)
        b = mono("[v for row in matrix for v in row]", 28).move_to(DOWN * 0.3)
        b_out = mono("[1, 2, 3, 4, 5, 6]", 26, color=C_YELLOW).next_to(b, DOWN, buff=0.3)
        with self.say("Don't confuse the two ifs. An if else at the front chooses a value for every item; "
                      "an if at the end filters items out. Several for clauses nest in reading order, "
                      "outer loop first, which flattens a matrix."):
            self.play(FadeIn(a))
            self.play(FadeIn(a_out, shift=0.2 * DOWN))
            self.play(FadeIn(b))
            self.play(FadeIn(b_out, shift=0.2 * DOWN))
        with self.say("But once you need several statements, temporary variables or error handling, "
                      "write a normal loop. Readability wins."):
            tip = tex(r"Several steps per item? A plain \texttt{for} loop is clearer.", 34, C_GOLD).to_edge(DOWN, buff=0.8)
            self.play(FadeIn(tip, shift=0.2 * UP))
        self.clear()
