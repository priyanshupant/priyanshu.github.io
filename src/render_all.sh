#!/bin/bash
# Render every scene in pacing.SCENES at the given quality (l|m|h), 4 at a time.
Q=${1:-m}
MANIM=${MANIM:-manim}
python3 -c "import pacing; [print(f, s) for f, s, _ in pacing.SCENES]" |
  xargs -P ${JOBS:-4} -n 2 sh -c "$MANIM -q$Q --disable_caching \$0 \$1 > logs/\$1.log 2>&1 && echo done \$1 || echo FAIL \$1"
