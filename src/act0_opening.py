"""Act 0 — opening v42 (12 Nov): the title card 'How Determinants Can Count' is the first thing on screen, in the
centre, and stays there for the whole intro; everything (2x2, 3x3, the general forms, the uses) comes and goes
above and below it; at the end it leaves and 'First, a simple puzzle' comes.
(previous: act0_opening_v41.py.bak = v20 layout)
"""
from common import *

TOP, BOT = UP * 2.45, DOWN * 2.45            # the two bands around the title


def fit(m, w=12.4, h=2.1):
    if m.width > w:
        m.scale_to_fit_width(w)
    if m.height > h:
        m.scale_to_fit_height(h)
    return m


class Opening(DScene):
    def construct(self):
        title = T("How Determinants Can Count", 46, weight=BOLD)
        self.add(title)
        self.play(Write(title), run_time=1.2)

        # 0 — we've all seen the determinant ... let's start from the very beginning
        self.cue(0)

        # 1 — 2x2: a d − b c (above the title)
        self.cue(1)
        m = Matrix([["a", "b"], ["c", "d"]], h_buff=1.0, v_buff=0.8)
        cells = m.get_entries()
        dl = MathTex(r"\det", color=YELLOW)
        rhs = MathTex("=", "ad", "-", "bc")
        rhs[2].set_color(YELLOW)
        formula = fit(VGroup(dl, m, rhs).arrange(RIGHT, buff=0.3), h=1.9).move_to(TOP)
        diag = Line(cells[0].get_center(), cells[3].get_center(), color=SOFT, stroke_width=8).set_opacity(0.65)
        anti = Line(cells[1].get_center(), cells[2].get_center(), color=SOFT, stroke_width=8).set_opacity(0.65)
        self.play(FadeIn(VGroup(dl, m), shift=DOWN * 0.15), run_time=0.6)
        self.cue_at(1, "a d minus", lead=0.3)
        self.play(Create(diag), FadeIn(rhs[:2]), run_time=0.55)
        self.play(Create(anti), FadeIn(rhs[2:]), run_time=0.55)
        self.play(FadeOut(diag), FadeOut(anti), run_time=0.3)

        # 2 — 3x3 below the title: six products, three +, three − (built quickly)
        self.cue(2)
        L = [["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]]
        m3 = Matrix(L, h_buff=0.9, v_buff=0.7)
        e3 = m3.get_entries()
        terms = [((0, 4, 8), "+"), ((1, 5, 6), "+"), ((2, 3, 7), "+"), ((2, 4, 6), "-"), ((1, 3, 8), "-"), ((0, 5, 7), "-")]
        txts = VGroup(*[MathTex(sg, "".join(L[i // 3][i % 3] for i in ix)) for ix, sg in terms]).arrange(RIGHT, buff=0.3)
        for k, (ix, sg) in enumerate(terms):
            txts[k][0].set_color(GOOD if sg == "+" else BAD)
        txts[0][0].set_opacity(0)
        row3 = fit(VGroup(MathTex(r"\det", color=YELLOW), m3, MathTex("="), txts).arrange(RIGHT, buff=0.3), h=2.0).move_to(BOT)
        self.play(FadeIn(row3[:3]), run_time=0.5)
        for k, (ix, sg) in enumerate(terms):
            boxes = VGroup(*[SurroundingRectangle(e3[i], color=GOOD if sg == "+" else BAD, buff=0.08) for i in ix])
            self.play(Create(boxes), FadeIn(txts[k], shift=RIGHT * 0.1), run_time=0.25)
            self.play(FadeOut(boxes), run_time=0.1)

        # 3-6 — the general forms: row expansion above; eigenvalues and Leibniz below
        self.cue(3)
        self.play(FadeOut(formula), FadeOut(row3), run_time=0.6)
        f_row = MathTex(r"\det A", "=", r"\sum_{j=1}^{n} (-1)^{1+j}\, a_{1j}\, \det A_{1j}").scale(0.95).move_to(TOP)
        f_eig = MathTex(r"\det A", "=", r"\lambda_1 \lambda_2 \cdots \lambda_n").scale(0.95).move_to(BOT + UP * 0.55)
        f_lei = MathTex(r"\det A", "=", r"\sum_{\sigma \in S_n} \operatorname{sgn}(\sigma)\, a_{1\sigma(1)}\, a_{2\sigma(2)} \cdots a_{n\sigma(n)}").scale(0.95)
        f_lei.move_to(BOT + DOWN * 0.6)
        for f in (f_eig, f_lei):                           # the = signs one under the other
            f.shift(RIGHT * (f_row[1].get_x() - f[1].get_x()))
        fm = VGroup(f_row, f_eig, f_lei)
        for k, cue in ((0, 4), (1, 5), (2, 6)):
            self.cue(cue)
            self.play(FadeIn(fm[k], shift=UP * 0.15), run_time=0.8)

        # 7 — it shows up all over mathematics
        self.cue(7)
        self.play(FadeOut(fm, shift=DOWN * 0.2), run_time=0.8)

        # 8 — equations: the statement above, the two lines below (the dot is the unique solution)
        origin = BOT + DOWN * 0.35
        pivot = origin + UP * 0.7
        slope = 0.3
        d1 = np.array([1.0, slope, 0.0]) / np.hypot(1, slope)
        R = 2.6
        fixed = Line(origin - R * d1, origin + R * d1, color=ANT1, stroke_width=5)
        angle = ValueTracker(-0.4)
        par = float(np.arctan(slope))

        def direction():
            t = angle.get_value()
            return np.array([np.cos(t), np.sin(t), 0.0])

        moving = always_redraw(lambda: Line(pivot - R * direction(), pivot + R * direction(), color=ANT2, stroke_width=5))

        def meet():
            dd = direction()
            mat = np.column_stack((d1[:2], -dd[:2]))
            if abs(np.linalg.det(mat)) < 1e-4:
                return origin + 40 * d1
            return origin + np.linalg.solve(mat, (pivot - origin)[:2])[0] * d1

        def meet_dot():
            q = meet()
            on = np.linalg.norm(q - origin) < R - 0.1 and np.linalg.norm(q - pivot) < R - 0.1
            return Dot(q if on else origin, radius=0.1, color=YELLOW).set_opacity(1 if on else 0)

        point = always_redraw(meet_dot)
        self.cue(8)
        top8 = fit(VGroup(MathTex(r"\begin{cases} a\,x + b\,y = e \\ c\,x + d\,y = f \end{cases}"),
                          MathTex(r"\text{has a unique solution} \iff \det\begin{bmatrix} a & b \\ c & d \end{bmatrix} \neq 0"))
                   .arrange(RIGHT, buff=0.7), h=1.4).move_to(TOP)
        nonzero = MathTex(r"\det \neq 0", color=SOFT).scale(0.8).move_to(BOT + RIGHT * 4.3)
        self.play(FadeIn(top8[0]), Create(fixed), Create(moving), FadeIn(nonzero), run_time=0.8)
        self.play(FadeIn(top8[1]), run_time=0.6)
        self.add(point)
        self.cue_at(8, "unique", lead=0.1)
        self.play(Flash(point, color=YELLOW, line_length=0.2, flash_radius=0.25), run_time=0.5)
        self.play(angle.animate.set_value(par), run_time=1.6, rate_func=rate_functions.ease_in_quad)
        self.remove(point)
        zero1 = MathTex(r"\det = 0", color=SOFT).scale(0.8).move_to(nonzero)
        self.play(FadeOut(nonzero), FadeIn(zero1), run_time=0.3)

        # 9 — scaling: the statement above; below, the unit square stretches and shears (ghost kept)
        self.cue(9)
        self.play(FadeOut(VGroup(fixed, moving, zero1, top8)), run_time=0.35)
        top9 = MathTex(r"\text{area}(A\,S) = |\det A| \cdot \text{area}(S)").move_to(TOP)
        center = BOT + LEFT * 0.8 + DOWN * 0.15
        u = 0.55
        Pp = lambda x, y: center + u * np.array([x, y, 0.0])
        grid = VGroup(*[Line(Pp(x, -2), Pp(x, 2), color=DIM, stroke_width=2) for x in range(-3, 4)],
                      *[Line(Pp(-3, y), Pp(3, y), color=DIM, stroke_width=2) for y in range(-2, 3)])
        sq_pts = [Pp(0, 0), Pp(1, 0), Pp(1, 1), Pp(0, 1)]
        square = Polygon(*sq_pts, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.3)
        ghost = Polygon(*sq_pts, stroke_color=SOFT, stroke_width=2, fill_opacity=0).set_stroke(opacity=0.8)
        plane = VGroup(grid, square)
        self.play(LaggedStart(*[Create(l) for l in grid], lag_ratio=0.03), FadeIn(square), run_time=0.7)
        self.add(ghost)
        self.cue_at(9, "scales", lead=0.2)
        self.play(FadeIn(top9), run_time=0.6)
        self.play(ApplyMatrix([[2, 0], [0, 1]], plane, about_point=center), run_time=1.0)
        self.play(ApplyMatrix([[1, 0.5], [0, 1]], plane, about_point=center), run_time=1.0)
        self.play(Indicate(square, color=YELLOW, scale_factor=1.08), run_time=0.7)

        # 10 — polygon area: the formula above; below, the polygon fanned into numbered triangles
        self.cue(10)
        U, O = 0.42, np.array([-1.3, -3.6, 0])
        Q = lambda x, y: O + U * np.array([x, y, 0.0])
        V = [(2, 1), (5, 2), (5, 4), (3, 5), (1, 3)]
        poly = Polygon(*[Q(*v) for v in V], stroke_color=INK, stroke_width=4, fill_opacity=0)
        tris = [(V[i], V[(i + 1) % 5]) for i in range(5)]
        tri = lambda a, b, col, op: Polygon(O, Q(*a), Q(*b), stroke_color=col, stroke_width=1.5, fill_color=col, fill_opacity=op)
        signed = [(a, b, a[0] * b[1] - a[1] * b[0]) for a, b in tris]
        assert sum(d for _, _, d in signed) / 2 == 10.5
        tv = VGroup(*[tri(a, b, YELLOW if d > 0 else SOFT, 0.4 if d > 0 else 0.55) for a, b, d in signed])
        labs = VGroup(*[MathTex(str(k + 1), color=BLACK if d > 0 else WHITE).scale(0.6)
                        .move_to((O + Q(*a) + Q(*b)) / 3) for k, (a, b, d) in enumerate(signed)])
        for k, (a, b, d) in enumerate(signed):
            if d < 0:
                labs[k].set_color(SOFT).shift(LEFT * 0.22)
        labs[0].move_to((O + Q(*V[0]) + Q(*V[1])) / 3 + DOWN * 0.2 + RIGHT * 0.16)
        self.play(FadeOut(plane), FadeOut(ghost), FadeOut(top9), Create(poly), run_time=0.8)
        self.remove(plane, ghost, *grid, square)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(t), FadeIn(l)) for t, l in zip(tv, labs)], lag_ratio=0.45), run_time=1.6)
        self.add(poly)
        shoe = fit(MathTex(r"\text{Area} = \tfrac{1}{2}\left[\det\!\left(M_{\triangle_1}\right) + \det\!\left(M_{\triangle_2}\right) + \cdots + \det\!\left(M_{\triangle_5}\right)\right]")).move_to(TOP)
        self.play(Write(shoe), run_time=1.2)
        self.wait(0.6)

        # 11 — "one of the most surprising places ... combinatorics": only the title is left
        self.cue(11)
        self.play(FadeOut(VGroup(poly, shoe, tv, labs)), run_time=0.6)

        # 12 — "how determinants can count": the title lights up as it is said
        self.cue(12)
        self.cue_at(12, "how determinants", lead=0.2)
        self.sfx("chime")
        self.play(title.animate.set_color(YELLOW).scale(1.08), run_time=0.8)
        self.cue_end(12)
        self.wait(0.6)

        # 13 — the title leaves; "let's start with a simple puzzle"
        self.cue(13)
        self.play(FadeOut(title, shift=UP * 0.3), run_time=0.6)
        card = T("First, a simple puzzle", 44, weight=BOLD)
        self.play(Write(card), run_time=1.0)
        self.cue_end(13)
        self.wait(0.6)
        self.play(FadeOut(card), run_time=0.6)
