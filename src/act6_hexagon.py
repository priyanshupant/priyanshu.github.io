"""Act 6 — Counting #2: tilings of the 2, 3, 2 hexagon (Script v2, 10:00-11:45).

    HexTiling      the hexagon on a triangular grid, the three lozenges, the cube illusion
    TilesToPaths   fade the flat tiles; two chains; squash onto the grid = ant 1 & ant 2; all 50

A tiling of the hexagon with sides a, b, c, a, b, c is a stack of cubes in an
a x b x c box: an a x b array of heights in 0..c, weakly decreasing along rows
and columns. Here (a, b, c) = (2, 3, 2): 50 tilings. The tiles with a vertical
edge form one chain per level z = 0..c-1, the outline of the cells taller than
z; level 1 is ant 1's route, level 0 ant 2's (checked in code below).
"""
from itertools import product

from common import *

BOX = (2, 2, 2)                       # a, b, c
R3 = np.sqrt(3) / 2
E1, E2, E3 = np.array([R3, -0.5, 0]), np.array([-R3, -0.5, 0]), np.array([0, 1.0, 0])
TOP_C, X_C, Y_C = GREY_A, GREY_C, GREY_D


def partitions(a=None, b=None, c=None):
    a, b, c = (a, b, c) if a else BOX
    out = []
    for vals in product(range(c + 1), repeat=a * b):
        h = [vals[i * b:(i + 1) * b] for i in range(a)]
        if all(h[i][j] >= h[i][j + 1] for i in range(a) for j in range(b - 1)) and \
           all(h[i][j] >= h[i + 1][j] for i in range(a - 1) for j in range(b)):
            out.append(tuple(map(tuple, h)))
    return out


PARTITIONS = partitions()
SHOW = ((2, 1), (1, 0))


def proj(x, y, z, s, c):
    return c + s * (x * E1 + y * E2 + z * E3)


def faces(h, box=None):
    a, b, cc = box or BOX
    out = []
    for i, j in product(range(a), range(b)):
        z = h[i][j]
        out.append(("T", [(i, j, z), (i + 1, j, z), (i + 1, j + 1, z), (i, j + 1, z)]))
    for j, z in product(range(b), range(cc)):
        m = sum(1 for i in range(a) if h[i][j] > z)
        out.append(("X", [(m, j, z), (m, j + 1, z), (m, j + 1, z + 1), (m, j, z + 1)]))
    for i, z in product(range(a), range(cc)):
        n = sum(1 for j in range(b) if h[i][j] > z)
        out.append(("Y", [(i, n, z), (i + 1, n, z), (i + 1, n, z + 1), (i, n, z + 1)]))
    return out


def tiling(h, s=1.0, c=ORIGIN, stroke=2, box=None):
    col = {"T": TOP_C, "X": X_C, "Y": Y_C}
    g = VGroup()
    for kind, cs in faces(h, box):
        poly = Polygon(*[proj(*q, s, c) for q in cs], fill_color=col[kind], fill_opacity=1,
                       stroke_color=BLACK, stroke_width=stroke)
        poly.kind = kind
        g.add(poly)
    return g


def triangles(s=1.0, c=ORIGIN, box=None, color=GREY_D):
    """All unit triangles of the hexagon: every lozenge split along its short diagonal."""
    seen, g = set(), VGroup()
    for h in partitions(*(box or BOX)):
        for kind, cs in faces(h, box):
            p = [proj(*q, s, c) for q in cs]
            if np.linalg.norm(p[0] - p[2]) < np.linalg.norm(p[1] - p[3]):
                tris = [(p[0], p[1], p[2]), (p[0], p[2], p[3])]
            else:
                tris = [(p[1], p[2], p[3]), (p[1], p[3], p[0])]
            for t in tris:
                key = tuple(np.round(sum(t) / 3, 3))
                if key not in seen:
                    seen.add(key)
                    g.add(Polygon(*t, stroke_color=color, stroke_width=1.2, fill_opacity=0))
    return g


def outline(s=1.0, c=ORIGIN, box=None):
    a, b, cc = box or BOX
    corners = [(a, 0, 0), (a, 0, cc), (0, 0, cc), (0, b, cc), (0, b, 0), (a, b, 0)]
    return Polygon(*[proj(*q, s, c) for q in corners], color=WHITE, stroke_width=3)


def contour(h, z, box=None):
    a, b, _ = box or BOX
    S = {(i, j) for i in range(a) for j in range(b) if h[i][j] > z}
    i, j, pts = 0, b, [(0, b)]
    while (i, j) != (a, 0):
        if j == 0 or (i, j - 1) in S:
            i += 1
        else:
            j -= 1
        pts.append((i, j))
    return pts


def chain(h, z, s, c, color, box=None, width=8):
    m = VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [proj(i, j, z + 0.5, s, c) for i, j in contour(h, z, box)])
    m.set_z_index(3)
    return m


def walker_path(h, z):
    b = BOX[1]
    if z == 1:
        return [(i, b - j + 1) for i, j in contour(h, 1)]   # ant 1: (0,1) -> (2,4)
    return [(i + 1, b - j) for i, j in contour(h, 0)]       # ant 2: (1,0) -> (3,3)


# the bijection, checked once at import
_pairs = {(tuple(walker_path(h, 1)), tuple(walker_path(h, 0))) for h in PARTITIONS}
assert len(PARTITIONS) == 20 and len(_pairs) == 20
assert all(p[0] == A1 and p[-1] == B1 and q[0] == A2 and q[-1] == B2 and first_meet(list(p), list(q)) is None
           for p, q in _pairs)


class HexTiling(DScene):
    def construct(self):
        card = T("Determinants can count much more than walkers.", 34).to_edge(UP, buff=0.4)
        self.cue(0)
        self.play(Write(card))
        c = LEFT * 1.4 + DOWN * 0.45
        s = 1.15
        # faint triangular grid points inside the box projection
        pts = triangles(s, c)
        hexo = outline(s, c)
        self.play(Create(hexo), run_time=1.0)
        self.play(LaggedStartMap(Create, pts, lag_ratio=0.02), run_time=1.0)
        tri_note = T("a hexagon cut into little triangles", 24, SOFT).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(tri_note))
        vs = hexo.get_vertices()
        sides = VGroup(*[T(str(n), 26, SOFT).move_to(c + 1.13 * ((vs[k] + vs[(k + 1) % 6]) / 2 - c))
                         for k, n in enumerate([BOX[0], BOX[2], BOX[1], BOX[0], BOX[2], BOX[1]])])
        self.play(FadeIn(sides))
        self.cue(1)
        kinds = VGroup(*[Polygon(*[proj(*q, 0.7, ORIGIN) for q in cs], fill_color=col, fill_opacity=1,
                                 stroke_color=BLACK, stroke_width=2)
                         for cs, col in [([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], TOP_C),
                                         ([(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)], X_C),
                                         ([(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)], Y_C)]])
        kinds.arrange(DOWN, buff=0.45).to_edge(RIGHT, buff=1.4).shift(DOWN * 0.3)
        klab = VGroup(T("lozenge = two triangles", 22, SOFT), T("three orientations", 22, SOFT)) \
            .arrange(DOWN, buff=0.05).next_to(kinds, UP, buff=0.35)
        self.play(FadeIn(kinds, lag_ratio=0.3), FadeIn(klab))
        # two triangles glue into one lozenge
        demo = tiling(SHOW, s, c)[0]                       # a flat tile of the example tiling
        dp = demo.get_vertices()
        if np.linalg.norm(dp[0] - dp[2]) < np.linalg.norm(dp[1] - dp[3]):
            t1, t2 = Polygon(dp[0], dp[1], dp[2]), Polygon(dp[0], dp[2], dp[3])
        else:
            t1, t2 = Polygon(dp[1], dp[2], dp[3]), Polygon(dp[1], dp[3], dp[0])
        for t in (t1, t2):
            t.set_fill(YELLOW, 0.6).set_stroke(YELLOW, 3)
        self.play(FadeOut(tri_note), FadeIn(t1), FadeIn(t2))
        glue = T("two triangles glued together = one tile (a lozenge)", 24, YELLOW).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(glue))
        self.play(FadeOut(t1), FadeOut(t2), FadeIn(demo.copy().set_fill(YELLOW, 0.8)), run_time=0.8)
        self.cue(2)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (hexo, pts, sides, kinds, klab, card)])
        # what is not allowed
        bad1 = demo.copy().set_fill(RED, 0.6).set_stroke(RED, 3).shift(LEFT * 1.25 * s * R3 * 2)
        x1 = cross(0.4).next_to(bad1, LEFT, buff=0.1)
        no1 = T("sticking out", 22, RED).next_to(x1, DOWN, buff=0.1)
        self.play(FadeIn(bad1), FadeIn(x1), FadeIn(no1))
        o1 = tiling(SHOW, s, c)[1].copy().set_fill(BLUE_D, 0.7)
        o2 = o1.copy().shift(0.5 * s * E1).set_fill(ORANGE, 0.7)
        x2 = cross(0.4).next_to(VGroup(o1, o2), RIGHT, buff=0.3)
        no2 = T("overlapping", 22, RED).next_to(x2, DOWN, buff=0.1)
        self.play(FadeIn(o1), FadeIn(o2), FadeIn(x2), FadeIn(no2))
        self.wait(0.8)
        self.play(*[FadeOut(m) for m in (bad1, x1, no1, o1, o2, x2, no2)])
        rule = T("a tiling: cover the hexagon exactly, no gaps, no overlaps", 28, YELLOW).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(rule))
        til = tiling(SHOW, s, c)
        self.cue(3)
        self.sfx("whoosh")
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.5) for t in til], lag_ratio=0.15), run_time=3)
        boxes = T("a stack of boxes in a corner?", 32).next_to(card, DOWN, buff=0.3)
        self.play(FadeOut(card), FadeIn(boxes))
        self.cue(4)
        self.play(Transform(rule, T("It's flat. Your brain is rendering 3D for free.", 28, YELLOW).move_to(rule)))
        orig = til.copy()
        flat = til.copy()
        for t in flat:
            t.set_fill(GREY_C, 1).set_stroke(WHITE, 2)
        self.cue_at(4, "completely flat")
        self.play(Transform(til, flat), run_time=0.8)
        self.wait(0.6)
        self.cue_at(4, "Your brain")
        self.play(Transform(til, orig), run_time=0.8)
        self.cue(5)
        q = T("How many tilings?", 38, YELLOW).move_to(boxes)
        self.play(Transform(boxes, q))
        for h in [PARTITIONS[i] for i in (7, 16, 19)] + [SHOW]:
            self.play(Transform(til, tiling(h, s, c)), run_time=0.6)
            self.wait(0.3)



class TilesToPaths(DScene):
    def construct(self):
        c = LEFT * 3.6 + DOWN * 0.4
        s = 0.95
        hexo = outline(s, c)
        til = tiling(SHOW, s, c)
        self.add(hexo, til)
        self.cue(0)
        note = T("fade the flat tiles", 28).to_edge(UP, buff=0.45)
        self.play(Write(note))
        tops = VGroup(*[t for t in til if t.kind == "T"])
        self.play(tops.animate.set_fill(opacity=0).set_stroke(GREY_B, 1.5), run_time=1.2)
        self.cue(1)
        self.play(Transform(note, T("walk through the tiles with vertical edges", 30).move_to(note)))
        vs = hexo.get_vertices()
        side = min(((vs[k], vs[(k + 1) % len(vs)]) for k in range(len(vs))
                    if abs(vs[k][0] - vs[(k + 1) % len(vs)][0]) < 1e-3), key=lambda e: e[0][0])
        mid = (side[0] + side[1]) / 2
        edges = VGroup(Line(side[0], mid, color=YELLOW, stroke_width=9), Line(mid, side[1], color=YELLOW, stroke_width=9))
        ch = [chain(SHOW, 1, s, c, ANT1), chain(SHOW, 0, s, c, ANT2)]
        self.cue_at(1, "Enter")
        self.play(Create(edges), run_time=0.6)
        self.play(Create(ch[0]), run_time=1.5)
        self.cue_at(1, "Two edges")
        self.play(Create(ch[1]), run_time=1.3)
        self.play(FadeOut(edges))
        expl = VGroup(T("2 vertical edges on the left side", 28),
                      T(f"→ 2 chains, {BOX[0] + BOX[1]} tiles each", 28),
                      T("tiles never overlap → chains never touch", 28, YELLOW),
                      T("and two non-touching chains fill in", 28),
                      T("to exactly one tiling", 28)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        expl.move_to(RIGHT * 2.8 + UP * 0.6)
        self.play(FadeIn(expl[:2], lag_ratio=0.25), run_time=1)
        self.cue(2)
        self.play(FadeIn(expl[2:], lag_ratio=0.25), run_time=1.5)
        self.cue(3)
        # squash onto the grid
        lat = Lattice(GRID[0], spacing=1.0, center=RIGHT * 3.6 + DOWN * 0.5, ny=GRID[1])
        ends = endpoints(lat, scale=0.85)
        self.play(FadeOut(expl), FadeIn(lat), FadeIn(ends))
        targets = [path_mob(lat, walker_path(SHOW, 1), ANT1, 8), path_mob(lat, walker_path(SHOW, 0), ANT2, 8)]
        self.play(*[ReplacementTransform(ch[k].copy(), targets[k]) for k in range(2)], run_time=2.5)
        L = ant(ANT1, 0.7).move_to(lat.p(*B1))
        N = ant(ANT2, 0.7).move_to(lat.p(*B2))
        self.play(FadeIn(L, scale=0.3), FadeIn(N, scale=0.3))
        self.play(Transform(note, T("It's ant 1 and ant 2 again!", 34, YELLOW).move_to(note)))
        for h in [PARTITIONS[i] for i in (2, 9, 15)] + [SHOW]:
            nt = tiling(h, s, c)
            for t in nt:
                if t.kind == "T":
                    t.set_fill(opacity=0).set_stroke(GREY_B, 1.5)
            nc = [chain(h, 1, s, c, ANT1), chain(h, 0, s, c, ANT2)]
            np_ = [path_mob(lat, walker_path(h, 1), ANT1, 8), path_mob(lat, walker_path(h, 0), ANT2, 8)]
            self.play(Transform(til, nt), *[Transform(ch[k], nc[k]) for k in range(2)],
                      *[Transform(targets[k], np_[k]) for k in range(2)], run_time=0.9)
            self.wait(0.3)
        self.cue(4)
        self.play(*[FadeOut(x) for x in self.mobjects])
        minis = VGroup(*[VGroup(outline(0.26), tiling(h, 0.26, stroke=0.8)) for h in PARTITIONS])
        minis.arrange_in_grid(4, 5, buff=(0.4, 0.3)).scale_to_fit_height(5.0).move_to(LEFT * 1.6 + UP * 0.6)
        self.play(LaggedStartMap(FadeIn, minis, lag_ratio=0.04), run_time=3)
        fifty = T(str(len(PARTITIONS)), 110, YELLOW, weight=BOLD).next_to(minis, RIGHT, buff=0.5)
        lab = T("tilings", 30).next_to(fifty, DOWN, buff=0.15)
        self.sfx("chime")
        self.play(FadeIn(fifty, scale=1.5), FadeIn(lab))
        same = T(f"the same {len(PARTITIONS)}", 26, SOFT).next_to(lab, DOWN, buff=0.3)
        self.play(FadeIn(same))
