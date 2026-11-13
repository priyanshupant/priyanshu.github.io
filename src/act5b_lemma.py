"""Act 5 (v13) — the general lemma, in Priyanshu's style.

    LemmaCard      "The general lemma" in the centre
    BookQuote      Aigner & Ziegler, Proofs from THE BOOK ("…once in their lifetime, is a Lemma…")
    LGVNames       Lindström (1973), Gessel & Viennot (1985) — name cards (no freely licensed photos exist)
    GeneralLemma   any one-way network; starts a1..an, ends b1..bn; M_ij = #paths a_i -> b_j;
                   det M = number of non-touching families a_i -> b_i (when crossed pairings must touch)
"""
from itertools import permutations, product
from common import *
import os

# ---- a general-looking one-way network (v16): EVERY arrow points to the right (horizontal or diagonal, at most
# one diagonal per square, so the drawing is planar). Starts down the LEFT edge, ends down the RIGHT edge, in the
# same top-to-bottom order: lanes a_i -> b_i.
import random
COLS, ROWS = 6, 6
NODES = [(c, r) for c in range(COLS) for r in range(ROWS)]


def _build(seed):
    rng = random.Random(seed)
    E = []
    for c in range(COLS - 1):
        for r in range(ROWS):
            if rng.random() < 0.85:
                E.append(((c, r), (c + 1, r)))
        for r in range(ROWS - 1):
            x = rng.random()
            if x < 0.4:
                E.append(((c, r), (c + 1, r + 1)))
            elif x < 0.8:
                E.append(((c, r + 1), (c + 1, r)))
    return E


EDGES = _build(55)
assert all(b[0] == a[0] + 1 for a, b in EDGES)          # every arrow goes one step to the right
SRC = [(0, 5), (0, 3), (0, 1)]          # a1, a2, a3: three of the six dots on the left, top to bottom
SNK = [(5, 5), (5, 4), (5, 2)]          # b1, b2, b3: three of the six on the right, same order
assert all(any(a == v or b == v for a, b in EDGES) for v in NODES)       # no dot left on its own
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
assert DETG == NT[(0, 1, 2)] == 8 and MG == [[3, 5, 0], [3, 6, 7], [1, 2, 5]], (MG, DETG, NT)
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
    """The quote first, then the book's cover as its source is said (names spoken, not written)."""

    def construct(self):
        import os
        q = T(QUOTE, 30, line_spacing=1.35).move_to(UP * 0.3)
        q.scale_to_fit_width(min(q.width, 12.4))
        split = sum(len(l.replace(' ', '')) for l in QUOTE.split('\n')[:2])
        # 0-1: the quote, read slowly
        self.cue(0)
        self.play(FadeIn(q[:split], lag_ratio=0.02), run_time=2.0)
        self.cue(1)
        self.play(FadeIn(q[split:], lag_ratio=0.02), run_time=2.0)
        # 2: and this is one of those lemmas
        self.cue(2)
        self.play(Indicate(q[split:], color=YELLOW, scale_factor=1.03), run_time=1.0)
        # 3: where the quote is from: the book's cover
        self.cue(3)
        cover = ImageMobject(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "book", "proofs_from_the_book.png"))
        cover.set_height(5.6)
        self.play(q.animate.scale(0.62).to_edge(LEFT, buff=0.5), run_time=0.8)
        cover.to_edge(RIGHT, buff=0.9)
        self.cue_at(3, "Proofs from", lead=0.3)
        self.play(FadeIn(cover, shift=LEFT * 0.3), run_time=0.9)
        # 4: many such beautiful pieces of mathematics
        self.cue(4)
        # 5: inspired by Erdős's Book of the most beautiful proofs
        self.cue(5)
        er = VGroup(T("“You don't have to believe in God,\nbut you should believe in The Book.”", 26, YELLOW, line_spacing=1.2),
                    T("Paul Erdős", 24, SOFT)).arrange(DOWN, aligned_edge=RIGHT, buff=0.15)
        er.next_to(q, DOWN, buff=0.7).align_to(q, LEFT)
        photo = ImageMobject(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "book", "erdos.png")).set_height(2.9)
        self.cue_at(5, "Paul Erdős", lead=0.2)
        self.play(cover.animate.set_height(3.6).move_to(np.array([3.9, 1.6, 0])), run_time=0.7)
        photo.move_to(np.array([cover.get_x(), -2.05, 0]))
        frame = SurroundingRectangle(photo, color=GREY_B, buff=0.03, stroke_width=2)
        self.play(FadeIn(photo), Create(frame), run_time=0.8)
        # 6: he famously said ...
        self.cue(6)
        self.cue_at(6, "you don't have to", lead=0.2)
        self.play(FadeIn(er, shift=UP * 0.15), run_time=0.9)
        self.cue_end(6)
        self.wait(0.5)
        self.play(FadeOut(q), FadeOut(cover), FadeOut(er), FadeOut(photo), FadeOut(frame), run_time=0.6)

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
    """v14 (Priyanshu: no calculations here): the LGV title stays on top; a directed acyclic graph; starts
    a_1..a_n and ends b_1..b_n; M_ij = number of paths a_i -> b_j (symbolic); det M = number of families
    a_1->b_1, ..., a_n->b_n that never touch (when every other pairing must touch); cost ~ n^3."""

    def construct(self):
        rnd = random.Random(3)
        sp, org = 0.95, LEFT * 6.2 + DOWN * 2.65
        pos = {v: org + sp * np.array([v[0], v[1] * 0.95, 0]) + np.array([rnd.uniform(-0.18, 0.18), rnd.uniform(-0.15, 0.15), 0])
               for v in NODES}
        for v in NODES:                                 # the two side columns stay neat (all possible ends)
            if v[0] in (0, COLS - 1):
                pos[v] = org + sp * np.array([v[0], v[1] * 0.95, 0])
        dots = VGroup(*[Dot(pos[v], radius=0.07, color=SOFT) for v in NODES])
        arrows = VGroup(*[Arrow(pos[a], pos[b], buff=0.1, stroke_width=3, color=DIM, max_tip_length_to_length_ratio=0.18,
                                tip_length=0.16) for a, b in EDGES])
        cols3 = [ANT1, ANT2, ANT3]
        alab = VGroup(*[MathTex(f"a_{i + 1}", color=cols3[i]).next_to(pos[SRC[i]], LEFT, buff=0.2) for i in range(3)])
        blab = VGroup(*[MathTex(f"b_{i + 1}", color=cols3[i]).next_to(pos[SNK[i]], RIGHT, buff=0.2) for i in range(3)])
        sdots = VGroup(*[Dot(pos[SRC[i]], radius=0.12, color=cols3[i]) for i in range(3)])
        edots = VGroup(*[Dot(pos[SNK[i]], radius=0.12, color=cols3[i]) for i in range(3)])

        def gpath_mob(p, col, w=7):
            return VMobject(stroke_color=col, stroke_width=w).set_points_as_corners([pos[v] for v in p])

        # 0: its name (said, not written): the title stays on top for the whole scene
        title = T("Lindström – Gessel – Viennot lemma", 32, YELLOW).to_edge(UP, buff=0.25)
        self.cue(0)
        self.play(Write(title), run_time=1.2)
        here = os.path.dirname(os.path.abspath(__file__))

        def face(key, name, x):
            f = os.path.join(here, "assets", "portraits", key + ".jpg")
            lab = T(name, 22)
            if not os.path.exists(f):                       # no photo yet: the name alone
                return Group(lab.scale(1.15)).move_to(np.array([x, 0.0, 0]))
            im = ImageMobject(f).set_height(2.5)
            g = Group(im, SurroundingRectangle(im, color=GREY_B, buff=0.02, stroke_width=1.5))
            lab.next_to(g, DOWN, buff=0.15)
            return Group(g, lab).move_to(np.array([x, 0.0, 0]))
        lind = face("lindstrom", "Bernt Lindström", -5.3)
        gess = face("gessel", "Ira Gessel", -2.85)
        vien = face("viennot", "Xavier Viennot", -0.4)
        y73 = T("1973", 26, YELLOW).move_to(np.array([-5.3, -2.05, 0]))
        y85 = T("1985", 26, YELLOW).move_to(np.array([-1.62, -2.05, 0]))
        gv = paper_page("gessel_viennot_1985", 4.2).move_to(np.array([4.1, -0.2, 0]))
        self.cue_at(0, "Bernt Lindström", lead=0.3)
        self.play(*([FadeIn(lind, shift=UP * 0.2)] if lind else []), FadeIn(y73), run_time=0.7)
        self.cue_at(0, "Gessel and Viennot rediscovered", lead=0.3)
        self.play(*[FadeIn(m, shift=UP * 0.2) for m in (gess, vien) if m], FadeIn(y85), run_time=0.8)
        self.play(FadeIn(gv, shift=LEFT * 0.3), run_time=0.7)
        self.cue_end(0)
        self.wait(0.8)
        self.play(*[FadeOut(m) for m in (lind, gess, vien, gv, y73, y85) if m], run_time=0.6)

        # 1: a directed acyclic graph: one-way arrows, no cycles
        self.cue(1)
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.03), run_time=0.8)
        self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=0.03), run_time=2.0)

        # 2: starts a_1..a_n and ends b_1..b_n
        self.cue(2)
        sides = VGroup(*[dots[NODES.index(v)] for v in NODES if v[0] in (0, COLS - 1)])
        self.play(Indicate(sides, color=YELLOW, scale_factor=1.6), run_time=0.9)
        self.cue_at(2, "points on the left", lead=0.2)
        self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in sdots], lag_ratio=0.3), run_time=1.0)
        self.cue_at(2, "on the right", lead=0.2)
        self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in edots], lag_ratio=0.3), run_time=1.0)
        self.cue_at(2, "label them", lead=0.2)
        self.play(FadeIn(alab), FadeIn(blab), run_time=0.6)

        # 3: the order matters: ends lined up like the starts, so a mixed-up pairing is forced to cross
        self.cue(3)
        self.cue_at(3, "same order", lead=0.2)
        order = VGroup(*[Line(pos[SRC[i]], pos[SNK[i]], color=cols3[i], stroke_width=2).set_stroke(opacity=0.35) for i in range(3)])
        lanes = VGroup(*[DashedLine(pos[SRC[i]], pos[SNK[i]], color=cols3[i], stroke_width=3, dash_length=0.12) for i in range(3)])
        self.cue_at(3, "first to first", lead=0.3)
        self.play(LaggedStart(*[Create(l) for l in lanes], lag_ratio=0.3), run_time=1.2)
        self.cue_at(3, "This makes sure", lead=0.1)
        self.play(FadeOut(lanes), run_time=0.4)
        mp = gpaths(SRC[1], SNK[2])[0]
        mq = next(q for q in gpaths(SRC[2], SNK[1]) if set(q) & set(mp))
        meet = next(v for v in mp if v in mq)
        mix = VGroup(gpath_mob(mp, ANT2, 7), gpath_mob(mq, ANT3, 7))
        self.cue_at(3, "if we pick", lead=0.2)
        self.play(Create(mix[0]), run_time=0.9)
        self.cue_at(3, "two wrong paths", lead=0.2)
        self.play(Create(mix[1]), run_time=0.9)
        ring = Circle(radius=0.3, color=MEET, stroke_width=6).move_to(pos[meet])
        self.cue_at(3, "must cross", lead=0.2)
        self.sfx("buzz")
        self.play(Create(ring), Flash(pos[meet], color=MEET), run_time=0.7)
        self.wait(0.6)
        self.play(*[FadeOut(x) for x in (*mix, ring)], run_time=0.5)

        # 3: the matrix M: entry (i, j) = number of paths from a_i to b_j (symbols only, no numbers)
        self.cue(4)
        M = MathTex(r"M = \begin{bmatrix} m_{11} & m_{12} & \cdots & m_{1n} \\ m_{21} & m_{22} & \cdots & m_{2n} \\"
                    r" \vdots & \vdots & \ddots & \vdots \\ m_{n1} & m_{n2} & \cdots & m_{nn} \end{bmatrix}").scale(0.85)
        M.move_to(RIGHT * 3.4 + UP * 1.45)
        mij = MathTex(r"m_{ij}", "=", r"\#\,\text{paths from } a_i \text{ to } b_j").scale(0.85).next_to(M, DOWN, buff=0.3)
        self.play(Write(M), run_time=1.4)
        self.cue_at(4, "number of paths", lead=0.2)
        self.play(Write(mij), run_time=1.0)
        # illustrate one entry: a few paths from a_1 to b_2, drawn and gone (no counting)
        allp = gpaths(SRC[0], SNK[1])                     # ALL the paths from a_1 to b_2, one after another
        hl = VGroup(SurroundingRectangle(alab[0], color=YELLOW, buff=0.06), SurroundingRectangle(blab[1], color=YELLOW, buff=0.06))
        self.play(Create(hl), run_time=0.4)
        shown = VGroup()
        for pth in allp:
            pm = gpath_mob(pth, ANT1, 6)
            self.play(Create(pm), *([shown.animate.set_stroke(opacity=0.25)] if len(shown) else []), run_time=0.35)
            shown.add(pm)
        self.wait(0.3)
        self.play(*[FadeOut(x) for x in shown], FadeOut(hl), run_time=0.4)

        # 4: det M counts the families a_1 -> b_1, ..., a_n -> b_n that never touch (written as it is said)
        self.cue(5)
        fam = VGroup(*[gpath_mob(GOODFAM[i], cols3[i], 8) for i in range(3)])
        st = MathTex(r"\det M", "=", r"\#\,\text{families } a_1\!\to b_1,\ \dots,\ a_n\!\to b_n", color=WHITE).scale(0.72)
        st2 = MathTex(r"\text{that never touch}", color=YELLOW).scale(0.72)
        st.next_to(mij, DOWN, buff=0.55)
        st.shift(RIGHT * (mij[1].get_x() - st[1].get_x()))
        st[2].set_color(YELLOW)
        st2.next_to(st[2], DOWN, buff=0.12).align_to(st[2], LEFT)
        blk = VGroup(st, st2)
        if blk.get_right()[0] > 6.9:
            blk.shift(LEFT * (blk.get_right()[0] - 6.9))
        self.cue_at(5, "the determinant of M", lead=0.2)
        self.play(Write(st[:2]), run_time=0.7)
        self.cue_at(5, "number of families", lead=0.2)
        self.play(Write(st[2]), run_time=1.0)
        self.cue_at(5, "never touch", lead=0.2)
        self.play(FadeIn(st2), LaggedStart(*[Create(m) for m in fam], lag_ratio=0.4), run_time=1.6)

        self.cue_end(5)
        self.wait(0.6)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.6)
