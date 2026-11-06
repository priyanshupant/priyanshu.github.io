"""Shared look and logic for "How Determinants Can Count".

NOTE: this is a stand-in rebuilt from the project description, because the
original common.py was not available in this session. Names follow the
original (colours, Lattice, path_mob, endpoints, sign_badge, pair_icon,
all_paths, first_meet, swap_tails, plus_pairs, minus_pairs). Helpers marked
NEW were added for Acts 2-3 (ant, house, tick, cross, walk_steps, over_to_you,
villain_card) and should be merged into the original file, together with the
house style: palette, FONT, backdrop/DScene and glow.
"""
from manim import *
import numpy as np

# ---------------------------------------------------------------- colours
# House style: Manim's default look (black background, stock colours).
BG = BLACK
ANT1 = BLUE        # walker 1: Leibniz
ANT2 = ORANGE      # walker 2: Newton
ANT3 = PURPLE      # walker 3: Seki (Act 5)
MEET = YELLOW      # meeting points
GOOD = GREEN
BAD = RED
DIM = GREY_D
INK = WHITE
SOFT = GREY_B
FONT = "DejaVu Serif"   # pinned: identical text on every machine (it was the default here)
GLOW = False       # the "polished dark" glow; off in the default theme

config.background_color = BG

def backdrop(vignette=0.55, grain=3, seed=1):
    """Full-frame background: base colour, faint grain and a soft vignette."""
    h, w = 360, 640
    rng = np.random.default_rng(seed)
    img = np.ones((h, w, 3)) * np.array(ManimColor(BG).to_rgb()) * 255
    img += rng.normal(0, grain, (h, w, 1))
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    img *= (1 - vignette * np.clip(r - 0.3, 0, None))[..., None]
    im = ImageMobject(np.clip(img, 0, 255).astype(np.uint8))
    im.stretch_to_fit_width(config.frame_width).stretch_to_fit_height(config.frame_height)
    im.set_z_index(-100)
    return im


import os as _os
SLIDES = bool(_os.environ.get("SLIDES"))      # SLIDES=1 manim ...  -> one manim-slides slide per narration line
if SLIDES:
    from manim._config.utils import ManimConfig as _MC
    # manim-slides 5.7 was written for older Manim: shim the three config keys it touches
    if not hasattr(_MC, "write_to_movie"):
        _MC.write_to_movie = property(lambda self: True, lambda self, v: None)
    if not hasattr(_MC, "flush_cache"):
        _MC.flush_cache = property(lambda self: False, lambda self, v: None)
    _mfc = _MC.max_files_cached
    _MC.max_files_cached = property(_mfc.fget, lambda self, v: _mfc.fset(self, -1 if v == float("inf") else v))
    from manim_slides import Slide as _Base
    config.max_files_cached = 100000   # slides need every partial clip; long scenes (Hook: 140+ anims) exceed the default 100
else:
    _Base = Scene


class DScene(_Base):
    """Base scene for every act.

    Sync: audio/tts.py writes the start time of every narration line
    (audio/voice/timing.json). Call self.cue(k) right before the visual that
    goes with line k: the render waits until that line starts, so pictures never
    run ahead of the voice. If a scene is behind at a cue, the lag is logged to
    logs/cue_lags.json so it can be tightened. Scenes end no earlier than their
    narration plus a short breath.
    """

    def setup(self):
        import json
        import os
        root = os.path.dirname(os.path.abspath(__file__))
        self._starts, self._vlen, self._lines = [], 0.0, []
        f = os.path.join(root, "audio", "voice", "timing.json")
        if os.path.exists(f):
            t = json.load(open(f)).get(type(self).__name__)
            if t:
                self._starts = [ln[0] for ln in t["lines"]]
                self._lines = t["lines"]
                self._vlen = t["length"]
        self._lags = []

    def cue(self, k, lead=0.15):
        """Wait until narration line k (0-based) is about to start.
        In slides mode (SLIDES=1) each cue starts a new slide instead, with the line as speaker notes."""
        if SLIDES:
            note = self._lines[k][2] if k < len(self._lines) else ""
            self.next_slide(notes=note)
            return
        if k >= len(self._starts):
            return
        target = self._starts[k] - lead
        now = self.renderer.time
        if now < target - 1e-3:
            Scene.wait(self, target - now)
        elif now - target > 0.4:
            self._lags.append([k, round(now - target, 2)])

    def cue_at(self, k, where, lead=0.1):
        """Wait until a point inside narration line k: `where` is a fraction of the line, or a
        word/phrase from its caption (speech is close to uniform per character)."""
        if SLIDES or k >= len(self._lines):
            return
        s, e, cap = self._lines[k]
        if isinstance(where, str):
            i = cap.find(where)
            assert i >= 0, (k, where, cap)
            where = i / max(1, len(cap))
        target = s + where * (e - s) - lead
        now = self.renderer.time
        if now < target - 1e-3:
            Scene.wait(self, target - now)
        elif now - target > 0.4:
            self._lags.append([f"{k}@{where:.2f}", round(now - target, 2)])

    def cue_end(self, k, lead=0.0):
        """Wait until narration line k has finished."""
        self.cue_at(k, 1.0, lead=lead)

    def sfx(self, name):
        """Mark a sound-effect cue at the current time (audio/mix.py reads them)."""
        import os
        if os.environ.get("SFX_LOG"):
            if not hasattr(self, "_cues"):
                self._cues = []
            self._cues.append([round(self.renderer.time, 3), name])

    def play(self, *animations, **kwargs):
        for a in animations:
            if getattr(a, "sfx", None):
                self.sfx(a.sfx)
        super().play(*animations, **kwargs)

    def tear_down(self):
        import json
        import os
        rest = (0 if SLIDES else self._vlen + 0.6) - self.renderer.time
        if rest > 0.05:
            Scene.wait(self, rest)
        root = os.path.dirname(os.path.abspath(__file__))
        lagf = os.path.join(root, "logs", "cue_lags.json")
        os.makedirs(os.path.dirname(lagf), exist_ok=True)
        d = json.load(open(lagf)) if os.path.exists(lagf) else {}
        d[type(self).__name__] = self._lags
        json.dump(d, open(lagf, "w"), indent=1)
        sfx_log = os.environ.get("SFX_LOG")
        if sfx_log:
            path = os.path.join(sfx_log, type(self).__name__ + ".json")
            json.dump(getattr(self, "_cues", []), open(path, "w"))
        super().tear_down()


def glow(mob, color=None, widths=(26, 17, 11), opacities=(0.05, 0.08, 0.16)):
    """Soft glow behind a stroked mobject: wider, faint copies underneath."""
    if not GLOW:
        return mob
    color = color or mob.get_stroke_color()
    layers = VGroup(*[mob.copy().set_stroke(color, w, opacity=o).set_fill(opacity=0)
                      for w, o in zip(widths, opacities)])
    return VGroup(layers, mob)


# ---------------------------------------------------------------- running example
AUTHOR = "Priyanshu · IIT Indore"

# Two ants on a 4 x 4 grid: ant 1 (0,1) -> (2,3), ant 2 (1,0) -> (3,2).
# Path matrix [[6, 4], [4, 6]], det = 20 = non-touching pairs (of 36).
A1, A2 = (0, 1), (1, 0)
B1, B2 = (2, 3), (3, 2)
GRID = (4, 4)


MIN_TEXT = 22


def T(s, size=32, color=INK, **kw):
    """Text in the house font (never below MIN_TEXT, so it stays readable on a phone)."""
    return Text(s, font=FONT, font_size=max(size, MIN_TEXT), color=color, **kw)


# ---------------------------------------------------------------- lattice
class Lattice(VGroup):
    """An n x m grid of dots (m = n unless ny is given). lat.p(x, y) gives the
    screen point of (x, y)."""

    def __init__(self, n=4, spacing=1.2, center=ORIGIN, dot_radius=0.06,
                 color=SOFT, ny=None, **kw):
        super().__init__(**kw)
        self.n, self.ny, self.spacing = n, ny or n, spacing
        self.origin = np.array(center) - spacing * ((n - 1) / 2 * RIGHT + (self.ny - 1) / 2 * UP)
        self.dots = {}
        for x in range(n):
            for y in range(self.ny):
                d = Dot(self.p(x, y), radius=dot_radius, color=color)
                self.dots[(x, y)] = d
                self.add(d)

    def p(self, x, y):
        # Read from the (0,0) dot so the lattice still works after shift/scale.
        if hasattr(self, "dots") and len(self.dots) == self.n * self.ny:
            o = self.dots[(0, 0)].get_center()
            s = (self.dots[(1, 0)].get_center() - o)[0]
            return o + s * (x * RIGHT + y * UP)
        return self.origin + self.spacing * (x * RIGHT + y * UP)

    @property
    def step(self):
        return np.linalg.norm(self.p(1, 0) - self.p(0, 0))


def path_mob(lat, pts, color=ANT1, width=8, glowing=False):
    """Polyline through lattice points; glowing=True adds the soft halo."""
    m = VMobject(stroke_color=color, stroke_width=width,
                 joint_type=LineJointType.ROUND)
    m.set_points_as_corners([lat.p(*q) for q in pts])
    return glow(m) if glowing else m


def endpoints(lat, scale=1.0, labels=True):
    """Start dots A1, A2 and houses B1, B2 for the running example."""
    g = VGroup()
    for (pt, col, name, d) in [(A1, ANT1, "A₁", LEFT), (A2, ANT2, "A₂", DOWN)]:
        dot = Dot(lat.p(*pt), radius=0.11 * scale, color=col)
        g.add(dot)
        if labels:
            g.add(T(name, 26 * scale, col).next_to(dot, d, buff=0.42 * scale))
    for (pt, col, name, d) in [(B1, ANT1, "B₁", UP), (B2, ANT2, "B₂", RIGHT)]:
        h = house(col, 0.32 * scale).move_to(lat.p(*pt))
        g.add(h)
        if labels:
            g.add(T(name, 26 * scale, col).next_to(h, d, buff=0.12 * scale))
    return g


def sign_badge(sign=+1, radius=0.32):
    col = GOOD if sign > 0 else BAD
    c = Circle(radius=radius, color=col, fill_color=BG, fill_opacity=1,
               stroke_width=4)
    return VGroup(c, T("+1" if sign > 0 else "−1", 26 * radius / 0.32, col)
                  .move_to(c))


def pair_icon(P, Q, size=1.0, c1=ANT1, c2=ANT2, meet=True):
    """Small thumbnail of a pair of paths on the 4 x 5 grid."""
    sp = size / (max(GRID) - 1)
    lat = Lattice(GRID[0], spacing=sp, dot_radius=0.018 * size / 1.0 + 0.008,
                  color=DIM, ny=GRID[1])
    frame = RoundedRectangle(corner_radius=0.08 * size, width=sp * (GRID[0] - 1) + 0.35 * size,
                             height=sp * (GRID[1] - 1) + 0.35 * size, stroke_color=DIM,
                             stroke_width=1.5).move_to(lat)
    g = VGroup(frame, lat, path_mob(lat, P, c1, 3.2 * size + 0.8),
               path_mob(lat, Q, c2, 3.2 * size + 0.8))
    m = first_meet(P, Q)
    if meet and m is not None:
        g.add(Circle(radius=0.07 * size + 0.02, color=MEET, stroke_width=2.5)
              .move_to(lat.p(*m)))
    g.lat = lat
    return g


# ---------------------------------------------------------------- NEW: characters & marks
def ant(color=ANT1, size=0.75):
    """Side-view cartoon ant facing right (eye + smile). NEW."""
    s_ = size
    outline = interpolate_color(ManimColor(color), BLACK, 0.45)
    abdomen = Ellipse(width=0.52 * s_, height=0.4 * s_).move_to(LEFT * 0.34 * s_ + UP * 0.04 * s_)
    thorax = Ellipse(width=0.24 * s_, height=0.19 * s_)
    head = Circle(radius=0.15 * s_).move_to(RIGHT * 0.25 * s_ + UP * 0.08 * s_)
    body = VGroup(abdomen, thorax, head).set_fill(color, 1).set_stroke(outline, 2)
    legs = VGroup()
    for x, dx in [(-0.09, -0.07), (0.0, 0.0), (0.09, 0.07)]:
        legs.add(VMobject().set_points_as_corners([
            np.array([x * s_, -0.05 * s_, 0]), np.array([(x + dx) * s_, -0.17 * s_, 0]),
            np.array([(x + 1.6 * dx) * s_, -0.3 * s_, 0])]))
    antenna = VMobject().set_points_smoothly([
        head.get_center() + np.array([0.03, 0.13, 0]) * s_,
        head.get_center() + np.array([0.12, 0.3, 0]) * s_,
        head.get_center() + np.array([0.24, 0.3, 0]) * s_])
    VGroup(legs, antenna).set_stroke(interpolate_color(ManimColor(color), BLACK, 0.3), 3)
    eye = Circle(radius=0.075 * s_, fill_color=WHITE, fill_opacity=1, stroke_width=0) \
        .move_to(head.get_center() + np.array([0.05, 0.03, 0]) * s_)
    pupil = Dot(eye.get_center() + RIGHT * 0.03 * s_, radius=0.035 * s_, color="#111111")
    shine = Dot(pupil.get_center() + UL * 0.012 * s_, radius=0.01 * s_, color=WHITE)
    smile = Arc(radius=0.06 * s_, start_angle=-PI * 0.85, angle=PI * 0.5,
                stroke_width=2, color="#111111").move_to(
        head.get_center() + np.array([0.07, -0.07, 0]) * s_)
    a = VGroup(legs, antenna, body, eye, pupil, shine, smile)
    # centre on the thorax so the ant sits on lattice points and turns in place
    a.shift(-thorax.get_center())
    a.set_z_index(5)
    a.heading = 0.0
    return a


def scholar(who="leibniz", size=0.85):
    """Leibniz / Newton / Seki as little cartoon heads that walk the grid.
    Leibniz: big dark curly wig. Newton: long white wig. Seki: dark topknot.
    A collar in the walker's colour ties each to his paths."""
    s = size
    col = {"leibniz": ANT1, "newton": ANT2, "seki": ANT3}[who]
    skin = "#F2C9A0"
    face = Circle(radius=0.26 * s, fill_color=skin, fill_opacity=1, stroke_color="#8A5A3C", stroke_width=1.5)
    parts = VGroup()
    if who in ("leibniz", "newton"):
        wig_c = "#4A2E1F" if who == "leibniz" else "#E8E8E8"
        n_side = 4 if who == "leibniz" else 5
        curls = VGroup()
        for k in range(7):                                    # crown
            ang = PI * (0.08 + 0.84 * k / 6)
            curls.add(Circle(radius=0.11 * s).move_to(np.array([np.cos(ang), np.sin(ang), 0]) * 0.27 * s))
        for side in (-1, 1):                                  # long sides
            for k in range(n_side):
                curls.add(Circle(radius=0.1 * s).move_to(
                    np.array([side * 0.3 * s, (0.05 - 0.13 * k) * s, 0])))
        curls.set_fill(wig_c, 1).set_stroke(interpolate_color(ManimColor(wig_c), BLACK, 0.35), 1)
        parts.add(curls)
    else:
        hair = Circle(radius=0.27 * s).set_fill("#222222", 1).set_stroke(width=0).shift(UP * 0.05 * s)
        knot = Circle(radius=0.09 * s).set_fill("#222222", 1).set_stroke(width=0).shift(UP * 0.33 * s)
        parts.add(hair, knot)
    collar = Polygon(np.array([-0.2, -0.22, 0]) * s, np.array([0.2, -0.22, 0]) * s,
                     np.array([0, -0.42, 0]) * s).set_fill(col, 1).set_stroke(WHITE, 1)
    eyes = VGroup(*[Dot(np.array([dx, 0.03, 0]) * s, radius=0.03 * s, color="#222222") for dx in (-0.09, 0.09)])
    smile = Arc(radius=0.09 * s, start_angle=-PI * 0.8, angle=PI * 0.6, stroke_width=2,
                color="#7A3B2E").shift(DOWN * 0.03 * s)
    g = VGroup(collar, parts, face, eyes, smile)
    g.shift(-face.get_center())
    g.set_z_index(5)
    g.heading, g.no_turn, g.who = 0.0, True, who
    g.eyes, g.smile = eyes, smile
    return g


def speech(text, mob, direction=UP, color=INK, size=28):
    """A little speech bubble next to a character."""
    t = T(text, size, BLACK)
    b = RoundedRectangle(corner_radius=0.15, width=t.width + 0.3, height=t.height + 0.25,
                         fill_color=WHITE, fill_opacity=1, stroke_color=color, stroke_width=2)
    g = VGroup(b, t.move_to(b))
    return g.next_to(mob, direction, buff=0.1)


PORTRAITS = {"leibniz", "newton", "seki", "cauchy", "kirchhoff", "valiant", "cramer", "laplace", "gauss"}


def portrait(key, name, years="", line="", size=1.5, color=INK):
    """Round portrait (assets/portraits/<key>_round.png) with a caption, or a
    name card with the same layout when no usable photo exists."""
    import os
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "portraits", f"{key}_round.png")
    ring = Circle(radius=size / 2, color=color, stroke_width=3)
    if os.path.exists(f):
        img = ImageMobject(f).set_height(size * 0.97)
        pic = Group(img, ring)
    else:
        initials = "".join(w[0] for w in name.replace("&", " ").split() if w[0].isupper())[:3]
        pic = Group(ring.set_fill(GREY_E, 1), T(initials, size * 20, color).move_to(ring))
    cap = VGroup(T(name, 26, color))
    if years:
        cap.add(T(years, 22, SOFT))
    if line:
        cap.add(T(line, 20, SOFT))
    cap.arrange(DOWN, buff=0.08)
    return Group(pic, cap.next_to(pic, DOWN, buff=0.15))


def matrix_mob(rows, size=44, color=INK, h_buff=0.75, v_buff=0.6):
    """A bracketed grid of numbers built from Text (no LaTeX)."""
    cells = VGroup(*[T(str(v), size, color) for r in rows for v in r])
    cells.arrange_in_grid(len(rows), len(rows[0]), buff=(h_buff, v_buff))
    h = cells.height + 0.35
    l = VMobject(stroke_color=color, stroke_width=3).set_points_as_corners(
        [UP * h / 2 + RIGHT * 0.15, UP * h / 2, DOWN * h / 2, DOWN * h / 2 + RIGHT * 0.15])
    r = l.copy().flip(UP)
    l.next_to(cells, LEFT, buff=0.18)
    r.next_to(cells, RIGHT, buff=0.18)
    g = VGroup(l, cells, r)
    g.cells = cells
    return g


def villain_card(text="THE PERMANENT", size=48):
    """The running-gag title card: heavy red type in a glowing box. NEW."""
    t = Text(text, font=FONT, weight=HEAVY, font_size=size, color=BAD)
    box = SurroundingRectangle(t, buff=0.28, corner_radius=0.14, color=BAD,
                               stroke_width=2.5, fill_color=BAD, fill_opacity=0.12)
    halo = box.copy().set_stroke(BAD, 14, opacity=0.13).set_fill(opacity=0)
    return VGroup(halo, box, t)


def house(color=ANT1, size=0.32):
    """A little house outline. NEW."""
    s = size
    h = Polygon(LEFT * s / 2 + DOWN * s / 2, RIGHT * s / 2 + DOWN * s / 2,
                RIGHT * s / 2 + UP * s * 0.1, UP * s * 0.55, LEFT * s / 2 + UP * s * 0.1,
                color=color, stroke_width=3, fill_color=BG, fill_opacity=1)
    door = Rectangle(width=s * 0.22, height=s * 0.32, color=color,
                     stroke_width=2).align_to(h, DOWN)
    return VGroup(h, door)


def tick(size=0.3, color=GOOD, width=5):
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners([LEFT * 0.5 + UP * 0.05, LEFT * 0.15 + DOWN * 0.35,
                             RIGHT * 0.5 + UP * 0.4])
    return m.scale(size)


def cross(size=0.3, color=BAD, width=5):
    return VGroup(Line(UL * 0.4, DR * 0.4), Line(UR * 0.4, DL * 0.4)) \
        .set_stroke(color, width).scale(size / 0.6 * 1.2)


def walk_steps(lat, walkers, step_time=0.45, trace=True):
    """Walk ants along paths one lattice step at a time, all in lock-step.
    walkers = [(ant_mob, pts, color), ...]. Returns (anims, traces): anims is
    a generator, so play its items in order (each step is built after the
    previous one has played); traces fills up with the drawn segments. NEW."""
    traces = []

    def gen():
        nsteps = max(len(p) for _, p, _ in walkers) - 1
        for i in range(nsteps):
            live = [(a, pts, col) for a, pts, col in walkers if i + 1 < len(pts)]
            turns = []
            for a, pts, col in live:
                if getattr(a, "no_turn", False):
                    continue
                (x0, y0), (x1, y1) = pts[i], pts[i + 1]
                target = np.arctan2(y1 - y0, x1 - x0)
                delta = (target - a.heading + PI) % TAU - PI
                if abs(delta) > 1e-6:
                    turns.append(Rotate(a, delta, about_point=a.get_center()))
                    a.heading = target
            if turns:
                yield AnimationGroup(*turns, run_time=0.15)
            # moves are built only after the turn has played
            moves_ = []
            for a, pts, col in live:
                (x0, y0), (x1, y1) = pts[i], pts[i + 1]
                moves_.append(a.animate.move_to(lat.p(x1, y1)))
                if trace:
                    seg = glow(Line(lat.p(x0, y0), lat.p(x1, y1), stroke_color=col,
                                    stroke_width=7))
                    traces.append(seg)
                    moves_.insert(0, Create(seg))
            step = AnimationGroup(*moves_, run_time=step_time, rate_func=smooth)
            step.sfx = "step"
            yield step

    return gen(), traces


def over_to_you(prompt, width=9):
    """'Over to you' pause card. NEW."""
    head = T("OVER TO YOU", 26, MEET, weight=BOLD)
    body = T(prompt, 32, INK, line_spacing=1.1)
    if body.width > width:
        body.scale_to_fit_width(width)
    g = VGroup(head, body).arrange(DOWN, buff=0.3)
    box = SurroundingRectangle(g, buff=0.4, corner_radius=0.2, color=MEET,
                               stroke_width=2.5, fill_color=BG, fill_opacity=0.92)
    return VGroup(box, g)


# ---------------------------------------------------------------- path logic
def all_paths(a, b):
    """All right/up lattice paths from a to b, in lexicographic R<U order."""
    (x1, y1) = b
    out = []

    def rec(cur):
        x, y = cur[-1]
        if (x, y) == tuple(b):
            out.append(list(cur))
            return
        if x < x1:
            rec(cur + [(x + 1, y)])
        if y < y1:
            rec(cur + [(x, y + 1)])

    rec([tuple(a)])
    return out


def moves(P):
    return "".join("R" if q[0] > p[0] else "U" for p, q in zip(P, P[1:]))


def first_meet(P, Q):
    """First vertex of P (walking along P) that also lies on Q, else None."""
    s = set(Q)
    for v in P:
        if v in s:
            return v
    return None


def swap_tails(P, Q):
    m = first_meet(P, Q)
    if m is None:
        return P, Q
    i, j = P.index(m), Q.index(m)
    return P[:i] + Q[j:], Q[:j] + P[i:]


def plus_pairs():
    return [(P, Q) for P in all_paths(A1, B1) for Q in all_paths(A2, B2)]


def minus_pairs():
    return [(P, Q) for P in all_paths(A1, B2) for Q in all_paths(A2, B1)]


# ---- the puzzle's big board (Hook, matrix, proof): same grid everywhere, no letter labels
BIG_C = LEFT * 3.2 + DOWN * 0.2


def big_lattice():
    return Lattice(4, spacing=1.45, center=BIG_C)


def board(lat):
    """Start dots and houses in the ants' colours (symbols only, no A/B labels)."""
    return VGroup(Dot(lat.p(*A1), radius=0.12, color=ANT1), Dot(lat.p(*A2), radius=0.12, color=ANT2),
                  house(ANT1, 0.6).move_to(lat.p(*B1)), house(ANT2, 0.6).move_to(lat.p(*B2)))
