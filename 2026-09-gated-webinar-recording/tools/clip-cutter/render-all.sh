#!/bin/zsh
# Cut, brand and contact-sheet every clip in a spec.
# usage: render-all.sh clips.json out/ [extra brand-clip.py args ...]
set -e
here=$(cd "$(dirname "$0")" && pwd)
spec=${1:?clips.json}; out=${2:?out dir}; shift 2
python3 "$here/precise-cuts.py" "$spec"
mkdir -p "$out"
python3 - "$spec" "$out" "$here" "$@" <<'PY'
import json, os, subprocess, sys
spec, out, here, *extra = sys.argv[1:]
work = json.load(open(spec)).get("work", "work")
for c in json.load(open(os.path.join(work, "clips", "manifest.json"))):
    mp4 = os.path.join(out, f"{c['id']}.mp4")
    subprocess.run(["python3", os.path.join(here, "brand-clip.py"), c["file"], c["srt"], mp4,
                    "--title", c["title"], "--speaker", c["speaker"], "--role", c["role"]] + extra, check=True)
    # one PNG per clip: a frame every 5 s, six across, so a whole clip can be checked at a glance
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-vf", "fps=1/5,scale=300:-1,tile=6x4",
                    "-frames:v", "1", os.path.join(out, f"{c['id']}-contact.png")], check=True)
    print("rendered", mp4, "(held for consent)" if c.get("hold_for_consent") else "")
PY
ls -la "$out"/*.mp4
