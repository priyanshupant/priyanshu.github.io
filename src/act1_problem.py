"""Act 1 — ant 1 and ant 2 refuse to meet (Script v2, 1:30-2:30).

    Problem   the grid, the homes, the three rules shown, the near miss, the question
"""
from common import *

GRID_C = LEFT * 4.05 + DOWN * 0.35


def grid_scene(scene, spacing=1.2, center=GRID_C, animate=True):
    lat = Lattice(GRID[0], spacing=spacing, center=center, ny=GRID[1])
    ends = endpoints(lat)
    L = ant(ANT1).move_to(lat.p(*A1))
    N = ant(ANT2).move_to(lat.p(*A2))
    if animate:
        scene.play(LaggedStartMap(FadeIn, lat, lag_ratio=0.03, run_time=1))
        scene.play(FadeIn(L, scale=0.5), FadeIn(N, scale=0.5))
    else:
        scene.add(lat, L, N)
    return lat, ends, L, N


class Problem(DScene):
    def construct(self):
        lat, ends, L, N = grid_scene(self)
        # homes
        self.play(FadeIn(VGroup(ends[4], ends[5]), shift=DOWN * 0.2), FadeIn(VGroup(ends[6], ends[7]), shift=DOWN * 0.2))
        self.play(FadeIn(VGroup(ends[0], ends[1], ends[2], ends[3])))
        self.wait(1)

        rules = VGroup(
            T("1.  Each step: one dot right, or one dot up.", 26),
            T("2.  Each walks to its own house.", 26),
            T("3.  Never stand on the same dot.", 26, t2c={"Never": YELLOW}),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(RIGHT, buff=0.4).shift(UP * 1.2)

        # rule 1, shown
        self.play(FadeIn(rules[0], shift=LEFT * 0.2))
        o = lat.p(1, 2)
        ok = VGroup(Arrow(o, lat.p(2, 2), buff=0.1, color=GOOD), Arrow(o, lat.p(1, 3), buff=0.1, color=GOOD))
        no = VGroup(Arrow(o, lat.p(0, 2), buff=0.1, color=BAD), Arrow(o, lat.p(1, 1), buff=0.1, color=BAD))
        xs = VGroup(*[cross(0.3).move_to(a.get_center()) for a in no])
        self.play(GrowArrow(ok[0]), GrowArrow(ok[1]))
        self.play(GrowArrow(no[0]), GrowArrow(no[1]), FadeIn(xs))
        self.wait(1.5)
        self.play(FadeOut(ok), FadeOut(no), FadeOut(xs))

        # rule 2, shown
        self.play(FadeIn(rules[1], shift=LEFT * 0.2))
        d1 = DashedLine(lat.p(*A1), lat.p(*B1), color=ANT1, dash_length=0.12).add_tip(tip_length=0.2)
        d2 = DashedLine(lat.p(*A2), lat.p(*B2), color=ANT2, dash_length=0.12).add_tip(tip_length=0.2)
        self.play(Create(d1), Create(d2), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(d1), FadeOut(d2))

        # rule 3, shown: the near miss
        self.play(FadeIn(rules[2], shift=LEFT * 0.2))
        spot = lat.p(1, 1)
        self.play(L.animate.move_to(spot + LEFT * 0.3), N.animate.move_to(spot + RIGHT * 0.3), run_time=0.9)
        ring = Circle(radius=0.55, color=MEET, stroke_width=5).move_to(spot)
        b1, b2 = speech("!", L, UP + LEFT * 0.3, size=34), speech("!", N, UP + RIGHT * 0.3, size=34)
        self.sfx("alert")
        self.play(Create(ring), FadeIn(b1, scale=1.4), FadeIn(b2, scale=1.4), run_time=0.5)
        self.wait(1.5)
        self.play(L.animate.move_to(lat.p(*A1)), N.animate.move_to(lat.p(*A2)),
                  FadeOut(ring), FadeOut(b1), FadeOut(b2), run_time=0.9)

        # crossing = sharing a dot
        note = T("On a grid, routes can only cross at a dot,\nso \"never meet\" also means \"never cross\".",
                 22, SOFT, line_spacing=1.15).next_to(rules, DOWN, buff=0.7, aligned_edge=LEFT)
        self.play(FadeIn(note))
        self.wait(2.5)

        q = T("How many ways can both get home\nwithout ever meeting?", 32, YELLOW, line_spacing=1.15) \
            .next_to(rules, DOWN, buff=1.0, aligned_edge=LEFT)
        self.play(FadeOut(note), Write(q))
        self.wait(3)
