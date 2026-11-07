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
        for an, word in ((a1, "hi!"), (a2, "yo!")):
            hi = speech(word, an, UP, size=40).shift(UP * 0.1)
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
        self.sfx("pop")
        self.play(FadeIn(h1, scale=1.5), Create(g1), run_time=0.8)
        self.sfx("pop")
        self.play(FadeIn(h2, scale=1.5), Create(g2), run_time=0.8)
        self.play(Indicate(h1, color=ANT1, scale_factor=1.3), Indicate(h2, color=ANT2, scale_factor=1.3), run_time=0.6)
        self.play(FadeOut(g1), FadeOut(g2), run_time=0.4)

        # rules, as bullets on the right; they appear as they are said
        bul1 = T("•  step up or right", 32)
        bul2 = T("•  paths never touch", 32)
        bullets = VGroup(bul1, bul2).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 3.1 + UP * 2.55)

        # 3: rules — up and right are fine; down and left are not
        self.cue(3)
        o = lat.p(*A1)
        self.cue_at(3, "step up", lead=0.2)
        self.play(self.face(a1, PI / 2), FadeIn(bul1, shift=LEFT * 0.2))
        self.play(a1.animate.move_to(lat.p(0, 2)), run_time=0.4)
        ok1 = tick(0.35, YELLOW).next_to(a1, LEFT, buff=0.15)
        self.play(FadeIn(ok1), run_time=0.2)
        self.cue_at(3, "to the right", lead=0.2)
        self.play(self.face(a1, 0))
        self.play(a1.animate.move_to(lat.p(1, 2)), run_time=0.4)
        ok2 = tick(0.35, YELLOW).next_to(a1, UP, buff=0.1)
        self.play(FadeIn(ok2), run_time=0.2)
        self.play(FadeOut(ok1), FadeOut(ok2), run_time=0.3)
        here = lat.p(1, 2)                                   # try down / left from where it got to
        self.cue_at(3, "Never down", lead=0.2)
        self.play(self.face(a1, -PI / 2))
        x1 = cross(0.36).move_to(lat.p(1, 1.45))
        self.sfx("buzz")
        self.play(a1.animate.shift(DOWN * 0.4), FadeIn(x1), run_time=0.3)
        self.play(a1.animate.move_to(here), run_time=0.3, rate_func=rush_from)
        self.cue_at(3, "never left", lead=0.2)
        self.play(self.face(a1, PI))
        x2 = cross(0.36).move_to(lat.p(0.45, 2))
        self.sfx("buzz")
        self.play(a1.animate.shift(LEFT * 0.4), FadeIn(x2), run_time=0.3)
        self.play(a1.animate.move_to(here), run_time=0.3, rate_func=rush_from)
        self.cue_end(3)
        self.play(FadeOut(x1), FadeOut(x2), run_time=0.3)
        self.play(self.face(a1, 0))                            # turn first, then walk back
        self.play(a1.animate.move_to(o), run_time=0.6)        # (rotate + .animate in one play loses the turn)

        # 4: many paths home — several each, and some of them cross
        self.cue(4)
        blue = [[(0, 1), (0, 2), (0, 3), (1, 3), (2, 3)], [(0, 1), (1, 1), (2, 1), (2, 2), (2, 3)]]
        orng = [[(1, 0), (2, 0), (3, 0), (3, 1), (3, 2)], [(1, 0), (1, 1), (1, 2), (2, 2), (3, 2)]]
        # each ant's two paths share no segment; a blue and an orange path cross at (1,1) and (2,2)
        bm = [path_mob(lat, P, ANT1, 6).set_stroke(opacity=0.85) for P in blue]
        om = [path_mob(lat, P, ANT2, 6).set_stroke(opacity=0.85) for P in orng]
        for mob, word in [(bm[0], "could go this way"), (bm[1], "or this way"), (om[0], "orange ant"), (om[1], "or that way")]:
            self.cue_at(4, word, lead=0.2)
            self.sfx("tick")
            self.play(Create(mob), run_time=0.8)
        crossings = VGroup(*[Circle(radius=0.28, color=MEET, stroke_width=5).move_to(lat.p(*p)) for p in [(1, 1), (2, 2)]])
        self.play(Create(crossings), run_time=0.6)
        self.cue_end(4)
        self.play(FadeOut(VGroup(*bm, *om, crossings)), run_time=0.4)

        # 5: the fight — if they meet, they fight
        self.cue(5)
        self.cue_at(5, "if they meet", lead=0.2)
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
        self.sfx("rumble")
        self.play(FadeIn(cloud, scale=0.3), FadeIn(cuss, scale=0.3), FadeOut(a1), FadeOut(a2), run_time=0.35)
        self.play(Wiggle(VGroup(cloud, cuss), scale_value=1.15, rotation_angle=0.08 * TAU), FadeIn(stars, lag_ratio=0.2), run_time=1.2)
        a1.move_to(lat.p(*A1)); a2.move_to(lat.p(*A2))
        self.play(FadeOut(VGroup(cloud, cuss, stars)), FadeIn(a1), FadeIn(a2), FadeIn(bul2, shift=LEFT * 0.2), run_time=0.5)
        self.play(self.face(a2, 0))

        # 6: neither steps on a dot the other walks on, not even later (said, not written)
        self.cue(6)
        P = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
        anims, tr = walk_steps(lat, [(a1, P, ANT1)], step_time=0.35)
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
        self.cue_at(6, "scent trail", lead=0.3)
        self.play(glow_.animate.set_stroke(opacity=0.35), run_time=0.4)
        self.play(a2.animate.move_to(lat.p(*A2)), FadeOut(bang), FadeOut(VGroup(*tr2)), run_time=0.7, rate_func=rush_from)
        self.cue_end(6)
        self.play(FadeOut(VGroup(glow_, ring, *tr)), a1.animate.move_to(lat.p(*A1)), run_time=0.6)
        self.play(self.face(a1, 0), self.face(a2, 0))

        # 7: the question
        self.cue(7)
        q = T("How many pairs of paths\nget them home\nwithout intersecting?", 34, YELLOW, line_spacing=1.2).move_to(RIGHT * 3.1 + UP * 0.55)
        self.cue_at(7, "how many", lead=0.2)
        self.play(Write(q), run_time=1.2)

        # 8: one is easy to find; 9: here's one where they cross
        self.cue(8)
        gp = VGroup(path_mob(lat, blue[0], ANT1, 7), path_mob(lat, orng[0], ANT2, 7))
        self.cue_at(8, "the blue one", lead=0.2)
        self.play(Create(gp[0]), run_time=0.7)
        self.cue_at(8, "the orange one", lead=0.2)
        self.play(Create(gp[1]), run_time=0.7)
        self.cue_at(8, "never meet", lead=0.2)
        okp = tick(0.6, GOOD).move_to(lat.p(3.0, 3.0) + RIGHT * 0.2)
        self.sfx("chime")
        self.play(FadeIn(okp, scale=1.4), run_time=0.4)
        self.cue(9)
        bp = VGroup(path_mob(lat, blue[1], ANT1, 7), path_mob(lat, orng[1], ANT2, 7))
        self.play(FadeOut(gp), FadeOut(okp), run_time=0.3)
        self.play(Create(bp[0]), Create(bp[1]), run_time=0.9)
        mring = Circle(radius=0.32, color=MEET, stroke_width=6).move_to(lat.p(1, 1))
        nop = cross(0.5).move_to(lat.p(3.0, 3.0) + RIGHT * 0.2)
        self.sfx("buzz")
        self.play(Create(mring), FadeIn(nop), run_time=0.5)
        self.cue_end(9)
        self.wait(1.0)                                   # let the crossing pair sit
        self.play(FadeOut(VGroup(bp, mring, nop)), run_time=0.3)

        # 10: check them all, one by one — fast; counters climb to 20 and 16
        self.cue(10)
        labg, labb = T("never meet:", 32, GOOD), T("meet:", 32, BAD)
        VGroup(labg, labb).arrange(DOWN, aligned_edge=RIGHT, buff=0.3).move_to(RIGHT * 2.6 + DOWN * 1.6)
        cg, cb = T("0", 40, GOOD).next_to(labg, RIGHT, buff=0.3), T("0", 40, BAD).next_to(labb, RIGHT, buff=0.3)
        self.play(FadeIn(VGroup(labg, labb, cg, cb)), run_time=0.4)
        ng = nb = 0
        words = ["This pair works", "This one doesn't", "Neither does this", "Or this one"]
        for k, (Pp, Qq) in enumerate(plus_pairs()):
            m = first_meet(Pp, Qq)
            pair = VGroup(path_mob(lat, Pp, ANT1, 6), path_mob(lat, Qq, ANT2, 6))
            if m is None:
                ng += 1; mark = VGroup()
            else:
                nb += 1; mark = Circle(radius=0.28, color=MEET, stroke_width=5).move_to(lat.p(*m))
            cg2 = T(str(ng), 40, GOOD).move_to(cg, aligned_edge=LEFT)
            cb2 = T(str(nb), 40, BAD).move_to(cb, aligned_edge=LEFT)
            if k < len(words):                                  # the first few, slowly, as they are named
                self.cue_at(10, words[k], lead=0.15)
                self.play(Create(pair), run_time=0.6)
                self.sfx("tick" if m is None else "buzz")
                self.play(Create(mark) if m is not None else Wait(0.01), Transform(cg, cg2), Transform(cb, cb2), run_time=0.4)
                self.wait(0.3)
                self.play(FadeOut(pair), FadeOut(mark), run_time=0.25)
            else:                                               # "and so on": speeding up
                dt = max(0.12, 0.4 * 0.88 ** (k - len(words)))
                self.add(pair, mark)
                self.play(Transform(cg, cg2), Transform(cb, cb2), run_time=dt)
                self.remove(pair, mark)
        assert (ng, nb) == (20, 16)

        # 11: twenty never meet, sixteen do
        self.cue(11)
        self.sfx("chime")
        self.play(Indicate(VGroup(labg, cg), color=GOOD, scale_factor=1.15), run_time=0.8)
        self.cue_at(11, "sixteen", lead=0.2)
        self.play(Indicate(VGroup(labb, cb), color=BAD, scale_factor=1.15), run_time=0.8)
        self.cue_end(11)
        self.wait(0.6)
        # erase only the right-hand side; the grid, ants and houses stay for the matrix
        self.play(FadeOut(VGroup(bullets, q, labg, labb, cg, cb)), run_time=0.6)
