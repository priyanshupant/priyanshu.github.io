#!/bin/bash
# Render every scene as manim-slides (one slide per narration line), then build
# one browser presentation: slides/presentation.html
#   ./render_slides.sh [l|m]      (default m = 720p)
Q=${1:-m}; MANIM=${MANIM:-manim}; MS=${MANIM_SLIDES:-manim-slides}
SC=$(python3 -c "import pacing; print(' '.join(s for f, s, _ in pacing.SCENES))")
python3 -c "import pacing; [print(f, s) for f, s, _ in pacing.SCENES]" |
  xargs -P ${JOBS:-4} -n 2 sh -c "SLIDES=1 $MANIM -q$Q --media_dir media_slides \$0 \$1 > logs/slides_\$1.log 2>&1 && echo done \$1 || echo FAIL \$1"
$MS convert $SC slides/presentation.html --open=false 2>/dev/null || $MS convert $SC slides/presentation.html
echo "open slides/presentation.html  (or: $MS present $SC)"
