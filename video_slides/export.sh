#!/bin/sh
# Chrome(Chromium)のheadlessモードで slides.html を1枚ずつPNGに書き出す
# 使い方: sh export.sh   （CHROME=ブラウザのパス で変更可）
cd "$(dirname "$0")"
CHROME="${CHROME:-$(command -v google-chrome || command -v chromium || echo /opt/pw-browsers/chromium-1194/chrome-linux/chrome)}"
for i in 1 2 3 4 5 6; do
  out=$(printf "scene_%02d.png" "$i")
  "$CHROME" --headless --no-sandbox --disable-gpu --hide-scrollbars \
    --window-size=1920,1080 --force-device-scale-factor=1 \
    --virtual-time-budget=2000 \
    --screenshot="$PWD/$out" "file://$PWD/slides.html#$i" 2>/dev/null
  echo "$out"
done
