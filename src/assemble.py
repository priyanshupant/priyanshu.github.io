"""Join the rendered scenes, in script order, into one video + a chapter list.

    python assemble.py [quality_dir]      # default 720p30 -> full_video_720p30.mp4
"""
import os
import subprocess
import sys

import pacing

HERE = os.path.dirname(os.path.abspath(__file__))
q = next((a for a in sys.argv[1:] if not a.startswith("--")), "720p30")
# YouTube-style chapters: a title starts a new chapter at the first scene listed.
CHAPTERS = {"Opening": "Determinants you met in school",
            "Hook": "A simple puzzle",
            "TableAndDet": "An old friend: the determinant", "ThreeAnts": "Three ants",
            "WhyCard": "Why does this work?", "LemmaCard": "The general lemma (Lindström–Gessel–Viennot)",
            "PatternCard": "Another example: hexagon tilings", "TheTrick": "How a determinant counts (D.I.E.)"}
files, chapters, t = [], [], 0.0
for f, sc, _ in pacing.SCENES:
    v = os.path.join(HERE, "media", "videos", f[:-3], q, sc + ".mp4")
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                       "-of", "csv=p=0", v]))
    files.append(v)
    if sc in CHAPTERS:
        chapters.append(f"{int(t // 60)}:{int(t % 60):02d} {CHAPTERS[sc]}")
    t += d
lst = os.path.join(HERE, "media", "concat.txt")
with open(lst, "w") as fh:
    fh.writelines(f"file '{v}'\n" for v in files)
out = os.path.join(HERE, f"full_video_{q}.mp4")
if "--chapters-only" not in sys.argv:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out], check=True)
with open(os.path.join(HERE, "chapters.txt"), "w") as fh:
    fh.write("\n".join(chapters) + f"\n\ntotal {int(t // 60)}:{int(t % 60):02d}\n")
print(open(os.path.join(HERE, "chapters.txt")).read())
print("wrote", out)
