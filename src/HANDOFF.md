# HANDOFF: "How Determinants Can Count"

**Shared working file for every assistant (Claude, ChatGPT, others) and for Priyanshu.**
Read it fully before doing anything. After you change something, update §6 *Current state*
and add a line to §10 *Change log*. Keep it truthful: say what was verified and what was not.

---

## 1. The project in one paragraph

- **What:** an expository video, *How Determinants Can Count*, by **Priyanshu** (research scholar, IIT Indore).
- **Competition:** **DepthTCS 2026** video competition, co-located with FSTTCS 2026. Limit 20 minutes; deadline **extended to 12 Nov 2026, Anywhere on Earth** (was 5 Nov). Rules (https://vaishs.github.io/DepthTCS/index.html#videos): creators must be students/postdocs; no AI video generators; **narration must be by one of the creators**; SoME AI policy applies (https://some.3b1b.co/ai-policy): AI may help with coding animations, editing, research, grammar; NOT script/narration/storytelling, core explanations, AI voices, or significant visual assets.
- **Audience:** theoretical computer scientists and mathematicians.
- **Animation:** Manim Community, default Manim look.
- **Voice:** currently a placeholder AI voice (Kokoro). Priyanshu may replace it with his own.

## 2. Published links (live, public)

| What | Link |
|---|---|
| Article (whole video, slide by slide, with captions) | https://priyanshupant.github.io/priyanshu.github.io/determinants/ |
| Presenter view (one voiced clip per narration line, cut from the film without music; caption below; → next; M mute) | https://priyanshupant.github.io/priyanshu.github.io/determinants/present.html |
| Plain slide deck (reveal.js; S = speaker notes) | https://priyanshupant.github.io/priyanshu.github.io/determinants/slides.html |
| Video (captioned) | https://priyanshupant.github.io/priyanshu.github.io/determinants/video.mp4 |

- These come from the GitHub repo `priyanshupant/priyanshu.github.io` (branch `main`, folder `determinants/`).
- Pages rebuilds on every push and goes live in about a minute.
- **Never** publish to `priyanshupant/priyanshupant.github.io` (his main site) or `priyanshupant/continuum` (private research; its own rules forbid publishing).

## 2a. Where the source lives, and how anyone (ChatGPT included) changes something

- **Source:** the folder `src/` of the public repo `priyanshupant/priyanshu.github.io` (branch `main`).
  The published site is `determinants/` in the same repo; it is **generated**, so never edit it by hand.
- **Automatic rebuild:** every push that touches `src/**` starts the GitHub Action
  `.github/workflows/build-determinants.yml`. On GitHub's servers it:
  1. downloads the voice model;
  2. re-records the whole AI voice (`audio/tts.py`);
  3. renders every scene;
  4. mixes the audio;
  5. renders the manim-slides deck;
  6. cuts the presenter clips;
  7. rebuilds the article;
  8. commits the new `determinants/` folder back to `main`.

  A rebuild takes roughly 1 to 1.5 hours. Progress shows under the repo's **Actions** tab, and a failed run uploads its logs as `build-logs`.
- **To change something (any assistant, or Priyanshu in the GitHub web editor):**
  1. **Words:** edit `src/narration.json`. A line is either a string, or a [spoken, caption] pair when the spelling differs from the speech (e.g. "sharp-P" / "#P"). A number is a pause in seconds.
     - The number of spoken lines in a scene must equal the number of `self.cue(k)` calls in that scene.
     - `cue_at(k, "word")` searches the caption text.
  2. **Animation:** edit the scene's `src/act*.py` file. Use `Text()` only (no LaTeX), Manim 0.22.1 API.
  3. **Commit and push to `main`**, then wait for the Action to finish. Audio, video, clips, deck and article all update together.
- **Manual run:** Actions tab → "build determinants" → *Run workflow*.
- **Local build** (needs ffmpeg, cairo, pango and `pip install -r src/requirements.txt`):
  ```bash
  bash src/scripts/build_site.sh
  ```
  It writes into `determinants/` (`SITE` defaults to the repo root).
- **Never** commit generated files (`media/`, `audio/voice/`, `*.mp4`, … are in `src/.gitignore`) or any API key.

## 3. The story (v8 opening; later acts retained from v7)

Each act answers the question the viewer is asking at that point.

| Act | Viewer's question | Content |
|---|---|---|
| 0 Opening | What else can a determinant do? | Familiar a d − b c formula; full-size animated examples of two equations becoming parallel, a square becoming a parallelogram, and the grid collapsing to a line; a short turn to counting; then two ants. No child joke, Valiant, or application/count montage. |
| 1 Puzzle | How many ways home without touching? | Two ants on a 4×4 grid, steps right/up. **Scent trail rule**: neither steps on any dot the other walks on, *not even later*, so we count vertex-disjoint paths. Pause and try. One good pair. Brute force: 36 pairs, 20 good. Table [[6,4],[4,6]], det = 20. "Coincidence? Hardly." Title. |
| 2 Numbers | Where do 6 and 4 come from? | Ant one's 6 routes; (a+b choose a). |
| 3 Formula | What do 6·6 and 4·4 count? | det = good + bad − swapped, so we need bad = swapped. |
| 4 Proof | Why is bad = swapped? | Tail swap at the first meeting point; swapping twice gives the original (involution); diagonal sweep shows every swapped pair must meet (discrete intermediate value theorem). Bijective proof. |
| 5 General | A fluke of the grid? | Moving the houses ("keep the order"); a third ant: 3×3 det = 50. LGV lemma on real numbers: 216 − 96 − 96 − 6 + 16 + 16 = 50; touching families cancel 198 against 198. Random network, det = 42. Cost n³ (ω staircase, ω ≤ 9/4 claim). |
| 6 Disguises | What else is secretly paths? | Hexagon lozenge tilings → our ants (20). Boxes in a corner 3×3×3: 980. Catalan mountains [[2,5],[5,14]]: 3. Aztec diamond 2, 8, 64, 1024; dominoes → paths, det 8. **Arctic circle** (random order-60 tiling via domino shuffling). |
| 7 Breaks | Does it always work? | 2×3 board: plain det −1. Kasteleyn's sign fix: −3, so 3. 4×4: 0, then 36. Chessboard 12,988,816. FKT for planar graphs. |
| 8 Why | So what? | Map; cancellation motif. Counting is #P-complete in general (Valiant 1979), but these reduce to one determinant in polynomial time. Thesis: "Determinants can count, because minus signs can cancel." Ants walk home. |

**Verified in code:** every number above (bijections for the Aztec diamond, Catalan, boxes and hexagon included). **Not verified by an assistant, so Priyanshu must check before citing:** the historical dates. (The ω ≤ 9/4 line WAS verified on 5 Nov by Claude: OpenAI's openai/math family 107 proves ω(ℂ) ≤ 9/4 with a Lean formalization; Shpilka's exposition is ECCC TR26-281, 27 Oct 2026. The bound is over ℂ; the all-fields bound is weaker. Narration now says "last month"; label "ω(ℂ) ≤ 9/4 (Oct 2026)".)

## 4. Priyanshu's preferences (learned; respect them)

- **Likes:** the ants and the original 4×4 grid; rigour; jokes for theory and maths audiences; the default Manim theme; detailed, clean explanations; "think like a TCS researcher watching"; working line by line; storyboards with pictures.
- **Rejected; do not bring back:**
  - a history-first opening, or a long montage first;
  - the permanent/VP-vs-VNP ending;
  - "over to you" segments;
  - Pascal's triangle;
  - Leibniz and Newton as characters;
  - the area intro as the main idea;
  - spanning trees as a main section (cut in v6);
  - the matroid claim (not his area).
- **Opening order he wants:** the determinant you've seen → counting → puzzle → the determinant surprise → explanation.
- **Tools:** he does **not** want Gemini used. He wants manim-slides, a presenter view with captions, VS Code, and the ability to switch between Claude and ChatGPT.

## 5. Lessons from reviews and references

- **Our own frame-by-frame reviews:** narration and picture must match word by word (`cue_at`); no static stretches over 5 s; text no smaller than 22 pt; pause after big reveals.
- **3Blue1Brown, "What makes a great math explanation":** the criteria are motivation, clarity, novelty and memorability. Don't over-philosophise the intro. Build intuition before formulas. Start with a naive solution, then refine it. Keep music quiet during technical parts.
- **Reference SoME4 video, "The Hidden Law of Crossing Paths" (Sohil Rathi):** the same lemma, with a similar rivals hook (generals at war).
  - **Ideas to borrow (proposed, NOT yet in the video):**
    - A. a tighter, second-person opening;
    - B. say "count everything, subtract the bad" before the table;
    - C. act title cards;
    - D. shaded **lanes** to show the same-order condition;
    - E. "straighten the paths" intuition before the diagonal sweep.
  - **Avoid** war framing. Our edge: a real proof, the computer-science payoff, the disguises, Kasteleyn and FKT.
  - Their mistake to avoid: "if the determinant is zero or negative, there are no paths" (the lane condition decides, not the sign).

## 6. Current state (update this when you change things)

- **11 Nov:** TheTrick (D.I.E. scene) removed from pacing (code kept in act4c_proof.py); ThreeProof now leads straight into LemmaCard. Benjamin–Quinn credit removed; Benjamin–Cameron (ants, 2005) kept. Naming still "wrong houses" (alternatives offered: meet-ups / mix-ups).

- **TheTrick (new, after ThreeProof):** "How a determinant counts": perm A = 6·6 + 4·4 = 52 (every pair, meeting or not) vs det A = 6·6 − 4·4 = 20 (only never meet; the minus boxed) → Benjamin & Quinn's D.I.E. method ("D.I.E., which stands for Description, Involution, Exception", verified in their PDF): Description = families of paths; Involution = swap the tails at the first meeting; Exception = the families that never meet. Sources verified this session: Benjamin & Cameron, "Counting on Determinants", Amer. Math. Monthly 112 (2005) 481–492, opens with "THE PROBLEM OF THE DETERMINED ANTS" (ants, permanent = all, determinant = non-intersecting; "for every intersecting n-path, we can uniquely identify another intersecting n-path with opposite sign") — our ant picture follows the same idea, so it is credited. Both added to CREDITS.

- **ThreeProof (new, act4c_proof.py, after Formula; Priyanshu asked how the 3×3 case works):** 5×5 grid, 3 ants (S3/E3, A = [[6,4,1],[4,6,4],[1,4,6]]); the six terms as rows, each with a little ant→house diagram, sign, product and count (216, 96, 96, 6, 16, 16), det A = 50; a meeting family: first meeting, swap the two tails → it moves to a term of opposite sign; swap again → back; then all 198 cancelling pairs run (counters fall to 50, 0, 0, 0, 0, 0); what's left: never-meeting families, all going home, 50 = det A. Rule (verified at import): lowest ant that meets anyone, its first shared dot, lowest other ant there; it is an involution and flips the sign.

- **Proof intro v14 (8 Nov, act4c_proof.py AllPairs; old act4c_proof_v13.py.bak):** WhyCard says only "Why does this work?"; AllPairs then: "Let's get back to our two ants" (grid, ants, houses + matrix A with house/ant labels) → det A = 6·6 − 4·4 (LaTeX) → why 6·6: six blue ways, six orange ways drawn on the grid; any with any → the 36 pairs (grid fades, thumbnails) → 20 never meet / 16 meet → why 4·4: the 16 pairs where the ants end up in the **wrong houses** (new name for "swapped") → "= all − wrong houses", "never meet = all − meet", "meet = 16 = wrong houses" (= aligned) → "But why is that?" → the grid comes back for SwappedToMeet. "Swapped" renamed to "wrong houses" in narration and bullets of SwappedToMeet, Bijection, Formula.

- **More ants v13c (8 Nov, Priyanshu chose layout "U" from two drawn sheets, ant_layouts.png / ant_layouts2.png):** grid grows to 7×7 with the old 4×4 as its middle (shifted by (1,1)); purple and pink ants + homes appear in a neat staircase (G4S/G4E); "Now move the ants and their homes anywhere you like": all four ants slide to S4 = blue (3,3), orange (1,1), purple (2,4), pink (1,3), then the homes to E4 = (6,5), (6,3), (5,6), (3,6) (each ant ≥ 5 steps from home; paths free to cross). A = [[10,1,10,1],[126,21,126,21],[5,0,10,3],[21,1,35,10]], det A = 252 = number of never-meeting ways (verified at import, other pairings impossible).

- **More ants v13b (8 Nov): all four ants and homes scattered — blue (3,2)→(5,5), orange (3,0)→(5,2), purple (0,1)→(1,4), pink (0,5)→(3,5); A = [[10,1,0,1],[21,6,0,1],[126,6,4,35],[1,0,0,1]], det A = 136 = the number of ways the ants get home without ever meeting (shown as two aligned lines); then "Isn't this so simple, and beautiful? … in understanding why this works lies the essence of how determinants can be used in counting problems. So, let's get into that." → WhyCard "Why does this work?". Verified exhaustively as before.**
- **More ants v13 (8 Nov, act3b_more.py ThreeAnts; old version act3b_more_v12.py.bak):** "nothing special about this scenario" → the 4×4 grid grows to 6×6 (dots slide) → two more ants (purple at (0,3), pink at (3,0)) → "Put their homes anywhere you like": homes at (1,2) blue, (3,3) orange, (3,5) purple, (5,3) pink → 4×4 matrix A = [[2,10,35,21],[1,10,21,35],[0,1,10,1],[0,1,1,10]] (rows/columns blue, orange, purple, pink; each entry flashes its ant and house) → det A = 486 → a sample of never-meeting families flashes by, "never meet: 486 ✓". Verified at import: exactly 486 families never meet, and every other pairing of ants to homes has none (so the determinant counts exactly these).

- **Puzzle + matrix pass (8 Nov):** Hook rules split into five slow lines (step up ✓, step right ✓, never left ✗, never down ✗); "many paths" shows zig-zag paths one at a time (each replaces the last); the easy and crossing pairs have their own lists (EASY, CROSS); question now "So here's the question: in how many ways can both ants get home, without ever meeting?" (screen: "In how many ways can / both ants get home / without ever meeting?"); the 36-pair check has one narration line per named pair (no lag). TableAndDet: after "four, and six", a counting aside under the matrix: four slots filled with →/↑ for a path, a second order, the two → boxed, C(4,2) = 6; to the orange house →→→↑, C(4,1) = 4 (LaTeX binomials). All cue lags now 0.

- **Opening v12 (8 Nov):** formulas in real LaTeX (MathTex; texlive + dvisvgm now installed here and added to the GitHub workflow apt line); 3×3 terms 3× faster; general forms without captions and without the pivots form (row expansion, permutations, eigenvalues; = signs aligned); scaling beat purely visual (no 1/2, no det = 2, line ends at "scales space"); polygon: triangles numbered 1–5 and "Area = ½ Σ det M_{T_i}, M_{T_i} = [[x_i, x_{i+1}], [y_i, y_{i+1}]]"; combinatorics beat with no text: the 6 paths across a small grid, a 2×4 board cycling its 5 domino tilings, a hexagon cycling lozenge tilings.
- **Opening v11 (8 Nov, Priyanshu's script):** "Most of us have seen the determinant in school" → 2×2 a d − b c → 3×3 with the six products built term by term (+ aei + bfg + cdh − ceg − bdi − afh, cells boxed green/red) → general forms (row expansion, signed sum over permutations, ± product of pivots, product of eigenvalues) → "all over mathematics" → unique solution (lines turn parallel) → scaling (area doubles) → polygon area → "combinatorics: the mathematics of counting" (the 6 paths across a small grid, counted) → title "How Determinants Can Count" → "Let's start with a simple puzzle." The squashed-flat beat and option B's stake line are gone; QuoteOpen (option D) removed from pacing. 1:09. Old version: act0_opening_v10.py.bak.

- **Own voice (8 Nov):** studio.py can record Priyanshu's voice per narration line (🎙 record / ▶ play / ⤒ upload a file / ✕ back to AI). Takes go to audio/recorded/<Scene>/<k>.wav (24 kHz mono, silence trimmed, loudness levelled) with audio/recorded/manifest.json storing the text each take was made for. audio/tts.py uses a take instead of Kokoro whenever the line's text still matches; if the text changes, the take is "stale" and the AI voice is used until he re-records. Commit audio/recorded/ so the GitHub build uses the takes too.

- **v14 "everything added, for review" (8 Nov, Priyanshu: "add em all … then I will tell what to remove"; slow, detailed).** Each addition is removable:
  - D: new scene **QuoteOpen** (act_extras.py) before Opening: Axler 1995 "Down with Determinants!" + quote, then Wigderson's quote, "So which is it? Let's take a look." (remove = delete its pacing line).
  - B: Opening line 7 "Counting is usually brutally hard. But sometimes, one determinant does it." with two small lines under the title (remove = drop that narration line and the cue-7 block in act0_opening.py; renumber cue 8 → 7).
  - E: chapter cards (act_extras.py, silent): PuzzleCard before Hook, ExCard1 (hexagon + boxes), ExCard2 (mountains), ExCard3 (Aztec), EndCard ("Why minus signs count") before Map. Chapters in assemble.py updated.
  - C: GeneralLemma cue 5 "And a determinant is fast: about n cubed steps…" with two lines under "here: det M = 13".
  - 1: SignsCard bridge: "With the ants, the bad terms cancelled on their own… With dominoes… fix the signs ourselves" ((20 + 16) − 16 with the 16s struck; dominoes: ?).
  - Signs section rebuilt slow and detailed: Dominoes2x3 (13 lines) names the three tilings, builds the matrix, goes through ALL SIX terms of the 3×3 determinant (three hit a zero, three are the tilings), det should be 3 but is −1, signs by number of swaps (2 → +, 1 → −); KastFix (7 lines) board as a graph, one −1 edge, only the all-standing tiling's term changes (1·1·(−1)), det −3, |det| 3. Board4x4 (5 lines): 36 tilings shown, plain det 0 because 18 are + and 18 are − (sorted on screen), Kasteleyn signs → all 36 same sign → 36 (all verified at import). FKT (8 lines): number, five months, why every other column (each little loop has exactly one minus), Kasteleyn's rule, perfect matchings, FKT for planar graphs, F: Vazirani 1989 (no K₃,₃) and Valiant's holographic algorithms (2004), board → infinity.
  - A: Finale cue 4: Mahajan & Vinay 1997 (write as signed sum, pair unwanted terms, cancel, no division); thesis is now cue 5.
  - G: credits "Written and produced by" + "Voice: placeholder AI voice (Kokoro)"; added Axler/Wigderson, Vazirani/Valiant, Mahajan & Vinay.
  - Length grows to about 20½ min (limit 20): Priyanshu will choose what to remove.
  - **KastWhy** (new, act8_dominoes.py, between Board4x4 and FKT; Priyanshu asked for the missing "why"): every little square has one minus sign → Kasteleyn's rule → lay two 4×4 tilings on top of each other (all flat vs T44[13]) → where they differ: two closed loops (4 and 8 squares) → switching = turning each loop → small loop: 1 swap + 1 minus edge = 2 flips, no change; big loop: 3 swaps + 1 minus edge = 4 flips, no change → Kasteleyn: every loop flips an even number of times → all tilings same sign, |det| counts them. Verified at import (and for all 630 pairs of 4×4 tilings during development). The rule beats moved out of FKT (FKT is now 6 lines).

- **Puzzle fixes applied (5 Nov):** Hook line 2 now "Each ant is heading home. Ant one, the blue one, lives up here. Ant two, the orange one, lives over there."; ant labels moved off the arrows; the question reads "…without touching?" and a rules box ("→ or ↑ only · no shared dot") stays up through the pause; OneGoodPair ants step beside their houses; TableAndDet diagonals neutral (yellow / grey, no green/red). Kept: "Peace in our time." (Priyanshu's call). BruteForce thumbnails could not grow (no room).
- **Act 2 pass (5 Nov):** Slots got a 2.0 s pause after line 0 (viewers watch all six step-choices before "Four choose two: six") and 0.6 s after line 1 — lags now ≤ 1.8 s (was 3.1 s); ListRoutes drawing sped up (no lag); green replaced by yellow for R/"a steps right" (green means never-meet); "always 4 steps: 2 R, 2 U" and the (a + b) choose a formula no longer run off screen.
- **Parked for after the full pass — verified quotes** (exact wording checked in the sources): Axler 1995 "Determinants are difficult, non-intuitive, and often defined without motivation."; Amdeberhan–Koutschan–Zeilberger 2023 "Yay for Determinants!" ("…not just wrong, but wrong…"; "determinants are easy, intuitive, and can be easily defined with great motivation"); Wigderson (Ahlfors lecture abstract) "The determinant is undoubtedly the most important polynomial function in mathematics."; Aigner–Ziegler, Proofs from THE BOOK, "Lattice paths and determinants": "…what they really want to prove, once in their lifetime, is a Lemma…"; Aaronson blog: "…only by some innocent-looking -1 factors…"; Weinberg (via Aaronson): "…it is also a determinant, except without minus signs."; Krattenthaler: "Evaluating determinants is not (okay: may not be) difficult!" and "linear algebra without determinants is an aberration"; Valiant 1979 "…annoyingly obvious even for small matrices…". Proposed: open with the Down-with/Yay "determinant war", Aigner–Ziegler before the proof, Weinberg/Aaronson near the end. Avoid the Lewis Carroll/Queen Victoria story (Carroll denied it). Unverified (do not use): Artin "shorten proofs by 50%", Strang paraphrases.
- **Sign section restyled (overnight, act8b_signs.py; Dominoes2x3 + KastFix replace SmallBoard2 + SignFix2):** no b₁/w₁ letters — the matrix rows/columns are tiny 2×3 boards with the square lit; a domino = one dark + one light square; entries filled with the pair highlighted; each tiling = one term; det A = −1 (+1 − 1 − 1); Kasteleyn: one −1 edge, only the all-vertical tiling uses it, det A = −1 − 1 − 1 = −3, |det A| = 3 ✓. Verified at import. Board4x4 and FKT unchanged.
- **v13 COMPLETE first pass (6 Nov): 16:09.** Last section: SignsCard "When the signs go wrong" ("But not every counting problem is secretly paths. What then?"); SmallBoard2 now opens "Take dominoes on a chessboard…" (old line referred to a chessboard in the opening that no longer exists); FKT: "…Listing one per second would take five months. The determinant does it in an instant." (12,988,816 s ≈ 150 days); Finale says meet / don't meet, not good / bad; Goodbye has no A₁/A₂ letters. ArcticCircle, SignFix2, Board4x4, Map, Credits unchanged. Remaining for the polish pass: chapter list, quotes, early #P stake line, cost line (n³, ω), Mahajan–Vinay beat (verify first), sound/pacing review, one full watch-through.
- **Disguises v13** (done) (Priyanshu: card title "Does the pattern repeat?"), file act6d_pattern.py: PatternCard ("So any puzzle that is secretly a family of paths that never touch, a determinant can count." with the recap "det = number of families that never touch" → title) → Hexagon (merged HexTiling + TilesToPaths: triangles → tile → three directions → tiling like boxes → "completely flat" → ? with a few tilings → fade the flat tiles → two chains → never touch → squashed onto our grid = our two ants → 20 tilings). WhatLGVCounts, HexTiling, TilesToPaths removed from pacing. Boxes (act6d_pattern.py, replaces BoxesCorner): bigger 3×3×3 box stacks up → three chains → squashed onto a 6×6 grid, three ants → matrix A = [[20,15,6],[15,20,15],[6,15,20]] (ant rows, house columns) → det A = 980 → "Percy MacMahon, 1915". Mountains (replaces CatalanMountains; v2 more detailed at Priyanshu's request: what Catalan numbers are — counts by length 2/4/6/8 steps = 1, 2, 5, 14; "one of the most famous sequences in combinatorics"; brackets (( )) and ( )( ) under the 4-step ranges; the 5 triangulations of a pentagon; why each matrix entry is Catalan by its step count): one range drawn step by step (✗ below sea level) → galleries 1, 2, 5, 14 (Catalan) → two ranges inside each other, a touching pair ✗ → starts/homes in ant colours → A = [[2,5],[5,14]] with an example path per entry → det A = 2·14 − 5·5 = 28 − 25 = 3 (aligned) → the 3 pairs. Aztec (detailed; AztecTiles + AztecPathsD replace AztecIntro + AztecPaths): diamond built row by row and tiled; order 1 → 2 (both shown), order 2 → 8 (all shown), order 3 → 64; "Guess the next one" → 1024 = 2¹, 2³, 2⁶, 2¹⁰; chessboard colouring → four kinds of domino → their jobs (flat step, step up, step down, nothing) → two paths left to right → tilings ⇄ non-touching path pairs (several shown) → A = [[2,2],[2,6]] (paths from each start to each end, counted in the graph of steps the dominoes can make; verified: only the straight pairing avoids touching) → det A = 2·6 − 2·2 = 8 → order 3: A = [[2,2,2],[2,6,10],[2,10,26]], det 64 → 2^(n(n+1)/2), EKLP 1992. (The old slide's [[12,4],[4,2]] also had det 8 but counted steps no domino makes.) Still old style: AztecIntro, AztecPaths, ArcticCircle (next, one at a time).
- **General lemma v13** (Priyanshu, act5b_lemma.py; replaces MoveHomes + LemmaVisual in pacing): LemmaCard "The general lemma" → BookQuote (Aigner & Ziegler, Proofs from THE BOOK, chapter "Lattice paths and determinants": "The essence of mathematics is proving theorems — and so, that is what mathematicians do: they prove theorems. But to tell the truth, what they really want to prove, once in their lifetime, is a Lemma…" — wording verified on Springer's chapter page) → LGVNames: name cards Bernt Lindström 1973 (matroid theory), Ira Gessel 1985, Xavier Viennot 1985 — NO PHOTOS: none of the three has a freely licensed photo on Wikipedia/Commons; add only with permission → GeneralLemma: a general one-way network (planar, edges right/up/up-right, seed 120), starts a₁ a₂ a₃, ends b₁ b₂ b₃, M = [[3,4,2],[7,11,9],[8,13,14]], the 4 paths a₁→b₂ counted, det M = number of families a₁→b₁…aₙ→bₙ that never touch, footnote "(when every crossed pairing must touch; in general, a signed count over pairings)", here det M = 13 (verified: 13 non-touching families; every other pairing has 0). The n³ / ω lines and the order ("move the houses") beat are not in this version — to decide.
- **AllPairs** (new, before the proof; Priyanshu): all 36 own-home pairs as thumbnails ("Six times six counts all thirty-six pairs going home"), coloured 20 never meet / 16 meet; 16 swapped thumbnails ("Four times four… also sixteen"); det A = 6·6 − 4·4 = (20 + 16) − 16 on the right; the minus sign must cancel 16 against 16 → "So they must match up, one to one. Let's see how." (arrow with ?). Then the proof below.
- **Proof v13** (current, Priyanshu's order: ants first, formula last; slow, visual, few words), file `act4c_proof.py`: SwappedToMeet (a swapped pair; blue starts left of orange and ends right — diagonal sweep with the column gap −1 −1 0 +1 +1 — so they share a dot; swap the tails at the first shared dot → each at its own home, paths meeting; ants walk them) → MeetToSwapped (another meeting pair → swap → each other's houses → swap again at the same dot → back) → Bijection (all 16 couples on the grid; the first three named one line each, "And so on", then "Sixteen of each") → Formula (det A = 6·6 − 4·4 = (20 + 16) − 16 = 20 with examples on the grid: a never-meet pair, a meeting pair turned into its swapped partner; the 16s linked and struck; ∎). Right-hand bullets: swapped → meeting, meeting → swapped, one to one. ReadCounts and the act4b proof scenes are no longer in pacing (bijection verified in code: swap_tails maps the 16 meeting pairs exactly onto the 16 swapped pairs).
- **More examples + why card (6 Nov, Priyanshu):** after "which is twenty. Voilà!" → "The same number as before." (no "Coincidence? Hardly") → new scene ThreeAnts (act3b_more.py): "In fact, there's nothing special about this scenario." The 4×4 board grows to 5×5 (old dots slide up one row), a purple ant ("hey!") and house join; matrix A = [[6,4,1],[4,6,4],[1,4,6]] (rows ants, columns houses), det A = 50; all 216 triples checked on the grid (first 3 slowly), never meet: 50. → WhyCard: "Why does this work?" centred → "Let's get back to our two ants, and work it out." → ReadCounts and the proof. SekiJoins removed from later in pacing (its example moved here).
- **Proof v12** (current, in Priyanshu's puzzle style): new file `act4b_proof.py` (SwapPaths, SwapTwice, DiagonalSweep, PutTogether; the old versions in act4_proof.py are no longer in pacing). Everything on the puzzle's big board (`big_lattice()` + `board()` in common.py: ants, coloured houses, no letters). Right-hand bullets as each step is said: "walk to the first shared dot", "swap the tails", "swap twice = no change". The blue ant walks its path to the first shared dot; tails swap; both ants walk their new paths and stop in front of the other's house. Couples shown as two icons with ⇄ arrows. Diagonal sweep: the gap row −1 −1 0 +1 +1 fills in on the right. PutTogether: all 16 meeting pairs are swapped into their partners on the grid (first two slow, then fast; "couples found: 16"), then det A = 6·6 − 4·4 = (20 + 16) − 16 = 20 with the = signs aligned and both 16s struck out; ∎. Wording uses meet / never meet, paths, blue/orange ant.
- **Puzzle v12**: whole video slower (TTS speed 0.97→0.90, gap between lines 0.45→0.8 s). Rules: down/left are tried from where the ant got to after up+right. "Many paths": 2 blue + 2 orange, each ant's two paths share no segment (blue and orange cross at two dots). Meter: first four pairs slow, named ("This pair works. This one doesn't. Neither does this one. Or this one. And so on.") with tick/buzz, then speeding up. Light sound effects (pop houses, tick paths, buzz ✗, rumble fight, chime 20). Hook ends erasing only the right-hand side; TableAndDet stays on the same grid: "…here comes an old friend." → "Consider this two-by-two matrix, A" (no box: A = [ ], house icons over columns, ant icons by rows) → first entry counted path by path (six) → second, "a little sneakier", blue ant to orange house (four) → "by symmetry" four and six → "Now find the determinant of A" with the = signs one under the other → "which is twenty. Voilà!" → "The same twenty. Coincidence? Hardly." (The word "determinant" is first said at "Now find the determinant".) ListRoutes and Slots are now CUT from pacing (Priyanshu: the puzzle already counts the paths). After "Coincidence? Hardly." comes ReadCounts with new wording: "…including the pairs that meet. That's the twenty that never meet, plus the sixteen that do. … So the determinant is: never meet, plus meet, minus swapped…"; on-screen labels say never meet / meet (not good / bad).
- (superseded) **Puzzle v11**: Hook now holds the whole puzzle on one screen, 12 lines: hi!/yo! → grid world → homes → rules (bullet "• step up or right" on the right; ✓ up/right, ✗ down/left) → many paths home (3 blue, 2 orange, crossings ringed) → the fight (dust cloud; bullet "• paths never touch") → scent trail (said, not written) → "how many pairs of paths get them home without intersecting?" → an easy good pair → one that crosses → "Let's check them all, one by one": all 36 pairs flash by, counters never meet 20 / meet 16 → "Twenty pairs never meet, and sixteen do." Word "paths" everywhere, not "routes". OneGoodPair and BruteForce REMOVED from pacing (code kept). TableAndDet: "I know what you're thinking: this is stupid… here comes my friend, the determinant." → "Consider this two-by-two determinant. Each entry counts the paths from one ant to one house." (rows = ant icons, columns = house icons) → "six times six minus four times four" → "It's twenty. Voilà!" → "The same twenty. Coincidence? Hardly."
- (superseded) **Puzzle v10**: Opening ends "Let's start with a simple puzzle." on an empty screen. Hook: 0 "Meet these two ants." (each hops, says "hi!") → 1 "They both live in a grid-like world." (grid appears) → 2 "And they both want to get back home, right now." (coloured houses + arrows) → 3 rules: blue ant steps up ✓ and right ✓, tries down ✗ and left ✗ → 4 "many ways home" (two blue routes, one orange) → 5 "They had a fight, and if they meet, they'll start fighting again." (they meet; cartoon dust cloud, #@%!, stars) → 6 scent-trail rule → 7 can't touch + question + rules box → 8 pause. No A₁/B₁/B₂ labels anywhere in the puzzle: colours, ants and houses only (TableAndDet headers are ant/house icons).
- **Opening v10** (current): montage REMOVED (Priyanshu). After the polygon: "One of the most beautiful and unexpected places I've found determinants is combinatorics." (screen: just the small formula) → "And today, I want to show you how determinants can count." with the title **How Determinants Can Count** written in the CENTRE of the screen (no name, no grid) → "Let's start with something small: two ants." (grid, then ants). 8 lines, 37.6 s.
- (superseded) **Opening v9**, Priyanshu's direction): after the polygon, "And many more. Determinants are everywhere." with a wall of six small unlabeled animations (lines turning parallel, square to parallelogram, grid squashed, polygon fan, cube sheared to a box, three points becoming collinear); "But one of the most beautiful places I find them is in combinatorics." (the montage cross-fades into the ants' grid); "Today, I want to show you how determinants can count." with the title **How Determinants Can Count** on screen (no name); "Let's start with something small: two ants." The old title card + author line at the end of TableAndDet was removed (its 2.2 s pause is now 0.4). Opening: 9 lines, 40.3 s.
- **Opening v8.5**: v8.4 plus a minimal polygon beat after "squashed flat": line "It even finds the area of any polygon."; pentagon, yellow fan triangles (+5, +6.5, +2), grey overhang triangles (−0.5, −2.5) cancel, label "area = ½ Σ det" (= 10.5, verified). 7 lines, 30.4 s.
- **Opening v8.4**: polygon beat REMOVED (Priyanshu: not obvious enough); back to three uses, 6 lines, 26 s. Equations beat shows "det ≠ 0" while the lines cross, then "det = 0" when parallel. Area beat made concrete: matrix [[2,1],[0,1]] (det 2) applied as stretch ×2 (the square labelled 1 becomes two squares, 1 | 1, then 2) then a shear (base and height kept, still 2), then "det = 2"; line: "…scales area. Here, every area doubles." Triangle-area / collinear-points beat offered, not added.
- (superseded) **Opening v8.3** (Priyanshu chose it): new line 4, after "squashed flat": "With signs, it even finds the area of any polygon: fan out triangles from one point, and the negative ones cancel exactly what sticks outside." Visual: pentagon (2,1),(5,2),(5,4),(3,5),(1,3), fan point O = (0,0); yellow triangles +5, +6.5, +2, grey triangles −0.5, −2.5; the grey lies exactly on the outside part; both vanish, leaving the pentagon. 13.5 − 3 = 10.5 = the area, checked independently (numerical estimate 10.507). It foreshadows the video's cancellation theme. Opening is 7 lines, 33.8 s, max cue lag 0.5 s.
- **Opening v8.2** wording (Priyanshu): line 1 "It tells us whether a system of linear equations has a unique solution." ("unique", since det = 0 can also mean infinitely many); line 2 "It measures how much a linear transformation scales area." with the label "area × |det|"; line 3 "And when it's zero, everything gets squashed flat." ("cannot be reversed" was too abstract). Opening 24.0 s, max cue lag 0.5 s. A deeper equations version (real system 2x+y=4, x+3y=7, Cramer's rule, live det 5→0) was built and shelved: Priyanshu wants it light (kept locally as act0_opening_v9_deep.py.bak, not in the repo).
- **Opening v8.1** (same six lines and beats as v8, made clearer and synced; rendered and frame-checked by Claude): 1.6 s pauses after "solve equations" and "measures area" so each picture finishes; the equation dot is the unique solution and slides off along the lines as they turn parallel, then "det = 0"; the area beat keeps a ghost unit square beside the parallelogram; the "cannot be reversed" beat flattens the plane by a rank-1 map whose kernel contains the difference of two marked points, so the blue and orange points visibly land on one spot; the flat line turns into the ants' grid (no black gap) with "counting" beside it. Cue lags: only line 4, 0.4 s. Opening is now 21.9 s.
- The GitHub Actions rebuild is verified working (run for v8 succeeded: build, commit, Pages). A full rebuild takes about 25 min; a new push cancels a running build.
- Earlier logged sync lags (not yet re-measured after v8): BruteForce 3.9 s, Slots 3.1 s, TableAndDet 1.7 s.
- **Still open for Priyanshu:** review the new opening line by line; whether to apply ideas A–E (§5); own voice versus placeholder voice.
- Remove any API keys that were pasted into chats (a Gemini key was pasted once; revoke it at aistudio.google.com).

## 7. How the project works

Everything is in the project folder (`determinants_video/`).

| File | Role |
|---|---|
| `pacing.py` | scene order (`SCENES`) |
| `narration.json` | every spoken line per scene. Strings are lines; numbers are pauses in seconds. Line *k* ↔ `self.cue(k)`. |
| `common.py` | shared look: colours (ANT1 blue, ANT2 orange, ANT3 purple, MEET yellow, GOOD green, BAD red); helpers (`Lattice`, `ant`, `path_mob`, `walk_steps`, `matrix_mob`, `T()`, text minimum 22); `DScene` |
| `act0_opening.py` … `act9_ending.py` | scenes; `act6c_arctic.py` has domino shuffling |
| `audio/tts.py` | AI voice to `audio/voice/*.wav` and `timing.json` (`--scene X` re-records one scene) |
| `audio/mix.py` | voice + sound effects + music + captions → `final_720p30.mp4` and `final_720p30_captioned.mp4`, `captions.srt` |
| `render_all.sh m` / `render_seq.sh m` | timed video render (parallel / sequential) |
| `render_slides.sh m` | manim-slides render (into `media_slides/`), building `slides/presentation.html` |
| `research/build_present.py` | builds the presenter view and deck into the site folder |
| `research/article.py` | builds the article (`article/index.html`) |
| `publish.sh` | rebuilds the slides, presenter view and article, then pushes the site (`--voice Scene`, `--video`) |
| `studio.py` | local editor/player (http://localhost:8765) |
| `.vscode/tasks.json` | VS Code tasks |
| `README.md` | setup |

**`DScene` sync:**
- `self.cue(k)` waits until narration line *k* starts.
- `self.cue_at(k, "word")` waits until that word in the line.
- `self.cue_end(k)` waits until the line ends.
- Lags are logged to `logs/cue_lags.json`.
- **Slides mode:** with `SLIDES=1`, `DScene` becomes a manim-slides `Slide` and each `cue(k)` becomes `next_slide(notes=line k)`. A small shim in `common.py` makes manim-slides 5.7 work with Manim 0.22.1.

**Environment:**
- Manim Community **0.22.1**. Use `Text()` only; no LaTeX.
- **Never** install manim-voiceover or manim-themes: they downgrade Manim and break rendering.
- You need ffmpeg and Python 3.10+.

**Typical edits:**
- **Change the words:** edit `narration.json`, then `python audio/tts.py --scene X`, then re-render that scene, then `audio/mix.py`.
- **Change an animation:** edit the scene, then `manim -qm file.py Scene` (video) or `SLIDES=1 manim -qm …` (slides).
- **Add a slide:** add a line in `narration.json` and a matching `self.cue(k)`. The number of cues must equal the number of spoken lines.
- **Publish:** `./publish.sh` (add `--video` after narration or animation changes for the voiced film).

## 8. Rules for assistants

1. Read §4 before proposing ideas. Don't bring back rejected ones.
2. Verify any number you put on screen, in code where possible, and say what you verified.
3. Never commit secrets or API keys. Never publish anywhere new without Priyanshu's explicit yes.
4. Keep the default Manim theme and the colours and characters above.
5. After any change: update §6, add to §10, and say what was done and what is left.

## 9. Reading list (for Priyanshu)

- Aigner & Ziegler, *Proofs from THE BOOK*, chapter "Lattice paths and determinants" (the proof in Act 4).
- Wikipedia: Lindström–Gessel–Viennot lemma; FKT algorithm.
- Mathologer, "The arctic circle theorem" (YouTube).
- Gessel & Viennot (1985); Jockusch, Propp & Shor (1995, arXiv math/9801068); Valiant (1979); Kasteleyn (1961).

## 10. Change log (newest first; one line each: date, who, what)
- 2026-11-11 · Claude · Opening narration lines 0–14 now Priyanshu's own recording (his wording in narration.json; takes in audio/recorded/Opening, manifest updated). Cleaned: DeepFilterNet3 + HPF 80 Hz, mild EQ/de-ess/compression, loudnorm −16 LUFS; long pauses inside lines shortened, tempo ×1.07. Lines 15–17 still AI (to record). cue_at phrases updated for lines 12, 14.
- 2026-11-11 · Claude · v18: Part 5 cut to hexagon + Aztec (Boxes, ExCard2, Mountains removed from pacing.py); ExCard1 subtitle 'tilings of a hexagon', ExCard3 now 'Example 2'; Map shows 4 panels (Aztec formula in LaTeX); Credits drop MacMahon/Catalan and the unused opening-quotes line. Length 23:51 (AI voice). First voice test of Priyanshu cleaned with DeepFilterNet + EQ/compress/loudnorm, takes in audio/recorded_demo/Opening_test1 (not active).
- 2026-11-11 · Claude · Video board (shared editor): https://claude.ai/artifact/7rr6uxYgBdgaTGuWyUS66H — 36 scene clips + editable narration/notes in its database (`scenes/<Scene>`). Priyanshu saves → status "changed"; Claude applies, re-renders, republishes the clip and sets status "done" + claude_reply. Source in `board/`.

- 2026-11-11 · Claude · scripts/setup_mac.sh: one-command Mac setup (Homebrew, Python 3.13, ffmpeg, cairo/pango, BasicTeX + Manim's LaTeX packages, venv, voice model, full render, mix) then starts the Studio on http://localhost:8765; `--studio` just starts it. Untested on a real Mac.
- 2026-11-11 · Claude · Opening v17: no 'Determinants' card (starts with the big det again; nothing stays on top; per-use maths moved up); no counting montage after the Valiant slide — 'combinatorics' is only said, then the title is written.
- 2026-11-11 · Claude · Opening: general forms back to calm animation speed, each with a very short line and a pause ("Expand along a row," / "multiply the eigenvalues," / "or add up signed products.").
- 2026-11-11 · Claude · Opening v16 = v14 with only Priyanshu's changes: fast general forms (one line), speed said + 'O(n³) computations using Gaussian elimination' with Gauss's portrait, 'and even faster' (no n^ω timeline), then algebraic complexity (det easy ✓), perm believed hard, Valiant 1979 #P-complete + 'efficient ⇒ P = NP (and much more)' (no perfect-matching graph), "So counting is usually hard. And yet, determinants… are one of the rare tricks that can count efficiently…" → montage → title. v15 kept as act0_opening_v15.py.bak.
- 2026-11-11 · Claude · Opening v15 (Priyanshu): faster start (general forms in one line with quick animations), uses one short line each, no n^ω timeline and no perfect-matching graph; one minimal slide: det ≈ n³ (said: Gaussian elimination, faster if you really want), counting → #P (efficient ⇒ P = NP), perm (det without signs) #P-complete with Valiant photo, 'algebraic complexity theory' label → "So when a counting problem turns into a determinant, it suddenly becomes easy" → combinatorics montage → title. Old: act0_opening_v14.py.bak.
- 2026-11-11 · Claude · Opening v14 order: forms → all over mathematics (equations, area, polygon) → speed timeline → algebraic complexity (det = model easy polynomial; perm = same sum without signs, believed hard) → Valiant 1979 perm #P-complete (#P = count solutions of NP problems; photo) → counting perfect matchings equally hard, efficient ⇒ P = NP and much more (Toda) → "And yet, with their minus signs, determinants can count…" → combinatorics montage → title. Old: act0_opening_v13.py.bak.
- 2026-11-11 · Claude · Opening: row expansion starts with 'a det[…]' (no leading +); new speed beat after the general forms: "For a computer scientist… fast to compute" + timeline of the exponent (c.1810 Gauss n³ with portrait; 1969 Strassen 2.81 with photo by David Eppstein, CC BY-SA 3.0; 1990 Coppersmith–Winograd 2.376; 2014 Le Gall 2.3729; 2024 Alman et al. 2.371339; 2026 AlphaEvolve/DeepMind 2.371177, announced Aug 2026, not yet independently verified). No OpenAI (no known result). Credits updated.
- 2026-11-11 · Claude · Opening: minors written as det[…] (not |…|); equations: "has a unique solution ⇔ det ≠ 0" in smaller type, shorter lines placed lower, the solution dot hides once it leaves the drawn lines.
- 2026-11-11 · Claude · Opening: each general form animated on the left while its formula appears on the right — row expansion (top entries boxed, row+column dimmed, +a|…| −b|…| +c|…|), eigenvalues (two directions stretched ×λ1, ×λ2, the shape between them grows), permutations (the six one-per-row-and-column picks with ± signs). Narration lengthened to explain each.
- 2026-11-11 · Claude · Opening v13: starts with a 'Determinants' card that rises to the top and stays through the intro, then turns into the title; the ad − bc formula no longer stays on top — each use shows its own maths at the top instead (system of equations ⇔ det ≠ 0; area(A S) = |det A|·area(S); polygon area formula).
- 2026-11-11 · Claude · GeneralLemma network v17: 6×6 dots, six possible ends on each side (all connected), three picked on each side not the top three: a = rows 5,3,1 (left), b = rows 5,4,2 (right), seed 55; M = [[3,5,0],[3,6,7],[1,2,5]], det 8 (not shown); 5 paths a1→b2 drawn; checked: only the straight pairing avoids touching.
- 2026-11-11 · Claude · GeneralLemma network v16: every arrow points right (said aloud), seed 179, 6×4; ALL 3 paths a1→b2 drawn when explaining m_ij; M = [[5,3,1],[9,6,3],[1,1,3]], det 6 (not shown), only the straight pairing avoids touching (checked). Fixed leftover paths (FadeOut of a group left its separately-created parts on screen).
- 2026-11-11 · Claude · GeneralLemma network v15: arrows flow left→right (seed 60), starts a1–a3 down the left edge, ends b1–b3 down the right edge in the same order (dashed 'lanes' shown on "same order"); mixed-up example a2→b3 & a3→b2 forced to cross. Verified: only the straight pairing can avoid touching; M = [[1,9,7],[0,6,6],[0,9,11]], det 12 (not shown).
- 2026-11-11 · Claude · GeneralLemma: n³/explodes lines and the bracketed condition removed; the condition is now explained when the points are picked: "keep the ends in the same order as the starts… if a1 goes to b2 and a2 to b1, the paths are forced to cross" with that mixed-up pair drawn and its meeting circled (all 28 such pairs meet, checked).
- 2026-11-11 · Claude · BookQuote: Erdős photo (assets/book/erdos.png, supplied by Priyanshu) appears as his name is said; the cover shrinks to the top right and the photo sits under it. Credits: photo attribution (believed to be Kmhkmh, Wikimedia Commons, CC BY 3.0 — CHECK) and the book cover.
- 2026-11-11 · Claude · GeneralLemma v14: no calculations (no '4 paths', no det 13): symbolic M (m_ij = # paths a_i→b_j), a few example paths drawn without counting, det M = # families that never touch (LaTeX), condition in two lines, n³ cost line kept. Old version act5b_lemma_v13.py.bak.
- 2026-11-11 · Claude · BookQuote: Erdős line added (spoken + written under the quote): "You don't have to believe in God, but you should believe in The Book." (1985 lecture, per Wikipedia/Quanta).
- 2026-11-11 · Claude · LGVNames removed: GeneralLemma now opens with the title 'Lindström – Gessel – Viennot lemma' (kept on top) while the names and years are only spoken; then 'First, take a directed acyclic graph: dots joined by one-way arrows, with no cycles…'.
- 2026-11-11 · Claude · BookQuote: quote first, then the book's cover (assets/book/proofs_from_the_book.png, supplied by Priyanshu) while the source is spoken; names no longer written.
- 2026-11-11 · Claude · Removed TheTrick (D.I.E.) from the video; credits updated.
- 2026-11-08 · Claude · TheTrick: involution explained in words ("a rule that pairs things up: apply it once, you jump to a partner; again, you come right back") with an A ⇄ B picture; layout fixed so Exception stays in frame.
- 2026-11-08 · Claude · TheTrick: permanent vs determinant, D.I.E. method; credits for Benjamin–Cameron (ants, 2005) and Benjamin–Quinn.
- 2026-11-08 · Claude · ThreeProof: the 3-ant cancellation shown term by term (198 pairs, 50 left).
- 2026-11-08 · Claude · Bijection/Formula: no 'couples'; every meeting pair has a matching wrong-house pair and vice versa → one-to-one → meet = wrong houses; det A = all − wrong houses = all − meet = never meet = 20.
- 2026-11-08 · Claude · Proof intro v14: back to the ants, why 6·6 / 4·4, 'wrong houses' naming, equal counts → why?
- 2026-11-08 · Claude · More ants v13c: 7×7, staircase then layout U, det 252.
- 2026-11-08 · Claude · More ants v13b: all ants/homes scattered, det 136, closing lines.
- 2026-11-08 · Claude · More ants: 6×6 grid, four ants, scattered homes, det 486 (verified).
- 2026-11-08 · Claude · Opening forms reordered (row, eigenvalues, permutations); ✓/✗ for the example pairs below the grid; pair check in a random-looking order (works, doesn't, does, doesn't, then the rest shuffled).
- 2026-11-08 · Claude · Puzzle: slower rules, zig-zag paths one at a time, new question; matrix: C(4,2)/C(4,1) counting aside.
- 2026-11-08 · Claude · Opening v12: LaTeX, no labels, no pivots, visual-only scaling, numbered polygon triangles, counting montage.
- 2026-11-08 · Claude · Opening v11 to Priyanshu's script; quotes removed from pacing.
- 2026-11-08 · Claude · Studio: record/upload your own voice per line; tts.py uses matching takes.
- 2026-11-08 · Claude · KastWhy: why Kasteleyn's rule works (superpose two tilings → loops; each loop flips the sign an even number of times).
- 2026-11-08 · Claude · v14: added every proposed option for review (D quotes, B stake line, E chapter cards, C cost line, bridge line, A Mahajan–Vinay, F Vazirani/Valiant, G credits) and rebuilt the signs section (Dominoes2x3, KastFix, Board4x4, FKT) slow and detailed; new file act_extras.py.
- 2026-11-06 · Claude (overnight) · Full watch-through: the crossing pair in the puzzle now stays up 1 s longer; AllPairs equation pulled inside the frame; credits match the video (added Aigner & Ziegler as the quote's source and Kasteleyn's 1967 planar result; removed vicious walkers, ω and portraits, which are no longer in the video).
- 2026-11-06 · Claude (overnight) · FKT history fixed: 1961 = chessboard/rectangles (Kasteleyn; Temperley & Fisher, independently); all planar graphs = Kasteleyn by 1967 (on-screen credit and narration "And by 1967, Kasteleyn had made it work for any graph you can draw without crossings…"). Rendered, slides tested.
- 2026-11-06 · Claude (overnight) · Board4x4: on-screen text cut to det A = 0 ✗, the two-line rule, |det A| = 36 (the joke is spoken only). Rendered, slides tested.
- 2026-11-06 · Claude (overnight) · New chapter list in assemble.py; consistency pass (no issues left); Mahajan–Vinay verified from the paper (drafted only). Overnight summary + options: OVERNIGHT.md at the repo root.
- 2026-11-06 · Claude (overnight) · Sign section 2×3 board restyled without letter labels. Rendered, frame-checked, slides tested.
- 2026-11-06 · Claude · Finished the first full pass: signs card, wording fixes in the sign section and ending, no letters in Goodbye. Full video 16:09. Rendered, slides tested.
- 2026-11-06 · Claude · Aztec diamond, detailed, in the new style (det 8 and 64 re-derived and verified). Rendered, frame-checked, slides tested.
- 2026-11-06 · Claude · Mountains v2: explains the Catalan numbers (counts by length, brackets, pentagon triangulations, why the matrix entries are Catalan). 81 s. Rendered, frame-checked, slides tested.
- 2026-11-06 · Claude · Mountains (Catalan, det 3) in the new style, detailed. Rendered, frame-checked, slides tested.
- 2026-11-06 · Claude · Boxes in a corner in the new style (det 980). Rendered, frame-checked, slides tested.
- 2026-11-06 · Claude · "Does the pattern repeat?" card + Hexagon (one continuous screen). Rendered, frame-checked, slides tested.
- 2026-11-06 · Claude · General lemma part (card, book quote, LGV name cards, general network with det 13). Rendered, frame-checked, slides tested.
- 2026-11-06 · Claude · Added `.nojekyll` at the repo root: Pages now serves files as-is and the deploy succeeded (two plain redeploys had timed out). Site LIVE with AllPairs + proof v13 (133 presenter slides). If deploys time out again: shrink determinants/video.mp4 (43 MB) and the presenter clips.
- 2026-11-06 · Claude · Pages deploy of the AllPairs build timed out on GitHub's side (10-min limit; the site is ~91 MB of clips). Re-triggered by a root-only push (HANDOFF.md), which redeploys Pages without re-running the video build. If it recurs, consider lighter presenter clips.
- 2026-11-06 · Claude · Added AllPairs (36 = 20 + 16, 16 swapped, "let's see how") before the proof. GitHub build for proof v13 SUCCEEDED (site live). Rendered, slides tested.
- 2026-11-06 · Claude · Proof v13 (act4c_proof.py) in Priyanshu's order. Rendered, frame-checked, slides mode tested, no cue lags.
- 2026-11-06 · Claude · Added ThreeAnts (3 ants, det 50 = 50 never meet) and WhyCard after the matrix; SekiJoins dropped from pacing. Rendered, frame-checked, slides mode tested.
- 2026-11-06 · Claude · Build fix 2: research/article.py had a fixed scene list including removed scenes (OneGoodPair, BruteForce, ListRoutes, Slots) and crashed; it now skips scenes not in pacing.py, and its descriptions of the opening, puzzle, matrix and proof are updated. Tested locally.
- 2026-11-06 · Claude · **Build fix:** the last three GitHub builds FAILED (site still showed the old version): slides mode crashed on Hook because Manim keeps only 100 partial clips and Hook has 140+ animations. common.py now sets config.max_files_cached = 100000 in SLIDES mode. All new scenes tested in slides mode locally. Lesson: after every push, check the Actions run finishes green.
- 2026-11-05 · Claude · Proof v12 rebuilt on the big board in the puzzle's style (act4b_proof.py). Rendered and frame-checked; no cue lags.
- 2026-11-05 · Claude · Cut ListRoutes + Slots; ReadCounts reworded (never meet / meet, paths). Rendered and frame-checked.
- 2026-11-05 · Claude · Fixed the blue ant ending up turned (rotate + .animate in one play() drops the rotation — always turn, then move). det A lines smaller, '=' aligned under the '=' of "A ="; no "Voilà!"/"never meet: 20" text; line now "The same number as before. Coincidence? Hardly." No coincidence quote (Priyanshu).
- 2026-11-05 · Claude · Puzzle v12 + global slower narration; matrix scene on the same grid. Rendered and frame-checked Opening, Hook, TableAndDet.
- 2026-11-05 · Claude · Puzzle v11 (one-screen puzzle with bullets, fast brute-force counters, "my friend, the determinant… Voilà!"); OneGoodPair/BruteForce dropped from pacing. Rendered and frame-checked.
- 2026-11-05 · Claude · Puzzle v10: rewritten Hook (hi!, grid world, homes, up/right rules with ✗ for down/left, many ways home, fight cloud), no letter labels in the puzzle. Rendered and frame-checked.
- 2026-11-05 · Claude · Opening v10: removed the montage; combinatorics line; centred title; grid only with the ants. Rendered and frame-checked.
- 2026-11-05 · Claude · Act 5 reviewed: all numbers re-verified by brute force (MoveHomes 20/40/20/14 and 0 with det −10; 3×3 det 50 = 216−96−96−6+16+16; network det 42). ω claim verified online; "this month" → "last month", label ω(ℂ) ≤ 9/4.
- 2026-11-05 · Claude · Proof (SwapTwice, DiagonalSweep, PutTogether) reviewed: maths correct (first meeting point preserved by the swap; gap −1→+1 in steps of ≤1). Only headings pulled in from the frame edge.
- 2026-11-05 · Claude · ReadCounts relayout: bigger thumbnails, readable labels, "equal?" arrow clear of the text. SwapPaths reviewed (correct, unchanged).
- 2026-11-05 · Claude · Act 2 (ListRoutes, Slots): sync, overflow and colour fixes. Rendered and frame-checked.
- 2026-11-05 · Claude · Ant-puzzle fixes (Hook wording and question, rules box, ants beside houses, neutral det colours). Quotes researched and parked. Rendered and frame-checked Hook, OneGoodPair, BruteForce, TableAndDet.
- 2026-11-05 · Claude · **Opening v9:** "and many more" montage, combinatorics line, title moved into the Opening (no name); title card removed from TableAndDet. Rendered and frame-checked.
- 2026-11-05 · Claude · Opening: the diagonal strokes through the matrix now fade out once a d − b c is formed (they used to stay all the way through).
- 2026-11-05 · Claude · **Opening v8.5:** re-added polygon area minimally (one short line, ~3 s visual, label "area = ½ Σ det"). Rendered and frame-checked.
- 2026-11-05 · Claude · **Opening v8.4:** removed the polygon beat; added det ≠ 0 label for crossing lines; area beat now a countable det-2 example (stretch then shear, 1 → 2). Rendered and frame-checked.
- 2026-11-05 · Claude · **Opening v8.3:** added the polygon-area (shoelace) beat: fan triangles with signed areas, negatives cancel the outside. Numbers verified. Rendered and frame-checked.
- 2026-11-05 · Claude · **Opening v8.2:** new wording for the three uses (unique solution; how much a linear transformation scales area, label "area × |det|"; "when it's zero, everything gets squashed flat"); squash now starts on "zero"; pauses retuned. Rendered and frame-checked.
- 2026-11-05 · Claude · **Opening v8.1:** fixed v8 sync (pictures lagged the voice by 1.2–2.4 s; now ≤ 0.4 s via two pauses), fixed parallel-lines-while-"det ≠ 0" slip, dot slides off instead of vanishing, ghost unit square, two points merging on collapse, grid hands over to the ants without a black gap. Fixed `build_site.sh` aborting when no scene failed. Rendered locally and checked frame by frame.
- 2026-11-05 · ChatGPT · **v8 opening source:** shorter six-line intro and larger sequential visuals for equations, area and non-invertibility; removed child joke, Valiant, chessboard and all preview count cards; kept exact ants/grid handoff, aligned cues, updated pacing. Static validation only; GitHub rebuild/render pending.
- 2026-11-05 · Claude · **Source on GitHub + automatic rebuild:** source copied to `src/` of the site repo. Added `requirements.txt` (pinned), `scripts/fetch_models.py` (downloads the Kokoro model; verified byte-identical), `scripts/build_site.sh` (full build), `.gitignore`, the workflow `.github/workflows/build-determinants.yml`, and §2a. Font pinned to DejaVu Serif, so renders match on any machine.
- 2026-11-05 · Claude · **Audio fix:** loudnorm had raised every output to 96 kHz AAC, which many browsers (Safari/iOS) won't play. `mix.py` and `build_present.py` now force 48 kHz stereo. Video and all 127 presenter clips rebuilt; clip URLs carry a `?v=` version tag so browsers refetch.
- 2026-11-05 · Claude · Presenter view now plays **voice + sound effects** per slide: `NO_MUSIC=1 audio/mix.py` makes `final_720p30_nomusic.mp4`; `research/build_present.py` cuts it into one clip per narration line (`determinants/clips/NNN.mp4`, 127 clips) so picture/voice/effects match the film exactly. Background-music button removed (Priyanshu: no music for now). `publish.sh` updated.
- 2026-11-05 · Claude · **v7 opening** (Priyanshu's design): det met in school (a d − b c) → three animated uses (solve equations: lines go parallel → no solution; triangle area ½|det|; grid squashed when det = 0) → “to me, the most surprising place is counting” → child counts “one, two, cha-cha-cha!” (own synthesized clave/shaker; no meme audio) → Leslie Valiant photo (Dennis Hamilton, CC BY 2.0) + #P-complete (perfect matchings flicker on a cube graph) → “a single determinant counts…” cards (20, 20, 12,988,816, 64) → hands over to the ants. Hook line 0 now “Meet two ants. They live on a grid.” Arctic teaser and “five months” removed. Video now 14:47.
- 2026-11-05 · Claude · Presenter view: optional background music (`determinants/music.mp3`, a gapless 64 s loop of the video's music bed, from `audio/music_loop.mp3`); ♪ button / M key, volume slider, remembers on/off. Started the slide-by-slide review (Opening 1–6 notes sent; awaiting Priyanshu's choices).
- 2026-11-05 · Claude · Created this HANDOFF.md, with AGENTS.md and CLAUDE.md pointers.
- 2026-11-05 · Claude · Published the presenter view (captions below the slides, arrow keys) and added `publish.sh`.
- 2026-11-05 · Claude · Published the article, deck and video to priyanshu.github.io/determinants. Fixed timed renders overwritten by slides mode (slides now render into `media_slides/`).
- 2026-11-05 · Claude · Watched and compared the SoME4 reference video; proposed improvements A–E (not applied).
- 2026-11-04 · Claude · v6 built from the storyboard: new opening (det → counts → chessboard), scent-trail puzzle, reorder, trees cut, manim-slides support, Studio.
- 2026-11-04 · Claude · v5: line-by-line review fixes (word-level sync, concrete lemma numbers, ω staircase, lanes and probe visuals, FKT matching view).
- Earlier · Claude · v1–v4: ants on a 4×4 grid, proof, LGV, disguises, Kasteleyn/FKT, arctic circle, finale; AI narration, mix, captions.
