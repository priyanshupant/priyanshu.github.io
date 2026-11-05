"""Build the soundtrack and captions, and mux the final video.

    python audio/mix.py [quality_dir]        # default 720p30

Inputs:  rendered scenes (media/videos/...), audio/voice/*.wav + timing.json
         (narration), audio/cues/<Scene>.json (sound-effect cues logged at render).
Outputs: audio/soundtrack.wav, captions.srt, and
         final_<q>.mp4            soft captions (players can toggle them)
         final_<q>_captioned.mp4  captions burned into a strip under the picture
Everything here is synthesized in code: no samples, no licences to worry about.
"""
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import pacing  # noqa: E402

SR = 48000
rng = np.random.default_rng(7)


def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", path]))


def env(n, attack, release):
    """Attack/exponential-release envelope over n samples."""
    t = np.arange(n) / SR
    e = np.minimum(1.0, t / max(attack, 1e-4)) * np.exp(-t / max(release, 1e-4))
    return e


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):          # short sounds only, so a plain loop is fine
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def tone(freq, length, attack=0.003, release=0.1, shape="sine"):
    n = int(length * SR)
    t = np.arange(n) / SR
    f = np.broadcast_to(np.asarray(freq, float), (n,)) if np.ndim(freq) else np.full(n, float(freq))
    ph = 2 * np.pi * np.cumsum(f) / SR
    w = np.sin(ph) if shape == "sine" else np.sign(np.sin(ph)) * 0.5
    return w * env(n, attack, release)


# --------------------------------------------------------------- sound effects
def make_sfx():
    S = {}
    noise = rng.normal(0, 1, int(0.05 * SR))
    S["step"] = [lowpass(noise * env(len(noise), 0.001, 0.012), c) * 0.5 for c in (1800, 2400)]
    S["tick"] = [tone(1400, 0.08, release=0.025) * 0.5]
    S["buzz"] = [lowpass(tone(150, 0.16, release=0.08, shape="square"), 900) * 0.6]
    S["chime"] = [(tone(880, 1.4, release=0.5) + 0.5 * tone(1320, 1.4, release=0.35)
                   + 0.25 * tone(1760, 1.4, release=0.25)) * 0.35]
    blip = lambda f: tone(f, 0.09, release=0.04)
    a = np.concatenate([blip(1000), np.zeros(int(0.04 * SR)), blip(1300)])
    S["alert"] = [a * 0.45]
    sweep = np.linspace(500, 1300, int(0.09 * SR))
    S["flip"] = [np.concatenate([tone(sweep, 0.09, release=0.08) * 0.4, tone(1300, 0.25, release=0.08) * 0.3])]
    S["pop"] = [tone(np.linspace(700, 180, int(0.08 * SR)), 0.08, release=0.03) * 0.55]
    wn = rng.normal(0, 1, int(0.7 * SR))
    sw = np.sin(np.linspace(0, np.pi, len(wn))) ** 2
    S["whoosh"] = [lowpass(wn * sw, 1200) * 0.35]
    n = int(1.8 * SR)
    t = np.arange(n) / SR
    rum = (np.sin(2 * np.pi * 46 * t) + 0.6 * np.sin(2 * np.pi * 69 * t)) * np.sin(np.linspace(0, np.pi, n)) ** 1.5
    rum += lowpass(rng.normal(0, 1, n), 200) * 0.8 * np.sin(np.linspace(0, np.pi, n))
    S["rumble"] = [rum * 0.5]
    # cha-cha: a wooden clave (two sine partials, fast decay) and a shaker (filtered noise burst)
    S["clave"] = [(tone(2500, 0.12, attack=0.001, release=0.03) + 0.4 * tone(5000, 0.12, attack=0.001, release=0.02)) * 0.5]
    sh = rng.normal(0, 1, int(0.12 * SR))
    S["shaker"] = [(sh - lowpass(sh, 4000)) * env(len(sh), 0.01, 0.05) * 0.6]
    return S


GAIN = {"step": 0.25, "tick": 0.35, "buzz": 0.35, "chime": 0.45, "alert": 0.45,
        "flip": 0.5, "pop": 0.4, "whoosh": 0.5, "rumble": 0.8, "clave": 0.5, "shaker": 0.35}


# --------------------------------------------------------------- music bed
def make_music(length):
    """Calm A-minor pad (Am F C G), 8 s per chord, with a soft plucked arpeggio."""
    n = int(length * SR)
    out = np.zeros(n)
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]   # MIDI notes
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    bar = 8.0
    t_all = np.arange(int(bar * SR)) / SR
    shape = np.minimum(1, t_all / 2.0) * np.minimum(1, (bar - t_all) / 2.0)   # slow swell per chord
    k = 0
    while k * bar < length:
        ch = chords[k % 4]
        seg = np.zeros(len(t_all))
        for m in ch + [ch[0] - 12]:
            for det in (-0.12, 0.12):                     # gentle chorus
                seg += np.sin(2 * np.pi * hz(m + det) * t_all) / 8
        seg *= shape
        # arpeggio: one soft pluck every second
        for j in range(8):
            m = ch[j % 3] + 12
            p = tone(hz(m), 1.2, attack=0.005, release=0.35) * 0.12
            s0 = int(j * SR)
            seg[s0:s0 + len(p)] += p[:max(0, len(seg) - s0)]
        a, b = int(k * bar * SR), min(n, int((k + 1) * bar * SR))
        out[a:b] += seg[:b - a]
        k += 1
    fade = int(3 * SR)
    out[:fade] *= np.linspace(0, 1, fade)
    out[-fade:] *= np.linspace(1, 0, fade)
    return out / (np.max(np.abs(out)) + 1e-9)


def place(track, clip, t, gain=1.0):
    s = int(t * SR)
    if s >= len(track):
        return
    e = min(len(track), s + len(clip))
    track[s:e] += clip[:e - s] * gain


# --------------------------------------------------------------- captions
def srt_time(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"


def chunks(text, start, end, max_chars=84, line=44):
    """Split a sentence into caption chunks (at most two lines), timed by length."""
    words, out, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > max_chars and cur:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    out.append(cur)
    total = sum(len(c) for c in out)
    t, res = start, []
    for c in out:
        d = (end - start) * len(c) / total
        # wrap to two lines near the middle
        if len(c) > line:
            ws, best = c.split(), None
            for i in range(1, len(ws)):
                a, b = " ".join(ws[:i]), " ".join(ws[i:])
                score = max(len(a), len(b))
                if best is None or score < best[0]:
                    best = (score, a + "\n" + b)
            c = best[1]
        res.append((t, t + d, c))
        t += d
    return res


def main(q="720p30"):
    voice = json.load(open(os.path.join(HERE, "voice", "timing.json")))
    offsets, t = {}, 0.0
    vids = []
    for f, sc, _ in pacing.SCENES:
        v = os.path.join(ROOT, "media", "videos", f[:-3], q, sc + ".mp4")
        offsets[sc] = t
        vids.append(v)
        t += dur(v)
    total = t
    n = int((total + 1) * SR)

    # narration
    vo = np.zeros(n)
    for sc, off in offsets.items():
        a, sr = sf.read(os.path.join(HERE, "voice", sc + ".wav"))
        if sr != SR:
            idx = np.arange(0, len(a), sr / SR)
            a = np.interp(idx, np.arange(len(a)), a)
        place(vo, a, off)
    vo /= np.max(np.abs(vo)) + 1e-9

    # sound effects
    fx = np.zeros(n)
    S = make_sfx()
    k = 0
    for sc, off in offsets.items():
        p = os.path.join(HERE, "cues", sc + ".json")
        if not os.path.exists(p):
            continue
        for ct, name in json.load(open(p)):
            variants = S[name]
            place(fx, variants[k % len(variants)], off + ct, GAIN[name])
            k += 1

    # music, ducked under the voice
    mus = make_music(total + 1)[:n]
    win = int(0.25 * SR)
    level = np.sqrt(np.convolve(vo ** 2, np.ones(win) / win, mode="same"))
    duck = 1 - 0.65 * np.clip(level / 0.08, 0, 1)
    duck = np.convolve(duck, np.ones(int(0.4 * SR)) / int(0.4 * SR), mode="same")
    no_music = bool(os.environ.get("NO_MUSIC"))
    mix = vo * 0.9 + fx * 0.8 + (0 if no_music else 1) * mus * 0.16 * duck
    mix /= np.max(np.abs(mix)) + 1e-9
    stereo = np.stack([mix, mix], axis=1) * 0.9
    wav = os.path.join(HERE, "soundtrack_nomusic.wav" if no_music else "soundtrack.wav")
    sf.write(wav, stereo, SR)
    if no_music:
        # voice + sound effects only, no subtitles: the source for the per-slide clips
        lst = os.path.join(ROOT, "media", "concat.txt")
        with open(lst, "w") as fh:
            fh.writelines(f"file '{v}'\n" for v in vids)
        silent = os.path.join(ROOT, "media", f"silent_{q}.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent],
                       check=True)
        out = os.path.join(ROOT, f"final_{q}_nomusic.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "160k",
                        "-t", f"{total:.3f}", out], check=True)
        json.dump(offsets, open(os.path.join(ROOT, "media", f"offsets_{q}.json"), "w"))
        print("wrote", out)
        return

    # captions
    entries = []
    for sc, off in offsets.items():
        for s, e, cap in voice[sc]["lines"]:
            entries += chunks(cap, off + s, off + e)
    srt = os.path.join(ROOT, "captions.srt")
    with open(srt, "w") as fh:
        for i, (s, e, c) in enumerate(entries, 1):
            fh.write(f"{i}\n{srt_time(s)} --> {srt_time(e)}\n{c}\n\n")

    # video: join scenes, then mux
    lst = os.path.join(ROOT, "media", "concat.txt")
    with open(lst, "w") as fh:
        fh.writelines(f"file '{v}'\n" for v in vids)
    silent = os.path.join(ROOT, "media", f"silent_{q}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent],
                   check=True)
    soft = os.path.join(ROOT, f"final_{q}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", wav, "-i", srt,
                    "-map", "0:v", "-map", "1:a", "-map", "2:s", "-c:v", "copy",
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-c:s", "mov_text", "-metadata:s:s:0", "language=eng", "-t", f"{total:.3f}", soft], check=True)
    # burned-in: picture scaled to 90% at the top, captions in the black strip below
    W, H = map(int, subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                             "stream=width,height", "-of", "csv=p=0", silent]).decode().split(","))
    w2, h2 = int(W * 0.9) // 2 * 2, int(H * 0.9) // 2 * 2
    # libass sizes are in units of a 288-line canvas, whatever the video height:
    # FontSize 10.5 -> ~26 px lines at 720p, so two lines fit the 10% strip.
    style = ("FontName=DejaVu Sans,FontSize=10.5,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
             "BorderStyle=1,Outline=0.6,Shadow=0,Alignment=2,MarginV=3")
    burned = os.path.join(ROOT, f"final_{q}_captioned.mp4")
    vf = (f"scale={w2}:{h2},pad={W}:{H}:{(W - w2) // 2}:0:black,"
          f"subtitles={srt}:original_size={W}x{H}:force_style='{style}'")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-vf", vf, "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", burned],
                   check=True)
    print(f"total {int(total // 60)}:{int(total % 60):02d}  captions {len(entries)}")
    print("wrote", soft)
    print("wrote", burned)


if __name__ == "__main__":
    main(*sys.argv[1:])
