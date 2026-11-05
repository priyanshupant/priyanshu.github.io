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
    """v10 puzzle. Lines: 0 meet the ants (hi!), 1 grid world, 2 homes, 3 rules (up/right only),
    4 many ways home, 5 the fight (if they meet, they fight), 6 scent trail rule,
    7 can't touch + question, 8 pause and try.  No A/B labels: colours and symbols only."""

    def face(self, a, target, run_time=0.15):
        delta = (target - a.heading + PI) % TAU - PI
        a.heading = target
        return Rotate(a, delta, about_point=a.get_center(), run_time=run_time)

    def construct(self):
        lat = Lattice(4, spacing=1.45, center=GRID_HOOK)
        a1 = ant(ANT1, 0.9).move_to(lat.p(*A1))
        a2 = ant(ANT2, 0.9).move_to(lat.p(*A2))
        starts = VGroup(Dot(lat.p(*A1), radius=0.12, color=ANT1), Dot(lat.p(*A2), radius=0.12, color=ANT2))
        h1 = house(ANT1, 0.6).move_to(lat.p(*B1))
        h2 = house(ANT2, 0.6).move_to(lat.p(*B2))

        # 0: meet these two ants — they say hi
        self.cue(0)
        self.play(FadeIn(a1, scale=0.5), FadeIn(a2, scale=0.5), run_time=0.6)
        for an in (a1, a2):
            hi = speech("hi!", an, UP, size=40).shift(UP * 0.1)
            self.sfx("pop")
            self.play(an.animate.shift(UP * 0.25), rate_func=there_and_back, run_time=0.4)
            self.play(FadeIn(hi, scale=0.6), run_time=0.25)
            an.hi = hi
        self.wait(0.5)
        self.play(FadeOut(a1.hi), FadeOut(a2.hi), run_time=0.3)

        # 1: a grid-like world
        self.cue(1)
        self.cue_at(1, "grid", lead=0.3)
        self.play(LaggedStartMap(FadeIn, lat, lag_ratio=0.03), FadeIn(starts), run_time=1.0)
        self.bring_to_front(a1, a2)

        # 2: they want to get home — the houses, in their colours
        self.cue(2)
        self.cue_at(2, "home", lead=0.3)
        g1 = CurvedArrow(lat.p(*A1) + UP * 0.35, lat.p(*B1) + LEFT * 0.4, angle=-PI / 3, color=ANT1)
        g2 = CurvedArrow(lat.p(*A2) + RIGHT * 0.45, lat.p(*B2) + DOWN * 0.4, angle=PI / 3, color=ANT2)
        self.play(FadeIn(h1, scale=1.5), Create(g1), run_time=0.7)
        self.play(FadeIn(h2, scale=1.5), Create(g2), run_time=0.7)
        self.play(Indicate(h1, color=ANT1, scale_factor=1.3), Indicate(h2, color=ANT2, scale_factor=1.3), run_time=0.6)
        self.play(FadeOut(g1), FadeOut(g2), run_time=0.4)

        # 3: rules — up and right are fine; down and left are not
        self.cue(3)
        o = lat.p(*A1)
        self.cue_at(3, "step up", lead=0.2)
        self.play(self.face(a1, PI / 2))
        self.play(a1.animate.move_to(lat.p(0, 2)), run_time=0.4)
        ok1 = tick(0.35, YELLOW).next_to(a1, LEFT, buff=0.15)
        self.play(FadeIn(ok1), run_time=0.2)
        self.cue_at(3, "to the right", lead=0.2)
        self.play(self.face(a1, 0))
        self.play(a1.animate.move_to(lat.p(1, 2)), run_time=0.4)
        ok2 = tick(0.35, YELLOW).next_to(a1, UP, buff=0.1)
        self.play(FadeIn(ok2), run_time=0.2)
        self.play(FadeOut(ok1), FadeOut(ok2), a1.animate.move_to(o), run_time=0.5)
        self.cue_at(3, "Never down", lead=0.2)
        self.play(self.face(a1, -PI / 2))
        x1 = cross(0.36).move_to(lat.p(0, 0.45))
        self.sfx("buzz")
        self.play(a1.animate.shift(DOWN * 0.4), FadeIn(x1), run_time=0.25)
        self.play(a1.animate.move_to(o), run_time=0.25, rate_func=rush_from)
        self.cue_at(3, "never left", lead=0.2)
        self.play(self.face(a1, PI))
        x2 = cross(0.36).move_to(o + LEFT * 0.75)
        self.sfx("buzz")
        self.play(a1.animate.shift(LEFT * 0.4), FadeIn(x2), run_time=0.25)
        self.play(a1.animate.move_to(o), run_time=0.25, rate_func=rush_from)
        self.play(self.face(a1, 0), FadeOut(x1), FadeOut(x2), run_time=0.3)

        # 4: many ways home — two for blue, one for orange
        self.cue(4)
        bA = [(0, 1), (0, 2), (0, 3), (1, 3), (2, 3)]
        bB = [(0, 1), (1, 1), (2, 1), (2, 2), (2, 3)]
        oA = [(1, 0), (2, 0), (3, 0), (3, 1), (3, 2)]
        rA, rB, rO = path_mob(lat, bA, ANT1, 7), path_mob(lat, bB, ANT1, 7), path_mob(lat, oA, ANT2, 7)
        self.cue_at(4, "could go this way", lead=0.2)
        self.play(Create(rA), run_time=0.8)
        self.cue_at(4, "or this way", lead=0.2)
        self.play(rA.animate.set_stroke(opacity=0.25), Create(rB), run_time=0.8)
        self.cue_at(4, "orange ant", lead=0.2)
        self.play(rB.animate.set_stroke(opacity=0.25), Create(rO), run_time=0.8)
        self.cue_end(4)
        self.play(FadeOut(VGroup(rA, rB, rO)), run_time=0.4)

        # 5: the fight — if they meet, they fight
        self.cue(5)
        self.cue_at(5, "if they meet", lead=0.2)
        meetP = [(0, 1), (1, 1)]
        meetQ = [(1, 0), (1, 1)]
        self.play(self.face(a1, 0), self.face(a2, PI / 2))
        self.play(a1.animate.move_to(lat.p(1, 1) + LEFT * 0.38), a2.animate.move_to(lat.p(1, 1) + DOWN * 0.38), run_time=0.6)
        self.cue_at(5, "fighting", lead=0.2)
        c0 = lat.p(1, 1)
        cloud = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=GREY_C, fill_opacity=1)
                         .move_to(c0 + np.array([dx, dy, 0]))
                         for r, dx, dy in [(0.62, 0, 0), (0.42, 0.62, 0.22), (0.42, -0.6, 0.18), (0.4, 0.1, 0.58),
                                           (0.38, 0.2, -0.5), (0.36, -0.42, -0.4), (0.34, 0.6, -0.3)]])
        limbs = VGroup(*[Line(c0 + 0.7 * np.array([np.cos(t), np.sin(t), 0]), c0 + 1.05 * np.array([np.cos(t), np.sin(t), 0]),
                              color=(ANT1 if k % 2 else ANT2), stroke_width=6) for k, t in enumerate([0.3, 1.4, 2.6, 3.7, 4.6, 5.6])])
        cuss = T("#@%!", 44, BAD, weight=BOLD).move_to(c0)
        stars = VGroup(*[Star(n=5, outer_radius=0.17, color=YELLOW, fill_opacity=1).move_to(c0 + 1.25 * np.array([np.cos(t), np.sin(t), 0]))
                         for t in np.linspace(0.4, TAU + 0.4, 5, endpoint=False)])
        cloud = VGroup(limbs, cloud)
        self.sfx("alert")
        self.play(FadeIn(cloud, scale=0.3), FadeIn(cuss, scale=0.3), FadeOut(a1), FadeOut(a2), run_time=0.35)
        self.play(Wiggle(VGroup(cloud, cuss), scale_value=1.15, rotation_angle=0.08 * TAU), FadeIn(stars, lag_ratio=0.2), run_time=1.2)
        a1.move_to(lat.p(*A1)); a2.move_to(lat.p(*A2))
        self.play(FadeOut(VGroup(cloud, cuss, stars)), FadeIn(a1), FadeIn(a2), run_time=0.5)
        self.play(self.face(a2, 0))

        # 6: so neither steps on any dot the other walks on; not even later (scent trail)
        self.cue(6)
        rule = VGroup(T("Neither steps on any dot", 30), T("the other one walks on.", 30)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(RIGHT * 3.3 + UP * 2.3)
        P = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
        anims, tr = walk_steps(lat, [(a1, P, ANT1)], step_time=0.35)
        self.play(FadeIn(rule), run_time=0.5)
        for an in anims:
            self.play(an)
        glow_ = VGroup(*[path_mob(lat, P, ANT1, w).set_stroke(opacity=op) for w, op in [(30, 0.10), (18, 0.2)]])
        self.play(FadeIn(glow_), run_time=0.4)
        self.cue_at(6, "Not even later", lead=0.2)
        Q = [(1, 0), (1, 1)]
        anims2, tr2 = walk_steps(lat, [(a2, Q, ANT2)], step_time=0.4)
        for an in anims2:
            self.play(an)
        self.play(a2.animate.move_to(lat.p(1, 1.55)), run_time=0.4)
        bang = speech("!", a2, RIGHT, color=BAD, size=48)
        bang[1].set_color(BAD)
        ring = Circle(radius=0.4, color=MEET, stroke_width=6).move_to(lat.p(1, 2))
        self.sfx("alert")
        self.play(FadeIn(bang, scale=1.5), Create(ring), run_time=0.4)
        scent = T("ants leave a scent trail", 28, SOFT).next_to(rule, DOWN, buff=0.3).align_to(rule, LEFT)
        self.cue_at(6, "scent trail", lead=0.3)
        self.play(FadeIn(scent), glow_.animate.set_stroke(opacity=0.35), run_time=0.5)
        self.play(a2.animate.move_to(lat.p(*A2)), FadeOut(bang), FadeOut(VGroup(*tr2)), run_time=0.7, rate_func=rush_from)
        self.cue_end(6)
        self.play(FadeOut(VGroup(glow_, ring, *tr)), a1.animate.move_to(lat.p(*A1)), run_time=0.6)
        self.play(self.face(a1, 0), self.face(a2, 0))

        # 7: their routes can't touch; the question (rules stay up)
        self.cue(7)
        r1 = path_mob(lat, [(0, 1), (1, 1), (2, 1), (2, 2), (2, 3)], ANT1, 7)
        r2 = path_mob(lat, [(1, 0), (1, 1), (1, 2), (2, 2), (3, 2)], ANT2, 7)
        self.play(Create(r1), Create(r2), run_time=1.0)
        xdots = VGroup(*[Circle(radius=0.3, color=MEET, stroke_width=6).move_to(lat.p(*p)) for p in [(1, 1), (2, 2)]])
        no2 = cross(0.6).move_to(lat.p(3, 0.0))
        self.cue_at(7, "can't touch", lead=0.2)
        self.sfx("buzz")
        self.play(Create(xdots), FadeIn(no2), run_time=0.6)
        q = T("How many pairs of routes\nget both ants home\nwithout touching?", 36, YELLOW, line_spacing=1.2).move_to(RIGHT * 3.2 + UP * 0.6)
        rules = VGroup(T("→ or ↑ only", 28, SOFT), T("no shared dot", 28, SOFT)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        rules = VGroup(SurroundingRectangle(rules, color=DIM, buff=0.25, corner_radius=0.1), rules).move_to(RIGHT * 3.2 + DOWN * 2.6)
        self.cue_at(7, "how many", lead=0.2)
        self.play(FadeOut(VGroup(r1, r2, xdots, no2)), FadeOut(rule), FadeOut(scent), Write(q), run_time=1.2)
        self.play(FadeIn(rules, shift=UP * 0.15), run_time=0.5)

        # 8: pause and try
        self.cue(8)
        tr_ = T("(pause and try to find one)", 28, SOFT).next_to(q, DOWN, buff=0.35)
        self.play(FadeIn(tr_), run_time=0.6)
        self.cue_end(8)
        self.wait(1.6)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.6)
