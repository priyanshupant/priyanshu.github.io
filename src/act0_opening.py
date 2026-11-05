"""Act 0 — short visual opening (v8.1: same beats as v8, clearer and in sync).

Seven narration lines, seven presenter slides:
  0 familiar 2x2 determinant
  1 equations: two lines meet in one dot; they turn parallel and the dot runs off
  2 area: the unit square (ghost kept) becomes a parallelogram
  3 det = 0: everything is squashed flat; two points land on one
  4 polygon area (shoelace): fan triangles, negative ones cancel the outside
  5 surprising turn: determinants can count
  6 the same two ants/grid that begin Hook
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
        formula = VGroup(dl, m, diag, anti, eq, ad, minus, bc)
        self.cue_end(0)
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
        self.play(Create(fixed), Create(moving), run_time=0.6)
        self.add(point)
        self.cue_at(1, "unique", lead=0.1)
        self.play(Flash(point, color=YELLOW, line_length=0.25, flash_radius=0.3), run_time=0.5)
        self.play(angle.animate.set_value(par), run_time=1.6, rate_func=rate_functions.ease_in_quad)
        self.remove(point)
        zero1 = T("det = 0", 34, SOFT).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(zero1), run_time=0.3)

        # 2 — area: unit square -> parallelogram; the ghost square stays for comparison.
        self.cue(2)
        self.play(FadeOut(VGroup(fixed, moving, zero1)), run_time=0.35)
        center = DOWN * 0.6 + LEFT * 0.6
        u = 0.8                                          # grid unit
        P = lambda x, y: center + u * np.array([x, y, 0.0])
        grid = VGroup(*[Line(P(x, -2), P(x, 2), color=DIM, stroke_width=2) for x in range(-3, 4)],
                      *[Line(P(-3, y), P(3, y), color=DIM, stroke_width=2) for y in range(-2, 3)])
        sq_pts = [P(0, 0), P(1, 0), P(1, 1), P(0, 1)]
        square = Polygon(*sq_pts, stroke_color=YELLOW, stroke_width=5, fill_color=YELLOW, fill_opacity=0.3)
        ghost = Polygon(*sq_pts, stroke_color=SOFT, stroke_width=2.5, fill_opacity=0).set_stroke(opacity=0.8)
        # two points one above the other: they will land on one point in beat 3
        p_top = Dot(P(-2, 1), radius=0.11, color=ANT1)
        p_bot = Dot(P(-2, -1), radius=0.11, color=ANT2)
        plane = VGroup(grid, square)
        self.play(LaggedStart(*[Create(l) for l in grid], lag_ratio=0.03), FadeIn(square), run_time=0.7)
        self.add(ghost)
        A = [[1.3, 0.5], [0.15, 1.0]]
        self.play(ApplyMatrix(A, VGroup(grid, square), about_point=center), run_time=1.2)
        area = T("area × |det|", 34, YELLOW).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(area), run_time=0.3)

        # 3 — can't undo: flatten onto a line; the parallelogram becomes a segment
        # and two different points land on the same point.
        self.cue(3)
        p_top.move_to(P(*(np.array(A) @ [-2, 1])))
        p_bot.move_to(P(*(np.array(A) @ [-2, -1])))
        self.play(FadeOut(ghost), FadeIn(p_top, scale=1.6), FadeIn(p_bot, scale=1.6), run_time=0.6)
        dif = p_top.get_center() - p_bot.get_center()
        k = dif[0] / dif[1]     # kernel of the flattening contains top - bot, so they land together
        flat = lambda p: np.array([p[0] - (p[1] - center[1]) * k, center[1], 0])   # rank-1 map
        self.cue_at(3, "zero", lead=0.1)
        self.play(plane.animate.apply_function(flat), p_top.animate.move_to(flat(p_top.get_center())),
                  p_bot.animate.move_to(flat(p_bot.get_center())), FadeOut(area), run_time=1.5)
        zero3 = T("det = 0", 34, SOFT).to_edge(DOWN, buff=0.6)
        self.play(Flash(p_bot.get_center(), color=YELLOW, line_length=0.2, flash_radius=0.3),
                  FadeIn(zero3), run_time=0.5)

        # 4 — area of any polygon (shoelace): fan triangles from O; signed areas
        # det(v_i, v_i+1)/2 are +5, +6.5, +2 (far edges) and −0.5, −2.5 (near edges).
        # 13.5 − 3 = 10.5 = the polygon's area; the negatives cover exactly the outside part.
        self.cue(4)
        U, O = 0.8, LEFT * 2.0 + DOWN * 2.9
        Q = lambda x, y: O + U * np.array([x, y, 0.0])
        V = [(2, 1), (5, 2), (5, 4), (3, 5), (1, 3)]
        poly = Polygon(*[Q(*v) for v in V], stroke_color=INK, stroke_width=5, fill_opacity=0)
        odot = Dot(O, radius=0.09, color=INK)
        self.play(FadeOut(VGroup(grid, square, p_top, p_bot, zero3)), Create(poly), run_time=0.9)
        tris = [(V[i], V[(i + 1) % 5]) for i in range(5)]
        sgn = [np.sign(a[0] * b[1] - a[1] * b[0]) for a, b in tris]
        pos = VGroup(*[Polygon(O, Q(*a), Q(*b), stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW, fill_opacity=0.4)
                       for (a, b), s_ in zip(tris, sgn) if s_ > 0])
        neg = VGroup(*[Polygon(O, Q(*a), Q(*b), stroke_color=SOFT, stroke_width=3, fill_color=SOFT, fill_opacity=0.55)
                       for (a, b), s_ in zip(tris, sgn) if s_ < 0])
        self.cue_at(4, "fan out", lead=0.2)
        self.play(FadeIn(odot, scale=1.5), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(t) for t in pos], lag_ratio=0.6), run_time=1.6)
        self.cue_at(4, "negative", lead=0.2)
        self.play(LaggedStart(*[FadeIn(t) for t in neg], lag_ratio=0.5), run_time=1.0)
        self.add(poly)
        self.wait(0.9)                                         # see: grey sits exactly on the outside part
        self.play(FadeOut(neg), FadeOut(pos), FadeOut(odot), poly.animate.set_fill(YELLOW, 0.4), run_time=0.9)
        self.play(Indicate(poly, color=YELLOW, scale_factor=1.04), run_time=0.6)

        # 5 — the turn to counting: the polygon gives way to the ants' grid.
        self.cue(5)
        lat = Lattice(4, spacing=1.45, center=GRID_HOOK)
        counting = T("counting", 72, YELLOW, weight=BOLD).move_to(RIGHT * 3.4 + UP * 0.3)
        self.play(FadeOut(VGroup(formula, poly)), FadeIn(lat), run_time=1.0)
        self.cue_at(5, "count", lead=0.2)
        self.sfx("chime")
        self.play(FadeIn(counting, scale=1.2), run_time=0.6)

        # 6 — hand over the exact lattice and two ants used in Hook.
        self.cue(6)
        self.cue_at(6, "two ants", lead=0.35)
        a1 = ant(ANT1, 0.9).move_to(lat.p(*A1))
        a2 = ant(ANT2, 0.9).move_to(lat.p(*A2))
        self.play(FadeOut(counting), FadeIn(a1, scale=0.5), FadeIn(a2, scale=0.5), run_time=0.8)
