#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inject progress bar + dark/light toggle into all 54 enhanced HTML files."""

import glob
import re
import os

BASE = "enhanced-assets/second task/obstetric"
files = glob.glob(f"{BASE}/**/*.html", recursive=True)
files.sort()
print(f"Found {len(files)} HTML files")

# ===== CSS to inject (inside <style> block) =====
EXTRA_CSS = """
  /* ===== PROGRESS BAR ===== */
  .progress-wrap {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    z-index: 99999;
    background: transparent;
  }
  .progress-wrap .progress-bar {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #2563eb, #60a5fa);
    transition: width 0.1s ease;
    border-radius: 0 2px 2px 0;
  }

  /* ===== DARK/LIGHT TOGGLE ===== */
  .theme-float {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 99998;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: none;
    background: #ffffff;
    color: #1a202c;
    font-size: 20px;
    cursor: pointer;
    box-shadow: 0 2px 12px rgba(0,0,0,0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.25s ease;
  }
  .theme-float:hover {
    transform: scale(1.1);
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
  }
  body.dark .theme-float {
    background: #1e1e2e;
    color: #fbbf24;
    box-shadow: 0 2px 12px rgba(0,0,0,0.4);
  }

  /* ===== DARK MODE VARIABLES ===== */
  body.dark {
    background: #0f1117;
    color: #e2e8f0;
  }
  body.dark .page {
    background: #1a1b26;
  }
  body.dark .section {
    background: #24253a;
    border-left-color: #60a5fa;
  }
  body.dark .section h2 {
    color: #93c5fd;
    border-bottom-color: #2d3748;
  }
  body.dark .section h3 { color: #60a5fa; }
  body.dark .section h4,
  body.dark .section strong { color: #cbd5e1; }
  body.dark .section p,
  body.dark .section li { color: #cbd5e1; }
  body.dark .topic-header {
    background: linear-gradient(135deg, #0c1e33 0%, #1a365d 60%, #2c5282 100%);
  }
  body.dark .topic-header .eyebrow { color: #90cdf4; }
  body.dark .topic-header .meta { color: #bee3f8; }
  body.dark a { color: #60a5fa; }
  body.dark .footer-note { color: #64748b; border-top-color: #2d3748; }
  body.dark .study-section summary { background: #2d3748; color: #e2e8f0; }
  body.dark .study-section summary:hover { background: #3a4a5e; }
  body.dark .references { background: #1e1e2e; }
  body.dark .references li { color: #a0aec0; }
  body.dark table { background: #1e1e2e; }
  body.dark table th { background: #2d3748; color: #e2e8f0; }
  body.dark table td { border-color: #2d3748; color: #cbd5e1; }
  body.dark table tr:nth-child(even) { background: #24253a; }
  body.dark .hero { background: linear-gradient(135deg, #0c1e33, #1e293b); }
  body.dark .container { background: #1a1b26; }
  body.dark .card,
  body.dark .info-box,
  body.dark .alert-box,
  body.dark .tip-box { background: #24253a; border-color: #2d3748; }
  body.dark .stats-grid .stat-card { background: #24253a; }
  body.dark table caption { color: #94a3b8; }
  body.dark blockquote { border-left-color: #60a5fa; background: #24253a; color: #cbd5e1; }
  body.dark code, body.dark pre { background: #2d3748; color: #e2e8f0; }
}

/* ===== BACK COMPAT - all existing rules below stay ===== */
"""

# ===== HTML to inject after <body> =====
PROGRESS_HTML = """\n<div class="progress-wrap" id="progressWrap">
  <div class="progress-bar" id="progressBar"></div>
</div>
"""

TOGGLE_HTML = """\n<button class="theme-float" id="themeFloatToggle" title="Toggle dark/light mode">\U0001F319</button>
"""

# ===== JS to inject before </body> =====
EXTRA_JS = """
<script>
(function() {
  'use strict';
  /* Progress bar */
  var pb = document.getElementById('progressBar');
  if (pb) {
    window.addEventListener('scroll', function() {
      var dh = document.documentElement.scrollHeight - window.innerHeight;
      var pct = dh > 0 ? (window.scrollY / dh) * 100 : 0;
      pb.style.width = pct + '%';
    });
  }

  /* Dark/Light toggle */
  var toggle = document.getElementById('themeFloatToggle');
  if (toggle) {
    var saved = localStorage.getItem('obstoric-theme');
    if (saved === 'dark') document.body.classList.add('dark');
    if (saved === 'dark') toggle.textContent = '\u2600\uFE0F';

    toggle.addEventListener('click', function() {
      var isDark = document.body.classList.toggle('dark');
      toggle.textContent = isDark ? '\u2600\uFE0F' : '\U0001F319';
      localStorage.setItem('obstoric-theme', isDark ? 'dark' : 'light');
    });
  }
})();
</script>
"""

# ===== Process each file =====
count = 0
for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # Skip if already processed (has the toggle)
    if 'themeFloatToggle' in content:
        print(f"  SKIP (already done): {fpath}")
        continue

    # 1. Inject CSS into <style> block
    style_end = content.rfind('</style>')
    if style_end == -1:
        print(f"  SKIP (no style tag): {fpath}")
        continue

    content = content[:style_end] + '\n' + EXTRA_CSS + content[style_end:]
    modified = True

    # 2. Inject progress bar HTML after <body>
    body_start = re.search(r'<body[^>]*>', content)
    if body_start:
        insert_pos = body_start.end()
        content = content[:insert_pos] + '\n' + PROGRESS_HTML + content[insert_pos:]
        modified = True

    # 3. Inject toggle button after progress bar
    prog_pos = content.find('id="progressWrap"')
    if prog_pos != -1:
        prog_end = content.find('</div>', prog_pos)
        if prog_end != -1:
            content = content[:prog_end+6] + '\n' + TOGGLE_HTML + content[prog_end+6:]
            modified = True

    # 4. Inject JS before </body>
    body_end = content.rfind('</body>')
    if body_end != -1:
        content = content[:body_end] + '\n' + EXTRA_JS + content[body_end:]
        modified = True

    if modified:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"  OK: {os.path.relpath(fpath)}")
    else:
        print(f"  NO CHANGE: {os.path.relpath(fpath)}")

print(f"\nDone! Modified {count} files.")
