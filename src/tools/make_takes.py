"""Cut a narration recording into line takes without clipping words.

usage: python make_takes.py <dir> <bounds.json>
  <dir>/raw.wav       mono 48 kHz original
  bounds.json         list of approximate line START times (s); the end of the last line is the file end

Steps: DeepFilterNet (dfn.wav, made beforehand) -> gentle EQ/comp/loudnorm (clean.wav);
word spans from whisper; each boundary is moved to the middle of the longest silent gap near it;
quiet stretches OUTSIDE words are turned down (breaths); long pauses inside a line are shortened;
each take keeps 0.12 s before its first sound and 0.30 s after its last (consonants ring out).
"""
import json, os, subprocess, sys
import numpy as np, soundfile as sf

D = sys.argv[1]
starts = json.load(open(sys.argv[2]))
os.chdir(D)
if not os.path.exists('clean.wav'):
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', 'dfn.wav', '-af',
                    'highpass=f=80,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.2:g=2,'
                    'equalizer=f=10000:t=h:w=3000:g=1.5,deesser=i=0.2,'
                    'acompressor=threshold=-20dB:ratio=2:attack=15:release=200:makeup=2,'
                    'loudnorm=I=-16:TP=-1.5:LRA=8,alimiter=limit=0.89', '-ar', '48000', 'clean.wav'], check=True)
x, sr = sf.read('clean.wav')
x = x if x.ndim == 1 else x.mean(1)
H = int(0.01 * sr)                                   # 10 ms frames
db = np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + H] ** 2)) + 1e-9) for i in range(0, len(x) - H, H)])
floor = np.percentile(db, 8)
quiet = db < floor + 10                               # "silence" level
sound = db > floor + 16                               # clearly audible (incl. s/sh/t)

if not os.path.exists('words.json'):
    from faster_whisper import WhisperModel
    m = WhisperModel("small.en", device="cpu", compute_type="int8")
    a = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', 'raw.wav', '-ar', '16000', '-f', 'f32le', '-'],
                       capture_output=True).stdout
    a = np.frombuffer(a, np.float32)
    W = [(w.word.strip(), w.start, w.end) for s in m.transcribe(a, word_timestamps=True,
                                                                 condition_on_previous_text=False)[0] for w in s.words]
    json.dump(W, open('words.json', 'w'))
W = json.load(open('words.json'))

# protect every word span (a little extra after: final consonants)
inword = np.zeros(len(db), bool)
for _, s, e in W:
    inword[max(0, int((s - 0.06) * 100)):min(len(db), int((e + 0.15) * 100))] = True
inword |= sound                                     # anything clearly audible is speech, whatever whisper says


def best_cut(t, before=0.6, after=0.35):
    """Middle of the longest run of quiet frames within [t-before, t+after]."""
    a, b = max(0, int((t - before) * 100)), min(len(db), int((t + after) * 100))
    best, bl, i = None, 0, a
    while i < b:
        if quiet[i]:
            j = i
            while j < b and quiet[j]:
                j += 1
            if j - i > bl:
                best, bl = (i + j) // 2, j - i
            i = j
        else:
            i += 1
    if best is None or bl < 4:                       # no real gap: the quietest frame
        best = a + int(np.argmin(db[a:b]))
    return best / 100


if isinstance(starts[0], list):                      # explicit [start, end] per take (retakes skipped)
    pairs = [(best_cut(a_, 0.5, 0.15) if a_ > 0.3 else 0.0, best_cut(b_, 0.1, 0.7)) for a_, b_ in starts]
else:
    cuts = [0.0] + [best_cut(t) for t in starts[1:]] + [len(x) / sr]
    pairs = [(cuts[k], cuts[k + 1]) for k in range(len(starts))]
cuts = [p[0] for p in pairs] + [pairs[-1][1]]
os.makedirs('takes', exist_ok=True)
gate = np.where(inword | ~quiet, 1.0, 10 ** (-20 / 20))
gate = np.convolve(gate, np.ones(5) / 5, mode='same')
g = np.interp(np.arange(len(x)) / sr, np.arange(len(db)) / 100, gate)
y = x * g
info = []
for k in range(len(starts)):
    a, b = int(pairs[k][0] * 100), int(pairs[k][1] * 100)
    snd = np.where(sound[a:b])[0]
    lo = a + max(0, snd[0] - 12)                      # 0.12 s before the first sound
    hi = min(b, a + snd[-1] + 30)                     # 0.30 s after the last
    keep = np.ones(hi - lo, bool)                     # shorten pauses > 0.6 s inside the line to 0.35 s
    i = 0
    seg_q = quiet[lo:hi] & ~inword[lo:hi]
    while i < len(seg_q):
        if seg_q[i]:
            j = i
            while j < len(seg_q) and seg_q[j]:
                j += 1
            if j - i > 60 and i > 0 and j < len(seg_q):
                keep[i + 17:j - 18] = False
            i = j
        else:
            i += 1
    frames = [f for f in range(lo, hi) if keep[f - lo]]
    s2 = np.concatenate([y[f * H:(f + 1) * H] for f in frames])
    fd = int(0.006 * sr)
    s2[:fd] *= np.linspace(0, 1, fd)
    s2[-fd:] *= np.linspace(1, 0, fd)
    sf.write(f'takes/{k}_48.wav', s2, sr)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', f'takes/{k}_48.wav', '-ar', '24000', '-ac', '1',
                    f'takes/{k}.wav'], check=True)
    info.append((k, round(pairs[k][0], 2), round(pairs[k][1], 2), round(len(s2) / sr, 2)))
json.dump(cuts, open('cuts.json', 'w'))
for r in info:
    print(*r)
