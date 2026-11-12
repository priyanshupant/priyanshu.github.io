"""Act 9 — The map, the limit, and nature (Script v2, 15:15-17:00).

    Map        everything determinants counted, around a central "det"
    Limit      K3,3 cannot be flattened; signs slide off; determinant vs permanent
    Nature     fermions = determinants (Pauli), bosons = permanents; boson sampling
    Goodbye    ant 1 and ant 2 get home without meeting; thanks
    Credits    rolling credits and reading list
"""
from common import *
from act3_two_walkers import GOOD_P, GOOD_Q
from act6_hexagon import tiling as hex_tiling, outline as hex_outline, SHOW
from act7_trees import graph_mob, HV, HE, TREES
from act8_dominoes import board, domino


def k33(scale=1.0, center=ORIGIN):
    top = [center + scale * np.array([x, 1.1, 0]) for x in (-1.6, 0, 1.6)]
    bot = [center + scale * np.array([x, -1.1, 0]) for x in (-1.6, 0, 1.6)]
    edges = VGroup(*[Line(a, b, color=YELLOW, stroke_width=3 * scale + 1) for a in top for b in bot])
    dots = VGroup(*[Dot(p, radius=0.09 * scale + 0.02, color=WHITE) for p in top + bot])
    return VGroup(edges, dots)


class Map(DScene):
    def construct(self):
        core = VGroup(Circle(radius=0.75, color=YELLOW), T("det", 44, YELLOW))
        self.cue(0)
        self.play(FadeIn(core, scale=0.8))
        from act6b_disguises import az_mob, AZ, CFAM
        hexg = VGroup(hex_outline(0.3), hex_tiling(SHOW, 0.3, stroke=1))
        b = board(2, 3, 0.32)
        b.add(*[domino(b.sq, x, y, 0.32) for x, y in [((0, 0), (1, 0)), ((0, 1), (1, 1)), ((0, 2), (1, 2))]])
        mt = VGroup(*[VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(
            [0.14 * np.array([x, y, 0]) for x, y in p]) for p, col in zip(CFAM[1], (ANT1, ANT2))])
        panels = [
            (pair_icon(GOOD_P, GOOD_Q, size=0.8, meet=False), "ants that never meet", "20"),
            (hexg, "hexagon tilings", "20"),
            (az_mob(AZ[2][5], 2, 0.24, ORIGIN), "Aztec diamonds", "2^(n(n+1)/2)"),
            (b, "domino tilings", "12,988,816"),
        ]
        items = []
        for k, (ic, name, num) in enumerate(panels):
            ang = PI / 2 - TAU * k / len(panels)
            pos = np.array([4.9 * np.cos(ang), 2.75 * np.sin(ang), 0])
            ic.scale(1.25)
            nm = MathTex(r"2^{n(n+1)/2}", color=YELLOW).scale(0.75) if num.startswith("2^") else T(num, 24, YELLOW)
            g = VGroup(ic, T(name, 22), nm).arrange(DOWN, buff=0.08).move_to(pos)
            ln = Line(core.get_center(), pos, color=GREY_D)
            ln.put_start_and_end_on(core.get_center() + 0.8 * normalize(pos), pos - (1.25 if abs(pos[0]) < 0.5 else 0.9) * normalize(pos))
            items.append((g, ln))
        for g, ln in items:
            self.play(Create(ln), FadeIn(g), run_time=0.7)
            self.wait(0.5)
        self.cue(1)
        self.play(Indicate(core, color=YELLOW, scale_factor=1.25))


class Limit(DScene):
    def construct(self):
        title = T("But not everything.", 38).to_edge(UP, buff=0.4)
        self.play(Write(title))
        g = k33(0.95, LEFT * 4.7 + DOWN * 0.2)
        self.play(Create(g[0], lag_ratio=0.1), FadeIn(g[1]), run_time=1.5)
        lab = T("K₃,₃: no drawing\nwithout crossings", 22, SOFT, line_spacing=1.1).next_to(g, DOWN, buff=0.3)
        self.play(FadeIn(lab))
        signs = VGroup(*[T("−", 44, FLIP_C, weight=BOLD).move_to(e.get_center() + UP * 0.15) for e in g[0][::2]])
        self.play(LaggedStartMap(FadeIn, signs, lag_ratio=0.15, scale=2), run_time=1)
        self.sfx("whoosh")
        self.play(LaggedStart(*[sg.animate.shift(DOWN * 4).rotate(PI).set_opacity(0) for sg in signs], lag_ratio=0.12),
                  run_time=1.8, rate_func=rush_into)
        self.wait(0.5)
        det = VGroup(T("determinant", 28, GOOD), T("Σ sign(σ) · ∏ aᵢσ(ᵢ)", 30),
                     T("polynomial time; even fast in parallel", 22, SOFT), T("(Csanky, 1976)", 20, SOFT)) \
            .arrange(DOWN, buff=0.12)
        perm = VGroup(T("permanent", 28, BAD), T("Σ  ∏ aᵢσ(ᵢ)   (all plus)", 30),
                      T("#P-complete: believed hopelessly hard", 22, SOFT), T("(Valiant, 1979)", 20, SOFT)) \
            .arrange(DOWN, buff=0.12)
        both = VGroup(det, perm).arrange(DOWN, buff=0.6).move_to(RIGHT * 0.8 + DOWN * 0.1)
        self.play(FadeIn(det, lag_ratio=0.2))
        self.wait(1.5)
        vp = portrait("valiant", "Leslie Valiant", size=1.0).next_to(perm, RIGHT, buff=0.4)
        self.play(FadeIn(perm, lag_ratio=0.2), FadeIn(vp))
        self.wait(2)
        never = T("Never underestimate a minus sign.", 32, YELLOW).to_edge(DOWN, buff=0.35)
        self.sfx("chime")
        self.play(Write(never))
        self.wait(3)


FLIP_C = ORANGE


class Nature(DScene):
    def construct(self):
        title = T("Nature uses both.", 38).to_edge(UP, buff=0.4)
        self.play(Write(title))
        e = VGroup(*[Circle(radius=0.28, color=BLUE, fill_opacity=0.6) for _ in range(2)]).arrange(RIGHT, buff=0.9)
        e.move_to(LEFT * 3.5 + UP * 0.8)
        el = VGroup(T("electrons (fermions)", 28, BLUE), T("amplitude = determinant", 26, GOOD),
                    T("never in the same state (Pauli)", 24, SOFT)).arrange(DOWN, buff=0.12).next_to(e, DOWN, buff=0.4)
        self.play(FadeIn(e), FadeIn(el, lag_ratio=0.2))
        self.play(e[0].animate.shift(RIGHT * 0.5), e[1].animate.shift(LEFT * 0.5), rate_func=there_and_back, run_time=1)
        like = T("just like ant 1 and ant 2", 22, YELLOW).next_to(el, DOWN, buff=0.25)
        self.play(FadeIn(like))
        self.wait(1.5)
        ph = VGroup(*[Circle(radius=0.28, color=ORANGE, fill_opacity=0.6) for _ in range(2)]).arrange(RIGHT, buff=0.9)
        ph.move_to(RIGHT * 3.5 + UP * 0.8)
        pl = VGroup(T("photons (bosons)", 28, ORANGE), T("amplitude = permanent", 26, BAD),
                    T("happy to bunch together", 24, SOFT)).arrange(DOWN, buff=0.12).next_to(ph, DOWN, buff=0.4)
        self.play(FadeIn(ph), FadeIn(pl, lag_ratio=0.2))
        self.play(ph[0].animate.shift(RIGHT * 0.6), ph[1].animate.shift(LEFT * 0.6), run_time=0.8)
        self.wait(1.5)
        bs = VGroup(T("Boson sampling", 30, YELLOW),
                    T("permanents are hard → simulating many photons is believed hard classically", 22),
                    T("Aaronson & Arkhipov (2011); photonic experiments since", 20, SOFT)).arrange(DOWN, buff=0.12)
        box = SurroundingRectangle(bs, color=YELLOW, buff=0.25, corner_radius=0.15)
        VGroup(bs, box).to_edge(DOWN, buff=0.4)
        self.play(Create(box), FadeIn(bs, lag_ratio=0.2))
        self.wait(3.5)


class Finale(DScene):
    """The cancellation motif one last time, why TCS cares, and the thesis line."""

    def construct(self):
        from act4_proof import is_bad
        own, sw = plus_pairs(), minus_pairs()
        good = [pq for pq in own if not is_bad(pq)]
        bad = [pq for pq in own if is_bad(pq)]
        gv = VGroup(*[pair_icon(*pq, size=0.68, meet=False) for pq in good])
        for ic in gv:
            ic[0].set_stroke(GOOD, 3)
        bv = VGroup(*[pair_icon(*pq, size=0.68, meet=False) for pq in bad])
        sv = VGroup(*[pair_icon(*pq, size=0.68, meet=False) for pq in sw])
        for ic in bv:
            ic[0].set_stroke(BAD, 3)
        for ic in sv:
            ic[0].set_stroke(ORANGE, 3)
        allv = VGroup(*gv, *bv, *sv)
        rng = np.random.default_rng(3)
        order = rng.permutation(len(allv))
        VGroup(*[allv[i] for i in order]).arrange_in_grid(4, 13, buff=0.12).move_to(UP * 0.3)
        signs = VGroup(*[T("+" if k < len(gv) + len(bv) else "−", 28, GOOD if k < len(gv) else
                           BAD if k < len(gv) + len(bv) else ORANGE).next_to(ic, UP, buff=0.02)
                         for k, ic in enumerate(allv)])
        # 0: everything counted, each with a sign
        self.cue(0)
        self.play(LaggedStartMap(FadeIn, allv, lag_ratio=0.02), run_time=2)
        self.play(FadeIn(signs), run_time=0.8)
        # 1: bad ones cancel in pairs; what is left is what we wanted
        self.cue(1)
        partner = [sw.index(tuple(swap_tails(*pq))) for pq in bad]
        for a in range(0, len(bad), 4):
            grp = range(a, min(a + 4, len(bad)))
            self.play(*[bv[i].animate.move_to(sv[partner[i]]) for i in grp],
                      *[signs[len(gv) + i].animate.move_to(signs[len(gv) + len(bad) + partner[i]]) for i in grp],
                      run_time=0.45)
            self.sfx("pop")
            self.play(*[FadeOut(VGroup(bv[i], sv[partner[i]], signs[len(gv) + i],
                                       signs[len(gv) + len(bad) + partner[i]]), scale=0.2) for i in grp], run_time=0.3)
        left = VGroup(*gv)
        self.play(FadeOut(VGroup(*signs[:len(gv)])), left.animate.arrange_in_grid(4, 5, buff=0.15).move_to(LEFT * 1.2),
                  run_time=1)
        tw = T("20", 110, GOOD, weight=BOLD).next_to(left, RIGHT, buff=0.8)
        self.sfx("chime")
        self.play(FadeIn(tw, scale=1.3))
        # 2: counting is usually hopeless
        self.cue(2)
        self.play(FadeOut(left), FadeOut(tw))
        hard = VGroup(T("counting perfect matchings", 34), T("of a general graph", 34),
                      T("#P-complete", 52, BAD, weight=BOLD), T("Valiant, 1979", 28, SOFT)).arrange(DOWN, buff=0.22)
        hard.move_to(LEFT * 3.4 + UP * 0.4)
        self.play(FadeIn(hard[:2]))
        self.cue_at(2, "sharp-P")
        self.sfx("buzz")
        self.play(Write(hard[2]), FadeIn(hard[3]))
        # 3: but non-touching paths / planar matchings -> a determinant
        self.cue(3)
        easy = VGroup(T("non-touching paths,", 34), T("planar matchings", 34),
                      T("one determinant", 52, GOOD, weight=BOLD), T("polynomial time", 28, SOFT)).arrange(DOWN, buff=0.22)
        easy.move_to(RIGHT * 3.4 + UP * 0.4)
        bar = Line(UP * 2.2, DOWN * 1.6, color=GREY_D)
        self.play(Create(bar), FadeIn(easy[:2]))
        self.cue_at(3, "one determinant")
        self.sfx("chime")
        self.play(Write(easy[2]), FadeIn(easy[3]))
        # 4: (option A) Mahajan & Vinay 1997: the determinant itself, by pairing up and cancelling
        self.cue(4)
        self.play(FadeOut(VGroup(hard, easy, bar)), run_time=0.6)
        mv = VGroup(T("Meena Mahajan  &  V. Vinay", 40, YELLOW), T("1997", 30, SOFT)).arrange(DOWN, buff=0.15).move_to(UP * 2.2)
        self.play(FadeIn(mv, shift=DOWN * 0.2), run_time=0.8)
        steps = VGroup(T("the determinant itself:", 30),
                       T("1.  write it as a big signed sum", 28),
                       T("2.  pair each unwanted term with one of opposite sign", 28),
                       T("3.  they cancel", 28, GOOD),
                       T("no division needed", 26, SOFT)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(mv, DOWN, buff=0.5)
        self.cue_at(4, "computed the determinant", lead=0.2)
        self.play(FadeIn(steps[0]), run_time=0.6)
        for k, ph in ((1, "write it"), (2, "pair up"), (3, "let them cancel"), (4, "No division")):
            self.cue_at(4, ph, lead=0.2)
            self.play(FadeIn(steps[k], shift=RIGHT * 0.15), run_time=0.6)
        self.cue_end(4)
        self.wait(0.4)

        # 5: thesis
        self.cue(5)
        thesis = VGroup(T("Determinants can count,", 48), T("because minus signs can cancel.", 48, YELLOW)) \
            .arrange(DOWN, buff=0.3)
        self.play(FadeOut(VGroup(mv, steps)), run_time=0.6)
        self.play(Write(thesis[0]), run_time=1.2)
        self.play(Write(thesis[1]), run_time=1.4)
        self.wait(1.5)
        self.play(FadeOut(thesis))


class Goodbye(DScene):
    """The ants go home safely; 'Thank you for watching.' appears just below while they walk (no other text)."""

    def construct(self):
        lat = Lattice(GRID[0], spacing=1.0, center=UP * 0.45, ny=GRID[1])
        ends = endpoints(lat, labels=False)
        L = ant(ANT1).move_to(lat.p(*A1))
        N = ant(ANT2).move_to(lat.p(*A2))
        thanks = T("Thank you for watching.", 44).to_edge(DOWN, buff=0.7)
        self.cue(0)
        self.play(FadeIn(lat), FadeIn(ends), FadeIn(L), FadeIn(N))
        anims, _ = walk_steps(lat, [(L, GOOD_P, ANT1), (N, GOOD_Q, ANT2)], step_time=0.3)
        for an in anims:
            self.play(an)
        self.play(Wiggle(L), Wiggle(N), run_time=0.8)          # a little wave from a safe distance
        b1, b2 = speech("bye!", L, UP), speech("bye!", N, RIGHT)
        self.sfx("pop")
        self.play(FadeIn(b1, scale=1.3), FadeIn(b2, scale=1.3))
        self.cue(1)                                            # "thank you for watching", just below the ants
        self.play(Write(thanks), run_time=1.2)
        self.cue_end(1)
        self.wait(1.5)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=1.0)


CREDITS = [
    ("Written and produced by", AUTHOR),
    ("Voice", "placeholder AI voice (Kokoro text-to-speech)"),
    ("Lattice paths", "Lindström 1973 · Gessel & Viennot 1985 · Karlin & McGregor 1959"),
    ("Ants on a grid", "A. T. Benjamin & N. T. Cameron, Counting on Determinants (Amer. Math. Monthly, 2005)"),
    ("The D.I.E. method", "A. T. Benjamin & J. J. Quinn, An Alternate Approach to Alternating Sums: A Method to DIE For"),
    ("The quote", "Aigner & Ziegler, Proofs from THE BOOK: \"Lattice paths and determinants\""),
    ("Photo of Paul Erdős", "Kmhkmh, Wikimedia Commons (CC BY 3.0)"),
    ("Book cover", "Proofs from THE BOOK, 6th ed., Springer"),
    ("Animation", "Manim Community; code written with AI assistance"),
]


class Credits(DScene):
    def construct(self):
        rows = VGroup(*[VGroup(T(a, 24, YELLOW), T(b, 22)).arrange(DOWN, buff=0.08) for a, b in CREDITS])
        rows.arrange(DOWN, buff=0.4).next_to(DOWN * 4.2, DOWN, buff=0)
        self.add(rows)
        self.play(rows.animate.shift(UP * (rows.height + 8.4)), run_time=22, rate_func=linear)


class Hope(DScene):
    """Ending (12 Nov plan): why this matters to a computer scientist. Determinants are fast (Gauss),
    the model 'easy' polynomial (algebraic complexity); the permanent drops the signs and is #P-complete
    (Valiant 1979). Counting is usually hard, but the minus signs give hope. Moved here from opening v17."""

    def construct(self):
        import os
        here = os.path.dirname(os.path.abspath(__file__))
        # 0 — fast: O(n^3) by Gaussian elimination (Gauss's portrait at the side), and even faster
        self.cue(0)
        head_c = T("algebraic complexity theory", 30, YELLOW).move_to(UP * 2.55)
        dform = MathTex(r"\det A", "=", r"\sum_{\sigma} \operatorname{sgn}(\sigma)", r"\prod_{i} a_{i\sigma(i)}").scale(0.95)
        dform.move_to(UP * 1.45 + LEFT * 1.6)
        easy = VGroup(T("easy", 28, GOOD), tick(0.3)).arrange(RIGHT, buff=0.15).next_to(dform, RIGHT, buff=0.6)
        speed = VGroup(MathTex(r"O(n^3) \text{ computations using Gaussian elimination}").scale(0.85),
                       MathTex(r"\text{and even faster}", color=GOOD).scale(0.85)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        speed.move_to(DOWN * 0.6 + LEFT * 0.9)
        gpic = Group()
        gf = os.path.join(here, "assets", "portraits", "gauss.jpg")
        if os.path.exists(gf):
            gim = ImageMobject(gf).set_height(2.0)
            gpic = Group(gim, SurroundingRectangle(gim, color=GREY_B, buff=0.02, stroke_width=1.5))
            gpic.next_to(speed, RIGHT, buff=0.6)
            if gpic.get_right()[0] > 6.9:
                gpic.shift(LEFT * (gpic.get_right()[0] - 6.9))
        self.play(Write(dform), run_time=1.0)
        self.cue_at(0, "Gaussian elimination", lead=0.2)
        self.play(FadeIn(speed[0]), FadeIn(gpic), run_time=0.8)
        self.cue_at(0, "even faster", lead=0.2)
        self.play(FadeIn(speed[1], shift=UP * 0.1), run_time=0.6)

        # 1 — algebraic complexity theory: the determinant is the model of an easy polynomial
        self.cue(1)
        self.play(FadeOut(speed), FadeOut(gpic), run_time=0.5)
        self.cue_at(1, "algebraic complexity", lead=0.2)
        self.play(FadeIn(head_c, shift=DOWN * 0.15), run_time=0.7)
        self.cue_at(1, "there, the determinant", lead=0.2)
        self.play(FadeIn(easy), Indicate(dform, color=GOOD, scale_factor=1.05), run_time=0.8)

        # 2 — its twin, the permanent: the same sum without the signs; believed much harder
        self.cue(2)
        pform = MathTex(r"\operatorname{perm} A", "=", r"\sum_{\sigma}", r"\prod_{i} a_{i\sigma(i)}").scale(0.95)
        pform.next_to(dform, DOWN, buff=0.55)
        pform.shift(RIGHT * (dform[1].get_x() - pform[1].get_x()))
        ghost_d = dform.copy()
        self.play(ghost_d.animate.move_to(pform, aligned_edge=LEFT), run_time=0.6)
        strike = Line(ghost_d[2].get_corner(DL), ghost_d[2].get_corner(UR), color=BAD, stroke_width=5)
        self.cue_at(2, "without the minus signs", lead=0.2)
        self.play(Create(strike), run_time=0.5)
        self.play(ReplacementTransform(VGroup(ghost_d, strike), pform), run_time=0.8)
        hard = T("believed hard", 28, BAD).next_to(pform, RIGHT, buff=0.6).align_to(easy, LEFT)
        self.cue_at(2, "believed", lead=0.2)
        self.play(FadeIn(hard), run_time=0.5)

        # 3 — Valiant 1979: the permanent is #P-complete
        self.cue(3)
        vp = Group()
        vf = os.path.join(here, "assets", "portraits", "valiant.jpg")
        if os.path.exists(vf):
            vim = ImageMobject(vf).set_height(1.7)
            vp = Group(vim, SurroundingRectangle(vim, color=GREY_B, buff=0.02, stroke_width=1.5)).move_to(LEFT * 5.5 + DOWN * 1.9)
        vt = VGroup(T("Leslie Valiant, 1979", 26, YELLOW),
                    MathTex(r"\operatorname{perm} \text{ is } \#\mathrm{P}\text{-complete}").scale(0.8),
                    MathTex(r"\#\mathrm{P}: \text{ count the solutions of an NP problem}", color=SOFT).scale(0.62)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        vt.next_to(vp, RIGHT, buff=0.35) if len(vp) else vt.move_to(LEFT * 2.5 + DOWN * 1.85)
        self.cue_at(3, "Leslie Valiant", lead=0.2)
        self.play(FadeIn(vp), FadeIn(vt[0]), run_time=0.7)
        self.cue_at(3, "sharp-P", lead=0.2)
        self.play(FadeIn(vt[1]), run_time=0.6)
        self.cue_at(3, "counting the solutions", lead=0.2)
        self.play(FadeIn(vt[2]), run_time=0.6)
        imp = MathTex(r"\text{efficient algorithm} \;\Rightarrow\; \mathrm{P} = \mathrm{NP} \text{ (and much more)}", color=BAD).scale(0.75)
        imp.move_to(DOWN * 3.45 + RIGHT * 0.6)
        self.cue_at(3, "efficient algorithm", lead=0.2)
        self.play(Write(imp), run_time=1.0)

        # 4 — so counting is usually hard; but the minus signs give hope
        self.cue(4)
        cplx = Group(head_c, easy, pform, hard, vp, vt, imp)
        self.play(FadeOut(cplx), dform.animate.move_to(UP * 0.6).scale(1.25), run_time=1.0)
        sg = SurroundingRectangle(dform[2][2:], color=YELLOW, buff=0.08)   # the sgn(σ)
        self.cue_at(4, "minus signs", lead=0.2)
        self.play(Create(sg), run_time=0.7)

        # 5 — determinants can count, because minus signs can cancel
        self.cue(5)
        last = T("Determinants can count,\nbecause minus signs can cancel.", 40, YELLOW, line_spacing=1.2).move_to(DOWN * 1.6)
        self.sfx("chime")
        self.play(Write(last), run_time=1.6)
        self.cue_end(5)
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
