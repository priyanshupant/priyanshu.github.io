"""Act 2 — One walker (Script v2, 2:30-3:30).

    ListRoutes   ant 1 walks his 10 routes; thumbnails with words; pattern 2R + 3U
    Slots        5 slots, choose which 2 are R: C(5,2) = 10; the four counts we need
"""
from math import comb

from common import *
from act1_problem import GRID_C


def route_icon(P, color=ANT1, size=0.85):
    lat = Lattice(GRID[0], spacing=size / (max(GRID) - 1), dot_radius=0.022, color=DIM, ny=GRID[1])
    frame = RoundedRectangle(corner_radius=0.07, width=size * 1.15, height=size * 1.15,
                             stroke_color=DIM, stroke_width=1.5).move_to(lat)
    return VGroup(frame, lat, path_mob(lat, P, color, 4))


def word_mob(P, size=24):
    w = moves(P)
    return VGroup(*[T(c, size, GOOD if c == "R" else BLUE_B) for c in w]).arrange(RIGHT, buff=0.06)


class ListRoutes(DScene):
    def construct(self):
        lat = Lattice(GRID[0], spacing=1.45, center=GRID_C + RIGHT * 0.3, ny=GRID[1])
        ends = endpoints(lat, scale=1.1)
        L = ant(ANT1, 0.85).move_to(lat.p(*A1))
        self.add(lat, ends[0], ends[1], ends[4], ends[5], L)
        q = T("How many ways can ant 1 get home?", 32).to_edge(UP, buff=0.35).shift(RIGHT * 1.6)
        self.cue(0)
        self.play(Write(q))
        paths = all_paths(A1, B1)
        icons = VGroup(*[route_icon(P, size=1.05) for P in paths]).arrange_in_grid(2, 3, buff=(0.55, 0.8))
        icons.move_to(RIGHT * 3.4 + UP * 0.7)
        words = VGroup(*[word_mob(P, 24).next_to(ic, DOWN, buff=0.1) for P, ic in zip(paths, icons)])
        cnt_lab = T("routes:", 34, SOFT).move_to(RIGHT * 1.7 + DOWN * 2.4)
        cnt = T("0", 54, ANT1).next_to(cnt_lab, RIGHT, buff=0.25)
        self.add(cnt_lab)
        self.add(cnt)
        self.cue(1)
        said = ["Right, right, up, up", "Right, up, right, up", "Right, up, up, right", "Up, right, right, up",
                "Up, right, up, right", "up, up, right, right"]
        assert ["".join("R" if c == "R" else "U" for c in moves(P)) for P in paths] == \
            ["".join(w[0].upper() for w in ph.split(", ")) for ph in said]
        for i, P in enumerate(paths):
            slow = i < 1
            self.cue_at(1, said[i], lead=0.05)
            anims, traces = walk_steps(lat, [(L, P, ANT1)], step_time=0.25 if slow else 0.14)
            for an in anims:
                self.play(an)
            self.sfx("tick")
            self.play(ReplacementTransform(VGroup(*traces), icons[i][2]), FadeIn(icons[i][:2]),
                      FadeIn(words[i]), Transform(cnt, T(str(i + 1), 54, ANT1).move_to(cnt)),
                      run_time=0.6 if slow else 0.35)
            self.play(L.animate.move_to(lat.p(*A1)), run_time=0.15)
        self.cue(2)
        self.play(Indicate(cnt, color=YELLOW, scale_factor=1.3))
        # the pattern
        self.cue(3)
        boxes = VGroup(*[SurroundingRectangle(w, color=YELLOW, buff=0.05) for w in words])
        R_, U_ = B1[0] - A1[0], B1[1] - A1[1]
        pat = T(f"always {R_ + U_} steps: {R_} R and {U_} U", 32, YELLOW).next_to(cnt_lab, DOWN, buff=0.35, aligned_edge=LEFT)
        self.cue_at(3, "every route")
        self.play(Create(boxes, lag_ratio=0.05), FadeIn(pat))
        why = T(f"(home is {R_} right and {U_} up)", 26, SOFT).next_to(pat, DOWN, buff=0.12, aligned_edge=LEFT)
        self.cue_at(3, "forced")
        self.play(FadeIn(why))
        hr = DoubleArrow(lat.p(*A1) + DOWN * 0.45, lat.p(B1[0], A1[1]) + DOWN * 0.45, buff=0, color=GOOD, stroke_width=4)
        hu = DoubleArrow(lat.p(B1[0], A1[1]) + RIGHT * 0.45, lat.p(*B1) + RIGHT * 0.45, buff=0, color=BLUE_B, stroke_width=4)
        self.play(GrowFromCenter(hr), GrowFromCenter(hu))


class Slots(DScene):
    def construct(self):
        from itertools import combinations
        R_, U_ = B1[0] - A1[0], B1[1] - A1[1]
        nst = R_ + U_
        head = T("A route is a choice", 42).to_edge(UP, buff=0.45)
        self.cue(0)
        self.play(Write(head))
        lat = Lattice(GRID[0], spacing=1.05, center=LEFT * 4.3 + DOWN * 0.4, ny=GRID[1])
        ends = endpoints(lat, scale=0.95)
        self.play(FadeIn(lat), FadeIn(VGroup(ends[0], ends[1], ends[4], ends[5])))
        slots = VGroup(*[Square(1.25, color=GREY_B) for _ in range(nst)]).arrange(RIGHT, buff=0.25).move_to(RIGHT * 2.2 + UP * 1.3)
        nums = VGroup(*[T(f"step {k + 1}", 22, GREY_C).next_to(s, UP, buff=0.12) for k, s in enumerate(slots)])
        self.cue_at(0, "choice of which")
        self.play(Create(slots), FadeIn(nums))
        cnt = T("0", 48, YELLOW).next_to(slots, RIGHT, buff=0.6)
        letters = route = None
        self.cue_at(0, "go right")
        for k, c in enumerate(combinations(range(nst), R_)):
            new = VGroup(*[T("R" if j in c else "U", 56, GOOD if j in c else BLUE_B).move_to(slots[j]) for j in range(nst)])
            pts, x, y = [A1], A1[0], A1[1]
            for j in range(nst):
                x, y = (x + 1, y) if j in c else (x, y + 1)
                pts.append((x, y))
            nr = path_mob(lat, pts, ANT1, 8)
            ncnt = T(str(k + 1), 48, YELLOW).move_to(cnt)
            if letters is None:
                self.play(FadeIn(new), Create(nr), FadeIn(ncnt), run_time=0.7)
            else:
                self.play(FadeOut(letters, run_time=0.1), FadeIn(new), ReplacementTransform(route, nr),
                          Transform(cnt, ncnt), run_time=0.35)
                self.wait(0.15)
            if letters is None:
                cnt = ncnt
            letters, route = new, nr
        ans = T(f"{nst} choose {R_}  =  {comb(nst, R_)}", 52, YELLOW).next_to(slots, DOWN, buff=0.7)
        self.cue(1)
        self.play(Write(ans))
        # 2: the general rule, as a picture
        self.cue(2)
        self.play(*[FadeOut(m) for m in (slots, nums, letters, cnt, route, ans, lat, ends[0], ends[1], ends[4], ends[5])],
                  Transform(head, T("Any route on this grid", 42).move_to(head)))
        g = Lattice(5, spacing=0.9, center=LEFT * 3.6 + DOWN * 0.5, ny=4)
        s0, e0 = (0, 0), (4, 2)
        box = Rectangle(width=4 * 0.9, height=2 * 0.9, color=GREY_B, stroke_width=2).move_to((g.p(*s0) + g.p(*e0)) / 2)
        sd, ed = Dot(g.p(*s0), radius=0.12, color=ANT1), house(ANT1, 0.38).move_to(g.p(*e0))
        ar = DoubleArrow(g.p(0, 0) + DOWN * 0.5, g.p(4, 0) + DOWN * 0.5, buff=0, color=GOOD, stroke_width=4)
        au = DoubleArrow(g.p(4, 0) + RIGHT * 0.5, g.p(4, 2) + RIGHT * 0.5, buff=0, color=BLUE_B, stroke_width=4)
        la = T("a steps right", 28, GOOD).next_to(ar, DOWN, buff=0.12)
        lb = T("b steps up", 28, BLUE_B).next_to(au, RIGHT, buff=0.12)
        self.play(FadeIn(g), Create(box), FadeIn(sd), FadeIn(ed))
        self.cue_at(2, "a steps right")
        self.play(GrowFromCenter(ar), FadeIn(la))
        self.cue_at(2, "b steps up")
        self.play(GrowFromCenter(au), FadeIn(lb))
        frm = VGroup(T("routes  =", 40), T("(a + b) choose a", 44, YELLOW)).arrange(RIGHT, buff=0.3).move_to(RIGHT * 3.2 + UP * 0.4)
        self.cue_at(2, "gives")
        self.play(Write(frm))
        # 3: the four numbers we need, in table order
        self.cue(3)
        self.play(*[FadeOut(m) for m in (g, box, sd, ed, ar, au, la, lb, frm)],
                  Transform(head, T("The four numbers we need", 42).move_to(head)))
        rows = [("ant 1 → its own home", A1, B1, ANT1), ("ant 1 → the other home", A1, B2, ANT1),
                ("ant 2 → the other home", A2, B1, ANT2), ("ant 2 → its own home", A2, B2, ANT2)]
        tab = VGroup()
        for name, a, b, col in rows:
            r, u = b[0] - a[0], b[1] - a[1]
            tab.add(VGroup(T(name, 32, col), T(f"{r} R + {u} U", 32, GREY_B),
                           T(f"({r + u} choose {r}) = {comb(r + u, r)}", 34, YELLOW)))
        for row in tab:
            row.arrange(RIGHT, buff=0.6)
        tab.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.3)
        for row, w in zip(tab, ["its own home: six", "other home: four", "first home: four", "its own: six"]):
            self.cue_at(3, w, lead=0.2)
            self.play(FadeIn(row, shift=UP * 0.2), run_time=0.45)
