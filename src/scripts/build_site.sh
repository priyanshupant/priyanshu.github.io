#!/bin/bash
# Full build: voice -> timed render -> mixes -> manim-slides -> presenter clips -> article.
# Writes the published files into $SITE/determinants (default: the parent repo).
#   bash scripts/build_site.sh
set -euo pipefail
cd "$(dirname "$0")/.."
SITE=${SITE:-..}
PY=${PY:-python3}
export MANIM=${MANIM:-manim} MANIM_SLIDES=${MANIM_SLIDES:-manim-slides}
mkdir -p logs audio/cues article "$SITE/determinants"

$PY scripts/fetch_models.py
$PY audio/tts.py

retry_failed() {   # parallel renders can race on Manim's text cache: redo failures one at a time
  local out=$1 mode=$2
  grep '^FAIL' "$out" | awk '{print $2}' | while read -r sc; do
    f=$($PY -c "import pacing; print(next(f for f, s, _ in pacing.SCENES if s == '$sc'))")
    echo "retrying $sc"
    if [ "$mode" = slides ]; then SLIDES=1 $MANIM -qm --media_dir media_slides "$f" "$sc"; else SFX_LOG=$PWD/audio/cues $MANIM -qm --disable_caching "$f" "$sc"; fi
  done
}

SFX_LOG=$PWD/audio/cues JOBS=${JOBS:-4} bash render_all.sh m | tee logs/render_all.out
retry_failed logs/render_all.out video
$PY audio/mix.py 720p30
NO_MUSIC=1 $PY audio/mix.py 720p30

JOBS=${JOBS:-4} bash render_slides.sh m | tee logs/render_slides.out
if grep -q '^FAIL' logs/render_slides.out; then
  retry_failed logs/render_slides.out slides
  SC=$($PY -c "import pacing; print(' '.join(s for f, s, _ in pacing.SCENES))")
  $MANIM_SLIDES convert $SC slides/presentation.html
fi

$PY research/build_present.py "$SITE/determinants"
$PY - <<'PYEOF'
import json, subprocess, pacing
d = {sc: float(subprocess.check_output(["ffprobe", "-v", "0", "-show_entries", "format=duration", "-of", "csv=p=0",
                                        f"media/videos/{f[:-3]}/720p30/{sc}.mp4"])) for f, sc, _ in pacing.SCENES}
json.dump(d, open("article/scene_durations.json", "w"))
PYEOF
$PY research/article.py
cp article/index.html "$SITE/determinants/index.html"
cp final_720p30_captioned.mp4 "$SITE/determinants/video.mp4"
cp captions.srt "$SITE/determinants/captions.srt"
$PY assemble.py 720p30 --chapters-only >/dev/null && cp chapters.txt "$SITE/determinants/chapters.txt"
echo "build complete"
