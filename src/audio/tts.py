"""Synthesize the narration with Kokoro (local, free) and write per-scene timing.

    python audio/tts.py [voice]       # default af_heart

Outputs audio/voice/<Scene>.wav and audio/voice/timing.json:
    {scene: {"length": seconds, "lines": [[start, end, caption], ...]}}
"""
import json
import os
import sys

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from narration import NARRATION  # noqa: E402

LEAD, GAP, SPEED, SR = 0.6, 0.8, 0.9, 24000     # slower: Priyanshu won't narrate faster than this


REC = os.path.join(HERE, "recorded")      # audio/recorded/<Scene>/<k>.wav + manifest.json (from studio.py)


def recorded(scene, k, text):
    """The recorded take for spoken line k of a scene, if one exists and was made for this exact text."""
    mf = os.path.join(REC, "manifest.json")
    if not os.path.exists(mf):
        return None
    m = json.load(open(mf, encoding="utf8")).get(scene, {}).get(str(k))
    f = os.path.join(REC, scene, f"{k}.wav")
    if not m or m != text or not os.path.exists(f):
        return None
    a, sr = sf.read(f, dtype="float32")
    assert sr == SR, (f, sr)
    return a if a.ndim == 1 else a.mean(axis=1)


def main(voice="af_heart", only=None):
    """only: a list of scene names to re-synthesize; the others keep their audio and timing."""
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(HERE, "models", "model_quantized.onnx"),
               os.path.join(HERE, "models", "voices.npz"))
    out = os.path.join(HERE, "voice")
    os.makedirs(out, exist_ok=True)
    tf = os.path.join(out, "timing.json")
    timing = json.load(open(tf)) if (only and os.path.exists(tf)) else {}
    for scene, lines in NARRATION.items():
        if only and scene not in only:
            continue
        parts, spans, t = [np.zeros(int(LEAD * SR), np.float32)], [], LEAD
        for ln in lines:
            if isinstance(ln, (int, float)):            # a deliberate silence
                parts.append(np.zeros(int(ln * SR), np.float32))
                t += ln
                continue
            spoken, caption = (ln, ln) if isinstance(ln, str) else ln
            a = recorded(scene, len(spans), caption)          # Priyanshu's own recording, if he made one
            gap = GAP - 0.4 if a is not None else GAP          # recorded takes carry ~0.4 s of their own silence
            if a is None:
                a, sr = k.create(spoken, voice=voice, speed=SPEED, lang="en-us")
                assert sr == SR
                a = a.astype(np.float32)
            spans.append([round(t, 3), round(t + len(a) / SR, 3), caption])
            parts += [a, np.zeros(int(gap * SR), np.float32)]
            t += len(a) / SR + gap
        audio = np.concatenate(parts)
        sf.write(os.path.join(out, f"{scene}.wav"), audio, SR)
        timing[scene] = {"length": round(len(audio) / SR, 3), "lines": spans}
        print(f"{scene:17s} {len(audio) / SR:6.1f}s  ({len(spans)} lines)")
    json.dump({k: timing[k] for k in NARRATION if k in timing}, open(tf, "w"), indent=1)
    print(f"total narration {sum(v['length'] for v in timing.values()) / 60:.1f} min")


if __name__ == "__main__":
    # python audio/tts.py                 -> every scene
    # python audio/tts.py --scene Hook    -> just these scenes (repeatable)
    args, only = sys.argv[1:], []
    while "--scene" in args:
        i = args.index("--scene")
        only.append(args[i + 1])
        del args[i:i + 2]
    main(*(args or ["af_heart"]), only=only or None)
