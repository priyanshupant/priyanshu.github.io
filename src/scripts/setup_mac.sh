#!/bin/bash
# One-time setup on a Mac, then open the Studio (record your voice line by line; Claude edits the same files).
#   bash scripts/setup_mac.sh            # first time: installs everything, builds the video, starts the Studio
#   bash scripts/setup_mac.sh --studio   # later: just start the Studio
# Not yet tested on a real Mac (written in a Linux container); if a step fails, paste the error to Claude.
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="/Library/TeX/texbin:/opt/homebrew/bin:/usr/local/bin:$PATH"

if [ "${1:-}" != "--studio" ]; then
  command -v brew >/dev/null || { echo "Install Homebrew first (https://brew.sh), then run this again."; exit 1; }
  brew install python@3.13 ffmpeg cairo pango pkg-config
  # LaTeX for the formulas (small TeX distribution + the packages Manim uses); asks for your Mac password once
  if ! command -v latex >/dev/null; then brew install --cask basictex; fi
  sudo tlmgr update --self
  sudo tlmgr install standalone preview doublestroke relsize fundus-calligra wasysym physics dvisvgm rsfs wasy \
       cm-super everysel setspace babel-english ragged2e mathastext microtype
  python3.13 -m venv .venv
  .venv/bin/pip install --upgrade pip
  .venv/bin/pip install -r requirements.txt
  .venv/bin/python scripts/fetch_models.py            # the AI voice (about 90 MB)
  mkdir -p logs audio/cues
  .venv/bin/python audio/tts.py                       # voice for every line
  MANIM=.venv/bin/manim JOBS=4 bash render_all.sh m   # render every scene (20-60 minutes the first time)
  .venv/bin/python audio/mix.py 720p30                # the full video with sound
fi
echo "Studio: open http://localhost:8765 in Safari or Chrome (Ctrl+C here to stop)"
MANIM=.venv/bin/manim PYTHON=.venv/bin/python .venv/bin/python studio.py
