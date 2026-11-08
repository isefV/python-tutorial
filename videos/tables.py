"""Shared pieces for the pandas lessons: the tutorial's sample DataFrame and table builders."""
from lesson import *

CITY = {"Tehran": C_GOLD, "Berlin": C_TEAL, "Tokyo": C_PURPLE}
C_IDX = C_GREY
C_VAL = C_BLUE

DF = [  # index, city, month, sales  (the DataFrame used throughout the pandas lessons)
    (0, "Tehran", "Jan", "120.0"),
    (1, "Berlin", "Jan", "95.0"),
    (2, "Tehran", "Feb", "140.0"),
    (3, "Tokyo", "Feb", "80.0"),
    (4, "Berlin", "Feb", "110.0"),
    (5, "Tokyo", "Jan", "NaN"),
]


def series_col(index, values, color=C_VAL, w_idx=0.6, w_val=1.0, h=0.6, size=26) -> VGroup:
    """Vertical Series: rows of (index cell, value cell)."""
    rows = VGroup()
    for i, v in zip(index, values):
        ic = cell(i, w=w_idx, h=h, color=C_IDX, size=size, fill_opacity=0.05)
        vc = cell(v, w=w_val, h=h, color=C_BAD if v == "NaN" else color, size=size)
        rows.add(VGroup(ic, vc).arrange(RIGHT, buff=0))
    return rows.arrange(DOWN, buff=0)


def df_table(rows=None, cols=("city", "month", "sales"), widths=(1.7, 1.3, 1.4), row_h=0.55, size=24) -> VGroup:
    """The sample DataFrame as a table_grid: t[0] is the header row, t[r][0] the index cell."""
    rows = DF if rows is None else rows
    pick = {"city": 1, "month": 2, "sales": 3}
    body = [tuple(r[pick[c]] for c in cols) for r in rows]
    return table_grid([tuple(cols)] + body, list(widths), row_h=row_h, size=size,
                      index=[r[0] for r in rows], index_w=0.6)


def column(t: VGroup, c: int) -> VGroup:
    return VGroup(*[t[r][c] for r in range(len(t))])
