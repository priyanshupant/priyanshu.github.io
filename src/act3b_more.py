"""v13b — after "the same number as before": nothing special about two ants; then the "why" card.

    ThreeAnts   (name kept) the board grows to 6x6, the blue and orange ants and homes move to scattered places,
                two more ants (purple, pink) join with homes; the 4x4 matrix A (rows = ants, columns = houses) has det 136 = the number of
                ways all four get home without any two meeting (verified by exhaustive search; every other
                pairing of ants to homes is impossible without meeting, so det counts exactly these)
    WhyCard     "Why does this work?" in the centre; back to the two ants
"""
import itertools
import random
from common import *

ANT4 = PINK
COLS = [ANT1, ANT2, ANT3, ANT4]                      # blue, orange, purple, pink (rows and columns in this order)
# first the neat staircase (the old two-ant puzzle shifted by (1, 1), plus two ants either side) ...
G4S = [(1, 2), (2, 1), (0, 3), (3, 0)]
G4E = [(3, 4), (4, 3), (2, 5), (5, 2)]
# ... then everyone moves to layout "U" (7x7): every ant at least 5 steps from home, paths free to cross
S4 = [(3, 3), (1, 1), (2, 4), (1, 3)]
E4 = [(6, 5), (6, 3), (5, 6), (3, 6)]
M4 = [[len(all_paths(s, e)) for e in E4] for s in S4]
DET4 = round(np.linalg.det(np.array(M4, dtype=float)))


def never_meet(starts, ends):
    """All families (one path per ant) in which no two paths share a dot."""
    PS = [all_paths(s, e) for s, e in zip(starts, ends)]
    out = []

    def rec(k, used, fam):
        if k == len(PS):
            out.append(list(fam))
            return
        for P in PS[k]:
            if used.isdisjoint(P):
                rec(k + 1, used | set(P), fam + [P])
    rec(0, set(), [])
    return out


FAM4 = never_meet(S4, E4)
assert DET4 == len(FAM4) == 252, (M4, DET4, len(FAM4))
assert all(abs(s[0] - e[0]) + abs(s[1] - e[1]) >= 5 for s, e in zip(S4, E4))
for perm in itertools.permutations(range(4)):         # LGV here counts exactly: no other pairing can avoid meeting
    if perm != (0, 1, 2, 3):
        assert not never_meet(S4, [E4[i] for i in perm])


class ThreeAnts(DScene):
    def construct(self):
        old = big_lattice()
        ends = board(old)
        a1 = ant(ANT1, 0.9).move_to(old.p(*A1))
        a2 = ant(ANT2, 0.9).move_to(old.p(*A2))
        self.add(old, ends, a1, a2)

        # 0: nothing special about this scenario
        self.cue(0)
        self.wait(0.3)

        # 1: a bigger grid: the old 4x4 slides in as the middle of a 7x7 (shifted by (1, 1))
        self.cue(1)
        lat = Lattice(7, spacing=0.8, center=LEFT * 3.5 + DOWN * 0.3)
        sh = lambda p: (p[0] + 1, p[1] + 1)
        slide = [old.dots[(x, y)].animate.move_to(lat.p(x + 1, y + 1)) for x in range(4) for y in range(4)]
        tgt_ends = VGroup(Dot(lat.p(*sh(A1)), radius=0.09, color=ANT1), Dot(lat.p(*sh(A2)), radius=0.09, color=ANT2),
                          house(ANT1, 0.4).move_to(lat.p(*sh(B1))), house(ANT2, 0.4).move_to(lat.p(*sh(B2))))
        self.play(*slide, Transform(ends, tgt_ends), a1.animate.move_to(lat.p(*sh(A1))).scale(0.62),
                  a2.animate.move_to(lat.p(*sh(A2))).scale(0.62), run_time=1.3)
        extra = VGroup(*[lat.dots[k] for k in lat.dots if not (1 <= k[0] <= 4 and 1 <= k[1] <= 4)])
        self.play(FadeIn(extra, lag_ratio=0.02), run_time=0.8)
        self.remove(old)
        self.add(lat)
        self.bring_to_front(ends, a1, a2)

        # 2: a few more ants with homes of their own, in a neat staircase
        self.cue(2)
        new_ants = []
        houses = [ends[2], ends[3]]
        for k, word in ((2, "hey!"), (3, "hi!")):
            an = ant(COLS[k], 0.56).move_to(lat.p(*G4S[k]))
            sd = Dot(lat.p(*G4S[k]), radius=0.09, color=COLS[k])
            self.sfx("pop")
            self.play(FadeIn(sd), FadeIn(an, shift=DOWN * 0.3), run_time=0.6)
            sp = speech(word, an, UP, size=28)
            self.play(FadeIn(sp, scale=0.6), run_time=0.3)
            h = house(COLS[k], 0.4).move_to(lat.p(*G4E[k]))
            self.sfx("pop")
            self.play(FadeOut(sp), FadeIn(h, scale=1.5), run_time=0.5)
            new_ants.append((an, sd))
            houses.append(h)

        # 3: now move the ants and their homes anywhere (to layout U)
        self.cue(3)
        movers = [(a1, ends[0]), (a2, ends[1])] + new_ants
        self.play(*[m.animate.move_to(lat.p(*S4[k])) for k, (an, sd) in enumerate(movers) for m in (an, sd)],
                  run_time=1.6)
        self.play(*[houses[k].animate.move_to(lat.p(*E4[k])) for k in range(4)], run_time=1.6)
        self.bring_to_front(*[an for an, _ in movers])

        # 4: "in order": if any ants swapped homes, some paths would be forced to meet
        self.cue(4)
        rule = VGroup(T("mix up homes", 30), MathTex(r"\Longrightarrow").scale(1.1), T("paths must meet", 30, BAD)) \
            .arrange(RIGHT, buff=0.3)
        rule.scale_to_fit_width(min(rule.width, 5.4)).move_to(RIGHT * 3.6 + UP * 1.3)
        self.play(FadeIn(rule, lag_ratio=0.3), run_time=1.0)

        # 5: example: blue to the pink home, pink to the blue home; however pink goes, it hits blue's path
        self.cue(5)
        others = VGroup(movers[1][0], movers[1][1], movers[2][0], movers[2][1], houses[1], houses[2])
        self.play(others.animate.set_opacity(0.25), run_time=0.5)
        bp = all_paths(S4[0], E4[3])[0]                        # blue -> pink home: straight up
        arrow1 = CurvedArrow(lat.p(*S4[0]) + RIGHT * 0.2, houses[3].get_center() + RIGHT * 0.3, angle=-PI / 4, color=ANT1)
        arrow2 = CurvedArrow(lat.p(*S4[3]) + DOWN * 0.25, houses[0].get_center() + DOWN * 0.3, angle=PI / 5, color=ANT4)
        self.play(Create(arrow1), Create(arrow2), run_time=1.0)
        self.wait(0.4)
        self.play(FadeOut(arrow1), FadeOut(arrow2), run_time=0.3)
        bm = path_mob(lat, bp, ANT1, 7)
        self.play(Create(bm), run_time=0.9)
        bset = set(map(tuple, bp))
        pinks = all_paths(S4[3], E4[0])
        pick = [pinks[i] for i in (0, len(pinks) // 2, len(pinks) - 1)]
        self.cue_at(5, "However", lead=0.3)
        for k, pp in enumerate(pick):
            pm = path_mob(lat, pp, ANT4, 7)
            hit = next(q for q in pp if tuple(q) in bset)
            self.play(Create(pm), run_time=0.8)
            xx = cross(0.36).move_to(lat.p(*hit))
            self.sfx("buzz")
            self.play(FadeIn(xx, scale=1.5), Flash(lat.p(*hit), color=BAD, flash_radius=0.3), run_time=0.5)
            self.wait(0.3)
            self.play(FadeOut(pm), FadeOut(xx), run_time=0.3)
        self.play(FadeOut(bm), FadeOut(rule), others.animate.set_opacity(1), run_time=0.6)
        self.bring_to_front(*[an for an, _ in movers])

        # 4: the same kind of matrix: rows = ants, columns = houses; each entry counts paths
        self.cue(6)
        M = matrix_mob([[str(v) for v in r] for r in M4], size=38, h_buff=0.75, v_buff=0.5)
        Aeq = T("A  =", 40)
        VGroup(Aeq, M).arrange(RIGHT, buff=0.3).move_to(RIGHT * 3.2 + UP * 1.2)
        cells = M.cells
        for c in cells:
            c.set_opacity(0)
        col_lab = VGroup(*[house(COLS[k], 0.36).next_to(cells[k], UP, buff=0.3) for k in range(4)])
        row_lab = VGroup(*[ant(COLS[k], 0.42).next_to(M, RIGHT, buff=0.25).match_y(cells[4 * k]) for k in range(4)])
        blk = VGroup(Aeq, M, col_lab, row_lab)
        blk.scale_to_fit_width(min(blk.width, 6.6)).move_to(RIGHT * 3.4 + UP * 1.3)
        self.play(FadeIn(Aeq), FadeIn(VGroup(M[0], M[2])), FadeIn(row_lab), FadeIn(col_lab), run_time=0.8)
        self.add(cells)
        self.cue_at(6, "each entry", lead=0.2)
        for k in range(16):
            i, j = divmod(k, 4)
            ring = VGroup(SurroundingRectangle(new_ants[i - 2][0] if i >= 2 else (a1 if i == 0 else a2), color=YELLOW, buff=0.05),
                          SurroundingRectangle(houses[j], color=YELLOW, buff=0.05))
            self.add(ring)
            self.sfx("tick")
            self.play(cells[k].animate.set_opacity(1), run_time=0.22)
            self.remove(ring)

        # 5: its determinant
        self.cue(7)
        x_eq = 1.3                                            # its own = column, clear of the grid
        eq = T("=", 36).move_to(np.array([x_eq, -1.25, 0]))
        row = VGroup(eq, T("det A", 36).next_to(eq, LEFT, buff=0.3), T(str(DET4), 44, YELLOW, weight=BOLD).next_to(eq, RIGHT, buff=0.3))
        self.cue_at(7, "two hundred", lead=0.3)
        self.sfx("chime")
        self.play(Write(row), run_time=0.9)

        # 6: = the number of ways all four get home without ever meeting (a sample flashes by)
        self.cue(8)
        eq2 = T("=", 36).move_to(np.array([x_eq, -2.0, 0]))
        words = T("the number of ways\nthe ants get home\nwithout ever meeting", 28, GOOD, line_spacing=1.1)
        words.next_to(eq2, RIGHT, buff=0.3).align_to(eq2, UP).shift(UP * 0.12)
        rng = random.Random(4)
        sample = rng.sample(FAM4, 24)
        self.cue_at(8, "exactly the number", lead=0.2)
        self.play(FadeIn(eq2), FadeIn(words), run_time=0.8)
        for k, f in enumerate(sample):
            fam = VGroup(*[path_mob(lat, f[i], COLS[i], 5) for i in range(4)])
            if k < 2:
                self.play(Create(fam), run_time=0.8)
                self.wait(0.4)
                self.play(FadeOut(fam), run_time=0.25)
            else:
                self.add(fam)
                self.wait(max(0.1, 0.35 * 0.88 ** (k - 2)))
                self.remove(fam)

        # 7: isn't this simple and beautiful?  8: understanding why is the essence  9: let's get into that
        self.cue(9)
        self.play(Indicate(VGroup(row, eq2, words), color=YELLOW, scale_factor=1.06), run_time=1.0)
        self.cue(10)
        self.cue(11)
        self.cue_end(11)
        self.wait(0.4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


class WhyCard(DScene):
    def construct(self):
        title = T("Why does this work?", 54, weight=BOLD)
        # 0: so, why does this work?
        self.cue(0)
        self.sfx("whoosh")
        self.play(Write(title), run_time=1.2)
        self.wait(0.8)                                         # the card alone, no narration
        self.play(FadeOut(title), run_time=0.6)
