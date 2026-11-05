"""Act 6c — The arctic circle: a uniformly random domino tiling of a big Aztec diamond.

    ArcticCircle   domino shuffling grows a random tiling from order 1 to 60; the frozen
                   corners and the circle (Jockusch–Propp–Shor 1995).

Domino shuffling (Elkies–Kuperberg–Larsen–Propp) with fair coins samples tilings
uniformly; checked at import: every step is a valid tiling, and order-2 samples hit
all 8 tilings.
"""
import os
import random

from PIL import Image, ImageDraw

from common import *

ORDER = 60


def cells(n):
    return {(x, y) for x in range(-n, n) for y in range(-n, n) if abs(x + 0.5) + abs(y + 0.5) <= n}


def shuffle_step(tiles, n, rng):
    """tiles: {(x, y, kind): dir} with kind 'h' (covers (x,y),(x+1,y)) or 'v' (covers (x,y),(x,y+1));
    dir in N S E W. Returns the order n+1 tiling."""
    t = dict(tiles)
    # 1. destroy: pairs that would collide (N below S, E left of W)
    for (x, y, k), d in list(tiles.items()):
        if (x, y, k) not in t:
            continue
        if k == "h" and d == "N" and t.get((x, y + 1, "h")) == "S":
            del t[(x, y, k)], t[(x, y + 1, "h")]
        elif k == "v" and d == "E" and t.get((x + 1, y, "v")) == "W":
            del t[(x, y, k)], t[(x + 1, y, "v")]
    # 2. slide
    mv = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}
    out = {}
    for (x, y, k), d in t.items():
        dx, dy = mv[d]
        out[(x + dx, y + dy, k)] = d
    # 3. create: fill the empty 2x2 blocks
    cov = set()
    for (x, y, k) in out:
        cov |= {(x, y), (x + 1, y)} if k == "h" else {(x, y), (x, y + 1)}
    C = cells(n + 1)
    assert cov <= C, "slide left the diamond"
    for (x, y) in sorted(C - cov, key=lambda p: (p[1], p[0])):
        if (x, y) in cov:
            continue
        blk = {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}
        assert blk <= C and not (blk & cov), "hole is not a 2x2 block"
        if rng.random() < 0.5:
            out[(x, y, "h")], out[(x, y + 1, "h")] = "S", "N"
        else:
            out[(x, y, "v")], out[(x + 1, y, "v")] = "W", "E"
        cov |= blk
    assert cov == C
    return out


def grow(order, seed=7):
    rng = random.Random(seed)
    t, seq = {}, []
    for n in range(order):
        t = shuffle_step(t, n, rng)
        seq.append(t)
    return seq


# sanity: uniform-ish over the 8 order-2 tilings
_seen = {frozenset(grow(2, seed=s)[-1]) for s in range(400)}
assert len(_seen) == 8, len(_seen)

COLS = {"N": "#C0392B", "S": "#2471A3", "E": "#229954", "W": "#D4AC0D"}


def tiling_png(t, n, path, px=8):
    W = 2 * n * px
    im = Image.new("RGB", (W, W), (0, 0, 0))
    dr = ImageDraw.Draw(im)
    for (x, y, k), d in t.items():
        w, h = (2, 1) if k == "h" else (1, 2)
        x0, y0 = (x + n) * px, (n - (y + h)) * px
        dr.rectangle([x0, y0, x0 + w * px - 1, y0 + h * px - 1], fill=COLS[d], outline=(20, 20, 20))
    im.save(path)
    return path


class ArcticCircle(DScene):
    def construct(self):
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media", "arctic")
        os.makedirs(out, exist_ok=True)
        seq = grow(ORDER)
        H = 6.6
        center = LEFT * 2.6 + DOWN * 0.25
        title = T("A random tiling", 38).to_corner(UR, buff=0.5)
        sub = T("every tiling equally likely", 26, SOFT).next_to(title, DOWN, buff=0.15).align_to(title, RIGHT)
        # 0: grow by shuffling
        self.cue(0)
        self.play(FadeIn(title), FadeIn(sub))
        cur = None
        ordlab = T("order 1", 30, YELLOW).next_to(sub, DOWN, buff=0.5).align_to(title, RIGHT)
        self.add(ordlab)
        for n in range(1, ORDER + 1):
            if n > 12 and n % 2 and n != ORDER:
                continue
            f = tiling_png(seq[n - 1], n, os.path.join(out, f"az{n:03d}.png"), px=max(4, 480 // n))
            im = ImageMobject(f).set_height(H * n / ORDER).move_to(center)
            new_lab = T(f"order {n}", 30, YELLOW).move_to(ordlab, aligned_edge=RIGHT)
            if cur is not None:
                self.remove(cur)
            self.remove(ordlab)
            ordlab = new_lab
            self.add(im, ordlab)
            cur = im
            self.wait(0.18 if n <= 12 else 0.1)
        # 1: order 60
        self.cue(1)
        self.play(Indicate(ordlab, color=YELLOW))
        # 2: frozen corners, chaos inside, and a circle
        self.cue(2)
        frozen = T("frozen corners", 28).next_to(ordlab, DOWN, buff=0.6).align_to(title, RIGHT)
        chaos = T("chaos inside", 28).next_to(frozen, DOWN, buff=0.2).align_to(title, RIGHT)
        self.play(FadeIn(frozen))
        self.play(FadeIn(chaos))
        circ = Circle(radius=H / (2 * np.sqrt(2)), color=WHITE, stroke_width=6) \
            .move_to(center)
        self.sfx("chime")
        self.play(Create(circ), run_time=2)
        circ_l = T("a perfect circle", 32, YELLOW).next_to(chaos, DOWN, buff=0.4).align_to(title, RIGHT)
        self.play(FadeIn(circ_l))
        # 3: name
        self.cue(3)
        thm = VGroup(T("the arctic circle theorem", 28, YELLOW),
                     T("Jockusch, Propp, Shor (1995)", 24, SOFT)).arrange(DOWN, buff=0.1, aligned_edge=RIGHT)
        thm.to_corner(DR, buff=0.5)
        self.play(FadeIn(thm))
        self.play(circ.animate.set_stroke(opacity=0.0), run_time=1.5)
