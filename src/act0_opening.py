"""Act 0 — short visual opening (v8).

Six narration lines, six presenter slides:
  0 familiar 2x2 determinant
  1 equations: intersecting lines become distinct parallel lines
  2 area: a unit square deforms into a parallelogram
  3 non-invertibility: the grid collapses to a line (det = 0)
  4 surprising turn: determinants can count
  5 the same two ants/grid that begin Hook

Keep the application examples brief. The puzzle supplies the main story.
"""
from common import *
from act0_hook import GRID_HOOK


class Opening(DScene):
    def construct(self):
        # 0 — familiar formula. Do not reuse green/red good/bad semantics.
        self.cue(0)
        m = matrix_mob([["a", "b"], ["c", "d"]], size=80).shift(LEFT * 2.6)
        cells = m.cells
        diag = Line(cells[0].get_center(), cells[3].get_center(),
                    color=SOFT, stroke_width=10).set_opacity(0.65)
        anti = Line(cells[1].get_center(), cells[2].get_center(),
                    color=SOFT, stroke_width=10).set_opacity(0.65)
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

        # The formula stays small above three full-size applications.
        self.cue(1)
        self.play(formula.animate.scale(0.47).to_edge(UP, buff=0.35), run_time=0.55)

        # 1 — solving equations. The marker follows the unique intersection;
        # when directions become parallel it leaves the picture.
        origin = DOWN * 0.55
        pivot = origin + UP * 0.8
        slope = 0.36
        first_direction = np.array([1.0, slope, 0.0])
        fixed = Line(origin - 3.3 * first_direction,
                     origin + 3.3 * first_direction,
                     color=ANT1, stroke_width=6)
        angle = ValueTracker(-0.40)

        def moving_line():
            t = angle.get_value()
            direction = np.array([np.cos(t), np.sin(t), 0])
            return Line(pivot - 3.5 * direction,
                        pivot + 3.5 * direction,
                        color=ANT2, stroke_width=6)

        moving = always_redraw(moving_line)

        def intersection():
            t = angle.get_value()
            direction = np.array([np.cos(t), np.sin(t)])
            mat = np.column_stack((first_direction[:2], -direction))
            if abs(np.linalg.det(mat)) < 1e-5:
                return origin + RIGHT * 30
            distance = np.linalg.solve(mat, (pivot - origin)[:2])[0]
            return origin + distance * first_direction

        point = always_redraw(
            lambda: Dot(intersection(), radius=0.11, color=YELLOW)
            .set_opacity(1 if np.linalg.norm(intersection() - origin) < 3.3 else 0)
        )
        determinant_label = T("det ≠ 0", 34, SOFT).to_edge(DOWN, buff=0.65)
        self.play(Create(fixed), FadeIn(moving), FadeIn(point),
                  FadeIn(determinant_label), run_time=0.8)
        self.play(angle.animate.set_value(float(np.arctan(slope))),
                  run_time=1.65, rate_func=smooth)
        zero_eq = T("det = 0", 34, SOFT).move_to(determinant_label)
        self.play(Transform(determinant_label, zero_eq), run_time=0.3)

        # 2 — unit square -> parallelogram. The transformed cell has
        # area |det(A)|; no numeric claims or unexplained formulas.
        self.cue(2)
        self.play(FadeOut(VGroup(fixed, moving, point, determinant_label)),
                  run_time=0.4)
        center = DOWN * 0.5
        spacing = 1.0
        grid = VGroup(
            *[Line(center + np.array([x, -2.0, 0]),
                   center + np.array([x, 2.0, 0]),
                   color=DIM, stroke_width=2) for x in range(-2, 3)],
            *[Line(center + np.array([-2.0, y, 0]),
                   center + np.array([2.0, y, 0]),
                   color=DIM, stroke_width=2) for y in range(-2, 3)]
        )
        square = Polygon(
            center, center + RIGHT * spacing,
            center + (RIGHT + UP) * spacing, center + UP * spacing,
            stroke_color=YELLOW, stroke_width=5,
            fill_color=YELLOW, fill_opacity=0.26
        )
        plane = VGroup(grid, square)
        self.play(LaggedStart(*[Create(line) for line in grid], lag_ratio=0.04),
                  FadeIn(square), run_time=0.8)
        self.play(ApplyMatrix([[1.2, 0.55], [0.1, 0.85]], plane,
                              about_point=center),
                  run_time=1.25)
        area_label = T("area = |det|", 34, YELLOW).to_edge(DOWN, buff=0.65)
        self.play(FadeIn(area_label), run_time=0.35)

        # 3 — collapse the plane to one line. The deformation has rank 1.
        self.cue(3)
        zero_area = T("det = 0", 34, SOFT).move_to(area_label)
        self.play(
            FadeOut(area_label),
            plane.animate.apply_function(
                lambda p: np.array([p[0], center[1], p[2]])
            ),
            FadeIn(zero_area),
            run_time=1.7,
        )

        # 4 — the turn is a question, not an application montage.
        self.cue(4)
        self.play(FadeOut(VGroup(formula, plane, zero_area)), run_time=0.55)
        counting = T("counting", 82, YELLOW, weight=BOLD)
        self.cue_at(4, "count", lead=0.2)
        self.sfx("chime")
        self.play(FadeIn(counting, scale=1.2), run_time=0.65)

        # 5 — hand over the exact lattice and two ants used in Hook.
        self.cue(5)
        self.cue_at(5, "two ants", lead=0.35)
        lat = Lattice(4, spacing=1.45, center=GRID_HOOK)
        a1 = ant(ANT1, 0.9).move_to(lat.p(*A1))
        a2 = ant(ANT2, 0.9).move_to(lat.p(*A2))
        self.play(FadeOut(counting), FadeIn(lat),
                  FadeIn(a1, scale=0.5), FadeIn(a2, scale=0.5),
                  run_time=0.9)
