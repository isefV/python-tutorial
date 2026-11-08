from lesson import *


class L04Collections(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 4, "collections", "Built-in collections", "Python"

    def construct(self):
        self.intro("Lesson four: the built-in collections. Four types cover almost everything: list, tuple, "
                   "dict and set. Knowing which one to reach for is half of writing good Python.",
                   r"list, tuple, dict, set and the \texttt{collections} module")
        self.overview()
        self.lists()
        self.dicts()
        self.sets()
        self.extras()
        self.outro([r"\texttt{list}: dynamic array; \texttt{tuple}: immutable record, hashable.",
                    r"\texttt{dict}: hash map with O(1) lookup, keeps insertion order.",
                    r"\texttt{set}: unique items, fast membership, set algebra.",
                    r"\texttt{Counter}, \texttt{defaultdict}, \texttt{deque} for the common special cases."],
                   "Lists for sequences you change, tuples for fixed records, dicts for lookup by key, sets "
                   "for uniqueness, and the collections module for counting, grouping and queues.")

    def overview(self):
        h = self.heading("Four collections")
        rows = [["type", "literal", "mutable", "ordered"],
                ["list", "[1, 2]", "yes", "yes"],
                ["tuple", "(1, 2)", "no", "yes"],
                ["dict", '{"k": 1}', "yes", "insertion"],
                ["set", "{1, 2}", "yes", "no"]]
        t = table_grid(rows, [1.8, 2.4, 1.8, 2.2], row_h=0.75, size=28).move_to(DOWN * 0.2)
        with self.say("Here they are side by side. Lists and tuples are ordered sequences; the difference is "
                      "that a tuple can't be changed. A dict maps keys to values and remembers insertion order. "
                      "A set holds unique items with no order at all."):
            self.play(FadeIn(t[0]))
            self.play(LaggedStart(*[FadeIn(r, shift=0.2 * RIGHT) for r in t[1:]], lag_ratio=0.4), run_time=2.5)
            self.play(Circumscribe(t[2][2], color=C_YELLOW))
        self.clear(keep=[h])
        self.h = h

    def lists(self):
        h = self.swap_heading(self.h, "list: a dynamic array")
        code = code_panel("xs = [3, 1, 4]\nxs.append(1)\nxs.extend([5, 9])\nxs.insert(0, 2)\n"
                          "last = xs.pop()\nxs.remove(4)", font_size=28).to_edge(LEFT, buff=0.6).shift(UP * 0.4)
        mk = Marker(code)
        W = 0.75

        def row(vals, color=C_OBJ):
            return VGroup(*[cell(v, w=W, h=W, color=color) for v in vals]).arrange(RIGHT, buff=0)
        anchor = RIGHT * 0.9 + UP * 0.4
        r = row([3, 1, 4]).move_to(anchor, aligned_edge=LEFT)
        with self.say("A list is a dynamic array of references. append adds one item at the end, "
                      "extend adds every item of another iterable, and insert puts an item at any position."):
            self.play(FadeIn(code), mk.to(0), FadeIn(r))
            self.play(mk.to(1))
            c = cell(1, w=W, h=W, color=C_NEW).next_to(r, RIGHT, buff=0)
            self.play(GrowFromEdge(c, LEFT)); r.add(c)
            self.play(mk.to(2))
            cs = VGroup(cell(5, w=W, h=W, color=C_NEW), cell(9, w=W, h=W, color=C_NEW)).arrange(RIGHT, buff=0)
            cs.next_to(r, RIGHT, buff=0)
            self.play(FadeIn(cs, shift=0.3 * LEFT)); r.add(*cs)
            self.play(mk.to(3))
            c0 = cell(2, w=W, h=W, color=C_NEW)
            self.play(r.animate.shift(RIGHT * W))
            c0.next_to(r, LEFT, buff=0)
            self.play(FadeIn(c0, shift=0.3 * DOWN))
            r.submobjects.insert(0, c0)
        with self.say("pop removes and returns the last item, and remove deletes the first occurrence of a "
                      "value. Appending and popping at the end are fast; inserting at the front must shift "
                      "everything."):
            self.play(mk.to(4))
            out = r[-1]
            self.play(out.animate.shift(DOWN * 1.4).set_color(C_GOLD))
            lab = mono("last", 24, color=C_GOLD).next_to(out, LEFT, buff=0.2)
            self.play(FadeIn(lab))
            r.remove(out)
            self.play(mk.to(5))
            four = r[3]
            self.play(four.animate.set_color(C_BAD))
            self.play(FadeOut(four, shift=UP * 0.5))
            r.remove(four)
            self.play(r[3:].animate.shift(LEFT * W))
            sl = mono("sorted(xs) returns a new list;  xs.sort() sorts in place", 24, color=C_GREY)
            sl.to_edge(DOWN, buff=0.6)
            self.play(FadeIn(sl))
        self.clear(keep=[h])
        self.h = h

    def dicts(self):
        h = self.swap_heading(self.h, "dict: a hash map")
        code = code_panel('d = {"a": 1}\nd["b"] = 2\nd.get("z", 0)\nfor k, v in d.items(): ...',
                          font_size=26).to_edge(LEFT, buff=0.6).shift(UP * 0.8)
        mk = Marker(code)
        slots = VGroup(*[Rectangle(width=3.2, height=0.6, stroke_color=GREY_D, stroke_width=1.5,
                                   fill_color=CODE_BG, fill_opacity=1) for _ in range(6)]).arrange(DOWN, buff=0)
        slots.move_to(RIGHT * 4.3 + DOWN * 0.2)
        idx = VGroup(*[mono(str(i), 18, color=C_GREY).next_to(s, LEFT, buff=0.15) for i, s in enumerate(slots)])

        def put(key, val, i):
            e = mono(f'"{key}": {val}', 26).move_to(slots[i])
            return e
        with self.say("A dict is a hash table. The key is hashed, and the hash picks a slot, so lookup, "
                      "insert and delete are constant time on average. That's why keys must be hashable: "
                      "strings, numbers, tuples, but not lists."):
            self.play(FadeIn(code), FadeIn(slots), FadeIn(idx), mk.to(0))
            for key, val, i, line in [("a", 1, 4, 0), ("b", 2, 1, 1)]:
                if line:
                    self.play(mk.to(line))
                k = pill(f'"{key}"', C_NAME, 24).move_to(RIGHT * 0.6 + DOWN * 1.8)
                hs = mono(f"hash -> {i}", 24, color=C_GREY).next_to(k, DOWN, buff=0.25)
                self.play(FadeIn(k), FadeIn(hs))
                e = put(key, val, i)
                self.play(ReplacementTransform(k, e), FadeOut(hs), slots[i].animate.set_stroke(C_BLUE, 2.5))
        with self.say("get returns a default instead of raising a key error when the key is missing, "
                      "and items gives you key, value pairs to loop over."):
            self.play(mk.to(2))
            z = mono("0", 28, color=C_YELLOW).next_to(code, DOWN, buff=0.4, aligned_edge=LEFT)
            self.play(FadeIn(z))
            self.play(mk.to(3))
        self.clear(keep=[h])
        self.h = h

    def sets(self):
        h = self.swap_heading(self.h, "set: unique items")
        A = Circle(1.8, color=C_BLUE, fill_opacity=0.12).move_to(LEFT * 3.3 + DOWN * 0.1)
        B = Circle(1.8, color=C_GOLD, fill_opacity=0.12).move_to(LEFT * 1.1 + DOWN * 0.1)
        la = mono("a = {1, 2, 3}", 28, color=C_BLUE).next_to(A, UP, buff=0.2).shift(LEFT * 1.3)
        lb = mono("b = {2, 3, 4}", 28, color=C_GOLD).next_to(B, UP, buff=0.2).shift(RIGHT * 1.3)
        n1 = mono("1", 34).move_to(LEFT * 4.2 + DOWN * 0.1)
        n23 = VGroup(mono("2", 34), mono("3", 34)).arrange(DOWN, buff=0.5).move_to(LEFT * 2.2 + DOWN * 0.1)
        n4 = mono("4", 34).move_to(RIGHT * 0.0 + DOWN * 0.1)
        res = VGroup(mono("a | b  ->  {1, 2, 3, 4}", 26), mono("a & b  ->  {2, 3}", 26),
                     mono("a - b  ->  {1}", 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        res.to_edge(RIGHT, buff=0.8).shift(DOWN * 0.1)
        with self.say("A set stores each item once, with fast membership tests, and supports real set "
                      "algebra: union, intersection and difference, written with bar, ampersand and minus. "
                      "Wrapping a list in set is the quickest way to drop duplicates."):
            self.play(Create(A), Create(B), FadeIn(la), FadeIn(lb))
            self.play(FadeIn(n1), FadeIn(n23), FadeIn(n4))
            self.play(A.animate.set_fill(C_BLUE, 0.35), B.animate.set_fill(C_GOLD, 0.35), FadeIn(res[0]))
            self.play(A.animate.set_fill(opacity=0.05), B.animate.set_fill(opacity=0.05))
            lens = Intersection(A, B, color=C_GREEN, fill_opacity=0.45, stroke_width=0)
            self.play(FadeIn(lens), FadeIn(res[1]))
            diff = Difference(A, B, color=C_BLUE, fill_opacity=0.45, stroke_width=0)
            self.play(FadeOut(lens), FadeIn(diff), FadeIn(res[2]))
            note = mono("{} is an empty dict;  use set()", 24, color=C_GREY).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(note))
        self.clear(keep=[h])
        self.h = h

    def extras(self):
        h = self.swap_heading(self.h, "The collections module")
        code = code_panel('Counter("mississippi").most_common(2)\n\ngroups = defaultdict(list)\n'
                          'groups[w[0]].append(w)\n\nrecent = deque(maxlen=3)', font_size=24)
        code.to_edge(LEFT, buff=0.5)
        mk = Marker(code)
        with self.say("The standard library adds a few specialised containers. Counter counts things. "
                      "defaultdict creates a missing value on first access, which makes grouping a one-liner. "
                      "And deque, with a max length, keeps only the last few items."):
            self.play(FadeIn(code), mk.to(0))
            c = mono("[('i', 4), ('s', 4)]", 26, color=C_YELLOW).move_to(RIGHT * 3.6 + UP * 1.6)
            self.play(FadeIn(c))
            self.play(mk.to(2, 3))
            g = mono("{'a': ['apple', 'avocado'],\n 'b': ['banana']}", 24, color=C_YELLOW).move_to(RIGHT * 3.6 + UP * 0.1)
            self.play(FadeIn(g))
            self.play(mk.to(5))
            W = 0.7
            boxes = VGroup(*[Square(W, stroke_color=C_BLUE, stroke_width=2) for _ in range(3)]).arrange(RIGHT, buff=0)
            boxes.move_to(RIGHT * 3.6 + DOWN * 1.8)
            self.play(Create(boxes))
            items = []
            for i in range(5):
                it = mono(str(i), 28).move_to(boxes[2])
                anims = [FadeIn(it, shift=LEFT * 1.0)]
                if len(items) == 3:
                    anims.append(FadeOut(items.pop(0), shift=LEFT * 0.8))
                anims += [o.animate.shift(LEFT * W) for o in items]
                self.play(*anims, run_time=0.5)
                items.append(it)
        self.clear()
