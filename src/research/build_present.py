"""Rebuild the published site folder:
   - presenter view (present.html): one clip per narration line, cut from the voiced film
     (final_720p30_nomusic.mp4 = voice + sound effects, no music), so picture, voice and
     effects are exactly as in the video; caption = that line
   - plain manim-slides deck (slides.html + presentation_assets)

   NO_MUSIC=1 python audio/mix.py 720p30     # first: the no-music film + scene offsets
   python research/build_present.py <site_dir>/determinants
"""
import json, os, re, shutil, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import pacing

out = sys.argv[1]
os.makedirs(os.path.join(out, "clips"), exist_ok=True)
film = "final_720p30_nomusic.mp4"
offsets = json.load(open("media/offsets_720p30.json"))
timing = json.load(open("audio/voice/timing.json"))
LEAD = 0.15
STAMP = int(__import__("time").time())

items, cuts = [], []
for f, sc, _ in pacing.SCENES:
    v = f"media/videos/{f[:-3]}/720p30/{sc}.mp4"
    dur = float(subprocess.check_output(["ffprobe", "-v", "0", "-show_entries", "format=duration", "-of", "csv=p=0", v]))
    off = offsets[sc]
    lines = timing.get(sc, {}).get("lines", [])
    if not lines:
        cuts.append((off, off + dur)); items.append({"t": "", "s": sc}); continue
    starts = [0.0] + [max(0.0, s - LEAD) for s, _, _ in lines[1:]] + [dur]
    for k, (s, e, cap) in enumerate(lines):
        cuts.append((off + starts[k], off + starts[k + 1]))
        items.append({"t": cap, "s": sc})

old = {os.path.basename(p) for p in os.listdir(os.path.join(out, "clips"))}
for n, ((a, b), it) in enumerate(zip(cuts, items), 1):
    name = f"{n:03d}.mp4"
    it["v"] = f"clips/{name}?v={STAMP}"           # version tag: browsers refetch after every rebuild
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", film,
                    "-c:v", "libx264", "-crf", "24", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
                    os.path.join(out, "clips", name)], check=True)
    old.discard(name)
for stale in old:                       # fewer slides than before: remove leftovers
    os.remove(os.path.join(out, "clips", stale))

tpl = open(os.path.join(out, "present.html")).read()
tpl = re.sub(r"const S=\[.*?\];", lambda m: "const S=" + json.dumps(items, ensure_ascii=False) + ";", tpl, count=1, flags=re.S)
open(os.path.join(out, "present.html"), "w").write(tpl)

shutil.copy("slides/presentation.html", os.path.join(out, "slides.html"))
shutil.rmtree(os.path.join(out, "presentation_assets"), ignore_errors=True)
shutil.copytree("slides/presentation_assets", os.path.join(out, "presentation_assets"))
print(len(items), "slides ->", out, f"({sum(b - a for a, b in cuts):.1f} s of clips)")
