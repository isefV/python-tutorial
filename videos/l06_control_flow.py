from lesson import *


class L06ControlFlow(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 6, "control-flow", "Control flow: if and match", "Python"

    def construct(self):
        self.intro("Lesson six: control flow. Python has if, elif and else, a one-line conditional "
                   "expression, and since version three point ten, structural pattern matching with match.",
                   r"\texttt{if} / \texttt{elif} / \texttt{else}, conditional expressions, \texttt{match}")
        self.if_chain()
        self.ternary()
        self.match_seq()
        self.match_shapes()
        self.outro([r"No parentheses, no braces: a condition, a colon, an indented block.",
                    r"\texttt{x if cond else y} is an expression; \texttt{pass} is an empty block.",
                    r"\texttt{match} destructures: capture names, \texttt{|} alternatives, guards, \texttt{\_}.",
                    r"Patterns also match dict keys and class attributes."],
                   "If statements need no parentheses, the conditional expression picks a value, and match "
                   "checks the shape of data and pulls out the pieces in one step.")

    def if_chain(self):
        h = self.heading("if / elif / else")
        code = code_panel('score = 82\nif score >= 90:\n    grade = "A"\nelif score >= 75:\n    grade = "B"\n'
                          'else:\n    grade = "C"', font_size=28).to_edge(LEFT, buff=0.6)
        mk = Marker(code)

        def node(txt, color):
            t = mono(txt, 26)
            b = RoundedRectangle(corner_radius=0.12, width=t.width + 0.5, height=0.8, stroke_color=color,
                                 fill_color=color, fill_opacity=0.12)
            return VGroup(b, t.move_to(b))
        c1 = node("score >= 90 ?", C_BLUE).move_to(RIGHT * 2.6 + UP * 2.0)
        c2 = node("score >= 75 ?", C_BLUE).move_to(RIGHT * 2.6 + UP * 0.0)
        gA = node('"A"', C_GREY).move_to(RIGHT * 5.4 + UP * 2.0)
        gB = node('"B"', C_GREY).move_to(RIGHT * 5.4 + UP * 0.0)
        gC = node('"C"', C_GREY).move_to(RIGHT * 2.6 + DOWN * 2.0)
        arrows = VGroup(Arrow(c1.get_right(), gA.get_left(), buff=0.1), Arrow(c2.get_right(), gB.get_left(), buff=0.1),
                        Arrow(c1.get_bottom(), c2.get_top(), buff=0.1), Arrow(c2.get_bottom(), gC.get_top(), buff=0.1))
        arrows.set_color(GREY_B)
        yes = VGroup(*[mono("yes", 18, color=C_GREEN).next_to(a, UP, buff=0.05) for a in arrows[:2]])
        no = VGroup(*[mono("no", 18, color=C_BAD).next_to(a, LEFT, buff=0.1) for a in arrows[2:]])
        with self.say("The condition needs no parentheses. A colon ends it, and the indented block below "
                      "runs when it's true. elif means else if, and the branches are tested top to bottom; "
                      "the first true one wins."):
            self.play(FadeIn(code))
            self.play(LaggedStart(FadeIn(c1), FadeIn(gA), FadeIn(c2), FadeIn(gB), FadeIn(gC), lag_ratio=0.2),
                      Create(arrows), FadeIn(yes), FadeIn(no), run_time=2)
        with self.say("Follow a score of eighty-two: not ninety or more, so on to the next test. "
                      "Seventy-five or more, yes, so the grade is B, and the else branch never runs."):
            dot = Dot(color=C_YELLOW, radius=0.14).move_to(c1.get_left() + LEFT * 0.4)
            self.play(mk.to(0), FadeIn(dot, scale=2))
            self.play(mk.to(1), dot.animate.move_to(c1.get_center()))
            self.play(Indicate(c1, color=C_BAD), run_time=0.8)
            self.play(mk.to(3), MoveAlongPath(dot, Line(c1.get_center(), c2.get_center())))
            self.play(Indicate(c2, color=C_GREEN), run_time=0.8)
            self.play(mk.to(4, color=C_GREEN), MoveAlongPath(dot, Line(c2.get_center(), gB.get_center())))
            self.play(gB[0].animate.set_stroke(C_GREEN).set_fill(C_GREEN, 0.3))
        self.clear(keep=[h])
        self.h = h

    def ternary(self):
        h = self.swap_heading(self.h, "The conditional expression")
        e = mono('status = "adult" if age >= 18 else "minor"', 34).move_to(UP * 0.8)
        with self.say("When you just need to choose a value, use the conditional expression: value if "
                      "condition else other value. It's an expression, so it fits anywhere a value does. "
                      "And when a block must exist but has nothing to do, write pass."):
            self.play(Write(e))
            parts = [(e[7:14], C_GREEN, "if true"), (e[16:23], C_BLUE, "condition"), (e[-7:], C_BAD, "if false")]
            labs = VGroup()
            for mob, col, txt in parts:
                br = Brace(mob, DOWN, color=col)
                labs.add(VGroup(br, tex(txt, 30, col).next_to(br, DOWN, buff=0.1)))
            self.play(LaggedStart(*[FadeIn(l, shift=0.2 * UP) for l in labs], lag_ratio=0.4))
            p = code_panel("if age < 0:\n    pass    # nothing to do yet", font_size=26).move_to(DOWN * 2.3)
            self.play(FadeIn(p))
        self.clear(keep=[h])
        self.h = h

    def match_seq(self):
        h = self.swap_heading(self.h, "match: sequence patterns")
        code = code_panel('match command.split():\n    case ["go", direction]:\n        return f"moving {direction}"\n'
                          '    case ["quit" | "exit"]:\n        return "bye"\n    case ["say", *words] if words:\n'
                          '        return " ".join(words)\n    case _:\n        return "unknown command"',
                          font_size=22).to_edge(LEFT, buff=0.4)
        mk = Marker(code)
        cases = [("go north", 1, 2, '"moving north"'), ("exit", 3, 4, '"bye"'),
                 ("say hello world", 5, 6, '"hello world"'), ("dance", 7, 8, '"unknown command"')]
        with self.say("match compares a value against patterns, top to bottom, and the first that fits wins. "
                      "There's no fall-through and no break. A pattern can capture names: a list of go and "
                      "something binds that something to direction."):
            self.play(FadeIn(code))
            cmd, i, j, res = cases[0]
            inp = mono(f'"{cmd}"', 30, color=C_YELLOW).move_to(RIGHT * 3.8 + UP * 2.2)
            lst = mono("['go', 'north']", 28).next_to(inp, DOWN, buff=0.4)
            self.play(FadeIn(inp), mk.to(0))
            self.play(TransformFromCopy(inp, lst))
            self.play(mk.to(i, j, color=C_GREEN))
            cap = mono("direction = 'north'", 26, color=C_GREEN).next_to(lst, DOWN, buff=0.5)
            self.play(FadeIn(cap, shift=0.2 * UP))
            out = mono("-> " + res, 28, color=C_YELLOW).next_to(cap, DOWN, buff=0.4)
            self.play(FadeIn(out))
        with self.say("A bar separates alternatives, star words captures the rest of the list, an if guard "
                      "adds a condition, and underscore is the wildcard that matches anything."):
            for cmd, i, j, res in cases[1:]:
                ni = mono(f'"{cmd}"', 30, color=C_YELLOW).move_to(inp)
                no = mono("-> " + res, 28, color=C_YELLOW).move_to(out)
                self.play(FadeOut(lst), FadeOut(cap), Transform(inp, ni), FadeOut(out), mk.to(i, j, color=C_GREEN))
                out = no
                self.play(FadeIn(out), run_time=0.8)
                self.wait(0.6)
        self.clear(keep=[h])
        self.h = h

    def match_shapes(self):
        h = self.swap_heading(self.h, "match: dict and class patterns")
        code = code_panel('match event:\n    case {"type": "click", "pos": (x, y)}:\n        ...\n'
                          '    case Point(x=0, y=0):\n        ...\n    case Point(x=x, y=y):\n        ...',
                          font_size=24).to_edge(LEFT, buff=0.5)
        mk = Marker(code)
        evs = [('{"type": "click", "pos": (3, 4)}', 1, "click at 3,4"), ("Point(0, 0)", 3, "origin"),
               ("Point(1, 2)", 5, "point 1,2")]
        with self.say("Patterns can look inside dicts and objects too. A mapping pattern checks keys and "
                      "unpacks nested values; a class pattern checks the type and its attributes, "
                      "with literals or with names to capture."):
            self.play(FadeIn(code))
            prev = None
            for ev, line, res in evs:
                e = mono(ev, 20, color=C_YELLOW).move_to(RIGHT * 4.0 + UP * 0.6)
                r = mono("-> " + res, 28, color=C_GREEN).move_to(RIGHT * 4.0 + DOWN * 0.5)
                anims = [mk.to(line, color=C_GREEN)]
                if prev:
                    anims += [FadeOut(prev[0]), FadeOut(prev[1])]
                self.play(FadeIn(e), *anims)
                self.play(FadeIn(r, shift=0.2 * UP))
                self.wait(0.5)
                prev = (e, r)
        self.clear()
