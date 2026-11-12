"""Act 0 — opening v50 (12 Nov, Priyanshu's plan): a 'Determinant' card first; we've all seen it; the Leibniz
formula (n! signed terms); for a computer scientist it is fast anyway (O(n^3)); its twin the permanent (same sum,
no signs) is #P-complete (Valiant 1979); counting is usually hard, yet determinants can sometimes count; today:
how is this possible -> title; 'let's start with a simple puzzle'.
(previous: act0_opening_v42.py.bak = title-in-the-middle school intro)
"""
import os
from common import *

HERE = os.path.dirname(os.path.abspath(__file__))


def framed(path, h):
    im = ImageMobject(path).set_height(h)
    return Group(im, SurroundingRectangle(im, color=GREY_B, buff=0.02, stroke_width=1.5))


class Opening(DScene):
    def construct(self):
        # the opening card
        card = T("Determinant", 64, weight=BOLD)
        self.play(Write(card), run_time=1.2)

        # 0: we've all seen the determinant: in school, in linear algebra, in algorithms
        self.cue(0)
        tags = VGroup(T("school", 30, SOFT), T("linear algebra", 30, SOFT), T("algorithms", 30, SOFT)) \
            .arrange(RIGHT, buff=0.9).next_to(card, DOWN, buff=0.7)
        for k, w in enumerate(("school", "linear algebra", "algorithms")):
            self.cue_at(0, w, lead=0.15)
            self.play(FadeIn(tags[k], shift=UP * 0.15), run_time=0.45)

        # 1: in general, Leibniz's formula: a sum over all permutations, each with a sign
        self.cue(1)
        leib = MathTex(r"\det A", "=", r"\sum_{\sigma \in S_n}", r"\operatorname{sgn}(\sigma)", r"\prod_{i=1}^{n} a_{i\sigma(i)}").scale(1.2)
        leib.move_to(UP * 1.6)
        self.play(FadeOut(tags), FadeOut(card, shift=UP * 0.3), run_time=0.7)
        self.cue_at(1, "Leibniz", lead=0.2)
        self.play(Write(leib), run_time=1.4)
        br = Brace(leib[2:], DOWN, color=SOFT)
        nf = MathTex(r"n! \text{ terms}", color=SOFT).scale(0.85).next_to(br, DOWN, buff=0.1)
        self.cue_at(1, "sign", lead=0.2)
        self.play(Indicate(leib[3], color=YELLOW, scale_factor=1.15), run_time=0.8)

        # 2: for a computer scientist: n! terms, and yet computed fast (Gaussian elimination, about n^3 steps)
        self.cue(2)
        self.cue_at(2, "factorial", lead=0.2)
        self.play(GrowFromCenter(br), FadeIn(nf), run_time=0.7)
        fast = VGroup(MathTex(r"O(n^3)", color=GOOD).scale(1.1), T("Gaussian elimination", 26, GOOD)).arrange(DOWN, buff=0.12)
        fast.next_to(nf, DOWN, buff=0.4)
        gpic = framed(os.path.join(HERE, "assets", "portraits", "gauss.jpg"), 1.7)
        gpic.next_to(fast, RIGHT, buff=0.6)
        self.cue_at(2, "efficiently", lead=0.2)
        self.play(FadeIn(fast, shift=UP * 0.1), FadeIn(gpic), run_time=0.8)

        # 3: its twin, the permanent: the same sum without the signs. Valiant 1979: #P-complete
        self.cue(3)
        self.play(FadeOut(VGroup(br, nf, fast)), FadeOut(gpic), run_time=0.6)
        ghost = leib.copy()
        self.play(ghost.animate.shift(DOWN * 2.0), run_time=0.7)
        strike = Line(ghost[3].get_corner(DL), ghost[3].get_corner(UR), color=BAD, stroke_width=6)
        self.cue_at(3, "without the minus signs", lead=0.2)
        self.play(Create(strike), run_time=0.5)
        perm = MathTex(r"\operatorname{perm} A", "=", r"\sum_{\sigma \in S_n}", r"\prod_{i=1}^{n} a_{i\sigma(i)}").scale(1.2)
        perm.move_to(ghost)
        perm.shift(RIGHT * (leib[1].get_x() - perm[1].get_x()))       # "=" under "="
        self.play(ReplacementTransform(VGroup(ghost, strike), perm), run_time=0.8)
        vp = framed(os.path.join(HERE, "assets", "portraits", "valiant.jpg"), 1.6).move_to(LEFT * 5.3 + DOWN * 2.55)
        vt = VGroup(T("Leslie Valiant, 1979", 26, YELLOW),
                    MathTex(r"\operatorname{perm} \text{ is } \#\mathrm{P}\text{-complete}", color=BAD).scale(0.85),
                    MathTex(r"\#\mathrm{P}: \text{ counting the solutions of NP problems}", color=SOFT).scale(0.62)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(vp, RIGHT, buff=0.35)
        self.cue_at(3, "Leslie Valiant", lead=0.2)
        self.play(FadeIn(vp), FadeIn(vt[0]), run_time=0.7)
        self.cue_at(3, "sharp-P", lead=0.2)
        self.play(FadeIn(vt[1]), run_time=0.6)
        self.cue_at(3, "counting the solutions", lead=0.2)
        self.play(FadeIn(vt[2]), run_time=0.6)

        # 4: so counting is usually hard; even so, determinants can sometimes count; today: how is this possible?
        self.cue(4)
        sg = SurroundingRectangle(leib[3], color=YELLOW, buff=0.1)
        self.cue_at(4, "determinants can sometimes count", lead=0.2)
        self.play(Create(sg), FadeOut(VGroup(perm, vt)), FadeOut(vp), run_time=0.8)
        self.cue_at(4, "how this is possible", lead=0.3)
        title = T("How Determinants Can Count", 50, weight=BOLD)
        self.play(FadeOut(VGroup(leib, sg)), run_time=0.5)
        self.sfx("chime")
        self.play(Write(title), run_time=1.3)

        # 5: let's start with a simple puzzle (subtitle under the title)
        self.cue(5)
        sub = T("First, a simple puzzle", 32, SOFT).next_to(title, DOWN, buff=0.45)
        self.cue_at(5, "simple puzzle", lead=0.4)
        self.play(FadeIn(sub, shift=UP * 0.15), run_time=0.7)
        self.cue_end(5)
        self.wait(0.8)
        self.play(FadeOut(VGroup(title, sub)), run_time=0.8)
