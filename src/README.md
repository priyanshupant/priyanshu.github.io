# How Determinants Can Count

A DepthTCS 2026 video by Priyanshu (IIT Indore), animated with Manim Community 0.22.1.

## Setup (once)

1. Install ffmpeg and Python 3.10 or newer.
2. Install the Python packages:
   `pip install manim==0.22.1 kokoro-onnx soundfile numpy pillow`
3. Download the voice model into `audio/models/` (`model_quantized.onnx` and
   `voices.npz`, from onnx-community/Kokoro-82M-v1.0-ONNX on Hugging Face).
   You only need this to re-record the AI voice.
4. Open this folder in VS Code. Accept the recommended extensions:
   - Python
   - Manim Sideview, which previews a scene beside its code.

## Work slide by slide: manim-slides

Every scene doubles as a manim-slides presentation, with one slide per narration
line. Each slide's speaker notes are its narration.

    pip install manim-slides                          # once
    SLIDES=1 manim -qm act0_hook.py Hook              # render one scene as slides
    manim-slides present Hook                         # present it: arrow keys, space
    manim-slides convert Hook slides/Hook.html        # or open it in a browser

    bash render_slides.sh m                           # all scenes -> slides/presentation.html

**Editing loop:**
1. Change the code in a scene. Each `self.cue(k)` starts slide k.
2. Re-render that scene with `SLIDES=1 manim -qm …`.
3. Present it again.

When you're happy with it, render normally (without `SLIDES=1`) and run the mix
to get the voiced video.

On Windows PowerShell, set the variable with `$env:SLIDES='1'` before running manim.

In slides mode the scenes don't wait for the narration timing. Each slide just
plays its animations and stops. The final video still uses the timed render with audio.

`manim-slides present` opens a window and needs Qt (`pip install manim-slides[pyside6]`).
The HTML export needs nothing extra.

## Or: the Studio (video + audio, slide by slide)

    python studio.py        # then open http://localhost:8765

- **Slides.** Every narration line is one slide.
  - ← and → move between slides; space plays or pauses.
  - "play slide" plays only that line, with audio, then stops.
  - "play through" keeps going past the end of the slide.
- **Narration tab.** Edit the words of each line, or add and remove pauses.
  Saving writes `narration.json`.
- **Code tab.** The scene's Manim file, opened at its class. Edit it, then save.
- **Rebuild tab.** Runs three steps, then reloads the video:
  1. re-records this scene's voice (optional);
  2. re-renders the scene;
  3. remixes the full video.

The Studio only listens on your own machine (localhost).

## The pieces

| File | What it is |
|---|---|
| `pacing.py` | Scene order (`SCENES`) |
| `narration.json` | Every spoken line, per scene; numbers are pauses in seconds |
| `common.py` | Shared helpers: grid, ants, paths, `DScene` with `cue()` sync |
| `act0_opening.py` … `act9_ending.py` | The scenes |
| `audio/tts.py` | AI narration → `audio/voice/*.wav` + `timing.json` (`--scene X` for one scene) |
| `audio/mix.py` | Voice + sound effects + music → `final_720p30.mp4`, `final_720p30_captioned.mp4`, `captions.srt` |
| `assemble.py` | `chapters.txt` |

**How sync works.** Inside a scene, `self.cue(k)` waits until narration line k
starts. `self.cue_at(k, "word")` waits until that word in the line. So if you
edit a line's words, re-record its voice and the animation follows. Lags are
logged to `logs/cue_lags.json`.

## Using your own voice

Record each scene as `audio/voice/<Scene>.wav`. Then update the line start and
end times in `audio/voice/timing.json`, either by hand or with a Whisper
alignment. After that, re-render the scenes and run the mix. `audio/tts.py`
shows the format.

## VS Code tasks

Open them with Terminal → Run Task. Available tasks:
- Studio
- Render scene (current file)
- Preview scene, low quality
- Re-record voice for one scene
- Re-record ALL narration
- Render ALL scenes
- Mix final video
