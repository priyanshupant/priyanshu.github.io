"""Style comparison stills. Render with:  manim -s -qm style_demo.py <Scene>

    StyleDark   polished dark (glow paths, vignette)
    StyleChalk  chalkboard (chalky strokes, handwritten font)
    StylePaper  light paper (ink colours, serif font)
    AntDesigns  three ant designs side by side
    FontChoices the same lines in four fonts
"""
from manim import *
import numpy as np

A1, A2, B1, B2 = (0, 1), (1, 0), (2, 3), (3, 2)
GOOD_P = [(0, 1), (0, 2), (0, 3), (1, 3), (2, 3)]
GOOD_Q = [(1, 0), (2, 0), (3, 0), (3, 1), (3, 2)]

THEMES = {
    "dark": dict(bg="#0F1117", ink="#E8E8F0", soft="#9AA0AE", dim="#3A3F4B",
                 a1="#9B8CFF", a2="#2EC4B6", meet="#FFB020", bad="#FF5C6C",
                 font="Inter", head_font="Inter"),
    "chalk": dict(bg="#24312C", ink="#F1EFE6", soft="#B9C2B8", dim="#5E6E66",
                  a1="#C9B8FF", a2="#8EE6D9", meet="#FFD36B", bad="#FF9A9A",
                  font="Caveat", head_font="Caveat"),
    "paper": dict(bg="#F5EFE4", ink="#2A2622", soft="#6E665C", dim="#C9BFAF",
                  a1="#5B48C2", a2="#0F8C80", meet="#D98200", bad="#C2362F",
                  font="Inter", head_font="Caladea"),
}


# ------------------------------------------------------------ backgrounds
def noise_bg(base, amount=10, vignette=0.0, seed=1):
    h, w = 360, 640
    rng = np.random.default_rng(seed)
    c = np.array(ManimColor(base).to_rgb()) * 255
    img = np.ones((h, w, 3)) * c
    img += rng.normal(0, amount, (h, w, 1))
    if vignette:
        yy, xx = np.mgrid[0:h, 0:w]
        r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
        img *= (1 - vignette * np.clip(r - 0.3, 0, None))[..., None]
    im = ImageMobject(np.clip(img, 0, 255).astype(np.uint8))
    im.stretch_to_fit_width(config.frame_width).stretch_to_fit_height(config.frame_height)
    im.set_z_index(-100)
    return im


# ------------------------------------------------------------ ants
def ant_cartoon(color, s=0.75, outline="#000000"):
    """Side-view cartoon ant facing right."""
    abdomen = Ellipse(width=0.52 * s, height=0.4 * s).move_to(LEFT * 0.34 * s + UP * 0.04 * s)
    thorax = Ellipse(width=0.24 * s, height=0.19 * s)
    head = Circle(radius=0.15 * s).move_to(RIGHT * 0.25 * s + UP * 0.08 * s)
    body = VGroup(abdomen, thorax, head).set_fill(color, 1) \
        .set_stroke(interpolate_color(ManimColor(color), BLACK, 0.45), 2)
    legs = VGroup()
    for x, dx in [(-0.09, -0.07), (0.0, 0.0), (0.09, 0.07)]:
        legs.add(VMobject().set_points_as_corners([
            np.array([x * s, -0.05 * s, 0]), np.array([(x + dx) * s, -0.17 * s, 0]),
            np.array([(x + 1.6 * dx) * s, -0.3 * s, 0])]))
    antenna = VMobject().set_points_smoothly([
        head.get_center() + np.array([0.03, 0.13, 0]) * s,
        head.get_center() + np.array([0.12, 0.3, 0]) * s,
        head.get_center() + np.array([0.24, 0.3, 0]) * s])
    VGroup(legs, antenna).set_stroke(interpolate_color(ManimColor(color), BLACK, 0.3), 3)
    eye = Circle(radius=0.075 * s, fill_color=WHITE, fill_opacity=1, stroke_width=0) \
        .move_to(head.get_center() + np.array([0.05, 0.03, 0]) * s)
    pupil = Dot(eye.get_center() + RIGHT * 0.03 * s, radius=0.035 * s, color="#111111")
    shine = Dot(pupil.get_center() + UL * 0.012 * s, radius=0.01 * s, color=WHITE)
    smile = Arc(radius=0.06 * s, start_angle=-PI * 0.85, angle=PI * 0.5,
                stroke_width=2, color="#111111").move_to(
        head.get_center() + np.array([0.07, -0.07, 0]) * s)
    return VGroup(legs, antenna, body, eye, pupil, shine, smile)


def ant_minimal(color, s=0.6):
    """Top-down silhouette (the current design)."""
    abdomen = Ellipse(width=0.48 * s, height=0.34 * s).shift(LEFT * 0.36 * s)
    thorax = Ellipse(width=0.26 * s, height=0.2 * s)
    head = Circle(radius=0.12 * s).shift(RIGHT * 0.27 * s)
    body = VGroup(abdomen, thorax, head).set_fill(color, 1).set_stroke(width=0)
    legs = VGroup(*[Line(RIGHT * dx * s, (RIGHT * dx * 1.8 + UP * g * 0.26) * s)
                    for dx in (-0.1, 0, 0.1) for g in (1, -1)])
    ants = VGroup(*[Line(RIGHT * 0.34 * s, (RIGHT * 0.52 + UP * g * 0.14) * s) for g in (1, -1)])
    VGroup(legs, ants).set_stroke(color, 3)
    return VGroup(legs, ants, body)


def ant_dot(color, s=0.6):
    """Coloured circle with a face."""
    c = Circle(radius=0.26 * s, fill_color=color, fill_opacity=1,
               stroke_color=interpolate_color(ManimColor(color), BLACK, 0.4), stroke_width=2)
    eyes = VGroup(*[VGroup(Circle(radius=0.07 * s, fill_color=WHITE, fill_opacity=1, stroke_width=0),
                           Dot(radius=0.035 * s, color="#111111").shift(RIGHT * 0.02 * s))
                    .move_to(c.get_center() + np.array([dx, 0.06, 0]) * s) for dx in (-0.09, 0.09)])
    smile = Arc(radius=0.09 * s, start_angle=-PI * 0.8, angle=PI * 0.6, stroke_width=2.5,
                color="#111111").move_to(c.get_center() + DOWN * 0.1 * s)
    ants = VGroup(*[VMobject().set_points_smoothly([
        c.get_top() + np.array([dx * 0.3, -0.02, 0]) * s,
        c.get_top() + np.array([dx * 0.6, 0.15, 0]) * s,
        c.get_top() + np.array([dx * 0.9, 0.2, 0]) * s]) for dx in (-0.3, 0.3)])
    ants.set_stroke(interpolate_color(ManimColor(color), BLACK, 0.3), 3)
    return VGroup(ants, c, eyes, smile)


def house(color, bg, s=0.4, width=3):
    h = Polygon(np.array([-s / 2, -s / 2, 0]), np.array([s / 2, -s / 2, 0]),
                np.array([s / 2, 0.1 * s, 0]), np.array([0, 0.55 * s, 0]),
                np.array([-s / 2, 0.1 * s, 0]), color=color, stroke_width=width,
                fill_color=bg, fill_opacity=1)
    door = Rectangle(width=0.22 * s, height=0.32 * s, color=color, stroke_width=width * 0.7) \
        .align_to(h, DOWN)
    return VGroup(h, door)


# ------------------------------------------------------------ strokes
def pts_of(lat_p, pts):
    return [lat_p(*q) for q in pts]


def stroke_dark(lat_p, pts, col):
    g = VGroup()
    for w, o in [(30, 0.05), (20, 0.08), (13, 0.16)]:
        g.add(VMobject(stroke_color=col, stroke_width=w, stroke_opacity=o,
                       joint_type=LineJointType.ROUND).set_points_as_corners(pts_of(lat_p, pts)))
    g.add(VMobject(stroke_color=col, stroke_width=7, joint_type=LineJointType.ROUND)
          .set_points_as_corners(pts_of(lat_p, pts)))
    return g


def stroke_chalk(lat_p, pts, col, seed=0):
    rng = np.random.default_rng(seed)
    g = VGroup()
    P = pts_of(lat_p, pts)
    for k in range(4):
        jit = []
        for a, b in zip(P, P[1:]):
            for t in np.linspace(0, 1, 7)[:-1]:
                jit.append(a + (b - a) * t + rng.normal(0, 0.025, 3) * np.array([1, 1, 0]))
        jit.append(P[-1] + rng.normal(0, 0.02, 3) * np.array([1, 1, 0]))
        g.add(VMobject(stroke_color=col, stroke_width=rng.uniform(2.5, 4.5),
                       stroke_opacity=rng.uniform(0.45, 0.8)).set_points_smoothly(jit))
    return g


def stroke_paper(lat_p, pts, col):
    P = pts_of(lat_p, pts)
    return VGroup(
        VMobject(stroke_color=col, stroke_width=8, stroke_opacity=0.18,
                 joint_type=LineJointType.ROUND).set_points_as_corners(
            [p + np.array([0.04, -0.04, 0]) for p in P]),
        VMobject(stroke_color=col, stroke_width=6, joint_type=LineJointType.ROUND)
        .set_points_as_corners(P))


# ------------------------------------------------------------ the shared frame
def build_frame(scene, key):
    th = THEMES[key]
    mode = th.get("mode", key)
    config.background_color = th["bg"]
    scene.camera.background_color = th["bg"]

    def T(s, size=32, col=None, head=False, **kw):
        return Text(s, font=th["head_font"] if head else th["font"],
                    font_size=size * (1.35 if th["font"] == "Caveat" else 1),
                    color=col or th["ink"], **kw)

    if mode == "dark":
        scene.add(noise_bg(th["bg"], amount=3, vignette=0.55))
    elif mode == "chalk":
        scene.add(noise_bg(th["bg"], amount=9, vignette=0.25, seed=3))
    else:
        scene.add(noise_bg(th["bg"], amount=6, vignette=0.12, seed=5))

    sp, origin = 1.35, LEFT * 5.4 + DOWN * 2.4

    def p(x, y):
        return origin + sp * (x * RIGHT + y * UP)

    # dots
    for x in range(4):
        for y in range(4):
            if mode == "chalk":
                d = Dot(p(x, y), radius=0.055, color=th["soft"]).set_opacity(0.8)
            else:
                d = Dot(p(x, y), radius=0.055, color=th["soft"] if mode == "dark" else th["dim"])
            scene.add(d)

    stroke = {"dark": stroke_dark, "chalk": stroke_chalk, "paper": stroke_paper}[mode]
    scene.add(stroke(p, GOOD_P, th["a1"]), stroke(p, GOOD_Q, th["a2"]))
    # starts, homes, labels
    for pt, col, name, d in [(A1, th["a1"], "A₁", LEFT), (A2, th["a2"], "A₂", DOWN)]:
        dot = Dot(p(*pt), radius=0.12, color=col)
        scene.add(dot, T(name, 26, col).next_to(dot, d, buff=0.15))
    for pt, col, name, d in [(B1, th["a1"], "B₁", UP), (B2, th["a2"], "B₂", RIGHT)]:
        h = house(col, th["bg"]).move_to(p(*pt))
        scene.add(h, T(name, 26, col).next_to(h, d, buff=0.12))
    # ants mid-walk
    scene.add(ant_cartoon(th["a1"]).move_to(p(0.55, 3) + UP * 0.2))
    scene.add(ant_cartoon(th["a2"]).rotate(PI / 2).move_to(p(3, 0.6) + RIGHT * 0.2))

    # title
    title = T("How many ways can both ants get home?", 36, head=True)
    title.to_edge(UP, buff=0.45).shift(RIGHT * 0.2)
    scene.add(title)

    # table + det
    cell, o = 1.15, RIGHT * 1.7 + UP * 1.0
    for r in range(2):
        for c in range(2):
            sq = Square(cell, color=th["dim"] if mode != "chalk" else th["soft"],
                        stroke_width=2.5).move_to(o + RIGHT * c * cell + DOWN * r * cell)
            scene.add(sq, T(["6", "4", "4", "6"][2 * r + c], 44).move_to(sq))
    scene.add(T("A₁", 30, th["a1"]).move_to(o + LEFT * 1.05),
              T("A₂", 30, th["a2"]).move_to(o + LEFT * 1.05 + DOWN * cell),
              T("B₁", 30, th["a1"]).move_to(o + UP * 0.95),
              T("B₂", 30, th["a2"]).move_to(o + UP * 0.95 + RIGHT * cell))
    det = VGroup(T("det = 6 × 6 − 4 × 4", 34), T("= 36 − 16 = 20", 34, th["meet"])) \
        .arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 2.4 + DOWN * 1.6)
    scene.add(det)

    # villain chip
    if mode == "dark":
        v = Text("THE PERMANENT", font="Inter", weight=HEAVY, font_size=34, color=th["bad"])
        box = SurroundingRectangle(v, buff=0.22, corner_radius=0.12, color=th["bad"],
                                   stroke_width=2, fill_color=th["bad"], fill_opacity=0.12)
        halo = box.copy().set_stroke(th["bad"], 12, opacity=0.12).set_fill(opacity=0)
        chip = VGroup(halo, box, v)
    elif mode == "chalk":
        v = T("THE PERMANENT", 36, th["bad"])
        chip = VGroup(v, SurroundingRectangle(v, color=th["bad"], buff=0.18, stroke_width=3)
                      .set_stroke(opacity=0.7))
    else:
        v = Text("THE PERMANENT", font="Caladea", weight=BOLD, font_size=34, color=th["bad"])
        chip = VGroup(v, Line(v.get_corner(DL) + DOWN * 0.12, v.get_corner(DR) + DOWN * 0.12,
                              color=th["bad"], stroke_width=2),
                      Line(v.get_corner(DL) + DOWN * 0.2, v.get_corner(DR) + DOWN * 0.2,
                           color=th["bad"], stroke_width=1))
    chip.move_to(RIGHT * 4.6 + DOWN * 3.1)
    scene.add(chip)

    # near-miss ring sample
    ring = Circle(radius=0.33, color=th["meet"], stroke_width=5).move_to(p(1, 1))
    if mode == "dark":
        ring = VGroup(ring.copy().set_stroke(width=16, opacity=0.15), ring)
    scene.add(ring, T("!", 34, th["meet"]).next_to(ring, UR, buff=0.0))


class StyleDark(Scene):
    def construct(self):
        build_frame(self, "dark")


class StyleChalk(Scene):
    def construct(self):
        build_frame(self, "chalk")


class StylePaper(Scene):
    def construct(self):
        build_frame(self, "paper")


class AntDesigns(Scene):
    def construct(self):
        th = THEMES["dark"]
        self.camera.background_color = th["bg"]
        cols = VGroup()
        for name, fn in [("Cartoon", ant_cartoon), ("Minimal (current)", ant_minimal),
                         ("Dot with face", ant_dot)]:
            pair = VGroup(fn(th["a1"]).scale(2.2), fn(th["a2"]).scale(2.2)) \
                .arrange(DOWN, buff=0.7)
            small = VGroup(fn(th["a1"]), fn(th["a2"])).arrange(RIGHT, buff=0.4)
            lab = Text(name, font="Inter", font_size=30, color=th["ink"])
            note = Text("at grid size:", font="Inter", font_size=20, color=th["soft"])
            cols.add(VGroup(lab, pair, note, small).arrange(DOWN, buff=0.45))
        cols.arrange(RIGHT, buff=1.4, aligned_edge=UP)
        self.add(cols)


class FontChoices(Scene):
    def construct(self):
        th = THEMES["dark"]
        self.camera.background_color = th["bg"]
        rows = VGroup()
        for name, font, k in [("Inter", "Inter", 1), ("DejaVu Sans (current)", "DejaVu Sans", 1),
                              ("Serif: Caladea", "Caladea", 1.05), ("Handwritten: Caveat", "Caveat", 1.35)]:
            lab = Text(name, font="Inter", font_size=20, color=th["soft"])
            t1 = Text("How Determinants Can Count", font=font, font_size=40 * k, color=th["ink"])
            t2 = Text("A₁ → B₁   det = 6 × 6 − 4 × 4 = 20", font=font, font_size=30 * k,
                      color=th["a1"])
            rows.add(VGroup(lab, t1, t2).arrange(DOWN, aligned_edge=LEFT, buff=0.12))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(ORIGIN)
        self.add(rows)


# ------------------------------------------------------------ community palettes
# iTerm2 colour schemes (github.com/mbadolato/iTerm2-Color-Schemes), the same
# source the manim-themes plugin uses. Files live in themes_src/.
import os
import plistlib


def _hex(c):
    return "#%02X%02X%02X" % tuple(int(round(c[k] * 255)) for k in
                                    ("Red Component", "Green Component", "Blue Component"))


def theme_from_iterm(name, font="Inter"):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "themes_src",
                        name + ".itermcolors")
    with open(path, "rb") as f:
        d = {k: _hex(v) for k, v in plistlib.load(f).items() if isinstance(v, dict)}
    bg, fg = d["Background Color"], d["Foreground Color"]
    light = sum(ManimColor(bg).to_rgb()) / 3 > 0.5
    return dict(bg=bg, ink=fg,
                soft=interpolate_color(ManimColor(fg), ManimColor(bg), 0.35).to_hex(),
                dim=(interpolate_color(ManimColor(fg), ManimColor(bg), 0.6).to_hex() if light
                     else d["Ansi 8 Color"]), a1=d["Ansi 5 Color"], a2=d["Ansi 6 Color"],
                meet=d["Ansi 3 Color"], bad=d["Ansi 1 Color"], font=font,
                head_font=font, mode="paper" if light else "dark")


PALETTES = ["Dracula", "Nord", "Catppuccin Mocha", "TokyoNight", "Gruvbox Dark",
            "Rose Pine", "Monokai Pro", "iTerm2 Solarized Light", "Catppuccin Latte"]


def _make(key):
    def construct(self):
        build_frame(self, key)
    return construct


for _n in PALETTES:
    _key = "iterm:" + _n
    THEMES[_key] = theme_from_iterm(_n)
    _cls = "Pal_" + "".join(ch for ch in _n.title() if ch.isalnum())
    globals()[_cls] = type(_cls, (Scene,), {"construct": _make(_key)})
