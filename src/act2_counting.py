"""Act 2 — Rules, and counting one walker (2:15-3:45).

Scenes (each renders on its own):
    Rules           three rules appear beside the grid
    OneWalkerPaths  pause card, then all 6 paths A1 -> B1 with a counter
    PascalNumbers   left + below numbers fill the grid, ending in 6 = C(4,2)
"""
from common import *

GRID_C = LEFT * 3.4 + DOWN * 0.2


def setup_grid(scene, ants_shown=(1, 2), houses_shown=(1, 2), animate=True):
    lat = Lattice(4, spacing=1.5, center=GRID_C)
    ends = endpoints(lat)
    # endpoints() order: A1 dot, A1 label, A2 dot, A2 label, B1 house, B1 label, B2 house, B2 label
    keep = VGroup()
    if 1 in ants_shown:
        keep.add(ends[0], ends[1])
    if 2 in ants_shown:
        keep.add(ends[2], ends[3])
    if 1 in houses_shown:
        keep.add(ends[4], ends[5])
    if 2 in houses_shown:
        keep.add(ends[6], ends[7])
    if animate:
        scene.play(LaggedStartMap(FadeIn, lat, lag_ratio=0.03, run_time=1))
        scene.play(FadeIn(keep, lag_ratio=0.1))
    else:
        scene.add(lat, keep)
    return lat, keep


class Rules(DScene):
    def construct(self):
        lat, ends = setup_grid(self)
        a1 = ant(ANT1).move_to(lat.p(*A1))
        a2 = ant(ANT2).move_to(lat.p(*A2))
        self.play(FadeIn(a1, scale=0.5), FadeIn(a2, scale=0.5))

        head = T("The rules", 40, INK, weight=BOLD)
        r1 = VGroup(T("1.", 30, SOFT), T("Walk only right or up.", 30))
        r2 = VGroup(T("2.", 30, SOFT),
                    VGroup(T("Ant 1:  A₁ → B₁", 30, ANT1),
                           T("Ant 2:  A₂ → B₂", 30, ANT2))
                    .arrange(DOWN, aligned_edge=LEFT, buff=0.15))
        r3 = VGroup(T("3.", 30, SOFT),
                    T("The ants may never stand\non the same dot.", 30,
                      line_spacing=1.1, t2c={"never": MEET}))
        for r in (r1, r2, r3):
            r.arrange(RIGHT, aligned_edge=UP, buff=0.25)
        rules = VGroup(head, r1, r2, r3).arrange(DOWN, aligned_edge=LEFT,
                                                 buff=0.5)
        rules.to_edge(RIGHT, buff=0.7)

        self.play(Write(head))
        # Rule 1: arrows right and up from the purple ant
        self.play(FadeIn(r1, shift=LEFT * 0.3))
        arr = VGroup(
            Arrow(a1.get_center(), lat.p(1, 1), buff=0.25, color=INK,
                  stroke_width=5, max_tip_length_to_length_ratio=0.3),
            Arrow(a1.get_center(), lat.p(0, 2), buff=0.25, color=INK,
                  stroke_width=5, max_tip_length_to_length_ratio=0.3))
        self.play(GrowArrow(arr[0]), GrowArrow(arr[1]))
        self.wait(0.6)
        self.play(FadeOut(arr))

        # Rule 2: each ant points to its own house
        self.play(FadeIn(r2, shift=LEFT * 0.3))
        h1 = CurvedArrow(lat.p(*A1) + UP * 0.25, lat.p(*B1) + LEFT * 0.3,
                         angle=-PI / 3, color=ANT1, stroke_width=4)
        h2 = CurvedArrow(lat.p(*A2) + RIGHT * 0.25, lat.p(*B2) + DOWN * 0.3,
                         angle=PI / 3, color=ANT2, stroke_width=4)
        self.play(Create(h1), Create(h2), run_time=1.2)
        self.wait(0.6)
        self.play(FadeOut(h1), FadeOut(h2))

        # Rule 3: both on one dot -> amber ring and a cross
        self.play(FadeIn(r3, shift=LEFT * 0.3))
        spot = lat.p(1, 1)
        self.play(a1.animate.move_to(spot + LEFT * 0.18),
                  a2.animate.move_to(spot + RIGHT * 0.18), run_time=0.8)
        ring = Circle(radius=0.42, color=MEET, stroke_width=5).move_to(spot)
        no = cross(0.5).move_to(spot + UR * 0.45)
        self.play(Create(ring), FadeIn(no, scale=1.5))
        self.play(ring.animate.scale(1.15), rate_func=there_and_back,
                  run_time=0.5)
        self.play(a1.animate.move_to(lat.p(*A1)), a2.animate.move_to(lat.p(*A2)),
                  FadeOut(ring), FadeOut(no), run_time=0.8)
        self.wait(1.5)


def single_icon(P, color=ANT1, size=0.9):
    lat = Lattice(4, spacing=size / 3, dot_radius=0.025, color=DIM)
    frame = RoundedRectangle(corner_radius=0.08, width=size * 1.4,
                             height=size * 1.4, stroke_color=DIM,
                             stroke_width=1.5).move_to(lat)
    return VGroup(frame, lat, path_mob(lat, P, color, 4))


class OneWalkerPaths(DScene):
    def construct(self):
        lat, ends = setup_grid(self, ants_shown=(1,), houses_shown=(1,),
                               animate=False)
        a1 = ant(ANT1).move_to(lat.p(*A1))
        self.add(a1)

        card = over_to_you("How many ways can ant 1\nget from A₁ to B₁?\n"
                           "Pause and count.")
        self.play(FadeIn(card, scale=0.9))
        for k in (3, 2, 1):
            n = T(str(k), 60, MEET, weight=BOLD).next_to(card, DOWN, buff=0.3)
            self.play(FadeIn(n, scale=1.4), run_time=0.3)
            self.wait(0.6)
            self.play(FadeOut(n), run_time=0.1)
        self.play(FadeOut(card))

        paths = all_paths(A1, B1)
        # Thumbnail slots on the right: 2 rows x 3
        slots = VGroup(*[single_icon(P) for P in paths]) \
            .arrange_in_grid(2, 3, buff=(0.45, 0.75))
        slots.move_to(RIGHT * 3.3 + DOWN * 0.1)
        labels = VGroup(*[T(moves(P), 24, SOFT).next_to(s, DOWN, buff=0.12)
                          for P, s in zip(paths, slots)])

        cnt_label = T("paths:", 34, SOFT)
        cnt = T("0", 56, ANT1)
        counter = VGroup(cnt_label, cnt).arrange(RIGHT, buff=0.25)
        counter.next_to(slots, UP, buff=0.55)
        self.play(FadeIn(counter))

        for i, P in enumerate(paths):
            slow = i < 2
            a1.heading = 0.0
            anims, traces = walk_steps(lat, [(a1, P, ANT1)],
                                       step_time=0.4 if slow else 0.16)
            for an in anims:
                self.play(an)
            trace = VGroup(*traces)
            self.sfx("tick")
            self.play(ReplacementTransform(trace, slots[i][2]),
                      FadeIn(slots[i][:2]), FadeIn(labels[i], shift=UP * 0.1),
                      Transform(cnt, T(str(i + 1), 56, ANT1).move_to(cnt)),
                      run_time=0.7 if slow else 0.4)
            # ant hops back to the start
            self.play(a1.animate.move_to(lat.p(*A1)).rotate(-a1.heading),
                      run_time=0.25)
            a1.heading = 0.0

        self.play(Indicate(cnt, color=MEET, scale_factor=1.4))
        note = T("2 rights + 2 ups, in any order", 28, INK) \
            .next_to(slots, DOWN, buff=0.75)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(2)


class PascalNumbers(DScene):
    def construct(self):
        lat, ends = setup_grid(self, ants_shown=(1,), houses_shown=(1,),
                               animate=False)
        # Dim the dots that ant 1 can never reach
        region = [(x, y) for x in range(3) for y in range(1, 4)]
        others = VGroup(*[d for k, d in lat.dots.items() if k not in region])
        self.play(others.animate.set_opacity(0.2), ends.animate.set_opacity(0.35))

        def bubble(v, x, y, col=INK):
            c = Circle(radius=0.3, color=col, stroke_width=2.5, fill_color=BG,
                       fill_opacity=1)
            return VGroup(c, T(str(v), 34, col).move_to(c)) \
                .move_to(lat.p(x, y))

        val, bub = {}, {}
        val[A1] = 1
        bub[A1] = bubble(1, *A1, ANT1)
        self.play(FadeIn(bub[A1], scale=1.6))
        self.wait(0.5)

        # Fill by anti-diagonals so the "left + below" flow reads clearly
        order = sorted([q for q in region if q != A1],
                       key=lambda q: (q[0] + q[1], q[0]))
        sums = VGroup()
        for (x, y) in order:
            preds = [q for q in [(x - 1, y), (x, y - 1)] if q in val]
            v = sum(val[q] for q in preds)
            val[(x, y)] = v
            final = (x, y) == B1
            arrows = VGroup(*[
                Arrow(lat.p(*q), lat.p(x, y), buff=0.32, stroke_width=5,
                      color=MEET, max_tip_length_to_length_ratio=0.35)
                for q in preds])
            b = bubble(v, x, y, ANT1 if final else INK)
            rt = 0.7 if len(preds) == 2 else 0.4
            self.play(*[GrowArrow(a) for a in arrows], run_time=rt)
            anims = [FadeIn(b, scale=1.4)]
            if len(preds) == 2:
                s = T(f"{val[preds[0]]} + {val[preds[1]]}", 22, MEET) \
                    .next_to(b, UR, buff=0.02)
                sums.add(s)
                anims.append(FadeIn(s))
            self.sfx("tick")
            self.play(*anims, run_time=rt)
            self.play(FadeOut(arrows), run_time=0.25)
            bub[(x, y)] = b

        self.play(FadeOut(sums))
        six = bub[B1]
        self.play(six.animate.scale(1.3), Flash(six, color=ANT1, line_length=0.25),
                  run_time=0.8)
        self.play(six.animate.scale(1 / 1.3))

        # Tilt to show Pascal's triangle
        tri = VGroup(*[bub[q] for q in region]).copy()
        tri_title = T("Pascal's triangle, tilted", 30, SOFT)
        tri.generate_target()
        tri.target.rotate(-3 * PI / 4, about_point=lat.p(1, 2)) \
            .move_to(RIGHT * 3.3 + UP * 0.6)
        for b in tri.target:
            b.rotate(3 * PI / 4)
        self.play(MoveToTarget(tri), run_time=1.5)
        tri_title.next_to(tri, UP, buff=0.4)
        self.play(FadeIn(tri_title))

        formula = VGroup(T("4 steps, choose which 2 go right:", 28, INK),
                         T("C(4, 2) = 6", 40, ANT1, weight=BOLD)) \
            .arrange(DOWN, buff=0.25).next_to(tri, DOWN, buff=0.6)
        self.play(Write(formula[0]), run_time=1)
        self.play(FadeIn(formula[1], scale=1.2))
        self.wait(2)
