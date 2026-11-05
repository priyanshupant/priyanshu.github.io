"""Act 4 — Why it works (Script v2, 5:30-8:30).

    ReadCounts    10·10 = all own-home pairs (good + bad); 10·5 = swapped-home pairs
    SwapPaths     first meeting point; swap the paths after it -> a swapped pair
    SwapTwice     swapping again restores the pair (an involution)
    DiagonalSweep every swapped pair must meet: the gap goes -1 -> +1 in steps of 1
    PutTogether   50 bad <-> 50 swapped cancel; the 50 good pairs remain
"""
from common import *
from act1_problem import GRID_C

P = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]   # ant 1, a bad pair...
Q = [(1, 0), (1, 1), (1, 2), (2, 2), (3, 2)]   # ...with ant 2, first meeting at (1,2)
N11, N12 = len(all_paths(A1, B1)), len(all_paths(A1, B2))
N21, N22 = len(all_paths(A2, B1)), len(all_paths(A2, B2))
NBAD = sum(1 for p, q in plus_pairs() if first_meet(p, q) is not None)
NGOOD = N11 * N22 - NBAD
NSW = N12 * N21
P_SW, Q_SW = swap_tails(P, Q)


def is_bad(pq):
    return first_meet(*pq) is not None


def split(lat, p, q, m, c1=ANT1, c2=ANT2):
    i, j = p.index(m), q.index(m)
    return (path_mob(lat, p[:i + 1], c1), DashedVMobject(path_mob(lat, p[i:], c1), num_dashes=18),
            path_mob(lat, q[:j + 1], c2), DashedVMobject(path_mob(lat, q[j:], c2), num_dashes=18))


class ReadCounts(DScene):
    def construct(self):
        top = T(f"det  =  {N11} · {N22}   −   {N12} · {N21}", 48).to_edge(UP, buff=0.35)
        self.add(top)
        self.cue(0)
        own, sw = plus_pairs(), minus_pairs()
        left = VGroup(*[pair_icon(p, q, size=0.5, meet=False) for p, q in own]).arrange_in_grid(N11, N22, buff=0.06)
        right = VGroup(*[pair_icon(p, q, size=0.5, meet=False) for p, q in sw]).arrange_in_grid(N12, N21, buff=0.06)
        left.move_to(UP * 0.45).to_edge(LEFT, buff=0.4)
        right.next_to(left, RIGHT, buff=0.45).align_to(left, DOWN)
        self.play(top[4:7].animate.set_color(YELLOW), LaggedStartMap(FadeIn, left, lag_ratio=0.01), run_time=2)
        ll = T("each to its own home", 28, YELLOW).next_to(left, DOWN, buff=0.15)
        self.play(FadeIn(ll))
        self.cue(1)
        # colour good / bad
        self.play(*[ic[0].animate.set_stroke(BAD if is_bad(pq) else GOOD, 2.5) for ic, pq in zip(left, own)], run_time=1)
        brace = VGroup(T(f"{N11 * N22} =", 28), T(f"{NGOOD} never meet", 28, GOOD), T("+", 28),
                       T(f"{NBAD} meet", 28, BAD)).arrange(RIGHT, buff=0.16)
        brace.next_to(ll, DOWN, buff=0.15)
        if brace.width > left.width:
            brace.scale_to_fit_width(left.width)
        brace.set_x(left.get_x())
        self.cue_at(1, "twenty that never meet")
        self.play(FadeIn(brace))
        self.cue(2)
        self.play(top[8:].animate.set_color(ORANGE), LaggedStartMap(FadeIn, right, lag_ratio=0.02), run_time=1.5)
        rl = VGroup(T("swapped homes", 28, ORANGE), T("each ant to the", 24, ORANGE), T("other one's house", 24, ORANGE)).arrange(DOWN, buff=0.08)
        rl.next_to(right, DOWN, buff=0.15)
        self.play(FadeIn(rl))
        self.cue(3)
        eq = VGroup(T("det  =", 36),
                    T(f"{NGOOD} never meet", 34, GOOD), T(f"+ {NBAD} meet", 34, BAD), T(f"− {NSW} swapped", 34, ORANGE))
        eq[1:].arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        eq[0].next_to(eq[1], UP, buff=0.3, aligned_edge=LEFT)
        eq.move_to(RIGHT * 3.2 + UP * 0.6)
        self.play(FadeIn(eq[0]), TransformFromCopy(brace[1], eq[1]), TransformFromCopy(brace[3], eq[2]),
                  TransformFromCopy(rl[0], eq[3]), run_time=1.2)
        self.cue_at(3, "For that")
        xr = max(eq[2].get_right()[0], eq[3].get_right()[0]) + 0.15      # clear of both lines of text
        link = CurvedArrow(np.array([xr, eq[2].get_y(), 0]), np.array([xr, eq[3].get_y(), 0]), angle=-PI / 1.6,
                           color=YELLOW, stroke_width=4)
        same = T("equal?", 28, YELLOW).next_to(link, RIGHT, buff=0.08)
        if same.get_right()[0] > 7.0:
            same.next_to(link, DOWN, buff=0.08)
        self.play(Create(link), FadeIn(same))
        self.cue_at(3, "Not roughly")
        res = T(f"= {NGOOD} never meet", 40, GOOD).next_to(eq[3], DOWN, buff=0.5).align_to(eq[1], LEFT)
        self.play(eq[2].animate.set_opacity(0.35), eq[3].animate.set_opacity(0.35), FadeIn(res, shift=UP * 0.2))
        self.cue_at(3, "Let's match")
        self.play(Indicate(VGroup(link, same), color=YELLOW))


class SwapPaths(DScene):
    def construct(self):
        lat = Lattice(GRID[0], spacing=1.2, center=GRID_C, ny=GRID[1])
        ends = endpoints(lat)
        L = ant(ANT1).move_to(lat.p(*A1))
        N = ant(ANT2).move_to(lat.p(*A2))
        self.add(lat, ends, L, N)
        lab = T("a bad pair", 34, BAD).move_to(RIGHT * 3 + UP * 2.6)
        self.cue(0)
        self.play(FadeIn(lab))
        m = first_meet(P, Q)
        anims, tr = walk_steps(lat, [(L, P, ANT1), (N, Q, ANT2)], step_time=0.45)
        for an in anims:
            self.play(an)
        self.cue(1)
        # a probe walks along ant 1's route, checking each dot against ant 2's route
        probe = Dot(lat.p(*P[0]), radius=0.16, color=YELLOW)
        self.play(FadeIn(probe, scale=2), run_time=0.3)
        for v in P[1:P.index(m) + 1]:
            self.play(probe.animate.move_to(lat.p(*v)), run_time=0.5)
            if v != m:
                self.play(Flash(probe, color=GREY_B, line_length=0.15, flash_radius=0.25), run_time=0.35)
        ring = Circle(radius=0.45, color=MEET, stroke_width=5).move_to(lat.p(*m))
        rl = VGroup(T("the first dot of ant 1's route", 28, MEET), T("that ant 2 also visits", 28, MEET)).arrange(DOWN, buff=0.06)
        rl.next_to(lab, DOWN, buff=0.6)
        arrow = Arrow(rl.get_left(), ring.get_right(), buff=0.15, color=MEET, stroke_width=3)
        self.sfx("alert")
        self.play(Create(ring), FadeOut(probe), FadeIn(rl), GrowArrow(arrow))
        self.cue(2)
        hP, tP, hQ, tQ = split(lat, P, Q, m)
        self.play(FadeOut(VGroup(*tr)), FadeIn(VGroup(hP, tP, hQ, tQ)), FadeOut(arrow))
        legend = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.6), T("before the meeting point", 26)).arrange(RIGHT),
                        VGroup(DashedLine(ORIGIN, RIGHT * 0.6), T("after it", 26)).arrange(RIGHT)) \
            .arrange(DOWN, aligned_edge=LEFT).next_to(rl, DOWN, buff=0.5)
        self.play(FadeIn(legend))
        swap = T("swap the tails", 34, YELLOW).next_to(legend, DOWN, buff=0.5)
        self.cue_at(2, "swap their")
        self.play(Write(swap))
        self.cue_at(2, "Ant one keeps")
        i, j = P.index(m), Q.index(m)
        ntP = DashedVMobject(path_mob(lat, Q[j:], ANT1), num_dashes=18)
        ntQ = DashedVMobject(path_mob(lat, P[i:], ANT2), num_dashes=18)
        self.sfx("whoosh")
        self.play(Transform(tP, ntP, path_arc=-PI / 2), Transform(tQ, ntQ, path_arc=-PI / 2),
                  L.animate(path_arc=-PI / 2).move_to(lat.p(*B2)),
                  N.animate(path_arc=-PI / 2).move_to(lat.p(*B1)), run_time=2.2)
        self.cue(3)
        self.play(Transform(lab, T("a swapped pair", 34, ORANGE).move_to(lab)))
        where = VGroup(T("ant 1 → B₂", 26, ANT1), T("ant 2 → B₁", 26, ANT2)).arrange(RIGHT, buff=0.5)
        where.next_to(swap, DOWN, buff=0.4)
        self.play(FadeIn(where))


class SwapTwice(DScene):
    def construct(self):
        lat = Lattice(GRID[0], spacing=1.2, center=GRID_C, ny=GRID[1])
        ends = endpoints(lat)
        m = first_meet(P, Q)
        i, j = P.index(m), Q.index(m)
        hP, hQ = path_mob(lat, P[:i + 1], ANT1), path_mob(lat, Q[:j + 1], ANT2)
        tP = DashedVMobject(path_mob(lat, Q[j:], ANT1), num_dashes=18)
        tQ = DashedVMobject(path_mob(lat, P[i:], ANT2), num_dashes=18)
        ring = Circle(radius=0.45, color=MEET, stroke_width=5).move_to(lat.p(*m))
        L = ant(ANT1).move_to(lat.p(*B2))
        N = ant(ANT2).move_to(lat.p(*B1))
        lab = T("a swapped pair", 32, ORANGE).move_to(RIGHT * 3 + UP * 2.6)
        self.add(lat, ends, hP, hQ, tP, tQ, ring, L, N, lab)
        self.cue(0)
        again = T("swap again at the first meeting point", 28, YELLOW).next_to(lab, DOWN, buff=0.6)
        self.play(Write(again))
        self.cue(1)
        same = T("nothing before it changed,\nso it is still the first meeting point", 28, SOFT, line_spacing=1.1) \
            .next_to(again, DOWN, buff=0.3)
        self.cue_at(1, "Nothing before")
        self.play(Indicate(VGroup(hP, hQ), color=YELLOW), FadeIn(same))
        self.cue_at(1, "still the first")
        self.play(ring.animate.scale(1.3), rate_func=there_and_back, run_time=0.6)
        ntP = DashedVMobject(path_mob(lat, P[i:], ANT1), num_dashes=18)
        ntQ = DashedVMobject(path_mob(lat, Q[j:], ANT2), num_dashes=18)
        self.cue_at(1, "swapping there")
        self.sfx("whoosh")
        self.play(Transform(tP, ntP, path_arc=PI / 2), Transform(tQ, ntQ, path_arc=PI / 2),
                  L.animate(path_arc=PI / 2).move_to(lat.p(*B1)),
                  N.animate(path_arc=PI / 2).move_to(lat.p(*B2)), run_time=1.6)
        self.play(Transform(lab, T("back to the bad pair", 34, BAD).move_to(lab)), run_time=0.5)
        # 2: the involution as a picture
        self.cue(2)
        a_ic = pair_icon(P, Q, size=1.4)
        b_ic = pair_icon(P_SW, Q_SW, size=1.4)
        a_ic[0].set_stroke(BAD, 3)
        b_ic[0].set_stroke(ORANGE, 3)
        pair = VGroup(a_ic, b_ic).arrange(RIGHT, buff=1.6).move_to(RIGHT * 3.8 + DOWN * 0.85)
        top_ar = CurvedArrow(a_ic.get_top() + UP * 0.1, b_ic.get_top() + UP * 0.1, angle=-PI / 3, color=YELLOW)
        bot_ar = CurvedArrow(b_ic.get_bottom() + DOWN * 0.1, a_ic.get_bottom() + DOWN * 0.1, angle=-PI / 3, color=YELLOW)
        sw1 = T("swap", 26, YELLOW).next_to(top_ar, UP, buff=0.05)
        sw2 = T("swap", 26, YELLOW).next_to(bot_ar, DOWN, buff=0.05)
        self.play(FadeOut(again), FadeOut(same), FadeIn(a_ic), run_time=0.6)
        self.play(Create(top_ar), FadeIn(sw1), FadeIn(b_ic), run_time=0.8)
        self.play(Create(bot_ar), FadeIn(sw2), run_time=0.8)
        inv = T("an involution", 40, YELLOW).next_to(lab, DOWN, buff=0.3)
        self.cue_at(2, "involution")
        self.play(Write(inv))
        joke = T("(like most committee meetings)", 26, SOFT).next_to(inv, DOWN, buff=0.1)
        self.cue_at(2, "Like most")
        self.play(FadeIn(joke))
        # 3: couples
        self.cue(3)
        cpl = T("bad pairs and swapped pairs that meet\ncome in perfect couples", 30, line_spacing=1.1).next_to(sw2, DOWN, buff=0.2)
        cpl.scale_to_fit_width(min(cpl.width, 6.2)).set_x(3.8)
        self.play(FadeIn(cpl), Circumscribe(pair, color=YELLOW))


class DiagonalSweep(DScene):
    def construct(self):
        lat = Lattice(GRID[0], spacing=1.2, center=GRID_C, ny=GRID[1])
        ends = endpoints(lat)
        self.add(lat, ends)
        mp = minus_pairs()
        p, q = mp[0]                       # a swapped pair: ant 1 -> B2, ant 2 -> B1
        pm, qm = path_mob(lat, p, ANT1, 7), path_mob(lat, q, ANT2, 7)
        title = T("Can a swapped pair avoid meeting?", 32).move_to(RIGHT * 2.6 + UP * 2.9)
        self.cue(0)
        self.play(Write(title))
        self.play(Create(pm), Create(qm), run_time=1.5)

        def diag_line(s):
            xa, xb = min(3.5, s + 0.5), max(-0.5, s - 3.5)      # clip x + y = s to the grid
            return DashedLine(lat.p(xa, s - xa), lat.p(xb, s - xb), color=GREY_B, dash_length=0.12)

        def spots(s):
            pl = next(v for v in p if v[0] + v[1] == s)
            ql = next(v for v in q if v[0] + v[1] == s)
            return pl, ql, VGroup(Dot(lat.p(*pl), radius=0.13, color=ANT1), Dot(lat.p(*ql), radius=0.13, color=ANT2))

        # 1: sweep once: one dot per ant per diagonal
        self.cue(1)
        rule = T("each step: next diagonal", 28).next_to(title, DOWN, buff=0.4)
        diag = diag_line(1)
        _, _, mk = spots(1)
        self.cue_at(1, "Sweep")
        self.play(Create(diag), FadeIn(mk), run_time=0.6)
        self.cue_at(1, "Every step")
        self.play(FadeIn(rule))
        for s in range(2, 6):
            _, _, nm = spots(s)
            self.play(Transform(diag, diag_line(s)), Transform(mk, nm), run_time=0.55)
            self.wait(0.15)
        # 2-4: the gap, filled in the order 1, 5, 2, 4 (3 is the punchline)
        self.cue(2)
        gap_lab = T("gap = ant 1's column − ant 2's column", 28, SOFT).next_to(rule, DOWN, buff=0.45)
        slots = VGroup(*[VGroup(T(f"s = {s}", 24, SOFT), T("?", 34, GREY_D)).arrange(DOWN, buff=0.1) for s in range(1, 6)])
        slots.arrange(RIGHT, buff=0.45).next_to(gap_lab, DOWN, buff=0.35)
        self.play(FadeIn(gap_lab), FadeIn(slots))

        def reveal(s):
            pl, ql, nm = spots(s)
            gap = pl[0] - ql[0]
            col = YELLOW if gap == 0 else (ANT1 if gap > 0 else ANT2)
            val = T(f"{gap:+d}" if gap else "0", 38, col).move_to(slots[s - 1][1])
            self.play(Transform(diag, diag_line(s)), Transform(mk, nm), Transform(slots[s - 1][1], val), run_time=0.6)
            return pl, gap
        self.cue_at(2, "At the start")
        reveal(1)
        self.cue(3)
        reveal(5)
        self.cue(4)
        self.cue_at(4, "next")
        reveal(2)
        reveal(4)
        step = T("each step: change of at most 1", 26, YELLOW).next_to(slots, DOWN, buff=0.3)
        self.play(FadeIn(step))
        # 5: so somewhere it is zero
        self.cue(5)
        pl, gap = reveal(3)
        ring = Circle(radius=0.45, color=MEET, stroke_width=5).move_to(lat.p(*pl))
        self.sfx("alert")
        self.play(Create(ring), Indicate(slots[2], color=YELLOW, scale_factor=1.4))
        meet = T("same dot!", 32, MEET).next_to(step, DOWN, buff=0.3)
        self.play(FadeIn(meet))
        ivt = T("(the intermediate value theorem,\nin its most humble form)", 26, SOFT, line_spacing=1.1).next_to(meet, DOWN, buff=0.35)
        self.cue_at(5, "That's the")
        self.play(FadeIn(ivt))


class PutTogether(DScene):
    def construct(self):
        own, sw = plus_pairs(), minus_pairs()
        bad = [k for k, pq in enumerate(own) if is_bad(pq)]
        good = [k for k, pq in enumerate(own) if not is_bad(pq)]
        partner = [sw.index(tuple(swap_tails(*own[k]))) for k in bad]
        assert sorted(partner) == list(range(NSW))
        # each swapped pair sits in the same grid position as its bad partner
        badv = VGroup(*[pair_icon(*own[k], size=0.6) for k in bad]).arrange_in_grid(4, 4, buff=0.1)
        swv = VGroup(*[pair_icon(*sw[partner[g]], size=0.6) for g in range(NBAD)]).arrange_in_grid(4, 4, buff=0.1)
        for ic in badv:
            ic[0].set_stroke(BAD, 2.5)
        for ic in swv:
            ic[0].set_stroke(ORANGE, 2.5)
        badv.move_to(LEFT * 3.2 + UP * 0.5)
        swv.move_to(RIGHT * 3.2 + UP * 0.5)
        t1 = T(f"{NBAD} bad pairs", 32, BAD).next_to(badv, UP, buff=0.2)
        t2 = T(f"{NSW} swapped pairs", 32, ORANGE).next_to(swv, UP, buff=0.2)
        eq = VGroup(T("det  =", 38), T(f"{NGOOD} good", 38, GOOD), T(f"+ {NBAD} bad", 38, BAD),
                    T(f"− {NSW} swapped", 38, ORANGE)).arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.55)
        self.cue(0)
        self.play(FadeIn(badv), FadeIn(swv), Write(t1), Write(t2), FadeIn(eq))
        k = 0
        while k < NBAD:
            n = 1 if k < 2 else 2 if k < 6 else 4
            if k == 6:
                self.cue(1)
            grp = list(range(k, min(NBAD, k + n)))
            links = VGroup(*[Line(badv[g].get_right(), swv[g].get_left(), color=YELLOW, stroke_width=2.5)
                             for g in grp])
            rt = 0.6 if k < 2 else 0.35 if k < 6 else 0.3
            self.play(Create(links), run_time=rt)
            self.sfx("pop")
            self.play(*[FadeOut(badv[g], scale=0.3) for g in grp], *[FadeOut(swv[g], scale=0.3) for g in grp],
                      FadeOut(links), run_time=rt)
            k += n
        cancel = VGroup(Line(eq[2].get_corner(DL), eq[2].get_corner(UR), color=YELLOW, stroke_width=5),
                        Line(eq[3].get_corner(DL), eq[3].get_corner(UR), color=YELLOW, stroke_width=5))
        self.cue_at(1, "It removes")
        self.play(Create(cancel), run_time=0.6)
        self.play(FadeOut(VGroup(eq[2], eq[3], cancel)), FadeOut(t1), FadeOut(t2),
                  VGroup(eq[0], eq[1]).animate.move_to(DOWN * 3.0), run_time=0.8)
        self.cue(2)
        goodv = VGroup(*[pair_icon(*own[k], size=0.6) for k in good]).arrange_in_grid(4, 5, buff=0.12)
        for ic in goodv:
            ic[0].set_stroke(GOOD, 2.5)
        goodv.move_to(UP * 0.7)
        self.play(LaggedStartMap(FadeIn, goodv, lag_ratio=0.02), run_time=1.2)
        res = T("= the pairs that never meet", 36, YELLOW).next_to(VGroup(eq[0], eq[1]), RIGHT, buff=0.35)
        VGroup(eq[0], eq[1], res).generate_target()
        self.sfx("chime")
        self.play(VGroup(eq[0], eq[1]).animate.shift(LEFT * res.width / 2), FadeIn(res.shift(LEFT * res.width / 2)))
        self.cue(3)
        fin = T("a bijective proof  ∎", 32, SOFT).next_to(VGroup(eq[0], res), UP, buff=0.3)
        self.play(FadeIn(fin))
