"""Act 0 — opening v39 (12 Nov): the TCS set-up, with nothing about the puzzle before the puzzle.

    decide (is there one?) vs count (how many?): counting is usually much harder, #P (Valiant 1979);
    yet one famous sum over n! terms is easy: the determinant (school ad - bc, then the general form), O(n^3);
    drop its signs: the permanent, #P-complete; so the minus signs make it easy... but counting never subtracts:
    can a determinant count anything real? Surprisingly often: title; 'let's start with a simple puzzle'.
(previous: act0_opening_v38.py.bak = four-ants set-up; act0_opening_v36.py.bak = v20 school/uses intro)
"""
from common import *


class Opening(DScene):
    def construct(self):
        # 0: two questions about any problem: is there a solution? how many?
        self.cue(0)
        q1 = VGroup(T("decide", 34, weight=BOLD), T("is there a solution?", 28, SOFT)).arrange(DOWN, buff=0.2)
        q2 = VGroup(T("count", 34, weight=BOLD), T("how many solutions?", 28, SOFT)).arrange(DOWN, buff=0.2)
        VGroup(q1, q2).arrange(RIGHT, buff=2.4).move_to(UP * 0.6)
        self.cue_at(0, "is there a solution", lead=0.2)
        self.play(FadeIn(q1, shift=UP * 0.15), run_time=0.7)
        self.cue_at(0, "how many", lead=0.2)
        self.play(FadeIn(q2, shift=UP * 0.15), run_time=0.7)

        # 1: counting is usually much harder; even when deciding is easy, counting can be #P-hard (Valiant 1979)
        self.cue(1)
        e1 = VGroup(T("often easy", 28, GOOD), tick(0.3)).arrange(RIGHT, buff=0.15).next_to(q1, DOWN, buff=0.5)
        e2 = VGroup(T("#P-hard", 30, BAD, weight=BOLD), T("Valiant, 1979", 22, SOFT)).arrange(DOWN, buff=0.12) \
            .next_to(q2, DOWN, buff=0.45)
        self.cue_at(1, "much harder", lead=0.2)
        self.play(q2[0].animate.set_color(BAD), run_time=0.5)
        self.cue_at(1, "finding one", lead=0.2)
        self.play(FadeIn(e1), run_time=0.6)
        self.cue_at(1, "sharp-P", lead=0.2)
        self.play(FadeIn(e2, shift=UP * 0.1), run_time=0.7)

        # 2: but one famous sum is easy: the determinant. school ad - bc; in general n! signed terms; O(n^3)
        self.cue(2)
        self.play(FadeOut(VGroup(q1, q2, e1, e2)), run_time=0.6)
        m2 = Matrix([["a", "b"], ["c", "d"]], h_buff=1.0, v_buff=0.8).scale(1.0)
        d2 = VGroup(MathTex(r"\det").scale(1.3), m2, MathTex("=", "ad", "-", "bc").scale(1.3)).arrange(RIGHT, buff=0.3)
        d2[2][2].set_color(BAD)
        d2.move_to(UP * 0.4)
        self.cue_at(2, "school", lead=0.3)
        self.play(FadeIn(d2[:2]), run_time=0.5)
        self.play(Write(d2[2]), run_time=0.8)
        leib = MathTex(r"\det A", "=", r"\sum_{\sigma}", r"\operatorname{sgn}(\sigma)", r"\prod_{i} a_{i\sigma(i)}").scale(1.2)
        leib.move_to(UP * 1.4)
        self.cue_at(2, "In general", lead=0.2)
        self.play(FadeOut(d2), Write(leib), run_time=1.2)
        br = Brace(leib[2:], DOWN, color=SOFT)
        nf = MathTex(r"n! \text{ terms}", color=SOFT).scale(0.8).next_to(br, DOWN, buff=0.1)
        self.play(GrowFromCenter(br), FadeIn(nf), run_time=0.6)
        fast = MathTex(r"O(n^3)", r"\text{ by Gaussian elimination}", color=GOOD).scale(0.9).next_to(nf, DOWN, buff=0.35)
        self.cue_at(2, "Gaussian elimination", lead=0.2)
        self.play(FadeIn(fast, shift=UP * 0.1), run_time=0.7)

        # 3: drop the signs: the permanent, the same sum, #P-complete. The only difference: the minus signs.
        self.cue_end(2)
        self.play(FadeOut(VGroup(br, nf)), fast.animate.scale(0.8).next_to(leib, DOWN, buff=0.3), run_time=0.6)
        ghost = leib.copy()
        self.play(ghost.animate.shift(DOWN * 2.3), run_time=0.7)
        self.cue(3)
        strike = Line(ghost[3].get_corner(DL), ghost[3].get_corner(UR), color=BAD, stroke_width=6)
        self.cue_at(3, "Drop its signs", lead=0.2)
        self.play(Create(strike), run_time=0.5)
        perm = MathTex(r"\operatorname{perm} A", "=", r"\sum_{\sigma}", r"\prod_{i} a_{i\sigma(i)}").scale(1.2)
        perm.move_to(ghost)
        perm.shift(RIGHT * (leib[1].get_x() - perm[1].get_x()))       # "=" under "="
        self.play(ReplacementTransform(VGroup(ghost, strike), perm), run_time=0.8)
        hard = T("#P-complete", 30, BAD, weight=BOLD).next_to(perm, DOWN, buff=0.3)
        self.cue_at(3, "sharp-P complete", lead=0.2)
        self.play(FadeIn(hard), run_time=0.5)
        sgbox = SurroundingRectangle(leib[3], color=YELLOW, buff=0.1)
        self.cue_at(3, "only difference", lead=0.2)
        self.play(Create(sgbox), run_time=0.6)

        # 4: so the minus signs make it easy. But counting never subtracts: can a determinant count anything real?
        self.cue(4)
        nt = MathTex(r"-3", r"\text{ solutions}").scale(1.0).to_edge(DOWN, buff=0.45)
        bx = SurroundingRectangle(nt, buff=0.12)
        x = VGroup(Line(bx.get_corner(DL), bx.get_corner(UR), color=BAD, stroke_width=6),
                   Line(bx.get_corner(UL), bx.get_corner(DR), color=BAD, stroke_width=6))
        self.cue_at(4, "never subtracts", lead=0.2)
        self.play(FadeIn(nt), run_time=0.5)
        self.play(Create(x), run_time=0.4)
        self.cue_at(4, "count anything", lead=0.2)
        self.play(Indicate(VGroup(leib, sgbox), color=YELLOW, scale_factor=1.05), run_time=0.9)

        # 5: surprisingly often, yes. Today: how determinants can count (title)
        self.cue(5)
        self.cue_at(5, "how determinants", lead=0.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        title = T("How Determinants Can Count", 50, weight=BOLD)
        self.sfx("chime")
        self.play(Write(title), run_time=1.3)

        # 6: "let's start with a simple puzzle": the subtitle under the title
        self.cue(6)
        sub = T("First, a simple puzzle", 32, SOFT).next_to(title, DOWN, buff=0.45)
        self.cue_at(6, "simple puzzle", lead=0.4)
        self.play(FadeIn(sub, shift=UP * 0.15), run_time=0.7)
        self.cue_end(6)
        self.wait(0.8)
        self.play(FadeOut(VGroup(title, sub)), run_time=0.8)
