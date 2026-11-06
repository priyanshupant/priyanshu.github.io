# Overnight work log (6–7 Nov 2026)

Everything is pushed to GitHub (`priyanshupant/priyanshu.github.io`, folder `src/`) and checked to build.
Your taste calls were **not** applied; they are drafted at the end for you to choose.

## Done
1. **Sign section, 2×3 board** (`Dominoes2x3` + `KastFix`): rebuilt in your style. No b₁/w₁ letters — the
   matrix rows and columns are tiny 2×3 boards with the relevant square lit. Verified in code: tiling signs
   +, −, − so det = −1; one −1 edge (only the all-vertical tiling uses it) → det = −3 → 3.
2. **Consistency pass** over every scene in the video: wording ("paths", "meet / never meet"), no stray
   letter labels (only a₁…aₙ, b₁…bₙ in the general lemma, as you asked), no cue lag above 1.5 s.
3. **Chapters** (used by the build for YouTube/presenter, `chapters_v13.txt`):
   0:00 Determinants you met in school · 0:41 A simple puzzle · 1:52 An old friend: the determinant ·
   2:40 Three ants · 3:14 Why does this work? · 5:36 The general lemma (LGV) · 7:10 Does the pattern repeat? ·
   7:21 Hexagon tilings · 8:17 Boxes in a corner · 8:53 Mountain ranges (Catalan) · 10:15 The Aztec diamond ·
   12:00 The arctic circle · 12:22 When the signs go wrong (Kasteleyn, FKT) · 14:52 Why minus signs count.
   Total ≈ 16:26.
4. **Mahajan–Vinay verified** from the paper's proof text (Chicago J. Theor. Comput. Sci. 1997; ECCC TR97-036):
   they compute the determinant combinatorially with "clow sequences" and prove it with "an involution on a
   signed set… paired with another clow sequence over the same multiset of edges, but with opposing sign… a
   weight-preserving involution" — exactly our tail-swap idea. This puts the determinant in GapL with a
   division-free algorithm.

5. **Board4x4:** on-screen text cut to **det A = 0 ✗**, the rule (two lines), **|det A| = 36**; the "very confident, very wrong" joke is spoken only.

## Options for you (drafted, NOT in the video)
- **A. Mahajan–Vinay beat** (Finale, before "Determinants can count…"):
  "And this isn't only a trick for puzzles. In 1997, Meena Mahajan and V. Vinay showed how to compute the
  determinant itself the same way: every unwanted term is paired with one of opposite sign, and they cancel."
  (Nice for FSTTCS: Meena Mahajan is at IMSc Chennai.)
- **B. Early #P stake** (Opening, after "how determinants can count"): "Counting is usually brutally hard —
  but sometimes, one determinant does it."
- **C. Cost line** (after "thirteen" in the general lemma): "And a determinant is fast: about n³ steps,
  while trying every family explodes." (+ optional ω ≤ 9/4 news, verified.)
- **D. Opening quote pair** (Axler 1995 "Determinants are difficult, non-intuitive…" → Wigderson
  "The determinant is undoubtedly the most important polynomial function in mathematics.").
- **E. Chapter cards** on screen (we already have four in-video cards; adding the rest would be small).
