"""Act 8 — Counting #4: dominoes (Script v2, 13:00-15:15).

    Dominoes8x8   a chessboard fills with dominoes: 12,988,816 tilings
    SmallBoard2   2x3 board, 3 tilings, the 0/1 table, det = -1 (signs +, -, -)
    SignFix2      Kasteleyn's one minus sign: det = -3, so 3
    Board4x4      plain det = 0 ("very confident, very wrong"); signed |det| = 36
    FKT           the pattern on 8x8; the rule; perfect matchings of planar graphs; FKT
"""
from common import *
from act7_kasteleyn import (board, domino, random_tiling, table_mob, entry_index, TILINGS, TABLE,
                            FLIP)


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


class Board4x4(DScene):
    def construct(self):
        s = 0.9
        b = board(4, 4, s, origin=LEFT * 5.2 + UP * 1.6)
        self.cue(0)
        self.play(FadeIn(b))
        plain = VGroup(T("det A = 0", 42, BAD), cross(0.35)).arrange(RIGHT, buff=0.3).move_to(RIGHT * 2.2 + UP * 2.0)
        self.sfx("buzz")
        self.play(FadeIn(plain), run_time=0.7)            # "very confident, very wrong" is spoken, not written
        joke = plain
        self.cue(1)
        g = signed_graph(b, 4, 4, s)
        self.play(Create(g), run_time=1.5)
        rule = T("−1 on the vertical edges\nof every other column", 26, FLIP, line_spacing=1.1).next_to(joke, DOWN, buff=0.6, aligned_edge=LEFT)
        self.play(FadeIn(rule))
        signed = T(f"|det A| = {abs(kast_det(4, 4))}", 44, YELLOW).next_to(rule, DOWN, buff=0.4, aligned_edge=LEFT)
        self.sfx("chime")
        self.play(Write(signed))
        tils = all_tilings(4, 4)
        sample = VGroup()
        for t in tils[::6][:6]:
            bb = board(4, 4, 0.3)
            bb.add(*[domino(bb.sq, x, y, 0.3) for x, y in t])
            sample.add(bb)
        sample.arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.4).shift(RIGHT * 1.6)
        lab = VGroup()
        self.play(LaggedStartMap(FadeIn, sample, lag_ratio=0.2), FadeIn(lab), run_time=1.5)


class FKT(DScene):
    def construct(self):
        s = 0.6
        big = board(8, 8, s, origin=LEFT * 5.6 + UP * 2.1)
        g = signed_graph(big, 8, 8, s, width=2)
        self.cue(0)
        self.play(FadeIn(big), run_time=0.8)
        self.play(Create(g, lag_ratio=0.01), run_time=2.0)
        num = T("|det| = 12,988,816", 44, YELLOW, weight=BOLD).move_to(RIGHT * 2.8 + UP * 2.6)
        self.cue_at(0, "twelve million")
        self.sfx("chime")
        self.play(FadeIn(num, scale=1.2))
        # 1: the rule
        self.cue(1)
        rule = VGroup(T("every little loop of four edges", 28),
                      T("has an odd number of minus signs", 28)).arrange(DOWN, buff=0.06).next_to(num, DOWN, buff=0.35)
        loop = Square(s, color=FLIP, stroke_width=7).move_to(big.sq[(3, 4)].get_corner(DR))
        self.play(FadeIn(rule), Create(loop))
        self.play(loop.animate.move_to(big.sq[(1, 1)].get_corner(DR)), run_time=0.7)
        self.play(loop.animate.move_to(big.sq[(5, 2)].get_corner(DR)), run_time=0.7)
        self.play(FadeOut(loop))
        # 2: squares -> vertices, dominoes -> edges, tiling = perfect matching
        self.cue(2)
        self.play(g.animate.set_stroke(opacity=0.15), run_time=0.3)
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
        pm = T("a tiling = a perfect matching", 32, YELLOW).next_to(rule, DOWN, buff=0.45)
        self.cue_at(2, "a tiling is")
        self.play(FadeIn(pm))
        # 3: any planar graph
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
        self.cue_at(3, "the FKT")
        self.play(Create(box), FadeIn(fkt, lag_ratio=0.2))
        # 4: let the board go to infinity
        self.cue(4)
        self.play(FadeOut(VGroup(pg, pd, pmat)), run_time=0.4)
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
        inf = T("tilings ≈ e^(0.29 × area)", 30, YELLOW).next_to(cur, DOWN, buff=0.15)
        gl = T("0.29… = G/π,  G = Catalan's constant", 24, SOFT).next_to(inf, DOWN, buff=0.08)
        self.play(FadeOut(lab), FadeIn(inf), FadeIn(gl))
