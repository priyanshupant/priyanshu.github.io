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

STEPS = ["swapped  →  meeting", "meeting  →  swapped", "one to one"]


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
        lab = T("couples:", 32, SOFT).move_to(RIGHT * (RX - 0.6) + DOWN * 0.4)
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

        # 5: sixteen of each
        self.cue(5)
        self.sfx("chime")
        self.play(Indicate(VGroup(lab, cnt), color=YELLOW, scale_factor=1.2), run_time=0.9)
        self.cue_end(5)
        self.wait(0.4)
        self.play(FadeOut(VGroup(steps, lab, cnt, mi, si, link)), run_time=0.5)


class Formula(DScene):
    def construct(self):
        lat, ends, a1, a2 = setup(self)
        rows = aligned([("det A", f"{N11} · {N22}  −  {N12} · {N21}", INK),
                        (None, f"({NGOOD} + {NBAD})  −  {N12 * N21}", INK),
                        (None, f"{NGOOD}", YELLOW)], x_eq=RX - 1.7, y0=2.2, dy=0.9, size=38)
        good = next(pq for pq in plus_pairs() if first_meet(*pq) is None)
        bad = MEETS[0]
        sw = swap_tails(*bad)

        # 0: now the formula
        self.cue(0)
        self.play(Write(rows[0]), run_time=1.2)

        # 1: six times six = every pair going home: twenty never meet + sixteen meet
        self.cue(1)
        r0 = rows[0][1]
        b66 = SurroundingRectangle(r0[0:3], color=YELLOW, buff=0.1, corner_radius=0.08)
        self.play(Create(b66), run_time=0.6)
        self.cue_at(1, "twenty", lead=0.2)
        g = pair(lat, *good)
        tk = tick(0.5, GOOD).move_to(RIGHT * (RX + 2.4) + DOWN * 0.4)
        self.play(Create(g), run_time=1.0)
        self.play(FadeIn(tk), run_time=0.3)
        self.cue_at(1, "sixteen", lead=0.2)
        b = pair(lat, *bad)
        rg = Circle(radius=0.32, color=MEET, stroke_width=5).move_to(lat.p(*first_meet(*bad)))
        self.play(FadeOut(g), FadeOut(tk), Create(b), run_time=1.0)
        self.play(Create(rg), run_time=0.4)
        r1 = rows[1]
        self.play(Write(VGroup(r1[0], r1[1][0:7])), run_time=1.0)          # "= (20 + 16)"
        self.play(FadeOut(b66), run_time=0.3)

        # 2: four times four = the sixteen swapped pairs
        self.cue(2)
        b44 = SurroundingRectangle(r0[-3:], color=ORANGE, buff=0.1, corner_radius=0.08)
        self.play(Create(b44), run_time=0.6)
        self.sfx("whoosh")
        self.play(Transform(b, pair(lat, *sw)), FadeOut(rg), run_time=1.2)
        self.play(Indicate(ends[3], color=ANT1, scale_factor=1.4), Indicate(ends[2], color=ANT2, scale_factor=1.4), run_time=0.8)
        self.play(Write(r1[1][7:]), FadeOut(b44), run_time=0.8)          # "− 16"

        # 3: they cancel the meeting pairs exactly
        self.cue(3)
        t = r1[1]
        s1 = Line(t[4].get_corner(DL), t[5].get_corner(UR), color=BAD, stroke_width=5)
        s2 = Line(t[-2].get_corner(DL), t[-1].get_corner(UR), color=BAD, stroke_width=5)
        arc = CurvedArrow(t[5].get_bottom() + DOWN * 0.1, t[-2].get_bottom() + DOWN * 0.1, angle=PI / 3, color=YELLOW)
        self.play(Create(arc), FadeOut(b), run_time=0.9)
        self.sfx("tick")
        self.play(Create(s1), Create(s2), run_time=0.8)

        # 4: twenty (one of the twenty that never meet, glowing on the grid)
        self.cue(4)
        self.sfx("chime")
        self.play(Write(rows[2]), FadeOut(arc), run_time=0.8)
        g2 = pair(lat, *good)
        self.play(Create(g2), run_time=1.0)

        # 5: a bijective proof
        self.cue(5)
        qed = Square(0.3, color=INK, fill_opacity=1).next_to(rows[2], RIGHT, buff=0.5)
        self.play(FadeIn(qed, scale=0.5), run_time=0.4)
        self.cue_end(5)
        self.wait(0.6)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.6)


class AllPairs(DScene):
    """Before the proof: the 36 pairs going home (20 never meet + 16 meet) and the 16 swapped pairs;
    the minus sign must cancel 16 against 16, so they must match up — let's see how."""

    def construct(self):
        own, sw = plus_pairs(), minus_pairs()
        left = VGroup(*[pair_icon(p, q, size=0.44, meet=False) for p, q in own]).arrange_in_grid(6, 6, buff=0.06)
        right = VGroup(*[pair_icon(p, q, size=0.44, meet=False) for p, q in sw]).arrange_in_grid(4, 4, buff=0.06)
        left.move_to(UP * 0.35).to_edge(LEFT, buff=0.45)
        right.next_to(left, RIGHT, buff=0.55).align_to(left, DOWN)
        rows = aligned([("det A", f"{N11} · {N22}  −  {N12} · {N21}", INK),
                        (None, f"({NGOOD} + {NBAD})  −  {N12 * N21}", INK)], x_eq=right.get_right()[0] + 2.4, y0=2.4, dy=0.8, size=32)

        # 0: six times six counts all thirty-six pairs going home
        self.cue(0)
        self.play(Write(rows[0]), run_time=1.0)
        r0 = rows[0][1]
        b66 = SurroundingRectangle(r0[0:3], color=YELLOW, buff=0.08, corner_radius=0.08)
        self.cue_at(0, "Six times six", lead=0.2)
        self.play(Create(b66), LaggedStartMap(FadeIn, left, lag_ratio=0.03), run_time=2.0)
        l36 = T("36 pairs going home", 26, YELLOW).next_to(left, DOWN, buff=0.15)
        self.play(FadeIn(l36), run_time=0.5)

        # 1: twenty never meet, sixteen do
        self.cue(1)
        cols = [BAD if first_meet(*pq) is not None else GOOD for pq in own]
        self.cue_at(1, "Twenty", lead=0.2)
        self.play(*[ic[0].animate.set_stroke(c, 2.5) for ic, c in zip(left, cols) if c == GOOD], run_time=0.9)
        self.cue_at(1, "Sixteen", lead=0.2)
        self.play(*[ic[0].animate.set_stroke(c, 2.5) for ic, c in zip(left, cols) if c == BAD], run_time=0.9)
        split = VGroup(T(f"{NGOOD} never meet", 26, GOOD), T("+", 26), T(f"{NBAD} meet", 26, BAD)).arrange(RIGHT, buff=0.15)
        split.next_to(l36, DOWN, buff=0.12)
        if split.width > left.width:
            split.scale_to_fit_width(left.width)
        split.set_x(left.get_x())
        r1 = rows[1]
        self.play(FadeIn(split), Write(VGroup(r1[0], r1[1][0:7])), FadeOut(b66), run_time=1.0)

        # 2: four times four counts the swapped pairs: also sixteen
        self.cue(2)
        b44 = SurroundingRectangle(r0[-3:], color=ORANGE, buff=0.08, corner_radius=0.08)
        self.play(Create(b44), LaggedStartMap(FadeIn, right, lag_ratio=0.05), run_time=1.6)
        for ic in right:
            ic[0].set_stroke(ORANGE, 2.5)
        l16 = T(f"{N12 * N21} swapped", 26, ORANGE).next_to(right, DOWN, buff=0.15)
        self.play(FadeIn(l16), Write(r1[1][7:]), FadeOut(b44), run_time=0.8)

        # 3: the minus sign must cancel the sixteen meeting pairs against the sixteen swapped ones
        self.cue(3)
        t = r1[1]
        arc = CurvedArrow(t[5].get_bottom() + DOWN * 0.1, t[-2].get_bottom() + DOWN * 0.1, angle=PI / 3, color=YELLOW)
        self.play(Create(arc), Indicate(split[2], color=BAD, scale_factor=1.3), Indicate(l16, color=ORANGE, scale_factor=1.3),
                  run_time=1.2)

        # 4: so they must match up, one to one. Let's see how.
        self.cue(4)
        reds = VGroup(*[ic for ic, c in zip(left, cols) if c == BAD])
        link = CurvedArrow(reds.get_top() + UP * 0.1, right.get_top() + UP * 0.1, angle=-PI / 4, color=YELLOW)
        qm = T("?", 40, YELLOW).next_to(link, UP, buff=0.05)
        self.play(Indicate(reds, color=BAD, scale_factor=1.06), run_time=0.8)
        self.play(Create(link), FadeIn(qm), run_time=0.9)
        self.cue_end(4)
        self.wait(0.6)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.6)
