#!/usr/bin/env bash
# rxz · roblox-thumbnail installer (macOS / Linux / Git Bash)
#   bash install.sh
# Copies this folder to ~/.claude/skills/roblox-thumbnail, backing up an older copy first.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
dst="$HOME/.claude/skills/roblox-thumbnail"

mkdir -p "$(dirname "$dst")"

if [ -d "$dst" ]; then
  stamp="$(date +%Y%m%d-%H%M%S)"
  backup="$HOME/.claude/skills-backup-$stamp-roblox-thumbnail"
  mv "$dst" "$backup"
  echo "  backed up the old copy to $backup"
fi

cp -R "$here" "$dst"
echo "  installed skill roblox-thumbnail -> $dst"

pybin=""
for cand in python3 python py; do
  if command -v "$cand" >/dev/null 2>&1; then
    pybin="$cand"
    "$cand" -c "import PIL" >/dev/null 2>&1 && break
  fi
done
if [ -z "$pybin" ]; then
  echo
  echo "  Python 3 was not found on PATH. Install Python 3.10+ and Pillow."
elif ! "$pybin" -c "import PIL" >/dev/null 2>&1; then
  echo
  echo "  Pillow is missing. Install it with:  $pybin -m pip install pillow"
fi

echo
echo "Done. Restart your agent, then type:  /roblox-thumbnail"
