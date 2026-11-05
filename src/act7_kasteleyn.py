"""Act 7 — When signs don't cooperate: Kasteleyn (11:45-14:00).

    Chessboard   dominoes fill a chessboard; 12,988,816 tilings
    SmallBoard   2x3 board, 3 tilings, the 0/1 table, perm = 3, det = -1, signs
    SignFix      one minus sign on the b3-w1 edge: det = -3; the pattern on 8x8; credits
"""
import random

from common import *

DARK_SQ, LIGHT_SQ = "#3A3A3A", "#CFCFCF"
DOMINO = TEAL
FLIP = ORANGE
# 2x3 board: (row, col) -> name. Top-left is black.
NAMES = {(0, 0): "b₁", (0, 1): "w₁", (0, 2): "b₂", (1, 0): "w₂", (1, 1): "b₃", (1, 2): "w₃"}
TILINGS = [  # each domino as two cells
    [((0, 0), (1, 0)), ((0, 1), (1, 1)), ((0, 2), (1, 2))],     # three vertical
    [((0, 0), (1, 0)), ((0, 1), (0, 2)), ((1, 1), (1, 2))],     # vertical left + two horizontal
    [((0, 0), (0, 1)), ((1, 0), (1, 1)), ((0, 2), (1, 2))],     # two horizontal + vertical right
]
TABLE = [[1, 1, 0], [1, 0, 1], [1, 1, 1]]   # rows b1..b3, cols w1..w3
B_ORDER = [(0, 0), (0, 2), (1, 1)]
W_ORDER = [(0, 1), (1, 0), (1, 2)]


def board(rows, cols, s, origin=ORIGIN, labels=False):
    g = VGroup()
    sq = {}
    for r in range(rows):
        for c in range(cols):
            dark = (r + c) % 2 == 0
            q = Square(s, stroke_width=1, stroke_color=GREY_C, fill_opacity=1,
                       fill_color=DARK_SQ if dark else LIGHT_SQ).move_to(origin + RIGHT * c * s + DOWN * r * s)
            sq[(r, c)] = q
            g.add(q)
            if labels:
                g.add(T(NAMES[(r, c)], 30 * s / 1.1, WHITE if dark else BLACK).move_to(q))
    g.sq = sq
    return g


def domino(sq, a, b, s, color=DOMINO):
    pa, pb = sq[a].get_center(), sq[b].get_center()
    w = abs(pa[0] - pb[0]) + s * 0.82
    h = abs(pa[1] - pb[1]) + s * 0.82
    return RoundedRectangle(corner_radius=s * 0.15, width=w, height=h, fill_color=color, fill_opacity=0.85,
                            stroke_color=WHITE, stroke_width=2).move_to((pa + pb) / 2)


def random_tiling(rows, cols, seed):
    rng = random.Random(seed)
    while True:
        cov, out = set(), []
        ok = True
        for r in range(rows):
            for c in range(cols):
                if (r, c) in cov:
                    continue
                opts = []
                if c + 1 < cols and (r, c + 1) not in cov:
                    opts.append((r, c + 1))
                if r + 1 < rows:
                    opts.append((r + 1, c))
                if not opts:
                    ok = False
                    break
                o = rng.choice(opts)
                cov |= {(r, c), o}
                out.append(((r, c), o))
            if not ok:
                break
        if ok:
            return out
        seed += 1
        rng = random.Random(seed)


def table_mob(entries, size=40):
    cells = VGroup(*[T(str(v), size) for row in entries for v in row]).arrange_in_grid(3, 3, buff=(0.75, 0.45))
    rl = VGroup(*[T(n, 30, SOFT).next_to(cells[3 * k], LEFT, buff=0.55) for k, n in enumerate(["b₁", "b₂", "b₃"])])
    cl = VGroup(*[T(n, 30, SOFT).next_to(cells[k], UP, buff=0.4) for k, n in enumerate(["w₁", "w₂", "w₃"])])
    g = VGroup(cells, rl, cl)
    g.cells = cells
    return g


def entry_index(a, b):
    """Table cell index for a domino covering cells a and b."""
    bl, wh = (a, b) if a in B_ORDER else (b, a)
    return 3 * B_ORDER.index(bl) + W_ORDER.index(wh)


class Chessboard(DScene):
    def construct(self):
        skip = T("Slightly more technical. Feel free to skip to 14:00.", 22, SOFT).to_corner(UR, buff=0.3)
        self.add(skip)
        s = 0.72
        b = board(8, 8, s, origin=LEFT * 5.6 + UP * 2.5)
        self.play(FadeIn(b, lag_ratio=0.01), run_time=1.5)
        doms = VGroup(*[domino(b.sq, x, y, s) for x, y in random_tiling(8, 8, 3)])
        self.play(LaggedStartMap(FadeIn, doms, lag_ratio=0.04, scale=0.6), run_time=3)
        self.wait(1)
        rng = random.Random(1)
        num = T("0", 64, YELLOW).move_to(RIGHT * 3.3 + UP * 0.4)
        lab = T("ways to tile it", 32).next_to(num, DOWN, buff=0.4)
        self.play(FadeIn(lab))
        for k in range(14):
            self.remove(num)
            num = T(f"{rng.randint(10**6, 10**8):,}", 64, YELLOW).move_to(RIGHT * 3.3 + UP * 0.4)
            self.add(num)
            Scene.wait(self, 1 / 15)      # not stretched by pacing
        self.remove(num)
        num = T("12,988,816", 64, YELLOW, weight=BOLD).move_to(RIGHT * 3.3 + UP * 0.4)
        self.sfx("chime")
        self.play(FadeIn(num, scale=1.3))
        self.wait(2)
        no = T("counting one by one: not an option", 26, SOFT).next_to(lab, DOWN, buff=0.4)
        self.play(FadeIn(no))
        self.wait(3)


class SmallBoard(DScene):
    def construct(self):
        s = 1.1
        b = board(2, 3, s, origin=LEFT * 4.6 + UP * 2.1, labels=True)
        title = T("a tiny board: 2 × 3", 32).next_to(b, UP, buff=0.3)
        self.play(FadeIn(b), Write(title))
        self.wait(1)
        # its three tilings
        small = VGroup()
        for k, t in enumerate(TILINGS):
            bb = board(2, 3, 0.5)
            bb.add(*[domino(bb.sq, x, y, 0.5) for x, y in t])
            small.add(bb)
        small.arrange(RIGHT, buff=0.6).move_to(LEFT * 3.4 + DOWN * 1.7)
        self.play(LaggedStartMap(FadeIn, small, lag_ratio=0.4, shift=UP * 0.2), run_time=2)
        three = T("3 tilings", 30, YELLOW).next_to(small, UP, buff=0.25)
        self.play(FadeIn(three))
        self.wait(2)
        idea = T("each domino = one black + one white neighbour", 26, SOFT).next_to(b, DOWN, buff=0.35)
        self.play(FadeIn(idea))
        self.wait(2)

        tab = table_mob(TABLE).move_to(RIGHT * 3.6 + UP * 1.4)
        ttl = T("1 where b and w are neighbours", 24, SOFT).next_to(tab, UP, buff=0.35)
        self.play(FadeIn(tab[1]), FadeIn(tab[2]), FadeIn(ttl))
        self.play(LaggedStartMap(FadeIn, tab.cells, lag_ratio=0.12), run_time=1.5)
        self.wait(1)
        # each tiling lights up its three 1s
        for k, t in enumerate(TILINGS):
            frame = SurroundingRectangle(small[k], color=YELLOW, buff=0.08)
            marks = VGroup(*[SurroundingRectangle(tab.cells[entry_index(x, y)], color=YELLOW, buff=0.12)
                             for x, y in t])
            self.play(Create(frame), Create(marks), run_time=0.6)
            self.wait(0.8)
            self.play(FadeOut(frame), FadeOut(marks), run_time=0.3)
        self.wait(1)

        perm = VGroup(T("permanent = 3", 34, GOOD), tick(0.35)).arrange(RIGHT, buff=0.3)
        det = VGroup(T("determinant = −1", 34, BAD), cross(0.35)).arrange(RIGHT, buff=0.3)
        res = VGroup(perm, det).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(tab, DOWN, buff=0.6)
        self.play(FadeIn(perm))
        card = villain_card("THE PERMANENT", 28).move_to(RIGHT * 1.5 + DOWN * 3.35)
        right = T("is right this time!", 24, BAD).next_to(card, RIGHT, buff=0.3)
        self.sfx("rumble")
        self.play(FadeIn(card, scale=1.4), FadeIn(right))
        self.wait(2)
        self.sfx("buzz")
        self.play(FadeIn(det))
        self.wait(2)
        # signs of the three tilings in the determinant
        signs = VGroup(*[T(sg, 44, GOOD if sg == "+" else BAD).next_to(small[k], DOWN, buff=0.2)
                         for k, sg in enumerate(["+", "−", "−"])])
        self.play(LaggedStartMap(FadeIn, signs, lag_ratio=0.3, scale=1.5))
        self.wait(1)
        self.play(Indicate(VGroup(small[0], signs[0]), color=YELLOW, scale_factor=1.15), run_time=1.2)
        odd = T("+1 − 1 − 1 = −1\nthe cancellation works against us", 24, SOFT, line_spacing=1.1) \
            .next_to(small, DOWN, buff=0.75)
        self.play(FadeIn(odd))
        self.wait(4)


class SignFix(DScene):
    def construct(self):
        s = 1.1
        b = board(2, 3, s, origin=LEFT * 4.6 + UP * 1.6, labels=True)
        self.add(b)
        # the graph on top: one node per square, one edge per neighbouring pair
        nodes = {k: b.sq[k].get_center() for k in b.sq}
        edges = {}
        for (r, c) in b.sq:
            for (dr, dc) in ((0, 1), (1, 0)):
                o = (r + dr, c + dc)
                if o in b.sq:
                    edges[((r, c), o)] = Line(nodes[(r, c)], nodes[o], color=YELLOW, stroke_width=4)
        g = VGroup(*edges.values(), *[Dot(p, radius=0.07, color=YELLOW) for p in nodes.values()])
        self.play(Create(g), run_time=1.5)
        self.wait(1)
        idea = T("Kasteleyn: if the signs don't cancel\nthe way we want, change the signs.",
                 30, YELLOW, line_spacing=1.15).to_edge(UP, buff=0.4).shift(RIGHT * 2.3)
        self.play(Write(idea), run_time=2)
        self.wait(2)
        e = edges[((0, 1), (1, 1))]
        minus = T("−", 54, FLIP, weight=BOLD).next_to(e, RIGHT, buff=0.12)
        self.sfx("flip")
        self.play(e.animate.set_color(FLIP).set_stroke(width=9), FadeIn(minus, scale=2))
        self.wait(1)

        tab = table_mob(TABLE).move_to(RIGHT * 3.6 + DOWN * 0.4)
        self.play(FadeIn(tab))
        k = entry_index((0, 1), (1, 1))
        new = T("−1", 40, FLIP).move_to(tab.cells[k])
        self.play(Transform(tab.cells[k], new))
        self.wait(1)
        small = VGroup()
        for t in TILINGS:
            bb = board(2, 3, 0.45)
            bb.add(*[domino(bb.sq, x, y, 0.45) for x, y in t])
            small.add(bb)
        small.arrange(RIGHT, buff=0.5).move_to(LEFT * 3.6 + DOWN * 1.6)
        old = VGroup(*[T(sg, 40, GOOD if sg == "+" else BAD).next_to(small[k], DOWN, buff=0.15)
                       for k, sg in enumerate(["+", "−", "−"])])
        self.play(FadeIn(small), FadeIn(old))
        self.wait(1)
        only = T("only the all-vertical tiling uses that edge", 22, SOFT).next_to(small, UP, buff=0.2)
        self.play(FadeIn(only), Indicate(small[0], color=FLIP))
        self.play(Transform(old[0], T("−", 40, BAD).move_to(old[0])))
        self.wait(1)
        res = VGroup(T("determinant = −3", 34, YELLOW),
                     VGroup(T("size = 3", 34, GOOD), tick(0.35)).arrange(RIGHT, buff=0.3)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, DOWN, buff=0.5)
        self.play(FadeIn(res[0]))
        self.sfx("chime")
        self.play(FadeIn(res[1]))
        fast = T("correct, and fast", 26, GOOD).next_to(res, DOWN, buff=0.3)
        self.play(FadeIn(fast))
        self.wait(3)

        # the pattern on the big board
        self.play(*[FadeOut(x) for x in self.mobjects])
        s2 = 0.6
        big = board(8, 8, s2, origin=LEFT * 5.6 + UP * 2.1)
        nodes = {k: big.sq[k].get_center() for k in big.sq}
        gl = VGroup()
        for (r, c) in big.sq:
            if c + 1 < 8:
                gl.add(Line(nodes[(r, c)], nodes[(r, c + 1)], color=YELLOW, stroke_width=2))
            if r + 1 < 8:
                gl.add(Line(nodes[(r, c)], nodes[(r + 1, c)], color=FLIP if c % 2 else YELLOW,
                            stroke_width=4 if c % 2 else 2))
        self.play(FadeIn(big), run_time=0.8)
        self.play(Create(gl, lag_ratio=0.01), run_time=2.5)
        pat = T("minus signs on every other\ncolumn of vertical edges", 26, FLIP, line_spacing=1.15) \
            .move_to(RIGHT * 3.3 + UP * 2.2)
        self.play(FadeIn(pat))
        num = T("12,988,816", 60, YELLOW, weight=BOLD).move_to(RIGHT * 3.3 + UP * 0.4)
        lab = T("|det| = number of tilings", 26).next_to(num, DOWN, buff=0.3)
        self.play(FadeIn(num, scale=1.3), FadeIn(lab))
        self.wait(2)
        cred = VGroup(T("P. W. Kasteleyn, 1961", 30),
                      T("Temperley & Fisher, the same year", 24, SOFT),
                      T("works for any graph drawn without crossings", 22, SOFT)) \
            .arrange(DOWN, buff=0.15).next_to(lab, DOWN, buff=0.6)
        self.play(FadeIn(cred, lag_ratio=0.3))
        self.wait(2)
        design = T("cancellation by design", 36, YELLOW).to_edge(DOWN, buff=0.4).shift(RIGHT * 3.3)
        self.play(Write(design))
        self.wait(3)
