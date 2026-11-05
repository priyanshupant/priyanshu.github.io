"""Act 0 — short visual opening (v8.1: same beats as v8, clearer and in sync).

Six narration lines, six presenter slides:
  0 familiar 2x2 determinant
  1 equations: two lines meet in one dot; they turn parallel and the dot runs off
  2 area: the unit square (ghost kept) becomes a parallelogram
  3 det = 0: everything is squashed flat; two points land on one
  4 surprising turn: determinants can count (the line becomes the ants' grid)
  5 the same two ants/grid that begin Hook
"""
from common import *
from act0_hook import GRID_HOOK


class Opening(DScene):
    def construct(self):
        # 0 — familiar formula. Neutral colours: green/red mean good/bad later.
        self.cue(0)
        m = matrix_mob([["a", "b"], ["c", "d"]], size=80).shift(LEFT * 2.6)
        cells = m.cells
        diag = Line(cells[0].get_center(), cells[3].get_center(), color=SOFT, stroke_width=10).set_opacity(0.65)
        anti = Line(cells[1].get_center(), cells[2].get_center(), color=SOFT, stroke_width=10).set_opacity(0.65)
        dl = T("det", 58, YELLOW).next_to(m, LEFT, buff=0.35)
        eq = T("=", 66).next_to(m, RIGHT, buff=0.55)
        ad = T("a d", 66).next_to(eq, RIGHT, buff=0.3)
        minus = T("−", 66, YELLOW).next_to(ad, RIGHT, buff=0.3)
        bc = T("b c", 66).next_to(minus, RIGHT, buff=0.3)
        self.play(FadeIn(m), FadeIn(dl), run_time=0.65)
        self.cue_at(0, "a d minus", lead=0.35)
        self.play(Create(diag), FadeIn(eq), FadeIn(ad), run_time=0.55)
        self.play(Create(anti), FadeIn(minus), FadeIn(bc), run_time=0.55)
        formula = VGroup(dl, m, eq, ad, minus, bc)
        self.cue_end(0)
        self.play(FadeOut(diag), FadeOut(anti), run_time=0.3)        # the diagonals have done their job
        self.play(formula.animate.scale(0.47).to_edge(UP, buff=0.35), run_time=0.5)

        # 1 — equations. The dot is the unique solution; when the lines turn
        # parallel it slides off along them (no solution), then det = 0.
        origin = DOWN * 0.55
        pivot = origin + UP * 0.8
        slope = 0.36
        d1 = np.array([1.0, slope, 0.0]) / np.hypot(1, slope)
        fixed = Line(origin - 4.2 * d1, origin + 4.2 * d1, color=ANT1, stroke_width=6)
        angle = ValueTracker(-0.45)
        par = float(np.arctan(slope))

        def direction():
            t = angle.get_value()
            return np.array([np.cos(t), np.sin(t), 0.0])

        moving = always_redraw(lambda: Line(pivot - 4.2 * direction(), pivot + 4.2 * direction(),
                                            color=ANT2, stroke_width=6))

        def meet():
            dd = direction()
            mat = np.column_stack((d1[:2], -dd[:2]))
            if abs(np.linalg.det(mat)) < 1e-4:
                return origin + 40 * d1
            return origin + np.linalg.solve(mat, (pivot - origin)[:2])[0] * d1

        point = always_redraw(lambda: Dot(meet(), radius=0.13, color=YELLOW))
        self.cue(1)
        nonzero = T("det ≠ 0", 34, SOFT).to_edge(DOWN, buff=0.6)
        self.play(Create(fixed), Create(moving), FadeIn(nonzero), run_time=0.6)
        self.add(point)
        self.cue_at(1, "unique", lead=0.1)
        self.play(Flash(point, color=YELLOW, line_length=0.25, flash_radius=0.3), run_time=0.5)
        self.play(angle.animate.set_value(par), run_time=1.6, rate_func=rate_functions.ease_in_quad)
        self.remove(point)
        zero1 = T("det = 0", 34, SOFT).to_edge(DOWN, buff=0.6)
        self.play(FadeOut(nonzero), FadeIn(zero1), run_time=0.3)

        # 2 — area: unit square -> parallelogram; the ghost square stays for comparison.
        self.cue(2)
        self.play(FadeOut(VGroup(fixed, moving, zero1)), run_time=0.35)
        center = DOWN * 0.6 + LEFT * 1.0
        u = 0.9                                          # grid unit
        P = lambda x, y: center + u * np.array([x, y, 0.0])
        grid = VGroup(*[Line(P(x, -2), P(x, 2), color=DIM, stroke_width=2) for x in range(-2, 3)],
                      *[Line(P(-2, y), P(2, y), color=DIM, stroke_width=2) for y in range(-2, 3)])
        sq_pts = [P(0, 0), P(1, 0), P(1, 1), P(0, 1)]
        square = Polygon(*sq_pts, stroke_color=YELLOW, stroke_width=5, fill_color=YELLOW, fill_opacity=0.3)
        ghost = Polygon(*sq_pts, stroke_color=SOFT, stroke_width=2.5, fill_opacity=0).set_stroke(opacity=0.8)
        # two points one above the other: they will land on one point in beat 3
        p_top = Dot(P(-2, 1), radius=0.11, color=ANT1)
        p_bot = Dot(P(-2, -1), radius=0.11, color=ANT2)
        plane = VGroup(grid, square)
        one = T("1", 34, YELLOW).move_to(square)
        self.play(LaggedStart(*[Create(l) for l in grid], lag_ratio=0.03), FadeIn(square), FadeIn(one), run_time=0.7)
        self.add(ghost)
        # A = shear · stretch = [[1, 0.5], [0, 1]] · [[2, 0], [0, 1]] = [[2, 1], [0, 1]], det 2
        self.cue_at(2, "scales", lead=0.2)
        one2 = one.copy()
        self.play(ApplyMatrix([[2, 0], [0, 1]], plane, about_point=center),
                  one.animate.move_to(P(0.5, 0.5)), one2.animate.move_to(P(1.5, 0.5)), run_time=1.0)
        halves = DashedLine(P(1, 0), P(1, 1), color=YELLOW, stroke_width=2)      # exactly two unit squares
        self.play(Create(halves), run_time=0.3)
        two = T("2", 34, YELLOW).move_to(P(1, 0.5))
        self.play(FadeOut(halves), ReplacementTransform(VGroup(one, one2), two), run_time=0.5)
        one = two
        self.play(ApplyMatrix([[1, 0.5], [0, 1]], plane, about_point=center),
                  one.animate.move_to(P(1.5, 0.5)), run_time=1.0)                 # base 2, height 1: still 2
        A = [[2, 1], [0, 1]]
        area = T("det = 2", 34, YELLOW).to_edge(DOWN, buff=0.6)
        self.cue_at(2, "doubles", lead=0.2)
        self.play(FadeIn(area), Indicate(one, color=YELLOW, scale_factor=1.4), run_time=0.6)

        # 3 — can't undo: flatten onto a line; the parallelogram becomes a segment
        # and two different points land on the same point.
        self.cue(3)
        p_top.move_to(P(*(np.array(A) @ [-2, 1])))
        p_bot.move_to(P(*(np.array(A) @ [-2, -1])))
        self.play(FadeOut(ghost), FadeOut(one), FadeIn(p_top, scale=1.6), FadeIn(p_bot, scale=1.6), run_time=0.6)
        dif = p_top.get_center() - p_bot.get_center()
        k = dif[0] / dif[1]     # kernel of the flattening contains top - bot, so they land together
        flat = lambda p: np.array([p[0] - (p[1] - center[1]) * k, center[1], 0])   # rank-1 map
        self.cue_at(3, "zero", lead=0.1)
        self.play(plane.animate.apply_function(flat), p_top.animate.move_to(flat(p_top.get_center())),
                  p_bot.animate.move_to(flat(p_bot.get_center())), FadeOut(area), run_time=1.5)
        zero3 = T("det = 0", 34, SOFT).to_edge(DOWN, buff=0.6)
        self.play(Flash(p_bot.get_center(), color=YELLOW, line_length=0.2, flash_radius=0.3),
                  FadeIn(zero3), run_time=0.5)

        # 4 — polygon area (shoelace), minimal. Fan from O: triangle areas det(v_i, v_i+1)/2 =
        # +5, +6.5, +2 (yellow) and −0.5, −2.5 (grey, exactly the overhang); 13.5 − 3 = 10.5.
        self.cue(4)
        U, O = 0.8, LEFT * 2.0 + DOWN * 2.9
        Q = lambda x, y: O + U * np.array([x, y, 0.0])
        V = [(2, 1), (5, 2), (5, 4), (3, 5), (1, 3)]
        poly = Polygon(*[Q(*v) for v in V], stroke_color=INK, stroke_width=5, fill_opacity=0)
        tris = [(V[i], V[(i + 1) % 5]) for i in range(5)]
        tri = lambda a, b, col, op: Polygon(O, Q(*a), Q(*b), stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=op)
        pos = VGroup(*[tri(a, b, YELLOW, 0.4) for a, b in tris if a[0] * b[1] - a[1] * b[0] > 0])
        neg = VGroup(*[tri(a, b, SOFT, 0.55) for a, b in tris if a[0] * b[1] - a[1] * b[0] < 0])
        self.play(FadeOut(VGroup(grid, square, p_top, p_bot, zero3)), Create(poly), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(t) for t in pos], lag_ratio=0.5), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(t) for t in neg], lag_ratio=0.5), run_time=0.7)
        self.add(poly)
        self.wait(0.5)
        shoe = T("area = ½ Σ det", 34, YELLOW).to_edge(DOWN, buff=0.6)
        self.play(FadeOut(neg), FadeOut(pos), poly.animate.set_fill(YELLOW, 0.4), FadeIn(shoe), run_time=0.8)

        # 5 — the turn: combinatorics (no grid yet; the formula stays on top)
        self.cue(5)
        self.play(FadeOut(VGroup(poly, shoe)), run_time=0.6)
        self.cue_at(5, "combinatorics", lead=0.2)
        self.play(formula.animate.set_color(YELLOW), run_time=0.6)

        # 6 — the title, in the centre of the screen, as it is said (no name)
        self.cue(6)
        title = T("How Determinants Can Count", 50, weight=BOLD)
        self.play(FadeOut(formula), run_time=0.4)
        self.cue_at(6, "how determinants", lead=0.2)
        self.sfx("chime")
        self.play(Write(title), run_time=1.3)

        # 7 — "let's start with a simple puzzle": clear the screen (the Hook brings the ants)
        self.cue(7)
        self.cue_at(7, "simple puzzle", lead=0.2)
        self.play(FadeOut(title), run_time=0.8)
