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
    ("act_extras.py", "QuoteOpen", 30), ("act0_opening.py", "Opening", 28),
    ("act_extras.py", "PuzzleCard", 3), ("act0_hook.py", "Hook", 45),
    # OneGoodPair and BruteForce now happen inside Hook (v10)
    ("act3_two_walkers.py", "TableAndDet", 35),
    ("act3b_more.py", "ThreeAnts", 40), ("act3b_more.py", "WhyCard", 6),
    # ListRoutes and Slots cut (v12): the puzzle already counts the paths one by one
    ("act4c_proof.py", "AllPairs", 30), ("act4c_proof.py", "SwappedToMeet", 30), ("act4c_proof.py", "MeetToSwapped", 20),
    ("act4c_proof.py", "Bijection", 20), ("act4c_proof.py", "Formula", 30),
    ("act5b_lemma.py", "LemmaCard", 6), ("act5b_lemma.py", "BookQuote", 20), ("act5b_lemma.py", "LGVNames", 15),
    ("act5b_lemma.py", "GeneralLemma", 50),
    ("act6d_pattern.py", "PatternCard", 8), ("act_extras.py", "ExCard1", 3), ("act6d_pattern.py", "Hexagon", 60),
    ("act6d_pattern.py", "Boxes", 45), ("act_extras.py", "ExCard2", 3), ("act6d_pattern.py", "Mountains", 50),
    ("act_extras.py", "ExCard3", 3), ("act6d_pattern.py", "AztecTiles", 45), ("act6d_pattern.py", "AztecPathsD", 70),
    ("act6c_arctic.py", "ArcticCircle", 30),
    ("act6d_pattern.py", "SignsCard", 6), ("act8b_signs.py", "Dominoes2x3", 50), ("act8b_signs.py", "KastFix", 30),
    ("act8_dominoes.py", "Board4x4", 20), ("act8_dominoes.py", "KastWhy", 60), ("act8_dominoes.py", "FKT", 35),
    ("act_extras.py", "EndCard", 3), ("act9_ending.py", "Map", 25), ("act9_ending.py", "Finale", 45),
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
