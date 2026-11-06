"""v13 — "When the signs go wrong", the 2x3 board in Priyanshu's style (no letter labels).

    Dominoes2x3  the 2x3 board, its 3 tilings; a domino = one dark + one light square; the matrix (rows = dark
                 squares, columns = light squares, shown as tiny boards with that square lit), a 1 where they
                 touch; each tiling = one term; det = +1 − 1 − 1 = −1
    KastFix      Kasteleyn (1961): one minus sign on one edge; only the all-vertical tiling uses it; det = −3 → 3
All numbers checked at import.
"""
from itertools import permutations
from common import *
from act7_kasteleyn import board, domino, TILINGS, TABLE, B_ORDER, W_ORDER, entry_index, FLIP, DARK_SQ, LIGHT_SQ


def _sgn(p):
    return round(np.linalg.det(np.eye(3)[list(p)]))


def _perm(t):
    p = [None] * 3
    for a, b in t:
        k = entry_index(a, b)
        p[k // 3] = k % 3
    return p


SIGNS = [_sgn(_perm(t)) for t in TILINGS]
FLIPK = entry_index((0, 1), (1, 1))
KT = [row[:] for row in TABLE]
KT[FLIPK // 3][FLIPK % 3] = -1
assert SIGNS == [1, -1, -1] and round(np.linalg.det(np.array(TABLE, float))) == -1
assert round(np.linalg.det(np.array(KT, float))) == -3 and FLIPK == 6
assert sum(1 for t in TILINGS if any(entry_index(a, b) == FLIPK for a, b in t)) == 1      # only one tiling uses it


def mini(cell, s=0.26):
    """A tiny 2x3 board with one square lit: the row/column header (no letters)."""
    b = board(2, 3, s)
    b.sq[cell].set_stroke(YELLOW, 3)
    b.sq[cell].set_fill(YELLOW, 0.9)
    return b


def table_sym(entries, size=40):
    cells = VGroup(*[T(str(v), size) for row in entries for v in row]).arrange_in_grid(3, 3, buff=(0.8, 0.5))
    rl = VGroup(*[mini(B_ORDER[k]).next_to(cells[3 * k], LEFT, buff=0.5) for k in range(3)])
    cl = VGroup(*[mini(W_ORDER[k]).next_to(cells[k], UP, buff=0.35) for k in range(3)])
    h = cells.height + 0.4
    lb = VMobject(stroke_color=INK, stroke_width=3).set_points_as_corners(
        [UP * h / 2 + RIGHT * 0.15, UP * h / 2, DOWN * h / 2, DOWN * h / 2 + RIGHT * 0.15]).next_to(cells, LEFT, buff=0.18)
    rb = lb.copy().rotate(PI).next_to(cells, RIGHT, buff=0.18)
    g = VGroup(cells, rl, cl, lb, rb)
    g.cells = cells
    return g


def small_tilings(s=0.5):
    out = VGroup()
    for t in TILINGS:
        bb = board(2, 3, s)
        bb.add(*[domino(bb.sq, x, y, s) for x, y in t])
        out.add(bb)
    return out


class Dominoes2x3(DScene):
    def construct(self):
        s = 1.05
        b = board(2, 3, s, origin=LEFT * 5.4 + UP * 2.3)
        small = small_tilings().arrange(RIGHT, buff=0.55).move_to(LEFT * 3.6 + DOWN * 1.5)

        # 0: dominoes on a chessboard; a 2x3 board has three tilings
        self.cue(0)
        self.play(FadeIn(b, lag_ratio=0.1), run_time=0.8)
        self.cue_at(0, "three tilings", lead=0.2)
        for sm in small:
            self.sfx("pop")
            self.play(FadeIn(sm, shift=UP * 0.2), run_time=0.6)

        # 1: a domino always covers one dark and one light square
        self.cue(1)
        d = domino(b.sq, (0, 0), (0, 1), s)
        self.play(FadeIn(d), run_time=0.5)
        self.play(Indicate(b.sq[(0, 0)], color=YELLOW, scale_factor=1.15), run_time=0.6)
        self.play(Indicate(b.sq[(0, 1)], color=YELLOW, scale_factor=1.15), run_time=0.6)
        self.play(FadeOut(d), run_time=0.3)

        # 2: the matrix: rows = dark squares, columns = light squares, a 1 where they touch
        self.cue(2)
        tab = table_sym(TABLE).move_to(RIGHT * 3.4 + UP * 1.0)
        for c in tab.cells:
            c.set_opacity(0)
        self.cue_at(2, "rows for the dark", lead=0.2)
        self.play(FadeIn(tab[3]), FadeIn(tab[4]), LaggedStartMap(FadeIn, tab[1], lag_ratio=0.3), run_time=1.0)
        self.cue_at(2, "columns for the light", lead=0.2)
        self.play(LaggedStartMap(FadeIn, tab[2], lag_ratio=0.3), run_time=0.9)
        self.add(tab.cells)
        self.cue_at(2, "a one wherever", lead=0.2)
        for i in range(3):
            for j in range(3):
                k = 3 * i + j
                bsq, wsq = b.sq[B_ORDER[i]], b.sq[W_ORDER[j]]
                hl = VGroup(SurroundingRectangle(bsq, color=YELLOW, buff=0.02), SurroundingRectangle(wsq, color=YELLOW, buff=0.02))
                self.add(hl)
                if TABLE[i][j]:
                    self.sfx("tick")
                self.play(tab.cells[k].animate.set_opacity(1), run_time=0.28)
                self.remove(hl)

        # 3: each tiling picks one entry in every row and every column: one term of the determinant
        self.cue(3)
        for k, t in enumerate(TILINGS):
            fr = SurroundingRectangle(small[k], color=YELLOW, buff=0.08)
            mk = VGroup(*[SurroundingRectangle(tab.cells[entry_index(x, y)], color=YELLOW, buff=0.14) for x, y in t])
            self.play(Create(fr), Create(mk), run_time=0.6)
            self.wait(0.5)
            self.play(FadeOut(fr), FadeOut(mk), run_time=0.3)

        # 4: so the determinant should be three. It's minus one.
        self.cue(4)
        hope = T("det A = 3 ?", 36).move_to(RIGHT * 3.4 + DOWN * 1.4)
        self.play(FadeIn(hope), run_time=0.6)
        self.cue_at(4, "minus one", lead=0.2)
        no = VGroup(T("det A = −1", 36, BAD), cross(0.35)).arrange(RIGHT, buff=0.3).move_to(hope)
        self.sfx("buzz")
        self.play(Transform(hope, no), run_time=0.6)

        # 5: the terms carry signs: + for this one, − for these two
        self.cue(5)
        sg = VGroup(*[T("+" if v > 0 else "−", 46, GOOD if v > 0 else BAD).next_to(small[i], DOWN, buff=0.15)
                      for i, v in enumerate(SIGNS)])
        for x in sg:
            self.play(FadeIn(x, scale=1.5), run_time=0.45)
        sum_ = T("+1  −  1  −  1  =  −1", 32, SOFT).next_to(hope, DOWN, buff=0.35)
        self.cue_at(5, "cancellation", lead=0.2)
        self.play(FadeIn(sum_), run_time=0.6)
        self.cue_end(5)
        self.wait(0.5)


class KastFix(DScene):
    def construct(self):
        s = 1.05
        b = board(2, 3, s, origin=LEFT * 5.4 + UP * 2.3)
        small = small_tilings().arrange(RIGHT, buff=0.55).move_to(LEFT * 3.6 + DOWN * 1.5)
        tab = table_sym(TABLE).move_to(RIGHT * 3.4 + UP * 1.0)
        sg = VGroup(*[T("+" if v > 0 else "−", 46, GOOD if v > 0 else BAD).next_to(small[i], DOWN, buff=0.15)
                      for i, v in enumerate(SIGNS)])
        self.add(b, small, tab, sg)

        # 0: Kasteleyn, 1961: change the signs
        self.cue(0)
        kc = VGroup(T("Pieter Kasteleyn", 34, YELLOW), T("physicist · 1961", 26, SOFT)).arrange(DOWN, buff=0.1).to_corner(UR, buff=0.35)
        self.play(FadeIn(kc, shift=DOWN * 0.2), run_time=0.8)

        # 1: a minus sign on this one edge
        self.cue(1)
        nodes = {k: b.sq[k].get_center() for k in b.sq}
        edges = {}
        for (r, c) in b.sq:
            for dr, dc in ((0, 1), (1, 0)):
                o = (r + dr, c + dc)
                if o in b.sq:
                    edges[((r, c), o)] = Line(nodes[(r, c)], nodes[o], color=YELLOW, stroke_width=4)
        g = VGroup(*edges.values(), *[Dot(p, radius=0.07, color=YELLOW) for p in nodes.values()])
        self.play(Create(g), run_time=1.0)
        e = edges[((0, 1), (1, 1))]
        minus = T("−1", 40, FLIP, weight=BOLD).next_to(e, RIGHT, buff=0.35)
        self.cue_at(1, "this one edge", lead=0.2)
        self.sfx("flip")
        self.play(e.animate.set_color(FLIP).set_stroke(width=9), FadeIn(minus, scale=2), run_time=0.7)
        self.play(Transform(tab.cells[FLIPK], T("−1", 40, FLIP).move_to(tab.cells[FLIPK])), run_time=0.7)

        # 2: only the all-vertical tiling uses that edge, so only its sign flips
        self.cue(2)
        user = [i for i, t in enumerate(TILINGS) if any(entry_index(a, c) == FLIPK for a, c in t)][0]
        self.play(Indicate(small[user], color=FLIP, scale_factor=1.12), run_time=0.9)
        self.sfx("flip")
        self.play(Transform(sg[user], T("−", 46, BAD).move_to(sg[user])), run_time=0.6)

        # 3: every tiling now has the same sign; det = −3; ignore the sign: 3
        self.cue(3)
        self.play(Indicate(sg, color=BAD, scale_factor=1.3), run_time=0.8)
        x_eq = 2.7
        rows = VGroup()
        for i, (lhs, rhs, col) in enumerate([("det A", "−1  −  1  −  1", INK), (None, "−3", INK), ("|det A|", "3", YELLOW)]):
            eq = T("=", 34).move_to(np.array([x_eq, -1.45 - 0.7 * i, 0]))
            g = VGroup(eq, T(rhs, 34 if i < 2 else 42, col, weight=BOLD if i == 2 else NORMAL).next_to(eq, RIGHT, buff=0.25))
            if lhs:
                g.add(T(lhs, 34).next_to(eq, LEFT, buff=0.25))
            rows.add(g)
        rows[2].add(tick(0.35).next_to(rows[2][1], RIGHT, buff=0.25))
        r1, r2 = VGroup(rows[0], rows[1]), rows[2]
        self.cue_at(3, "minus three", lead=0.2)
        self.play(Write(r1), run_time=0.9)
        self.cue_at(3, "Ignore the sign", lead=0.2)
        self.sfx("chime")
        self.play(Write(r2), run_time=0.8)
        self.cue_end(3)
        self.wait(0.6)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.6)
