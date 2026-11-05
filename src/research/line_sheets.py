"""Review sheets: for every narration line, frames at 15%, 50%, 90% of the line (plus 0.6s after),
with the caption, so picture can be checked against what is heard at that moment."""
import json, os, subprocess, sys, textwrap
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import pacing
q = "720p30"
voice = json.load(open(os.path.join(ROOT, "audio/voice/timing.json")))
out = os.path.join(ROOT, "previews/lines"); os.makedirs(out, exist_ok=True)
video = os.path.join(ROOT, "final_720p30.mp4")
items, t = [], 0.0
for f, sc, _ in pacing.SCENES:
    v = os.path.join(ROOT, "media/videos", f[:-3], q, sc + ".mp4")
    d = float(subprocess.check_output(["ffprobe", "-v", "0", "-show_entries", "format=duration", "-of", "csv=p=0", v]))
    for k, (s, e, cap) in enumerate(voice[sc]["lines"]):
        items.append((sc, k, t + s, t + e, cap))
    t += d
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
W, H, PER = 400, 225, 4
def grab(ts, path):
    subprocess.run(["ffmpeg", "-v", "0", "-y", "-ss", f"{ts:.2f}", "-i", video, "-frames:v", "1", "-vf", f"scale={W}:{H}", path])
    return Image.open(path)
for p in range(0, len(items), PER):
    rows = items[p:p + PER]
    sheet = Image.new("RGB", (W * 4, (H + 64) * len(rows)), (40, 40, 40))
    dr = ImageDraw.Draw(sheet)
    for r, (sc, k, s, e, cap) in enumerate(rows):
        y = r * (H + 64)
        for c, ts in enumerate([s + 0.15 * (e - s), s + 0.5 * (e - s), s + 0.9 * (e - s), e + 0.6]):
            im = grab(ts, "/tmp/_g.png")
            sheet.paste(im, (c * W, y + 64))
            dr.text((c * W + 4, y + 66), f"{int(ts//60)}:{ts%60:04.1f}", fill=(255, 255, 0), font=font)
        txt = f"{sc} #{k} [{int(s//60)}:{s%60:04.1f}-{int(e//60)}:{e%60:04.1f}]  " + cap
        dr.multiline_text((6, y + 4), "\n".join(textwrap.wrap(txt, 185)[:3]), fill=(255, 255, 255), font=font)
    sheet.save(os.path.join(out, f"L{p // PER:02d}.png"))
print(len(items), "lines")
