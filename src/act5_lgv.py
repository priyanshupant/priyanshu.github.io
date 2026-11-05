"""Act 5 — Any arrangement, any number of walkers (Script v2, 8:30-10:00).

    MoveHomes   ant 2's house moves; brute force and det agree; wrong order -> 0 and a minus sign
    SekiJoins   three walkers, 3x3 det = 175 = non-touching triples
    Lemma       the LGV statement, the cost of a determinant, omega <= 9/4
    LGVCredits  Lindström, Gessel & Viennot (+ Karlin–McGregor, Fisher's "vicious walkers")
"""
from itertools import product
from math import comb

from common import *


def n_paths(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    return comb(dx + dy, dx) if dx >= 0 and dy >= 0 else 0


def det_n(M):
    return round(np.linalg.det(np.array(M, float)))


def peaceful(starts, homes):
    fams = product(*[all_paths(s, h) for s, h in zip(starts, homes)])
    return sum(1 for f in fams if all(not (set(f[i]) & set(f[j]))
                                      for i in range(len(f)) for j in range(i + 1, len(f))))


class MoveHomes(DScene):
    def construct(self):
        lat = Lattice(5, spacing=1.05, center=LEFT * 4 + DOWN * 0.3, ny=5)
        title = T("Move the houses: does the trick still work?", 32).to_edge(UP, buff=0.35)
        self.cue(0)
        self.play(Write(title))
        s1 = Dot(lat.p(*A1), radius=0.1, color=ANT1)
        s2 = Dot(lat.p(*A2), radius=0.1, color=ANT2)
        h1 = house(ANT1, 0.32).move_to(lat.p(*B1))
        h2 = house(ANT2, 0.32).move_to(lat.p(*B2))
        self.play(FadeIn(lat), FadeIn(s1), FadeIn(s2), FadeIn(h1), FadeIn(h2))
        hdr = VGroup(T("ant 2's house", 28, ANT2), T("brute force", 28, GOOD), T("det", 28, YELLOW)) \
            .arrange(RIGHT, buff=0.8).move_to(RIGHT * 2.6 + UP * 2.2)
        self.play(FadeIn(hdr))
        rows = VGroup()
        for k, b2 in enumerate([(3, 2), (4, 2), (4, 1), (3, 1), (1, 4)]):
            if k == 4:
                self.cue(2)
            self.play(h2.animate.move_to(lat.p(*b2)), run_time=0.6)
            M = [[n_paths(A1, B1), n_paths(A1, b2)], [n_paths(A2, B1), n_paths(A2, b2)]]
            bf, d = peaceful([A1, A2], [B1, b2]), det_n(M)
            wrong = b2 == (1, 4)
            row = VGroup(T(str(b2), 30, ANT2), T(str(bf), 32, GOOD), T(str(d), 32, BAD if wrong else YELLOW))
            for c, h in zip(row, hdr):
                c.move_to([h.get_x(), 1.6 - 0.6 * k, 0])
            self.play(FadeIn(row), run_time=0.4)
            rows.add(row)
            if wrong:
                note = VGroup(T("wrong order: no peaceful routes at all;", 26, BAD),
                              T("det counts the swapped pairing, with a minus sign", 26, BAD)) \
                    .arrange(DOWN, buff=0.05, aligned_edge=LEFT).next_to(rows, DOWN, buff=0.45)
                note.scale_to_fit_width(min(note.width, 7.6)).to_edge(RIGHT, buff=0.3)
                self.play(FadeIn(note))
            else:
                self.wait(0.4)
            if k == 3:
                self.cue(1)
                rule = T("Keep the order (ant 1's house up-left of ant 2's) and it always works.", 28, YELLOW) \
                    .to_edge(DOWN, buff=0.35)
                self.play(FadeIn(rule))


SEKI_S = [(0, 2), (1, 1), (2, 0)]
SEKI_E = [(2, 4), (3, 3), (4, 2)]


class SekiJoins(DScene):
    def construct(self):
        lat = Lattice(5, spacing=1.05, center=LEFT * 4 + DOWN * 0.3, ny=5)
        who = ["leibniz", "newton", "seki"]
        cols = [ANT1, ANT2, ANT3]
        self.cue(0)
        self.play(FadeIn(lat))
        chars = []
        for k in range(3):
            self.add(Dot(lat.p(*SEKI_S[k]), radius=0.08, color=cols[k]), house(cols[k], 0.3).move_to(lat.p(*SEKI_E[k])))
            chars.append(ant(cols[k], 0.7).move_to(lat.p(*SEKI_S[k])))
        self.play(FadeIn(chars[0]), FadeIn(chars[1]))
        intro = T("A third ant joins,\nwith its own start and house.", 26,
                  line_spacing=1.15).move_to(RIGHT * 2.6 + UP * 2.6)
        self.play(FadeIn(chars[2], shift=DOWN * 0.3), FadeIn(intro))
        # one peaceful triple
        fam = next(f for f in product(*[all_paths(s, e) for s, e in zip(SEKI_S, SEKI_E)])
                   if all(not (set(f[i]) & set(f[j])) for i in range(3) for j in range(i + 1, 3)))
        anims, _ = walk_steps(lat, [(chars[k], fam[k], cols[k]) for k in range(3)], step_time=0.35)
        for an in anims:
            self.play(an)
        M = [[n_paths(s, e) for e in SEKI_E] for s in SEKI_S]
        m = matrix_mob(M, size=40).move_to(RIGHT * 2.6 + UP * 0.4)
        for k, c in enumerate(m.cells):
            c.set_color(cols[k // 3])
        self.cue(1)
        self.play(FadeOut(intro), FadeIn(m))
        d = det_n(M)
        det = T(f"det = {d}", 42, YELLOW).next_to(m, DOWN, buff=0.45)
        self.sfx("chime")
        self.play(Write(det))
        tot = int(np.prod([n_paths(s, e) for s, e in zip(SEKI_S, SEKI_E)]))
        bf = T(f"brute force: {peaceful(SEKI_S, SEKI_E)} of {tot} triples", 28, GOOD).next_to(det, DOWN, buff=0.3)
        self.play(FadeIn(bf))


PERMS = [((0, 1, 2), +1), ((1, 0, 2), -1), ((0, 2, 1), -1), ((2, 1, 0), -1), ((1, 2, 0), +1), ((2, 0, 1), +1)]


def perm_mob(sig, sign, w=1.15, h=1.3):
    """Three starts (left) joined to three ends (right) by the pairing sig, with its sign."""
    cols = [ANT1, ANT2, ANT3]
    ys = [h / 2, 0, -h / 2]
    g = VGroup()
    for i in range(3):
        g.add(Line(LEFT * w / 2 + UP * ys[i], RIGHT * w / 2 + UP * ys[sig[i]], color=cols[i], stroke_width=5))
    for i in range(3):
        g.add(Dot(LEFT * w / 2 + UP * ys[i], radius=0.08, color=cols[i]))
        g.add(Dot(RIGHT * w / 2 + UP * ys[i], radius=0.08, color=INK))
    badge = T("+" if sign > 0 else "−", 40, GOOD if sign > 0 else BAD).next_to(g, LEFT, buff=0.2)
    return VGroup(badge, g)


# the concrete example: SekiJoins' three ants
LM = [[n_paths(a, b) for b in SEKI_E] for a in SEKI_S]
assert LM == [[6, 4, 1], [4, 6, 4], [1, 4, 6]]


def _fams(sig, touching):
    fams = product(*[all_paths(SEKI_S[i], SEKI_E[sig[i]]) for i in range(3)])
    nt = lambda f: all(not (set(f[a]) & set(f[b])) for a in range(3) for b in range(a + 1, 3))
    return sum(1 for f in fams if nt(f) != touching)


TERMS = [LM[0][sg[0]] * LM[1][sg[1]] * LM[2][sg[2]] for sg, _ in PERMS]
assert TERMS == [216, 96, 96, 6, 16, 16]
assert sum(sn * t for (sg, sn), t in zip(PERMS, TERMS)) == 50
assert _fams(PERMS[0][0], False) == 50 and all(_fams(sg, False) == 0 for sg, _ in PERMS[1:])
POS_T = sum(t for (sg, sn), t in zip(PERMS, TERMS) if sn > 0) - 50     # touching, + sign
NEG_T = sum(t for (sg, sn), t in zip(PERMS, TERMS) if sn < 0)
assert POS_T == NEG_T == 198

# omega over the years (upper bounds)
OMEGA = [(1968, 3.0, ""), (1969, 2.8074, "Strassen 1969"), (1978, 2.796, ""), (1979, 2.780, ""),
         (1981, 2.496, ""), (1986, 2.479, ""), (1990, 2.3755, "Coppersmith–Winograd 1990"), (2010, 2.3737, ""),
         (2012, 2.3729, ""), (2014, 2.3729, ""), (2022, 2.3719, ""), (2024, 2.3713, ""), (2026, 2.25, "9/4, 2026")]


class LemmaVisual(DScene):
    """The LGV lemma on the three-ant example: matrix, signed terms with their counts,
    the touching families cancelling 198 against 198, the 50 that never touch."""

    def construct(self):
        cols = [ANT1, ANT2, ANT3]
        head = T("The general statement", 40).to_edge(UP, buff=0.3)
        # 0: network + matrix
        self.cue(0)
        self.play(Write(head))
        lat = Lattice(5, spacing=0.62, center=LEFT * 5.0 + UP * 1.05, ny=5)
        se = VGroup(*[Dot(lat.p(*SEKI_S[k]), radius=0.09, color=cols[k]) for k in range(3)],
                    *[house(cols[k], 0.26).move_to(lat.p(*SEKI_E[k])) for k in range(3)])
        self.play(FadeIn(lat), FadeIn(se))
        M = matrix_mob(LM, size=40, h_buff=0.6, v_buff=0.4).move_to(LEFT * 1.2 + UP * 1.05)
        for k, c in enumerate(M.cells):
            c.set_color(cols[k // 3])
        ml = T("paths from each start\nto each end", 26, SOFT, line_spacing=1.1).next_to(M, RIGHT, buff=0.5)
        self.cue_at(0, "count the paths")
        self.play(FadeIn(M), FadeIn(ml))
        # 1: expand into pairings with signs
        self.cue(1)
        terms = VGroup(*[perm_mob(sg, sn, w=1.0, h=1.1) for sg, sn in PERMS]).arrange(RIGHT, buff=0.5)
        dl = T("det =", 36, YELLOW).next_to(terms, LEFT, buff=0.3)
        row = VGroup(dl, terms)
        row.scale_to_fit_width(min(row.width, 11.8)).move_to(LEFT * 0.7 + DOWN * 0.95)
        self.play(FadeOut(ml), FadeIn(dl), LaggedStartMap(FadeIn, terms, lag_ratio=0.2, shift=UP * 0.2), run_time=1.8)
        # 2: the numbers
        self.cue(2)
        nums = VGroup(*[T(str(t), 36, GOOD if sn > 0 else BAD).next_to(terms[k][1], DOWN, buff=0.25)
                        for k, ((sg, sn), t) in enumerate(zip(PERMS, TERMS))])
        for k, w in enumerate(["two hundred", "minus ninety-six,", "minus ninety-six, minus six", "minus six",
                               "plus sixteen,", "plus sixteen."]):
            if k == 2:
                w = "ninety-six, minus six"
            self.cue_at(2, w, lead=0.15)
            self.play(FadeIn(nums[k], scale=1.3), run_time=0.35)
        tot = T("= 50", 40, YELLOW).next_to(terms, RIGHT, buff=0.25)
        self.play(FadeIn(tot))
        # 3: of the 216 only 50 never touch; crossed pairings always touch
        self.cue(3)
        split = VGroup(T("50", 32, GOOD), T("never touch", 22, GOOD), T("166", 32, BAD), T("touch", 22, BAD)) \
            .arrange(DOWN, buff=0.04).move_to(nums[0], aligned_edge=UP)
        self.play(ReplacementTransform(nums[0], split), run_time=0.8)
        self.cue_at(3, "crossed")
        tch = VGroup(*[T("all touch", 22, BAD).next_to(nums[k], DOWN, buff=0.08) for k in range(1, 6)])
        self.play(LaggedStartMap(FadeIn, tch, lag_ratio=0.15))
        # 4: tail swap pairs touching families of opposite sign: 198 vs 198
        self.cue(4)
        pos = VGroup(split[2], split[3], nums[4], nums[5], tch[3], tch[4])
        neg = VGroup(nums[1], nums[2], nums[3], tch[0], tch[1], tch[2])
        bal = VGroup(T("166 + 16 + 16 = 198", 32, GOOD), T("⟷", 36, YELLOW), T("96 + 96 + 6 = 198", 32, BAD)) \
            .arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.45)
        self.play(Indicate(pos, color=GOOD), run_time=0.8)
        self.play(Indicate(neg, color=BAD), run_time=0.8)
        self.cue_at(4, "one hundred ninety-eight")
        self.play(FadeIn(bal))
        self.cue_at(4, "They all cancel")
        self.sfx("pop")
        self.play(FadeOut(pos, scale=0.3), FadeOut(neg, scale=0.3), FadeOut(bal),
                  *[t.animate.set_opacity(0.2) for t in terms[1:]], tot.animate.set_opacity(0.3), run_time=1.0)
        # 5: what is left
        self.cue(5)
        res = T("det  =  number of families that never touch", 34, YELLOW).to_edge(DOWN, buff=0.5)
        self.play(Indicate(VGroup(terms[0], split[0], split[1]), color=GOOD), Write(res))
        # 6: name
        self.cue(6)
        name = T("The Lindström–Gessel–Viennot lemma", 40, YELLOW).move_to(head)
        cred = T("Lindström 1973 · Gessel & Viennot 1985", 26, SOFT).next_to(name, DOWN, buff=0.15)
        self.play(Transform(head, name), FadeIn(cred))
        # 7: vicious walkers: the three ants walk a peaceful family
        self.cue(7)
        fam = next(f for f in product(*[all_paths(a, b) for a, b in zip(SEKI_S, SEKI_E)])
                   if all(not (set(f[a]) & set(f[b])) for a in range(3) for b in range(a + 1, 3)))
        ants = [ant(cols[k], 0.5).move_to(lat.p(*SEKI_S[k])) for k in range(3)]
        vic = T("physicists: \"vicious walkers\"", 30, SOFT).next_to(M, RIGHT, buff=0.5)
        self.play(*[FadeIn(a) for a in ants], FadeIn(vic))
        anims, _ = walk_steps(lat, [(ants[k], fam[k], cols[k]) for k in range(3)], step_time=0.3)
        for an in anims:
            self.play(an)
        # 8: the cost
        self.cue(8)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (head, cred)])
        cost = VGroup(
            VGroup(T("n ants, brute force:", 34), T("exponential", 34, BAD)).arrange(RIGHT, buff=0.3),
            VGroup(T("a determinant:", 34), T("about n³ steps", 34, GOOD)).arrange(RIGHT, buff=0.3),
            VGroup(T("with fast matrix multiplication:", 30), T("n^ω", 34, GOOD)).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.6)
        self.play(FadeIn(cost[0]))
        self.cue_at(8, "A determinant")
        self.play(FadeIn(cost[1]))
        self.cue_at(8, "or n to")
        self.play(FadeIn(cost[2]))
        # 9: omega keeps falling: the staircase
        self.cue(9)
        self.play(FadeOut(cost), FadeOut(cred), Transform(head, T("ω keeps falling", 40, YELLOW).move_to(head)))
        ax = Axes(x_range=[1965, 2029, 10], y_range=[1.9, 3.1, 0.25], x_length=11, y_length=5.0,
                  axis_config={"color": GREY_B, "include_ticks": False}, tips=False).move_to(DOWN * 0.3)
        yl = VGroup(*[T(f"{v}", 24, SOFT).next_to(ax.c2p(1965, v), LEFT, buff=0.15) for v in (2.0, 2.5, 3.0)])
        xl = VGroup(*[T(str(y), 24, SOFT).next_to(ax.c2p(y, 1.9), DOWN, buff=0.15) for y in (1970, 1990, 2010, 2026)])
        floor = DashedLine(ax.c2p(1965, 2.0), ax.c2p(2029, 2.0), color=GREY_D)
        fl = T("ω ≥ 2", 24, GREY_C).next_to(ax.c2p(2029, 2.0), UP, buff=0.08).shift(LEFT * 0.5)
        self.play(Create(ax), FadeIn(yl), FadeIn(xl), Create(floor), FadeIn(fl), run_time=1.0)
        pts = []
        for k, (yr, w, _) in enumerate(OMEGA):
            if k:
                pts.append(ax.c2p(yr, OMEGA[k - 1][1]))
            pts.append(ax.c2p(yr, w))
        pts.append(ax.c2p(2028, OMEGA[-1][1]))
        stair = VMobject(stroke_color=YELLOW, stroke_width=5).set_points_as_corners(pts[:-3])
        last = VMobject(stroke_color=YELLOW, stroke_width=6).set_points_as_corners(pts[-4:])
        labs = VGroup()
        for yr, w, nm in OMEGA[:-1]:
            if nm:
                labs.add(T(nm, 24, INK).next_to(ax.c2p(yr, w), UR, buff=0.12))
        self.play(Create(stair), FadeIn(labs, lag_ratio=0.5), run_time=2.5)
        self.cue_at(9, "nine quarters")
        self.sfx("chime")
        dot = Dot(ax.c2p(2026, 2.25), radius=0.11, color=YELLOW)
        nl = T("9/4  (Oct 2026)", 28, YELLOW).next_to(dot, DOWN, buff=0.2).shift(LEFT * 0.6)
        self.play(Create(last), FadeIn(dot, scale=2), FadeIn(nl), run_time=1.0)
        who = T("AI model at OpenAI · checked in Lean · explained by Amir Shpilka", 26).to_edge(DOWN, buff=0.25)
        self.cue_at(9, "Proved")
        self.play(FadeIn(who))


# ---------------------------------------------------------------- what LGV can count
import random as _random


def _network(nx=6, ny=4, seed=13):
    """A planar one-way network: right and up roads, some diagonals, a few roads missing."""
    rng = _random.Random(seed)
    V = [(x, y) for x in range(nx) for y in range(ny)]
    E = []
    for x, y in V:
        if x + 1 < nx and rng.random() > 0.12:
            E.append(((x, y), (x + 1, y)))
        if y + 1 < ny and rng.random() > 0.12:
            E.append(((x, y), (x, y + 1)))
        if x + 1 < nx and y + 1 < ny and rng.random() < 0.35:
            E.append(((x, y), (x + 1, y + 1)))
    return V, E


def _dag_paths(E, a, b):
    out_ = {}
    for u, v in E:
        out_.setdefault(u, []).append(v)
    res = []

    def rec(cur):
        if cur[-1] == b:
            res.append(tuple(cur))
            return
        for v in out_.get(cur[-1], []):
            rec(cur + [v])
    rec([a])
    return res


NV, NE = _network()
NS = [(0, 0), (0, 1), (0, 2)]
NT = [(5, 1), (5, 2), (5, 3)]
NM = [[len(_dag_paths(NE, s, t)) for t in NT] for s in NS]
NDET = round(np.linalg.det(np.array(NM, float)))
NFAMS = [f for f in product(*[_dag_paths(NE, NS[i], NT[i]) for i in range(3)])
         if len({q for p in f for q in p}) == sum(len(p) for p in f)]
assert NDET == len(NFAMS) and NDET > 0


class WhatLGVCounts(DScene):
    def construct(self):
        title = T("What can this count?", 40).to_edge(UP, buff=0.35)
        self.cue(0)
        self.play(Write(title))
        sp, c0 = 1.0, LEFT * 5.6 + DOWN * 1.8
        pos = {v: c0 + sp * np.array([v[0], v[1], 0]) for v in NV}
        roads = VGroup(*[Arrow(pos[u], pos[v], buff=0.12, stroke_width=3, color=GREY_B,
                               max_tip_length_to_length_ratio=0.18) for u, v in NE])
        dots = VGroup(*[Dot(pos[v], radius=0.05, color=GREY_C) for v in NV])
        self.play(FadeIn(dots), LaggedStartMap(GrowArrow, roads, lag_ratio=0.02), run_time=1.8)
        lab = T("any network of one-way roads with no loops", 26, SOFT).next_to(roads, DOWN, buff=0.3)
        self.play(FadeIn(lab))
        cols = [ANT1, ANT2, ANT3]
        ends = VGroup(*[Dot(pos[s], radius=0.11, color=cols[i]) for i, s in enumerate(NS)],
                      *[house(cols[i], 0.3).move_to(pos[t]) for i, t in enumerate(NT)])
        # 1: the matrix and its determinant
        self.cue(1)
        self.play(FadeIn(ends))
        Mm = matrix_mob(NM, size=38, h_buff=0.6, v_buff=0.4).move_to(RIGHT * 2.6 + UP * 1.2)
        for k, c in enumerate(Mm.cells):
            c.set_color(cols[k // 3])
        ml = T("routes from each start to each end", 24, SOFT).next_to(Mm, UP, buff=0.25)
        self.cue_at(1, "Count")
        self.play(FadeIn(Mm), FadeIn(ml))
        dt = T(f"det = {NDET}", 44, YELLOW).next_to(Mm, RIGHT, buff=0.45)
        if dt.get_right()[0] > 7.0:
            dt.next_to(Mm, DOWN, buff=0.35)
        self.cue_at(1, "take the")
        self.sfx("chime")
        self.play(Write(dt))
        # 2: = the number of ways nobody meets; flick through the families
        self.cue(2)
        cnt_l = T("families where nobody meets:", 28).move_to(RIGHT * 2.6 + DOWN * 1.5)
        cnt = T("0", 52, GOOD).next_to(cnt_l, DOWN, buff=0.2)
        self.play(FadeIn(cnt_l), FadeIn(cnt))
        cur = None
        step = max(1, len(NFAMS) // 14)
        shown = list(range(0, len(NFAMS), step))
        for k in shown:
            f = NFAMS[k]
            pm = VGroup(*[VMobject(stroke_color=cols[i], stroke_width=7).set_points_as_corners([pos[v] for v in f[i]])
                          for i in range(3)])
            nc = T(str(k + 1), 52, GOOD).move_to(cnt)
            if cur is not None:
                self.remove(cur)
            self.add(pm)
            self.remove(cnt)
            cnt = nc
            self.add(cnt)
            cur = pm
            self.wait(0.18)
        self.cue_at(2, "Here it")
        self.remove(cnt)
        cnt = T(str(len(NFAMS)), 60, GOOD, weight=BOLD).move_to(cnt)
        self.sfx("chime")
        self.play(FadeIn(cnt, scale=1.4), Indicate(dt, color=YELLOW))
        self.cue_at(2, "Of course")
        hg = T("(of course it is)", 26, SOFT).next_to(cnt, RIGHT, buff=0.3)
        self.play(FadeIn(hg))
        self.cue(3)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not title])
        big = T("Any puzzle that is secretly non-touching paths,\na determinant can count.", 34, YELLOW,
                line_spacing=1.2).next_to(title, DOWN, buff=0.5)
        self.play(Write(big))
        from act6_hexagon import tiling as _til, outline as _out, SHOW as _show, BOX as _box
        from act6b_disguises import az_mob, AZ, CFAM
        thumbs = Group(
            VGroup(_out(0.45), _til(_show, 0.45, stroke=1)),
            VGroup(_out(0.3, box=(3, 3, 3)), _til(((2, 1, 1), (1, 1, 0), (1, 0, 0)), 0.3, stroke=1, box=(3, 3, 3))),
            VGroup(*[VMobject(stroke_color=col, stroke_width=4).set_points_as_corners(
                [0.18 * np.array([x, y, 0]) for x, y in p]) for p, col in zip(CFAM[1], (ANT1, ANT2))]),
            az_mob(AZ[2][5], 2, 0.3, ORIGIN),
        )
        names = ["hexagon tilings", "boxes in a corner", "mountain ranges", "Aztec diamond"]
        for th in thumbs:
            th.scale_to_fit_height(2.0)
        cards = Group(*[Group(th, T(nm, 24)).arrange(DOWN, buff=0.3) for th, nm in zip(thumbs, names)])
        cards.arrange(RIGHT, buff=0.7).next_to(big, DOWN, buff=0.7)
        if cards.width > 13:
            cards.scale_to_fit_width(13)
        self.cue_at(3, "And these")
        self.play(LaggedStartMap(FadeIn, cards, lag_ratio=0.3, shift=UP * 0.2), run_time=2)
