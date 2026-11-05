"""Build storyboard/index.html: the v6 script beat by beat, each with an image
(a frame of the current cut at scene:line:fraction, or a mockup still)."""
import base64, io, json, os, subprocess, sys
sys.path.insert(0, ".")
import pacing
from PIL import Image

V = json.load(open("audio/voice/timing.json"))
off, t = {}, 0.0
for f, sc, _ in pacing.SCENES:
    off[sc] = t
    t += float(subprocess.check_output(["ffprobe", "-v", "0", "-show_entries", "format=duration", "-of", "csv=p=0",
                                        f"media/videos/{f[:-3]}/720p30/{sc}.mp4"]))
MOCK = "media/images/storyboard_mock/{}_ManimCE_v0.22.1.png"

def img(src):
    if src.startswith("mock:"):
        im = Image.open(MOCK.format(src[5:]))
    else:
        sc, k, fr = src.split(":")
        s, e, _ = V[sc]["lines"][int(k)]
        ts = off[sc] + s + float(fr) * (e - s)
        subprocess.run(["ffmpeg", "-v", "0", "-y", "-ss", f"{ts:.2f}", "-i", "final_720p30.mp4", "-frames:v", "1", "/tmp/_sb.png"])
        im = Image.open("/tmp/_sb.png")
    im = im.convert("RGB").resize((640, 360))
    b = io.BytesIO(); im.save(b, "JPEG", quality=82)
    return base64.b64encode(b.getvalue()).decode()

# (act title, viewer question, [(id, narration, visual note, image source, status)])
S = [
("Act 0 · Hook", "—", [
 ("0.1", "(no voice, 3 s, soft music)", "The finished arctic-circle tiling glows, then fades. 'Here's where we're headed.'", "ArcticCircle:2:0.95", "reuse"),
 ("0.2", "You've met the determinant. For a two-by-two matrix, it's a d minus b c.", "Matrix [[a,b],[c,d]]; main diagonal glows green → 'a d', other glows red → '− b c'. This diagonal glow returns at every determinant.", "mock:MockDet", "new"),
 ("0.3", "It's how we check whether equations have a unique solution, find eigenvalues, and change variables in integrals.", "Three small panels, each on its word (labels corrected: 'unique solution ⇔ det ≠ 0').", "Hook:8:0.9", "reuse, fix label"),
 ("0.4", "But here's something it does that most courses never mention. It counts.", "Panels slide away; 'det → it counts'.", "mock:MockCounts", "new"),
 ("0.5", "How many ways can you tile a chessboard with dominoes? About thirteen million. If you listed them, one every second, you'd be at it for five months.", "Board fills with dominoes; a clock spins; '≈ 5 months'.", "mock:MockChess", "new"),
 ("0.6", "A determinant gives the exact number, instantly. So how can a formula possibly count?", "'det' lands on 12,988,816.", "Dominoes8x8:1:0.6", "reuse"),
]),
("Act 1 · The puzzle", "How can a formula count?", [
 ("1.1", "Let's start with the smallest example I know. Meet two ants. They live on a grid.", "Grid fades in, two ants.", "Hook:0:0.95", "reuse"),
 ("1.2", "Every step goes one dot right, or one dot up. Never left, never down.", "Arrows from the ant; it tries left, bounces back.", "Hook:1:0.9", "reuse (arrows from ant)"),
 ("1.3", "The blue ant, ant one, lives here. The orange ant, ant two, lives there.", "Homes appear on 'here' and 'there'.", "Hook:2:0.9", "reuse"),
 ("1.4", "There's one small problem. They had a fight. Now neither will set foot on any dot the other one walks on. Not even later: ants leave a scent trail.", "Ant one walks, leaving a glowing trail. Ant two reaches the trail: red '!', backs off.", "mock:MockScent", "new"),
 ("1.5", "So their two routes can't touch, anywhere. How many pairs of routes get both ants home? Maybe pause, and try to find one.", "Question; 2-second hold.", "Hook:5:0.95", "reuse"),
 ("1.6", "Here's one. Ant one goes up first, ant two goes right first. They never meet. Peace in our time.", "One good pair walked.", "OneGoodPair:1:0.9", "reuse"),
 ("1.7", "To find them all, the honest way: each ant has six routes, so thirty-six pairs. Check them one by one. This pair never meets. This one does. So does this one…", "6×6 grid labelled by routes; first three spotlighted.", "BruteForce:1:0.5", "reuse"),
 ("1.8", "…twenty pairs never meet.", "Tally boxed: 20.", "BruteForce:3:0.95", "reuse"),
 ("1.9", "Now something that looks completely unrelated. Count the routes from each ant to each home, put those four numbers in a little square, and take the determinant: six times six, minus four times four…", "Table [[6,4],[4,6]], same green/red diagonal glow as 0.2.", "TableAndDet:5:0.95", "reuse"),
 ("1.10", "…twenty. (pause) The same twenty. Coincidence? Hardly. Let's find out why.", "'20 = brute force 20', then the title and author.", "TableAndDet:7:0.95", "reuse"),
]),
("Act 2 · Where the numbers come from", "What are the 6 and the 4?", [
 ("2.1", "First, those four numbers. How many ways can ant one get home? Take a guess. (pause) Let's list them: right, right, up, up. Right, up, right, up… six.", "Ant walks each route as it is read; thumbnails; counter 6.", "ListRoutes:1:0.97", "reuse"),
 ("2.2", "Notice: every route is four steps, two right and two up. So a route is just a choice of which two steps go right. Four choose two: six.", "Slots; every choice drawn as a route.", "Slots:0:0.9", "reuse"),
 ("2.3", "The same works for any start and home: a steps right and b steps up gives a-plus-b choose a routes. Ant one to its home: six. To the other: four. Ant two: four and six. That's our little square.", "General box picture, then the four numbers.", "Slots:3:0.95", "reuse"),
]),
("Act 3 · Reading the formula", "What do the two products count?", [
 ("3.1", "Here's the thing that bugged me when I first saw this. Six times six counts every way to send each ant to its own home, including the pairs that crash into each other. Twenty good, sixteen bad.", "36 pairs, coloured green/red; '36 = 20 good + 16 bad'.", "ReadCounts:1:0.95", "reuse"),
 ("3.2", "Four times four counts something stranger: each ant walking to the other one's house.", "16 swapped pairs.", "ReadCounts:2:0.95", "reuse"),
 ("3.3", "So the determinant is good, plus bad, minus swapped. For that to equal the good ones, the swapped must cancel the bad exactly. Not roughly. Exactly. Let's match them up.", "'det = 20 good + 16 bad − 16 swapped', 'equal?' arrow.", "ReadCounts:3:0.95", "reuse"),
]),
("Act 4 · The proof", "Why is bad = swapped?", [
 ("4.1", "Take a bad pair. Walk along ant one's route and stop at the first dot ant two also visits.", "Probe walks; first meeting dot ringed.", "SwapPaths:1:0.95", "reuse"),
 ("4.2", "From that dot on, swap their tails. Look where they end: each at the other's house. A bad pair became a swapped pair.", "Tails swap with an arc.", "SwapPaths:3:0.95", "reuse"),
 ("4.3", "And it undoes itself. Nothing before that dot changed, so it's still the first meeting point. Swap again, and you're back where you started. Do it twice and nothing happened: an involution. Like most committee meetings.", "Two icons with swap arrows both ways.", "SwapTwice:2:0.95", "reuse"),
 ("4.4", "One worry left: could a swapped pair avoid meeting, and have no partner? Sweep a diagonal. Ant one starts a column to the left, ends a column to the right, and moves at most one column per step. So somewhere they share a dot.", "Diagonal sweep; gap −1 … +1; 0 ringed.", "DiagonalSweep:5:0.7", "reuse"),
 ("4.5", "So bad and swapped pairs pair off perfectly, and cancel. What survives is exactly the twenty.", "Pairs link and pop; 20 green remain.", "PutTogether:2:0.95", "reuse"),
 ("4.6", "So far: the minus sign isn't throwing things away at random. It removes an exact copy of the bad pairs.", "Recap card.", "mock:MockRecap", "new"),
]),
("Act 5 · It's not about ants", "Is this a fluke of this grid?", [
 ("5.1", "You might be thinking: surely that's a fluke of this little grid. Move the second house anywhere, and the two counts still agree, as long as the order stays the same.", "Table of house positions: brute force = det.", "MoveHomes:1:0.95", "reuse"),
 ("5.2", "Add a third ant. Three-by-three table: fifty. Brute force over all the triples: fifty.", "Three ants, matrix, det 50.", "SekiJoins:1:0.95", "reuse"),
 ("5.3", "Here's why, in general. Expanding the determinant gives one term for each way to pair starts with homes, each with a sign: two hundred sixteen, minus ninety-six, minus ninety-six, minus six, plus sixteen, plus sixteen.", "Six pairing diagrams with their values.", "LemmaVisual:2:0.98", "reuse"),
 ("5.4", "Every family that touches gets cancelled by the same tail swap: one hundred ninety-eight against one hundred ninety-eight. What's left: the fifty that never touch.", "Touching parts cancel; 50 stays.", "LemmaVisual:5:0.6", "reuse"),
 ("5.5", "That's the Lindström–Gessel–Viennot lemma, and it works for any one-way network, roads in any directions, any number of walkers. Here: forty-two. Of course.", "General network, det 42, counter 42.", "WhatLGVCounts:2:0.95", "reuse"),
 ("5.6", "And it's fast. Brute force over n ants explodes; a determinant takes about n cubed steps. And that exponent keeps falling: this October it reached nine quarters.", "ω staircase from 3 to 9/4.", "LemmaVisual:9:0.95", "reuse"),
 ("5.7", "So anything that's secretly a family of non-touching paths, a determinant can count. And they're hiding everywhere.", "Four thumbnails of what's coming.", "WhatLGVCounts:3:0.95", "reuse"),
]),
("Act 6 · Disguises", "What else is secretly paths?", [
 ("6.1", "Look at this hexagon, cut into little triangles. Glue two together and you get a tile. Can you cover the hexagon, no gaps, no overlaps?", "Triangles, lozenges, sticking out / overlapping crossed.", "HexTiling:2:0.6", "reuse"),
 ("6.2", "Here's one. Your brain insists it's a stack of boxes. It's completely flat.", "Shading goes flat grey, then back to 3D.", "HexTiling:4:0.4", "reuse"),
 ("6.3", "Fade the flat tiles and follow the others left to right: two chains that never touch. Squash the hexagon onto our grid…", "Chains → routes on the ant grid.", "TilesToPaths:3:0.9", "reuse"),
 ("6.4", "…and they're our two ants. Twenty tilings. All this time, our ants were tiling a hexagon.", "All 20 tilings, '20'.", "TilesToPaths:4:0.95", "reuse"),
 ("6.5", "A bigger box, three ants: nine hundred eighty. Mountain ranges that never touch: a table of Catalan numbers, determinant three, and there are exactly three.", "Boxes 980, then Catalan mountains.", "CatalanMountains:3:0.9", "reuse"),
 ("6.6", "And the Aztec diamond. Tile it with dominoes: two ways, then eight, then sixty-four. Guess the next. (pause) One thousand and twenty-four. Colour it like a chessboard, and the dominoes link into paths that never touch.", "Counts 2, 8, 64; dominoes become paths.", "AztecPaths:1:0.95", "reuse"),
 ("6.7", "Now pick one tiling at random, on a big diamond. The corners freeze into brick walls, the middle is chaos, and the boundary is a perfect circle. That's the picture we started with.", "Arctic circle grows to order 60; circle drawn. Callback to 0.1.", "ArcticCircle:2:0.95", "reuse"),
]),
("Act 7 · When it breaks", "Does it always work?", [
 ("7.1", "Back to the chessboard from the start. Shrink it to two by three: three tilings. A domino joins a black square to a white neighbour; put a one wherever they touch.", "2×3 board, table of 1s.", "SmallBoard2:1:0.9", "reuse"),
 ("7.2", "It should say three. It says minus one. The signs cancel the wrong things: plus for this tiling, minus for these two.", "det = −1, signs +, −, −.", "SmallBoard2:3:0.95", "reuse"),
 ("7.3", "In 1961 the physicist Pieter Kasteleyn had a fix: if the signs don't cancel the way you want, change the signs. Flip one edge: minus three. Three tilings.", "One edge turns orange; det = −3 ✓.", "SignFix2:2:0.95", "reuse"),
 ("7.4", "Four by four: the plain determinant says zero. Very confident, very wrong. Flip every other column: thirty-six. Right.", "4×4 board, |det| = 36.", "Board4x4:1:0.95", "reuse"),
 ("7.5", "The full chessboard: twelve million, nine hundred eighty-eight thousand, eight hundred sixteen. The five-month count, in an instant.", "Callback to 0.5: the clock, then the number.", "FKT:0:0.95", "reuse + callback"),
 ("7.6", "And it works for any graph you can draw without crossings: the FKT algorithm counts perfect matchings in polynomial time.", "Squares → dots, dominoes → edges; planar graph; FKT card.", "FKT:3:0.95", "reuse"),
]),
("Act 8 · Why it matters", "So what?", [
 ("8.1", "Step back. Ants, hexagons, boxes, mountains, diamonds, chessboards. Every time, the same move: count everything, good and bad, with signs, and let the bad ones cancel in pairs.", "The map around 'det', then the 52 signed pairs cancelling to 20.", "Map:0:0.95", "reuse"),
 ("8.2", "For a computer scientist, that's remarkable. Counting is usually hopeless: counting perfect matchings of a general graph is #P-complete. But turn a problem into non-touching paths, or a planar matching, and it's a single determinant.", "#P-complete vs one determinant.", "Finale:3:0.9", "reuse"),
 ("8.3", "Determinants can count, because minus signs can cancel.", "Thesis line.", "Finale:4:0.95", "reuse"),
 ("8.4", "As for our ants: twenty ways home, and they never had to meet. Thanks for watching.", "Ants walk home, wave. Callback to Act 1.", "Goodbye:0:0.95", "reuse"),
]),
]

words = 0
html = ["""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Storyboard v6</title><style>
:root{--bg:#111;--fg:#eee;--soft:#aaa;--acc:#f2c94c;--card:#1c1c1c}
body{background:var(--bg);color:var(--fg);font:16px/1.5 Georgia,serif;margin:0;padding:24px 16px;max-width:1100px;margin:auto}
h1{font-size:28px}h2{color:var(--acc);margin-top:48px;border-bottom:1px solid #333;padding-bottom:6px}
.q{color:var(--soft);font-style:italic;margin:-6px 0 16px}
.beat{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:18px;background:var(--card);border-radius:10px;padding:14px;margin:12px 0}
.beat img{width:100%;border-radius:6px;display:block}
.id{color:var(--acc);font-weight:bold}.n{font-size:18px;margin:4px 0 10px}.v{color:var(--soft);font-size:14px}
.tag{display:inline-block;font-size:12px;padding:1px 8px;border-radius:9px;background:#333;margin-top:8px}
.tag.new{background:#2f5d3a}
@media(max-width:700px){.beat{grid-template-columns:1fr}}
</style></head><body>
<h1>How Determinants Can Count: storyboard v6</h1>
<p class="v">Each beat: what is said (large), what is shown (grey), and a picture. "reuse" pictures are frames from the current cut; "new" pictures are rough mockups of animations still to build.</p>"""]
for act, q, beats in S:
    html.append(f"<h2>{act}</h2><div class='q'>Viewer's question: {q}</div>")
    for i, n, v, src, st in beats:
        words += len(n.split())
        cls = "tag new" if st.startswith("new") else "tag"
        html.append(f"<div class='beat'><img src='data:image/jpeg;base64,{img(src)}' alt='{i}'><div><span class='id'>{i}</span>"
                    f"<div class='n'>{n}</div><div class='v'>{v}</div><span class='{cls}'>{st}</span></div></div>")
html.append(f"<p class='v'>Narration: {words} words ≈ {words/150:.1f} min of speech; with animation and pauses the video runs about 15–17 min.</p></body></html>")
open("storyboard/index.html", "w").write("\n".join(html))
# plain script too
with open("storyboard/script_v6.md", "w") as fh:
    for act, q, beats in S:
        fh.write(f"## {act}\n*Viewer's question: {q}*\n\n")
        for i, n, v, src, st in beats:
            fh.write(f"**{i}** {n}\n> {v}\n\n")
print(words, "words")
