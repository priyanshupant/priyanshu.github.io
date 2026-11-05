"""Act 5 — Any number of walkers (9:30-10:00).

    ManyWalkers   three non-touching paths on a 5x5 grid, 3x3 det = 50, n x n, history
"""
from common import *
from act0_cold_open import matrix_mob

S3 = [(0, 2), (1, 1), (2, 0)]
E3 = [(2, 4), (3, 3), (4, 2)]
P3 = [[(0, 2), (0, 3), (0, 4), (1, 4), (2, 4)],
      [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3)],
      [(2, 0), (3, 0), (4, 0), (4, 1), (4, 2)]]
COUNTS = [[6, 4, 1], [4, 6, 4], [1, 4, 6]]   # paths S_i -> E_j
DET3 = 50                                    # = number of non-touching triples (checked by brute force)


class ManyWalkers(DScene):
    def construct(self):
        lat = Lattice(5, spacing=1.0, center=LEFT * 3.6 + DOWN * 0.4)
        cols = [ANT1, ANT2, ANT3]
        self.play(FadeIn(lat))
        ants = []
        for k in range(3):
            d = Dot(lat.p(*S3[k]), radius=0.09, color=cols[k])
            h = house(cols[k], 0.3).move_to(lat.p(*E3[k]))
            a = ant(cols[k], 0.6).move_to(lat.p(*S3[k]))
            ants.append(a)
            self.add(d, h)
        self.play(*[FadeIn(a, scale=0.3) for a in ants])
        anims, _ = walk_steps(lat, [(ants[k], P3[k], cols[k]) for k in range(3)], step_time=0.35)
        for an in anims:
            self.play(an)
        self.wait(1)

        m = matrix_mob(COUNTS, size=40).move_to(RIGHT * 2.4 + UP * 1.4)
        for k, c in enumerate(m.cells):
            if k in (0, 4, 8):
                c.set_color(YELLOW)
        det = T(f"det = {DET3}", 40, YELLOW).next_to(m, DOWN, buff=0.5)
        same = T(f"= number of ways all three\nget home without touching", 26, SOFT,
                 line_spacing=1.15).next_to(det, DOWN, buff=0.3)
        self.play(FadeIn(m))
        self.sfx("chime")
        self.play(Write(det))
        self.play(FadeIn(same))
        self.wait(1.5)
        nn = T("n ants  →  n × n determinant", 32).next_to(same, DOWN, buff=0.5)
        self.play(Write(nn))
        self.wait(1.5)

        self.play(*[FadeOut(x) for x in self.mobjects])
        title = T("The Lindström–Gessel–Viennot lemma", 44, YELLOW).to_edge(UP, buff=0.8)
        people = VGroup(
            VGroup(T("Bernt Lindström", 34), T("1973", 30, SOFT),
                   T("motivation: matroid theory", 24, BLUE)).arrange(DOWN, buff=0.15),
            VGroup(T("Ira Gessel & Gérard Viennot", 34), T("1985", 30, SOFT),
                   T("rediscovered it, showed its power", 24, SOFT)).arrange(DOWN, buff=0.15),
        ).arrange(RIGHT, buff=1.2).next_to(title, DOWN, buff=1.0)
        self.play(Write(title))
        self.play(LaggedStartMap(FadeIn, people, lag_ratio=0.4, shift=UP * 0.2), run_time=1.5)
        self.wait(3)
        self.play(FadeOut(title), FadeOut(people))
