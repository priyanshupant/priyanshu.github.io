"""Additions for review (8 Nov): each is its own scene, so removing one = deleting its line in pacing.py.

    QuoteOpen   (option D) Axler 1995 "Down with Determinants!" vs Wigderson
    PuzzleCard  (option E) chapter card before the puzzle
    ExCard1-3   (option E) chapter cards for the examples (hexagon + boxes, mountains, Aztec)
    EndCard     (option E) chapter card before the map / finale
"""
from common import *


AXLER = "“Determinants are difficult, non-intuitive,\nand often defined without motivation.”"
WIGDERSON = "“The determinant is undoubtedly the most important\npolynomial function in mathematics.”"


class QuoteOpen(DScene):
    def construct(self):
        # 0: Axler's title
        self.cue(0)
        ttl = T("Down with Determinants!", 46, BAD, weight=BOLD).move_to(UP * 2.3)
        who1 = T("Sheldon Axler, 1995", 26, SOFT).next_to(ttl, DOWN, buff=0.2)
        self.play(Write(ttl), run_time=1.2)
        self.play(FadeIn(who1), run_time=0.5)
        # 1: what he says
        self.cue(1)
        q1 = T(AXLER, 32, line_spacing=1.3).next_to(who1, DOWN, buff=0.5)
        self.play(FadeIn(q1, lag_ratio=0.02), run_time=2.2)
        # 2: Wigderson's view
        self.cue(2)
        top = VGroup(ttl, who1, q1)
        self.play(top.animate.scale(0.75).set_opacity(0.45).to_edge(UP, buff=0.35), run_time=0.8)
        q2 = T(WIGDERSON, 32, GOOD, line_spacing=1.3).move_to(DOWN * 0.9)
        who2 = T("Avi Wigderson", 26, SOFT).next_to(q2, DOWN, buff=0.3)
        self.play(FadeIn(q2, lag_ratio=0.02), run_time=2.2)
        self.play(FadeIn(who2), run_time=0.5)
        # 3: so which is it?
        self.cue(3)
        self.cue_at(3, "Let's", lead=0.2)
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=0.8)


def chapter_card(scene, title, sub=None):
    t = T(title, 50, weight=BOLD)
    g = VGroup(t)
    if sub:
        g.add(T(sub, 30, SOFT))
        g.arrange(DOWN, buff=0.3)
    scene.sfx("whoosh")
    scene.play(Write(t), *([FadeIn(g[1])] if sub else []), run_time=1.0)
    scene.wait(0.9)
    scene.play(FadeOut(g), run_time=0.5)


class PuzzleCard(DScene):
    def construct(self):
        chapter_card(self, "A simple puzzle")


class ExCard1(DScene):
    def construct(self):
        chapter_card(self, "Example 1", "tilings of a hexagon")


class ExCard2(DScene):
    def construct(self):
        chapter_card(self, "Example 2", "mountain ranges")


class ExCard3(DScene):
    def construct(self):
        chapter_card(self, "Example 2", "the Aztec diamond")


class EndCard(DScene):
    def construct(self):
        chapter_card(self, "Why minus signs count")
