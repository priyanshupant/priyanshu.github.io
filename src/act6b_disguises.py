"""Act 6b — The same paths in disguise.

    BoxesCorner        hexagon tilings = boxes stacked in a corner; 3x3x3 box: 3 walkers, det = 980
    CatalanMountains   two non-touching mountain ranges: det [[2,5],[5,14]] = 3, all three shown
    AztecIntro         the Aztec diamond and its domino tilings (2, 8, ...)
    AztecPaths         dominoes -> non-touching paths; det [[12,4],[4,2]] = 8; order 3: 64; 2^(n(n+1)/2)

All counts are checked in code at import (research/aztec.py, research/catalan_boxes.py).
"""
from fractions import Fraction as Fr
from itertools import product
from math import comb

from common import *
from act6_hexagon import tiling, outline, chain, partitions, contour, proj

# ------------------------------------------------------------------ boxes
BOX3 = (3, 3, 3)
PART3 = partitions(*BOX3)
assert len(PART3) == 980


def box_walker(h, z, box=BOX3):
    a, b, c = box
    return [(i + (c - 1 - z), b - j + z) for i, j in contour(h, z, box)]


class BoxesCorner(DScene):
    def construct(self):
        title = T("Tilings of a hexagon = boxes stacked in a corner", 32).to_edge(UP, buff=0.4)
        self.cue(0)
        self.play(Write(title))
        c, s = LEFT * 3.4 + DOWN * 0.5, 0.75
        hexo = outline(s, c, BOX3)
        empty = tuple(tuple(0 for _ in range(3)) for _ in range(3))
        til = tiling(empty, s, c, box=BOX3)
        self.play(Create(hexo), FadeIn(til))
        # stack cubes one at a time
        h = [[0] * 3 for _ in range(3)]
        order = [(0, 0), (0, 1), (1, 0), (0, 0), (1, 1), (0, 2), (2, 0), (0, 1), (0, 0)]
        for i, j in order:
            h[i][j] += 1
            self.play(Transform(til, tiling(tuple(map(tuple, h)), s, c, box=BOX3)), run_time=0.35)
        self.cue(1)
        H = tuple(map(tuple, h))
        note = T("a 3 × 3 × 3 box: 3 walkers", 26, YELLOW).move_to(RIGHT * 3 + UP * 2.4)
        self.play(FadeIn(note))
        for t in til:
            if t.kind == "T":
                t.set_fill(opacity=0).set_stroke(GREY_B, 1.2)
        cols = [ANT1, ANT2, ANT3]
        chs = [chain(H, z, s, c, cols[2 - z], BOX3, width=6) for z in range(3)]
        self.play(*[Create(ch) for ch in chs], run_time=1.6)
        lat = Lattice(6, spacing=0.55, center=RIGHT * 3.2 + DOWN * 0.6)
        paths = [path_mob(lat, box_walker(H, z), cols[2 - z], 6) for z in range(3)]
        self.play(FadeIn(lat))
        self.play(*[ReplacementTransform(chs[z].copy(), paths[z]) for z in range(3)], run_time=2)
        M = [[comb(6, 3 + z - zz) for zz in range(3)] for z in range(3)]
        d = round(np.linalg.det(np.array(M, float)))
        res = VGroup(T(f"3 × 3 determinant = {d}", 30, YELLOW), T("tilings, or stacks of boxes", 22, SOFT)) \
            .arrange(DOWN, buff=0.1).next_to(lat, DOWN, buff=0.3)
        self.cue(2)
        self.sfx("chime")
        self.play(FadeIn(res))
        self.cue(3)
        mac = VGroup(T("MacMahon (1915), any a × b × c box:", 24, SOFT),
                     T("∏  (i + j + k − 1) / (i + j + k − 2)", 28)).arrange(DOWN, buff=0.12).next_to(hexo, DOWN, buff=0.35)
        self.play(FadeIn(mac))


# ------------------------------------------------------------------ Catalan mountains
def dyck(a, b):
    out = []

    def rec(cur):
        x, y = cur[-1]
        if x == b[0]:
            if y == 0:
                out.append(tuple(cur))
            return
        for dy in (1, -1):
            if y + dy >= 0 and abs(y + dy) <= b[0] - x - 1:
                rec(cur + [(x + 1, y + dy)])
    rec([a])
    return out


CS = [(0, 0), (-2, 0)]
CE = [(4, 0), (6, 0)]
CM = [[len(dyck(s, e)) for e in CE] for s in CS]
CFAM = [f for f in product(*[dyck(CS[i], CE[i]) for i in range(2)])
        if len({q for p in f for q in p}) == sum(len(p) for p in f)]
assert CM == [[2, 5], [5, 14]] and len(CFAM) == 3


class CatalanMountains(DScene):
    def construct(self):
        title = T("Mountain ranges that never touch", 36).to_edge(UP, buff=0.4)
        self.cue(0)
        self.play(Write(title))
        rule = T("up or down each step, never below sea level", 24, SOFT).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(rule))
        u = 0.42

        def mtn(path, origin, col):
            pts = [origin + u * np.array([x, y, 0]) for x, y in path]
            line = VMobject(stroke_color=col, stroke_width=6).set_points_as_corners(pts)
            fill = Polygon(*pts, stroke_width=0, fill_color=col, fill_opacity=0.18)
            return VGroup(fill, line)
        panels = VGroup()
        for k, (inner, outer) in enumerate(CFAM):
            o = np.array([-5.2 + 4.6 * k, -1.5, 0])
            sea = Line(o + u * LEFT * 2.6, o + u * RIGHT * 6.6, color=BLUE_E, stroke_width=3)
            g = VGroup(sea, mtn(outer, o, ANT2), mtn(inner, o, ANT1))
            g.add(Dot(o + u * np.array([-2, 0, 0]), radius=0.06, color=ANT2), Dot(o, radius=0.06, color=ANT1),
                  Dot(o + u * np.array([4, 0, 0]), radius=0.06, color=ANT1), Dot(o + u * np.array([6, 0, 0]), radius=0.06, color=ANT2))
            panels.add(g)
        self.play(FadeIn(panels[0]))
        self.cue(1)
        q = T("how many ways?", 32, YELLOW).move_to(UP * 1.6)
        self.play(FadeIn(q))
        self.cue(2)
        cat = T("Catalan numbers:  1, 1, 2, 5, 14, 42, …", 30, SOFT).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(cat))
        m = matrix_mob(CM, size=40).move_to(UP * 1.5 + LEFT * 0.8)
        cl = VGroup(*[T(nm, 22, SOFT).next_to(c, DOWN, buff=0.05) for nm, c in zip(["C₂", "C₃", "C₃", "C₄"], m.cells)])
        d = T(f"det = {round(np.linalg.det(np.array(CM, float)))}", 36, YELLOW).next_to(m, RIGHT, buff=0.5)
        self.cue_at(2, "Put four")
        self.play(FadeOut(q), FadeIn(m), FadeIn(cl))
        self.sfx("chime")
        self.play(Write(d))
        self.cue(3)
        self.play(LaggedStart(FadeIn(panels[1]), FadeIn(panels[2]), lag_ratio=0.5), run_time=1.5)
        all3 = T("exactly 3", 32, YELLOW).next_to(panels, DOWN, buff=0.25)
        self.play(FadeIn(all3))


# ------------------------------------------------------------------ Aztec diamond
def az_cells(n):
    return {(x, y) for x in range(-n, n) for y in range(-n, n) if abs(x + 0.5) + abs(y + 0.5) <= n}


def az_tilings(n):
    C = az_cells(n)
    order = sorted(C)
    out = []

    def rec(cov, cur):
        free = next((c for c in order if c not in cov), None)
        if free is None:
            out.append(tuple(cur))
            return
        x, y = free
        for o in ((x + 1, y), (x, y + 1)):
            if o in C and o not in cov:
                rec(cov | {free, o}, cur + [(free, o)])
    rec(frozenset(), [])
    return out


def dtype(d):
    (x, y), (x2, y2) = d
    return ("H" if y2 == y else "V", (x + y) % 2)


RULE = {("H", 0): "F", ("H", 1): None, ("V", 0): "U", ("V", 1): "D"}
TYPE_COL = {("H", 0): TEAL_D, ("H", 1): GREY_D, ("V", 0): GOLD_D, ("V", 1): MAROON_D}


def az_segment(d):
    (x, y), _ = d
    k = RULE[dtype(d)]
    if k == "F":
        return (x, y + 0.5), (x + 2, y + 0.5)
    if k == "U":
        return (x, y + 0.5), (x + 1, y + 1.5)
    if k == "D":
        return (x, y + 1.5), (x + 1, y + 0.5)
    return None


AZ = {n: az_tilings(n) for n in (1, 2, 3)}
assert [len(AZ[n]) for n in (1, 2, 3)] == [2, 8, 64]


def az_mob(t, n, u, c, with_paths=True, colored=True):
    g = VGroup()
    for d in t:
        (x, y), (x2, y2) = d
        w, h = (2, 1) if y2 == y else (1, 2)
        r = Rectangle(width=w * u * 0.94, height=h * u * 0.94, stroke_color=WHITE, stroke_width=1.5,
                      fill_color=TYPE_COL[dtype(d)] if colored else GREY_D, fill_opacity=0.85)
        r.move_to(c + u * np.array([x + w / 2, y + h / 2, 0]))
        g.add(r)
    paths = VGroup()
    if with_paths:
        for d in t:
            sg = az_segment(d)
            if sg:
                a, b = sg
                paths.add(Line(c + u * np.array([*a, 0]), c + u * np.array([*b, 0]), color=WHITE, stroke_width=5))
    return VGroup(g, paths)


class AztecIntro(DScene):
    def construct(self):
        title = T("The Aztec diamond", 40).to_edge(UP, buff=0.4)
        self.cue(0)
        self.play(Write(title))
        u = 0.6
        c = LEFT * 3.2 + DOWN * 0.4
        cells = VGroup(*[Square(u, stroke_color=GREY_B, stroke_width=1.5).move_to(c + u * np.array([x + 0.5, y + 0.5, 0]))
                         for x, y in az_cells(3)])
        self.play(LaggedStartMap(Create, cells, lag_ratio=0.02), run_time=1.5)
        rows = T("rows of 2, 4, 6, 6, 4, 2 squares", 24, SOFT).next_to(cells, DOWN, buff=0.3)
        self.play(FadeIn(rows))
        self.cue(1)
        t = AZ[3][17]
        dom = az_mob(t, 3, u, c, with_paths=False, colored=False)[0]
        self.play(LaggedStartMap(FadeIn, dom, lag_ratio=0.05), run_time=1.5)
        counts = VGroup(*[VGroup(T(f"order {n}", 24, SOFT), T(str(len(AZ[n])), 34, YELLOW)).arrange(DOWN, buff=0.1)
                          for n in (1, 2, 3)]).arrange(RIGHT, buff=0.8).move_to(RIGHT * 3.4 + UP * 1.6)
        tiny = VGroup(*[az_mob(tt, 1, 0.42, ORIGIN, with_paths=False, colored=False)[0] for tt in AZ[1]]) \
            .arrange(RIGHT, buff=0.4).move_to(RIGHT * 3.4 + DOWN * 0.6)
        self.cue_at(1, "smallest")
        self.play(FadeIn(counts[0]), FadeIn(tiny, lag_ratio=0.4))
        self.cue_at(1, "The next has")
        self.play(FadeOut(tiny), run_time=0.3)
        small = VGroup(*[az_mob(tt, 2, 0.3, ORIGIN, with_paths=False, colored=False)[0] for tt in AZ[2]]) \
            .arrange_in_grid(2, 4, buff=0.25).move_to(RIGHT * 3.4 + DOWN * 0.6)
        self.play(FadeIn(counts[1]), LaggedStartMap(FadeIn, small, lag_ratio=0.1), run_time=1.2)
        self.cue_at(1, "The next, sixty")
        self.play(FadeIn(counts[2]))
        self.cue(2)
        q = T("2, 8, 64, ?", 36, YELLOW).to_edge(DOWN, buff=0.4).shift(RIGHT * 3)
        self.play(Write(q))
        self.cue(3)
        q2 = T("2, 8, 64, 1024: powers of 2", 34, YELLOW).move_to(q)
        self.sfx("chime")
        self.play(Transform(q, q2))


class AztecPaths(DScene):
    def construct(self):
        u = 0.85
        c = LEFT * 4.2 + DOWN * 0.2
        t = AZ[2][5]
        board = az_mob(t, 2, u, c, with_paths=True, colored=True)
        plain = az_mob(t, 2, u, c, with_paths=False, colored=False)[0]
        self.add(plain)
        title = T("Dominoes become paths", 36).to_edge(UP, buff=0.4)
        self.cue(0)
        self.play(Write(title))
        legend = VGroup()
        for key, lab in [(("H", 0), "flat step"), (("V", 0), "step up"), (("V", 1), "step down"), (("H", 1), "nothing")]:
            w, h = (2, 1) if key[0] == "H" else (1, 2)
            r = Rectangle(width=w * 0.3, height=h * 0.3, fill_color=TYPE_COL[key], fill_opacity=0.85, stroke_color=WHITE, stroke_width=1)
            legend.add(VGroup(r, T(lab, 22)).arrange(RIGHT, buff=0.2))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 0.6 + UP * 0.7)
        lt = T("colour the board like a chessboard:\n4 kinds of domino", 22, SOFT, line_spacing=1.1).next_to(legend, UP, buff=0.3)
        self.play(Transform(plain, board[0]), FadeIn(lt), FadeIn(legend, lag_ratio=0.2), run_time=1.5)
        self.cue(1)
        self.play(LaggedStartMap(Create, board[1], lag_ratio=0.2), run_time=2)
        msg = VGroup(T("2 paths, left side to right side", 24),
                     T("dominoes never overlap → paths never touch", 24, YELLOW),
                     T("and every such pair of paths = one tiling", 24)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        msg.next_to(legend, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(FadeIn(msg, lag_ratio=0.3), run_time=2.5)
        cur = VGroup(plain, board[1])
        for k in (0, 3, 6, 5):
            nb = az_mob(AZ[2][k], 2, u, c)
            self.play(Transform(cur[0], nb[0]), Transform(cur[1], nb[1]), run_time=0.7)
            self.wait(0.3)
        self.cue(2)
        self.play(FadeOut(msg), FadeOut(legend), FadeOut(lt))
        m = matrix_mob([[12, 4], [4, 2]], size=36).move_to(RIGHT * 1.6 + UP * 1.0)
        mt = T("route counts between the ends", 22, SOFT).next_to(m, UP, buff=0.25)
        d = T("det = 8", 38, YELLOW).next_to(m, RIGHT, buff=0.5)
        self.play(FadeIn(mt), FadeIn(m))
        self.sfx("chime")
        self.play(Write(d))
        self.cue(3)
        big = az_mob(AZ[3][41], 3, 0.36, RIGHT * 3.0 + DOWN * 1.9)
        three = T("order 3: 3 paths, det = 64", 24, YELLOW).next_to(big, LEFT, buff=0.4)
        self.play(FadeIn(big), FadeIn(three))
        self.cue(4)
        thm = VGroup(T("order n:  2^(n(n+1)/2) tilings", 30, YELLOW),
                     T("Elkies, Kuperberg, Larsen, Propp (1992)", 20, SOFT),
                     T("the paths proof: Eu & Fu (2005)", 20, SOFT)).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.4)
        self.play(FadeIn(thm, lag_ratio=0.2))
