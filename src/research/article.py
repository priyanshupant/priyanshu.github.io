"""Build article/index.html: the companion article + production guide.
Every slide (narration line) gets a frame and its caption (what you say)."""
import base64, html, io, json, os, subprocess, sys
sys.path.insert(0, ".")
import pacing
from PIL import Image

V = json.load(open("audio/voice/timing.json"))
DUR = json.load(open("article/scene_durations.json"))
off, t, durs = {}, 0.0, {}
for f, sc, _ in pacing.SCENES:
    off[sc] = t
    d = DUR.get(sc, 0.0)
    durs[sc] = d; t += d
TOTAL = t
FILE = {sc: f for f, sc, _ in pacing.SCENES}

def frame(ts, w=480):
    subprocess.run(["ffmpeg", "-v", "0", "-y", "-ss", f"{ts:.2f}", "-i", "final_720p30.mp4", "-frames:v", "1", "/tmp/_a.png"])
    im = Image.open("/tmp/_a.png").convert("RGB").resize((w, w * 9 // 16))
    b = io.BytesIO(); im.save(b, "JPEG", quality=78)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def clipframe(path, w=480):
    d = float(subprocess.check_output(["ffprobe", "-v", "0", "-show_entries", "format=duration", "-of", "csv=p=0", path]))
    subprocess.run(["ffmpeg", "-v", "0", "-y", "-ss", f"{max(0, d - 0.12):.2f}", "-i", path, "-frames:v", "1", "/tmp/_a.png"])
    im = Image.open("/tmp/_a.png").convert("RGB").resize((w, w * 9 // 16))
    b = io.BytesIO(); im.save(b, "JPEG", quality=78)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def mm(x): return f"{int(x // 60)}:{int(x % 60):02d}"
E = html.escape

# Acts: (title, the viewer's question, [scenes], article prose per scene, optional tip boxes per scene)
ACTS = [
 ("Act 0 · The hook", "How can a formula possibly count?", [
   ("Opening", "We start on familiar ground. Every linear-algebra student knows the determinant as a d − b c, and as the thing that decides unique solutions, finds eigenvalues and changes variables. Then the turn: it can also <b>count</b>. The chessboard makes that concrete: about thirteen million domino tilings, five months to list one per second, yet one determinant gives 12,988,816 instantly.",
    "From the reference video: get to the question fast. Keep this opening to about 25 seconds, and speak the puzzle to the viewer (“Your job: get both ants home”).")]),
 ("Act 1 · The puzzle", "How many ways can both ants get home without touching?", [
   ("Hook", "Two ants on a 4×4 grid, each step right or up. They had a fight: neither will step on any dot the other walks on, <i>not even later</i>, because ants leave a scent trail. This matters mathematically: we count pairs of routes that share no dot at all (vertex-disjoint paths), not just routes that avoid meeting at the same moment. On a grid, crossing means sharing a dot.", None),
   ("OneGoodPair", "One peaceful pair, to show the goal is possible.", None),
   ("BruteForce", "The honest way: 6 × 6 = 36 pairs, checked one by one, and 20 never meet. This is the naive method we'll beat.",
    "From the reference video: name the idea before using it. “When counting the good ones is hard, count everything and subtract the bad ones.”"),
   ("TableAndDet", "The surprise. Put the route counts in a 2×2 table, ant by home: [[6, 4], [4, 6]]. Its determinant 6·6 − 4·4 = 20 is exactly the brute-force answer. Coincidence? Hardly. Then the title card.", None)]),
 ("Act 2 · Where the numbers come from", "What are the 6 and the 4?", [
   ("ListRoutes", "Ant one's six routes, walked as they are read aloud. Each is four steps: two right, two up.", None),
   ("Slots", "A route is a choice of which steps go right, so a steps right and b steps up give (a+b choose a) routes. Our four numbers are 6, 4, 4, 6.", None)]),
 ("Act 3 · Reading the formula", "What do 6·6 and 4·4 count?", [
   ("ReadCounts", "6·6 counts every pair sending each ant to its own home: 20 good + 16 bad. 4·4 counts pairs where the ants go to each other's homes (swapped). So det = good + bad − swapped, and it equals good exactly when bad = swapped.",
    "From the reference video: say it as “total minus bad”. 6·6 is everything; 4·4 is what we remove.")]),
 ("Act 4 · The proof", "Why is #bad = #swapped?", [
   ("SwapPaths", "Take a bad pair. Find the first dot of ant one's route that ant two also visits, and swap the tails from there. The ants end at each other's homes: a swapped pair.", None),
   ("SwapTwice", "Swapping again at the same first meeting point restores the original, because nothing before it changed. The map is an involution, so bad and swapped pairs come in couples.", None),
   ("DiagonalSweep", "Could a swapped pair avoid meeting, and so have no partner? Sweep the diagonals x + y = s. The column gap starts at −1, ends at +1, and changes by at most 1 per step, so it hits 0: the ants share a dot. This is a discrete intermediate value theorem.",
    "From the reference video: first show both routes straightened into lines that obviously cross (2 seconds of intuition), then the sweep for rigour."),
   ("PutTogether", "Every bad pair has exactly one swapped partner and vice versa. In the determinant they cancel, leaving exactly the 20 good pairs. A bijective proof.", None)]),
 ("Act 5 · It's not about ants", "Is this a fluke of the grid?", [
   ("MoveHomes", "Move a house and the counts keep agreeing, as long as the starts and homes stay in the same order. Reverse the order and there are 0 peaceful routes; the determinant then counts the swapped pairing with a minus sign.",
    "From the reference video: draw a shaded <b>lane</b> per ant. Non-overlapping lanes is the visual form of “same order”; overlapping lanes give zero."),
   ("SekiJoins", "A third ant: a 3×3 table gives 50, and brute force over all triples agrees.", None),
   ("LemmaVisual", "The general statement, on real numbers. Expanding the 3×3 determinant gives one signed term per pairing: 216 − 96 − 96 − 6 + 16 + 16 = 50. Of the 216 own-home families, 50 never touch. The tail swap pairs every touching family with one of opposite sign (198 against 198), so only the non-touching families survive. This is the Lindström–Gessel–Viennot lemma (Lindström 1973; Gessel and Viennot 1985). A determinant costs about n³ steps, or n^ω with fast matrix multiplication.", None),
   ("WhatLGVCounts", "Any one-way network with no loops works: here a random network with diagonal roads gives a 3×3 determinant of 42, matching brute force. Anything that is secretly non-touching paths, a determinant can count.", None)]),
 ("Act 6 · Disguises", "What else is secretly non-touching paths?", [
   ("HexTiling", "A hexagon cut into triangles, tiled by lozenges (pairs of triangles). A tiling looks like boxes stacked in a corner, but it is completely flat.", None),
   ("TilesToPaths", "Follow the non-flat tiles from left to right: two chains that never touch. Squash the hexagon onto the grid and the chains are exactly our two ants' routes. 20 tilings: our ants were tiling a hexagon.", None),
   ("BoxesCorner", "A 3×3×3 box gives three non-touching chains; a 3×3 determinant counts 980 stackings. MacMahon's formula covers every box (plane partitions).", None),
   ("CatalanMountains", "Two nested mountain ranges that never touch: a 2×2 table of Catalan numbers [[2, 5], [5, 14]] has determinant 3, and there are exactly 3.", None),
   ("AztecIntro", "The Aztec diamond: 2, 8, 64, then 1024 domino tilings, the pattern 2^(n(n+1)/2).", None),
   ("AztecPaths", "Colour it like a chessboard; the four domino types become flat, up, down or no step, so a tiling becomes a family of non-touching paths. The 2×2 route-count determinant is 12·2 − 4·4 = 8.", None),
   ("ArcticCircle", "A uniformly random tiling of a big diamond (order 60, via domino shuffling): frozen brick-wall corners, chaos inside, and a perfect circle between them (Jockusch–Propp–Shor 1995). That's the picture from the very start.", None)]),
 ("Act 7 · When it breaks", "Does the plain determinant always work?", [
   ("SmallBoard2", "Dominoes on a chessboard are perfect matchings, not paths. The 0/1 adjacency determinant of a 2×3 board is −1, not 3: the signs cancel good configurations.", None),
   ("SignFix2", "Kasteleyn (1961): if the signs don't cancel the way you want, change the signs. Flipping one edge makes all three tilings carry the same sign: det = −3, so 3.", None),
   ("Board4x4", "On 4×4 the plain determinant says 0 (“very confident, very wrong”); with minus signs on every other column, |det| = 36, which is right.", None),
   ("FKT", "On the full chessboard: 12,988,816, the five-month count, instantly. The rule is that every 4-cycle carries an odd number of minus signs. It works for any planar graph: the FKT algorithm counts perfect matchings in polynomial time.", None)]),
 ("Act 8 · Why it matters", "So what?", [
   ("Map", "Ants, hexagons, boxes, mountains, diamonds, chessboards: all counted by one determinant each.", None),
   ("Finale", "The same move every time: count everything with signs and let the bad cases cancel in pairs. For computer science this is remarkable. Counting perfect matchings in general is #P-complete (Valiant 1979), but non-touching paths and planar matchings reduce to a single determinant, computable in polynomial time.", None),
   ("Goodbye", "The ants walk home: twenty ways, and they never had to meet.", None)]),
]

parts = []
slide_no = 0
for act, q, scenes in ACTS:
    parts.append(f"<h2>{E(act)}</h2><p class='q'>The viewer's question: <i>{E(q)}</i></p>")
    for sc, prose, tip in scenes:
        sj = json.load(open(f"slides/{sc}.json"))["slides"]
        lines = [(None, None, x["notes"] or "(no narration)") for x in sj]
        parts.append(f"<h3>{E(sc)} <span class='meta'>{mm(off[sc])} · {FILE[sc]} · {len(lines)} slide{'s' if len(lines)!=1 else ''}</span></h3><p>{prose}</p>")
        if tip:
            parts.append(f"<div class='tip'><b>Improvement:</b> {tip}</div>")
        parts.append("<div class='slides'>")
        for k, (s, e, cap) in enumerate(lines):
            slide_no += 1
            img = clipframe(sj[k]["file"])
            parts.append(f"<figure><img src='{img}' alt='{E(sc)} slide {k}'><figcaption><span class='sn'>slide {slide_no} · cue({k})</span>{E(cap)}</figcaption></figure>")
        parts.append("</div>")

GUIDE = r"""
<h2 id="guide">Part 2 · Making it with manim-slides</h2>
<h3>The idea in one paragraph</h3>
<p>Every act is a Manim scene class (in <code>act*.py</code>) that inherits from <code>DScene</code> in <code>common.py</code>. Inside a scene, <code>self.cue(k)</code> marks where narration line <i>k</i> begins. The same code renders two ways:</p>
<ul>
<li><b>Slides mode</b> (<code>SLIDES=1</code>): <code>DScene</code> becomes a manim-slides <code>Slide</code>, and every <code>cue(k)</code> becomes <code>self.next_slide(notes=line k)</code>. So you get one slide per line, with that line as the speaker note. Use this to build, edit and present.</li>
<li><b>Video mode</b> (default): <code>cue(k)</code> waits until line <i>k</i> starts in the recorded voice, so the picture stays in sync with the audio. Use this for the final film.</li>
</ul>

<h3>A scene, as you'll edit it</h3>
<pre>class OneGoodPair(DScene):
    def construct(self):
        lat = Lattice(4, spacing=1.2, center=GRID_C)
        L, N = ant(ANT1).move_to(lat.p(*A1)), ant(ANT2).move_to(lat.p(*A2))
        self.add(lat, endpoints(lat), L, N)

        self.cue(0)                      # slide 0: "Here's one. Ant one goes up first…"
        for step in walk_steps(lat, [(L, GOOD_P, ANT1), (N, GOOD_Q, ANT2)])[0]:
            self.play(step)

        self.cue(1)                      # slide 1: "They never meet. Peace in our time."
        msg = T("They never meet.", 34).to_edge(RIGHT)
        self.play(FadeIn(msg))</pre>
<p>The words for each cue live in <code>narration.json</code> under the scene name, in the same order. A number in that list is a pause in seconds.</p>

<h3>Setup (once)</h3>
<pre>pip install manim==0.22.1 manim-slides           # + ffmpeg on your PATH
pip install "manim-slides[pyside6]"              # only for the presenter window
pip install kokoro-onnx soundfile numpy          # only to re-record the AI voice</pre>
<p>manim-slides 5.7 expects three config keys that Manim 0.22 removed. <code>common.py</code> adds a small compatibility shim, so nothing needs downgrading.</p>

<h3>The editing loop, slide by slide</h3>
<pre># 1. render one act as slides (one slide per narration line)
SLIDES=1 manim -qm act3_two_walkers.py TableAndDet        # Windows: $env:SLIDES='1'; manim -qm ...

# 2. present it: → / ← / space; notes = what you say
manim-slides present TableAndDet
#    …or as a browser deck (press S for speaker notes)
manim-slides convert TableAndDet slides/TableAndDet.html

# 3. edit the code or narration.json, repeat 1–2

# all acts as one deck: slides/presentation.html
bash render_slides.sh m</pre>
<p>To add a slide, add a line to <code>narration.json</code> and a matching <code>self.cue(k)</code> before the animation that goes with it. To split a slide, split the line in two and add a cue. The cue count must equal the number of spoken lines (pauses don't count).</p>

<h3>From slides to the final video</h3>
<ol>
<li><b>Voice.</b> <code>python audio/tts.py --scene TableAndDet</code> re-records one act with the placeholder AI voice and writes line timings to <code>audio/voice/timing.json</code>. To use <b>your own voice</b>, record <code>audio/voice/&lt;Scene&gt;.wav</code> per act, reading the captions above, and put each line's start and end seconds in <code>timing.json</code>.</li>
<li><b>Render in video mode.</b> <code>manim -qm act3_two_walkers.py TableAndDet</code> (no <code>SLIDES</code>). The cues now wait for your voice. Lags are logged in <code>logs/cue_lags.json</code>.</li>
<li><b>Mix.</b> <code>python audio/mix.py 720p30</code> joins all acts and adds voice, sound effects, a quiet music bed, and captions. It produces <code>final_720p30.mp4</code> (soft subtitles), <code>final_720p30_captioned.mp4</code> (burned-in) and <code>captions.srt</code>. <code>python assemble.py 720p30 --chapters-only</code> writes <code>chapters.txt</code>.</li>
</ol>
<p>The <b>Studio</b> (<code>python studio.py</code>, then open http://localhost:8765) does steps 1–3 for one act with a button, and plays the voiced video slide by slide. VS Code tasks (Terminal → Run Task) cover the same commands.</p>

<h3>File map</h3>
<table>
<tr><td><code>pacing.py</code></td><td>scene order</td></tr>
<tr><td><code>narration.json</code></td><td>every spoken line per scene (= slide notes)</td></tr>
<tr><td><code>common.py</code></td><td>grid, ants, paths, colours, <code>DScene</code> with <code>cue()</code>, slides mode</td></tr>
<tr><td><code>act0_opening.py … act9_ending.py</code></td><td>the scenes</td></tr>
<tr><td><code>render_slides.sh</code></td><td>all scenes → manim-slides + <code>slides/presentation.html</code></td></tr>
<tr><td><code>audio/tts.py</code>, <code>audio/mix.py</code></td><td>voice; final mix with captions</td></tr>
<tr><td><code>studio.py</code>, <code>.vscode/tasks.json</code></td><td>slide-by-slide editor; VS Code tasks</td></tr>
</table>

<h3>Before you submit</h3>
<ul>
<li>Every number in the video is computer-checked. Verify the factual claims yourself: <b>ω ≤ 9/4</b> (October 2026, attributed to OpenAI and explained by Amir Shpilka). Also check the dates: Lindström 1973, Gessel–Viennot 1985, Kasteleyn 1961, Valiant 1979, Jockusch–Propp–Shor 1995.</li>
<li>Read Aigner &amp; Ziegler, <i>Proofs from THE BOOK</i>, chapter “Lattice paths and determinants”. It is exactly the proof in Act 4.</li>
<li>Expand the 3×3 determinant [[6,4,1],[4,6,4],[1,4,6]] by hand once, so Act 5 is yours.</li>
</ul>
"""

doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>How Determinants Can Count</title><style>
:root{{--bg:#fbfaf7;--fg:#1d1d1f;--soft:#666;--acc:#9a6b00;--card:#fff;--line:#e6e2d8;--tip:#fff6dd}}
@media (prefers-color-scheme:dark){{:root{{--bg:#121212;--fg:#eee;--soft:#aaa;--acc:#f2c94c;--card:#1c1c1c;--line:#2c2c2c;--tip:#2a2412}}}}
body{{background:var(--bg);color:var(--fg);font:17px/1.6 Georgia,serif;margin:0}}
main{{max-width:980px;margin:auto;padding:28px 16px 80px}}
h1{{font-size:34px;line-height:1.2;margin-bottom:4px}}h2{{margin-top:56px;color:var(--acc);border-bottom:1px solid var(--line);padding-bottom:6px}}
h3{{margin-top:34px}}.meta{{font:13px system-ui,sans-serif;color:var(--soft);font-weight:normal}}
.q{{color:var(--soft);margin-top:-8px}}.tip{{background:var(--tip);border-left:3px solid var(--acc);padding:10px 14px;border-radius:4px;font-size:15px;margin:12px 0}}
.slides{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px;margin:14px 0}}
figure{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden}}
figure img{{width:100%;display:block}}figcaption{{padding:8px 10px;font-size:15px}}
.sn{{display:block;font:12px system-ui,sans-serif;color:var(--soft);margin-bottom:2px}}
pre{{background:#0e0e0e;color:#ddd;padding:12px;border-radius:6px;overflow-x:auto;font-size:13.5px;line-height:1.45}}
code{{font-size:14px}}table td{{padding:4px 10px;border-bottom:1px solid var(--line);vertical-align:top}}
nav a{{color:var(--acc)}}
</style></head><body><main>
<h1>How Determinants Can Count</h1>
<p class="meta">Companion article and production guide · Priyanshu, IIT Indore · DepthTCS 2026 · video length {mm(TOTAL)} · {slide_no} slides</p>
<p style="font:15px system-ui,sans-serif"><b>▶ <a href="video.mp4">Watch the video</a></b> (captioned) · <b><a href="present.html">Presenter view</a></b> (slides with the words to say below; → for next) · <a href="slides.html">plain slide deck</a></p>
<p>This page is the whole video in written form. Each act opens with the question it answers, then a short explanation of the mathematics. After that, every slide is shown as a frame, and its caption is exactly what you say on that slide. Highlighted boxes mark improvements to make, adapted from a SoME4 explainer on the same lemma. <a href="#guide">Part 2</a> explains how to build, edit and present it with manim-slides.</p>
<nav><p><b>Contents:</b> {' · '.join(E(a.split(' · ')[1]) for a, _, _ in ACTS)} · <a href="#guide">Making it</a></p></nav>
<h2 style="margin-top:30px">Part 1 · The video</h2>
{''.join(parts)}
{GUIDE}
</main></body></html>"""
open("article/index.html", "w").write(doc)
print(slide_no, "slides;", round(len(doc) / 1e6, 1), "MB")
