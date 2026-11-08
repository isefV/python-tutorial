from lesson import *


class L20NumpyIndexing(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 20, "numpy-indexing", "Indexing, slicing and masks", "NumPy"

    def construct(self):
        self.intro("Lesson twenty: indexing NumPy arrays. You'll select rows, columns, blocks, and anything that "
                   "matches a condition, and you need to know which selections share memory with the original.",
                   r"\texttt{[row, col]}, slices, boolean masks, fancy indexing, views")
        self.grid = grid_of(range(12), 3, 4, w=0.85, size=28).move_to(LEFT * 3.2 + DOWN * 0.3)
        self.basic()
        self.masks()
        self.fancy()
        self.views()
        self.outro([r"\texttt{a[r, c]}, \texttt{a[r]}, \texttt{a[:, c]}, \texttt{a[1:, ::2]}: one bracket, all axes.",
                    r"Masks select by condition; combine with \texttt{\&}, \texttt{|}, \texttt{\~} and parentheses.",
                    r"Fancy indexing takes lists of indices; \texttt{np.where} picks element-wise.",
                    r"Slices are \emph{views}; masks and fancy indexing return \emph{copies}."],
                   "One bracket indexes every axis, masks select by condition, index lists pick arbitrary "
                   "elements, and only basic slices share memory with the original.")

    def show(self, src, target, result, color=C_YELLOW):
        c = code_panel(src, font_size=30).move_to(RIGHT * 3.4 + UP * 1.4)
        parts = target if isinstance(target, list) else [target]
        box = VGroup(*[SurroundingRectangle(t, color=color, buff=0.04, stroke_width=5) for t in parts])
        r = mono(result, 28, color=color).next_to(c, DOWN, buff=0.4)
        self.play(FadeIn(c), Create(box))
        self.play(Write(r))
        return VGroup(c, box, r)

    def basic(self):
        h = self.heading("Basic indexing and slicing")
        g = self.grid
        axes = VGroup(mono("rows", 22, color=C_GREY).next_to(g, LEFT, buff=0.25),
                      mono("columns", 22, color=C_GREY).next_to(g, UP, buff=0.2))
        with self.say("Index a two-dimensional array with one pair of brackets: row, then column. a of one, two "
                      "is the element in row one, column two."):
            self.play(LaggedStart(*[FadeIn(c) for c in g], lag_ratio=0.04), FadeIn(axes))
            shown = self.show("a[1, 2]", g[6], "-> 6")
        with self.say("Leave out the column to get a whole row. A colon means everything along that axis, so a of "
                      "colon, two is column two. Slices with steps work on every axis at once."):
            for src, tgt, res in [("a[1]", VGroup(*g[4:8]), "-> [4 5 6 7]"),
                                  ("a[:, 2]", VGroup(g[2], g[6], g[10]), "-> [ 2  6 10]"),
                                  ("a[1:, ::2]", [g[4], g[6], g[8], g[10]], "-> [[ 4  6]\n    [ 8 10]]")]:
                self.play(FadeOut(shown))
                shown = self.show(src, tgt, res)
                self.wait(0.6)
            self.play(FadeOut(shown))
        self.h = h
        self.axes = axes

    def masks(self):
        h = self.swap_heading(self.h, "Boolean masks")
        g = self.grid
        c = code_panel("mask = a % 2 == 0\na[mask]", font_size=30).move_to(RIGHT * 3.4 + UP * 1.6)
        mk = Marker(c)
        with self.say("A comparison on an array gives an array of booleans, the same shape: a mask. Indexing with "
                      "the mask keeps exactly the True positions, and returns them as a flat copy."):
            self.play(FadeIn(c), mk.to(0))
            overlays = VGroup()
            for i, cl in enumerate(g):
                even = i % 2 == 0
                o = Rectangle(width=cl.width, height=cl.height, stroke_width=0, fill_opacity=0.5,
                              fill_color=C_GREEN if even else C_RED).move_to(cl)
                overlays.add(o)
            self.play(LaggedStart(*[FadeIn(o) for o in overlays], lag_ratio=0.05), run_time=1.5)
            self.play(mk.to(1))
            picked = VGroup(*[cell(i, w=0.7, h=0.7, color=C_GREEN, size=24) for i in range(0, 12, 2)]).arrange(RIGHT, buff=0)
            picked.move_to(RIGHT * 3.4 + DOWN * 0.2)
            self.play(LaggedStart(*[TransformFromCopy(g[i], picked[i // 2]) for i in range(0, 12, 2)], lag_ratio=0.12), run_time=1.8)
        more = VGroup(mono("a[(a > 2) & (a < 6)]", 26), mono("np.where(a > 5, a, 0)", 26), mono("a[a > 9] = -1", 26))
        more.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.4 + DOWN * 2.2)
        with self.say("Combine conditions with ampersand and bar, not and and or, and wrap each condition in "
                      "parentheses. np dot where picks from two options element by element, and a mask on the left "
                      "of an assignment changes only the matching elements."):
            self.play(LaggedStart(*[FadeIn(m, shift=0.2 * UP) for m in more], lag_ratio=0.4), run_time=2)
        self.play(FadeOut(c), FadeOut(mk.mob), FadeOut(overlays), FadeOut(picked), FadeOut(more))
        self.h = h

    def fancy(self):
        h = self.swap_heading(self.h, "Fancy indexing")
        g = self.grid
        with self.say("You can also index with lists of positions. A list of row numbers picks those rows, in that "
                      "order. Two lists pair up: rows zero and two, with columns one and three, gives two single "
                      "elements."):
            shown = self.show("a[[0, 2]]", [VGroup(*g[0:4]), VGroup(*g[8:12])], "-> rows 0 and 2")
            self.wait(0.8)
            self.play(FadeOut(shown))
            shown = self.show("a[[0, 2], [1, 3]]", [g[1], g[11]], "-> [ 1 11]")
        with self.say("A common use is sorting by another array: argsort returns the positions that would sort it, "
                      "and indexing with them reorders the values."):
            self.play(FadeOut(shown))
            c = mono("values[np.argsort(values)]  -> [10 20 30]", 26, color=C_YELLOW).move_to(RIGHT * 2.6 + UP * 1.4)
            c.to_edge(RIGHT, buff=0.4)
            self.play(FadeIn(c))
            self.wait(0.5)
            self.play(FadeOut(c))
        self.h = h

    def views(self):
        h = self.swap_heading(self.h, "Views versus copies")
        g = self.grid
        code = code_panel("row = a[0]\nrow[0] = 99\na[0, 0]   # 99 !\n\npicked = a[a > 5]\npicked[:] = 0\na.max()   # 11",
                          font_size=26).move_to(RIGHT * 3.4 + DOWN * 0.2)
        mk = Marker(code)
        with self.say("Here's the subtle part. A basic slice is a view: a window onto the same memory. Change the "
                      "view and the original array changes too."):
            self.play(FadeIn(code), mk.to(0))
            view = SurroundingRectangle(VGroup(*g[0:4]), color=C_GOLD, buff=0.04, stroke_width=5)
            vl = mono("view", 22, color=C_GOLD).next_to(view, UP, buff=0.1)
            self.play(Create(view), FadeIn(vl), FadeOut(self.axes))
            self.play(mk.to(1))
            n = cell(99, w=0.85, h=0.85, color=C_RED, size=26, fill_opacity=0.35).move_to(g[0])
            self.play(Transform(g[0], n), Flash(g[0], color=C_RED))
            self.play(mk.to(2, color=C_RED))
        with self.say("Masks and fancy indexing always build a new array, so changing the result leaves the "
                      "original alone. When you need an independent piece of a slice, call dot copy."):
            self.play(mk.to(4, 5, color=C_GREEN))
            cp = VGroup(*[cell(0, w=0.6, h=0.6, color=C_GREEN, size=22) for _ in range(6)]).arrange(RIGHT, buff=0)
            cp.next_to(g, DOWN, buff=0.6)
            cl = mono("copy", 22, color=C_GREEN).next_to(cp, LEFT, buff=0.2)
            self.play(FadeIn(cp), FadeIn(cl))
            self.play(mk.to(6, color=C_GREEN), Indicate(g[11], color=C_GREEN))
        self.clear()
