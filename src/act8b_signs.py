"""v14 — "When the signs go wrong", the 2x3 board in Priyanshu's style (no letter labels), slow and detailed:
the six terms of the 3x3 determinant one by one, three vanish (a zero), three are the tilings, their signs by swaps.

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



PERMS = list(permutations(range(3)))                           # term = row i picks column p[i]
TPERM = [tuple(_perm(t)) for t in TILINGS]                       # the tilings' terms
assert sorted(TPERM) == sorted(p for p in PERMS if all(TABLE[i][p[i]] for i in range(3)))



def _swaps(p):
    seen, cyc = set(), 0
    for i in range(3):
        if i not in seen:
            cyc += 1
            j = i
            while j not in seen:
                seen.add(j)
                j = p[j]
    return 3 - cyc


assert [_swaps(p) for p in TPERM] == [2, 1, 1] and all((-1) ** _swaps(p) == sg for p, sg in zip(TPERM, SIGNS))

TERM_SIZE = 30


def term_line(p, entries, sign=None, flip=None):
    """'+  1 · 1 · 1  =  +1   (2 swaps)': row i's entry is entries[i][p[i]]."""
    vals = [entries[i][p[i]] for i in range(3)]
    prod = VGroup()
    for k, v in enumerate(vals):
        if k:
            prod.add(T("·", TERM_SIZE, SOFT))
        prod.add(T("(−1)" if v < 0 else str(v), TERM_SIZE, FLIP if v < 0 else (BAD if v == 0 else INK)))
    prod.arrange(RIGHT, buff=0.14)
    val = int(np.prod(vals)) * (sign or 1)
    sgn = T("+" if (sign or 1) > 0 else "−", TERM_SIZE + 6, GOOD if (sign or 1) > 0 else BAD)
    if sign is None:
        sgn.set_opacity(0)
    vtxt = ("+" if val > 0 and sign else "") + ("−" if val < 0 else "") + str(abs(val))
    eq = T("=", TERM_SIZE, SOFT)
    v = T(vtxt, TERM_SIZE, INK if val else SOFT)
    g = VGroup(sgn, prod, eq, v).arrange(RIGHT, buff=0.22)
    sw = _swaps(p)
    g.add(T(f"({sw} swap{'s' if sw != 1 else ''})", 22, SOFT).next_to(g, RIGHT, buff=0.3))
    if sign is None:
        g[4].set_opacity(0)
    g.p = p
    return g


def layout(entries=TABLE, signed=True):
    """The shared end state of Dominoes2x3 / start of KastFix."""
    s = 1.05
    b = board(2, 3, s, origin=LEFT * 5.4 + UP * 2.3)
    small = small_tilings().arrange(RIGHT, buff=0.55).move_to(LEFT * 3.6 + DOWN * 1.5)
    tab = table_sym(entries).move_to(RIGHT * 3.4 + UP * 1.35)
    sg = VGroup(*[T("+" if v > 0 else "−", 46, GOOD if v > 0 else BAD).next_to(small[i], DOWN, buff=0.15)
                  for i, v in enumerate(SIGNS)])
    terms = VGroup(*[term_line(p, entries, SIGNS[i] if signed else None) for i, p in enumerate(TPERM)])
    terms.arrange(DOWN, buff=0.22)
    for t in terms[1:]:                                            # line up the = signs
        t.shift(RIGHT * (terms[0][2].get_x() - t[2].get_x()))
    terms.move_to(RIGHT * 2.9 + DOWN * 1.25)
    return s, b, small, tab, sg, terms


def tile_box(tab, p):
    return VGroup(*[SurroundingRectangle(tab.cells[3 * i + p[i]], color=YELLOW, buff=0.14) for i in range(3)])


class Dominoes2x3(DScene):
    def construct(self):
        s, b, small, tab, sg, terms = layout()

        # 0: dominoes on a chessboard; start small, a 2x3 board
        self.cue(0)
        self.play(FadeIn(b, lag_ratio=0.1), run_time=0.8)

        # 1: its three tilings, one at a time as they are named
        self.cue(1)
        for k, phrase in enumerate(["three standing", "one standing", "two lying flat and"]):
            self.cue_at(1, phrase, lead=0.2)
            self.sfx("pop")
            self.play(FadeIn(small[k], shift=UP * 0.2), run_time=0.6)

        # 2: a domino always covers one dark and one light square
        self.cue(2)
        d = domino(b.sq, (0, 0), (0, 1), s)
        self.play(FadeIn(d), run_time=0.5)
        self.cue_at(2, "one dark", lead=0.2)
        self.play(Indicate(b.sq[(0, 0)], color=YELLOW, scale_factor=1.15), run_time=0.7)
        self.cue_at(2, "one light", lead=0.2)
        self.play(Indicate(b.sq[(0, 1)], color=YELLOW, scale_factor=1.15), run_time=0.7)
        self.play(FadeOut(d), run_time=0.3)

        # 3: the matrix: a row for each dark square, a column for each light square
        self.cue(3)
        for c in tab.cells:
            c.set_opacity(0)
        self.cue_at(3, "one row", lead=0.2)
        self.play(FadeIn(tab[3]), FadeIn(tab[4]), LaggedStartMap(FadeIn, tab[1], lag_ratio=0.4), run_time=1.4)
        self.cue_at(3, "one column", lead=0.2)
        self.play(LaggedStartMap(FadeIn, tab[2], lag_ratio=0.4), run_time=1.2)

        # 4: a one where they touch, a zero where they don't (each pair lit on the board)
        self.cue(4)
        self.add(tab.cells)
        for i in range(3):
            for j in range(3):
                k = 3 * i + j
                hl = VGroup(SurroundingRectangle(b.sq[B_ORDER[i]], color=YELLOW, buff=0.02),
                            SurroundingRectangle(b.sq[W_ORDER[j]], color=YELLOW, buff=0.02),
                            SurroundingRectangle(tab.cells[k], color=YELLOW, buff=0.1))
                self.add(hl)
                if TABLE[i][j]:
                    self.sfx("tick")
                self.play(tab.cells[k].animate.set_opacity(1), run_time=0.4)
                self.wait(0.12)
                self.remove(hl)

        # 5: a 3x3 determinant = six terms; each picks one entry per row and per column, multiplied
        self.cue(5)
        demo = tile_box(tab, (0, 1, 2))
        self.cue_at(5, "Each term", lead=0.2)
        self.play(Create(demo[0]), run_time=0.5)
        self.play(Create(demo[1]), run_time=0.5)
        self.play(Create(demo[2]), run_time=0.5)
        self.play(FadeOut(demo), run_time=0.4)

        # 6: all six, one by one
        self.cue(6)
        six = VGroup(*[term_line(p, TABLE) for p in PERMS])
        for t in six:
            t[4].set_opacity(0)
        six.arrange_in_grid(3, 2, buff=(0.7, 0.25), flow_order="dr").move_to(RIGHT * 3.0 + DOWN * 1.3)
        six.scale_to_fit_width(min(six.width, 7.4))
        if six.get_right()[0] > 7.0:
            six.shift(LEFT * (six.get_right()[0] - 7.0))
        for p, line in zip(PERMS, six):
            bx = tile_box(tab, p)
            self.play(Create(bx), run_time=0.4)
            zero = [i for i in range(3) if TABLE[i][p[i]] == 0]
            extra = []
            if zero:
                extra = [Indicate(tab.cells[3 * zero[0] + p[zero[0]]], color=BAD, scale_factor=1.5)]
                self.sfx("buzz")
            else:
                fr = SurroundingRectangle(small[TPERM.index(p)], color=YELLOW, buff=0.08)
                extra = [Create(fr)]
                self.sfx("tick")
            self.play(FadeIn(line[:4], shift=RIGHT * 0.1), *extra, run_time=0.5)
            self.wait(0.25)
            self.play(FadeOut(bx), *([FadeOut(fr)] if not zero else []), run_time=0.3)

        # 7: three of them pick up a zero: they vanish
        self.cue(7)
        zl = VGroup(*[six[k] for k, p in enumerate(PERMS) if p not in TPERM])
        self.play(*[ln[:4].animate.set_opacity(0.3) for ln in zl], run_time=0.6)
        self.play(FadeOut(zl, scale=0.6), run_time=0.6)

        # 8: the other three pick only ones, and each one is a tiling
        self.cue(8)
        keep = [six[PERMS.index(p)] for p in TPERM]
        uns = VGroup(*[term_line(p, TABLE) for p in TPERM])
        for i in range(3):
            uns[i].shift(terms[i][2].get_center() - uns[i][2].get_center())
        self.play(*[ReplacementTransform(keep[i][:4], uns[i][:4]) for i in range(3)], run_time=0.9)
        self.cue_at(8, "each of them", lead=0.2)
        for i, p in enumerate(TPERM):
            fr = SurroundingRectangle(small[i], color=YELLOW, buff=0.08)
            bx = tile_box(tab, p)
            ln = SurroundingRectangle(uns[i][1:4], color=YELLOW, buff=0.08)
            self.play(Create(fr), Create(bx), Create(ln), run_time=0.5)
            self.wait(0.6)
            self.play(FadeOut(fr), FadeOut(bx), FadeOut(ln), run_time=0.3)

        # 9: so the determinant should be three. It's minus one.
        self.cue(9)
        x_eq = 1.6                                                  # the det lines' own = column (fits the frame)
        hope = VGroup(T("det A", 32), T("=", 32), T("3 ?", 32)).arrange(RIGHT, buff=0.25)
        hope.shift(RIGHT * (x_eq - hope[1].get_x()) + UP * (terms.get_bottom()[1] - 0.55 - hope.get_y()))
        self.play(FadeIn(hope), run_time=0.6)
        self.cue_at(9, "minus one", lead=0.2)
        no = VGroup(T("−1", 32, BAD), cross(0.3)).arrange(RIGHT, buff=0.25).next_to(hope[1], RIGHT, buff=0.25)
        self.sfx("buzz")
        self.play(Transform(hope[2], no), run_time=0.6)

        # 10: the culprit: every term also gets a sign, by the number of swaps
        self.cue(10)
        rule = VGroup(T("even number of swaps → +", 26, GOOD), T("odd number of swaps → −", 26, BAD)) \
            .arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to(LEFT * 3.6 + DOWN * 3.25)
        self.cue_at(10, "plus if", lead=0.2)
        self.play(FadeIn(rule[0]), run_time=0.6)
        self.cue_at(10, "minus if", lead=0.2)
        self.play(FadeIn(rule[1]), run_time=0.6)

        # 11: this tiling: two swaps, plus; these two: one swap each, minus
        self.cue(11)
        for i in range(3):
            if i == 1:
                self.cue_at(11, "These two", lead=0.2)
            self.play(ReplacementTransform(uns[i][:4], terms[i][:4]), FadeIn(terms[i][4]), FadeIn(sg[i], scale=1.5),
                      Indicate(small[i], color=YELLOW, scale_factor=1.06), run_time=0.8)
            self.wait(0.2)

        # 12: +1 − 1 − 1 = −1: the cancellation eats the good ones
        self.cue(12)
        sum_ = VGroup(T("=", 32), T("+1  −  1  −  1  =  −1", 32, SOFT)).arrange(RIGHT, buff=0.25)
        sum_.shift(RIGHT * (x_eq - sum_[0].get_x()) + UP * (hope.get_y() - 0.6 - sum_.get_y()))
        self.play(FadeIn(sum_), run_time=0.8)
        self.cue_at(12, "cancellation", lead=0.2)
        self.play(Indicate(VGroup(sg[0], sg[1]), color=BAD, scale_factor=1.3), run_time=0.8)
        self.cue_end(12)
        self.wait(0.4)
        self.play(FadeOut(VGroup(hope, sum_, rule)), run_time=0.6)


class KastFix(DScene):
    def construct(self):
        s, b, small, tab, sg, terms = layout()
        self.add(b, small, tab, sg, terms)

        # 0: Kasteleyn, 1961: change the signs
        self.cue(0)
        kc = VGroup(T("Pieter Kasteleyn", 34, YELLOW), T("physicist · 1961", 26, SOFT)).arrange(DOWN, buff=0.1)
        kc.move_to(LEFT * 3.6 + DOWN * 3.2)
        self.play(FadeIn(kc, shift=UP * 0.2), run_time=0.8)

        # 1: the board as a graph: a dot per square, an edge per touching pair
        self.cue(1)
        nodes = {k: b.sq[k].get_center() for k in b.sq}
        edges = {}
        for (r, c) in b.sq:
            for dr, dc in ((0, 1), (1, 0)):
                o = (r + dr, c + dc)
                if o in b.sq:
                    edges[((r, c), o)] = Line(nodes[(r, c)], nodes[o], color=YELLOW, stroke_width=4)
        dots = VGroup(*[Dot(p, radius=0.08, color=YELLOW) for p in nodes.values()])
        self.cue_at(1, "a dot", lead=0.2)
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.2, scale=1.5), run_time=1.0)
        self.cue_at(1, "an edge", lead=0.2)
        self.play(LaggedStart(*[Create(e) for e in edges.values()], lag_ratio=0.2), run_time=1.4)
        self.add(dots)

        # 2: a minus sign on this one edge; in the matrix its 1 becomes −1
        self.cue(2)
        e = edges[((0, 1), (1, 1))]
        minus = T("−1", 40, FLIP, weight=BOLD).next_to(e, RIGHT, buff=0.3)
        self.cue_at(2, "this one edge", lead=0.2)
        self.sfx("flip")
        self.play(e.animate.set_color(FLIP).set_stroke(width=9), FadeIn(minus, scale=2), run_time=0.8)
        self.cue_at(2, "In the matrix", lead=0.2)
        ring = SurroundingRectangle(tab.cells[FLIPK], color=FLIP, buff=0.12)
        self.play(Create(ring), run_time=0.4)
        self.play(Transform(tab.cells[FLIPK], T("−1", 40, FLIP).move_to(tab.cells[FLIPK])), run_time=0.7)
        self.play(FadeOut(ring), run_time=0.3)

        # 3: only the all-standing tiling uses that edge
        self.cue(3)
        user = [i for i, t in enumerate(TILINGS) if any(entry_index(a, c) == FLIPK for a, c in t)][0]
        assert user == 0
        self.cue_at(3, "only the all", lead=0.2)
        fr = SurroundingRectangle(small[user], color=FLIP, buff=0.08)
        self.play(Create(fr), Indicate(small[user], color=FLIP, scale_factor=1.1), run_time=0.9)

        # 4: its term: +1 -> one entry is −1 -> −1; the other two terms don't change
        self.cue(4)
        ln = SurroundingRectangle(terms[user][1:4], color=FLIP, buff=0.08)
        self.play(Create(ln), run_time=0.5)
        self.cue_at(4, "Now one", lead=0.2)
        nl = term_line(TPERM[user], KT, SIGNS[user])
        nl.shift(terms[user][1].get_left() - nl[1].get_left())
        self.sfx("flip")
        self.play(Transform(terms[user][1], nl[1]), Transform(terms[user][2], nl[2]), Transform(terms[user][3], nl[3]),
                  terms[user][4].animate.next_to(nl[3], RIGHT, buff=0.3), run_time=0.8)
        self.play(Transform(sg[user], T("−", 46, BAD).move_to(sg[user])), run_time=0.6)
        self.play(FadeOut(ln), FadeOut(fr), run_time=0.3)
        self.cue_at(4, "The other two", lead=0.2)
        self.play(Indicate(VGroup(terms[1], terms[2]), color=SOFT, scale_factor=1.04), run_time=0.9)

        # 5: every tiling has the same sign: det = −1 − 1 − 1 = −3
        self.cue(5)
        self.play(Indicate(sg, color=BAD, scale_factor=1.3), FadeOut(kc), run_time=0.9)
        x_eq = 1.6
        r1 = VGroup(T("det A", 32), T("=", 32), T("−1  −  1  −  1  =  −3", 32)).arrange(RIGHT, buff=0.25)
        r1.shift(RIGHT * (x_eq - r1[1].get_x()) + UP * (terms.get_bottom()[1] - 0.55 - r1.get_y()))
        self.cue_at(5, "The determinant", lead=0.2)
        self.play(Write(r1), run_time=1.0)

        # 6: ignore the sign: 3 = the number of tilings
        self.cue(6)
        r2 = VGroup(T("|det A|", 36, YELLOW), T("=", 36), T("3", 42, YELLOW, weight=BOLD)).arrange(RIGHT, buff=0.25)
        r2.add(tick(0.35).next_to(r2, RIGHT, buff=0.25))
        r2.shift(RIGHT * (x_eq - r2[1].get_x()) + UP * (r1.get_y() - 0.7 - r2.get_y()))
        self.sfx("chime")
        self.play(Write(r2), run_time=0.9)
        self.cue_at(6, "exactly the number", lead=0.2)
        self.play(Indicate(small, color=YELLOW, scale_factor=1.05), run_time=0.9)
        self.cue_end(6)
        self.wait(0.6)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.6)
