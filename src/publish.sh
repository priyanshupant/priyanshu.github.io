#!/bin/bash
# Update the public site (presenter view, slide deck, article, video) after edits.
#   ./publish.sh                 # slides + article only
#   ./publish.sh --voice Hook    # also re-record Hook's voice first
#   ./publish.sh --video         # also re-render the voiced video and re-mix it
# SITE = local clone of github.com/priyanshupant/priyanshu.github.io
set -e
SITE=${SITE:-../priyanshu.github.io}
PY=${PY:-python3}
while [ $# -gt 0 ]; do
  case $1 in
    --voice) $PY audio/tts.py --scene "$2"; shift 2 ;;
    --video) VIDEO=1; shift ;;
    *) echo "unknown option $1"; exit 1 ;;
  esac
done
bash render_slides.sh m                                   # manim-slides deck (one slide per narration line)
if [ -n "$VIDEO" ]; then bash render_all.sh m; $PY audio/mix.py 720p30; fi   # timed, voiced film
NO_MUSIC=1 $PY audio/mix.py 720p30                        # voice + effects only, for the presenter clips
$PY research/build_present.py "$SITE/determinants"        # presenter view (voiced clip per line) + deck
$PY research/article.py && cp article/index.html "$SITE/determinants/index.html"
if [ -n "$VIDEO" ]; then
  cp final_720p30_captioned.mp4 "$SITE/determinants/video.mp4"; cp captions.srt "$SITE/determinants/"
fi
cd "$SITE" && git add -A && git commit -q -m "Update determinants video pages" && git push origin main
echo "Pushed. Live in about a minute at https://priyanshupant.github.io/priyanshu.github.io/determinants/present.html"
