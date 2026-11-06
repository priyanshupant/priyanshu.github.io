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


# ------------------------------------------------------------------ boxes in a corner (3 x 3 x 3 box)
from act6b_disguises import BOX3, PART3, box_walker
from math import comb

M3B = [[comb(6, 3 + z - zz) for zz in range(3)] for z in range(3)]        # rows/cols: blue, orange, purple
assert M3B == [[20, 15, 6], [15, 20, 15], [6, 15, 20]] and round(np.linalg.det(np.array(M3B, float))) == len(PART3) == 980


class Boxes(DScene):
    def construct(self):
        cols = [ANT1, ANT2, ANT3]
        c, s = LEFT * 3.6 + DOWN * 0.3, 0.85
        hexo = outline(s, c, BOX3)
        h = [[0] * 3 for _ in range(3)]
        til = tiling(tuple(map(tuple, h)), s, c, box=BOX3)

        # 0: a bigger box: three by three by three; stack the boxes in
        self.cue(0)
        self.play(Create(hexo), FadeIn(til), run_time=1.0)
        order = [(0, 0), (0, 1), (1, 0), (0, 0), (1, 1), (0, 2), (2, 0), (0, 1), (0, 0), (1, 0)]
        for k, (i, j) in enumerate(order):
            h[i][j] += 1
            if k % 2 == 0:
                self.sfx("tick")
            self.play(Transform(til, tiling(tuple(map(tuple, h)), s, c, box=BOX3)), run_time=0.4)
        H = tuple(map(tuple, h))

        # 1: now three chains, so three ants
        self.cue(1)
        for t in til:
            if t.kind == "T":
                t.set_fill(opacity=0).set_stroke(GREY_B, 1.2)
        self.play(Transform(til, til.copy()), run_time=0.8)
        chs = [chain(H, z, s, c, cols[2 - z], BOX3, width=7) for z in range(3)]
        for ch in reversed(chs):
            self.play(Create(ch), run_time=1.0)

        # 2: squash onto a grid: three ants that never touch
        self.cue(2)
        lat = Lattice(6, spacing=0.72, center=RIGHT * 3.4 + DOWN * 0.3)
        ends = VGroup(*[VGroup(Dot(lat.p(*box_walker(H, z)[0]), radius=0.09, color=cols[2 - z]),
                               house(cols[2 - z], 0.36).move_to(lat.p(*box_walker(H, z)[-1]))) for z in range(3)])
        self.play(FadeIn(lat), FadeIn(ends), run_time=0.8)
        paths = [path_mob(lat, box_walker(H, z), cols[2 - z], 7) for z in range(3)]
        self.sfx("whoosh")
        self.play(*[ReplacementTransform(chs[z].copy(), paths[z]) for z in range(3)], run_time=2.0)
        ants_ = VGroup(*[ant(cols[2 - z], 0.5).move_to(lat.p(*box_walker(H, z)[0])) for z in range(3)])
        self.sfx("pop")
        self.play(FadeIn(ants_, scale=0.4), run_time=0.6)

        # 3: same recipe: count paths ant -> house, take the determinant
        self.cue(3)
        board = VGroup(lat, ends, ants_, *paths)
        self.play(FadeOut(VGroup(hexo, til, *chs)), board.animate.move_to(LEFT * 3.6 + DOWN * 0.3), run_time=1.2)
        M = matrix_mob([[str(v) for v in r] for r in M3B], size=44, h_buff=0.8, v_buff=0.55)
        Aeq = T("A  =", 42)
        VGroup(Aeq, M).arrange(RIGHT, buff=0.3).move_to(RIGHT * 3.0 + UP * 1.3)
        col_lab = VGroup(*[house(cols[k], 0.4).next_to(M.cells[k], UP, buff=0.35) for k in range(3)])
        row_lab = VGroup(*[ant(cols[k], 0.45).next_to(M, RIGHT, buff=0.3).match_y(M.cells[3 * k]) for k in range(3)])
        for cl in M.cells:
            cl.set_opacity(0)
        self.play(FadeIn(Aeq), FadeIn(VGroup(M[0], M[2])), FadeIn(col_lab), FadeIn(row_lab), run_time=0.8)
        self.add(M.cells)
        self.cue_at(3, "count the paths", lead=0.2)
        for k in range(9):
            self.sfx("tick")
            self.play(M.cells[k].animate.set_opacity(1), run_time=0.25)

        # 4: nine hundred and eighty stacks of boxes
        self.cue(4)
        eq = T("=", 38).move_to(np.array([Aeq[-1].get_x(), -1.2, 0]))
        row = VGroup(eq, T("det A", 38).next_to(eq, LEFT, buff=0.3),
                     T("980", 46, YELLOW, weight=BOLD).next_to(eq, RIGHT, buff=0.3))
        self.sfx("chime")
        self.play(Write(row), run_time=0.9)

        # 5: MacMahon counted these over a century ago; the ants do it with one determinant
        self.cue(5)
        mac = T("Percy MacMahon, 1915", 26, SOFT).next_to(row, DOWN, buff=0.5).align_to(row, LEFT)
        self.cue_at(5, "MacMahon", lead=0.2)
        self.play(FadeIn(mac), run_time=0.6)
        self.cue_end(5)
        self.wait(0.6)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.6)
