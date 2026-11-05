"""Act 0 — Cold open (0:00-1:00).

    ColdOpen   two ants, their homes, a near miss, the question, a flash of det
"""
from common import *


def matrix_mob(rows, size=44, color=INK, h_buff=0.75, v_buff=0.6):
    """A bracketed grid of numbers built from Text (no LaTeX)."""
    cells = VGroup(*[T(str(v), size, color) for r in rows for v in r])
    cells.arrange_in_grid(len(rows), len(rows[0]), buff=(h_buff, v_buff))
    h = cells.height + 0.35
    l = VMobject(stroke_color=color, stroke_width=3).set_points_as_corners(
        [UP * h / 2 + RIGHT * 0.15, UP * h / 2, DOWN * h / 2, DOWN * h / 2 + RIGHT * 0.15])
    r = l.copy().flip(UP)
    l.next_to(cells, LEFT, buff=0.18)
    r.next_to(cells, RIGHT, buff=0.18)
    g = VGroup(l, cells, r)
    g.cells = cells
    return g


class ColdOpen(DScene):
    def construct(self):
        lat = Lattice(4, spacing=1.3, center=LEFT * 3 + DOWN * 0.3)
        ends = endpoints(lat)
        self.play(LaggedStartMap(FadeIn, lat, lag_ratio=0.04, run_time=1.2))
        a1 = ant(ANT1).move_to(lat.p(*A1))
        a2 = ant(ANT2).move_to(lat.p(*A2))
        self.play(FadeIn(ends[0]), FadeIn(ends[2]), FadeIn(a1, scale=0.3), FadeIn(a2, scale=0.3))
        self.wait(1.5)
        # their homes, with an arrow from each ant to its own house
        self.play(FadeIn(ends[4], shift=DOWN * 0.3), FadeIn(ends[6], shift=DOWN * 0.3))
        h1 = CurvedArrow(lat.p(*A1) + UP * 0.35, lat.p(*B1) + LEFT * 0.35,
                         angle=-PI / 3, color=ANT1)
        h2 = CurvedArrow(lat.p(*A2) + RIGHT * 0.4, lat.p(*B2) + DOWN * 0.35,
                         angle=PI / 3, color=ANT2)
        self.play(Create(h1), Create(h2), run_time=1.2)
        self.play(FadeIn(VGroup(ends[1], ends[3], ends[5], ends[7])))
        self.wait(2)
        self.play(FadeOut(h1), FadeOut(h2))

        # they had a fight
        fight = T("They had a fight.", 36).to_edge(RIGHT, buff=1.2).shift(UP * 1.5)
        self.play(Write(fight))
        self.wait(2)

        # near miss at (1, 1)
        spot = lat.p(1, 1)
        self.play(a1.animate.move_to(lat.p(0.62, 1)),
                  Rotate(a2, PI / 2, about_point=a2.get_center()), run_time=0.6)
        a2.heading = PI / 2
        self.play(a2.animate.move_to(lat.p(1, 0.62)), run_time=0.8)
        ring = Circle(radius=0.45, color=MEET, stroke_width=5).move_to(spot)
        bangs = VGroup(T("!", 48, MEET, weight=BOLD).next_to(a1, UP, buff=0.05),
                       T("!", 48, MEET, weight=BOLD).next_to(a2, RIGHT, buff=0.05))
        self.sfx("alert")
        self.play(Create(ring), FadeIn(bangs, scale=2), run_time=0.4)
        self.play(ring.animate.scale(1.2), rate_func=there_and_back, run_time=0.5)
        self.wait(0.8)
        # awkward retreat
        self.play(a1.animate.move_to(lat.p(*A1)), a2.animate.move_to(lat.p(*A2)),
                  FadeOut(ring), FadeOut(bangs), run_time=0.9, rate_func=rush_from)
        self.play(Wiggle(a1, scale_value=1.05, rotation_angle=0.05 * TAU),
                  Wiggle(a2, scale_value=1.05, rotation_angle=0.05 * TAU))
        self.wait(1)

        # the question
        q = T("How many ways can they\nboth get home without\never meeting?", 40,
              line_spacing=1.2).next_to(fight, DOWN, buff=0.8, aligned_edge=LEFT)
        self.play(Write(q), run_time=2)
        self.wait(3)

        # flash: four numbers in a little square, then "det"
        self.play(FadeOut(fight), q.animate.scale(0.75).to_edge(UP, buff=0.6).to_edge(RIGHT, buff=0.8))
        m = matrix_mob([[6, 4], [4, 6]]).move_to(RIGHT * 3.6 + DOWN * 0.6)
        det = T("det", 44, YELLOW).next_to(m, LEFT, buff=0.35)
        self.play(FadeIn(m, scale=0.8))
        self.wait(0.5)
        self.sfx("chime")
        self.play(Write(det))
        self.play(Indicate(VGroup(det, m), color=YELLOW, scale_factor=1.1))
        self.wait(2)
        yes = T("Yes. That determinant.", 30, SOFT).next_to(m, DOWN, buff=0.7)
        self.play(FadeIn(yes, shift=UP * 0.2))
        self.wait(3)

        # title
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob is not None])
        title = T("How Determinants Can Count", 60, weight=BOLD)
        sub = T("what the minus signs are really doing", 30, SOFT).next_to(title, DOWN, buff=0.4)
        self.sfx("whoosh")
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.2))
        self.wait(3)
        self.play(FadeOut(title), FadeOut(sub))
