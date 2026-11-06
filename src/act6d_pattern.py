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


# ------------------------------------------------------------------ mountain ranges (Catalan)
from act6b_disguises import dyck, CS, CE, CM, CFAM

CAT = [len(dyck((0, 0), (2 * n, 0))) for n in range(1, 5)]
assert CAT == [1, 2, 5, 14] and CM == [[2, 5], [5, 14]] and len(CFAM) == 3
assert round(np.linalg.det(np.array(CM, float))) == 3


class Mountains(DScene):
    """Detailed: what a range is; counting by length (1, 2, 5, 14); the Catalan numbers and where else they
    appear (brackets, triangulated pentagons); two ranges that never touch = paths; why the matrix is Catalan;
    det = 3 and the three pairs."""

    def construct(self):
        u, o = 0.7, LEFT * 4.0 + DOWN * 2.0
        P = lambda x, y: o + u * np.array([x, y, 0])

        def mtn(path, col, w=6, op=0.16, at=P):
            pts = [at(x, y) for x, y in path]
            return VGroup(Polygon(*pts, stroke_width=0, fill_color=col, fill_opacity=op),
                          VMobject(stroke_color=col, stroke_width=w).set_points_as_corners(pts))
        sea = Line(P(-3, 0), P(7, 0), color=BLUE_E, stroke_width=4)

        # 0: a range: up or down each step, never below sea level, starts and ends at sea level
        self.cue(0)
        self.play(Create(sea), run_time=0.8)
        one = [(0, 0), (1, 1), (2, 2), (3, 1), (4, 0)]
        segs = VGroup()
        for (x0, y0), (x1, y1) in zip(one, one[1:]):
            sg = Line(P(x0, y0), P(x1, y1), color=ANT1, stroke_width=6)
            self.sfx("step")
            self.play(Create(sg), run_time=0.5)
            segs.add(sg)
        bad = VGroup(DashedLine(P(4, 0), P(5, -1), color=BAD, stroke_width=5), cross(0.3).move_to(P(5, -1.25)))
        self.cue_at(0, "never dips", lead=0.2)
        self.sfx("buzz")
        self.play(FadeIn(bad), run_time=0.4)
        self.play(FadeOut(bad), run_time=0.4)
        ends_ = VGroup(Dot(P(0, 0), radius=0.1, color=YELLOW), Dot(P(4, 0), radius=0.1, color=YELLOW))
        self.cue_at(0, "starts and ends", lead=0.2)
        self.play(FadeIn(ends_, scale=1.6), run_time=0.5)
        self.play(FadeOut(ends_), run_time=0.3)

        # 1: how many ranges of each length: 1, 2, 5, 14 (one beat each)
        self.cue(1)
        self.play(FadeOut(segs), FadeOut(sea), run_time=0.4)
        g_u = 0.16
        rows = VGroup()
        for n in range(1, 4):
            ms = VGroup(*[mtn(p, ANT1, 3, 0.12, at=lambda x, y: np.array([x * g_u, y * g_u, 0]))
                          for p in dyck((0, 0), (2 * n, 0))]).arrange(RIGHT, buff=0.28, aligned_edge=DOWN)
            lab = T(f"{2 * n} steps", 24, SOFT)
            rows.add(VGroup(lab, ms, T(str(CAT[n - 1]), 34, YELLOW)).arrange(RIGHT, buff=0.4))
        rows.add(VGroup(T("8 steps", 24, SOFT), T("…", 34, SOFT), T(str(CAT[3]), 34, YELLOW)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.75).to_corner(UL, buff=0.6)
        for k, r in enumerate(rows):
            self.cue_at(1, ["two steps", "four steps", "Six steps", "Eight steps"][k], lead=0.15)
            self.play(FadeIn(r[0]), FadeIn(r[1], lag_ratio=0.15), run_time=0.8)
            self.sfx("tick")
            self.play(FadeIn(r[2], scale=1.4), run_time=0.3)

        # 2: one, two, five, fourteen: the Catalan numbers
        self.cue(2)
        seq = T("1,  2,  5,  14,  42, …", 40, YELLOW).move_to(RIGHT * 3.7 + UP * 2.7)
        name = T("the Catalan numbers", 32).next_to(seq, DOWN, buff=0.25)
        self.play(Write(seq), run_time=1.0)
        self.play(FadeIn(name), run_time=0.6)

        # 3: brackets: up = "(", down = ")"; every range is a balanced bracket string
        self.cue(3)
        r4 = rows[1][1]
        br = VGroup(*[T("".join("(" if b[1] > a_[1] else ")" for a_, b in zip(p, p[1:])), 30, ANT1).next_to(m, DOWN, buff=0.18)
                      for p, m in zip(dyck((0, 0), (4, 0)), r4)])
        self.cue_at(3, "opening bracket", lead=0.2)
        self.play(Indicate(r4, color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.play(FadeIn(br, shift=UP * 0.15), run_time=0.8)

        # 4: and the ways to cut a pentagon into triangles: five again
        self.cue(4)
        def pent(k, r=0.42):
            vs = [r * np.array([np.cos(PI / 2 + TAU * i / 5), np.sin(PI / 2 + TAU * i / 5), 0]) for i in range(5)]
            g = VGroup(Polygon(*vs, color=INK, stroke_width=3))
            g.add(Line(vs[k], vs[(k + 2) % 5], color=YELLOW, stroke_width=3), Line(vs[k], vs[(k + 3) % 5], color=YELLOW, stroke_width=3))
            return g
        pents = VGroup(*[pent(k) for k in range(5)]).arrange(RIGHT, buff=0.35).move_to(RIGHT * 3.7 + DOWN * 1.6)
        five = T("5", 40, YELLOW).next_to(pents, DOWN, buff=0.3)
        self.cue_at(4, "pentagon", lead=0.2)
        self.play(LaggedStart(*[FadeIn(p_) for p_ in pents], lag_ratio=0.3), run_time=1.6)
        self.play(FadeIn(five, scale=1.4), Indicate(rows[2][2], color=YELLOW, scale_factor=1.4), run_time=0.7)

        # 5: two ranges, one inside the other, never touching
        self.cue(5)
        self.play(FadeOut(VGroup(rows, seq, name, br, pents, five)), FadeIn(sea), run_time=0.6)
        inner, outer = CFAM[0]
        ok = VGroup(mtn(outer, ANT2), mtn(inner, ANT1))
        self.play(FadeIn(ok[0]), run_time=0.9)
        self.play(FadeIn(ok[1]), run_time=0.9)
        tk = tick(0.5, GOOD).move_to(P(6.6, 3.0))
        self.play(FadeIn(tk), run_time=0.3)
        touch = next((p, q) for p in dyck(CS[0], CE[0]) for q in dyck(CS[1], CE[1]) if set(p) & set(q))
        tm = VGroup(mtn(touch[1], ANT2), mtn(touch[0], ANT1))
        hit = sorted(set(touch[0]) & set(touch[1]))[0]
        ring = Circle(radius=0.3, color=MEET, stroke_width=5).move_to(P(*hit))
        xx = cross(0.4).move_to(P(6.6, 3.0))
        self.cue_at(5, "never touch", lead=0.2)
        self.play(FadeOut(ok), FadeOut(tk), FadeIn(tm), run_time=0.8)
        self.sfx("buzz")
        self.play(Create(ring), FadeIn(xx), run_time=0.5)

        # 6: paths again: two walkers, from these starts to these ends
        self.cue(6)
        self.play(FadeOut(VGroup(tm, ring, xx)), run_time=0.5)
        starts = VGroup(Dot(P(*CS[0]), radius=0.12, color=ANT1), Dot(P(*CS[1]), radius=0.12, color=ANT2))
        homes = VGroup(house(ANT1, 0.42).move_to(P(*CE[0]) + DOWN * 0.45), house(ANT2, 0.42).move_to(P(*CE[1]) + DOWN * 0.45))
        ants_ = VGroup(ant(ANT1, 0.5).next_to(starts[0], DOWN, buff=0.15), ant(ANT2, 0.5).next_to(starts[1], DOWN, buff=0.15))
        self.cue_at(6, "starting", lead=0.2)
        self.play(FadeIn(starts), FadeIn(ants_), run_time=0.7)
        self.cue_at(6, "ending", lead=0.2)
        self.play(FadeIn(homes), run_time=0.7)

        # 7: why the matrix is Catalan: blue->blue 4 steps (2), blue->orange 6 (5), orange: 5 and 14
        self.cue(7)
        M = matrix_mob([[str(v) for v in r] for r in CM], size=50, h_buff=0.9, v_buff=0.6)
        Aeq = T("A  =", 46)
        VGroup(Aeq, M).arrange(RIGHT, buff=0.3).move_to(RIGHT * 3.4 + UP * 1.6)
        col_lab = VGroup(*[house([ANT1, ANT2][k], 0.42).next_to(M.cells[k], UP, buff=0.35) for k in range(2)])
        row_lab = VGroup(*[ant([ANT1, ANT2][k], 0.5).next_to(M, RIGHT, buff=0.3).match_y(M.cells[2 * k]) for k in range(2)])
        for cl in M.cells:
            cl.set_opacity(0)
        self.play(FadeIn(Aeq), FadeIn(VGroup(M[0], M[2])), FadeIn(col_lab), FadeIn(row_lab), run_time=0.8)
        self.add(M.cells)
        words = ["four steps", "six steps", "The orange walker", "fourteen"]
        for k, (si, ej) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
            self.cue_at(7, words[k], lead=0.2)
            ex = mtn(dyck(CS[si], CE[ej])[0], [ANT1, ANT2][si], 5, 0.1)
            nsteps = CE[ej][0] - CS[si][0]
            tag = T(f"{nsteps} steps", 22, SOFT).next_to(M.cells[k], DOWN, buff=0.08)
            self.play(FadeIn(ex), FadeIn(tag), run_time=0.6)
            self.sfx("tick")
            self.play(M.cells[k].animate.set_opacity(1), run_time=0.3)
            self.play(FadeOut(ex), FadeOut(tag), run_time=0.3)

        # 8: its determinant: 2·14 − 5·5 = 3 ('=' under the '=' of A =)
        self.cue(8)
        x_eq = Aeq[-1].get_x()
        lines = [("det A", "2 · 14  −  5 · 5", INK), (None, "28  −  25", INK), (None, "3", YELLOW)]
        rowsd = VGroup()
        for i, (lhs, rhs, col) in enumerate(lines):
            eq = T("=", 38).move_to(np.array([x_eq, -0.4 - 0.75 * i, 0]))
            g = VGroup(eq, T(rhs, 38 if i < 2 else 46, col, weight=BOLD if i == 2 else NORMAL).next_to(eq, RIGHT, buff=0.3))
            if lhs:
                g.add(T(lhs, 38).next_to(eq, LEFT, buff=0.3))
            rowsd.add(g)
        self.cue_at(8, "two times fourteen", lead=0.2)
        self.play(Write(rowsd[0]), run_time=1.0)
        self.play(Write(rowsd[1]), run_time=0.7)
        self.sfx("chime")
        self.play(Write(rowsd[2]), run_time=0.7)

        # 9: and here they are: exactly three
        self.cue(9)
        self.play(FadeOut(VGroup(starts, homes, ants_, sea)), run_time=0.4)
        panels = VGroup()
        for inner_, outer_ in CFAM:
            Q = lambda x, y: 0.32 * np.array([x, y, 0])
            panels.add(VGroup(Line(Q(-2.6, 0), Q(6.6, 0), color=BLUE_E, stroke_width=3),
                              mtn(outer_, ANT2, 4, 0.16, at=Q), mtn(inner_, ANT1, 4, 0.16, at=Q)))
        panels.arrange(DOWN, buff=0.45).move_to(LEFT * 3.4 + DOWN * 0.1)
        for pn in panels:
            self.sfx("pop")
            self.play(FadeIn(pn, shift=UP * 0.2), run_time=0.7)
        self.cue_end(9)
        self.wait(0.6)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.6)
