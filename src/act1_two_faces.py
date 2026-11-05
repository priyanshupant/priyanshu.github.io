"""Act 1 — Two faces of the determinant (1:00-2:15).

    AreaView      unit square -> parallelogram under [[2,1],[1,2]]: area = ad - bc
    TwoFormulas   ad - bc vs ad + bc, THE PERMANENT, fast vs believed hard
"""
from common import *
from act0_cold_open import matrix_mob


class AreaView(DScene):
    def construct(self):
        plane = NumberPlane(x_range=[-8, 8], y_range=[-5, 5],
                            background_line_style={"stroke_opacity": 0.5})
        self.play(Create(plane, lag_ratio=0.05), run_time=1.5)
        sq = Polygon(ORIGIN, RIGHT, RIGHT + UP, UP, color=YELLOW, fill_opacity=0.5, stroke_width=3)
        i_hat = Arrow(ORIGIN, RIGHT, buff=0, color=GREEN)
        j_hat = Arrow(ORIGIN, UP, buff=0, color=RED)
        self.play(FadeIn(sq), GrowArrow(i_hat), GrowArrow(j_hat))
        area1 = T("area = 1", 30, YELLOW).add_background_rectangle().move_to(RIGHT * 0.5 + DOWN * 0.6)
        self.play(FadeIn(area1))
        self.wait(1)

        m = matrix_mob([["a", "b"], ["c", "d"]], size=40)
        nums = matrix_mob([[2, 1], [1, 2]], size=40)
        box = VGroup(m, T("=", 40), nums).arrange(RIGHT, buff=0.3)
        box.add_background_rectangle(opacity=0.85, buff=0.2).to_corner(UL, buff=0.4)
        self.play(FadeIn(box))
        self.wait(1)
        self.play(FadeOut(area1))
        mat = [[2, 1], [1, 2]]
        self.sfx("whoosh")
        self.play(ApplyMatrix(mat, plane), ApplyMatrix(mat, sq),
                  ApplyMatrix(mat, i_hat), ApplyMatrix(mat, j_hat), run_time=3)
        self.wait(1)
        area = VGroup(T("area = ad − bc", 34, YELLOW),
                      T("= 2·2 − 1·1 = 3", 34, YELLOW)).arrange(DOWN, aligned_edge=LEFT)
        area.add_background_rectangle(opacity=0.85, buff=0.15).to_corner(UR, buff=0.5)
        self.play(Write(area))
        self.wait(2)
        credit = T("(3Blue1Brown has a lovely video on this picture)", 24, SOFT) \
            .add_background_rectangle(opacity=0.85).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(credit))
        self.wait(3)
        # area[0] is the background rectangle, area[1] "area = ad − bc", area[2] the numbers
        formula = T("ad − bc", 72)
        self.play(*[FadeOut(x) for x in (plane, sq, i_hat, j_hat, box, credit, area[0], area[2])],
                  ReplacementTransform(area[1], formula), run_time=1.2)
        self.wait(1)


class TwoFormulas(DScene):
    def construct(self):
        det = T("ad − bc", 72)
        self.add(det)
        self.wait(1)
        perm = T("ad + bc", 72)
        self.play(det.animate.shift(LEFT * 3), FadeIn(perm.shift(RIGHT * 3), shift=LEFT * 0.5))
        self.wait(1)
        minus, plus = det[2], perm[2]
        self.play(minus.animate.set_color(YELLOW).scale(1.5), run_time=0.6)
        self.play(minus.animate.scale(1 / 1.5), run_time=0.4)
        self.play(plus.animate.set_color(YELLOW).scale(1.5), run_time=0.6)
        self.play(plus.animate.scale(1 / 1.5), run_time=0.4)
        self.wait(1.5)
        lab_d = T("determinant", 30, SOFT).next_to(det, UP, buff=0.4)
        self.play(FadeIn(lab_d))
        self.wait(1)

        # the villain
        dark = FullScreenRectangle(fill_color=BLACK, fill_opacity=0.75, stroke_width=0)
        card = villain_card("THE PERMANENT", 84)
        self.play(FadeIn(dark), run_time=0.8)
        self.sfx("rumble")
        self.play(FadeIn(card, scale=1.6), run_time=0.5, rate_func=rush_into)
        self.play(card.animate.shift(LEFT * 0.08), rate_func=wiggle, run_time=0.5)
        self.wait(2)
        lab_p = T("permanent", 30, BAD).next_to(perm, UP, buff=0.4)
        self.play(FadeOut(dark), card.animate.scale(0.35).next_to(lab_p, UP, buff=0.25), FadeIn(lab_p))
        self.wait(1)

        fast = VGroup(T("fast to compute", 30, GOOD),
                      T("your laptop: a blink", 24, SOFT)).arrange(DOWN, buff=0.15)
        hard = VGroup(T("believed hopelessly hard", 30, BAD),
                      T("Valiant, 1979", 24, SOFT)).arrange(DOWN, buff=0.15)
        fast.next_to(det, DOWN, buff=0.7)
        hard.next_to(perm, DOWN, buff=0.7)
        self.play(FadeIn(fast, shift=UP * 0.2))
        self.wait(2)
        self.play(FadeIn(hard, shift=UP * 0.2))
        self.wait(3)
        same = T("Same formula. Only the minus sign differs.", 30).to_edge(DOWN, buff=0.6)
        self.play(Write(same))
        self.wait(2)
        qm = T("?", 120, YELLOW, weight=BOLD).move_to(UP * 0.1)
        self.sfx("chime")
        self.play(FadeIn(qm, scale=2))
        self.wait(3)
        q = T("What are the minus signs doing?", 36, YELLOW).move_to(UP * 3)
        self.play(FadeOut(lab_d), FadeOut(lab_p), FadeOut(card), Write(q))
        self.wait(3)
        self.play(*[FadeOut(x) for x in self.mobjects])
