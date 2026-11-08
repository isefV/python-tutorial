from lesson import *


class L07Loops(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 7, "loops", "Loops", "Python"

    def construct(self):
        self.intro("Lesson seven: loops. Python has no C-style for loop with an index, a test and an "
                   "increment. A for loop walks over the items of any iterable, and a few helpers cover the "
                   "cases where you used to need the index.", r"\texttt{for}, \texttt{range}, \texttt{enumerate}, "
                   r"\texttt{zip}, \texttt{while}, \texttt{else}")
        self.for_items()
        self.enum_zip()
        self.while_loop()
        self.loop_else()
        self.outro([r"\texttt{for x in iterable}: loop over items, not indices.",
                    r"\texttt{range}, \texttt{enumerate} and \texttt{zip} replace index arithmetic.",
                    r"\texttt{break} leaves the loop, \texttt{continue} skips to the next item.",
                    r"A loop's \texttt{else} runs only if the loop did not \texttt{break}."],
                   "Loop over the items themselves, use range, enumerate and zip when you need numbers or "
                   "pairs, and remember that a loop's else means no break happened.")

    def for_items(self):
        h = self.heading("for walks over items")
        cstyle = mono("for (int i = 0; i < n; i++)", 30, color=C_GREY).move_to(UP * 2.0)
        code = code_panel("for x in [10, 20, 30]:\n    print(x)", font_size=30).move_to(LEFT * 3.2 + DOWN * 0.2)
        row = list_obj([10, 20, 30], w=1.0).move_to(RIGHT * 3.0 + UP * 0.3)
        con = Console(width=3.4, height=2.2).move_to(RIGHT * 3.0 + DOWN * 2.0)
        with self.say("Forget the index, the test and the increment. You write for x in a list, and x "
                      "takes each item in turn."):
            self.play(FadeIn(cstyle))
            self.play(Create(Cross(cstyle, stroke_color=C_BAD, stroke_width=5)))
            self.play(FadeIn(code), FadeIn(row), FadeIn(con))
            tag = name_tag("x").next_to(row[0][0], DOWN, buff=0.35)
            self.play(FadeIn(tag))
            for i in range(3):
                if i:
                    self.play(tag.animate.next_to(row[0][i], DOWN, buff=0.35), run_time=0.6)
                self.play(Indicate(row[0][i], color=C_YELLOW), con.print(str((i + 1) * 10)), run_time=0.7)
        with self.say("When you really want numbers, range produces them: range of five is zero to four, "
                      "and range takes a start, a stop that is excluded, and a step."):
            r1 = mono("range(5)          -> 0 1 2 3 4", 28).move_to(LEFT * 2.6 + DOWN * 2.2)
            r2 = mono("range(10, 0, -3)  -> 10 7 4 1", 28).next_to(r1, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(FadeIn(r1, shift=0.2 * UP))
            self.play(FadeIn(r2, shift=0.2 * UP))
        self.clear(keep=[h])
        self.h = h

    def enum_zip(self):
        h = self.swap_heading(self.h, "enumerate and zip")
        names = list_obj(['"ann"', '"bob"', '"cy"'], w=1.3, h=0.8, size=26, label="names").move_to(RIGHT * 2.2 + DOWN * 0.1)
        ages = list_obj([31, 25, 19], w=1.3, h=0.8, size=26, label="ages", color=C_GOLD).move_to(RIGHT * 2.2 + DOWN * 2.5)
        code = code_panel("for i, name in enumerate(names, start=1):\n    ...\nfor name, age in zip(names, ages):\n    ...",
                          font_size=24).to_edge(UP, buff=1.0)
        with self.say("Need a counter as well? enumerate yields index, item pairs, and you can choose "
                      "where counting starts."):
            self.play(FadeIn(code), FadeIn(names))
            mk = Marker(code)
            self.play(mk.to(0))
            nums = VGroup(*[mono(str(i + 1), 26, color=C_GREEN).next_to(c, DOWN, buff=0.15)
                            for i, c in enumerate(names[0])])
            self.play(LaggedStart(*[FadeIn(n, scale=0.5) for n in nums], lag_ratio=0.3))
        with self.say("zip walks several iterables in parallel and stops at the shortest. "
                      "And for a dict, items gives you each key with its value."):
            self.play(mk.to(2), FadeOut(nums), FadeIn(ages))
            pairs = VGroup(*[Line(a.get_bottom(), b.get_top(), color=C_YELLOW, stroke_width=3)
                             for a, b in zip(names[0], ages[0])])
            self.play(LaggedStart(*[Create(p) for p in pairs], lag_ratio=0.3))
            tups = VGroup(*[mono(t, 24, color=C_YELLOW) for t in ["('ann', 31)", "('bob', 25)", "('cy', 19)"]])
            tups.arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT, buff=0.8).shift(DOWN * 1.3)
            self.play(LaggedStart(*[FadeIn(t, shift=0.2 * RIGHT) for t in tups], lag_ratio=0.3))
            d = mono("for key, value in config.items(): ...", 24, color=C_GREY).to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.8)
            self.play(FadeIn(d))
        self.clear(keep=[h])
        self.h = h

    def while_loop(self):
        h = self.swap_heading(self.h, "while, break and continue")
        code = code_panel('while queue:\n    item = queue.pop(0)\n    if item is None:\n        continue\n'
                          '    if item == "STOP":\n        break\n    print("processing", item)',
                          font_size=26).to_edge(LEFT, buff=0.5)
        mk = Marker(code)
        vals = ['"a"', "None", '"b"', '"STOP"', '"c"']
        q = list_obj(vals, w=1.15, h=0.75, size=24, label="queue").move_to(RIGHT * 3.4 + UP * 1.6)
        con = Console(width=4.6, height=1.9).move_to(RIGHT * 3.4 + DOWN * 1.4)
        with self.say("while repeats as long as its condition is truthy; a non-empty list counts as true. "
                      "continue jumps straight to the next round, skipping the rest of the body."):
            self.play(FadeIn(code), FadeIn(q), FadeIn(con), mk.to(0))
            for k, v in enumerate(vals[:3]):
                it = q[0][k]
                self.play(mk.to(1), it.animate.shift(DOWN * 1.1), run_time=0.6)
                if v == "None":
                    self.play(mk.to(2, 3, color=C_GOLD), it.animate.set_color(C_GOLD), run_time=0.6)
                    self.play(FadeOut(it), run_time=0.4)
                else:
                    self.play(mk.to(6, color=C_GREEN), con.print(f"processing {v[1:-1]}"), run_time=0.6)
                    self.play(FadeOut(it), run_time=0.4)
        with self.say("break leaves the loop immediately. When STOP comes off the queue, the loop ends, "
                      "and the last item is never processed."):
            it = q[0][3]
            self.play(mk.to(1), it.animate.shift(DOWN * 1.1), run_time=0.6)
            self.play(mk.to(4, 5, color=C_BAD), it.animate.set_color(C_BAD))
            self.play(Circumscribe(q[0][4], color=C_GREY), Flash(it, color=C_BAD))
        self.clear(keep=[h])
        self.h = h

    def loop_else(self):
        h = self.swap_heading(self.h, "else on a loop")
        code = code_panel('for n in numbers:\n    if n % 2 == 0:\n        print("found", n)\n        break\n'
                          'else:\n    print("no even number")', font_size=26).to_edge(LEFT, buff=0.5)
        mk = Marker(code)
        with self.say("Loops can have an else clause. It runs when the loop finishes normally, without a "
                      "break, which is exactly the 'searched everything and found nothing' case."):
            self.play(FadeIn(code))
            for vals, hit in [([3, 5, 8, 9], 2), ([3, 5, 7], None)]:
                row = list_obj(vals, w=0.9).move_to(RIGHT * 3.4 + UP * 1.0)
                self.play(FadeIn(row))
                for i, v in enumerate(vals):
                    ok = i == hit
                    self.play(Indicate(row[0][i], color=C_GREEN if ok else C_GREY), mk.to(1), run_time=0.45)
                    if ok:
                        res = mono(f"found {v}", 28, color=C_GREEN).move_to(RIGHT * 3.4 + DOWN * 0.8)
                        self.play(mk.to(2, 3, color=C_GREEN), FadeIn(res))
                        break
                else:
                    res = mono("no even number", 28, color=C_GOLD).move_to(RIGHT * 3.4 + DOWN * 0.8)
                    self.play(mk.to(4, 5, color=C_GOLD), FadeIn(res))
                self.wait(0.8)
                self.play(FadeOut(row), FadeOut(res))
        with self.say("One more habit: never remove items from a list while looping over it. "
                      "Build a new list instead, usually with a comprehension, which is the next lesson."):
            safe = code_panel("nums = [n for n in nums if n % 2]", font_size=28).to_edge(DOWN, buff=0.6).to_edge(RIGHT, buff=0.5)
            self.play(FadeIn(safe, shift=0.2 * UP))
        self.clear()
