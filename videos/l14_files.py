from lesson import *


def file_icon(name, color=C_BLUE, w=1.4, h=1.7):
    body = Polygon([-w / 2, h / 2, 0], [w / 2 - 0.35, h / 2, 0], [w / 2, h / 2 - 0.35, 0], [w / 2, -h / 2, 0],
                   [-w / 2, -h / 2, 0], stroke_color=color, fill_color=color, fill_opacity=0.12, stroke_width=2.5)
    lab = mono(name, 18, color=color).next_to(body, DOWN, buff=0.12)
    return VGroup(body, lab)


class L14Files(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 14, "files-context-managers", "Files and context managers", "Python"

    def construct(self):
        self.intro("Lesson fourteen: files and context managers. Reading and writing files is easy in Python; "
                   "the important part is the with statement, which guarantees that resources are released.",
                   r"\texttt{open}, \texttt{pathlib}, JSON, CSV, your own context managers")
        self.with_open()
        self.pathlib()
        self.formats()
        self.own_cm()
        self.outro([r"Open files in a \texttt{with} block; pass an explicit \texttt{encoding}.",
                    r"\texttt{pathlib.Path}: join with \texttt{/}, read and write in one call.",
                    r"\texttt{json.dumps}/\texttt{loads} and \texttt{csv.DictReader}/\texttt{DictWriter}.",
                    r"\texttt{@contextmanager}: code before \texttt{yield} = enter, after = exit."],
                   "Always open files with with and an explicit encoding, prefer pathlib for paths, use the json "
                   "and csv modules for data, and write your own context managers for any setup and teardown.")

    def with_open(self):
        h = self.heading("with open(...)")
        code = code_panel('with open(path, "w", encoding="utf-8") as f:\n    f.write("first line\\n")\n'
                          '    f.write("second line\\n")\n\nwith open(path, encoding="utf-8") as f:\n'
                          '    for number, line in enumerate(f, start=1):\n        print(number, line.rstrip())',
                          font_size=22).to_edge(LEFT, buff=0.4).shift(UP * 0.6)
        mk = Marker(code)
        fi = file_icon("notes.txt").move_to(RIGHT * 4.6 + UP * 1.0)
        state = mono("closed", 24, color=C_GREY).next_to(fi, DOWN, buff=0.5)
        with self.say("open returns a file object, and the with statement makes sure it gets closed when the "
                      "block ends, whether it ends normally or with an exception. Always pass an encoding; "
                      "the default depends on the operating system."):
            self.play(FadeIn(code), FadeIn(fi), FadeIn(state))
            self.play(mk.to(0))
            self.play(Transform(state, mono("open  (mode 'w')", 24, color=C_GREEN).move_to(state)),
                      fi[0].animate.set_stroke(C_GREEN))
            lines = VGroup(*[Line(LEFT * 0.45, RIGHT * 0.45, stroke_width=3, color=WHITE) for _ in range(2)])
            lines.arrange(DOWN, buff=0.22).move_to(fi[0]).shift(UP * 0.3)
            for i in range(2):
                self.play(mk.to(1 + i), Create(lines[i]), run_time=0.6)
            self.play(Transform(state, mono("closed automatically", 24, color=C_GOLD).move_to(state)),
                      fi[0].animate.set_stroke(C_BLUE))
        modes = mono('"r" read   "w" write (truncate)   "a" append   "b" binary', 22, color=C_GREY)
        modes.to_edge(DOWN, buff=0.5)
        with self.say("Iterating over a file yields one line at a time, so even huge files never have to fit in "
                      "memory. The mode picks read, write, append or binary."):
            self.play(mk.to(4, 6))
            self.play(FadeIn(modes))
        self.clear(keep=[h])
        self.h = h

    def pathlib(self):
        h = self.swap_heading(self.h, "pathlib")
        e = mono('path = Path(tmp) / "data" / "notes.txt"', 32).move_to(UP * 2.0)
        parts = VGroup(pill("tmp", C_GREY, 24), pill("data", C_BLUE, 24), pill("notes.txt", C_GOLD, 24))
        parts.arrange(RIGHT, buff=0.5).move_to(UP * 0.6)
        slashes = VGroup(*[mono("/", 34, color=C_YELLOW).move_to((parts[i].get_right() + parts[i + 1].get_left()) / 2)
                           for i in range(2)])
        with self.say("pathlib represents paths as objects. The slash operator joins them, with the right "
                      "separator for each operating system."):
            self.play(Write(e))
            self.play(LaggedStart(*[FadeIn(p, shift=0.2 * UP) for p in parts], lag_ratio=0.3), FadeIn(slashes))
        attrs = VGroup(mono("path.name    -> 'notes.txt'", 26), mono("path.stem    -> 'notes'", 26),
                       mono("path.suffix  -> '.txt'", 26), mono("path.read_text(encoding='utf-8')", 26, color=C_GREEN),
                       mono("Path(tmp).glob('*.csv')", 26, color=C_GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        attrs.move_to(DOWN * 1.8)
        with self.say("A path knows its name, stem and suffix, can read or write a whole file in one call, "
                      "and can glob for matching files."):
            self.play(LaggedStart(*[FadeIn(a, shift=0.2 * RIGHT) for a in attrs], lag_ratio=0.3), run_time=2.5)
        self.clear(keep=[h])
        self.h = h

    def formats(self):
        h = self.swap_heading(self.h, "JSON and CSV")
        d = mono('{"name": "demo",\n "debug": True,\n "levels": [1, 2, 3]}', 24).move_to(LEFT * 4.0 + UP * 0.9)
        dl = tex("Python dict", 30, C_BLUE).next_to(d, UP, buff=0.3)
        j = mono('{\n  "name": "demo",\n  "debug": true,\n  "levels": [1, 2, 3]\n}', 24, color=C_GOLD).move_to(RIGHT * 3.8 + UP * 0.9)
        jl = tex("JSON text", 30, C_GOLD).next_to(j, UP, buff=0.3)
        a1 = Arrow(d.get_right() + UP * 0.3, j.get_left() + UP * 0.3, buff=0.3, color=C_GOLD)
        a2 = Arrow(j.get_left() + DOWN * 0.4, d.get_right() + DOWN * 0.4, buff=0.3, color=C_BLUE)
        t1 = mono("json.dumps", 22, color=C_GOLD).next_to(a1, UP, buff=0.08)
        t2 = mono("json.loads", 22, color=C_BLUE).next_to(a2, DOWN, buff=0.08)
        with self.say("The json module converts between Python objects and JSON text: dumps produces a string, "
                      "loads parses one. Note how True becomes lower-case true."):
            self.play(FadeIn(d), FadeIn(dl))
            self.play(GrowArrow(a1), FadeIn(t1), FadeIn(j), FadeIn(jl))
            self.play(GrowArrow(a2), FadeIn(t2))
        csvt = mono("city,sales\nTehran,120\nBerlin,95", 22, color=C_GREEN).move_to(LEFT * 5.0 + DOWN * 2.3)
        rows = mono("{'city': 'Tehran', 'sales': '120'}\n{'city': 'Berlin', 'sales': '95'}", 22).move_to(RIGHT * 3.2 + DOWN * 2.3)
        ar = Arrow(csvt.get_right(), rows.get_left(), buff=0.25, color=C_GREEN)
        tl = mono("csv.DictReader", 20, color=C_GREEN).next_to(ar, DOWN, buff=0.1)
        with self.say("For CSV, DictReader turns each row into a dict keyed by the header. Every value comes back "
                      "as a string, so convert numbers yourself."):
            self.play(FadeIn(csvt), GrowArrow(ar), FadeIn(tl), FadeIn(rows))
        self.clear(keep=[h])
        self.h = h

    def own_cm(self):
        h = self.swap_heading(self.h, "Writing a context manager")
        code = code_panel('@contextmanager\ndef timer(label):\n    start = time.perf_counter()\n    try:\n        yield\n'
                          '    finally:\n        elapsed = time.perf_counter() - start\n        print(f"{label}: {elapsed:.4f}s")\n\n'
                          'with timer("sum of squares"):\n    total = sum(i * i for i in range(100_000))',
                          font_size=22).to_edge(LEFT, buff=0.4)
        b1 = SurroundingRectangle(VGroup(code.code_lines[2]), color=C_GREEN, buff=0.06)
        b2 = SurroundingRectangle(code.code_lines[4], color=C_YELLOW, buff=0.06)
        b3 = SurroundingRectangle(VGroup(code.code_lines[5], code.code_lines[7]), color=C_GOLD, buff=0.06)
        labs = VGroup(tex("enter", 32, C_GREEN), tex(r"the \texttt{with} body runs here", 32, C_YELLOW),
                      tex("exit (always)", 32, C_GOLD))
        for l, b in zip(labs, [b1, b2, b3]):
            l.next_to(code, RIGHT, buff=0.5).match_y(b)
        with self.say("Writing your own is easiest with the contextmanager decorator. Everything before the "
                      "yield is the setup; the with block runs at the yield; everything after it, in a finally, "
                      "is the teardown that always happens."):
            self.play(FadeIn(code))
            for b, l in zip([b1, b2, b3], labs):
                self.play(Create(b), FadeIn(l, shift=0.2 * LEFT), run_time=0.9)
            out = mono("sum of squares: 0.0041s", 24, color=C_YELLOW).next_to(code, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(FadeIn(out))
        with self.say("A class works too: define dunder enter and dunder exit. Files, locks, database "
                      "transactions and temporary directories all use exactly this protocol."):
            cls = mono("class Indent:\n    def __enter__(self): ...\n    def __exit__(self, exc_type, exc, tb): ...", 20, color=C_GREY)
            cls.next_to(code, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(FadeOut(out), FadeIn(cls))
        self.clear()
