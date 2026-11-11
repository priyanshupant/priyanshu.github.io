"""Act 0 — opening v38 (12 Nov): set up the problem the 3Blue1Brown / Numberphile way.

    a concrete surprise first (four ants, 21,000 ways to walk home, how many never meet?),
    then the shortcut (one 4x4 determinant says 252, exactly right),
    then the tool (the school determinant, and its general form with a sign on every term),
    then the paradox (counting only adds; how can minus signs count?), then the promise and the title.
(previous: act0_opening_v36.py.bak = v20, the school/forms/uses intro)
"""
import random
from common import *
from act3b_more import S4, E4, M4, DET4, COLS, FAM4

DIAG = [M4[i][i] for i in range(4)]
TOTAL = int(np.prod(DIAG))
assert TOTAL == 21000 and DET4 == 252


def _meeting_family(rng):
    """A random 'everyone walks home' family in which some two ants meet."""
    PS = [all_paths(S4[i], E4[i]) for i in range(4)]
    while True:
        fam = [rng.choice(PS[i]) for i in range(4)]
        for i in range(4):
            for j in range(i + 1, 4):
                common = [q for q in fam[i] if tuple(q) in set(map(tuple, fam[j]))]
                if common:
                    return fam, common[0]


class Opening(DScene):
    def construct(self):
        rng = random.Random(5)
        lat = Lattice(7, spacing=0.72, center=LEFT * 3.6 + DOWN * 0.25)
        ants = VGroup(*[ant(COLS[i], 0.5).move_to(lat.p(*S4[i])) for i in range(4)])
        homes = VGroup(*[house(COLS[i], 0.36).move_to(lat.p(*E4[i])) for i in range(4)])

        def fam_mob(fam, w=5):
            return VGroup(*[path_mob(lat, fam[i], COLS[i], w) for i in range(4)])

        # 0: four ants want to walk home, stepping only up or right
        self.cue(0)
        self.play(FadeIn(lat), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(a, shift=DOWN * 0.2) for a in ants], lag_ratio=0.2),
                  LaggedStart(*[FadeIn(h, scale=1.4) for h in homes], lag_ratio=0.2), run_time=1.2)
        rules = VGroup(T("↑", 34), T("→", 34)).arrange(RIGHT, buff=0.3).next_to(lat, DOWN, buff=0.25)
        self.cue_at(0, "up or right", lead=0.2)
        self.play(FadeIn(rules), run_time=0.5)

        # 1: each ant alone has 10 to 21 ways home: together 21,000 ways to walk
        self.cue(1)
        icons = VGroup(*[VGroup(ant(COLS[i], 0.42), MathTex(str(DIAG[i])).scale(0.9)).arrange(DOWN, buff=0.12)
                         for i in range(4)])
        prod = VGroup(icons[0], MathTex(r"\times"), icons[1], MathTex(r"\times"), icons[2], MathTex(r"\times"),
                      icons[3]).arrange(RIGHT, buff=0.25).move_to(RIGHT * 3.4 + UP * 1.6)
        tot = MathTex("=", r"21{,}000", r"\text{ ways}").scale(1.1).next_to(prod, DOWN, buff=0.45)
        tot[1].set_color(YELLOW)
        for k in range(4):                                  # a few of each ant's own paths flash by
            ps = rng.sample(all_paths(S4[k], E4[k]), 3)
            for p in ps:
                m = path_mob(lat, p, COLS[k], 5)
                self.add(m)
                self.wait(0.12)
                self.remove(m)
            self.play(FadeIn(prod[2 * k]), *([FadeIn(prod[2 * k - 1])] if k else []), run_time=0.3)
        self.cue_at(1, "twenty-one thousand", lead=0.2)
        self.play(Write(tot), run_time=0.8)

        # 2: but their paths must never meet. How many of the 21,000 work?
        self.cue(2)
        bad, at = _meeting_family(rng)
        bm = fam_mob(bad)
        self.play(Create(bm), run_time=1.0)
        x = cross(0.32).move_to(lat.p(*at))
        self.sfx("buzz")
        self.play(FadeIn(x, scale=1.5), Flash(lat.p(*at), color=BAD, flash_radius=0.3), run_time=0.5)
        self.wait(0.3)
        self.play(FadeOut(bm), FadeOut(x), run_time=0.3)
        gm = fam_mob(FAM4[37])
        self.play(Create(gm), run_time=1.0)
        ok = tick(0.35).next_to(lat, RIGHT, buff=0.2).shift(DOWN * 1.2)
        self.play(FadeIn(ok, scale=1.4), run_time=0.4)
        q = MathTex("?", color=YELLOW).scale(1.4).next_to(tot, DOWN, buff=0.4)
        self.cue_at(2, "How many", lead=0.2)
        self.play(FadeOut(gm), FadeOut(ok), FadeIn(q), run_time=0.5)

        # 3: checking them one by one would take forever (families flicker by)
        self.cue(3)
        for k in range(14):
            f = fam_mob([rng.choice(all_paths(S4[i], E4[i])) for i in range(4)], 4)
            self.add(f)
            self.wait(0.09)
            self.remove(f)
        self.cue_at(3, "shortcut", lead=0.2)

        # 4: write the 4x4 numbers: paths from each ant to each home; its determinant: 252, exactly the answer
        self.cue(4)
        top = VGroup(prod, tot, q)
        M = matrix_mob([[str(v) for v in r] for r in M4], size=30, h_buff=0.55, v_buff=0.38)
        cl = VGroup(*[house(COLS[k], 0.28).next_to(M.cells[k], UP, buff=0.22) for k in range(4)])
        rl = VGroup(*[ant(COLS[k], 0.34).next_to(M, RIGHT, buff=0.2).match_y(M.cells[4 * k]) for k in range(4)])
        mat = VGroup(M, cl, rl).move_to(RIGHT * 3.3 + UP * 0.7)
        self.play(FadeOut(top), FadeIn(mat), run_time=0.9)
        det = VGroup(MathTex(r"\det", "=").scale(1.1), T(str(DET4), 46, YELLOW, weight=BOLD)).arrange(RIGHT, buff=0.25)
        det.next_to(mat, DOWN, buff=0.45)
        self.cue_at(4, "determinant", lead=0.2)
        self.sfx("chime")
        self.play(Write(det), run_time=0.9)
        self.cue_at(4, "exactly", lead=0.2)
        good = VGroup(tick(0.3), T("never meet", 26, GOOD)).arrange(RIGHT, buff=0.15).next_to(det, DOWN, buff=0.25)
        self.play(FadeIn(good), run_time=0.5)
        for k in range(3):
            f = fam_mob(FAM4[(k * 83) % len(FAM4)])
            self.add(f)
            self.wait(0.35)
            self.remove(f)

        # 5: the determinant from school: a d - b c, and the 3x3 (built quickly)
        self.cue(5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        m2 = Matrix([["a", "b"], ["c", "d"]], h_buff=1.0, v_buff=0.8).scale(1.1)
        d2 = VGroup(MathTex(r"\det").scale(1.4), m2, MathTex("=", "ad", "-", "bc").scale(1.4)).arrange(RIGHT, buff=0.3)
        d2[2][2].set_color(BAD)
        d2.move_to(UP * 1.6)
        self.play(FadeIn(d2[:2]), run_time=0.5)
        self.cue_at(5, "a d minus", lead=0.3)
        self.play(Write(d2[2]), run_time=0.8)
        L = [["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]]
        terms = [("+", "aei"), ("+", "bfg"), ("+", "cdh"), ("-", "ceg"), ("-", "bdi"), ("-", "afh")]
        t3 = MathTex(*sum([[sg, t] for sg, t in terms], []))
        t3[0].set_opacity(0)
        for k, (sg, _) in enumerate(terms):
            t3[2 * k].set_color(GOOD if sg == "+" else BAD)
        d3 = VGroup(MathTex(r"\det").scale(1.1), Matrix(L, h_buff=0.8, v_buff=0.6).scale(0.8), MathTex("="), t3) \
            .arrange(RIGHT, buff=0.25).move_to(DOWN * 0.6)
        self.cue_at(5, "three-by-three", lead=0.2)
        self.play(FadeIn(d3[:3]), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(t3[2 * k:2 * k + 2]) for k in range(6)], lag_ratio=0.35), run_time=1.6)

        # 6: in general: a sum over all permutations, with a sign on every term
        self.cue(6)
        leib = MathTex(r"\det A", "=", r"\sum_{\sigma}", r"\operatorname{sgn}(\sigma)", r"\prod_{i} a_{i\sigma(i)}").scale(1.25)
        leib.move_to(UP * 0.3)
        self.play(FadeOut(d2), FadeOut(d3), run_time=0.5)
        self.play(Write(leib), run_time=1.2)
        sgbox = SurroundingRectangle(leib[3], color=YELLOW, buff=0.1)
        pm = MathTex(r"\pm 1", color=YELLOW).scale(0.9).next_to(sgbox, DOWN, buff=0.2)
        self.cue_at(6, "sign", lead=0.2)
        self.play(Create(sgbox), FadeIn(pm), run_time=0.7)

        # 7: the paradox: counting only adds; you can't have minus three ways. How can minus signs count?
        self.cue(7)
        nt = MathTex(r"-3", r"\text{ ways}").scale(1.2).move_to(DOWN * 2.0)
        bx = SurroundingRectangle(nt, buff=0.12)
        neg = VGroup(nt, VGroup(Line(bx.get_corner(DL), bx.get_corner(UR), color=BAD, stroke_width=6),
                                Line(bx.get_corner(UL), bx.get_corner(DR), color=BAD, stroke_width=6)))
        self.cue_at(7, "minus three ways", lead=0.2)
        self.play(FadeIn(neg[0]), run_time=0.5)
        self.play(Create(neg[1]), run_time=0.4)
        self.cue_at(7, "how can", lead=0.2)
        self.play(Indicate(VGroup(sgbox, pm, leib[3]), color=BAD, scale_factor=1.15), run_time=0.9)

        # 8: today: how determinants can count, and why the minus signs are the secret (title)
        self.cue(8)
        self.cue_at(8, "how determinants", lead=0.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        title = T("How Determinants Can Count", 50, weight=BOLD)
        self.sfx("chime")
        self.play(Write(title), run_time=1.3)

        # 9: "let's start with just two ants": the subtitle appears under the title
        self.cue(9)
        sub = T("First, a simple puzzle", 32, SOFT).next_to(title, DOWN, buff=0.45)
        self.cue_at(9, "two ants", lead=0.4)
        self.play(FadeIn(sub, shift=UP * 0.15), run_time=0.7)
        self.cue_end(9)
        self.wait(0.8)
        self.play(FadeOut(VGroup(title, sub)), run_time=0.8)
