"""Sheet of slides a..b (1-based): last frame of each slide clip + its caption.
   python research/slide_sheet.py 1 6 out.png"""
import html, re, subprocess, sys, textwrap
from PIL import Image, ImageDraw, ImageFont
a, b, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
s = open("slides/presentation.html").read()
secs = re.findall(r"<section(.*?)</section>", s, re.S)[a - 1:b]
W, H = 560, 315
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
cols = 2
rows = (len(secs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (W + 10) + 10, rows * (H + 120) + 10), (24, 24, 24))
d = ImageDraw.Draw(sheet)
for i, sec in enumerate(secs):
    v = "slides/" + re.search(r'data-background-video="([^"]+)"', sec).group(1)
    n = re.search(r'<aside class="notes"[^>]*>(.*?)</aside>', sec, re.S)
    cap = html.unescape(n.group(1).strip()) if n else "(no narration: animation only)"
    dur = float(subprocess.check_output(["ffprobe", "-v", "0", "-show_entries", "format=duration", "-of", "csv=p=0", v]))
    subprocess.run(["ffmpeg", "-v", "0", "-y", "-ss", f"{max(0, dur - 0.1):.2f}", "-i", v, "-frames:v", "1", "/tmp/_s.png"])
    im = Image.open("/tmp/_s.png").convert("RGB").resize((W, H))
    x, y = 10 + (i % cols) * (W + 10), 10 + (i // cols) * (H + 120)
    sheet.paste(im, (x, y))
    d.text((x, y + H + 6), f"Slide {a + i}  ({dur:.1f}s of animation)", fill=(242, 201, 76), font=bold)
    d.multiline_text((x, y + H + 28), "\n".join(textwrap.wrap(cap, 70)[:5]), fill=(235, 235, 235), font=font, spacing=3)
sheet.save(out)
