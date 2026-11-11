"""Act 0 — opening v20 (11 Nov): v11 base (school 2x2/3x3, general forms) + v17 uses with formulas on top; no matrix kept on top; combinatorics line on a clear screen, then the title.
(previous: act0_opening_v19.py.bak; v11 = git 854a40e)
(previous version: act0_opening_v10.py.bak)

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
        # 0 — most of us have seen the determinant in school
        self.cue(0)
        big = MathTex(r"\det", color=YELLOW).scale(3.2)
        self.play(Write(big), run_time=1.0)

        # 1 — 2x2: a d − b c (diagonals, then they fade)
        self.cue(1)
        m = Matrix([["a", "b"], ["c", "d"]], h_buff=1.1, v_buff=0.9).scale(1.5).shift(LEFT * 2.4)
        cells = m.get_entries()
        diag = Line(cells[0].get_center(), cells[3].get_center(), color=SOFT, stroke_width=10).set_opacity(0.65)
        anti = Line(cells[1].get_center(), cells[2].get_center(), color=SOFT, stroke_width=10).set_opacity(0.65)
        dl = MathTex(r"\det", color=YELLOW).scale(1.9).next_to(m, LEFT, buff=0.3)
        rhs = MathTex("=", "ad", "-", "bc").scale(1.9).next_to(m, RIGHT, buff=0.4)
        rhs[2].set_color(YELLOW)
        self.play(ReplacementTransform(big, dl), FadeIn(m), run_time=0.7)
        self.cue_at(1, "a d minus", lead=0.3)
        self.play(Create(diag), FadeIn(rhs[:2]), run_time=0.55)
        self.play(Create(anti), FadeIn(rhs[2:]), run_time=0.55)
        formula = VGroup(dl, m, rhs)
        self.cue_end(1)
        self.play(FadeOut(diag), FadeOut(anti), run_time=0.3)
        self.play(FadeOut(VGroup(diag, anti, formula)), run_time=0.5)

        # 2 — 3x3: six products, three with +, three with − (built quickly)
        self.cue(2)
        L = [["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]]
        m3 = Matrix(L, h_buff=1.0, v_buff=0.8).scale(1.1).move_to(LEFT * 3.4 + DOWN * 0.3)
        e3 = m3.get_entries()
        d3 = MathTex(r"\det", color=YELLOW).scale(1.3).next_to(m3, LEFT, buff=0.25)
        self.play(FadeIn(m3), FadeIn(d3), run_time=0.5)
        terms = [((0, 4, 8), "+"), ((1, 5, 6), "+"), ((2, 3, 7), "+"), ((2, 4, 6), "-"), ((1, 3, 8), "-"), ((0, 5, 7), "-")]
        eq3 = MathTex("=").scale(1.3).next_to(m3, RIGHT, buff=0.35)
        txts = VGroup()
        for k, (ix, sg) in enumerate(terms):
            col = GOOD if sg == "+" else BAD
            txts.add(MathTex(sg, "".join(L[i // 3][i % 3] for i in ix)).scale(1.3))
            txts[-1][0].set_color(col)
        r1, r2 = VGroup(*txts[:3]).arrange(RIGHT, buff=0.35), VGroup(*txts[3:]).arrange(RIGHT, buff=0.35)
        VGroup(r1, r2).arrange(DOWN, buff=0.45, aligned_edge=LEFT).next_to(eq3, RIGHT, buff=0.3)
        VGroup(r1, r2).shift(UP * (eq3.get_y() - r1.get_y()))
        txts[0][0].set_opacity(0)                         # no leading +
        out = VGroup(eq3, txts)
        self.play(FadeIn(eq3), run_time=0.2)
        for k, (ix, sg) in enumerate(terms):
            col = GOOD if sg == "+" else BAD
            boxes = VGroup(*[SurroundingRectangle(e3[i], color=col, buff=0.1) for i in ix])
            self.play(Create(boxes), FadeIn(txts[k], shift=RIGHT * 0.1), run_time=0.25)
            self.play(FadeOut(boxes), run_time=0.1)

        # 3-6 — general forms of the determinant (one per phrase)
        self.cue(3)
        self.play(FadeOut(VGroup(m3, d3, out)), run_time=0.6)
        fm = VGroup(
            MathTex(r"\det A", "=", r"\sum_{j=1}^{n} (-1)^{1+j}\, a_{1j}\, \det A_{1j}"),
            MathTex(r"\det A", "=", r"\lambda_1 \lambda_2 \cdots \lambda_n"),
            MathTex(r"\det A", "=", r"\sum_{\sigma \in S_n} \operatorname{sgn}(\sigma)\, a_{1\sigma(1)}\, a_{2\sigma(2)} \cdots a_{n\sigma(n)}"),
        )
        fm.arrange(DOWN, buff=0.55).move_to(DOWN * 0.5)
        for f in fm[1:]:                                   # the = signs one under the other
            f.shift(RIGHT * (fm[0][1].get_x() - f[1].get_x()))
        fm.move_to(DOWN * 0.5)
        for k, cue in ((0, 4), (1, 5), (2, 6)):
            self.cue(cue)
            self.play(FadeIn(fm[k], shift=UP * 0.15), run_time=0.8)

        # 7 — it shows up all over mathematics
        self.cue(7)
        self.play(FadeOut(fm, shift=DOWN * 0.3), run_time=0.8)

        # 8 — equations. The dot is the unique solution; when the lines turn parallel it slides off.
        origin = DOWN * 0.9
        pivot = origin + UP * 0.8
        slope = 0.36
        d1 = np.array([1.0, slope, 0.0]) / np.hypot(1, slope)
        fixed = Line(origin - 2.8 * d1, origin + 2.8 * d1, color=ANT1, stroke_width=6)
        angle = ValueTracker(-0.45)
        par = float(np.arctan(slope))

        def direction():
            t = angle.get_value()
            return np.array([np.cos(t), np.sin(t), 0.0])

        moving = always_redraw(lambda: Line(pivot - 2.8 * direction(), pivot + 2.8 * direction(),
                                            color=ANT2, stroke_width=6))

        def meet():
            dd = direction()
            mat = np.column_stack((d1[:2], -dd[:2]))
            if abs(np.linalg.det(mat)) < 1e-4:
                return origin + 40 * d1
            return origin + np.linalg.solve(mat, (pivot - origin)[:2])[0] * d1

        def meet_dot():                                    # the solution, shown only while it is on the drawn lines
            q = meet()
            on = np.linalg.norm(q - origin) < 2.7 and np.linalg.norm(q - pivot) < 2.7
            return Dot(q if on else origin, radius=0.13, color=YELLOW).set_opacity(1 if on else 0)

        point = always_redraw(meet_dot)
        self.cue(8)
        top8 = VGroup(MathTex(r"\begin{cases} a\,x + b\,y = e \\ c\,x + d\,y = f \end{cases}"),
                      MathTex(r"\text{has a unique solution} \iff \det\begin{bmatrix} a & b \\ c & d \end{bmatrix} \neq 0")).arrange(RIGHT, buff=0.8)
        top8.scale(0.75).to_edge(UP, buff=0.5)
        nonzero = MathTex(r"\det \neq 0", color=SOFT).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(top8[0]), Create(fixed), Create(moving), FadeIn(nonzero), run_time=0.8)
        self.play(FadeIn(top8[1]), run_time=0.6)
        self.add(point)
        self.cue_at(8, "unique", lead=0.1)
        self.play(Flash(point, color=YELLOW, line_length=0.25, flash_radius=0.3), run_time=0.5)
        self.play(angle.animate.set_value(par), run_time=1.6, rate_func=rate_functions.ease_in_quad)
        self.remove(point)
        zero1 = MathTex(r"\det = 0", color=SOFT).to_edge(DOWN, buff=0.6)
        self.play(FadeOut(nonzero), FadeIn(zero1), run_time=0.3)

        # 9 — scaling: unit square -> stretch x2 -> shear; the ghost square stays for comparison
        self.cue(9)
        self.play(FadeOut(VGroup(fixed, moving, zero1, top8)), run_time=0.35)
        top9 = MathTex(r"\text{area}(A\,S) = |\det A| \cdot \text{area}(S)").to_edge(UP, buff=0.6)
        center = DOWN * 0.6 + LEFT * 1.0
        u = 0.9
        P = lambda x, y: center + u * np.array([x, y, 0.0])
        grid = VGroup(*[Line(P(x, -2), P(x, 2), color=DIM, stroke_width=2) for x in range(-2, 3)],
                      *[Line(P(-2, y), P(2, y), color=DIM, stroke_width=2) for y in range(-2, 3)])
        sq_pts = [P(0, 0), P(1, 0), P(1, 1), P(0, 1)]
        square = Polygon(*sq_pts, stroke_color=YELLOW, stroke_width=5, fill_color=YELLOW, fill_opacity=0.3)
        ghost = Polygon(*sq_pts, stroke_color=SOFT, stroke_width=2.5, fill_opacity=0).set_stroke(opacity=0.8)
        plane = VGroup(grid, square)
        self.play(LaggedStart(*[Create(l) for l in grid], lag_ratio=0.03), FadeIn(square), run_time=0.7)
        self.add(ghost)
        self.cue_at(9, "scales", lead=0.2)
        self.play(FadeIn(top9), run_time=0.6)
        self.play(ApplyMatrix([[2, 0], [0, 1]], plane, about_point=center), run_time=1.0)
        self.play(ApplyMatrix([[1, 0.5], [0, 1]], plane, about_point=center), run_time=1.0)
        self.play(Indicate(square, color=YELLOW, scale_factor=1.08), run_time=0.7)

        # 10 — polygon area (shoelace): fan from O; +5, +6.5, +2 and −0.5, −2.5 (the overhang); 10.5
        self.cue(10)
        U, O = 0.8, LEFT * 2.4 + DOWN * 3.0
        Q = lambda x, y: O + U * np.array([x, y, 0.0])
        V = [(2, 1), (5, 2), (5, 4), (3, 5), (1, 3)]
        poly = Polygon(*[Q(*v) for v in V], stroke_color=INK, stroke_width=5, fill_opacity=0)
        tris = [(V[i], V[(i + 1) % 5]) for i in range(5)]
        tri = lambda a, b, col, op: Polygon(O, Q(*a), Q(*b), stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=op)
        signed = [(a, b, a[0] * b[1] - a[1] * b[0]) for a, b in tris]
        tv = VGroup(*[tri(a, b, YELLOW if d > 0 else SOFT, 0.4 if d > 0 else 0.55) for a, b, d in signed])
        labs = VGroup(*[MathTex(str(k + 1), color=BLACK if d > 0 else WHITE).scale(0.9)
                        .move_to((O + Q(*a) + Q(*b)) / 3) for k, (a, b, d) in enumerate(signed)])
        for k, (a, b, d) in enumerate(signed):              # thin overhang triangles: label just outside
            if d < 0:
                labs[k].set_color(SOFT).move_to((O + Q(*a) + Q(*b)) / 3 + normalize((Q(*a) + Q(*b)) / 2 - O) * 0.0 + LEFT * 0.35)
        labs[0].move_to((O + Q(*V[0]) + Q(*V[1])) / 3 + DOWN * 0.32 + RIGHT * 0.25)   # thin sliver: label just below
        assert sum(d for _, _, d in signed) / 2 == 10.5
        self.play(FadeOut(plane), FadeOut(ghost), FadeOut(top9), Create(poly), run_time=0.8)
        self.remove(plane, ghost, *grid, square)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(t), FadeIn(l)) for t, l in zip(tv, labs)], lag_ratio=0.45), run_time=1.6)
        self.add(poly)
        shoe = MathTex(r"\text{Area} = \tfrac{1}{2}\left[\det\!\left(M_{\triangle_1}\right) + \det\!\left(M_{\triangle_2}\right) + \cdots + \det\!\left(M_{\triangle_5}\right)\right]")
        shoe.scale(0.85).to_edge(UP, buff=0.5)
        self.play(Write(shoe), run_time=1.2)
        self.wait(0.6)


        # 11 — "one of the most surprising places ... combinatorics": no animation, a clear screen
        self.cue(11)
        self.play(FadeOut(VGroup(poly, shoe, tv, labs)), run_time=0.6)

        # 12 — today: how determinants can count (title in the centre as it is said)
        self.cue(12)
        title = T("How Determinants Can Count", 50, weight=BOLD)
        self.cue_at(12, "how determinants", lead=0.2)
        self.sfx("chime")
        self.play(Write(title), run_time=1.3)
        # 13 — "let's start with a simple puzzle": the subtitle appears under the title (no separate card)
        self.cue(13)
        sub = T("First, a simple puzzle", 32, SOFT).next_to(title, DOWN, buff=0.45)
        self.cue_at(13, "simple puzzle", lead=0.4)
        self.play(FadeIn(sub, shift=UP * 0.15), run_time=0.7)
        self.cue_end(13)
        self.wait(0.8)
        self.play(FadeOut(VGroup(title, sub)), run_time=0.8)
