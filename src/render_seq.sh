#!/bin/bash
# Render every scene in pacing.SCENES one at a time (no text-cache races). Usage: ./render_seq.sh l|m
Q=${1:-l}; MANIM=${MANIM:-manim}
python3 -c "import pacing; [print(f, s) for f, s, _ in pacing.SCENES]" | while read f s; do
  $MANIM -q$Q --disable_caching $f $s > logs/$s.log 2>&1 && echo "done $s" || echo "FAIL $s"
done
