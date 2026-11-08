"""Act 8 — Counting #4: dominoes (Script v2, 13:00-15:15).

    Dominoes8x8   a chessboard fills with dominoes: 12,988,816 tilings
    SmallBoard2   2x3 board, 3 tilings, the 0/1 table, det = -1 (signs +, -, -)
    SignFix2      Kasteleyn's one minus sign: det = -3, so 3
    Board4x4      plain det = 0 ("very confident, very wrong"); signed |det| = 36
    KastWhy       why the rule works: two tilings -> loops; each loop flips the sign an even number of times
    FKT           the pattern on 8x8; perfect matchings of planar graphs; FKT
"""
from common import *
from act7_kasteleyn import (board, domino, random_tiling, table_mob, entry_index, TILINGS, TABLE,
                            FLIP, DOMINO)


def all_tilings(R, C):
    out = []

    def rec(cov, cur):
        free = next(((r, c) for r in range(R) for c in range(C) if (r, c) not in cov), None)
        if free is None:
            out.append(list(cur))
            return
        r, c = free
        if c + 1 < C and (r, c + 1) not in cov:
            rec(cov | {(r, c), (r, c + 1)}, cur + [((r, c), (r, c + 1))])
        if r + 1 < R and (r + 1, c) not in cov:
            rec(cov | {(r, c), (r + 1, c)}, cur + [((r, c), (r + 1, c))])
    rec(frozenset(), [])
    return out


def kast_det(R, C, signed=True):
    B = [(r, c) for r in range(R) for c in range(C) if (r + c) % 2 == 0]
    W = [(r, c) for r in range(R) for c in range(C) if (r + c) % 2]
    M = np.zeros((len(B), len(W)))
    for i, (r, c) in enumerate(B):
        for j, (r2, c2) in enumerate(W):
            if abs(r - r2) + abs(c - c2) == 1:
                M[i, j] = -1 if (signed and c == c2 and c % 2 == 1) else 1
    return round(np.linalg.det(M))


assert len(all_tilings(4, 4)) == 36 and kast_det(4, 4, False) == 0 and abs(kast_det(4, 4)) == 36
assert abs(kast_det(8, 8)) == 12988816


def signed_graph(b, R, C, s, width=3):
    nodes = {k: b.sq[k].get_center() for k in b.sq}
    g = VGroup()
    for (r, c) in b.sq:
        if c + 1 < C:
            g.add(Line(nodes[(r, c)], nodes[(r, c + 1)], color=YELLOW, stroke_width=width))
        if r + 1 < R:
            neg = c % 2 == 1
            g.add(Line(nodes[(r, c)], nodes[(r + 1, c)], color=FLIP if neg else YELLOW,
                       stroke_width=width * (1.8 if neg else 1)))
    return g


class Dominoes8x8(DScene):
    def construct(self):
        card = T("Sometimes the signs need help.", 36).to_edge(UP, buff=0.4)
        self.cue(0)
        self.play(Write(card))
        s = 0.68
        b = board(8, 8, s, origin=LEFT * 5.4 + UP * 2.1)
        self.play(FadeIn(b, lag_ratio=0.01), run_time=1.2)
        doms = VGroup(*[domino(b.sq, x, y, s) for x, y in random_tiling(8, 8, 3)])
        self.play(LaggedStartMap(FadeIn, doms, lag_ratio=0.04, scale=0.6), run_time=3)
        self.cue(1)
        num = T("12,988,816", 60, YELLOW, weight=BOLD).move_to(RIGHT * 3.2 + UP * 0.4)
        lab = T("ways to tile a chessboard", 28).next_to(num, DOWN, buff=0.3)
        self.sfx("chime")
        self.play(FadeIn(num, scale=1.3), FadeIn(lab))
        no = T("nobody is checking that by hand", 24, SOFT).next_to(lab, DOWN, buff=0.4)
        self.play(FadeIn(no))


class SmallBoard2(DScene):
    def construct(self):
        s = 1.1
        b = board(2, 3, s, origin=LEFT * 4.6 + UP * 2.1, labels=True)
        self.cue(0)
        self.play(FadeIn(b))
        small = VGroup()
        for t in TILINGS:
            bb = board(2, 3, 0.5)
            bb.add(*[domino(bb.sq, x, y, 0.5) for x, y in t])
            small.add(bb)
        small.arrange(RIGHT, buff=0.6).move_to(LEFT * 3.4 + DOWN * 1.4)
        three = T("3 tilings", 30, YELLOW).next_to(small, UP, buff=0.25)
        self.play(LaggedStartMap(FadeIn, small, lag_ratio=0.4), FadeIn(three), run_time=1.6)
        idea = T("each domino = one black + one white square", 22, SOFT).next_to(b, DOWN, buff=0.3)
        idea.set_x(max(idea.get_x(), -7.1 + idea.width / 2 + 0.2))
        self.play(FadeIn(idea))
        self.cue(1)
        tab = table_mob(TABLE).move_to(RIGHT * 3.6 + UP * 1.4)
        ttl = T("1 where black and white squares touch", 24, SOFT).next_to(tab, UP, buff=0.35)
        self.play(FadeIn(tab[1]), FadeIn(tab[2]), FadeIn(ttl))
        self.play(LaggedStartMap(FadeIn, tab.cells, lag_ratio=0.12), run_time=1.4)
        for k, t in enumerate(TILINGS):
            fr = SurroundingRectangle(small[k], color=YELLOW, buff=0.08)
            mk = VGroup(*[SurroundingRectangle(tab.cells[entry_index(x, y)], color=YELLOW, buff=0.12) for x, y in t])
            self.play(Create(fr), Create(mk), run_time=0.6)
            self.wait(0.4)
            self.play(FadeOut(fr), FadeOut(mk), run_time=0.3)
        self.cue(2)
        hope = T("should give 3...", 30).next_to(tab, DOWN, buff=0.5)
        self.play(FadeIn(hope))
        self.wait(0.6)
        det = VGroup(T("det = −1", 36, BAD), cross(0.35)).arrange(RIGHT, buff=0.3).move_to(hope)
        self.sfx("buzz")
        self.play(Transform(hope, det))
        self.cue(3)
        signs = VGroup(*[T(sg, 44, GOOD if sg == "+" else BAD).next_to(small[k], DOWN, buff=0.15)
                         for k, sg in enumerate(["+", "−", "−"])])
        self.play(LaggedStartMap(FadeIn, signs, lag_ratio=0.3, scale=1.5))
        eat = T("+1 − 1 − 1 = −1: the cancellation eats the good ones", 24, SOFT).to_edge(DOWN, buff=0.35).shift(LEFT * 1.2)
        self.play(FadeIn(eat))


class SignFix2(DScene):
    def construct(self):
        s = 1.1
        b = board(2, 3, s, origin=LEFT * 4.6 + UP * 1.7, labels=True)
        self.add(b)
        self.cue(0)
        kc = VGroup(T("Pieter Kasteleyn", 34), T("physicist, Leiden · 1961", 26, SOFT)).arrange(DOWN, buff=0.1) \
            .to_corner(UR, buff=0.4)
        self.play(FadeIn(kc))
        idea = T("If the signs don't cancel the way you want,\nchange the signs.", 28, YELLOW, line_spacing=1.15) \
            .to_corner(UL, buff=0.4)
        self.play(Write(idea), run_time=1.6)
        nodes = {k: b.sq[k].get_center() for k in b.sq}
        edges = {}
        for (r, c) in b.sq:
            for dr, dc in ((0, 1), (1, 0)):
                o = (r + dr, c + dc)
                if o in b.sq:
                    edges[((r, c), o)] = Line(nodes[(r, c)], nodes[o], color=YELLOW, stroke_width=4)
        g = VGroup(*edges.values(), *[Dot(p, radius=0.07, color=YELLOW) for p in nodes.values()])
        self.play(Create(g))
        self.cue(1)
        e = edges[((0, 1), (1, 1))]
        minus = T("−", 54, FLIP, weight=BOLD).next_to(e, RIGHT, buff=0.1)
        self.sfx("flip")
        self.play(e.animate.set_color(FLIP).set_stroke(width=9), FadeIn(minus, scale=2))
        tab = table_mob(TABLE).move_to(RIGHT * 2.8 + DOWN * 0.7)
        self.play(FadeIn(tab))
        k = entry_index((0, 1), (1, 1))
        self.play(Transform(tab.cells[k], T("−1", 40, FLIP).move_to(tab.cells[k])))
        small = VGroup()
        for t in TILINGS:
            bb = board(2, 3, 0.42)
            bb.add(*[domino(bb.sq, x, y, 0.42) for x, y in t])
            small.add(bb)
        small.arrange(RIGHT, buff=0.45).move_to(LEFT * 3.7 + DOWN * 1.5)
        sg = VGroup(*[T(x, 40, GOOD if x == "+" else BAD).next_to(small[i], DOWN, buff=0.12)
                      for i, x in enumerate(["+", "−", "−"])])
        self.play(FadeIn(small), FadeIn(sg))
        only = T("only the all-vertical tiling uses that edge", 22, SOFT).next_to(small, UP, buff=0.2)
        self.play(FadeIn(only), Indicate(small[0], color=FLIP))
        self.play(Transform(sg[0], T("−", 40, BAD).move_to(sg[0])))
        res = VGroup(T("det = −3", 36, YELLOW), VGroup(T("so 3 tilings", 32, GOOD), tick(0.35)).arrange(RIGHT, buff=0.25)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.45)
        self.cue(2)
        self.play(FadeIn(res[0]))
        self.sfx("chime")
        self.play(FadeIn(res[1]))


def tiling_sign(t, R, C, signed):
    """Sign of a tiling's term in the (plain or Kasteleyn) determinant: sgn(perm) * product of its entries."""
    B = [(r, c) for r in range(R) for c in range(C) if (r + c) % 2 == 0]
    W = [(r, c) for r in range(R) for c in range(C) if (r + c) % 2]
    p, prod = [None] * len(B), 1
    for a, b in t:
        bl, wh = (a, b) if (a[0] + a[1]) % 2 == 0 else (b, a)
        p[B.index(bl)] = W.index(wh)
        if signed and bl[1] == wh[1] and bl[1] % 2 == 1:
            prod = -prod
    sg = round(np.linalg.det(np.eye(len(p))[p]))
    return sg * prod


T44 = all_tilings(4, 4)
PLAIN44 = [tiling_sign(t, 4, 4, False) for t in T44]
KAST44 = [tiling_sign(t, 4, 4, True) for t in T44]
assert PLAIN44.count(1) == 18 and PLAIN44.count(-1) == 18 and len(set(KAST44)) == 1
assert sum(KAST44) == kast_det(4, 4)


def k33(scale=1.0, center=ORIGIN):
    top = [center + scale * np.array([x, 1.1, 0]) for x in (-1.6, 0, 1.6)]
    bot = [center + scale * np.array([x, -1.1, 0]) for x in (-1.6, 0, 1.6)]
    edges = VGroup(*[Line(a, b, color=YELLOW, stroke_width=3 * scale + 1) for a in top for b in bot])
    dots = VGroup(*[Dot(p, radius=0.09 * scale + 0.02, color=WHITE) for p in top + bot])
    return VGroup(edges, dots)


class Board4x4(DScene):
    def construct(self):
        s = 0.9
        b = board(4, 4, s, origin=LEFT * 5.2 + UP * 1.6)
        # thumbnails of all 36 tilings, 4 rows x 9
        thumbs = VGroup()
        for t in T44:
            bb = board(4, 4, 0.13)
            bb.add(*[domino(bb.sq, x, y, 0.13) for x, y in t])
            thumbs.add(bb)
        thumbs.arrange_in_grid(4, 9, buff=(0.12, 0.3)).move_to(RIGHT * 3.6 + DOWN * 1.35)

        # 0: a 4x4 board has 36 tilings
        self.cue(0)
        self.play(FadeIn(b), run_time=0.8)
        self.cue_at(0, "thirty-six", lead=0.3)
        self.play(LaggedStartMap(FadeIn, thumbs, lag_ratio=0.06, scale=0.7), run_time=2.4)
        n36 = T("36 tilings", 30, YELLOW).next_to(thumbs, UP, buff=0.3)
        self.play(FadeIn(n36), run_time=0.5)

        # 1: the plain matrix (8 x 8) says zero
        self.cue(1)
        pm = T("plain matrix A: 8 × 8, ones where squares touch", 24, SOFT).move_to(RIGHT * 2.0 + UP * 3.3)
        self.play(FadeIn(pm), run_time=0.6)
        plain = VGroup(T("det A = 0", 42, BAD), cross(0.35)).arrange(RIGHT, buff=0.3).next_to(pm, DOWN, buff=0.35)
        self.cue_at(1, "It says", lead=0.2)
        self.sfx("buzz")
        self.play(FadeIn(plain), run_time=0.7)

        # 2: 18 tilings with +, 18 with −: they cancel
        self.cue(2)
        frames = VGroup(*[SurroundingRectangle(th, color=GOOD if v > 0 else BAD, buff=0.04, stroke_width=3)
                          for th, v in zip(thumbs, PLAIN44)])
        marks = VGroup(*[T("+" if v > 0 else "−", 24, GOOD if v > 0 else BAD).next_to(th, DOWN, buff=0.02)
                         for th, v in zip(thumbs, PLAIN44)])
        self.play(LaggedStartMap(Create, frames, lag_ratio=0.03), LaggedStartMap(FadeIn, marks, lag_ratio=0.03), run_time=2.0)
        # sort: the 18 plus tilings on top, the 18 minus below
        order = [k for k in range(36) if PLAIN44[k] > 0] + [k for k in range(36) if PLAIN44[k] < 0]
        slots = thumbs.copy().arrange_in_grid(4, 9, buff=(0.12, 0.3)).move_to(thumbs)
        self.cue_at(2, "eighteen tilings", lead=0.2)
        self.play(*[VGroup(thumbs[k], frames[k], marks[k]).animate.shift(slots[i].get_center() - thumbs[k].get_center())
                    for i, k in enumerate(order)], run_time=1.4)
        lab_p = T("18 ×  +1", 28, GOOD).next_to(VGroup(*[thumbs[k] for k in order[:18]]), LEFT, buff=0.25)
        lab_m = T("18 ×  −1", 28, BAD).next_to(VGroup(*[thumbs[k] for k in order[18:]]), LEFT, buff=0.25)
        VGroup(lab_p, lab_m).set_x(min(lab_p.get_x(), -0.05))
        self.play(FadeIn(lab_p), FadeIn(lab_m), run_time=0.6)
        canc = T("18 − 18 = 0", 30, SOFT).next_to(plain, DOWN, buff=0.25).align_to(plain, LEFT)
        self.cue_at(2, "They cancel", lead=0.2)
        self.play(FadeIn(canc), run_time=0.6)

        # 3: Kasteleyn: minus signs on the vertical edges of every other column
        self.cue(3)
        g = signed_graph(b, 4, 4, s)
        self.play(Create(g), run_time=1.6)
        rule = T("−1 on the vertical edges\nof every other column", 24, FLIP, line_spacing=1.1).next_to(b, DOWN, buff=0.3)
        self.play(FadeIn(rule), run_time=0.6)

        # 4: now all 36 get the same sign: |det A| = 36
        self.cue(4)
        same = KAST44[0]
        col = GOOD if same > 0 else BAD
        flips = [k for k in range(36) if PLAIN44[k] != same]
        self.play(*[frames[k].animate.set_color(col) for k in flips],
                  *[Transform(marks[k], T("+" if same > 0 else "−", 24, col).move_to(marks[k])) for k in flips],
                  Transform(VGroup(lab_p, lab_m), T(f"36 ×  {'+' if same > 0 else '−'}1", 28, col).move_to(VGroup(lab_p, lab_m))),
                  run_time=1.2)
        signed = VGroup(T(f"|det A| = {abs(kast_det(4, 4))}", 42, YELLOW), tick(0.35)).arrange(RIGHT, buff=0.3)
        signed.move_to(VGroup(plain, canc)).align_to(plain, LEFT)
        self.cue_at(4, "the determinant gives", lead=0.2)
        self.sfx("chime")
        self.play(FadeOut(VGroup(plain, canc)), FadeIn(signed), run_time=0.8)
        self.cue_end(4)
        self.wait(0.5)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.6)


def superpose_loops(t1, t2):
    """The closed loops where two tilings differ (each loop = its list of squares in order)."""
    adj = {}
    for t in (t1, t2):
        for a, b in t:
            adj.setdefault(a, []).append(b)
            adj.setdefault(b, []).append(a)
    seen, out = set(), []
    for v in adj:
        if v in seen or adj[v][0] == adj[v][1]:
            continue
        cyc, cur = [v], v
        seen.add(v)
        while True:
            nxt = [x for x in adj[cur] if x not in seen]
            if not nxt:
                break
            cur = nxt[0]
            seen.add(cur)
            cyc.append(cur)
        out.append(cyc)
    return out


def is_minus(a, b):
    return a[1] == b[1] and a[1] % 2 == 1


WA, WB = T44[0], T44[13]                                         # all flat / two loops (4 and 8 squares)
LOOPS = sorted(superpose_loops(WA, WB), key=len)
assert [len(c) for c in LOOPS] == [4, 8]
for c in LOOPS:                                                  # k-cycle: k-1 swaps; minus edges make it even
    k, L = len(c) // 2, len(c)
    assert (k - 1 + sum(is_minus(c[i], c[(i + 1) % L]) for i in range(L))) % 2 == 0
assert [sum(is_minus(c[i], c[(i + 1) % len(c)]) for i in range(len(c))) for c in LOOPS] == [1, 1]
TINT_B = PINK


class KastWhy(DScene):
    """Why Kasteleyn's rule works: superpose two tilings -> loops; turning a loop of 2k squares
    = k-1 swaps, and the rule gives it exactly the right number of minus edges: an even number of flips."""

    def construct(self):
        s = 0.9
        b = board(4, 4, s, origin=LEFT * 5.2 + UP * 1.6)
        g = signed_graph(b, 4, 4, s)
        c = lambda k: b.sq[k].get_center()
        R = -1.5                                                     # right-hand column x

        # 0: every little square has exactly one minus sign
        self.cue(0)
        self.play(FadeIn(b), Create(g), run_time=1.2)
        loop = Square(s, color=YELLOW, stroke_width=8).move_to(b.sq[(0, 0)].get_corner(DR))
        cnt = T("1 minus sign: odd", 30, FLIP).move_to(RIGHT * 1.6 + UP * 1.6)
        self.cue_at(0, "Look at any", lead=0.2)
        self.play(Create(loop), run_time=0.6)
        self.cue_at(0, "exactly one", lead=0.2)
        self.play(FadeIn(cnt), run_time=0.5)
        for rc in [(0, 1), (1, 2), (2, 0), (2, 2)]:
            self.play(loop.animate.move_to(b.sq[rc].get_corner(DR)), run_time=0.5)
            self.play(Indicate(cnt, color=FLIP, scale_factor=1.1), run_time=0.35)

        # 1: Kasteleyn's rule
        self.cue(1)
        self.play(FadeOut(loop), FadeOut(cnt), run_time=0.4)
        rule = VGroup(T("• every little square: odd number of −", 26),
                      T("  ⇒  every tiling: the same sign", 26, YELLOW)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        rule.move_to(np.array([R, 2.9, 0]), aligned_edge=LEFT)
        self.play(FadeIn(rule[0]), run_time=0.6)
        self.cue_at(1, "then every", lead=0.2)
        self.play(FadeIn(rule[1]), run_time=0.6)
        why = T("why?", 30, SOFT).next_to(rule, DOWN, buff=0.25).align_to(rule, LEFT)
        self.cue_at(1, "see why", lead=0.2)
        self.play(FadeIn(why), run_time=0.4)

        # 2: two tilings, one on top of the other
        self.cue(2)
        thumbs = VGroup()
        for t, col in ((WA, DOMINO), (WB, TINT_B)):
            bb = board(4, 4, 0.3)
            bb.add(*[domino(bb.sq, x, y, 0.3, color=col) for x, y in t])
            thumbs.add(bb)
        thumbs.arrange(RIGHT, buff=0.5).move_to(np.array([2.4, 0.9, 0]))
        self.play(FadeOut(why), FadeIn(thumbs[0], shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(thumbs[1], shift=UP * 0.2), run_time=0.6)
        self.play(g.animate.set_stroke(opacity=0.2), run_time=0.4)
        off = 0.07
        la = VGroup(*[Line(c(x) + UP * off * (x[0] == y[0]) + LEFT * off * (x[1] == y[1]),
                           c(y) + UP * off * (x[0] == y[0]) + LEFT * off * (x[1] == y[1]), color=DOMINO, stroke_width=9)
                      for x, y in WA])
        lb = VGroup(*[Line(c(x) + DOWN * off * (x[0] == y[0]) + RIGHT * off * (x[1] == y[1]),
                           c(y) + DOWN * off * (x[0] == y[0]) + RIGHT * off * (x[1] == y[1]), color=TINT_B, stroke_width=9)
                      for x, y in WB])
        self.play(TransformFromCopy(thumbs[0], la), run_time=0.9)
        self.play(TransformFromCopy(thumbs[1], lb), run_time=0.9)

        # 3: where they agree nothing happens; where they differ, closed loops (two here)
        self.cue(3)
        same = {frozenset(e) for e in WA} & {frozenset(e) for e in WB}
        agree = VGroup(*[ln for ln, e in zip(la, WA) if frozenset(e) in same],
                       *[ln for ln, e in zip(lb, WB) if frozenset(e) in same])
        self.cue_at(3, "Where they agree", lead=0.2)
        self.play(agree.animate.set_color(GREY_D), run_time=0.7)
        self.cue_at(3, "closed loops", lead=0.2)
        halos = VGroup(*[Polygon(*[c(v) for v in cyc], color=YELLOW, stroke_width=3, fill_opacity=0.12, fill_color=YELLOW)
                         for cyc in LOOPS])
        for h in halos:
            self.play(FadeIn(h), run_time=0.6)
        two = T("2 loops", 28, YELLOW).next_to(thumbs, DOWN, buff=0.35)
        self.play(FadeIn(two), run_time=0.4)

        # 4: switching tilings = turning each loop (every domino slides over by one)
        self.cue(4)
        onloop = [ln for ln, e in zip(la, WA) if frozenset(e) not in same]
        tgt = [ln for ln, e in zip(lb, WB) if frozenset(e) not in same]
        ghost = VGroup(*[x.copy() for x in onloop])
        self.cue_at(4, "you turn", lead=0.2)
        self.play(*[Transform(gh, tg.copy().set_color(DOMINO)) for gh, tg in zip(ghost, tgt)], run_time=1.2)
        self.play(FadeOut(ghost), run_time=0.4)

        # 5: the small loop: flat -> standing, one swap: the sign flips once
        self.cue(5)
        tally = VGroup()
        h1 = T("small loop", 28, YELLOW).move_to(np.array([R, -0.75, 0]), aligned_edge=LEFT)
        self.play(Indicate(halos[0], color=YELLOW, scale_factor=1.05), FadeOut(two), FadeIn(h1), run_time=0.8)
        sm = [ln for ln, e in zip(la, WA) if set(e) <= set(LOOPS[0])]
        smt = [ln for ln, e in zip(lb, WB) if set(e) <= set(LOOPS[0])]
        gh = VGroup(*[x.copy() for x in sm])
        self.cue_at(5, "Two flat", lead=0.2)
        self.play(*[Transform(x, y.copy().set_color(DOMINO)) for x, y in zip(gh, smt)], run_time=1.0)
        self.play(FadeOut(gh), run_time=0.3)
        f1 = T("1 swap  →  1 flip", 22).next_to(h1, DOWN, buff=0.15).align_to(h1, LEFT)
        self.cue_at(5, "one swap", lead=0.2)
        self.play(FadeIn(f1), run_time=0.5)

        # 6: but it uses one minus edge: a second flip -> no change
        self.cue(6)
        me = next((x, y) for x, y in WB if set((x, y)) <= set(LOOPS[0]) and is_minus(x, y))
        mline = Line(c(me[0]), c(me[1]), color=FLIP, stroke_width=12)
        self.cue_at(6, "one minus edge", lead=0.2)
        self.sfx("flip")
        self.play(Create(mline), Flash(mline.get_center(), color=FLIP), run_time=0.7)
        f2 = T("1 minus edge  →  +1 flip", 22, FLIP).next_to(f1, DOWN, buff=0.1).align_to(h1, LEFT)
        self.play(FadeIn(f2), run_time=0.5)
        ok1 = VGroup(T("2 flips: no change", 22, GOOD), tick(0.28)).arrange(RIGHT, buff=0.2).next_to(f2, DOWN, buff=0.1).align_to(h1, LEFT)
        self.cue_at(6, "Two flips", lead=0.2)
        self.sfx("tick")
        self.play(FadeIn(ok1), run_time=0.5)
        self.play(FadeOut(mline), run_time=0.3)

        # 7: the big loop: three swaps, one minus edge: four flips -> no change
        self.cue(7)
        blk = VGroup(h1, f1, f2, ok1)
        self.play(blk.animate.set_opacity(0.35), Indicate(halos[1], color=YELLOW, scale_factor=1.03), run_time=0.8)
        h2 = T("big loop", 28, YELLOW).move_to(np.array([2.7, -0.75, 0]), aligned_edge=LEFT)
        bg = [ln for ln, e in zip(la, WA) if set(e) <= set(LOOPS[1])]
        bgt = [ln for ln, e in zip(lb, WB) if set(e) <= set(LOOPS[1])]
        gh = VGroup(*[x.copy() for x in bg])
        self.play(FadeIn(h2), *[Transform(x, y.copy().set_color(DOMINO)) for x, y in zip(gh, bgt)], run_time=1.2)
        self.play(FadeOut(gh), run_time=0.3)
        g1 = T("3 swaps  →  3 flips", 22).next_to(h2, DOWN, buff=0.15).align_to(h2, LEFT)
        self.cue_at(7, "three swaps", lead=0.2)
        self.play(FadeIn(g1), run_time=0.5)
        me2 = next((x, y) for x, y in WB if set((x, y)) <= set(LOOPS[1]) and is_minus(x, y))
        mline2 = Line(c(me2[0]), c(me2[1]), color=FLIP, stroke_width=12)
        self.cue_at(7, "one minus edge", lead=0.2)
        self.sfx("flip")
        self.play(Create(mline2), Flash(mline2.get_center(), color=FLIP), run_time=0.7)
        g2 = T("1 minus edge  →  +1 flip", 22, FLIP).next_to(g1, DOWN, buff=0.1).align_to(h2, LEFT)
        self.play(FadeIn(g2), run_time=0.5)
        ok2 = VGroup(T("4 flips: no change", 22, GOOD), tick(0.28)).arrange(RIGHT, buff=0.2).next_to(g2, DOWN, buff=0.1).align_to(h2, LEFT)
        self.cue_at(7, "Again", lead=0.2)
        self.sfx("tick")
        self.play(FadeIn(ok2), blk.animate.set_opacity(1), run_time=0.6)
        self.play(FadeOut(mline2), run_time=0.3)

        # 8: Kasteleyn: always an even number of flips per loop
        self.cue(8)
        gen = T("every loop: an even number of flips", 28, YELLOW).move_to(np.array([2.0, -2.85, 0]))
        self.play(FadeIn(gen, shift=UP * 0.15), run_time=0.7)

        # 9: so all tilings have the same sign; |det| counts them all
        self.cue(9)
        fin = VGroup(T("all tilings: the same sign", 28, GOOD), T("|det A| = number of tilings", 32, YELLOW)) \
            .arrange(DOWN, buff=0.15).move_to(np.array([2.0, -3.05, 0]))
        self.play(FadeOut(gen), FadeIn(fin[0]), run_time=0.6)
        self.cue_at(9, "the determinant counts", lead=0.2)
        self.sfx("chime")
        self.play(Write(fin[1]), run_time=0.9)
        self.cue_end(9)
        self.wait(0.6)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.6)


class FKT(DScene):
    def construct(self):
        s = 0.6
        big = board(8, 8, s, origin=LEFT * 5.6 + UP * 2.1)
        g = signed_graph(big, 8, 8, s, width=2)
        # 0: the chessboard, same signs, the number
        self.cue(0)
        self.play(FadeIn(big), run_time=0.8)
        self.cue_at(0, "with the same signs", lead=0.2)
        self.play(Create(g, lag_ratio=0.01), run_time=2.0)
        num = T("|det| = 12,988,816", 44, YELLOW, weight=BOLD).move_to(RIGHT * 2.8 + UP * 2.6)
        self.cue_at(0, "twelve million")
        self.sfx("chime")
        self.play(FadeIn(num, scale=1.2))

        # 1: one per second: five months; the determinant: an instant
        self.cue(1)
        slow = T("listing, one per second:  ≈ 5 months", 26, SOFT).next_to(num, DOWN, buff=0.35)
        fast = T("the determinant:  an instant", 26, GOOD).next_to(slow, DOWN, buff=0.15).align_to(slow, LEFT)
        self.play(FadeIn(slow), run_time=0.6)
        self.cue_at(1, "The determinant", lead=0.2)
        self.play(FadeIn(fast), run_time=0.6)

        # 2: squares -> vertices, dominoes -> edges, tiling = perfect matching
        self.cue(2)
        self.play(g.animate.set_stroke(opacity=0.15), FadeOut(VGroup(slow, fast)), run_time=0.4)
        cur = None
        for seed in range(4, 10):
            nd = VGroup(*[domino(big.sq, x, y, s) for x, y in random_tiling(8, 8, seed)])
            if cur is None:
                self.play(FadeIn(nd), run_time=0.3)
            else:
                self.remove(cur)
                self.add(nd)
                self.wait(0.2)
            cur = nd
        til = random_tiling(8, 8, 9)
        dots = VGroup(*[Dot(big.sq[k].get_center(), radius=0.07, color=WHITE) for k in big.sq])
        self.cue_at(2, "Squares are")
        self.play(FadeOut(g), big.animate.set_fill(opacity=0.12).set_stroke(opacity=0.2), FadeIn(dots),
                  cur.animate.set_fill(opacity=0.35), run_time=0.8)
        edges = VGroup(*[Line(big.sq[a].get_center(), big.sq[b].get_center(), color=YELLOW, stroke_width=7)
                         for a, b in til])
        self.cue_at(2, "dominoes are")
        self.play(ReplacementTransform(cur, edges), run_time=0.9)
        pm = T("a tiling = a perfect matching", 32, YELLOW).next_to(num, DOWN, buff=0.45)
        self.cue_at(2, "a tiling is")
        self.play(FadeIn(pm))

        # 3: any planar graph: the FKT algorithm
        self.cue(3)
        V = [np.array([1.6 * np.cos(TAU * k / 8 + PI / 8), 1.6 * np.sin(TAU * k / 8 + PI / 8), 0]) for k in range(8)] + \
            [np.array([0.65 * np.cos(TAU * k / 4 + PI / 4), 0.65 * np.sin(TAU * k / 4 + PI / 4), 0]) for k in range(4)]
        E = [(k, (k + 1) % 8) for k in range(8)] + [(8 + k, 8 + (k + 1) % 4) for k in range(4)] + \
            [(2 * k, 8 + k) for k in range(4)] + [(2 * k + 1, 8 + k) for k in range(4)] + [(8, 10)]
        Mt = [(1, 2), (3, 4), (5, 6), (7, 0), (8, 9), (10, 11)]
        ctr = LEFT * 3.5 + DOWN * 0.1
        pg = VGroup(*[Line(ctr + V[a], ctr + V[b], color=GREY_B, stroke_width=3) for a, b in E])
        pd = VGroup(*[Dot(ctr + v, radius=0.09, color=WHITE) for v in V])
        pmat = VGroup(*[Line(ctr + V[a], ctr + V[b], color=YELLOW, stroke_width=8) for a, b in Mt])
        assert sorted(x for e in Mt for x in e) == list(range(12)) and all(e in E or e[::-1] in E for e in Mt)
        self.play(FadeOut(VGroup(big, dots, edges)), FadeIn(pg), FadeIn(pd), run_time=0.8)
        self.cue_at(3, "without crossings")
        self.play(Create(pmat), run_time=0.8)
        fkt = VGroup(T("the FKT algorithm", 34, YELLOW),
                     T("chessboard: Kasteleyn; Temperley & Fisher, 1961", 24),
                     T("all planar graphs: Kasteleyn, 1967", 24),
                     T("perfect matchings of any planar graph", 28),
                     T("in polynomial time", 30, GOOD)).arrange(DOWN, buff=0.1)
        fkt.scale_to_fit_width(min(fkt.width, 5.6))
        box = SurroundingRectangle(fkt, color=YELLOW, buff=0.2, corner_radius=0.15)
        VGroup(fkt, box).next_to(pm, DOWN, buff=0.35)
        if box.get_right()[0] > 6.9:
            VGroup(fkt, box).shift(LEFT * (box.get_right()[0] - 6.9))
        self.cue_at(3, "This is the FKT")
        self.play(Create(box), FadeIn(fkt, lag_ratio=0.2))

        # 4: (option F) the story kept going: Vazirani 1989 (no K3,3 inside), Valiant's holographic algorithms
        self.cue(4)
        fk = VGroup(fkt, box)
        self.play(FadeOut(VGroup(num, pm, pg, pd, pmat)), fk.animate.to_edge(UP, buff=0.35).set_x(3.6), run_time=0.8)
        kk = k33(0.85, LEFT * 3.6 + DOWN * 0.2)
        kl = T("K₃,₃", 34, YELLOW).next_to(kk, DOWN, buff=0.3)
        v1 = VGroup(T("1989 · Vijay Vazirani", 28, YELLOW), T("graphs with no K₃,₃ hiding inside", 24)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        v2 = VGroup(T("2004 · Leslie Valiant", 28, YELLOW), T("holographic algorithms, built on FKT", 24)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        VGroup(v1, v2).arrange(DOWN, buff=0.45, aligned_edge=LEFT).next_to(fk, DOWN, buff=0.6).align_to(fk, LEFT)
        self.cue_at(4, "In 1989", lead=0.2)
        self.play(Create(kk[0], lag_ratio=0.1), FadeIn(kk[1]), FadeIn(kl), FadeIn(v1), run_time=1.4)
        self.cue_at(4, "Leslie Valiant", lead=0.2)
        self.play(FadeIn(v2), run_time=0.8)

        # 5: let the board go to infinity
        self.cue(5)
        self.play(FadeOut(VGroup(kk, kl, v1, v2, fk)), run_time=0.5)
        num2 = T("|det| = 12,988,816", 40, YELLOW, weight=BOLD).move_to(RIGHT * 3.0 + UP * 1.0)
        self.play(FadeIn(num2), run_time=0.5)
        from PIL import Image as _Im
        import os as _os
        out = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "media", "boards")
        _os.makedirs(out, exist_ok=True)
        cur = None
        lab = None
        for n in (8, 16, 32, 64, 128):
            px = max(2, 512 // n)
            arr = np.zeros((n * px, n * px, 3), np.uint8)
            for r in range(n):
                for c in range(n):
                    v = 70 if (r + c) % 2 == 0 else 200
                    arr[r * px:(r + 1) * px, c * px:(c + 1) * px] = v
            f = _os.path.join(out, f"b{n}.png")
            _Im.fromarray(arr).save(f)
            im = ImageMobject(f).set_height(4.8).move_to(LEFT * 3.5 + DOWN * 0.1)
            nl = T(f"{n} × {n}", 30, SOFT).next_to(im, DOWN, buff=0.15)
            self.play(FadeIn(im), FadeIn(nl), *([FadeOut(cur), FadeOut(lab)] if cur else []), run_time=0.45)
            cur, lab = im, nl
        inf = T("tilings ≈ e^(0.29 × area)", 30, YELLOW).next_to(num2, DOWN, buff=0.4)
        gl = T("0.29… = G/π,  G = Catalan's constant", 24, SOFT).next_to(inf, DOWN, buff=0.12)
        self.play(FadeIn(inf), FadeIn(gl))
        self.cue_end(5)
        self.wait(0.6)
