"""Quick still mockups for new storyboard beats (not final animations)."""
from common import *
from act7_kasteleyn import board, domino, random_tiling


class MockDet(Scene):
    def construct(self):
        m = matrix_mob([["a", "b"], ["c", "d"]], size=72).shift(LEFT * 2.5)
        c = m.cells
        g = Line(c[0].get_center(), c[3].get_center(), color=GOOD, stroke_width=10).set_opacity(0.6)
        r = Line(c[1].get_center(), c[2].get_center(), color=BAD, stroke_width=10).set_opacity(0.6)
        f = VGroup(T("=", 64), T("a d", 64, GOOD), T("−", 64), T("b c", 64, BAD)).arrange(RIGHT, buff=0.35).next_to(m, RIGHT, buff=0.6)
        t = T("You've met the determinant.", 40).to_edge(UP, buff=0.8)
        self.add(g, r, m, f, t)


class MockCounts(Scene):
    def construct(self):
        d = T("det", 96, YELLOW).shift(LEFT * 2)
        a = T("→  it counts", 60).next_to(d, RIGHT, buff=0.5)
        self.add(d, a)


class MockChess(Scene):
    def construct(self):
        s = 0.62
        s = 0.55
        b = board(8, 8, s, origin=LEFT * 6.3 + UP * 1.9)
        doms = VGroup(*[domino(b.sq, x, y, s) for x, y in random_tiling(8, 8, 5)])
        q = T("How many domino tilings?", 38).move_to(RIGHT * 2.6 + UP * 2.6)
        clock = VGroup(Circle(radius=0.9, color=INK), Line(ORIGIN, UP * 0.7, color=INK), Line(ORIGIN, RIGHT * 0.5, color=INK)) \
            .scale(0.7).move_to(RIGHT * 0.6 + UP * 0.6)
        l1 = VGroup(T("listing one per second:", 28, SOFT), T("about 5 months", 40, BAD)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(clock, RIGHT, buff=0.4)
        l2 = VGroup(T("one determinant:", 28, SOFT), T("12,988,816, instantly", 34, GOOD)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(l1, DOWN, buff=0.8, aligned_edge=LEFT)
        self.add(b, doms, q, clock, l1, l2)


class MockScent(Scene):
    def construct(self):
        lat = Lattice(4, spacing=1.45, center=LEFT * 3.2 + DOWN * 0.2)
        ends = endpoints(lat, scale=1.15)
        P = [(0, 1), (1, 1), (1, 2), (2, 2), (2, 3)]
        trail = VGroup(*[path_mob(lat, P, ANT1, w).set_stroke(opacity=o) for w, o in [(28, 0.12), (18, 0.22), (8, 0.9)]])
        a1 = ant(ANT1, 0.9).move_to(lat.p(*B1))
        a2 = ant(ANT2, 0.9).move_to(lat.p(1.55, 0.6))
        bang = speech("!", a2, UP, color=BAD, size=48)
        bang[1].set_color(BAD)
        back = Arrow(lat.p(1.9, 0.35), lat.p(2.7, 0.35), color=ANT2, buff=0.1)
        txt = VGroup(T("Neither will step on any dot", 34), T("the other one walks on.", 34),
                     T("Not even later:", 30, SOFT), T("ants leave a scent trail.", 30, SOFT)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.4).shift(UP * 0.8)
        self.add(lat, ends, trail, a1, a2, bang, back, txt)


class MockRecap(Scene):
    def construct(self):
        t = T("So far", 30, SOFT).to_edge(UP, buff=1.2)
        e = VGroup(T("det  =", 48), T("good", 48, GOOD), T("+ bad", 48, BAD), T("− swapped", 48, ORANGE)).arrange(RIGHT, buff=0.3)
        s = T("and bad = swapped, exactly", 36, YELLOW).next_to(e, DOWN, buff=0.6)
        self.add(t, e, s)
