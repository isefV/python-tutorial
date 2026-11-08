from tables import *


class L24PandasLoad(Lesson):
    NUM, SLUG, TITLE, CATEGORY = 24, "pandas-load-inspect", "Load and inspect", "pandas"

    def construct(self):
        self.intro("Lesson twenty-four: loading and inspecting data. Real work starts with a file, and the first "
                   "few minutes with a new dataset always follow the same routine.",
                   r"\texttt{read\_csv}, \texttt{head}, \texttt{info}, \texttt{describe}, missing values")
        self.read()
        self.structure()
        self.counts()
        self.write()
        self.outro([r"\texttt{pd.read\_csv} (and \texttt{read\_excel}, \texttt{read\_parquet}, \texttt{read\_sql}).",
                    r"First look: \texttt{head}, \texttt{shape}, \texttt{dtypes}, \texttt{info}, \texttt{describe}.",
                    r"\texttt{value\_counts}, \texttt{nunique} and \texttt{isna().sum()} find surprises early.",
                    r"Write back with \texttt{to\_csv(index=False)}, \texttt{to\_json}, \texttt{to\_parquet}."],
                   "Read the file, look at the first rows, check the shape and types, summarize the numbers, "
                   "count the categories and the missing values, and only then start analysing.")

    def read(self):
        h = self.heading("Reading a CSV")
        csv = mono("city,month,sales\nTehran,Jan,120\nBerlin,Jan,95\nTehran,Feb,140\nTokyo,Feb,80\nBerlin,Feb,110\nTokyo,Jan,",
                   24, color=C_GREEN)
        fi = SurroundingRectangle(csv, color=C_GREEN, buff=0.25)
        fl = mono("sales.csv", 20, color=C_GREEN).next_to(fi, UP, buff=0.1, aligned_edge=LEFT)
        g = VGroup(fi, csv, fl).move_to(LEFT * 4.2 + DOWN * 0.3)
        t = df_table(size=22, row_h=0.5).move_to(RIGHT * 3.0 + DOWN * 0.3)
        call = mono('df = pd.read_csv("sales.csv")', 26, color=C_YELLOW).to_edge(UP, buff=1.0)
        with self.say("read csv turns a text file into a DataFrame. It reads the header for column names, guesses "
                      "each column's type, and treats empty fields as missing. There are siblings for Excel, Parquet, "
                      "JSON and SQL databases."):
            self.play(FadeIn(g))
            self.play(FadeIn(call))
            arr = Arrow(fi.get_right(), t.get_left(), buff=0.2, color=C_YELLOW)
            self.play(GrowArrow(arr), FadeIn(t, shift=0.3 * RIGHT))
            self.play(Circumscribe(t[6][3], color=C_BAD))
        with self.say("head shows the first rows, five by default, and tail the last ones. That's always the first "
                      "thing to run: does the data look like you expected?"):
            hd = mono("df.head(3)", 26, color=C_GOLD).next_to(t, UP, buff=0.3)
            self.play(FadeIn(hd), *[t[r].animate.set_opacity(0.2) for r in range(4, 7)])
        self.clear(keep=[h])
        self.h = h

    def structure(self):
        h = self.swap_heading(self.h, "Structure and summary statistics")
        info = code_panel("df.shape   # (6, 3)\ndf.dtypes  # city str, month str, sales float64\ndf.info()", font_size=24)
        info.to_edge(UP, buff=1.0)
        rows = [["", "sales"], ["count", "5"], ["mean", "109.0"], ["std", "23.8"], ["min", "80.0"], ["50%", "110.0"], ["max", "140.0"]]
        d = table_grid(rows, [1.4, 1.6], row_h=0.5, size=24).move_to(LEFT * 1.8 + DOWN * 1.4)
        dl = mono("df.describe()", 26, color=C_GOLD).next_to(d, LEFT, buff=0.5).align_to(d, UP)
        with self.say("Next, the structure: shape, the d-type of every column, and info, which adds non-null counts "
                      "and memory use. Already you can see that sales has only five values out of six."):
            self.play(FadeIn(info))
        with self.say("describe summarizes every numeric column: count, mean, standard deviation, minimum, quartiles "
                      "and maximum. Again count is five, so one value is missing."):
            self.play(FadeIn(dl), FadeIn(d[0]))
            self.play(LaggedStart(*[FadeIn(r, shift=0.2 * RIGHT) for r in d[1:]], lag_ratio=0.2), run_time=2)
            self.play(Circumscribe(d[1], color=C_BAD))
        self.clear(keep=[h])
        self.h = h

    def counts(self):
        h = self.swap_heading(self.h, "Values, counts and missing data")
        ax = BarChart([2, 2, 2], bar_names=["Tehran", "Berlin", "Tokyo"], y_range=[0, 3, 1], y_length=3, x_length=5,
                      bar_colors=[C_GOLD, C_TEAL, C_PURPLE], bar_width=0.6,
                      x_axis_config={"font_size": 26}, y_axis_config={"font_size": 22})
        ax.move_to(LEFT * 3.2 + DOWN * 0.6)
        al = mono('df["city"].value_counts()', 24, color=C_YELLOW).next_to(ax, UP, buff=0.4)
        with self.say("For text columns, value counts tells you how often each value appears, and nunique how many "
                      "distinct values there are. Typos and inconsistent spellings show up here immediately."):
            self.play(FadeIn(al), Create(ax), run_time=1.5)
            nu = mono('df["city"].nunique() -> 3', 24).next_to(ax, DOWN, buff=0.4)
            self.play(FadeIn(nu))
        na = table_grid([["", "missing"], ["city", "0"], ["month", "0"], ["sales", "1"]], [1.6, 1.6], row_h=0.55, size=24)
        na.move_to(RIGHT * 3.4 + DOWN * 0.6)
        na[3][1][1].set_color(C_BAD)
        nl = mono("df.isna().sum()", 24, color=C_YELLOW).next_to(na, UP, buff=0.4)
        with self.say("And isna dot sum counts missing values per column. True counts as one, so summing the boolean "
                      "mask counts the gaps."):
            self.play(FadeIn(nl), FadeIn(na))
            self.play(Circumscribe(na[3], color=C_BAD))
        self.clear(keep=[h])
        self.h = h

    def write(self):
        h = self.swap_heading(self.h, "Writing data")
        rows = VGroup(mono("df.to_csv(\"out.csv\", index=False)", 28), mono('df.to_json(orient="records")', 28),
                      mono('df.to_parquet("out.parquet")', 28), mono('df.to_excel("out.xlsx")', 28))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.3)
        with self.say("Writing is the mirror image: to csv, to json, to parquet, to excel. Pass index equals False "
                      "to csv unless the index carries real information; otherwise you get an extra unnamed column."):
            self.play(LaggedStart(*[FadeIn(r, shift=0.2 * RIGHT) for r in rows], lag_ratio=0.3), run_time=2)
            self.play(Circumscribe(rows[0], color=C_YELLOW))
        self.clear()
