# HANDOFF: "How Determinants Can Count"

**Shared working file for every assistant (Claude, ChatGPT, others) and for Priyanshu.**
Read it fully before doing anything. After you change something, update §6 *Current state*
and add a line to §10 *Change log*. Keep it truthful: say what was verified and what was not.

---

## 1. The project in one paragraph

- **What:** an expository video, *How Determinants Can Count*, by **Priyanshu** (research scholar, IIT Indore).
- **Competition:** **DepthTCS 2026** video competition, co-located with FSTTCS 2026. Limit 20 minutes; deadline **5 Nov 2026, Anywhere on Earth**.
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

**Verified in code:** every number above (bijections for the Aztec diamond, Catalan, boxes and hexagon included). **Not verified by an assistant, so Priyanshu must check before citing:** the ω ≤ 9/4 line ("October 2026, an AI model at OpenAI, checked in Lean, explained by Amir Shpilka, ECCC TR26-281"), and the historical dates.

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

- **Opening v8.3** (Priyanshu chose it): new line 4, after "squashed flat": "With signs, it even finds the area of any polygon: fan out triangles from one point, and the negative ones cancel exactly what sticks outside." Visual: pentagon (2,1),(5,2),(5,4),(3,5),(1,3), fan point O = (0,0); yellow triangles +5, +6.5, +2, grey triangles −0.5, −2.5; the grey lies exactly on the outside part; both vanish, leaving the pentagon. 13.5 − 3 = 10.5 = the area, checked independently (numerical estimate 10.507). It foreshadows the video's cancellation theme. Opening is 7 lines, 33.8 s, max cue lag 0.5 s.
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
