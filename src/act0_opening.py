"""Act 0 — opening v11 (Priyanshu's script, 8 Nov): school 2x2 and 3x3, general forms, uses, combinatorics, title.
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
import os
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
        self.play(FadeOut(formula, shift=UP * 0.3), run_time=0.5)          # each use brings its own maths to the top

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

        # 3-4 — the general forms, quickly: row expansion, eigenvalues, permutations (one line, fast animations)
        self.cue(3)
        self.play(FadeOut(VGroup(m3, d3, out)), run_time=0.5)
        fm = VGroup(
            MathTex(r"\det A", "=", r"\sum_{j=1}^{n} (-1)^{1+j}\, a_{1j}\, \det A_{1j}"),
            MathTex(r"\det A", "=", r"\lambda_1 \lambda_2 \cdots \lambda_n"),
            MathTex(r"\det A", "=", r"\sum_{\sigma \in S_n} \operatorname{sgn}(\sigma)\, a_{1\sigma(1)}\, a_{2\sigma(2)} \cdots a_{n\sigma(n)}"),
        )
        for f in fm:
            f.scale(0.78)
        fm.arrange(DOWN, buff=0.6).move_to(RIGHT * 2.6 + DOWN * 0.4)
        for f in fm[1:]:
            f.shift(RIGHT * (fm[0][1].get_x() - f[1].get_x()))
        if fm.get_right()[0] > 6.9:
            fm.shift(LEFT * (fm.get_right()[0] - 6.9))
        L3 = [["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]]
        LEFTC = LEFT * 3.7 + DOWN * 0.1
        self.cue(4)
        # expand along a row
        mx = Matrix(L3, h_buff=0.85, v_buff=0.7).scale(1.0).move_to(LEFTC + UP * 0.6)
        ent = mx.get_entries()
        self.play(FadeIn(mx), run_time=0.5)
        minors = [[(1, 1), (1, 2), (2, 1), (2, 2)], [(1, 0), (1, 2), (2, 0), (2, 2)], [(1, 0), (1, 1), (2, 0), (2, 1)]]
        terms = VGroup()
        for j in range(3):
            keep = [3 * r + c for r, c in minors[j]]
            dim = [k for k in range(9) if k not in keep and k != j]
            box = SurroundingRectangle(ent[j], color=YELLOW, buff=0.08)
            mn = [L3[r][c] for r, c in minors[j]]
            sg = "+" if j % 2 == 0 else "-"
            t = MathTex(sg, L3[0][j], r"\det\begin{bmatrix} %s & %s \\ %s & %s \end{bmatrix}" % tuple(mn)).scale(0.62)
            t[0].set_color(GOOD if sg == "+" else BAD)
            if j == 0:
                t[0].set_opacity(0)
            terms.add(t)
            terms.arrange(RIGHT, buff=0.15).next_to(mx, DOWN, buff=0.35)
            self.play(Create(box), *[ent[k].animate.set_opacity(0.2) for k in dim], run_time=0.45)
            self.play(FadeIn(t, shift=DOWN * 0.1), run_time=0.45)
            self.play(FadeOut(box), *[ent[k].animate.set_opacity(1) for k in dim], run_time=0.3)
        self.play(FadeIn(fm[0], shift=LEFT * 0.2), run_time=0.7)
        # multiply the eigenvalues
        self.cue(5)
        self.play(FadeOut(VGroup(mx, terms)), run_time=0.4)
        o5 = LEFTC + DOWN * 1.0 + LEFT * 0.4
        v1, v2 = np.array([1.4, 0.45, 0]), np.array([-0.45, 1.25, 0])
        a1 = Arrow(o5, o5 + v1, buff=0, color=ANT1, stroke_width=6)
        a2 = Arrow(o5, o5 + v2, buff=0, color=ANT2, stroke_width=6)
        par = Polygon(o5, o5 + v1, o5 + v1 + v2, o5 + v2, stroke_width=0, fill_color=YELLOW, fill_opacity=0.3)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(par), run_time=0.7)
        l1, l2 = 2.0, 1.5
        self.play(a1.animate.put_start_and_end_on(o5, o5 + l1 * v1), a2.animate.put_start_and_end_on(o5, o5 + l2 * v2),
                  Transform(par, Polygon(o5, o5 + l1 * v1, o5 + l1 * v1 + l2 * v2, o5 + l2 * v2, stroke_width=0,
                                         fill_color=YELLOW, fill_opacity=0.3)), run_time=1.2)
        self.play(FadeIn(fm[1], shift=LEFT * 0.2), run_time=0.7)
        # signed products over permutations
        self.cue(6)
        self.play(FadeOut(VGroup(a1, a2, par)), run_time=0.4)
        my = Matrix(L3, h_buff=0.85, v_buff=0.7).scale(1.0).move_to(LEFTC + UP * 0.2)
        ey = my.get_entries()
        self.play(FadeIn(my), run_time=0.5)
        for p, sg in [((0, 1, 2), "+"), ((1, 2, 0), "+"), ((2, 0, 1), "+"), ((2, 1, 0), "-"), ((0, 2, 1), "-"), ((1, 0, 2), "-")]:
            col = GOOD if sg == "+" else BAD
            bx = VGroup(*[SurroundingRectangle(ey[3 * i + p[i]], color=col, buff=0.08) for i in range(3)])
            self.play(Create(bx), run_time=0.35)
            self.play(FadeOut(bx), run_time=0.2)
        self.play(FadeIn(fm[2], shift=LEFT * 0.2), run_time=0.7)

        # 5 — it shows up all over mathematics
        self.cue(7)
        self.play(FadeOut(fm, shift=DOWN * 0.3), FadeOut(my), run_time=0.6)

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
        assert sum(d for _, _, d in signed) / 2 == 10.5
        self.play(FadeOut(plane), FadeOut(ghost), FadeOut(top9), Create(poly), run_time=0.8)
        self.remove(plane, ghost, *grid, square)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(t), FadeIn(l)) for t, l in zip(tv, labs)], lag_ratio=0.45), run_time=1.6)
        self.add(poly)
        shoe = VGroup(MathTex(r"\text{Area} = \tfrac{1}{2}\sum_{i=1}^{5} \det M_{T_i}"),
                      MathTex(r"M_{T_i} = \begin{bmatrix} x_i & x_{i+1} \\ y_i & y_{i+1} \end{bmatrix}"))
        shoe.arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.5)
        self.play(Write(shoe[0]), run_time=1.0)
        self.play(FadeIn(shoe[1]), run_time=0.6)
        self.wait(0.6)
        self.play(FadeOut(tv), FadeOut(labs), poly.animate.set_fill(YELLOW, 0.4), run_time=0.8)

        # 9 — fast: O(n^3) computations by Gaussian elimination (Gauss's portrait at the side), and even faster
        self.cue(11)
        self.play(FadeOut(VGroup(poly, shoe)), run_time=0.6)
        head_c = T("algebraic complexity theory", 30, YELLOW).move_to(UP * 2.55)
        dform = MathTex(r"\det A", "=", r"\sum_{\sigma} \operatorname{sgn}(\sigma)", r"\prod_{i} a_{i\sigma(i)}").scale(0.95)
        dform.move_to(UP * 1.45 + LEFT * 1.6)
        easy = VGroup(T("easy", 28, GOOD), tick(0.3)).arrange(RIGHT, buff=0.15).next_to(dform, RIGHT, buff=0.6)
        speed = VGroup(MathTex(r"O(n^3) \text{ computations using Gaussian elimination}").scale(0.85),
                       MathTex(r"\text{and even faster}", color=GOOD).scale(0.85)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        speed.move_to(DOWN * 0.6 + LEFT * 0.9)
        gpic = Group()
        gf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "portraits", "gauss.jpg")
        if os.path.exists(gf):
            gim = ImageMobject(gf).set_height(2.0)
            gpic = Group(gim, SurroundingRectangle(gim, color=GREY_B, buff=0.02, stroke_width=1.5))
            gpic.next_to(speed, RIGHT, buff=0.6)
            if gpic.get_right()[0] > 6.9:
                gpic.shift(LEFT * (gpic.get_right()[0] - 6.9))
        self.play(Write(dform), run_time=1.0)
        self.cue_at(11, "Gaussian elimination", lead=0.2)
        self.play(FadeIn(speed[0]), FadeIn(gpic), run_time=0.8)
        self.cue_at(11, "even faster", lead=0.2)
        self.play(FadeIn(speed[1], shift=UP * 0.1), run_time=0.6)

        # 10 — algebraic complexity theory: the determinant is the model of an easy polynomial
        self.cue(12)
        self.play(FadeOut(speed), FadeOut(gpic), run_time=0.5)
        self.cue_at(12, "algebraic complexity", lead=0.2)
        self.play(FadeIn(head_c, shift=DOWN * 0.15), run_time=0.7)
        self.cue_at(12, "there, the determinant", lead=0.2)
        self.play(FadeIn(easy), Indicate(dform, color=GOOD, scale_factor=1.05), run_time=0.8)

        # 11 — its twin, the permanent: the same sum without the signs; believed much harder
        self.cue(13)
        pform = MathTex(r"\operatorname{perm} A", "=", r"\sum_{\sigma}", r"\prod_{i} a_{i\sigma(i)}").scale(0.95)
        pform.next_to(dform, DOWN, buff=0.55)
        pform.shift(RIGHT * (dform[1].get_x() - pform[1].get_x()))
        ghost_d = dform.copy()
        self.play(ghost_d.animate.move_to(pform, aligned_edge=LEFT).shift(RIGHT * (dform[1].get_x() - pform[1].get_x()) * 0), run_time=0.6)
        strike = Line(ghost_d[2].get_corner(DL), ghost_d[2].get_corner(UR), color=BAD, stroke_width=5)
        self.cue_at(13, "without the minus signs", lead=0.2)
        self.play(Create(strike), run_time=0.5)
        self.play(ReplacementTransform(VGroup(ghost_d, strike), pform), run_time=0.8)
        hard = VGroup(T("believed hard", 28, BAD)).next_to(pform, RIGHT, buff=0.6).align_to(easy, LEFT)
        self.cue_at(13, "believed", lead=0.2)
        self.play(FadeIn(hard), run_time=0.5)

        # 12 — Valiant 1979: the permanent is #P-complete (#P = counting the solutions of NP problems)
        self.cue(14)
        vp = Group()
        vf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "portraits", "valiant.jpg")
        if os.path.exists(vf):
            vim = ImageMobject(vf).set_height(1.7)
            vp = Group(vim, SurroundingRectangle(vim, color=GREY_B, buff=0.02, stroke_width=1.5)).move_to(LEFT * 5.5 + DOWN * 1.9)
        vt = VGroup(T("Leslie Valiant, 1979", 26, YELLOW),
                    MathTex(r"\operatorname{perm} \text{ is } \#\mathrm{P}\text{-complete}").scale(0.8),
                    MathTex(r"\#\mathrm{P}: \text{ count the solutions of an NP problem}", color=SOFT).scale(0.62)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        vt.next_to(vp, RIGHT, buff=0.35) if len(vp) else vt.move_to(LEFT * 2.5 + DOWN * 1.85)
        self.cue_at(14, "Leslie Valiant", lead=0.2)
        self.play(FadeIn(vp), FadeIn(vt[0]), run_time=0.7)
        self.cue_at(14, "sharp-P", lead=0.2)
        self.play(FadeIn(vt[1]), run_time=0.6)
        self.cue_at(14, "counting the solutions", lead=0.2)
        self.play(FadeIn(vt[2]), run_time=0.6)

        imp = MathTex(r"\text{efficient algorithm} \;\Rightarrow\; \mathrm{P} = \mathrm{NP} \text{ (and much more)}", color=BAD).scale(0.75)
        imp.move_to(DOWN * 3.45 + RIGHT * 0.6)
        self.cue_at(14, "efficient algorithm", lead=0.2)
        self.play(Write(imp), run_time=1.0)

        # 13 — so counting is usually hard; and yet determinants are one of the rare tricks that count efficiently
        self.cue(15)
        self.cue_at(15, "And yet", lead=0.2)
        self.play(Indicate(dform, color=YELLOW, scale_factor=1.08), run_time=0.9)
        cplx = Group(head_c, dform, easy, pform, hard, vp, vt, imp)

        prev = cplx                                   # (no montage: 'combinatorics' is only said)

        # 19 — today: how determinants can count (title in the centre as it is said)
        self.cue(16)
        title = T("How Determinants Can Count", 50, weight=BOLD)
        self.cue_at(16, "how determinants", lead=0.2)
        self.play(FadeOut(prev), run_time=0.5)
        self.sfx("chime")
        self.play(Write(title), run_time=1.3)

        # 20 — "let's start with a simple puzzle": clear the screen (the Hook brings the ants)
        self.cue(17)
        self.cue_at(17, "simple puzzle", lead=0.2)
        self.play(FadeOut(title), run_time=0.8)


