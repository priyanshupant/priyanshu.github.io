"""Act 3 — Two walkers: brute force, then the trick (Script v2, 3:30-5:30).

    OneGoodPair   one peaceful pair walked by ant 1 and ant 2
    BruteForce    all 100 pairs checked: 50 never meet, 50 meet
    TableAndDet   the 2x2 path table [[10,10],[5,10]], det = 50 = brute force
"""
from common import *
from act1_problem import GRID_C

GOOD_P = [(0, 1), (0, 2), (0, 3), (1, 3), (2, 3)]   # ant 1: up first, then right
GOOD_Q = [(1, 0), (2, 0), (3, 0), (3, 1), (3, 2)]   # ant 2: right first, then up
N11, N12 = len(all_paths(A1, B1)), len(all_paths(A1, B2))
N21, N22 = len(all_paths(A2, B1)), len(all_paths(A2, B2))
NGOOD = sum(1 for P, Q in plus_pairs() if first_meet(P, Q) is None)


def touches(P, Q):
    return first_meet(P, Q) is not None


class OneGoodPair(DScene):
    def construct(self):
        lat = Lattice(GRID[0], spacing=1.2, center=GRID_C, ny=GRID[1])
        ends = endpoints(lat, labels=False)
        L = ant(ANT1).move_to(lat.p(*A1))
        N = ant(ANT2).move_to(lat.p(*A2))
        self.add(lat, ends, L, N)
        self.cue(0)
        anims, _ = walk_steps(lat, [(L, GOOD_P, ANT1), (N, GOOD_Q, ANT2)], step_time=0.5)
        for an in anims:
            self.play(an)
        self.play(L.animate.shift(LEFT * 0.5), N.animate.shift(DOWN * 0.5), run_time=0.4)   # step beside the houses, not on them
        self.cue(1)
        msg = VGroup(T("They never meet.", 34), T("Peace in our time.", 30, GOOD)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 1.3 + UP * 1, aligned_edge=LEFT)
        self.play(FadeIn(msg[0], shift=UP * 0.2))
        self.play(FadeIn(msg[1], shift=UP * 0.2))


class BruteForce(DScene):
    def construct(self):
        title = T(f"{N11} routes  ×  {N22} routes  =  {N11 * N22} pairs", 38).to_edge(UP, buff=0.3)
        title[:7].set_color(ANT1)
        title[8:15].set_color(ANT2)
        self.cue(0)
        self.play(Write(title))
        pairs = plus_pairs()
        P1s, P2s = all_paths(A1, B1), all_paths(A2, B2)
        sz = 0.74
        icons = VGroup(*[pair_icon(P, Q, size=sz, meet=False) for P, Q in pairs])
        icons.arrange_in_grid(N11, N22, buff=0.1).move_to(LEFT * 2.6 + DOWN * 0.55)
        frames = VGroup(*[ic[0].copy().set_stroke(DIM, 1.5) for ic in icons])
        # rows: ant 1's route; columns: ant 2's route
        from act2_one_walker import route_icon
        rows = VGroup(*[route_icon(P, ANT1, 0.5).next_to(icons[r * N22], LEFT, buff=0.25) for r, P in enumerate(P1s)])
        cols = VGroup(*[route_icon(Q, ANT2, 0.5).next_to(icons[c], UP, buff=0.18) for c, Q in enumerate(P2s)])
        assert all(pairs[r * N22 + c] == (P1s[r], P2s[c]) for r in range(N11) for c in range(N22))
        self.cue_at(0, "thirty-six")
        self.play(LaggedStartMap(FadeIn, frames, lag_ratio=0.02), LaggedStartMap(FadeIn, rows, lag_ratio=0.1),
                  LaggedStartMap(FadeIn, cols, lag_ratio=0.1), run_time=1.5)
        lab_g, lab_b = T("never meet:", 32, GOOD), T("meet:", 32, BAD)
        labs = VGroup(lab_g, lab_b).arrange(DOWN, aligned_edge=RIGHT, buff=0.45).move_to(RIGHT * 3.7 + UP * 1.7)
        n_g = T("0", 46, GOOD).next_to(lab_g, RIGHT, buff=0.3)
        n_b = T("0", 46, BAD).next_to(lab_b, RIGHT, buff=0.3).align_to(n_g, LEFT)
        self.cue(1)
        self.play(FadeIn(labs), FadeIn(n_g), FadeIn(n_b))
        good = bad = 0
        k = 0
        said = ["This pair", "This one meets", "So does"]
        batches = [1] * 3 + [3] * 3 + [6] * 2
        while k < len(pairs):
            size = batches.pop(0) if batches else 100
            if k < 3:
                self.cue_at(1, said[k], lead=0.05)
            elif k == 3:
                self.cue_at(1, "And so on", lead=0.05)
            idx = list(range(k, min(len(pairs), k + size)))
            anims, marks = [], []
            for i in idx:
                P, Q = pairs[i]
                bad_ = touches(P, Q)
                ic = icons[i]
                anims.append(FadeIn(ic, scale=1.2))
                mk = (cross(0.26) if bad_ else tick(0.26)).move_to(ic[0].get_corner(DR) + UL * 0.12)
                marks.append(mk)
                if bad_:
                    marks.append(Circle(radius=0.09, color=MEET, stroke_width=3).move_to(ic.lat.p(*first_meet(P, Q))))
                    bad += 1
                else:
                    good += 1
            single = size == 1
            self.sfx("buzz" if single and touches(*pairs[idx[0]]) else "tick")
            if single:
                spot = SurroundingRectangle(icons[idx[0]], color=YELLOW, buff=0.06)
                self.play(FadeIn(icons[idx[0]], scale=1.6), Create(spot), run_time=0.45)
                self.play(*[FadeIn(m) for m in marks], FadeOut(spot),
                          Transform(n_g, T(str(good), 46, GOOD).move_to(n_g, aligned_edge=LEFT)),
                          Transform(n_b, T(str(bad), 46, BAD).move_to(n_b, aligned_edge=LEFT)), run_time=0.35)
            else:
                self.play(LaggedStart(*anims, lag_ratio=0.15), run_time=0.5)
                self.play(*[FadeIn(m) for m in marks],
                          Transform(n_g, T(str(good), 46, GOOD).move_to(n_g, aligned_edge=LEFT)),
                          Transform(n_b, T(str(bad), 46, BAD).move_to(n_b, aligned_edge=LEFT)), run_time=0.3)
            k += size
        # 2: twenty
        self.cue(2)
        fifty = SurroundingRectangle(VGroup(lab_g, n_g), color=GOOD, buff=0.15)
        self.sfx("chime")
        self.play(Create(fifty), Indicate(n_g, color=GOOD, scale_factor=1.3))


class TableAndDet(DScene):
    """v11: same grid as the Hook (only the right-hand side changes). A matrix A whose rows are
    the ants and columns the houses; entries counted path by path; then det A, '=' aligned."""

    def construct(self):
        from act0_hook import GRID_HOOK
        lat = Lattice(4, spacing=1.45, center=GRID_HOOK)
        a1 = ant(ANT1, 0.9).move_to(lat.p(*A1))
        a2 = ant(ANT2, 0.9).move_to(lat.p(*A2))
        starts = VGroup(Dot(lat.p(*A1), radius=0.12, color=ANT1), Dot(lat.p(*A2), radius=0.12, color=ANT2))
        h1 = house(ANT1, 0.6).move_to(lat.p(*B1))
        h2 = house(ANT2, 0.6).move_to(lat.p(*B2))
        self.add(lat, starts, h1, h2, a1, a2)

        M = matrix_mob([[str(N11), str(N12)], [str(N21), str(N22)]], size=60, h_buff=1.0, v_buff=0.75)
        Aeq = T("A  =", 52)
        VGroup(Aeq, M).arrange(RIGHT, buff=0.3).move_to(RIGHT * 3.4 + UP * 1.5)
        cells = M.cells
        for c in cells:
            c.set_opacity(0)
        col_lab = VGroup(house(ANT1, 0.5).next_to(cells[0], UP, buff=0.45), house(ANT2, 0.5).next_to(cells[1], UP, buff=0.45))
        row_lab = VGroup(ant(ANT1, 0.6).next_to(M, RIGHT, buff=0.35).match_y(cells[0]),
                         ant(ANT2, 0.6).next_to(M, RIGHT, buff=0.35).match_y(cells[2]))

        # 0: "this is stupid, there must be an easier way… here comes an old friend"
        self.cue(0)
        self.cue_at(0, "magic trick", lead=0.2)
        self.sfx("whoosh")

        # 1: consider this 2x2 matrix A: rows are the ants, columns the houses
        self.cue(1)
        self.cue_at(1, "matrix", lead=0.2)
        self.play(FadeIn(Aeq), FadeIn(VGroup(M[0], M[2])), run_time=0.8)
        self.add(cells)                                   # entries start invisible and are revealed one by one
        self.cue_at(1, "rows", lead=0.2)
        self.play(FadeIn(row_lab, shift=LEFT * 0.2), run_time=0.6)
        self.cue_at(1, "columns", lead=0.2)
        self.play(FadeIn(col_lab, shift=DOWN * 0.2), run_time=0.6)

        def count_into(k, s_, e_, col, word, line):
            """Draw the paths from s_ to e_ one by one; the entry counts up as they appear."""
            cell = cells[k]
            ring = SurroundingRectangle(cell, color=MEET, buff=0.2, corner_radius=0.1)
            self.cue_at(line, word, lead=0.2)
            self.play(Create(ring), run_time=0.4)
            num = T("0", 60).move_to(cell)
            self.add(num)
            prev = None
            for j, P in enumerate(all_paths(s_, e_), 1):
                pm = path_mob(lat, P, col, 7)
                anims = [Create(pm)] + ([prev.animate.set_stroke(opacity=0.18)] if prev else [])
                self.play(*anims, run_time=0.45)
                self.sfx("tick")
                self.play(Transform(num, T(str(j), 60).move_to(cell)), run_time=0.2)
                prev = pm
                self.add(pm)
                pm.tag = True
            self.play(FadeOut(VGroup(*[m for m in self.mobjects if getattr(m, "tag", False)])), FadeOut(ring), run_time=0.4)
            self.remove(num)
            cell.set_opacity(1)

        # 2: first entry: blue ant to its own home (six)
        self.cue(2)
        count_into(0, A1, B1, ANT1, "first entry", 2)
        # 3: second entry, the sneaky one: blue ant to the orange ant's house (four)
        self.cue(3)
        count_into(1, A1, B2, ANT1, "paths from the blue", 3)
        # 4: by symmetry, the orange ant: four and six
        self.cue(4)
        self.cue_at(4, "symmetry", lead=0.2)
        self.sfx("pop")
        self.play(cells[2].animate.set_opacity(1), cells[3].animate.set_opacity(1), run_time=0.8)

        # 5-8: counting paths on a grid is easy: count the rights and the ups, then choose
        self.cue(5)
        P1 = [(0, 1), (1, 1), (2, 1), (2, 2), (2, 3)]           # R R U U
        P2 = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]           # U R U R
        P3 = [(0, 1), (1, 1), (2, 1), (3, 1), (3, 2)]           # R R R U (to the orange house)

        def steps(P):
            return ["R" if P[i + 1][0] > P[i][0] else "U" for i in range(len(P) - 1)]

        slots = VGroup(*[Square(0.62, color=SOFT, stroke_width=3) for _ in range(4)]).arrange(RIGHT, buff=0.14)
        slots.move_to(RIGHT * 2.6 + DOWN * 1.15)
        arrow = {"R": r"\rightarrow", "U": r"\uparrow"}

        def fill(P, col):
            return VGroup(*[MathTex(arrow[st], color=col).scale(1.1).move_to(sq) for st, sq in zip(steps(P), slots)])

        pm = path_mob(lat, P1, ANT1, 7)
        self.play(Create(pm), FadeIn(slots), run_time=0.9)
        # 6: two rights and two ups, in some order
        self.cue(6)
        self.cue_at(6, "two steps right", lead=0.2)
        ar = fill(P1, ANT1)
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.1) for x in ar], lag_ratio=0.3), run_time=1.0)
        self.cue_at(6, "different order", lead=0.2)
        pm2 = path_mob(lat, P2, ANT1, 7)
        ar2 = fill(P2, ANT1)
        self.play(ReplacementTransform(pm, pm2), ReplacementTransform(ar, ar2), run_time=0.9)
        pm, ar = pm2, ar2
        # 7: which two of the four go right: 4 choose 2 = 6
        self.cue(7)
        self.cue_at(7, "which two", lead=0.2)
        rs = VGroup(*[SurroundingRectangle(x, color=YELLOW, buff=0.12) for x, st in zip(ar, steps(P2)) if st == "R"])
        self.play(Create(rs), run_time=0.6)
        c42 = MathTex(r"\binom{4}{2} = 6", color=YELLOW).scale(1.0).next_to(slots, RIGHT, buff=0.45)
        self.cue_at(7, "four choose two", lead=0.2)
        self.play(Write(c42), FadeOut(rs), run_time=0.8)
        self.play(Indicate(cells[0], color=YELLOW, scale_factor=1.3), run_time=0.7)
        # 8: to the orange house: three rights, one up: 4 choose 1 = 4
        self.cue(8)
        pm3 = path_mob(lat, P3, ANT1, 7)
        ar3 = fill(P3, ANT1)
        self.play(ReplacementTransform(pm, pm3), ReplacementTransform(ar, ar3), FadeOut(c42), run_time=0.9)
        c41 = MathTex(r"\binom{4}{1} = 4", color=YELLOW).scale(1.0).next_to(slots, RIGHT, buff=0.45)
        self.cue_at(8, "Four choose one", lead=0.2)
        self.play(Write(c41), run_time=0.8)
        self.play(Indicate(cells[1], color=YELLOW, scale_factor=1.3), run_time=0.7)
        self.cue_end(8)
        self.play(FadeOut(VGroup(pm3, ar3, slots, c41)), run_time=0.5)

        # 9-10: det A, each '=' directly under the '=' of "A ="
        x_eq = Aeq[-1].get_x()
        lines = [(T("det A", 36), T(f"{N11} · {N22}  −  {N12} · {N21}", 36)),
                 (None, T(f"{N11 * N22}  −  {N12 * N21}", 36)),
                 (None, T(f"{N11 * N22 - N12 * N21}", 44, YELLOW, weight=BOLD))]
        rows = VGroup()
        for i, (lhs, rhs) in enumerate(lines):
            eq = T("=", 36).move_to(np.array([x_eq, -0.75 - 0.75 * i, 0]))
            rhs.next_to(eq, RIGHT, buff=0.3)
            grp = VGroup(eq, rhs)
            if lhs is not None:
                lhs.next_to(eq, LEFT, buff=0.3)
                grp.add(lhs)
            rows.add(grp)
        self.cue(9)
        self.cue_at(9, "determinant of A", lead=0.2)
        self.play(Write(rows[0][2]), Write(rows[0][0]), run_time=0.7)
        self.cue_at(9, "six times six", lead=0.2)
        self.play(Write(rows[0][1]), run_time=1.0)
        self.play(Write(rows[1]), run_time=0.8)
        self.cue(10)
        self.sfx("chime")
        self.play(Write(rows[2]), run_time=0.8)

        # 11: the same number as before; then only the right-hand side clears (the next scene grows the grid)
        self.cue(11)
        self.play(Indicate(rows[2], color=YELLOW, scale_factor=1.2), run_time=0.9)
        self.cue_end(11)
        self.play(FadeOut(VGroup(Aeq, M, col_lab, row_lab, rows)), run_time=0.6)

