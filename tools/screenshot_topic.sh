#!/bin/bash
# Batch screenshot all slides for a topic, then auto-classify visuals
# Usage: ./screenshot_topic.sh <slides_dir> <output_dir>

SLIDES_DIR="$1"
OUTPUT_DIR="$2"
mkdir -p "$OUTPUT_DIR"

for f in "$SLIDES_DIR"/slide_*.html; do
  num=$(basename "$f" .html | sed 's/slide_//')
  out="$OUTPUT_DIR/slide_${num}.png"
  if [ -f "$out" ]; then
    echo "SKIP slide_${num}.png (exists)"
  else
    google-chrome --headless --window-size=1280,720 \
      --screenshot="$out" \
      --default-background-color=000000 \
      "$f" 2>/dev/null
    echo "DONE slide_${num}.png"
  fi
done

echo "=== All done ==="

# Auto-classify visuals
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/classify_visuals.py" "$OUTPUT_DIR" --output "$OUTPUT_DIR/../visuals_report.md" 2>/dev/null || true
echo "=== Visual classification done ==="
