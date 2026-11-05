"""Act 7 — Counting #3: spanning trees (Script v2, 11:45-13:00).

    HouseTrees   the house graph, what a spanning tree is, all 11 of them
    Laplacian    degrees on the diagonal, -1 per edge; delete a row and column; det = 11
    Cayley       K4: 16, K5: 125, n^(n-2); Kirchhoff 1847
"""
from itertools import combinations

from common import *

HV = [np.array(p, float) for p in [(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0), (0, 2.1, 0)]]
HE = [(0, 1), (1, 2), (2, 3), (3, 0), (2, 4), (3, 4)]


def is_tree(n, edges):
    if len(edges) != n - 1:
        return False
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[ra] = rb
    return True


TREES = [S for S in combinations(HE, 4) if is_tree(5, S)]
assert len(TREES) == 11


def graph_mob(V, E, keep=None, scale=1.0, center=ORIGIN, col=YELLOW, dim=GREY_D, r=0.12, w=5):
    pts = [center + scale * v for v in V]
    g = VGroup()
    for e in E:
        on = keep is None or e in keep
        g.add(Line(pts[e[0]], pts[e[1]], color=col if on else dim, stroke_width=w if on else w * 0.5,
                   stroke_opacity=1 if on else 0.5))
    g.add(*[Dot(p, radius=r, color=WHITE) for p in pts])
    return g


def laplacian(n, E):
    L = [[0] * n for _ in range(n)]
    for a, b in E:
        L[a][a] += 1
        L[b][b] += 1
        L[a][b] -= 1
        L[b][a] -= 1
    return L


class HouseTrees(DScene):
    def construct(self):
        card = T("Determinants can count trees.", 36).to_edge(UP, buff=0.4)
        self.play(Write(card))
        k = portrait("kirchhoff", "Gustav Kirchhoff", "1847", "electrical circuits", size=1.4).to_corner(UR, buff=0.4)
        self.play(FadeIn(k))
        g = graph_mob(HV, HE, scale=1.1, center=LEFT * 3.5 + DOWN * 0.6)
        self.play(Create(g), run_time=1.5)
        self.wait(1)
        dfn = VGroup(T("spanning tree:", 28, YELLOW), T("keep some edges so that", 24),
                     T("every vertex is connected", 24), T("and there are no loops", 24)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(RIGHT * 0.9 + UP * 1.1)
        self.play(FadeIn(dfn, lag_ratio=0.2))
        ex1 = graph_mob(HV, HE, keep=TREES[0], scale=1.1, center=LEFT * 3.5 + DOWN * 0.6)
        self.play(Transform(g, ex1))
        tk = tick(0.5).next_to(g, DOWN, buff=0.2)
        self.play(FadeIn(tk))
        self.wait(1)
        loop = (HE[0], HE[1], HE[2], HE[3])
        ex2 = graph_mob(HV, HE, keep=loop, scale=1.1, center=LEFT * 3.5 + DOWN * 0.6)
        cx = cross(0.5).move_to(tk)
        self.play(Transform(g, ex2), Transform(tk, cx))
        lp = T("a loop", 24, BAD).next_to(cx, RIGHT, buff=0.2)
        self.play(FadeIn(lp))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in (g, tk, lp, dfn)])
        minis = VGroup(*[graph_mob(HV, HE, keep=S, scale=0.42, r=0.06, w=4) for S in TREES]) \
            .arrange_in_grid(2, 6, buff=(0.55, 0.6)).move_to(LEFT * 1.4 + DOWN * 0.4)
        cnt = T("0", 54, YELLOW).move_to(RIGHT * 5 + DOWN * 1.2)
        self.add(cnt)
        for i, mi in enumerate(minis):
            self.sfx("tick")
            self.play(FadeIn(mi, scale=0.8), Transform(cnt, T(str(i + 1), 54, YELLOW).move_to(cnt)),
                      run_time=0.45 if i > 2 else 0.8)
        self.wait(2.5)


class Laplacian(DScene):
    def construct(self):
        g = graph_mob(HV, HE, scale=0.8, center=LEFT * 5 + UP * 0.6)
        labels = VGroup(*[T(str(i + 1), 22, BLACK).move_to(LEFT * 5 + UP * 0.6 + 0.8 * v) for i, v in enumerate(HV)])
        for d in g[len(HE):]:
            d.scale(1.8)
        self.add(g, labels)
        rec = VGroup(T("the recipe:", 28, YELLOW), T("diagonal: number of neighbours", 24),
                     T("−1 for every edge, 0 elsewhere", 24)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        rec.next_to(g, DOWN, buff=0.5).align_to(g, LEFT).shift(LEFT * 0.4)
        self.play(FadeIn(rec, lag_ratio=0.2))
        L = laplacian(5, HE)
        m = matrix_mob([[("−1" if v == -1 else str(v)) for v in row] for row in L], size=34, h_buff=0.55, v_buff=0.35)
        m.move_to(RIGHT * 0.1 + UP * 0.6)
        for i, c in enumerate(m.cells):
            r, cc = divmod(i, 5)
            if r == cc:
                c.set_color(YELLOW)
            elif L[r][cc] == -1:
                c.set_color(BLUE_B)
            else:
                c.set_color(GREY_C)
        self.play(FadeIn(m))
        self.wait(2)
        # cross out row 1 and column 1
        row = Line(m.cells[0].get_left() + LEFT * 0.2, m.cells[4].get_right() + RIGHT * 0.2, color=RED, stroke_width=5)
        col = Line(m.cells[0].get_top() + UP * 0.15, m.cells[20].get_bottom() + DOWN * 0.15, color=RED, stroke_width=5)
        self.play(Create(row), Create(col))
        self.wait(1)
        det = T("det = 11", 46, YELLOW).next_to(m, RIGHT, buff=0.5)
        self.sfx("chime")
        self.play(Write(det))
        self.wait(1.5)
        thm = VGroup(T("Matrix-Tree Theorem (Kirchhoff, 1847)", 26, YELLOW),
                     T("the proof is a cancellation again:", 22, SOFT),
                     T("configurations with a loop cancel in pairs", 22, SOFT)).arrange(DOWN, buff=0.08)
        thm.move_to(RIGHT * 2.6 + DOWN * 2.2)
        self.play(FadeIn(thm, lag_ratio=0.2))
        joke = T("Kirchhoff was trying to understand circuits and accidentally learned to count trees.", 22, GREY_B) \
            .to_edge(DOWN, buff=0.3)
        self.play(FadeIn(joke))
        self.wait(3)


class Cayley(DScene):
    def construct(self):
        def kn(n, center, scale):
            V = [np.array([np.cos(TAU * k / n + PI / 2), np.sin(TAU * k / n + PI / 2), 0]) for k in range(n)]
            return graph_mob(V, list(combinations(range(n), 2)), scale=scale, center=center, r=0.09, w=3)
        k4 = kn(4, LEFT * 3.5 + UP * 0.4, 1.4)
        k5 = kn(5, RIGHT * 1.0 + UP * 0.4, 1.5)
        self.play(Create(k4))
        l4 = T("K₄: 16 spanning trees", 28).next_to(k4, DOWN, buff=0.4)
        self.play(FadeIn(l4))
        self.wait(1)
        self.play(Create(k5))
        l5 = T("K₅: 125", 28).next_to(k5, DOWN, buff=0.4)
        self.play(FadeIn(l5))
        self.wait(1)
        cay = VGroup(T("Kₙ:", 36), T("nⁿ⁻²", 48, YELLOW)).arrange(RIGHT, buff=0.3).move_to(RIGHT * 5 + UP * 0.4)
        self.sfx("chime")
        self.play(FadeIn(cay, scale=1.2))
        name = T("Cayley's formula", 24, SOFT).next_to(cay, DOWN, buff=0.25)
        self.play(FadeIn(name))
        tl = T("Try listing 125 by hand.", 24, GREY_B).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(tl))
        self.wait(3)


class TreesBrief(DScene):
    """Short version for v3: determinants also count spanning trees."""

    def construct(self):
        card = T("Determinants count other things too.", 36).to_edge(UP, buff=0.4)
        self.cue(0)
        self.play(Write(card))
        g = graph_mob(HV, HE, scale=0.9, center=LEFT * 4.6 + UP * 0.2)
        self.play(Create(g))
        lab = VGroup(T("spanning trees:", 30, YELLOW), T("connect every dot, no loops", 26, SOFT)) \
            .arrange(DOWN, buff=0.08).next_to(g, DOWN, buff=0.3)
        self.cue_at(0, "a spanning tree")
        self.play(FadeIn(lab))
        minis = VGroup(*[graph_mob(HV, HE, keep=S, scale=0.38, r=0.06, w=4) for S in TREES]) \
            .arrange_in_grid(2, 6, buff=(0.35, 0.45)).move_to(RIGHT * 1.2 + UP * 0.5)
        cnt = T("0", 56, YELLOW).move_to(RIGHT * 5.9 + UP * 0.5)
        self.add(cnt)
        for i, mi in enumerate(minis):
            self.play(FadeIn(mi, scale=0.8), Transform(cnt, T(str(i + 1), 56, YELLOW).move_to(cnt)), run_time=0.22)
        self.cue(1)
        k = portrait("kirchhoff", "Kirchhoff, 1847", size=1.3).move_to(LEFT * 0.8 + DOWN * 2.3)
        res = VGroup(T("one determinant = 11", 32, YELLOW), T("complete graph on n dots: nⁿ⁻²", 28, SOFT)) \
            .arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(k, RIGHT, buff=0.5)
        self.play(FadeIn(k))
        self.cue_at(1, "a determinant")
        self.sfx("chime")
        self.play(FadeIn(res[0]))
        self.cue_at(1, "For the complete")
        self.play(FadeIn(res[1]))
