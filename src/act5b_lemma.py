"""Act 5 (v13) — the general lemma, in Priyanshu's style.

    LemmaCard      "The general lemma" in the centre
    BookQuote      Aigner & Ziegler, Proofs from THE BOOK ("…once in their lifetime, is a Lemma…")
    LGVNames       Lindström (1973), Gessel & Viennot (1985) — name cards (no freely licensed photos exist)
    GeneralLemma   any one-way network; starts a1..an, ends b1..bn; M_ij = #paths a_i -> b_j;
                   det M = number of non-touching families a_i -> b_i (when crossed pairings must touch)
"""
from itertools import permutations, product
from common import *

# ---- a general-looking one-way network: a jittered 5 x 4 grid, edges only right / up / up-right (planar)
import random
_rng = random.Random(120)
COLS, ROWS = 5, 4
NODES = [(c, r) for c in range(COLS) for r in range(ROWS)]
EDGES = []
for c, r in NODES:
    for dc, dr, pr in [(1, 0, 0.75), (0, 1, 0.7), (1, 1, 0.3)]:
        if c + dc < COLS and r + dr < ROWS and _rng.random() < pr:
            EDGES.append(((c, r), (c + dc, r + dr)))
SRC = [(0, 2), (0, 1), (0, 0)]          # a1, a2, a3 down the left side
SNK = [(2, 3), (3, 3), (4, 3)]          # b1, b2, b3 along the top
OUT = {v: [b for a, b in EDGES if a == v] for v in NODES}


def gpaths(a, b):
    if a == b:
        return [[a]]
    return [[a] + p for n in OUT[a] for p in gpaths(n, b)]


MG = [[len(gpaths(a, b)) for b in SNK] for a in SRC]
DETG = round(np.linalg.det(np.array(MG, dtype=float)))


def disjoint(fam):
    return all(not (set(fam[i]) & set(fam[j])) for i in range(len(fam)) for j in range(i + 1, len(fam)))


NT = {s: sum(1 for f in product(*[gpaths(SRC[i], SNK[s[i]]) for i in range(3)]) if disjoint(f))
      for s in permutations(range(3))}
assert all(NT[s] == 0 for s in NT if s != (0, 1, 2)), NT      # only the straight pairing can avoid touching
assert DETG == NT[(0, 1, 2)] == 13 and MG == [[3, 4, 2], [7, 11, 9], [8, 13, 14]], (MG, DETG, NT)
GOODFAM = next(f for f in product(*[gpaths(SRC[i], SNK[i]) for i in range(3)]) if disjoint(f))


class LemmaCard(DScene):
    def construct(self):
        t = T("The general lemma", 54, weight=BOLD)
        self.cue(0)
        self.sfx("whoosh")
        self.play(Write(t), run_time=1.2)
        self.cue_end(0)
        self.wait(0.6)
        self.play(FadeOut(t), run_time=0.6)


QUOTE = ("“The essence of mathematics is proving theorems —\n"
         "and so, that is what mathematicians do: they prove theorems.\n"
         "But to tell the truth, what they really want to prove,\n"
         "once in their lifetime, is a Lemma…”")


class BookQuote(DScene):
    def construct(self):
        q = T(QUOTE, 30, line_spacing=1.35).move_to(UP * 0.6)
        q.scale_to_fit_width(min(q.width, 12.4))
        who = T("Martin Aigner & Günter M. Ziegler, Proofs from THE BOOK", 26, SOFT).next_to(q, DOWN, buff=0.6)
        # 0-1: the quote, read slowly
        self.cue(0)
        self.play(FadeIn(q[:sum(len(l.replace(' ', '')) for l in QUOTE.split('\n')[:2])], lag_ratio=0.02), run_time=2.0)
        self.cue(1)
        self.play(FadeIn(q[sum(len(l.replace(' ', '')) for l in QUOTE.split('\n')[:2]):], lag_ratio=0.02), run_time=2.0)
        self.play(FadeIn(who), run_time=0.6)
        # 2: and this is one of them
        self.cue(2)
        self.cue_end(2)
        self.wait(0.5)
        self.play(FadeOut(q), FadeOut(who), run_time=0.6)


def name_card(name, year, line, col=YELLOW):
    box = RoundedRectangle(width=3.6, height=2.3, corner_radius=0.2, stroke_color=DIM, stroke_width=2)
    g = VGroup(T(name, 34, col), T(year, 30), T(line, 24, SOFT)).arrange(DOWN, buff=0.22).move_to(box)
    return VGroup(box, g)


class LGVNames(DScene):
    def construct(self):
        title = T("Lindström – Gessel – Viennot lemma", 40, YELLOW).to_edge(UP, buff=0.8)
        c1 = name_card("Bernt Lindström", "1973", "matroid theory")
        c2 = name_card("Ira Gessel", "1985", "combinatorics")
        c3 = name_card("Xavier Viennot", "1985", "combinatorics")
        cards = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.4)
        # 0: it's called the Lindström–Gessel–Viennot lemma
        self.cue(0)
        self.play(Write(title), run_time=1.2)
        # 1: Lindström found it in 1973
        self.cue(1)
        self.play(FadeIn(c1, shift=UP * 0.2), run_time=0.7)
        # 2: Gessel and Viennot rediscovered it in 1985
        self.cue(2)
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(c3, shift=UP * 0.2), run_time=0.7)
        self.cue_end(2)
        self.wait(0.5)
        self.play(FadeOut(VGroup(title, cards)), run_time=0.6)


class GeneralLemma(DScene):
    def construct(self):
        rnd = random.Random(3)
        sp, org = 1.35, LEFT * 6.0 + DOWN * 2.4
        pos = {v: org + sp * np.array([v[0], v[1] * 0.95, 0]) + np.array([rnd.uniform(-0.18, 0.18), rnd.uniform(-0.15, 0.15), 0])
               for v in NODES}
        for v in SRC + SNK:                             # keep the starts and ends neatly in a column
            pos[v] = org + sp * np.array([v[0], v[1] * 0.95, 0])
        dots = VGroup(*[Dot(pos[v], radius=0.07, color=SOFT) for v in NODES])
        arrows = VGroup(*[Arrow(pos[a], pos[b], buff=0.1, stroke_width=3, color=DIM, max_tip_length_to_length_ratio=0.18,
                                tip_length=0.16) for a, b in EDGES])
        cols3 = [ANT1, ANT2, ANT3]
        alab = VGroup(*[T(f"a{'₁₂₃'[i]}", 30, cols3[i]).next_to(pos[SRC[i]], LEFT, buff=0.2) for i in range(3)])
        blab = VGroup(*[T(f"b{'₁₂₃'[i]}", 30, cols3[i]).next_to(pos[SNK[i]], UP, buff=0.2) for i in range(3)])
        sdots = VGroup(*[Dot(pos[SRC[i]], radius=0.12, color=cols3[i]) for i in range(3)])
        edots = VGroup(*[Dot(pos[SNK[i]], radius=0.12, color=cols3[i]) for i in range(3)])

        def gpath_mob(p, col, w=7):
            return VMobject(stroke_color=col, stroke_width=w).set_points_as_corners([pos[v] for v in p])

        # 0: any one-way network
        self.cue(0)
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.03), run_time=0.8)
        self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=0.03), run_time=2.0)

        # 1: starts a1..an and ends b1..bn
        self.cue(1)
        self.cue_at(1, "starting points", lead=0.2)
        self.play(FadeIn(sdots), FadeIn(alab), run_time=0.8)
        self.cue_at(1, "ends", lead=0.2)
        self.play(FadeIn(edots), FadeIn(blab), run_time=0.8)

        # 2: the matrix: entry (i, j) counts the paths from a_i to b_j
        self.cue(2)
        M = matrix_mob([[str(v) for v in r] for r in MG], size=42, h_buff=0.75, v_buff=0.55)
        Meq = T("M  =", 42)
        VGroup(Meq, M).arrange(RIGHT, buff=0.3).move_to(RIGHT * 3.3 + UP * 1.9)
        for c in M.cells:
            c.set_opacity(0)
        rl = VGroup(*[T(f"a{'₁₂₃'[i]}", 26, cols3[i]).next_to(M, RIGHT, buff=0.3).match_y(M.cells[3 * i]) for i in range(3)])
        cl = VGroup(*[T(f"b{'₁₂₃'[j]}", 26, cols3[j]).next_to(M.cells[j], UP, buff=0.3) for j in range(3)])
        self.play(FadeIn(Meq), FadeIn(VGroup(M[0], M[2])), FadeIn(rl), FadeIn(cl), run_time=0.8)
        self.add(M.cells)
        # show one entry being counted: paths a1 -> b2
        self.cue_at(2, "counts the paths", lead=0.2)
        ring = SurroundingRectangle(M.cells[1], color=MEET, buff=0.15)
        self.play(Create(ring), run_time=0.4)
        shown = VGroup()
        for p in gpaths(SRC[0], SNK[1]):
            pm = gpath_mob(p, ANT1, 6)
            self.play(Create(pm), *([shown.animate.set_stroke(opacity=0.2)] if len(shown) else []), run_time=0.45)
            shown.add(pm)
        self.sfx("tick")
        self.play(M.cells[1].animate.set_opacity(1), FadeOut(shown), FadeOut(ring), run_time=0.5)
        self.play(*[c.animate.set_opacity(1) for k, c in enumerate(M.cells) if k != 1], run_time=0.8)

        # 3: the determinant counts the families a_i -> b_i that never touch
        self.cue(3)
        fam = VGroup(*[gpath_mob(GOODFAM[i], cols3[i], 8) for i in range(3)])
        self.cue_at(3, "never touch", lead=0.2)
        self.play(LaggedStart(*[Create(m) for m in fam], lag_ratio=0.4), run_time=1.6)
        st = VGroup(T("det M", 34), T("=", 34), T("number of families", 30, YELLOW)).arrange(RIGHT, buff=0.22)
        st2 = T("a₁→b₁, …, aₙ→bₙ that never touch", 28, YELLOW).next_to(st[2], DOWN, buff=0.15).align_to(st[2], LEFT)
        blk = VGroup(st, st2)
        blk.scale_to_fit_width(min(blk.width, 6.0)).move_to(np.array([0.6, -0.55, 0]), aligned_edge=LEFT)
        self.play(Write(st), run_time=1.0)
        self.play(FadeIn(st2), run_time=0.6)

        # 4: the condition, said plainly (and the signed version, small, for the experts)
        self.cue(4)
        note = T("(when every crossed pairing must touch;\n in general, a signed count over pairings)", 22, SOFT, line_spacing=1.1)
        note.next_to(blk, DOWN, buff=0.35).align_to(blk, LEFT)
        self.play(FadeIn(note), run_time=0.7)
        here = T(f"here:  det M = {DETG}", 32).next_to(note, DOWN, buff=0.35).align_to(blk, LEFT)
        self.cue_at(4, "Here", lead=0.2)
        self.sfx("chime")
        self.play(Write(here), Indicate(fam, scale_factor=1.03), run_time=1.0)
        self.cue_end(4)
        self.wait(0.6)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.6)
