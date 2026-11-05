import sys, narration
SCREEN = {
 "Montage": "Four boxes: equations (solvable iff det ≠ 0), area scaling, eigenvalues, change of variables. Then: \"Determinants can count.\"",
 "ColdOpen": "4×4 grid, two ants, two houses, a near miss with \"!\", the question, a flash of [[6,4],[4,6]] and \"det\", title card.",
 "Problem": "The three rules, each shown: allowed and forbidden arrows; dashed lines to each house; the near miss. Note: crossing = sharing a dot.",
 "ListRoutes": "Ant 1 walks each route exactly as it is read aloud; big thumbnails with RRUU words; counter to 6; boxes around the words; arrows showing home is 2 right and 2 up.",
 "Slots": "4 large slots; every choice of 2 R's drawn as a route on the grid with a counter to 6; \"4 choose 2 = 6\"; a general a×b box with arrows for a and b; \"(a+b) choose a\"; the four numbers in table order 6, 4, 4, 6.",
 "OneGoodPair": "One peaceful pair walked step by step.",
 "BruteForce": "Empty 6×6 grid with ant 1's routes as row labels and ant 2's as column labels; first three pairs spotlighted with the correct verdicts; the rest in batches; tallies 20/16; \"brute force with more ants\": 36, 216, 60,466,176.",
 "TableAndDet": "2×2 table filled cell by cell; det = 6·6 − 4·4 = 20; brute force 20 beside it; \"Coincidence?\"",
 "ReadCounts": "36 own-home pairs (20 green, 16 red) and 16 swapped pairs; det = 20 good + 16 bad − 16 swapped; arrow \"equal?\" between bad and swapped; \"= 20 good\".",
 "SwapPaths": "A bad pair walks; a probe walks ant 1's route and stops at the first shared dot; tails swap; now a swapped pair.",
 "SwapTwice": "Swap again; the ring pulses (still the first meeting point); back to the bad pair; two icons with swap arrows both ways: an involution.",
 "DiagonalSweep": "One full sweep first; then the gap table filled −1 (start), +1 (end), −1, +1, and finally 0 at s=3 with the meeting dot ringed; IVT note.",
 "PutTogether": "16 bad and 16 swapped pairs, each partner in the same grid position; links and pops; det = 20 good + 16 bad − 16 swapped with the last two struck out; 20 good pairs remain.",
 "MoveHomes": "Second house moves; brute force and det agree (20, 40, 20, 14); wrong order: 0 vs −10; \"keep the order\" rule.",
 "SekiJoins": "Third ant; 3×3 table [[6,4,1],[4,6,4],[1,4,6]]; det = 50 = brute force (of 216).",
 "Lemma": "The LGV statement in words; cost n³ or n^ω; the ω ≤ 9/4 card.",
 "LGVCredits": "Name cards: Lindström (1973), Gessel and Viennot (1985); Karlin–McGregor; Fisher's \"vicious walkers\".",
 "WhatLGVCounts": "A random one-way network; its matrix and det = 42; families where nobody meets flick by and the counter lands on 42; four large thumbnails of what's coming.",
 "HexTiling": "Hexagon cut into triangles; lozenge from two triangles; sticking out / overlapping crossed out; a tiling; the shading turns flat grey and back (\"your brain renders 3D\"); several tilings.",
 "TilesToPaths": "Flat tiles fade; the two left vertical edges highlighted; two chains drawn; squash onto the grid: the ants' routes; all 20 tilings.",
 "BoxesCorner": "Cubes stack in a 3×3×3 box; three chains; three walkers on a grid; det = 980; MacMahon's formula.",
 "CatalanMountains": "Two nested mountain ranges; Catalan numbers; [[2,5],[5,14]] det = 3; all three shown.",
 "AztecIntro": "The Aztec diamond; dominoes; counts 2, 8, 64.",
 "AztecPaths": "Four domino kinds: flat, up, down, nothing; paths appear; [[12,4],[4,2]] det = 8; order 3: 64; 2^(n(n+1)/2).",
 "TreesBrief": "House graph; its 11 spanning trees appear with a counter to 11; Kirchhoff; one determinant = 11; nⁿ⁻².",
 "Dominoes8x8": "A chessboard fills with dominoes: 12,988,816.",
 "SmallBoard2": "2×3 board, 3 tilings, table of 1s, det = −1, signs +, −, −.",
 "SignFix2": "Kasteleyn name card; one edge gets a minus sign; det = −3, so 3.",
 "Board4x4": "Plain det = 0; signed det 36; six sample tilings.",
 "FKT": "8×8 with the sign pattern; |det| = 12,988,816; a 4-edge loop slides around; random tilings flicker; squares become dots and dominoes become matching edges; a planar graph with a perfect matching; FKT card; boards grow 8→128 and tilings ≈ e^(0.29·area), 0.29 = G/π.",
 "Hook": "Ants appear, then the grid; right/up arrows and crossed left/down arrows drawn on each spoken word; homes one at a time; \"They had a fight.\" with red \"!\" bubbles; two crossing routes with both crossing dots ringed; the question; a flurry of all 36 pairs (\"list every possibility\") that collapses into [[6,4],[4,6]]; montage items appear on their words; title with author.",
 "LemmaVisual": "The three-ant network and its matrix [[6,4,1],[4,6,4],[1,4,6]]; det expands into six signed pairings with values 216, −96, −96, −6, +16, +16 = 50; 216 splits into 50 never touch + 166 touch; crossed pairings all touch; 166+16+16 = 198 ⟷ 96+96+6 = 198 cancel; det = number of families that never touch; LGV name; the ants walk a peaceful family (vicious walkers); cost; ω staircase from 3 to 9/4.",
 "ArcticCircle": "A uniformly random domino tiling grows by domino shuffling from order 1 to 60; frozen corners, chaotic centre, the circle drawn; arctic circle theorem (Jockusch–Propp–Shor 1995).",
 "Finale": "All 52 signed pairs; bad and swapped pairs fly together and vanish; 20 green remain. #P-complete (Valiant 1979) vs one determinant in polynomial time. Thesis: \"Determinants can count, because minus signs can cancel.\"",
 "Map": "Seven panels around \"det\": ants 20, hexagon 20, boxes 980, mountains 3, Aztec 2^(n(n+1)/2), trees 11, dominoes 12,988,816.",
 "Goodbye": "The ants walk home and wave; \"Thanks for watching\".",
 "Credits": "Rolling credits and reading list.",
}
NAMES = {"SekiJoins": "A third ant"}
head = sys.argv[1]; scenes = sys.argv[2].split(",")
out = [f"## {head}", ""]
for sc in scenes:
    out.append(f"### {NAMES.get(sc, sc)}")
    out.append(f"**On screen:** {SCREEN[sc]}")
    out.append("")
    lines = [l if isinstance(l, str) else l[1] for l in narration.NARRATION[sc] if not isinstance(l, (int, float))]
    if lines:
        out.append("**Narration:** " + " ".join(lines))
        out.append("")
print("\n".join(out))
