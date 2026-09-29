#!/bin/bash
# build.py -> thumb.html -> headless Chrome -> thumb.png, plus a 400x250 card-size proof.
set -e
D="$(cd "$(dirname "$0")" && pwd)"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"

python3 "$D/build.py"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-color-profile=srgb \
  --font-render-hinting=none --disable-lcd-text --no-first-run --virtual-time-budget=4000 \
  --window-size=1600,1000 --screenshot="$D/thumb.png" "file://$D/thumb.html" 2>/dev/null

# The proof is what the blog grid actually shows. Judge legibility here, not on the full render.
python3 - "$D" <<'EOF'
import sys, pathlib
from PIL import Image
d = pathlib.Path(sys.argv[1])
Image.open(d / "thumb.png").resize((400, 250), Image.LANCZOS).save(d / "thumb-at-card-size.png")
print("wrote", d / "thumb.png", "and", d / "thumb-at-card-size.png")
EOF
