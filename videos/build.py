"""Render every lesson video and concatenate them per category.

Run from this folder (manim's environment provides PyAV):

    uvx --python 3.12 --from manim python build.py              # 1080p60, everything (-j 4 workers)
    uvx --python 3.12 --from manim python build.py -q l         # fast 480p drafts
    uvx --python 3.12 --from manim python build.py --only 3 21  # just these lessons
    uvx --python 3.12 --from manim python build.py --concat-only

Output (gitignored):
    ../output/lessons/<res>/NN-slug.mp4           one ~2 min video per lesson
    ../output/lessons/<res>/<category>.mp4        all lessons of a category, in order
Narration (committed): narration/NN-slug.txt is written by each scene when it renders;
this script also writes narration/<category>-all.txt with timestamps for the joined video.
"""
import argparse
import queue
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path

import av

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "output" / "lessons"
NARR = HERE / "narration"
RES = {"l": "480p15", "m": "720p30", "h": "1080p60", "k": "2160p60"}
CATEGORIES = ["Python", "NumPy", "pandas", "Matplotlib"]
META = re.compile(r'class (\w+)\(Lesson\):\s*\n\s*NUM, SLUG, TITLE, CATEGORY = (\d+), "([^"]+)", "([^"]+)", "([^"]+)"')


def discover():
    lessons = []
    for f in sorted(HERE.glob("l[0-9][0-9]_*.py")):
        m = META.search(f.read_text(encoding="utf-8"))
        if not m:
            sys.exit(f"{f.name}: no Lesson subclass with NUM, SLUG, TITLE, CATEGORY")
        cls, num, slug, title, cat = m.groups()
        lessons.append(dict(file=f, cls=cls, num=int(num), slug=slug, title=title, cat=cat,
                            name=f"{int(num):02d}-{slug}"))
    return sorted(lessons, key=lambda l: l["num"])


def render(lesson, quality, media):
    """Render one lesson into `media` (one media dir per worker: parallel manim runs must not share a Tex cache)."""
    cmd = [sys.executable, "-m", "manim", f"-q{quality}", "-v", "WARNING", "--progress_bar", "none",
           "--media_dir", str(media), lesson["file"].name, lesson["cls"]]
    stale = OUT / RES[quality] / f"{lesson['name']}.mp4"
    stale.unlink(missing_ok=True)
    t0 = time.time()
    p = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
    if p.returncode:
        print(p.stdout[-3000:], p.stderr[-3000:], sep="\n")
        raise RuntimeError(f"render failed: {lesson['name']}")
    src = media / "videos" / lesson["file"].stem / RES[quality] / f"{lesson['cls']}.mp4"
    dst = OUT / RES[quality] / f"{lesson['name']}.mp4"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    print(f"  {lesson['name']:32s} {duration(dst):6.1f}s  (rendered in {time.time() - t0:.0f}s)", flush=True)


def duration(path) -> float:
    with av.open(str(path)) as c:
        s = c.streams.video[0]
        return float(s.duration * s.time_base) if s.duration else c.duration / 1e6


def concat(paths, dst):
    """Join same-format mp4 files without re-encoding (packet remux with shifted timestamps)."""
    out = av.open(str(dst), "w")
    ostream = None
    offset = Fraction(0)
    for p in paths:
        with av.open(str(p)) as inp:
            ist = inp.streams.video[0]
            if ostream is None:
                ostream = out.add_stream_from_template(ist)
            tb = ist.time_base
            shift = int(offset / tb)
            end = 0
            for pkt in inp.demux(ist):
                if pkt.dts is None:
                    continue
                end = max(end, pkt.pts + (pkt.duration or 0))
                pkt.pts += shift
                pkt.dts += shift
                pkt.stream = ostream
                out.mux(pkt)
            offset += end * tb
    out.close()
    return float(offset)


def fmt_t(t):
    m, s = divmod(int(round(t)), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def join_narration(cat, lessons, offsets, total):
    lines = [f"{cat} - all lessons in one video ({cat.lower()}.mp4, {fmt_t(total)})", ""]
    for l, off in zip(lessons, offsets):
        txt = (NARR / f"{l['name']}.txt").read_text(encoding="utf-8").splitlines()
        lines.append(f"===== [{fmt_t(off)}] Lesson {l['num']:02d} - {l['title']} =====")
        for row in txt:
            m = re.match(r"\[(\d+):(\d+)\] (.*)", row)
            if m:
                lines += [f"[{fmt_t(off + int(m[1]) * 60 + int(m[2]))}] {m[3]}", ""]
    (NARR / f"{cat.lower()}-all.txt").write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-q", "--quality", default="h", choices=RES)
    ap.add_argument("--only", type=int, nargs="+", help="lesson numbers to render")
    ap.add_argument("--concat-only", action="store_true")
    ap.add_argument("--no-concat", action="store_true", help="render only")
    ap.add_argument("-j", "--jobs", type=int, default=4, help="parallel manim processes")
    a = ap.parse_args()

    lessons = discover()
    todo = [l for l in lessons if not a.only or l["num"] in a.only]
    if not a.concat_only:
        jobs = queue.Queue()
        for l in todo:
            jobs.put(l)
        failed = []

        def worker(k):
            media = OUT / f"media_w{k}"
            while True:
                try:
                    l = jobs.get_nowait()
                except queue.Empty:
                    return
                try:
                    render(l, a.quality, media)
                except RuntimeError as e:
                    failed.append(l["name"])
                    print(e, flush=True)
        n = max(1, min(a.jobs, len(todo)))
        print(f"rendering {len(todo)} lessons at {RES[a.quality]} with {n} workers ...", flush=True)
        with ThreadPoolExecutor(n) as ex:
            for f in [ex.submit(worker, k) for k in range(n)]:
                f.result()
        if failed:
            print("FAILED:", ", ".join(sorted(failed)))

    if a.no_concat:
        return
    folder = OUT / RES[a.quality]
    for cat in CATEGORIES:
        group = [l for l in lessons if l["cat"] == cat]
        if not group:
            continue
        paths = [folder / f"{l['name']}.mp4" for l in group]
        missing = [p.name for p in paths if not p.exists()]
        if missing:
            print(f"skip {cat}.mp4: missing {', '.join(missing)}")
            continue
        offsets, t = [], 0.0
        for p in paths:
            offsets.append(t)
            t += duration(p)
        total = concat(paths, folder / f"{cat.lower()}.mp4")
        join_narration(cat, group, offsets, total)
        print(f"{cat.lower()}.mp4: {len(paths)} lessons, {fmt_t(total)}")


if __name__ == "__main__":
    main()
