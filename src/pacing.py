"""Scene order, target lengths (seconds) and the pacing tool.

    python pacing.py measure   # dry-run every scene, log natural timings
    python pacing.py scales    # compute wait-stretch factors -> pacing_scales.json
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MANIM = os.environ.get("MANIM", "manim")

# (file, scene, target seconds) in video order; acts follow the script's clock.
SCENES = [
    ("act0_opening.py", "Opening", 28), ("act0_hook.py", "Hook", 45),
    ("act3_two_walkers.py", "OneGoodPair", 15), ("act3_two_walkers.py", "BruteForce", 30),
    ("act3_two_walkers.py", "TableAndDet", 35),
    ("act2_one_walker.py", "ListRoutes", 25), ("act2_one_walker.py", "Slots", 25),
    ("act4_proof.py", "ReadCounts", 30), ("act4_proof.py", "SwapPaths", 25), ("act4_proof.py", "SwapTwice", 25),
    ("act4_proof.py", "DiagonalSweep", 30), ("act4_proof.py", "PutTogether", 25),
    ("act5_lgv.py", "MoveHomes", 25), ("act5_lgv.py", "SekiJoins", 20), ("act5_lgv.py", "LemmaVisual", 60),
    ("act5_lgv.py", "WhatLGVCounts", 35),
    ("act6_hexagon.py", "HexTiling", 45), ("act6_hexagon.py", "TilesToPaths", 50),
    ("act6b_disguises.py", "BoxesCorner", 35), ("act6b_disguises.py", "CatalanMountains", 30),
    ("act6b_disguises.py", "AztecIntro", 30), ("act6b_disguises.py", "AztecPaths", 45),
    ("act6c_arctic.py", "ArcticCircle", 30),
    ("act8_dominoes.py", "SmallBoard2", 35), ("act8_dominoes.py", "SignFix2", 25),
    ("act8_dominoes.py", "Board4x4", 20), ("act8_dominoes.py", "FKT", 35),
    ("act9_ending.py", "Map", 25), ("act9_ending.py", "Finale", 45),
    ("act9_ending.py", "Goodbye", 15), ("act9_ending.py", "Credits", 25),
]

if __name__ == "__main__":
    log = os.path.join(HERE, "pacing_log.json")
    if sys.argv[1] == "measure":
        if os.path.exists(log):
            os.remove(log)
        for f, sc, _ in SCENES:
            r = subprocess.run([MANIM, "--dry_run", "--disable_caching", f, sc], cwd=HERE,
                               env={**os.environ, "PACING_LOG": log}, capture_output=True, text=True)
            print(("ok  " if r.returncode == 0 else "ERR ") + sc)
            if r.returncode:
                print(r.stdout[-2000:], r.stderr[-2000:])
    elif sys.argv[1] == "voice":
        # Re-time every scene to its narration (audio/voice/timing.json). Real animation
        # time comes from the last render: play = file length - stretched waits - pad.
        q = sys.argv[2] if len(sys.argv) > 2 else "720p30"
        d = json.load(open(log))
        voice = json.load(open(os.path.join(HERE, "audio", "voice", "timing.json")))
        out, total = {}, 0
        for f, sc, _ in SCENES:
            play, wait = d[sc]                      # dry-run measurement (waits excluded from play)
            target = voice[sc]["length"] + 1.2          # narration + a short breath
            scale = 1.0 if wait < 1e-6 else max(0.4, min(6.0, (target - play) / wait))
            pad = max(0.0, target - play - wait * scale)
            out[sc] = [round(scale, 3), round(pad, 2)]
            length = play + wait * scale + pad
            total += length
            print(f"{sc:17s} voice {voice[sc]['length']:5.1f}s  anim {play:5.1f}s  -> scene {length:5.1f}s  (wait x{scale:.2f}, pad {pad:.1f})")
        json.dump(out, open(os.path.join(HERE, "pacing_scales.json"), "w"), indent=1)
        print(f"total {total / 60:.1f} min")
    else:
        d = json.load(open(log))
        out, total = {}, 0
        for f, sc, target in SCENES:
            play, wait = d[sc]
            natural = play + wait
            scale = 1.0 if wait < 1e-6 else max(1.0, min(4.0, (target - play) / wait))
            pad = max(0.0, target - play - wait * scale)
            out[sc] = [round(scale, 3), round(pad, 2)]
            total += play + wait * scale + pad
            print(f"{sc:18s} natural {natural:6.1f}s  target {target:4d}s  wait x{scale:4.2f}  pad {pad:5.1f}s")
        json.dump(out, open(os.path.join(HERE, "pacing_scales.json"), "w"), indent=1)
        print(f"total {total / 60:.1f} min")
