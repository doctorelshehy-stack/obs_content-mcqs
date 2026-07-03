#!/usr/bin/env python3
"""
classify_visuals.py — Classify slide images into:
  • completely_text    (text only, no diagrams/figures)
  • completely_visual  (diagram/image only, no meaningful text)
  • hybrid             (text + diagram/image)

Usage:
  python3 classify_visuals.py <png-dir> [--output report.md] [--threshold 0.05]

Output: JSON report + optional markdown summary.
"""

import argparse, json, os, sys, subprocess, tempfile, re
from pathlib import Path
from collections import Counter

# --- venv bootstrap ---
VENV = "/tmp/classify_venv"
if os.path.isdir(VENV):
    py = os.path.join(VENV, "bin", "python3")
    if os.path.isfile(py) and sys.executable != py:
        os.execv(py, [py] + sys.argv)

import cv2
import numpy as np
from PIL import Image
import pytesseract

# ============================================================
#  IMAGE CLASSIFIER
# ============================================================

def estimate_text_ratio(img_array):
    """Return fraction of pixels that belong to text regions."""
    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    # Adaptive threshold to isolate ink/pixels
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 31, 10)
    # Morphology to connect nearby text chars into blocks
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    text_pixels = np.count_nonzero(dilated)
    total_pixels = dilated.size
    return text_pixels / total_pixels if total_pixels else 0.0


def detect_visual_elements(img_array):
    """Detect non-text graphical elements (lines, contours, shapes).
    Returns: (has_lines: bool, contour_count: int, visual_ratio: float)
    """
    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    # Lines (Hough)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80,
                            minLineLength=40, maxLineGap=10)
    has_lines = lines is not None and len(lines) > 5

    # Contours
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 31, 10)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    # Filter small noise contours
    min_area = img_array.shape[0] * img_array.shape[1] * 0.005
    large = [c for c in contours if cv2.contourArea(c) > min_area]
    contour_count = len(large)

    # Edge density
    edge_pixels = np.count_nonzero(edges)
    visual_ratio = edge_pixels / edges.size if edges.size else 0.0
    return has_lines, contour_count, visual_ratio


def has_image_region(img_array):
    """Detect if image contains embedded picture/illustration
    by looking for high-color-variance rectangular regions."""
    h, w = img_array.shape[:2]
    # Check corners (slides usually have text margins)
    # Look for blocks with high color variance (photos/diagrams)
    lab = cv2.cvtColor(img_array, cv2.COLOR_BGR2LAB)
    l_channel = lab[:, :, 0]
    # Divide into grid blocks
    block_h, block_w = h // 8, w // 8
    high_var_blocks = 0
    for r in range(8):
        for c in range(8):
            y1, y2 = r*block_h, (r+1)*block_h
            x1, x2 = c*block_w, (c+1)*block_w
            block = l_channel[y1:y2, x1:x2]
            var = np.var(block)
            if var > 800:  # high variance = likely image content
                high_var_blocks += 1
    return high_var_blocks > 12  # more than ~19% high-var blocks


def has_meaningful_text(img_path):
    """Use tesseract to check if image has meaningful text."""
    try:
        text = pytesseract.image_to_string(
            Image.open(img_path), lang='eng',
            config='--psm 6 --oem 3'
        )
        # Count alphanumeric words (ignore short garbage)
        words = [w for w in text.split() if len(w) > 2 and
                 any(c.isalpha() for c in w)]
        return len(words) >= 3, text.strip()
    except Exception:
        return False, ""


def classify_image(img_path, text_threshold=0.05):
    """Classify a single image into one of three categories."""
    img = cv2.imread(str(img_path))
    if img is None:
        return {"file": Path(img_path).name, "class": "error",
                "reason": "cannot read", "text_ratio": 0.0,
                "text_content": ""}

    text_ratio = estimate_text_ratio(img)
    has_lines, contour_count, visual_ratio = detect_visual_elements(img)
    has_img_region = has_image_region(img)
    has_text, text_content = has_meaningful_text(img_path)

    # --- Classification logic ---
    has_visual = (
        has_lines or
        contour_count > 8 or
        visual_ratio > 0.08 or
        has_img_region
    )

    if has_text and has_visual:
        cls = "hybrid"
        reason_parts = []
        if has_text:
            reason_parts.append("text detected")
        if has_lines:
            reason_parts.append(f"lines({contour_count})")
        if contour_count > 8:
            reason_parts.append(f"contours({contour_count})")
        if visual_ratio > 0.08:
            reason_parts.append(f"edges({visual_ratio:.2%})")
        if has_img_region:
            reason_parts.append("image-region")
        reason = " + ".join(reason_parts)

    elif has_text and not has_visual:
        cls = "completely_text"
        reason = f"text-only ({len(text_content.split())} words)"

    elif has_visual and not has_text:
        cls = "completely_visual"
        reason_parts = ["no-text"]
        if has_lines:
            reason_parts.append("lines")
        if contour_count > 8:
            reason_parts.append(f"contours({contour_count})")
        if has_img_region:
            reason_parts.append("image")
        reason = ", ".join(reason_parts)

    else:
        cls = "completely_text"
        reason = "minimal content (blank?"

    return {
        "file": Path(img_path).name,
        "class": cls,
        "reason": reason,
        "text_ratio": round(text_ratio, 4),
        "contour_count": contour_count,
        "visual_ratio": round(visual_ratio, 4),
        "has_visual_elements": has_visual,
        "text_preview": text_content[:150] if text_content else ""
    }


def generate_markdown(results, image_dir):
    """Generate a human-readable markdown report."""
    lines = []
    counts = Counter(r["class"] for r in results)

    lines.append("# Slide Visual Classification Report\n")
    lines.append(f"**Source:** `{image_dir}`")
    lines.append(f"**Total slides:** {len(results)}\n")
    lines.append("## Summary\n")
    lines.append(f"| Category | Count | % |")
    lines.append(f"|----------|-------|---|")
    for cat in ["completely_text", "completely_visual", "hybrid"]:
        n = counts.get(cat, 0)
        pct = n / len(results) * 100 if results else 0
        lines.append(f"| **{cat}** | {n} | {pct:.0f}% |")
    lines.append("")

    for cat in ["completely_text", "hybrid", "completely_visual"]:
        items = [r for r in results if r["class"] == cat]
        if not items:
            continue
        emoji = {"completely_text": "📄", "completely_visual": "🖼️",
                 "hybrid": "📊"}
        lines.append(f"## {emoji.get(cat, '❓')} {cat} ({len(items)})\n")
        for r in items:
            lines.append(f"- **{r['file']}** — {r['reason']}")
            if r.get("text_preview") and len(r["text_preview"]) > 5:
                lines.append(f"  > {r['text_preview'][:120]}")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Classify slide images into text/visual/hybrid")
    parser.add_argument("image_dir",
                        help="Directory containing PNG/JPG images")
    parser.add_argument("--output", "-o",
                        help="Output markdown report path")
    parser.add_argument("--json", "-j",
                        help="Output JSON report path")
    parser.add_argument("--threshold", type=float, default=0.05,
                        help="Text ratio threshold (default: 0.05)")
    args = parser.parse_args()

    img_dir = Path(args.image_dir)
    if not img_dir.is_dir():
        print(f"❌ Directory not found: {args.image_dir}", file=sys.stderr)
        sys.exit(1)

    # Find images sorted
    images = sorted(img_dir.glob("*.png")) + sorted(img_dir.glob("*.jpg"))
    if not images:
        print(f"❌ No PNG/JPG images found in {args.image_dir}",
              file=sys.stderr)
        sys.exit(1)

    print(f"🔍 Processing {len(images)} images in {args.image_dir}...\n")
    results = []
    for i, img_path in enumerate(images, 1):
        result = classify_image(img_path, args.threshold)
        results.append(result)
        icon = {"completely_text": "📄", "completely_visual": "🖼️",
                "hybrid": "📊", "error": "❌"}
        print(f"  {i:3d}/{len(images)} {icon.get(result['class'], '❓')} "
              f"{result['file']:45s} → {result['class']}")

    # Summary
    counts = Counter(r["class"] for r in results)
    print(f"\n{'='*50}")
    print(f"  📄 completely_text : {counts.get('completely_text', 0)}")
    print(f"  🖼️ completely_visual: {counts.get('completely_visual', 0)}")
    print(f"  📊 hybrid          : {counts.get('hybrid', 0)}")
    print(f"{'='*50}")

    # Save reports
    if args.json:
        with open(args.json, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n✅ JSON report saved to: {args.json}")

    if args.output:
        md = generate_markdown(results, args.image_dir)
        Path(args.output).write_text(md)
        print(f"✅ Markdown report saved to: {args.output}")
        print(md)
    else:
        # Print inline
        print(generate_markdown(results, args.image_dir))


if __name__ == "__main__":
    main()
