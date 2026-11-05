"""Act 0 — A short history (Script v2, 0:00-1:30).

    History    timeline 1683-1812 with portraits; Seki "10 years earlier"
    Montage    four places determinants show up
    Title      title card, then the Leibniz-Newton bridge
"""
from common import *

EVENTS = [  # (year, key, name, line)
    (1683, "seki", "Seki Takakazu", "determinants up to 5×5, by hand"),
    (1693, "leibniz", "Leibniz", "first European determinant"),
    (1750, "cramer", "Cramer", "Cramer's rule"),
    (1772, "laplace", "Laplace", "with Vandermonde: computing them"),
    (1801, "gauss", "Gauss", "names it \"determinant\""),
    (1812, "cauchy", "Cauchy", "the modern meaning"),
]


class History(DScene):
    def construct(self):
        title = T("The determinant: a short history", 40).to_edge(UP, buff=0.4)
        self.play(Write(title))
        x0, x1 = -5.5, 5.5
        line = Line(LEFT * 6.6, RIGHT * 6.6, color=GREY_C).shift(DOWN * 0.6)
        self.play(Create(line))
        xs = np.linspace(x0, x1, len(EVENTS))
        cards = []
        for (year, key, name, what), x in zip(EVENTS, xs):
            tickm = Line(UP * 0.12, DOWN * 0.12, color=GREY_C).move_to([x, -0.6, 0])
            yr = T(str(year), 26, YELLOW).next_to(tickm, DOWN, buff=0.15)
            card = portrait(key, name, size=1.15)
            card[1].scale(0.8)
            card[1].next_to(card[0], DOWN, buff=0.1)
            card.move_to([x, 1.25, 0])
            words = what.split(" ")
            half = (len(words) + 1) // 2
            note = T(" ".join(words[:half]) + "\n" + " ".join(words[half:]), 16, SOFT,
                     line_spacing=1.0).next_to(yr, DOWN, buff=0.15)
            self.play(Create(tickm), FadeIn(yr), FadeIn(card, shift=DOWN * 0.2), FadeIn(note), run_time=0.8)
            cards.append((card, yr))
            if key == "leibniz":
                arc = CurvedArrow(cards[0][1].get_bottom() + DOWN * 1.0, yr.get_bottom() + DOWN * 1.0,
                                  angle=PI / 3, color=ANT3)
                ten = T("10 years earlier", 22, ANT3).next_to(arc, DOWN, buff=0.08)
                self.play(Create(arc), FadeIn(ten))
                self.wait(2)
            else:
                self.wait(0.8)
        gc = T("Gauss gave it a name. Cauchy gave it a meaning.", 28, YELLOW).to_edge(DOWN, buff=0.4)
        self.play(Write(gc))
        self.wait(3)
        src = T("timeline: MacTutor History of Mathematics", 16, GREY_C).to_corner(DR, buff=0.15)
        self.play(FadeIn(src))
        self.wait(2)


class Montage(DScene):
    def construct(self):
        cells = []
        # 1. equations
        eq = VGroup(T("2x + y = 3", 30), T("x + 2y = 3", 30)).arrange(DOWN, aligned_edge=LEFT)
        eqn = VGroup(eq, T("solvable  ⇔  det ≠ 0", 24, YELLOW)).arrange(DOWN, buff=0.35)
        cells.append((eqn, "equations"))
        # 2. area
        sq = Polygon(ORIGIN, RIGHT, RIGHT + UP, UP, color=YELLOW, fill_opacity=0.4)
        pg = Polygon(ORIGIN, RIGHT * 2 + UP, RIGHT * 3 + UP * 3, RIGHT + UP * 2, color=BLUE, fill_opacity=0.3)
        area = VGroup(VGroup(sq, pg).scale(0.55), T("area × |det|", 24, YELLOW)).arrange(DOWN, buff=0.3)
        cells.append((area, "area and volume"))
        # 3. eigenvalues
        eig = VGroup(T("det(A − λI) = 0", 30), T("eigenvalues", 24, YELLOW)).arrange(DOWN, buff=0.35)
        cells.append((eig, "eigenvalues"))
        # 4. change of variables
        cv = VGroup(T("dx dy = |det J| du dv", 28), T("change of variables", 24, YELLOW)).arrange(DOWN, buff=0.35)
        cells.append((cv, "integrals"))
        g = Group()
        for mob, lab in cells:
            box = RoundedRectangle(corner_radius=0.2, width=5.6, height=2.8, color=GREY_C)
            g.add(VGroup(box, mob.move_to(box)))
        g.arrange_in_grid(2, 2, buff=0.4)
        for c in g:
            self.play(FadeIn(c, scale=0.9), run_time=0.8)
            self.wait(1.2)
        self.wait(1.5)
        self.play(FadeOut(g))
        today = VGroup(T("Today: something different.", 38),
                       T("Determinants can count.", 44, YELLOW)).arrange(DOWN, buff=0.4)
        self.play(Write(today[0]))
        self.wait(1)
        self.play(Write(today[1]))
        self.wait(2)
        self.play(FadeOut(today))


class Title(DScene):
    def construct(self):
        title = T("How Determinants Can Count", 60, weight=BOLD)
        self.sfx("whoosh")
        self.play(Write(title), run_time=1.5)
        self.wait(2)
        self.play(title.animate.scale(0.5).to_edge(UP, buff=0.4))
        L = scholar("leibniz", 2.2).move_to(LEFT * 2.5 + DOWN * 0.5)
        N = scholar("newton", 2.2).move_to(RIGHT * 2.5 + DOWN * 0.5)
        self.play(FadeIn(L, shift=RIGHT), FadeIn(N, shift=LEFT))
        cap = T("Leibniz and Newton: a small disagreement about calculus", 28, SOFT).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(cap))
        self.play(L.animate.shift(RIGHT * 1.2), N.animate.shift(LEFT * 1.2), run_time=0.6)
        b1, b2 = speech("dy/dx!", L), speech("ẋ!", N)
        self.sfx("alert")
        self.play(FadeIn(b1, scale=1.3), FadeIn(b2, scale=1.3), run_time=0.4)
        self.wait(1.2)
        self.play(L.animate.shift(LEFT * 1.6), N.animate.shift(RIGHT * 1.6), FadeOut(b1), FadeOut(b2), run_time=0.7)
        self.wait(2)
