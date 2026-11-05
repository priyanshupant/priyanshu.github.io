"""Act 0 (v7) - the opening.

Narration "Opening" (one slide per line):
 0 the determinant you met in school: a d - b c
 1 what we used it for: solve equations / find areas / undo a matrix
 2 the turn: to me, the most surprising place is counting
 3 ask a child: one, two, cha-cha-cha
 4 ask Leslie Valiant: #P-complete (counting perfect matchings)
 5 and yet a single determinant counts: routes, hexagon tilings, chessboard dominoes
 6 let's see how, starting with two ants  (hands over to Hook: same grid + ants)
"""
import os
from itertools import combinations

from common import *
from act0_hook import GRID_HOOK
from act3_two_walkers import GOOD_P, GOOD_Q
from act6_hexagon import tiling as hex_tiling, outline as hex_outline, SHOW
from act6b_disguises import az_mob, AZ
from act7_kasteleyn import board, domino, random_tiling

HERE = os.path.dirname(os.path.abspath(__file__))
PANEL_W = 3.6


def panel_frame(center):
    return RoundedRectangle(corner_radius=0.15, width=PANEL_W, height=2.9, stroke_color=DIM,
                            stroke_width=2).move_to(center)


def perfect_matchings(n, E):
    out = []

    def rec(left, cur):
        if not left:
            out.append(list(cur))
            return
        v = min(left)
        for a, b in E:
            if v in (a, b):
                w = b if a == v else a
                if w in left and w != v:
                    rec(left - {v, w}, cur + [(a, b)])
    rec(frozenset(range(n)), [])
    return out


class Opening(DScene):
    def construct(self):
        # 0: a d - b c
        self.cue(0)
        m = matrix_mob([["a", "b"], ["c", "d"]], size=80).shift(LEFT * 2.6)
        c = m.cells
        g = Line(c[0].get_center(), c[3].get_center(), color=GOOD, stroke_width=12).set_opacity(0.55)
        r = Line(c[1].get_center(), c[2].get_center(), color=BAD, stroke_width=12).set_opacity(0.55)
        eq = T("=", 70).next_to(m, RIGHT, buff=0.6)
        ad = T("a d", 70, GOOD).next_to(eq, RIGHT, buff=0.4)
        mi = T("−", 70).next_to(ad, RIGHT, buff=0.35)
        bc = T("b c", 70, BAD).next_to(mi, RIGHT, buff=0.35)
        dl = T("det", 60, YELLOW).next_to(m, LEFT, buff=0.35)
        self.play(FadeIn(m), FadeIn(dl), run_time=0.8)
        self.cue_at(0, "a d minus", lead=0.3)
        self.play(Create(g), FadeIn(eq), FadeIn(ad, shift=RIGHT * 0.2), run_time=0.7)
        self.play(Create(r), FadeIn(mi), FadeIn(bc, shift=RIGHT * 0.2), run_time=0.7)
        formula = VGroup(dl, m, g, r, eq, ad, mi, bc)

        # 1: three school uses, each a tiny animation
        self.cue(1)
        self.play(formula.animate.scale(0.5).to_edge(UP, buff=0.35), run_time=0.7)
        centers = [LEFT * 4.4 + DOWN * 0.6, DOWN * 0.6, RIGHT * 4.4 + DOWN * 0.6]
        frames = VGroup(*[panel_frame(p) for p in centers])

        # (a) solve equations: two lines meet in one point; tilt toward parallel -> det -> 0
        ca = centers[0] + UP * 0.15
        la = Line(ca + LEFT * 1.5 + DOWN * 0.6, ca + RIGHT * 1.5 + UP * 0.6, color=ANT1, stroke_width=5)
        ang = ValueTracker(-0.9)
        off = np.array([0, -0.55, 0])                    # line B passes below line A's centre

        def lb_line():
            d = np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0])
            return Line(ca + off - 1.7 * d, ca + off + 1.7 * d, color=ANT2, stroke_width=5)
        lb = always_redraw(lb_line)
        dA = la.get_unit_vector()

        def crossing():
            d = np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0])
            M = np.array([[dA[0], -d[0]], [dA[1], -d[1]]])
            if abs(np.linalg.det(M)) < 1e-3:
                return ca + RIGHT * 99
            t = np.linalg.solve(M, (ca + off - ca)[:2])[0]
            return ca + t * dA
        dot = always_redraw(lambda: Dot(crossing(), radius=0.1, color=YELLOW).set_opacity(
            1 if np.linalg.norm(crossing() - ca) < 1.5 else 0))
        lab_a = T("solve equations", 24, YELLOW).next_to(frames[0], DOWN, buff=0.15)
        detv = always_redraw(lambda: T(f"det = {np.sin(ang.get_value() - 0.3805):.2f}", 22, SOFT)
                             .move_to(frames[0].get_top() + DOWN * 0.3))
        # (b) area of a triangle
        cb = centers[1] + UP * 0.1
        dots = VGroup(*[Dot(cb + 0.42 * np.array([x - 3, y - 2, 0]), radius=0.025, color=DIM)
                        for x in range(7) for y in range(5)])
        P = [cb + 0.42 * np.array(v) for v in [(-2.5, -1.5, 0), (2, -0.5, 0), (-0.5, 1.6, 0)]]
        tri = Polygon(*P, color=GOOD, stroke_width=4, fill_color=GOOD, fill_opacity=0.0)
        area = T("area = ½ |det|", 26, GOOD).move_to(frames[1].get_top() + DOWN * 0.3)
        lab_b = T("find areas", 24, YELLOW).next_to(frames[1], DOWN, buff=0.15)
        # (c) undo a matrix: grid -> sheared -> squashed flat when det = 0
        cc = centers[2] + UP * 0.1
        grid = VGroup(*[Line(cc + 0.45 * np.array([i, -2, 0]), cc + 0.45 * np.array([i, 2, 0]), color=ANT3, stroke_width=2)
                        for i in range(-2, 3)],
                      *[Line(cc + 0.45 * np.array([-2, j, 0]), cc + 0.45 * np.array([2, j, 0]), color=ANT3, stroke_width=2)
                        for j in range(-2, 3)])
        lab_c = T("undo a matrix?", 24, YELLOW).next_to(frames[2], DOWN, buff=0.15)
        cant = T("det = 0: can't undo", 24, BAD).move_to(frames[2].get_top() + DOWN * 0.3)

        self.cue_at(1, "solve equations", lead=0.25)
        self.play(Create(frames[0]), Create(la), Create(lb), FadeIn(dot, scale=1.5), FadeIn(lab_a), FadeIn(detv), run_time=0.7)
        self.play(ang.animate.set_value(float(np.arctan2(dA[1], dA[0]))), run_time=1.6, rate_func=smooth)
        nosol = T("parallel: no solution", 22, BAD).move_to(frames[0].get_bottom() + UP * 0.3)
        self.play(FadeIn(nosol), run_time=0.3)
        self.cue_at(1, "find areas", lead=0.25)
        self.play(Create(frames[1]), FadeIn(dots), Create(tri), FadeIn(lab_b), run_time=0.7)
        self.play(tri.animate.set_fill(opacity=0.45), FadeIn(area), run_time=0.6)
        self.cue_at(1, "undone", lead=0.25)
        self.play(Create(frames[2]), Create(grid, lag_ratio=0.05), FadeIn(lab_c), run_time=0.7)
        self.play(ApplyMatrix([[1, 0.6], [0.3, 1]], grid, about_point=cc), run_time=0.7)
        self.play(grid.animate.apply_function(lambda p: cc + (lambda q: np.array([q[0] + q[1], (q[0] + q[1]) * 0.5, 0]))(p - cc) * 0.6),
                  FadeIn(cant), run_time=0.8)
        uses = VGroup(frames, la, dot, lab_a, nosol, dots, tri, area, lab_b, grid, lab_c, cant)

        # 2: the turn: counting
        self.cue(2)
        self.cue_at(2, "most surprising", lead=0.3)
        self.play(FadeOut(VGroup(uses, formula)), FadeOut(lb), FadeOut(detv), run_time=0.8)
        counting = T("counting", 84, YELLOW, weight=BOLD)
        self.cue_at(2, "counting", lead=0.15)
        self.sfx("chime")
        self.play(FadeIn(counting, scale=1.3), run_time=0.7)

        # 3: ask a child: one, two, cha-cha-cha
        self.cue(3)
        self.play(counting.animate.scale(0.45).to_edge(UP, buff=0.4), run_time=0.5)
        kid = T("ask a child:", 34, SOFT).move_to(UP * 1.7)
        self.play(FadeIn(kid), run_time=0.4)
        a1 = ant(ANT1, 1.1).move_to(LEFT * 1.6 + DOWN * 1.7)
        a2 = ant(ANT2, 1.1).move_to(RIGHT * 1.6 + DOWN * 1.7)
        self.play(FadeIn(a1, scale=0.5), FadeIn(a2, scale=0.5), run_time=0.4)
        n1 = T("1", 120, INK, weight=BOLD).move_to(LEFT * 2.2 + UP * 0.3)
        n2 = T("2", 120, INK, weight=BOLD).move_to(UP * 0.3)
        self.cue_at(3, "one", lead=0.05)
        self.sfx("clave")
        self.play(FadeIn(n1, scale=1.6), run_time=0.25)
        self.cue_at(3, "two", lead=0.05)
        self.sfx("clave")
        self.play(FadeIn(n2, scale=1.6), run_time=0.25)
        cha = T("cha-cha-cha!", 64, YELLOW, weight=BOLD).move_to(RIGHT * 3.0 + UP * 0.3)
        self.cue_at(3, "cha", lead=0.05)
        self.add(cha.set_opacity(0))
        for k in range(3):
            self.sfx("shaker" if k < 2 else "clave")
            sh = 0.35 if k % 2 == 0 else -0.35
            self.play(a1.animate.shift(RIGHT * sh + UP * 0.12), a2.animate.shift(LEFT * sh + UP * 0.12),
                      cha.animate.set_opacity((k + 1) / 3), run_time=0.17, rate_func=there_and_back)
            self.wait(0.03)
        self.play(cha.animate.set_opacity(1).scale(1.08), run_time=0.15)
        child = VGroup(kid, a1, a2, n1, n2, cha)

        # 4: ask Leslie Valiant: #P-complete
        self.cue(4)
        self.remove(*child)                              # hard cut: the music stops
        f = os.path.join(HERE, "assets", "portraits", "valiant_round.png")
        photo = ImageMobject(f).set_height(3.0).move_to(LEFT * 3.6 + UP * 0.35)
        ring = Circle(radius=1.5, color=INK, stroke_width=3).move_to(photo)
        name = T("Leslie Valiant", 32).next_to(ring, DOWN, buff=0.2)
        credit = T("photo: Dennis Hamilton, CC BY 2.0", 22, DIM).to_corner(DL, buff=0.25)
        self.play(FadeIn(photo), Create(ring), FadeIn(name), FadeIn(credit), run_time=0.6)
        # a graph whose perfect matchings flicker past (cube graph Q3: 9 matchings)
        cg = RIGHT * 3.2 + UP * 0.35
        Vq = [np.array([x, y, 0]) * 1.45 for x, y in [(-1, -1), (1, -1), (1, 1), (-1, 1)]] + \
             [np.array([x, y, 0]) * 0.55 for x, y in [(-1, -1), (1, -1), (1, 1), (-1, 1)]]
        Eq = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
        PM = perfect_matchings(8, Eq)
        assert len(PM) == 9
        gedges = VGroup(*[Line(cg + Vq[a], cg + Vq[b], color=DIM, stroke_width=3) for a, b in Eq])
        gdots = VGroup(*[Dot(cg + v, radius=0.08, color=INK) for v in Vq])
        self.play(Create(gedges), FadeIn(gdots), run_time=0.6)
        cur = None
        self.cue_at(4, "Even counting", lead=0.2)
        for k in range(len(PM) * 2):
            mt = VGroup(*[Line(cg + Vq[a], cg + Vq[b], color=YELLOW, stroke_width=8) for a, b in PM[k % len(PM)]])
            if cur is not None:
                self.remove(cur)
            self.add(mt)
            cur = mt
            self.wait(0.16)
        pm_lab = T("perfect matchings", 26, YELLOW).next_to(gedges, DOWN, buff=0.35)
        self.play(FadeIn(pm_lab), run_time=0.4)
        sharp = T("#P-complete", 56, BAD, weight=BOLD).to_edge(DOWN, buff=0.75).shift(RIGHT * 1.6)
        yr = T("Valiant, 1979", 26, SOFT).next_to(sharp, DOWN, buff=0.1)
        self.cue_at(4, "#P-complete", lead=0.2)
        self.sfx("buzz")
        self.play(FadeIn(sharp, scale=1.3), FadeIn(yr), run_time=0.6)
        valiant = Group(photo, ring, name, credit, gedges, gdots, cur, pm_lab, sharp, yr)

        # 5: and yet a single determinant counts these
        self.cue(5)
        self.play(FadeOut(valiant), counting.animate.set_opacity(0), run_time=0.6)
        h = 2.3

        def card(mob, count, label):
            mob.scale_to_fit_height(h)
            tag = VGroup(T("det", 26, YELLOW), T("= " + count, 26, INK)).arrange(RIGHT, buff=0.15)
            return VGroup(mob, T(label, 26, SOFT, line_spacing=1.0), tag).arrange(DOWN, buff=0.2)
        c1 = card(pair_icon(GOOD_P, GOOD_Q, size=1.4, meet=False), "20", "routes that\nnever cross")
        c2 = card(VGroup(hex_outline(0.5), hex_tiling(SHOW, 0.5, stroke=1)), "20", "tilings of\na hexagon")
        bd = board(8, 8, 0.3)
        bd.add(*[domino(bd.sq, x, y, 0.3) for x, y in random_tiling(8, 8, 5)])
        c3 = card(bd, "12,988,816", "dominoes on\na chessboard")
        c4 = card(az_mob(AZ[3][41], 3, 0.3, ORIGIN, with_paths=False), "64", "an Aztec\ndiamond")
        cards = VGroup(c1, c2, c3, c4).arrange(RIGHT, buff=0.55).move_to(DOWN * 0.1)
        if cards.width > 13.2:
            cards.scale_to_fit_width(13.2)
        head = T("a single determinant counts…", 36, YELLOW).to_edge(UP, buff=0.5)
        self.cue_at(5, "a single determinant", lead=0.2)
        self.play(FadeIn(head), run_time=0.5)
        for cd, w in zip([c1, c2, c3], ["routes", "tilings of a hexagon", "dominoes"]):
            self.cue_at(5, w, lead=0.2)
            self.sfx("pop")
            self.play(FadeIn(cd, shift=UP * 0.2, scale=0.9), run_time=0.5)
        self.play(FadeIn(c4, shift=UP * 0.2, scale=0.9), run_time=0.5)

        # 6: let's see how: hand over to the ant puzzle (same grid and ants as Hook)
        self.cue(6)
        self.cue_at(6, "two ants", lead=0.6)
        lat = Lattice(4, spacing=1.45, center=GRID_HOOK)
        b1 = ant(ANT1, 0.9).move_to(lat.p(*A1))
        b2 = ant(ANT2, 0.9).move_to(lat.p(*A2))
        self.play(FadeOut(VGroup(cards, head)), run_time=0.6)
        self.play(LaggedStartMap(FadeIn, lat, lag_ratio=0.03), FadeIn(b1, scale=0.4), FadeIn(b2, scale=0.4), run_time=1.0)
