"""Act 4 (v12) — why the determinant counts, on the puzzle's own board.

Priyanshu's style: one continuous grid (same size as the puzzle), ants + houses, no letters;
short bullets on the right as each step is said; everything else spoken; first examples slow,
then "and so on"; equations with each '=' under the one above.

    SwapPaths      a meeting pair: walk the blue path to the first shared dot; swap the tails
    SwapTwice      swapping again puts everything back (an involution) -> perfect couples
    DiagonalSweep  every swapped pair must meet: the column gap goes -1 -> +1 in steps of <= 1
    PutTogether    match all 16 meeting pairs with the 16 swapped pairs; det A = (20 + 16) - 16 = 20
"""
from common import *

P = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]   # blue, a pair that meets...
Q = [(1, 0), (1, 1), (1, 2), (2, 2), (3, 2)]   # ...with orange; first shared dot (1, 2)
M = first_meet(P, Q)
P_SW, Q_SW = swap_tails(P, Q)                  # blue now ends at the orange house, and vice versa
N11, N12 = len(all_paths(A1, B1)), len(all_paths(A1, B2))
N21, N22 = len(all_paths(A2, B1)), len(all_paths(A2, B2))
NBAD = sum(1 for p, q in plus_pairs() if first_meet(p, q) is not None)
NGOOD = N11 * N22 - NBAD
assert (N11, N12, N21, N22, NBAD, NGOOD) == (6, 4, 4, 6, 16, 20)

RX = 3.1   # x-centre of the right-hand side


def bullet_list(texts):
    g = VGroup(*[T("•  " + t, 30) for t in texts]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    g.to_edge(UP, buff=0.45)
    g.set_x(RX)
    g.align_to(np.array([RX - 2.7, 0, 0]), LEFT)
    return g


def turn(a, target):
    delta = (target - a.heading + PI) % TAU - PI
    a.heading = target
    return Rotate(a, delta, about_point=a.get_center(), run_time=0.15)


def walk(scene, lat, a, pts, col=None, step=0.4, trace=False):
    """Walk an ant along pts (turn, then move — never both in one play)."""
    segs = VGroup()
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        scene.play(turn(a, np.arctan2(y1 - y0, x1 - x0)))
        anims = [a.animate.move_to(lat.p(x1, y1))]
        if trace:
            s = Line(lat.p(x0, y0), lat.p(x1, y1), color=col, stroke_width=7)
            segs.add(s)
            anims.append(Create(s))
        scene.sfx("step")
        scene.play(*anims, run_time=step)
    return segs


def setup(scene, at1=A1, at2=A2):
    lat = big_lattice()
    ends = board(lat)
    a1 = ant(ANT1, 0.9).move_to(lat.p(*at1))
    a2 = ant(ANT2, 0.9).move_to(lat.p(*at2))
    scene.add(lat, ends, a1, a2)
    return lat, ends, a1, a2


def aligned(rows, x_eq, y0, dy=0.75, size=34):
    """rows: [(lhs or None, rhs, colour)] -> VGroup of [eq, rhs, (lhs)] with every '=' at x_eq."""
    out = VGroup()
    for i, (lhs, rhs, col) in enumerate(rows):
        eq = T("=", size).move_to(np.array([x_eq, y0 - dy * i, 0]))
        r = T(rhs, size, col).next_to(eq, RIGHT, buff=0.3)
        g = VGroup(eq, r)
        if lhs:
            g.add(T(lhs, size).next_to(eq, LEFT, buff=0.3))
        out.add(g)
    return out


class SwapPaths(DScene):
    def construct(self):
        lat, ends, a1, a2 = setup(self)
        steps = bullet_list(["walk to the first shared dot", "swap the tails"])
        pm, qm = path_mob(lat, P, ANT1, 6).set_stroke(opacity=0.55), path_mob(lat, Q, ANT2, 6).set_stroke(opacity=0.55)

        # 0: take a pair that meets
        self.cue(0)
        self.play(Create(pm), Create(qm), run_time=1.2)

        # 1: the blue ant walks its path and stops at the first dot the orange path also visits
        self.cue(1)
        self.cue_at(1, "Walk along", lead=0.2)
        self.play(FadeIn(steps[0], shift=LEFT * 0.2), run_time=0.5)
        i = P.index(M)
        for k in range(i):
            walk(self, lat, a1, P[k:k + 2], step=0.5)
            if P[k + 1] != M:
                self.play(Flash(a1.get_center(), color=GREY_B, line_length=0.15, flash_radius=0.3), run_time=0.3)
        ring = Circle(radius=0.42, color=MEET, stroke_width=6).move_to(lat.p(*M))
        self.sfx("alert")
        self.play(Create(ring), run_time=0.5)

        # 2: from that dot on, swap the tails
        self.cue(2)
        j = Q.index(M)
        headP, tailP = path_mob(lat, P[:i + 1], ANT1, 7), path_mob(lat, P[i:], ANT1, 7)
        headQ, tailQ = path_mob(lat, Q[:j + 1], ANT2, 7), path_mob(lat, Q[j:], ANT2, 7)
        self.play(FadeOut(pm), FadeOut(qm), FadeIn(VGroup(headP, tailP, headQ, tailQ)), run_time=0.5)
        self.cue_at(2, "swap their tails", lead=0.2)
        self.play(FadeIn(steps[1], shift=LEFT * 0.2), run_time=0.5)
        newP, newQ = path_mob(lat, Q[j:], ANT1, 7), path_mob(lat, P[i:], ANT2, 7)
        self.sfx("whoosh")
        self.play(Transform(tailP, newP), Transform(tailQ, newQ), run_time=1.4)
        # the ants follow their new paths home: blue goes on along the old orange tail…
        self.cue_at(2, "keeps its start", lead=0.2)
        walk(self, lat, a1, Q[j:], step=0.45)
        # …and orange walks its head to the shared dot, then the old blue tail
        walk(self, lat, a2, Q[:j + 1] + P[i + 1:], step=0.4)

        # 3: each ends at the other's house (standing just in front of it, so the house stays visible)
        self.play(a1.animate.shift(DOWN * 0.5), a2.animate.shift(DOWN * 0.5), run_time=0.3)
        self.cue(3)
        h1, h2 = ends[2], ends[3]
        self.cue_at(3, "other's house", lead=0.2)
        self.sfx("chime")
        self.play(Indicate(h2, color=ANT1, scale_factor=1.4), Indicate(h1, color=ANT2, scale_factor=1.4), run_time=1.0)
        self.cue_end(3)
        self.wait(0.4)


class SwapTwice(DScene):
    def construct(self):
        lat, ends, a1, a2 = setup(self, at1=B2, at2=B1)
        a1.shift(DOWN * 0.5); a2.shift(DOWN * 0.5)
        a1.heading = a2.heading = 0
        steps = bullet_list(["walk to the first shared dot", "swap the tails", "swap twice = no change"])
        self.add(steps[0], steps[1])
        i, j = P.index(M), Q.index(M)
        headP, tailP = path_mob(lat, P[:i + 1], ANT1, 7), path_mob(lat, Q[j:], ANT1, 7)
        headQ, tailQ = path_mob(lat, Q[:j + 1], ANT2, 7), path_mob(lat, P[i:], ANT2, 7)
        ring = Circle(radius=0.42, color=MEET, stroke_width=6).move_to(lat.p(*M))
        self.add(headP, tailP, headQ, tailQ, ring)
        self.bring_to_front(a1, a2)

        # 0: and the swap undoes itself
        self.cue(0)
        self.play(Indicate(ring, color=MEET, scale_factor=1.25), run_time=0.8)

        # 1: nothing before the dot changed -> same first shared dot -> swap back
        self.cue(1)
        self.cue_at(1, "Nothing before", lead=0.2)
        glow = VGroup(path_mob(lat, P[:i + 1], ANT1, 18).set_stroke(opacity=0.25),
                      path_mob(lat, Q[:j + 1], ANT2, 18).set_stroke(opacity=0.25))
        self.play(FadeIn(glow), run_time=0.6)
        self.cue_at(1, "swapping there again", lead=0.2)
        self.sfx("whoosh")
        self.play(Transform(tailP, path_mob(lat, P[i:], ANT1, 7)), Transform(tailQ, path_mob(lat, Q[j:], ANT2, 7)),
                  a1.animate(path_arc=PI / 2).move_to(lat.p(*B1) + DOWN * 0.5), a2.animate(path_arc=PI / 2).move_to(lat.p(*B2) + DOWN * 0.5),
                  run_time=1.4)
        self.play(FadeOut(glow), run_time=0.4)

        # 2: twice = nothing happened: an involution (like most committee meetings)
        self.cue(2)
        self.cue_at(2, "Do it twice", lead=0.2)
        self.play(FadeIn(steps[2], shift=LEFT * 0.2), run_time=0.5)

        # 3: so meeting pairs and swapped pairs come in perfect couples
        self.cue(3)
        meet_ic = pair_icon(P, Q, size=1.1)
        swap_ic = pair_icon(P_SW, Q_SW, size=1.1)
        meet_ic[0].set_stroke(BAD, 3)
        swap_ic[0].set_stroke(ORANGE, 3)
        VGroup(meet_ic, swap_ic).arrange(RIGHT, buff=1.6).move_to(RIGHT * RX + DOWN * 0.9)
        top = CurvedArrow(meet_ic.get_top() + UP * 0.1, swap_ic.get_top() + UP * 0.1, angle=-PI / 3, color=YELLOW)
        bot = CurvedArrow(swap_ic.get_bottom() + DOWN * 0.1, meet_ic.get_bottom() + DOWN * 0.1, angle=-PI / 3, color=YELLOW)
        self.cue_at(3, "perfect couples", lead=0.3)
        self.play(FadeIn(meet_ic), FadeIn(swap_ic), run_time=0.6)
        self.play(Create(top), Create(bot), run_time=0.8)
        self.cue_end(3)
        self.wait(0.4)
        self.play(FadeOut(VGroup(steps, meet_ic, swap_ic, top, bot)), run_time=0.5)


class DiagonalSweep(DScene):
    def construct(self):
        lat, ends, a1, a2 = setup(self)
        pm, qm = path_mob(lat, P_SW, ANT1, 7), path_mob(lat, Q_SW, ANT2, 7)
        gaps = [p[0] - q[0] for p, q in zip(P_SW, Q_SW)]                 # blue column − orange column
        assert gaps[0] == -1 and gaps[-1] == 1 and all(abs(b - a) <= 1 for a, b in zip(gaps, gaps[1:]))
        z = gaps.index(0)

        # 0: could a swapped pair avoid meeting?
        self.cue(0)
        self.play(Create(pm), Create(qm), run_time=1.2)

        # 1: sweep a diagonal; on each diagonal each ant stands on exactly one dot
        self.cue(1)
        d = 1.45 * 4.3
        def diag(s):
            c = (lat.p(0, s) + lat.p(s, 0)) / 2
            return DashedLine(c + np.array([-1, 1, 0]) * d / 2.8, c + np.array([1, -1, 0]) * d / 2.8, color=SOFT, stroke_width=3)
        line = diag(1)
        mk1, mk2 = Dot(lat.p(*P_SW[0]), radius=0.15, color=ANT1), Dot(lat.p(*Q_SW[0]), radius=0.15, color=ANT2)
        self.cue_at(1, "Sweep a diagonal", lead=0.2)
        self.play(Create(line), FadeIn(mk1), FadeIn(mk2), run_time=0.6)
        for s in range(2, 6):
            self.sfx("tick")
            self.play(Transform(line, diag(s)), mk1.animate.move_to(lat.p(*P_SW[s - 1])), mk2.animate.move_to(lat.p(*Q_SW[s - 1])),
                      run_time=0.55)
        self.play(Transform(line, diag(1)), mk1.animate.move_to(lat.p(*P_SW[0])), mk2.animate.move_to(lat.p(*Q_SW[0])),
                  run_time=0.6)

        # 2-4: the gap between their columns: −1 at the start, +1 at the end, steps of at most one
        lab = T("gap:", 32, SOFT).move_to(RIGHT * (RX - 2.2) + UP * 1.6)
        slots = [RIGHT * (RX - 1.1 + 0.95 * k) + UP * 1.6 for k in range(5)]
        vals = [T(f"{g:+d}" if g else "0", 34, ANT1 if g > 0 else ANT2 if g < 0 else YELLOW).move_to(slots[k])
                for k, g in enumerate(gaps)]
        qs = [T("?", 34, DIM).move_to(slots[k]) for k in range(5)]
        self.cue(2)
        self.cue_at(2, "Track the gap", lead=0.2)
        self.play(FadeIn(lab), *[FadeIn(q_) for q_ in qs], run_time=0.6)
        self.cue_at(2, "one column to the left", lead=0.2)
        self.play(Transform(qs[0], vals[0]), Indicate(VGroup(mk1, mk2), scale_factor=1.4), run_time=0.6)
        self.cue(3)
        self.play(Transform(line, diag(5)), mk1.animate.move_to(lat.p(*P_SW[-1])), mk2.animate.move_to(lat.p(*Q_SW[-1])),
                  run_time=0.8)
        self.play(Transform(qs[-1], vals[-1]), run_time=0.5)
        self.cue(4)
        for k in range(1, 4):
            self.play(Transform(line, diag(k + 1)), mk1.animate.move_to(lat.p(*P_SW[k])), mk2.animate.move_to(lat.p(*Q_SW[k])),
                      run_time=0.5)
            self.sfx("tick")
            self.play(Transform(qs[k], vals[k]), run_time=0.35)

        # 5: so somewhere it is zero: they share a dot
        self.cue(5)
        self.play(Transform(line, diag(z + 1)), mk1.animate.move_to(lat.p(*P_SW[z])), mk2.animate.move_to(lat.p(*Q_SW[z])),
                  run_time=0.6)
        ring = Circle(radius=0.42, color=MEET, stroke_width=6).move_to(lat.p(*P_SW[z]))
        self.cue_at(5, "they share a dot", lead=0.2)
        self.sfx("chime")
        self.play(Create(ring), Indicate(qs[z], color=YELLOW, scale_factor=1.5), run_time=0.7)
        self.cue_end(5)
        self.wait(0.4)
        self.play(FadeOut(VGroup(pm, qm, line, mk1, mk2, ring, lab, *qs)), run_time=0.5)


class PutTogether(DScene):
    def construct(self):
        lat, ends, a1, a2 = setup(self)
        meet = [pq for pq in plus_pairs() if first_meet(*pq) is not None]
        assert len(meet) == NBAD
        lab = T("couples found:", 30, SOFT).move_to(RIGHT * (RX - 0.4) + UP * 2.6)
        cnt = T("0", 36, YELLOW).next_to(lab, RIGHT, buff=0.3)

        # 0: every meeting pair has exactly one swapped partner (first two slowly, then the rest fast)
        self.cue(0)
        self.play(FadeIn(lab), FadeIn(cnt), run_time=0.5)
        for k, (p, q) in enumerate(meet):
            m = first_meet(p, q)
            ps, qs_ = swap_tails(p, q)
            a = VGroup(path_mob(lat, p, ANT1, 6), path_mob(lat, q, ANT2, 6))
            b = VGroup(path_mob(lat, ps, ANT1, 6), path_mob(lat, qs_, ANT2, 6))
            ring = Circle(radius=0.3, color=MEET, stroke_width=5).move_to(lat.p(*m))
            c2 = T(str(k + 1), 36, YELLOW).move_to(cnt, aligned_edge=LEFT)
            if k < 2:
                self.play(Create(a), Create(ring), run_time=0.7)
                self.sfx("whoosh")
                self.play(Transform(a, b), run_time=0.8)
                self.sfx("pop")
                self.play(Transform(cnt, c2), run_time=0.3)
                self.wait(0.3)
                self.play(FadeOut(a), FadeOut(ring), run_time=0.3)
            else:
                dt = max(0.12, 0.35 * 0.85 ** (k - 2))
                self.add(a, ring)
                self.play(Transform(a, b), Transform(cnt, c2), run_time=dt)
                self.remove(a, ring)

        # 1: in the determinant they cancel
        rows = aligned([("det A", f"{N11} · {N22}  −  {N12} · {N21}", INK),
                        (None, f"({NGOOD} + {NBAD})  −  {N12 * N21}", INK),
                        (None, f"{NGOOD}", YELLOW)], x_eq=RX - 1.2, y0=1.0)
        self.cue(1)
        self.play(Write(rows[0]), run_time=1.0)
        self.cue_at(1, "they cancel", lead=0.2)
        self.play(Write(rows[1]), run_time=1.0)
        r = rows[1][1]
        s1 = Line(r[4].get_corner(DL), r[5].get_corner(UR), color=BAD, stroke_width=4)   # the 16 inside the bracket
        s2 = Line(r[-2].get_corner(DL), r[-1].get_corner(UR), color=BAD, stroke_width=4)  # the 16 being subtracted
        self.cue_at(1, "exact copy", lead=0.2)
        self.sfx("tick")
        self.play(Create(s1), Create(s2), run_time=0.6)

        # 2: what survives: the twenty that never meet
        self.cue(2)
        self.sfx("chime")
        self.play(Write(rows[2]), run_time=0.8)

        # 3: a bijective proof
        self.cue(3)
        qed = Square(0.3, color=INK, fill_opacity=1).next_to(rows[2], RIGHT, buff=0.5)
        self.play(FadeIn(qed, scale=0.5), run_time=0.4)
        self.cue_end(3)
        self.wait(0.6)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.6)
