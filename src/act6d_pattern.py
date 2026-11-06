"""v13 — "Does the pattern repeat?": the disguises, in Priyanshu's style (one at a time).

    PatternCard   bridge line + the card "Does the pattern repeat?"
    Hexagon       triangles -> tiles -> a tiling (looks like boxes) -> how many? -> fade the flat tiles ->
                  two chains that never touch -> squashed onto our grid they are our two ants -> 20
Reuses the verified tiling geometry of act6_hexagon.py (20 tilings <-> the 20 non-touching ant pairs).
"""
from common import *
from act6_hexagon import (PARTITIONS, SHOW, TOP_C, X_C, Y_C, proj, tiling, triangles, outline, chain,
                          walker_path)


class PatternCard(DScene):
    def construct(self):
        t = T("Does the pattern repeat?", 54, weight=BOLD)
        # 0: so any puzzle that is secretly non-touching paths, a determinant can count
        self.cue(0)
        recap = VGroup(T("det", 40), T("=", 40), T("number of families that never touch", 34, YELLOW)).arrange(RIGHT, buff=0.25)
        self.play(FadeIn(recap, shift=UP * 0.2), run_time=1.0)
        # 1: does the pattern repeat?
        self.cue(1)
        self.cue_at(1, "Does the pattern", lead=0.2)
        self.sfx("whoosh")
        self.play(FadeOut(recap, shift=UP * 0.3), run_time=0.5)
        self.play(Write(t), run_time=1.2)
        self.cue_end(1)
        self.wait(0.5)
        self.play(FadeOut(t), run_time=0.6)


class Hexagon(DScene):
    def construct(self):
        c, s = LEFT * 3.4 + DOWN * 0.3, 1.35
        hexo = outline(s, c)
        tris = triangles(s, c, color=GREY_C)

        # 0: a hexagon, cut into little triangles
        self.cue(0)
        self.play(Create(hexo), run_time=1.0)
        self.play(LaggedStartMap(Create, tris, lag_ratio=0.02), run_time=1.5)

        # 1: glue two neighbours: a tile; tiles point three ways
        self.cue(1)
        demo = tiling(SHOW, s, c)[0]
        dp = demo.get_vertices()
        if np.linalg.norm(dp[0] - dp[2]) < np.linalg.norm(dp[1] - dp[3]):
            t1, t2 = Polygon(dp[0], dp[1], dp[2]), Polygon(dp[0], dp[2], dp[3])
        else:
            t1, t2 = Polygon(dp[1], dp[2], dp[3]), Polygon(dp[1], dp[3], dp[0])
        for t in (t1, t2):
            t.set_fill(YELLOW, 0.55).set_stroke(YELLOW, 3)
        self.cue_at(1, "Glue", lead=0.2)
        self.play(FadeIn(t1), run_time=0.4)
        self.play(FadeIn(t2), run_time=0.4)
        glued = demo.copy().set_fill(YELLOW, 0.8).set_stroke(YELLOW, 3)
        self.sfx("pop")
        self.play(FadeOut(t1), FadeOut(t2), FadeIn(glued), run_time=0.7)
        kinds = VGroup(*[Polygon(*[proj(*q, 0.75, ORIGIN) for q in cs], fill_color=col, fill_opacity=1,
                                 stroke_color=BLACK, stroke_width=2)
                         for cs, col in [([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], TOP_C),
                                         ([(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)], X_C),
                                         ([(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)], Y_C)]])
        kinds.arrange(RIGHT, buff=0.8).move_to(RIGHT * 3.4 + UP * 0.4)
        self.cue_at(1, "three directions", lead=0.2)
        self.play(LaggedStart(*[FadeIn(k, scale=0.6) for k in kinds], lag_ratio=0.35), run_time=1.2)

        # 2: cover it; it looks like a stack of boxes
        self.cue(2)
        til = tiling(SHOW, s, c)
        self.play(FadeOut(glued), FadeOut(kinds), run_time=0.4)
        self.sfx("whoosh")
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.4) for t in til], lag_ratio=0.12), run_time=2.6)
        self.remove(tris)

        # 3: it's flat; your brain does the 3D for free
        self.cue(3)
        orig = til.copy()
        flat = til.copy()
        for t in flat:
            t.set_fill(GREY_C, 1).set_stroke(WHITE, 2)
        self.cue_at(3, "flat", lead=0.2)
        self.play(Transform(til, flat), run_time=0.8)
        self.wait(0.5)
        self.cue_at(3, "Your brain", lead=0.2)
        self.play(Transform(til, orig), run_time=0.8)

        # 4: how many ways? (a few other tilings flicker by)
        self.cue(4)
        q = T("?", 90, YELLOW, weight=BOLD).move_to(RIGHT * 3.4 + UP * 0.3)
        self.play(FadeIn(q, scale=1.4), run_time=0.5)
        for h in [PARTITIONS[i] for i in (7, 16, 19)] + [SHOW]:
            self.play(Transform(til, tiling(h, s, c)), run_time=0.7)
            self.wait(0.25)

        # 5: fade out the flat tiles; the others link into chains
        self.cue(5)
        tops = VGroup(*[t for t in til if t.kind == "T"])
        self.cue_at(5, "Fade out", lead=0.2)
        self.play(tops.animate.set_fill(opacity=0).set_stroke(GREY_B, 1.5), FadeOut(q), run_time=1.2)
        ch = [chain(SHOW, 1, s, c, ANT1), chain(SHOW, 0, s, c, ANT2)]
        self.cue_at(5, "chains", lead=0.2)
        self.play(Create(ch[0]), run_time=1.5)
        self.play(Create(ch[1]), run_time=1.5)

        # 6: tiles never overlap, so the chains never touch
        self.cue(6)
        self.play(Indicate(VGroup(*ch), color=YELLOW, scale_factor=1.04), run_time=1.0)

        # 7: squash it onto our grid: the two chains are our two ants
        self.cue(7)
        lat = Lattice(4, spacing=1.0, center=RIGHT * 3.4 + DOWN * 0.35)
        bd = VGroup(Dot(lat.p(*A1), radius=0.1, color=ANT1), Dot(lat.p(*A2), radius=0.1, color=ANT2),
                    house(ANT1, 0.45).move_to(lat.p(*B1)), house(ANT2, 0.45).move_to(lat.p(*B2)))
        self.play(FadeIn(lat), FadeIn(bd), run_time=0.8)
        tg = [path_mob(lat, walker_path(SHOW, 1), ANT1, 8), path_mob(lat, walker_path(SHOW, 0), ANT2, 8)]
        self.cue_at(7, "squash", lead=0.2)
        self.sfx("whoosh")
        self.play(*[ReplacementTransform(ch[k].copy(), tg[k]) for k in range(2)], run_time=2.2)
        a1 = ant(ANT1, 0.65).move_to(lat.p(*A1))
        a2 = ant(ANT2, 0.65).move_to(lat.p(*A2))
        self.cue_at(7, "our two ants", lead=0.2)
        self.sfx("pop")
        self.play(FadeIn(a1, scale=0.4), FadeIn(a2, scale=0.4), run_time=0.6)
        # a few more tilings: chains and ant paths change together
        for h in [PARTITIONS[i] for i in (2, 9, 15)] + [SHOW]:
            nt = tiling(h, s, c)
            for t in nt:
                if t.kind == "T":
                    t.set_fill(opacity=0).set_stroke(GREY_B, 1.5)
            nc = [chain(h, 1, s, c, ANT1), chain(h, 0, s, c, ANT2)]
            npth = [path_mob(lat, walker_path(h, 1), ANT1, 8), path_mob(lat, walker_path(h, 0), ANT2, 8)]
            self.play(Transform(til, nt), *[Transform(ch[k], nc[k]) for k in range(2)],
                      *[Transform(tg[k], npth[k]) for k in range(2)], run_time=1.0)
            self.wait(0.35)

        # 8: so there are twenty tilings — our ants were tiling a hexagon all along
        self.cue(8)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.6)
        minis = VGroup(*[VGroup(outline(0.26), tiling(h, 0.26, stroke=0.8)) for h in PARTITIONS])
        minis.arrange_in_grid(4, 5, buff=(0.4, 0.3)).scale_to_fit_height(5.0).move_to(LEFT * 1.4 + DOWN * 0.1)
        self.play(LaggedStartMap(FadeIn, minis, lag_ratio=0.05), run_time=2.4)
        twenty = T(str(len(PARTITIONS)), 110, YELLOW, weight=BOLD).next_to(minis, RIGHT, buff=0.7)
        self.sfx("chime")
        self.play(FadeIn(twenty, scale=1.5), run_time=0.6)
        self.cue_end(8)
        self.wait(0.6)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.6)
