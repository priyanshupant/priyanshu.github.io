"""Act 8 — The villain explained, and closing (14:00-15:00).

    NonPlanar          Kasteleyn's minus signs fall off a graph with crossings
    VillainExplained   THE PERMANENT: counts everything, cancels nothing
    ThreePanels        free / by design / none; the takeaway; VP vs VNP
    Goodbye            the ants walk home and wave
"""
from common import *
from act7_kasteleyn import board, domino, TILINGS

GOOD_P = [(0, 1), (0, 2), (0, 3), (1, 3), (2, 3)]
GOOD_Q = [(1, 0), (2, 0), (3, 0), (3, 1), (3, 2)]


def k33(scale=1.0, center=ORIGIN):
    top = [center + scale * np.array([x, 1.1, 0]) for x in (-1.6, 0, 1.6)]
    bot = [center + scale * np.array([x, -1.1, 0]) for x in (-1.6, 0, 1.6)]
    edges = VGroup(*[Line(a, b, color=YELLOW, stroke_width=3 * scale + 1) for a in top for b in bot])
    dots = VGroup(*[Dot(p, radius=0.09 * scale + 0.02, color=WHITE) for p in top + bot])
    return VGroup(edges, dots)


class NonPlanar(DScene):
    def construct(self):
        g = k33(1.4, LEFT * 2.5)
        self.play(Create(g[0], lag_ratio=0.1), FadeIn(g[1]), run_time=1.5)
        note = T("a graph that can't be drawn\nwithout crossings", 30, line_spacing=1.15).move_to(RIGHT * 3.3 + UP * 1.5)
        self.play(FadeIn(note))
        self.wait(1)
        signs = VGroup(*[T("−", 48, ORANGE, weight=BOLD).move_to(e.get_center() + UP * 0.15)
                         for e in g[0][::2]])
        self.play(LaggedStartMap(FadeIn, signs, lag_ratio=0.15, scale=2), run_time=1.2)
        self.wait(0.5)
        self.sfx("whoosh")
        self.play(LaggedStart(*[sg.animate.shift(DOWN * 4.5).rotate(PI * 1.5).set_opacity(0) for sg in signs],
                              lag_ratio=0.15), run_time=2, rate_func=rush_into)
        fail = T("no way to place the minus signs\nso everything lines up", 28, BAD, line_spacing=1.15) \
            .next_to(note, DOWN, buff=0.6)
        self.sfx("buzz")
        self.play(FadeIn(fail))
        self.wait(3)


class VillainExplained(DScene):
    def construct(self):
        card = villain_card("THE PERMANENT", 80)
        self.play(FadeIn(card, scale=1.2))
        self.wait(1)
        self.play(card.animate.shift(UP * 1.4))
        sub = T("counts everything, cancels nothing", 40, INK).next_to(card, DOWN, buff=0.7)
        self.play(Write(sub))
        f = T("ad + bc + …   (no minus signs anywhere)", 30, SOFT).next_to(sub, DOWN, buff=0.6)
        self.play(FadeIn(f))
        self.wait(3)


class ThreePanels(DScene):
    def construct(self):
        q = T("What are the minus signs doing?", 36, YELLOW).to_edge(UP, buff=0.5)
        self.play(Write(q))
        icons = [
            pair_icon(GOOD_P, GOOD_Q, size=1.2, meet=False),
            VGroup(b := board(2, 3, 0.5), *[domino(b.sq, x, y, 0.5) for x, y in TILINGS[0]]),
            k33(0.6),
        ]
        heads = ["Paths (LGV)", "Dominoes, flat grids\n(Kasteleyn)", "General graphs\n(the permanent)"]
        tags = [("cancellation for free", GOOD), ("cancellation by design", YELLOW), ("no cancellation", BAD)]
        panels = VGroup()
        for ic, hd, (tg, col) in zip(icons, heads, tags):
            box = RoundedRectangle(corner_radius=0.2, width=4.2, height=4.4, color=col, stroke_width=3)
            ic.move_to(box.get_center() + UP * 0.8)
            h = T(hd, 24, line_spacing=1.1).next_to(ic, DOWN, buff=0.35)
            t = T(tg, 24, col).move_to(box.get_bottom() + UP * 0.45)
            panels.add(VGroup(box, ic, h, t))
        panels.arrange(RIGHT, buff=0.25).next_to(q, DOWN, buff=0.4)
        for p in panels:
            self.play(FadeIn(p, shift=UP * 0.3), run_time=0.8)
            self.wait(1.5)
        self.wait(1)
        line = T("Minus signs are a cancellation engine.", 40, YELLOW, weight=BOLD)
        self.play(FadeOut(panels), FadeOut(q))
        self.sfx("chime")
        self.play(Write(line), run_time=1.5)
        self.wait(1)
        d = T("The determinant has one. The permanent doesn't.", 30).next_to(line, DOWN, buff=0.5)
        self.play(FadeIn(d))
        self.wait(2)
        oq = VGroup(T("Open question", 26, SOFT),
                    T("Are minus signs necessary for fast computation?", 30),
                    T("(Valiant: VP vs VNP)", 26, BLUE)).arrange(DOWN, buff=0.2)
        box = SurroundingRectangle(oq, buff=0.35, corner_radius=0.15, color=BLUE)
        VGroup(oq, box).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(box), FadeIn(oq, lag_ratio=0.2))
        self.wait(3)


class Goodbye(DScene):
    def construct(self):
        lat = Lattice(4, spacing=1.3, center=DOWN * 0.3)
        ends = endpoints(lat)
        a1 = ant(ANT1).move_to(lat.p(*A1))
        a2 = ant(ANT2).move_to(lat.p(*A2))
        self.play(FadeIn(lat), FadeIn(ends), FadeIn(a1), FadeIn(a2))
        anims, _ = walk_steps(lat, [(a1, GOOD_P[:-1], ANT1), (a2, GOOD_Q[:-1], ANT2)], step_time=0.5)
        for an in anims:
            self.play(an)
        # turn to face each other and wave
        self.play(Rotate(a2, PI / 2, about_point=a2.get_center()), run_time=0.3)
        bye1 = T("bye!", 30, ANT1).next_to(a1, UP, buff=0.2)
        bye2 = T("bye!", 30, ANT2).next_to(a2, RIGHT, buff=0.2)
        self.play(a1.animate.shift(UP * 0.2), a2.animate.shift(UP * 0.2), rate_func=there_and_back, run_time=0.4)
        self.sfx("pop")
        self.play(FadeIn(bye1, scale=1.4), FadeIn(bye2, scale=1.4))
        self.play(Wiggle(a1), Wiggle(a2))
        self.wait(1)
        home = T("Twenty different ways home.", 32).to_edge(UP, buff=0.4)
        self.play(FadeIn(home))
        self.wait(2)
        self.play(*[FadeOut(x) for x in self.mobjects])
        thanks = T("Thanks for watching.", 54)
        sub = T("How Determinants Can Count · DepthTCS 2026", 26, SOFT).next_to(thanks, DOWN, buff=0.4)
        self.play(Write(thanks))
        self.play(FadeIn(sub))
        self.wait(3)
