"""Act 4 (v13) — why it works, in Priyanshu's order: ants first, formula last.

    SwappedToMeet  a swapped pair; blue starts left of orange and ends right of it (diagonal sweep,
                   gap -1 .. +1) so they share a dot; swap the tails at the first shared dot ->
                   each ant at its own home, paths meeting
    MeetToSwapped  the other way: a meeting pair -> swap at the first shared dot -> swapped houses;
                   swap again at the same dot -> back where we started
    Bijection      all 16 meeting pairs matched with the 16 swapped pairs, one to one
    Formula        det A = 6·6 − 4·4 = (20 + 16) − 16 = 20, with examples on the grid
Slow, visual, few words; same board, symbols only; bullets on the right; '=' aligned.
"""
from common import *
from act4b_proof import setup, walk, turn, bullet_list, aligned, RX

P = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]   # own homes, meeting at (1, 2)
Q = [(1, 0), (1, 1), (1, 2), (2, 2), (3, 2)]
SP, SQ = swap_tails(P, Q)                      # the swapped pair it comes from
assert swap_tails(SP, SQ) == (P, Q) and SP[-1] == B2 and SQ[-1] == B1
P2 = [(0, 1), (1, 1), (2, 1), (2, 2), (2, 3)]  # another meeting pair, first shared dot (1, 1)
Q2 = [(1, 0), (1, 1), (1, 2), (2, 2), (3, 2)]
P2s, Q2s = swap_tails(P2, Q2)
assert first_meet(P2, Q2) == (1, 1) == first_meet(P2s, Q2s) and swap_tails(P2s, Q2s) == (P2, Q2)
N11, N12 = len(all_paths(A1, B1)), len(all_paths(A1, B2))
N21, N22 = len(all_paths(A2, B1)), len(all_paths(A2, B2))
MEETS = [pq for pq in plus_pairs() if first_meet(*pq) is not None]
NBAD, NGOOD = len(MEETS), N11 * N22 - len(MEETS)
assert (N11, N12, N21, N22, NBAD, NGOOD) == (6, 4, 4, 6, 16, 20)
assert sorted(swap_tails(*pq) for pq in MEETS) == sorted(minus_pairs())        # the bijection, checked

STEPS = ["wrong houses  →  meet", "meet  →  wrong houses", "one to one"]


def pair(lat, p, q, w=7, op=1.0):
    return VGroup(path_mob(lat, p, ANT1, w).set_stroke(opacity=op), path_mob(lat, q, ANT2, w).set_stroke(opacity=op))


class SwappedToMeet(DScene):
    def construct(self):
        lat, ends, a1, a2 = setup(self)
        steps = bullet_list(STEPS)
        sp = pair(lat, SP, SQ)

        # 0: a pair where the ants swap houses
        self.cue(0)
        self.play(FadeIn(steps[0], shift=LEFT * 0.2), run_time=0.6)
        self.play(Create(sp[0]), run_time=1.4)
        self.play(Indicate(ends[3], color=ANT1, scale_factor=1.4), run_time=0.7)      # blue ends at the orange house
        self.play(Create(sp[1]), run_time=1.4)
        self.play(Indicate(ends[2], color=ANT2, scale_factor=1.4), run_time=0.7)

        # 1: blue starts left of orange and ends right of it (sweep the diagonals; the column gap)
        self.cue(1)
        gaps = [p[0] - q[0] for p, q in zip(SP, SQ)]
        assert gaps == [-1, -1, 0, 1, 1]
        d = 6.2

        def diag(s):
            c = (lat.p(0, s) + lat.p(s, 0)) / 2
            return DashedLine(c + np.array([-1, 1, 0]) * d / 2.8, c + np.array([1, -1, 0]) * d / 2.8, color=SOFT, stroke_width=3)
        line = diag(1)
        mk = VGroup(Dot(lat.p(*SP[0]), radius=0.16, color=ANT1), Dot(lat.p(*SQ[0]), radius=0.16, color=ANT2))
        slots = [RIGHT * (RX - 1.6 + 0.95 * k) + UP * 0.9 for k in range(5)]
        vals = [T(f"{g:+d}" if g else "0", 36, ANT1 if g > 0 else ANT2 if g < 0 else YELLOW).move_to(slots[k])
                for k, g in enumerate(gaps)]
        qs = VGroup(*[T("·", 36, DIM).move_to(s_) for s_ in slots])
        gl = T("column gap (blue − orange)", 24, SOFT).next_to(VGroup(*[Dot(x) for x in slots]), UP, buff=0.3)
        self.play(Create(line), FadeIn(mk), FadeIn(qs), FadeIn(gl), run_time=0.8)
        self.play(Transform(qs[0], vals[0]), run_time=0.5)
        for s in range(2, 6):
            self.sfx("tick")
            self.play(Transform(line, diag(s)), mk[0].animate.move_to(lat.p(*SP[s - 1])), mk[1].animate.move_to(lat.p(*SQ[s - 1])),
                      run_time=0.8)
            self.play(Transform(qs[s - 1], vals[s - 1]), run_time=0.4)

        # 2: so somewhere they share a dot
        self.cue(2)
        z = gaps.index(0)
        self.play(Transform(line, diag(z + 1)), mk[0].animate.move_to(lat.p(*SP[z])), mk[1].animate.move_to(lat.p(*SQ[z])),
                  run_time=1.0)
        ring = Circle(radius=0.42, color=MEET, stroke_width=6).move_to(lat.p(*SP[z]))
        self.sfx("alert")
        self.play(Create(ring), Indicate(qs[z], color=YELLOW, scale_factor=1.6), run_time=0.8)
        self.play(FadeOut(line), FadeOut(mk), FadeOut(qs), FadeOut(gl), run_time=0.6)

        # 3: the first shared dot along the blue path; swap the tails from there
        self.cue(3)
        m = first_meet(SP, SQ)
        i, j = SP.index(m), SQ.index(m)
        h1, t1 = path_mob(lat, SP[:i + 1], ANT1, 7), path_mob(lat, SP[i:], ANT1, 7)
        h2, t2 = path_mob(lat, SQ[:j + 1], ANT2, 7), path_mob(lat, SQ[j:], ANT2, 7)
        self.remove(sp)
        self.add(h1, t1, h2, t2, ring)
        self.play(t1.animate.set_stroke(width=12), t2.animate.set_stroke(width=12), run_time=0.8)   # these are the tails
        self.play(t1.animate.set_stroke(width=7), t2.animate.set_stroke(width=7), run_time=0.5)
        self.sfx("whoosh")
        self.play(Transform(t1, path_mob(lat, SQ[j:], ANT1, 7)), Transform(t2, path_mob(lat, SP[i:], ANT2, 7)), run_time=2.0)

        # 4: now each is at its own home, and the paths meet (the ants walk them)
        self.cue(4)
        walk(self, lat, a1, P, step=0.5)
        walk(self, lat, a2, Q, step=0.5)
        self.play(a1.animate.shift(DOWN * 0.5), a2.animate.shift(DOWN * 0.5), run_time=0.3)
        self.sfx("chime")
        self.play(Indicate(ends[2], color=ANT1, scale_factor=1.4), Indicate(ends[3], color=ANT2, scale_factor=1.4),
                  Indicate(ring, color=MEET, scale_factor=1.3), run_time=1.0)
        self.cue_end(4)
        self.wait(0.5)


class MeetToSwapped(DScene):
    def construct(self):
        lat, ends, a1, a2 = setup(self)
        steps = bullet_list(STEPS)
        self.add(steps[0])

        # 0: the other way: a pair that meets on the way home
        self.cue(0)
        self.play(FadeIn(steps[1], shift=LEFT * 0.2), run_time=0.6)
        pm = pair(lat, P2, Q2)
        self.play(Create(pm[0]), run_time=1.3)
        self.play(Create(pm[1]), run_time=1.3)
        m = first_meet(P2, Q2)
        ring = Circle(radius=0.42, color=MEET, stroke_width=6).move_to(lat.p(*m))
        self.sfx("alert")
        self.play(Create(ring), run_time=0.6)

        # 1: swap the tails at the first shared dot -> each other's houses
        self.cue(1)
        i, j = P2.index(m), Q2.index(m)
        h1, t1 = path_mob(lat, P2[:i + 1], ANT1, 7), path_mob(lat, P2[i:], ANT1, 7)
        h2, t2 = path_mob(lat, Q2[:j + 1], ANT2, 7), path_mob(lat, Q2[j:], ANT2, 7)
        self.remove(pm)
        self.add(h1, t1, h2, t2, ring)
        self.play(t1.animate.set_stroke(width=12), t2.animate.set_stroke(width=12), run_time=0.7)
        self.play(t1.animate.set_stroke(width=7), t2.animate.set_stroke(width=7), run_time=0.4)
        self.sfx("whoosh")
        self.play(Transform(t1, path_mob(lat, Q2[j:], ANT1, 7)), Transform(t2, path_mob(lat, P2[i:], ANT2, 7)), run_time=2.0)
        self.play(Indicate(ends[3], color=ANT1, scale_factor=1.4), Indicate(ends[2], color=ANT2, scale_factor=1.4), run_time=0.9)

        # 2: swap again at the same dot -> back where we started
        self.cue(2)
        self.play(Indicate(ring, color=MEET, scale_factor=1.35), run_time=0.8)
        self.sfx("whoosh")
        self.play(Transform(t1, path_mob(lat, P2[i:], ANT1, 7)), Transform(t2, path_mob(lat, Q2[j:], ANT2, 7)), run_time=2.0)
        self.play(Indicate(ends[2], color=ANT1, scale_factor=1.4), Indicate(ends[3], color=ANT2, scale_factor=1.4), run_time=0.9)
        self.cue_end(2)
        self.wait(0.4)
        self.play(FadeOut(VGroup(h1, t1, h2, t2, ring)), run_time=0.5)


class Bijection(DScene):
    def construct(self):
        lat, ends, a1, a2 = setup(self)
        steps = bullet_list(STEPS)
        self.add(steps[0], steps[1])
        lab = T("matched:", 32, SOFT).move_to(RIGHT * (RX - 0.6) + DOWN * 0.4)
        cnt = T("0", 40, YELLOW).next_to(lab, RIGHT, buff=0.3)
        mi = pair_icon(*MEETS[0], size=1.0)
        si = pair_icon(*swap_tails(*MEETS[0]), size=1.0)
        mi[0].set_stroke(BAD, 3); si[0].set_stroke(ORANGE, 3)
        icons = VGroup(mi, si).arrange(RIGHT, buff=1.2).move_to(RIGHT * RX + UP * 0.9)
        link = DoubleArrow(mi.get_right(), si.get_left(), buff=0.15, color=YELLOW, stroke_width=4)

        # 0: swapped pairs and meeting pairs match up, one to one
        self.cue(0)
        self.play(FadeIn(steps[2], shift=LEFT * 0.2), FadeIn(lab), FadeIn(cnt), run_time=0.7)
        # 1-3: the first three named slowly; 4: "and so on"
        for k, (p, q) in enumerate(MEETS):
            ps, qs_ = swap_tails(p, q)
            a = pair(lat, p, q, 6)
            ring = Circle(radius=0.3, color=MEET, stroke_width=5).move_to(lat.p(*first_meet(p, q)))
            nmi = pair_icon(p, q, size=1.0).move_to(mi); nmi[0].set_stroke(BAD, 3)
            nsi = pair_icon(ps, qs_, size=1.0).move_to(si); nsi[0].set_stroke(ORANGE, 3)
            c2 = T(str(k + 1), 40, YELLOW).move_to(cnt, aligned_edge=LEFT)
            if k < 3:                                   # the first three, slowly, as they are named
                self.cue(1 + k)
                self.play(Create(a), Create(ring), FadeIn(nmi) if k == 0 else Transform(mi, nmi), run_time=0.9)
                if k == 0:
                    mi = nmi
                self.sfx("whoosh")
                self.play(Transform(a, pair(lat, ps, qs_, 6)), run_time=1.0)
                self.play(FadeIn(nsi) if k == 0 else Transform(si, nsi), GrowArrow(link) if k == 0 else Wait(0.01),
                          Transform(cnt, c2), run_time=0.6)
                if k == 0:
                    si = nsi
                self.sfx("pop")
                self.wait(0.2)
                self.play(FadeOut(a), FadeOut(ring), run_time=0.3)
            else:                                       # then the rest, faster and faster
                if k == 3:
                    self.cue(4)
                dt = max(0.18, 0.5 * 0.85 ** (k - 3))
                self.add(a, ring)
                self.play(Transform(a, pair(lat, ps, qs_, 6)), Transform(mi, nmi), Transform(si, nsi), Transform(cnt, c2), run_time=dt)
                self.remove(a, ring)

        # 5: a one-to-one match, so: meet = wrong houses
        self.cue(5)
        eqm = MathTex(r"\text{meet}", "=", r"\text{wrong houses}", color=YELLOW).scale(1.0)
        eqm.move_to(RIGHT * RX + DOWN * 1.6)
        self.sfx("chime")
        self.play(Indicate(VGroup(lab, cnt), color=YELLOW, scale_factor=1.2), run_time=0.8)
        self.cue_at(5, "exactly as many", lead=0.2)
        self.play(Write(eqm), run_time=1.0)
        self.cue_end(5)
        self.wait(0.4)
        self.play(FadeOut(VGroup(steps, lab, cnt, mi, si, link, eqm)), run_time=0.5)


class Formula(DScene):
    """det A = all − wrong houses = all − meet = never meet = 20 (the = signs aligned), with examples on the grid."""

    def construct(self):
        lat, ends, a1, a2 = setup(self)
        x_eq = RX - 0.9
        def row(lhs, rhs, y, col=WHITE):
            m = MathTex(lhs, "=", rhs, color=col)
            m.shift(np.array([x_eq, y, 0]) - m[1].get_center())
            return m
        r0 = row(r"\det A", r"\text{all} - \text{wrong houses}", 2.0)
        r1 = row("", r"\text{all} - \text{meet}", 1.0)
        r2 = row("", r"\text{never meet}", 0.0, GOOD)
        r3 = row("", r"20", -1.0, YELLOW)
        for r in (r1, r2, r3):                 # an empty lhs drops out: re-align on the '='
            r.shift(np.array([x_eq - r[0].get_x(), 0, 0]))
        good = next(pq for pq in plus_pairs() if first_meet(*pq) is None)
        bad = MEETS[0]
        sw = swap_tails(*bad)

        # 0: now the formula falls into place
        self.cue(0)
        # 1: det A = all − wrong houses (a wrong-house pair on the grid)
        self.cue(1)
        self.play(Write(r0), run_time=1.2)
        b = pair(lat, *sw)
        self.play(Create(b), run_time=1.0)
        self.play(Indicate(ends[3], color=ANT1, scale_factor=1.4), Indicate(ends[2], color=ANT2, scale_factor=1.4), run_time=0.8)
        # 2: = all − meet (the same pair, tails swapped: now it meets)
        self.cue(2)
        self.sfx("whoosh")
        rg = Circle(radius=0.32, color=MEET, stroke_width=5).move_to(lat.p(*first_meet(*bad)))
        self.play(Transform(b, pair(lat, *bad)), run_time=1.1)
        self.play(Create(rg), Write(r1), run_time=1.0)
        # 3: = the pairs that never meet
        self.cue(3)
        self.play(FadeOut(b), FadeOut(rg), run_time=0.4)
        g = pair(lat, *good)
        self.play(Create(g), Write(r2), run_time=1.2)
        # 4: twenty
        self.cue(4)
        self.sfx("chime")
        self.play(Write(r3), run_time=0.8)
        # 5: a bijective proof
        self.cue(5)
        qed = Square(0.3, color=INK, fill_opacity=1).next_to(r3, RIGHT, buff=0.5)
        self.play(FadeIn(qed, scale=0.5), run_time=0.4)
        self.cue_end(5)
        self.wait(0.6)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.6)


class AllPairs(DScene):
    """v14 (Priyanshu): back to the two ants with the matrix; det A = 6·6 − 4·4; why 6·6 = all 36 pairs of
    paths home (20 never meet + 16 meet), why 4·4 = the 16 pairs that go to the wrong houses; so
    det = all − wrong houses while never meet = all − meet; equal exactly because 16 = 16. But why?"""

    def construct(self):
        own, sw = plus_pairs(), minus_pairs()
        # 0: back to the two ants (grid, ants, houses) with the matrix on the right
        lat = big_lattice()
        ends = board(lat)
        a1 = ant(ANT1, 0.9).move_to(lat.p(*A1))
        a2 = ant(ANT2, 0.9).move_to(lat.p(*A2))
        grid = VGroup(lat, ends, a1, a2)
        M = matrix_mob([[str(N11), str(N12)], [str(N21), str(N22)]], size=50, h_buff=0.95, v_buff=0.7)
        Aeq = MathTex("A", "=").scale(1.2)
        VGroup(Aeq, M).arrange(RIGHT, buff=0.3)
        col_lab = VGroup(house(ANT1, 0.42).next_to(M.cells[0], UP, buff=0.35), house(ANT2, 0.42).next_to(M.cells[1], UP, buff=0.35))
        row_lab = VGroup(ant(ANT1, 0.5).next_to(M, RIGHT, buff=0.3).match_y(M.cells[0]),
                         ant(ANT2, 0.5).next_to(M, RIGHT, buff=0.3).match_y(M.cells[2]))
        mat = VGroup(Aeq, M, col_lab, row_lab).move_to(RIGHT * 3.4 + UP * 2.35)
        self.cue(0)
        self.play(FadeIn(grid), run_time=0.9)
        self.play(FadeIn(mat), run_time=0.8)

        # 1: its determinant: 6·6 − 4·4 (each '=' under the last)
        self.cue(1)
        x_eq = 2.5
        def row(lhs, rhs, y, col=WHITE, sc=0.95):
            m = MathTex(lhs, "=", rhs, color=col).scale(sc)
            m.shift(np.array([x_eq, y, 0]) - m[1].get_center())
            return m
        r0 = row(r"\det A", r"6 \cdot 6 - 4 \cdot 4", 0.5, sc=1.05)
        self.cue_at(1, "six times six", lead=0.2)
        self.play(Write(r0), run_time=1.2)

        # 2-3: why 6·6: six blue ways home, six orange ways home; any with any: all 36 pairs
        self.cue(2)
        b66 = SurroundingRectangle(r0[2][0:3], color=YELLOW, buff=0.08)
        self.play(Create(b66), run_time=0.5)
        bl = VGroup(*[path_mob(lat, p, ANT1, 6).set_stroke(opacity=0.85) for p in all_paths(A1, B1)])
        ol = VGroup(*[path_mob(lat, q, ANT2, 6).set_stroke(opacity=0.85) for q in all_paths(A2, B2)])
        self.cue_at(2, "The blue ant has six", lead=0.2)
        self.play(LaggedStart(*[Create(x) for x in bl], lag_ratio=0.25), run_time=1.4)
        self.play(FadeOut(bl), run_time=0.3)
        self.cue_at(2, "the orange ant has six", lead=0.2)
        self.play(LaggedStart(*[Create(x) for x in ol], lag_ratio=0.25), run_time=1.4)
        self.play(FadeOut(ol), run_time=0.3)
        self.cue(3)
        left = VGroup(*[pair_icon(p, q, size=0.38, meet=False) for p, q in own]).arrange_in_grid(6, 6, buff=0.05)
        right = VGroup(*[pair_icon(p, q, size=0.38, meet=False) for p, q in sw]).arrange_in_grid(4, 4, buff=0.05)
        left.move_to(DOWN * 0.1).to_edge(LEFT, buff=0.35)
        right.next_to(left, RIGHT, buff=0.4).align_to(left, DOWN)
        self.play(FadeOut(grid), run_time=0.6)
        self.play(LaggedStartMap(FadeIn, left, lag_ratio=0.04), run_time=2.2)
        l36 = T("all: 36", 26, YELLOW).next_to(left, DOWN, buff=0.15)
        self.play(FadeIn(l36), run_time=0.4)

        # 4: twenty never meet, sixteen meet
        self.cue(4)
        cols = [BAD if first_meet(*pq) is not None else GOOD for pq in own]
        self.cue_at(4, "Twenty", lead=0.2)
        self.play(*[ic[0].animate.set_stroke(c, 2.5) for ic, c in zip(left, cols) if c == GOOD], run_time=0.9)
        self.cue_at(4, "Sixteen", lead=0.2)
        self.play(*[ic[0].animate.set_stroke(c, 2.5) for ic, c in zip(left, cols) if c == BAD], run_time=0.9)
        split = VGroup(T(f"{NGOOD} never meet", 24, GOOD), T(f"{NBAD} meet", 24, BAD)).arrange(DOWN, buff=0.08)
        split.next_to(l36, DOWN, buff=0.1)
        self.play(FadeIn(split), FadeOut(b66), run_time=0.6)

        # 5: why 4·4: four ways each to the other's house: the 16 pairs that go to the wrong houses
        self.cue(5)
        b44 = SurroundingRectangle(r0[2][-3:], color=ORANGE, buff=0.08)
        self.play(Create(b44), run_time=0.5)
        self.cue_at(5, "So four times four", lead=0.2)
        self.play(LaggedStartMap(FadeIn, right, lag_ratio=0.06), run_time=1.6)
        for ic in right:
            ic[0].set_stroke(ORANGE, 2.5)
        l16 = T("16 wrong houses", 24, ORANGE).next_to(right, DOWN, buff=0.15)
        self.play(FadeIn(l16), run_time=0.5)

        # 6: so det A = all pairs − wrong-house pairs
        self.cue(6)
        r1 = MathTex("=", r"\text{all} - \text{wrong houses}").scale(0.95)
        r1.shift(np.array([r0[1].get_x(), -0.3, 0]) - r1[0].get_center())
        self.play(FadeOut(b44), Write(r1), run_time=1.2)
        # 7: but never meet = all pairs − pairs that meet
        self.cue(7)
        r2 = row(r"\text{never meet}", r"\text{all} - \text{meet}", -1.35, col=GOOD, sc=0.95)
        self.play(Write(r2), run_time=1.2)
        # 8: equal exactly when meet = wrong houses: and they are, 16 and 16
        self.cue(8)
        self.cue_at(8, "And there are", lead=0.2)
        r3 = row(r"\text{meet}", r"16 = \text{wrong houses}", -2.45, col=YELLOW, sc=0.95)
        self.play(Write(r3), Indicate(split[1], color=BAD, scale_factor=1.3), Indicate(l16, color=ORANGE, scale_factor=1.3), run_time=1.2)

        # 9: but why is that? (the grid comes back; the next scene shows how they correspond)
        self.cue(9)
        reds = VGroup(*[ic for ic, c in zip(left, cols) if c == BAD])
        link = CurvedArrow(reds.get_top() + UP * 0.1, right.get_top() + UP * 0.1, angle=-PI / 4, color=YELLOW)
        qm = T("?", 40, YELLOW).next_to(link, UP, buff=0.05)
        self.play(Create(link), FadeIn(qm), run_time=0.9)
        self.cue_end(9)
        self.wait(0.5)
        self.play(FadeOut(VGroup(left, right, l36, l16, split, link, qm, mat, r0, r1, r2, r3)), run_time=0.7)
        self.play(FadeIn(grid), run_time=0.7)


# ---------------------------------------------------------------- three ants: the same cancellation
from itertools import permutations as _perms, product as _product
import random as _random

S3 = [(0, 2), (1, 1), (2, 0)]
E3 = [(2, 4), (3, 3), (4, 2)]
COL3 = [ANT1, ANT2, ANT3]
ROWS3 = [(0, 1, 2), (1, 0, 2), (0, 2, 1), (2, 1, 0), (1, 2, 0), (2, 0, 1)]   # home; three swaps; two circles


def _sgn(p):
    return round(np.linalg.det(np.eye(3)[list(p)]))


def first_meeting3(fam):
    """Lowest ant that meets anyone, the first such dot on its path, the lowest other ant there."""
    for i in range(3):
        for v in fam[i]:
            js = [j for j in range(3) if j != i and v in fam[j]]
            if js:
                return i, v, min(js)
    return None


def swap3(fam, i, v, j):
    P, Q = fam[i], fam[j]
    a, b = P.index(v), Q.index(v)
    f = list(fam)
    f[i], f[j] = P[:a] + Q[b:], Q[:b] + P[a:]
    return tuple(tuple(x) for x in f)


FAMS3 = {p: [tuple(tuple(x) for x in f) for f in _product(*[all_paths(S3[i], E3[p[i]]) for i in range(3)])] for p in ROWS3}
WHERE3 = {f: p for p, v in FAMS3.items() for f in v}
PAIRS3, NEVER3 = [], {p: 0 for p in ROWS3}
for _p, _v in FAMS3.items():
    for _f in _v:
        _m = first_meeting3(_f)
        if _m is None:
            NEVER3[_p] += 1
            continue
        _g = swap3(_f, *_m)
        assert _sgn(WHERE3[_g]) == -_sgn(_p) and first_meeting3(_g) == _m and swap3(_g, *_m) == _f
        if _f < _g:
            PAIRS3.append((_f, _g))
assert [len(FAMS3[p]) for p in ROWS3] == [216, 96, 96, 6, 16, 16] and len(PAIRS3) == 198
assert NEVER3 == {p: (50 if p == (0, 1, 2) else 0) for p in ROWS3}
assert sum(_sgn(p) * len(v) for p, v in FAMS3.items()) == 50


def assign_icon(p, w=0.9, h=0.55):
    """Three ant-coloured dots on top, three houses below; a line from each ant to the house it goes to."""
    xs = [-w / 2, 0, w / 2]
    dots = VGroup(*[Dot(np.array([xs[i], h / 2, 0]), radius=0.06, color=COL3[i]) for i in range(3)])
    hs = VGroup(*[house(COL3[i], 0.2).move_to(np.array([xs[i], -h / 2, 0])) for i in range(3)])
    ln = VGroup(*[Line(dots[i].get_center(), hs[p[i]].get_top(), color=COL3[i], stroke_width=3) for i in range(3)])
    return VGroup(ln, dots, hs)


class ThreeProof(DScene):
    def construct(self):
        lat = Lattice(5, spacing=1.0, center=LEFT * 4.3 + DOWN * 0.3)
        ants = VGroup(*[ant(COL3[i], 0.7).move_to(lat.p(*S3[i])) for i in range(3)])
        hs = VGroup(*[house(COL3[i], 0.45).move_to(lat.p(*E3[i])) for i in range(3)])

        # 0: and with three ants?
        self.cue(0)
        self.play(FadeIn(lat), FadeIn(hs), FadeIn(ants, lag_ratio=0.3), run_time=1.2)

        # 1: six terms: one per way of sending the ants to the houses
        self.cue(1)
        table = VGroup()
        cnts = []
        for p in ROWS3:
            sg = _sgn(p)
            vals = [len(all_paths(S3[i], E3[p[i]])) for i in range(3)]
            ic = assign_icon(p)
            s_ = MathTex("+" if sg > 0 else "-", color=GOOD if sg > 0 else BAD).scale(0.9)
            prod = MathTex(r" \cdot ".join(map(str, vals))).scale(0.8)
            eq = MathTex("=").scale(0.8)
            c = MathTex(str(len(FAMS3[p]))).scale(0.85)
            r = VGroup(ic, s_, prod, eq, c).arrange(RIGHT, buff=0.3)
            table.add(r)
            cnts.append(c)
        table.arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(RIGHT * 2.6 + UP * 0.6)
        for r in table[1:]:                                   # line the = signs up
            r[3:].shift(RIGHT * (table[0][3].get_x() - r[3].get_x()))
            r[1:3].shift(RIGHT * (table[0][2].get_right()[0] - r[2].get_right()[0]))
        table.scale(1.2).move_to(RIGHT * 3.2 + UP * 0.35)
        for k, r in enumerate(table):
            if k in (1, 4):
                self.cue_at(1, "two ants" if k == 1 else "circle", lead=0.2)
            self.play(FadeIn(r[0]), run_time=0.35)

        # 2: each term counts the families for that way, with a sign; they add up to 50
        self.cue(2)
        self.play(LaggedStart(*[FadeIn(r[1:]) for r in table], lag_ratio=0.15), run_time=1.6)
        total = MathTex(r"\det A", "=", "50", color=YELLOW).scale(1.2)
        total.next_to(table, DOWN, buff=0.25).align_to(table[0][3], LEFT).shift(LEFT * (total[0].width + 0.25))
        self.cue_at(2, "fifty", lead=0.3)
        self.play(Write(total), run_time=0.8)

        # 3: a family that meets; the first meeting; swap the two tails from there
        self.cue(3)
        f, g = next((f, g) for f, g in PAIRS3 if WHERE3[f] == (0, 1, 2) and WHERE3[g] == (1, 0, 2))
        i, v, j = first_meeting3(f)
        fam = VGroup(*[path_mob(lat, list(f[k]), COL3[k], 6) for k in range(3)])
        box_f = SurroundingRectangle(table[0], color=YELLOW, buff=0.06)
        self.play(Create(fam), Create(box_f), run_time=1.2)
        ring = Circle(radius=0.28, color=MEET, stroke_width=5).move_to(lat.p(*v))
        self.cue_at(3, "first meeting", lead=0.2)
        self.play(Create(ring), run_time=0.5)
        self.cue_at(3, "swap", lead=0.2)
        self.sfx("whoosh")
        fam2 = VGroup(*[path_mob(lat, list(g[k]), COL3[k], 6) for k in range(3)])
        self.play(Transform(fam, fam2), run_time=1.2)

        # 4: it now belongs to a term with the opposite sign; swap again and it comes back: they cancel
        self.cue(4)
        box_g = SurroundingRectangle(table[ROWS3.index(WHERE3[g])], color=YELLOW, buff=0.06)
        arr = CurvedArrow(box_f.get_right() + LEFT * 0.05, box_g.get_right() + LEFT * 0.05, angle=-PI / 2, color=YELLOW)
        self.play(Create(box_g), Create(arr), run_time=0.9)
        self.cue_at(4, "Swap again", lead=0.2)
        self.play(Transform(fam, VGroup(*[path_mob(lat, list(f[k]), COL3[k], 6) for k in range(3)])), run_time=1.0)
        self.cue_at(4, "cancel", lead=0.2)
        self.play(Indicate(VGroup(table[0][1], table[1][1]), color=YELLOW, scale_factor=1.6), run_time=0.8)
        self.play(FadeOut(VGroup(fam, ring, box_f, box_g, arr)), run_time=0.4)

        # 5: every meeting family has a partner: watch them cancel (counters fall)
        self.cue(5)
        left = {p: len(FAMS3[p]) for p in ROWS3}
        order = PAIRS3[:]
        _random.Random(2).shuffle(order)
        batch = 6
        for b0 in range(0, len(order), batch):
            chunk = order[b0:b0 + batch]
            for f_, g_ in chunk:
                left[WHERE3[f_]] -= 1
                left[WHERE3[g_]] -= 1
            f_, g_ = chunk[0]
            show = VGroup(*[path_mob(lat, list(f_[k]), COL3[k], 5) for k in range(3)])
            self.add(show)
            self.play(*[Transform(cnts[k], MathTex(str(left[p]), color=SOFT if left[p] == 0 else WHITE).scale(0.85 * 1.2)
                                  .move_to(cnts[k], aligned_edge=LEFT)) for k, p in enumerate(ROWS3)], run_time=0.13)
            self.remove(show)
        assert left == NEVER3

        # 6: what's left: the families where nobody meets, all going home: 50 = det A
        self.cue(6)
        self.cue_at(6, "fifty of them", lead=0.3)
        good = [f_ for f_ in FAMS3[(0, 1, 2)] if first_meeting3(f_) is None][:1][0]
        gm = VGroup(*[path_mob(lat, list(good[k]), COL3[k], 6) for k in range(3)])
        self.sfx("chime")
        self.play(Create(gm), Indicate(cnts[0], color=GOOD, scale_factor=1.4), run_time=1.0)
        self.cue_at(6, "Exactly the determinant", lead=0.2)
        self.play(Indicate(total, color=YELLOW, scale_factor=1.15), run_time=0.9)
        self.cue_end(6)
        self.wait(0.6)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.6)


class TheTrick(DScene):
    """How a determinant counts: without signs (the permanent) every family is counted; the signs let the
    unwanted ones cancel. Benjamin & Quinn's D.I.E. method: Description, Involution, Exception (wording checked)."""

    def construct(self):
        # 0: so here's how a determinant really counts
        self.cue(0)
        top = T("How a determinant counts", 44, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(top), run_time=1.0)

        # 1: drop the signs: the permanent counts every family (meeting or not)
        self.cue(1)
        perm = MathTex(r"\operatorname{perm} A", "=", r"6 \cdot 6 + 4 \cdot 4", "=", "52").scale(1.05)
        dett = MathTex(r"\det A", "=", r"6 \cdot 6 - 4 \cdot 4", "=", "20").scale(1.05)
        VGroup(perm, dett).arrange(DOWN, buff=0.6).move_to(UP * 0.9)
        dett.shift(RIGHT * (perm[1].get_x() - dett[1].get_x()))
        pl = T("every pair of paths, meeting or not", 26, SOFT).next_to(perm, RIGHT, buff=0.4)
        dl = T("only the pairs that never meet", 26, GOOD).next_to(dett, RIGHT, buff=0.4)
        grp = VGroup(perm, dett, pl, dl)
        grp.scale_to_fit_width(min(grp.width, 13.2)).move_to(UP * 0.9)
        self.play(Write(perm), run_time=1.0)
        self.cue_at(1, "every family", lead=0.2)
        self.play(FadeIn(pl), run_time=0.6)

        # 2: the signs make the difference: the unwanted families cancel
        self.cue(2)
        self.play(Write(dett), run_time=1.0)
        mbox = SurroundingRectangle(dett[2][3], color=YELLOW, buff=0.08)
        self.cue_at(2, "signs", lead=0.2)
        self.play(Create(mbox), FadeIn(dl), run_time=0.8)

        # 3-6: the D.I.E. method (the title makes room)
        self.cue(3)
        self.play(FadeOut(VGroup(grp, mbox, top)), run_time=0.6)
        die = T("D . I . E .", 56, YELLOW, weight=BOLD).to_edge(UP, buff=0.45)
        who = T("Arthur Benjamin & Jennifer Quinn, “A Method to DIE For”", 24, SOFT).next_to(die, DOWN, buff=0.15)
        self.cue_at(3, "D.I.E.", lead=0.2)
        self.play(Write(die), FadeIn(who), run_time=1.0)
        rows = VGroup()
        for word, rule, here, col in [
            ("Description", "what the sum counts, ignoring the signs", "families of paths", INK),
            ("Involution", "a rule that pairs things up:\ndo it twice, and you're back\n(each + object gets a − partner)", "swap the tails at the first meeting", ORANGE),
            ("Exception", "whatever has no partner survives", "the families that never meet", GOOD)]:
            r = VGroup(T(word, 32, col, weight=BOLD), T(rule, 25, line_spacing=1.1), T("here: " + here, 23, SOFT)).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(who, DOWN, buff=0.4)
        rows.set_x(0)
        if rows.get_bottom()[1] < -3.75:
            rows.scale_to_fit_height(rows.height - (-3.75 - rows.get_bottom()[1])).next_to(who, DOWN, buff=0.4).set_x(0)
        for k in range(3):
            self.cue(4 + k)
            self.play(FadeIn(rows[k][0], shift=RIGHT * 0.2), run_time=0.5)
            self.play(FadeIn(rows[k][1]), run_time=0.6)
            if k == 1:                                      # do it twice, you're back: a tiny A ⇄ B
                ab = VGroup(T("A", 34), T("B", 34)).arrange(RIGHT, buff=1.2).move_to(np.array([4.6, rows[1].get_y(), 0]))
                arr = VGroup(CurvedArrow(ab[0].get_top(), ab[1].get_top(), angle=-PI / 2, color=ORANGE),
                             CurvedArrow(ab[1].get_bottom(), ab[0].get_bottom(), angle=-PI / 2, color=ORANGE))
                self.cue_at(5, "Apply it once", lead=0.2)
                self.play(FadeIn(ab), Create(arr[0]), run_time=0.7)
                self.cue_at(5, "apply it again", lead=0.2)
                self.play(Create(arr[1]), run_time=0.7)
            self.cue_at(4 + k, "Here", lead=0.2)
            self.play(FadeIn(rows[k][2]), run_time=0.5)
        self.cue_end(6)
        self.wait(0.6)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.6)
