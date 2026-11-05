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
        ends = endpoints(lat)
        L = ant(ANT1).move_to(lat.p(*A1))
        N = ant(ANT2).move_to(lat.p(*A2))
        self.add(lat, ends, L, N)
        self.cue(0)
        anims, _ = walk_steps(lat, [(L, GOOD_P, ANT1), (N, GOOD_Q, ANT2)], step_time=0.5)
        for an in anims:
            self.play(an)
        self.play(L.animate.shift(UP * 0.15), N.animate.shift(UP * 0.15), rate_func=there_and_back, run_time=0.4)
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
    def construct(self):
        lat = Lattice(GRID[0], spacing=1.15, center=LEFT * 4.5 + DOWN * 0.3, ny=GRID[1])
        ends = endpoints(lat, scale=0.95)
        self.add(lat, ends)
        cell = 1.5
        origin = RIGHT * 0.6 + UP * 2.1
        cells = {}
        boxes = VGroup()
        for r in range(2):
            for c in range(2):
                sq = Square(cell, color=DIM, stroke_width=2.5).move_to(origin + RIGHT * c * cell + DOWN * r * cell)
                cells[(r, c)] = sq
                boxes.add(sq)
        row_lab = VGroup(T("ant 1", 30, ANT1).next_to(cells[(0, 0)], LEFT, buff=0.3),
                         T("ant 2", 30, ANT2).next_to(cells[(1, 0)], LEFT, buff=0.3))
        col_lab = VGroup(T("B₁", 34, ANT1).next_to(cells[(0, 0)], UP, buff=0.2),
                         T("B₂", 34, ANT2).next_to(cells[(0, 1)], UP, buff=0.2))
        self.cue(0)
        self.cue_at(0, "Count the routes", lead=0.2)
        self.play(Create(boxes), FadeIn(row_lab, shift=RIGHT * 0.2), FadeIn(col_lab, shift=DOWN * 0.2))
        spec = [((0, 0), A1, B1, ANT1), ((0, 1), A1, B2, ANT1), ((1, 0), A2, B1, ANT2), ((1, 1), A2, B2, ANT2)]
        nums = {}
        for i, (rc, s, e, col) in enumerate(spec):
            paths = all_paths(s, e)
            sq = cells[rc]
            self.play(sq.animate.set_stroke(MEET, 4), run_time=0.3)
            drawn = VGroup(*[path_mob(lat, P, col, 6).set_stroke(opacity=0.45) for P in paths])
            self.play(LaggedStart(*[Create(m) for m in drawn], lag_ratio=0.15), run_time=0.8)
            n = T(str(len(paths)), 56).move_to(sq)
            self.sfx("tick")
            self.play(FadeIn(n, scale=1.4), FadeOut(drawn), sq.animate.set_stroke(DIM, 2.5), run_time=0.45)
            nums[rc] = n
        d1 = T(f"det  =  {N11} · {N22}  −  {N12} · {N21}", 38)
        d2 = T(f"=  {N11 * N22}  −  {N12 * N21}", 38)
        d3 = T(f"=  {N11 * N22 - N12 * N21}", 48, YELLOW, weight=BOLD)
        det = VGroup(d1, d2, d3).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(boxes, DOWN, buff=0.4).shift(RIGHT * 0.6)
        diag = VGroup(cells[(0, 0)], cells[(1, 1)])
        anti = VGroup(cells[(0, 1)], cells[(1, 0)])
        self.cue(1)
        self.play(Write(d1[:4]))
        self.cue_at(1, "six times")
        self.play(diag.animate.set_stroke(GOOD, 5), Write(d1[4:7]), run_time=0.8)
        self.cue_at(1, "minus")
        self.play(anti.animate.set_stroke(BAD, 5), Write(d1[7:]), run_time=0.8)
        self.play(Write(d2))
        self.cue(2)
        self.sfx("chime")
        self.play(Write(d3))
        bf = VGroup(T("brute force:", 30, GOOD), T(str(NGOOD), 46, GOOD, weight=BOLD)).arrange(RIGHT, buff=0.3) \
            .next_to(d3, RIGHT, buff=1.2)
        self.cue(3)
        self.play(FadeIn(bf, shift=LEFT))
        self.sfx("chime")
        eq = T("=", 46).move_to((d3.get_right() + bf.get_left()) / 2)
        self.play(FadeIn(eq))
        self.cue_at(3, "Coincidence", lead=0.2)
        q = T("Coincidence?", 42, YELLOW).move_to(RIGHT * 5.0 + UP * 1.4)
        self.play(Write(q))
        self.cue_at(3, "Let's find", lead=0.1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        title = T("How Determinants Can Count", 60, weight=BOLD)
        by = T(AUTHOR, 28, SOFT).next_to(title, DOWN, buff=0.45)
        self.sfx("whoosh")
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(by, shift=UP * 0.2))
        self.wait(1.8)
        self.play(FadeOut(title), FadeOut(by))
