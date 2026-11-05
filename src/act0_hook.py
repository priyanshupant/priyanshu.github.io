"""Act 0 — The hook (replaces Montage + ColdOpen + Problem).

    Hook   two ants, their rules inside the story, one question, the determinant
           flash, a quick animated montage of where determinants live, title card.
Narration lines (narration.py "Hook"): 0 ants & moves, 1 homes, 2 the fight,
3 crossing = sharing, 4 the question, 5 a determinant, 6 that determinant
(montage), 7 it can count (title).
"""
from common import *

GRID_HOOK = LEFT * 3.2 + DOWN * 0.2


class Hook(DScene):
    """v6: the puzzle. Lines: 0 ants on a grid, 1 moves, 2 homes, 3 fight + scent trail,
    4 can't touch + question, 5 pause and try."""

    def construct(self):
        lat = Lattice(4, spacing=1.45, center=GRID_HOOK)
        ends = endpoints(lat, scale=1.15)
        a1 = ant(ANT1, 0.9).move_to(lat.p(*A1))
        a2 = ant(ANT2, 0.9).move_to(lat.p(*A2))

        # 0: two ants on a grid (already on screen: the Opening ends on this exact picture)
        self.add(lat, a1, a2)
        self.cue(0)
        self.cue_at(0, "Meet two", lead=0.2)
        self.play(a1.animate.scale(1.25), a2.animate.scale(1.25), rate_func=there_and_back, run_time=0.6)
        self.cue_at(0, "They live")
        self.play(LaggedStartMap(Indicate, lat, lag_ratio=0.02, color=YELLOW, scale_factor=1.6), run_time=1.0)

        # 1: right or up, drawn from the ant; never left, never down
        self.cue(1)
        o = lat.p(*A1)
        ok = VGroup(Arrow(o, lat.p(1, 1), buff=0.35, color=GOOD, stroke_width=8),
                    Arrow(o, lat.p(0, 2), buff=0.35, color=GOOD, stroke_width=8))
        no = VGroup(Arrow(o, lat.p(-0.8, 1), buff=0.35, color=BAD, stroke_width=8),
                    Arrow(o, lat.p(0, 0), buff=0.35, color=BAD, stroke_width=8))
        xs = VGroup(*[cross(0.36).move_to(a.get_center()) for a in no])
        self.cue_at(1, "right")
        self.play(GrowArrow(ok[0]), run_time=0.5)
        self.cue_at(1, "up.")
        self.play(GrowArrow(ok[1]), run_time=0.5)
        self.cue_at(1, "Never left")
        self.play(GrowArrow(no[0]), FadeIn(xs[0]), a1.animate.shift(LEFT * 0.35), run_time=0.4)
        self.play(a1.animate.shift(RIGHT * 0.35), run_time=0.3, rate_func=rush_from)
        self.cue_at(1, "never down")
        self.play(GrowArrow(no[1]), FadeIn(xs[1]), run_time=0.5)
        self.cue_end(1)
        self.play(FadeOut(ok), FadeOut(no), FadeOut(xs), run_time=0.4)

        # 2: homes, on "here" and "there"
        self.cue(2)
        h1 = CurvedArrow(lat.p(*A1) + UP * 0.35, lat.p(*B1) + LEFT * 0.4, angle=-PI / 3, color=ANT1)
        h2 = CurvedArrow(lat.p(*A2) + RIGHT * 0.45, lat.p(*B2) + DOWN * 0.4, angle=PI / 3, color=ANT2)
        n1 = T("ant 1", 30, ANT1).next_to(a1, DOWN, buff=0.35)
        n2 = T("ant 2", 30, ANT2).next_to(a2, RIGHT, buff=0.35)
        self.play(FadeIn(n1), Indicate(a1, color=ANT1), run_time=0.6)
        self.cue_at(2, "lives here", lead=0.2)
        self.play(FadeIn(VGroup(ends[4], ends[5]), shift=DOWN * 0.3), FadeIn(VGroup(ends[0], ends[1])), Create(h1), run_time=0.9)
        self.cue_at(2, "The orange")
        self.play(FadeIn(n2), Indicate(a2, color=ANT2), run_time=0.6)
        self.cue_at(2, "lives there", lead=0.2)
        self.play(FadeIn(VGroup(ends[6], ends[7]), shift=DOWN * 0.3), FadeIn(VGroup(ends[2], ends[3])), Create(h2), run_time=0.9)
        self.cue_end(2)
        self.play(FadeOut(h1), FadeOut(h2), FadeOut(n1), FadeOut(n2), run_time=0.4)

        # 3: the fight; the scent trail
        self.cue(3)
        fight = T("They had a fight.", 44).move_to(RIGHT * 3.4 + UP * 2.6)
        self.cue_at(3, "They had")
        self.play(Write(fight), run_time=0.8)
        P = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
        self.cue_at(3, "Now neither")
        anims, tr = walk_steps(lat, [(a1, P, ANT1)], step_time=0.4)
        for an in anims:
            self.play(an)
        glow = VGroup(*[path_mob(lat, P, ANT1, w).set_stroke(opacity=op) for w, op in [(30, 0.10), (18, 0.2)]])
        rule = VGroup(T("Neither steps on any dot", 30), T("the other one walks on.", 30)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(fight, DOWN, buff=0.45)
        self.play(FadeIn(glow), FadeIn(rule), run_time=0.6)
        self.cue_at(3, "Not even later")
        Q = [(1, 0), (1, 1)]
        anims2, tr2 = walk_steps(lat, [(a2, Q, ANT2)], step_time=0.45)
        for an in anims2:
            self.play(an)
        self.play(a2.animate.move_to(lat.p(1, 1.55)), run_time=0.4)
        bang = speech("!", a2, RIGHT, color=BAD, size=48)
        bang[1].set_color(BAD)
        ring = Circle(radius=0.4, color=MEET, stroke_width=6).move_to(lat.p(1, 2))
        self.sfx("alert")
        self.play(FadeIn(bang, scale=1.5), Create(ring), run_time=0.4)
        scent = T("ants leave a scent trail", 28, SOFT).next_to(rule, DOWN, buff=0.3).align_to(rule, LEFT)
        self.cue_at(3, "ants leave", lead=0.2)
        self.play(FadeIn(scent), glow.animate.set_stroke(opacity=0.35), run_time=0.5)
        self.play(a2.animate.move_to(lat.p(*A2)), FadeOut(bang), FadeOut(VGroup(*tr2)), run_time=0.7, rate_func=rush_from)
        self.cue_end(3)
        self.play(FadeOut(VGroup(glow, ring, *tr)), a1.animate.move_to(lat.p(*A1)), run_time=0.6)

        # 4: so the routes can't touch; the question
        self.cue(4)
        r1 = path_mob(lat, [(0, 1), (1, 1), (2, 1), (2, 2), (2, 3)], ANT1, 7)
        r2 = path_mob(lat, [(1, 0), (1, 1), (1, 2), (2, 2), (3, 2)], ANT2, 7)
        self.play(Create(r1), Create(r2), run_time=1.0)
        xdots = VGroup(*[Circle(radius=0.3, color=MEET, stroke_width=6).move_to(lat.p(*p)) for p in [(1, 1), (2, 2)]])
        no2 = cross(0.6).move_to(lat.p(3, 0.0))
        self.cue_at(4, "can't touch", lead=0.2)
        self.sfx("buzz")
        self.play(Create(xdots), FadeIn(no2), run_time=0.6)
        q = T("How many pairs of routes\nget both ants home?", 38, YELLOW, line_spacing=1.2).move_to(RIGHT * 3.4 + DOWN * 0.6)
        self.cue_at(4, "How many", lead=0.2)
        self.play(FadeOut(VGroup(r1, r2, xdots, no2)), FadeOut(rule), FadeOut(scent), Write(q), run_time=1.2)

        # 5: pause and try
        self.cue(5)
        tr_ = T("(pause and try to find one)", 28, SOFT).next_to(q, DOWN, buff=0.4)
        self.play(FadeIn(tr_), run_time=0.6)
        self.cue_end(5)
        self.wait(1.6)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.6)
