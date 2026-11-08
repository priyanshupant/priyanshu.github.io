"""Silent visual drafts of other places the sign-and-cancel trick (D.I.E.) works, for Priyanshu to choose from.

    Subsets     even-sized vs odd-sized subsets of {1,2,3,4}: toggle the 1 -> every subset pairs with one of
                the other parity -> nothing left: sum of (-1)^k C(4,k) = 0     (Benjamin & Quinn, first example)
    Fibonacci   tilings of length 1..4 by squares and dominoes, sign (-1)^length; toggle the LAST tile
                (square <-> domino) -> left: length-4 tilings ending in a square: -1 + 2 - 3 + 5 = 3 (Benjamin & Quinn)
    Trees       a square with one diagonal has 8 spanning trees = det of its reduced Laplacian (Kirchhoff)
All numbers checked at import.
"""
from itertools import combinations
from common import *

# --- subsets
SUBS = [frozenset(c) for k in range(5) for c in combinations(range(1, 5), k)]
EVEN = [s for s in SUBS if len(s) % 2 == 0]
ODD = [s for s in SUBS if len(s) % 2 == 1]
TOG = {s: s ^ {1} for s in SUBS}
assert len(EVEN) == len(ODD) == 8 and all(TOG[TOG[s]] == s and len(TOG[s]) % 2 != len(s) % 2 for s in SUBS)

# --- Fibonacci tilings (S = square, D = domino)
def tilings(n):
    if n == 0:
        return [""]
    out = [t + "S" for t in tilings(n - 1)]
    if n >= 2:
        out += [t + "D" for t in tilings(n - 2)]
    return out


def length(t):
    return sum(1 if c == "S" else 2 for c in t)


ALL = [t for n in range(1, 5) for t in tilings(n)]
def toggle(t):
    return t[:-1] + ("D" if t[-1] == "S" else "S")
EXC = [t for t in ALL if length(t) == 4 and t[-1] == "S"]
assert [len(tilings(n)) for n in range(1, 5)] == [1, 2, 3, 5]
assert all(toggle(toggle(t)) == t for t in ALL)
assert all(toggle(t) in ALL for t in ALL if t not in EXC) and len(EXC) == 3
assert sum((-1) ** length(t) for t in ALL) == 3 == len(EXC)

# --- spanning trees of a square with one diagonal (a-b-c-d-a, plus a-c)
V = ["a", "b", "c", "d"]
E = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "a"), ("a", "c")]
def is_tree(es):
    parent = {v: v for v in V}
    def f(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for u, w in es:
        ru, rw = f(u), f(w)
        if ru == rw:
            return False
        parent[ru] = rw
    return True
TREES = [es for es in combinations(E, 3) if is_tree(es)]
LAP = np.array([[3, -1, -1], [-1, 2, -1], [-1, -1, 3]], float)       # rows/cols a, b, c (d removed)
assert len(TREES) == 8 == round(np.linalg.det(LAP))


def subset_mob(s, col):
    return VGroup(*[T(str(i), 26, YELLOW if i == 1 else col) for i in sorted(s)] or [T("∅", 26, col)]).arrange(RIGHT, buff=0.12)


def strip(t, u=0.32, col=TEAL):
    g = VGroup()
    x = 0
    for c in t:
        w = u if c == "S" else 2 * u
        g.add(RoundedRectangle(width=w - 0.04, height=u - 0.04, corner_radius=0.05, fill_color=col if c == "S" else ORANGE,
                               fill_opacity=0.85, stroke_color=WHITE, stroke_width=1.5).move_to(RIGHT * (x + w / 2)))
        x += w
    return g


class ExamplesDraft(DScene):
    def construct(self):
        # ---------------- 1. subsets
        cap = T("1 · Even subsets = odd subsets", 34, YELLOW).to_edge(UP, buff=0.35)
        self.play(FadeIn(cap), run_time=0.5)
        hdr = VGroup(T("even size  (+)", 28, GOOD), T("odd size  (−)", 28, BAD)).arrange(RIGHT, buff=3.2).next_to(cap, DOWN, buff=0.4)
        colE = VGroup(*[subset_mob(s, GOOD) for s in EVEN]).arrange(DOWN, buff=0.18).next_to(hdr[0], DOWN, buff=0.3)
        colO = VGroup(*[subset_mob(TOG[s], BAD) for s in EVEN]).arrange(DOWN, buff=0.18).next_to(hdr[1], DOWN, buff=0.3)
        for a, b in zip(colE, colO):
            b.match_y(a)
        self.play(FadeIn(hdr), LaggedStartMap(FadeIn, colE, lag_ratio=0.1), LaggedStartMap(FadeIn, colO, lag_ratio=0.1), run_time=1.6)
        rule = T("rule: put the 1 in, or take it out", 26, YELLOW).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(rule), run_time=0.5)
        links = VGroup(*[Line(a.get_right() + RIGHT * 0.15, b.get_left() + LEFT * 0.15, color=YELLOW, stroke_width=3) for a, b in zip(colE, colO)])
        self.play(LaggedStartMap(Create, links, lag_ratio=0.15), run_time=1.6)
        self.wait(0.4)
        self.play(*[FadeOut(VGroup(a, b, l), scale=0.3) for a, b, l in zip(colE, colO, links)], run_time=0.9)
        res = MathTex(r"\binom40-\binom41+\binom42-\binom43+\binom44 = 0", color=YELLOW).scale(0.9)
        self.play(Write(res), run_time=1.0)
        self.wait(1.2)
        self.play(FadeOut(VGroup(cap, hdr, rule, res)), run_time=0.5)

        # ---------------- 2. Fibonacci tilings
        cap = T("2 · Tilings with squares and dominoes", 34, YELLOW).to_edge(UP, buff=0.35)
        self.play(FadeIn(cap), run_time=0.5)
        rows = VGroup()
        mobs = {}
        for n in range(1, 5):
            sg = T("+" if n % 2 == 0 else "−", 34, GOOD if n % 2 == 0 else BAD)
            ts = VGroup()
            for t in tilings(n):
                m = strip(t)
                mobs[t] = m
                ts.add(m)
            ts.arrange(RIGHT, buff=0.35)
            rows.add(VGroup(T(f"length {n}", 24, SOFT), sg, ts).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(cap, DOWN, buff=0.5).set_x(-0.5)
        self.play(LaggedStartMap(FadeIn, rows, lag_ratio=0.2), run_time=1.5)
        rule = T("rule: flip the last tile  (square ↔ domino)", 26, YELLOW).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(rule), run_time=0.5)
        done = set()
        pairs = []
        for t in ALL:
            if t in EXC or t in done:
                continue
            u = toggle(t)
            done |= {t, u}
            pairs.append((t, u))
        for t, u in pairs:
            ln = Line(mobs[t].get_bottom(), mobs[u].get_top(), color=YELLOW, stroke_width=3) \
                if mobs[t].get_y() > mobs[u].get_y() else Line(mobs[t].get_top(), mobs[u].get_bottom(), color=YELLOW, stroke_width=3)
            self.play(Create(ln), Indicate(mobs[t], color=YELLOW), Indicate(mobs[u], color=YELLOW), run_time=0.5)
            self.play(FadeOut(VGroup(mobs[t], mobs[u], ln), scale=0.3), run_time=0.35)
        left = VGroup(*[mobs[t] for t in EXC])
        self.play(Indicate(left, color=GOOD, scale_factor=1.15), run_time=0.8)
        res = MathTex(r"-1 + 2 - 3 + 5 = 3", color=YELLOW).scale(0.95).next_to(rows, DOWN, buff=0.35)
        self.play(Write(res), run_time=0.9)
        self.wait(1.2)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.5)

        # ---------------- 3. spanning trees (a determinant again)
        cap = T("3 · Spanning trees (Kirchhoff)", 34, YELLOW).to_edge(UP, buff=0.35)
        self.play(FadeIn(cap), run_time=0.5)
        pos = {"a": np.array([-1, 1, 0]), "b": np.array([1, 1, 0]), "c": np.array([1, -1, 0]), "d": np.array([-1, -1, 0])}
        def gmob(es, sc=0.55, c=ORIGIN, col=YELLOW):
            return VGroup(*[Line(c + sc * pos[u], c + sc * pos[w], color=col, stroke_width=4) for u, w in es],
                          *[Dot(c + sc * pos[v], radius=0.06) for v in V])
        big = gmob(E, 1.0, LEFT * 4.5 + UP * 0.2, GREY_B)
        self.play(FadeIn(big), run_time=0.6)
        thumbs = VGroup(*[gmob(es, 0.38) for es in TREES]).arrange_in_grid(2, 4, buff=0.35).move_to(RIGHT * 2.2 + UP * 0.9)
        self.play(LaggedStartMap(FadeIn, thumbs, lag_ratio=0.15), run_time=1.6)
        det = MathTex(r"\det\begin{bmatrix}3&-1&-1\\-1&2&-1\\-1&-1&3\end{bmatrix} = 8", color=YELLOW).scale(0.85).next_to(thumbs, DOWN, buff=0.5)
        self.play(Write(det), run_time=1.2)
        self.wait(1.5)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.5)
