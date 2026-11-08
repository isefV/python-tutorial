from lesson import *


class L10Closures(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 10, "lambdas-closures-scope", "Lambdas, closures and scope", "Python"

    def construct(self):
        self.intro("Lesson ten: functions are objects. You can store them, pass them to other functions and "
                   "return them. That opens the door to lambdas and closures, and it makes scoping rules matter.",
                   r"lambdas, closures, LEGB, late binding")
        self.values()
        self.closures()
        self.legb()
        self.late_binding()
        self.outro([r"Functions are values: pass them as \texttt{key=}, store them, return them.",
                    r"A closure keeps the variables of the scope it was created in.",
                    r"Lookup order is LEGB; \texttt{nonlocal}/\texttt{global} allow rebinding.",
                    r"Closures read variables late; bind early with \texttt{lambda i=i: i}."],
                   "Functions are ordinary values, closures carry their environment with them, names are "
                   "looked up local, enclosing, global, built-in, and closures see a variable's final value.")

    def values(self):
        h = self.heading("Functions as values and lambdas")
        code = code_panel("people = [(\"bob\", 25), (\"ann\", 31), (\"cy\", 19)]\n"
                          "sorted(people, key=lambda p: p[1])", font_size=28).to_edge(UP, buff=1.1)
        rows = VGroup(*[mono(t, 30) for t in ["('bob', 25)", "('ann', 31)", "('cy', 19)"]]).arrange(DOWN, buff=0.3)
        rows.move_to(LEFT * 2.5 + DOWN * 1.2)
        with self.say("Here a function is passed as an argument. sorted calls the key function on every item "
                      "and sorts by what it returns. lambda p colon p of one is a small anonymous function: one "
                      "expression, returned automatically."):
            self.play(FadeIn(code), FadeIn(rows))
            lam = SurroundingRectangle(code.code_lines[1], color=C_GOLD, buff=0.05)
            self.play(Create(lam))
            keys = VGroup(*[mono(k, 30, color=C_GOLD).next_to(r, RIGHT, buff=0.8) for r, k in zip(rows, ["25", "31", "19"])])
            self.play(LaggedStart(*[TransformFromCopy(r[-3:-1], k) for r, k in zip(rows, keys)], lag_ratio=0.3))
            order = [2, 0, 1]
            self.play(*[VGroup(rows[o], keys[o]).animate.move_to(VGroup(rows[k], keys[k]).get_center() + RIGHT * 5.5)
                        for k, o in enumerate(order)], run_time=1.5)
        self.clear(keep=[h])
        self.h = h

    def closures(self):
        h = self.swap_heading(self.h, "Closures")
        code = code_panel("def make_counter():\n    count = 0\n    def inc():\n        nonlocal count\n"
                          "        count += 1\n        return count\n    return inc\n\nc1, c2 = make_counter(), make_counter()\n"
                          "c1(); c1(); c2()", font_size=22).to_edge(LEFT, buff=0.4)
        mk = Marker(code)

        def fn_box(name, color):
            b = RoundedRectangle(corner_radius=0.15, width=3.2, height=1.5, stroke_color=color, fill_color=color,
                                 fill_opacity=0.08)
            t = mono(f"{name}: inc", 22, color=color).move_to(b.get_top() + DOWN * 0.3)
            cellb = Rectangle(width=1.6, height=0.6, stroke_color=C_GOLD, fill_color=C_GOLD, fill_opacity=0.12)
            cellb.move_to(b.get_center() + DOWN * 0.25)
            v = mono("count = 0", 20).move_to(cellb)
            return VGroup(b, t, cellb, v)
        b1 = fn_box("c1", C_BLUE).move_to(RIGHT * 3.6 + UP * 1.3)
        b2 = fn_box("c2", C_TEAL).move_to(RIGHT * 3.6 + DOWN * 1.2)
        with self.say("make counter defines an inner function and returns it. The inner function remembers "
                      "count, even after make counter has finished. That captured environment is a closure. "
                      "nonlocal lets it rebind count instead of creating a new local."):
            self.play(FadeIn(code), mk.to(0, 6))
            self.play(mk.to(8))
            self.play(FadeIn(b1), FadeIn(b2))
            lab = tex("captured cell", 28, C_GOLD).next_to(b2, DOWN, buff=0.3)
            self.play(FadeIn(lab), Indicate(b1[2], color=C_GOLD), Indicate(b2[2], color=C_GOLD))
        with self.say("Each call to make counter creates a fresh cell. Calling c1 twice brings its count to two, "
                      "while c2 has its own count, which is one."):
            self.play(mk.to(9))
            for box, val in [(b1, 1), (b1, 2), (b2, 1)]:
                nv = mono(f"count = {val}", 20, color=C_YELLOW).move_to(box[3])
                self.play(Transform(box[3], nv), Indicate(box[2], color=C_GOLD), run_time=0.7)
        self.clear(keep=[h])
        self.h = h

    def legb(self):
        h = self.swap_heading(self.h, "Name lookup: LEGB")
        cols = [C_GREY, C_PURPLE, C_BLUE, C_GREEN]
        names = ["Built-in   (len, print, ...)", "Global   (module level)", "Enclosing   (outer function)", "Local   (this function)"]
        boxes = VGroup()
        for i, (n, c) in enumerate(zip(names, cols)):
            r = RoundedRectangle(corner_radius=0.2, width=11 - 2.2 * i, height=6.0 - 1.25 * i, stroke_color=c,
                                 fill_color=c, fill_opacity=0.06)
            t = Text(n, font_size=24, color=c).move_to(r.get_top() + DOWN * 0.35)
            boxes.add(VGroup(r, t))
        boxes.move_to(DOWN * 0.4)
        for b in boxes[1:]:
            b.move_to(boxes[0][0].get_center() + DOWN * 0.3 * 0)
        for i in range(1, 4):
            boxes[i].shift(DOWN * 0.32 * i)
        with self.say("When Python meets a name, it looks in four places in order: the local function, any "
                      "enclosing functions, the module's globals, and finally the built-ins. The first hit wins."):
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.3), run_time=2)
            dot = Dot(boxes[3][0].get_center() + DOWN * 0.1, color=C_YELLOW, radius=0.12)
            self.play(FadeIn(dot, scale=2))
            for i in [2, 1, 0]:
                self.play(dot.animate.move_to(boxes[i][0].get_bottom() + UP * 0.3 + RIGHT * 0.2 * (3 - i)), run_time=0.7)
        with self.say("Reading an outer name always works, but assigning to it creates a new local, unless you "
                      "declare it global or nonlocal. And note that blocks like if and for don't create a scope; "
                      "the loop variable is still alive after the loop."):
            note = mono("for i in range(3): pass\nprint(i)   # 2", 24, color=C_YELLOW).move_to(boxes[3][0])
            note.shift(DOWN * 0.2)
            self.play(FadeOut(dot), FadeIn(note))
        self.clear(keep=[h])
        self.h = h

    def late_binding(self):
        h = self.swap_heading(self.h, "Late binding in closures")
        bad = code_panel("funcs = [lambda: i for i in range(3)]\n[f() for f in funcs]   # [2, 2, 2]", font_size=28)
        good = code_panel("funcs = [lambda i=i: i for i in range(3)]\n[f() for f in funcs]   # [0, 1, 2]", font_size=28)
        VGroup(bad, good).arrange(DOWN, buff=1.4).move_to(LEFT * 0.0 + DOWN * 0.1)
        with self.say("A classic trap: three lambdas that each return i. They all return two. A closure looks up "
                      "the variable when it's called, not when it's created, and by then the loop has finished."):
            self.play(FadeIn(bad))
            self.play(Create(SurroundingRectangle(bad, color=C_BAD, buff=0.08)))
        with self.say("The fix binds the current value early, as a default argument. Map, filter and reduce exist "
                      "too, but a comprehension usually reads better."):
            self.play(FadeIn(good, shift=0.2 * UP))
            self.play(Create(SurroundingRectangle(good, color=C_GREEN, buff=0.08)))
        self.clear()
