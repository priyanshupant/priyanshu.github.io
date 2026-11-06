"""v12 — after "which is twenty": nothing special about two ants; then the "why" card.

    ThreeAnts   the board grows to 5x5, a third (purple) ant and house join; the 3x3 matrix A
                (rows = ants, columns = houses) has det 50 = the triples that never meet (of 216)
    WhyCard     "Why does this work?" in the centre; back to the two ants
Same style as the puzzle: one board, symbols only, right-hand side for the maths, '=' aligned.
"""
from itertools import product
from common import *

S3 = [(0, 2), (1, 1), (2, 0)]          # the two-ant puzzle shifted up one row, plus a purple ant
E3 = [(2, 4), (3, 3), (4, 2)]
COLS = [ANT1, ANT2, ANT3]
M3 = [[len(all_paths(s, e)) for e in E3] for s in S3]
FAMS = list(product(*[all_paths(s, e) for s, e in zip(S3, E3)]))


def disjoint(f):
    return all(not (set(f[i]) & set(f[j])) for i in range(3) for j in range(i + 1, 3))


NEVER = sum(1 for f in FAMS if disjoint(f))
DET3 = round(np.linalg.det(np.array(M3, dtype=float)))
assert M3 == [[6, 4, 1], [4, 6, 4], [1, 4, 6]] and DET3 == NEVER == 50 and len(FAMS) == 216


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

        # 1: a bigger grid, and a third ant with a house of its own
        self.cue(1)
        lat = Lattice(5, spacing=1.18, center=LEFT * 3.5 + DOWN * 0.25)
        moved = {(x, y): (x, y + 1) for x in range(4) for y in range(4)}      # old dot -> its place on the new grid
        new_ends = VGroup(Dot(lat.p(*S3[0]), radius=0.11, color=ANT1), Dot(lat.p(*S3[1]), radius=0.11, color=ANT2),
                          house(ANT1, 0.5).move_to(lat.p(*E3[0])), house(ANT2, 0.5).move_to(lat.p(*E3[1])))
        self.cue_at(1, "bigger", lead=0.2)
        # every old dot slides to its place on the bigger grid; the new row and column fade in
        slide = [old.dots[(x, y)].animate.move_to(lat.p(x, y + 1)) for x in range(4) for y in range(4)]
        extra = VGroup(*[lat.dots[k] for k in lat.dots if not (k[0] <= 3 and 1 <= k[1] <= 4)])
        self.play(*slide, Transform(ends, new_ends), a1.animate.move_to(lat.p(*S3[0])).scale(0.85),
                  a2.animate.move_to(lat.p(*S3[1])).scale(0.85), run_time=1.2)
        self.play(FadeIn(extra, lag_ratio=0.05), run_time=0.6)
        self.remove(old)
        self.add(lat)
        self.bring_to_front(ends, a1, a2)
        a3 = ant(ANT3, 0.77).move_to(lat.p(*S3[2]))
        h3 = house(ANT3, 0.5).move_to(lat.p(*E3[2]))
        s3 = Dot(lat.p(*S3[2]), radius=0.11, color=ANT3)
        self.cue_at(1, "third ant", lead=0.2)
        self.sfx("pop")
        self.play(FadeIn(s3), FadeIn(a3, shift=DOWN * 0.3), run_time=0.6)
        hey = speech("hey!", a3, UP, size=34)
        self.play(FadeIn(hey, scale=0.6), run_time=0.3)
        self.cue_at(1, "house of its own", lead=0.2)
        self.sfx("pop")
        self.play(FadeIn(h3, scale=1.5), FadeOut(hey), run_time=0.6)
        ants = [a1, a2, a3]

        # 2: the same kind of matrix: rows are the ants, columns the houses
        self.cue(2)
        M = matrix_mob([[str(v) for v in r] for r in M3], size=46, h_buff=0.8, v_buff=0.55)
        Aeq = T("A  =", 44)
        VGroup(Aeq, M).arrange(RIGHT, buff=0.3).move_to(RIGHT * 3.4 + UP * 1.2)
        cells = M.cells
        for c in cells:
            c.set_opacity(0)
        col_lab = VGroup(*[house(COLS[k], 0.42).next_to(cells[k], UP, buff=0.4) for k in range(3)])
        row_lab = VGroup(*[ant(COLS[k], 0.5).next_to(M, RIGHT, buff=0.3).match_y(cells[3 * k]) for k in range(3)])
        self.play(FadeIn(Aeq), FadeIn(VGroup(M[0], M[2])), FadeIn(row_lab), FadeIn(col_lab), run_time=0.8)
        self.add(cells)
        self.cue_at(2, "each entry", lead=0.2)
        for k in range(9):
            self.sfx("tick")
            self.play(cells[k].animate.set_opacity(1), run_time=0.22)

        # 3: its determinant is fifty
        self.cue(3)
        x_eq = Aeq[-1].get_x()
        eq = T("=", 38).move_to(np.array([x_eq, -1.1, 0]))
        row = VGroup(eq, T("det A", 38).next_to(eq, LEFT, buff=0.3), T(str(DET3), 46, YELLOW, weight=BOLD).next_to(eq, RIGHT, buff=0.3))
        self.cue_at(3, "fifty", lead=0.3)
        self.sfx("chime")
        self.play(Write(row), run_time=0.8)

        # 4: exactly the number of ways all three get home without their paths intersecting
        self.cue(4)
        lab = T("never meet:", 30, GOOD).move_to(RIGHT * 2.6 + DOWN * 2.3)
        cnt = T("0", 36, GOOD).next_to(lab, RIGHT, buff=0.3)
        self.cue_at(4, "exactly the number", lead=0.2)
        self.play(FadeIn(lab), FadeIn(cnt), run_time=0.4)
        n = 0
        for k, f in enumerate(FAMS):
            fam = VGroup(*[path_mob(lat, f[i], COLS[i], 5).set_stroke(opacity=0.75 if k >= 3 else 1) for i in range(3)])
            if disjoint(f):
                n += 1
            c2 = T(str(n), 36, GOOD).move_to(cnt, aligned_edge=LEFT)
            if k < 3:
                self.play(Create(fam), run_time=0.5)
                self.play(Transform(cnt, c2), run_time=0.2)
                self.play(FadeOut(fam), run_time=0.2)
            else:
                self.add(fam)
                self.play(Transform(cnt, c2), run_time=1 / 30)
                self.remove(fam)
        assert n == 50
        self.play(Indicate(VGroup(row, lab, cnt), color=YELLOW, scale_factor=1.1), run_time=0.8)
        self.cue_end(4)
        self.wait(0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


class WhyCard(DScene):
    def construct(self):
        title = T("Why does this work?", 54, weight=BOLD)
        # 0: so, why does this work?
        self.cue(0)
        self.sfx("whoosh")
        self.play(Write(title), run_time=1.2)
        # 1: back to our two ants
        self.cue(1)
        self.cue_end(1)
        self.play(FadeOut(title), run_time=0.6)
