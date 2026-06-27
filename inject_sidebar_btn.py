#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add sidebar-back button to all 54 enhanced HTML files.
Clicking it opens the parent dashboard sidebar (if in iframe) or goes to dashboard-enhanced.html."""

import glob
import re
import os

BASE = "enhanced-assets/second task/obstetric"
files = glob.glob(f"{BASE}/**/*.html", recursive=True)
files.sort()
print(f"Found {len(files)} HTML files")

# ===== CSS for the sidebar-back button =====
BACK_BTN_CSS = """
  /* ===== SIDEBAR BACK BUTTON ===== */
  .sidebar-back-btn {
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 99997;
    width: 36px;
    height: 36px;
    border-radius: 8px;
    border: none;
    background: rgba(255,255,255,0.9);
    color: #1a202c;
    font-size: 16px;
    cursor: pointer;
    box-shadow: 0 1px 6px rgba(0,0,0,0.12);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    backdrop-filter: blur(4px);
  }
  .sidebar-back-btn:hover {
    background: #ffffff;
    box-shadow: 0 2px 12px rgba(0,0,0,0.18);
    transform: scale(1.05);
  }
  body.dark .sidebar-back-btn {
    background: rgba(30,30,46,0.9);
    color: #e2e8f0;
    box-shadow: 0 1px 6px rgba(0,0,0,0.3);
  }
  body.dark .sidebar-back-btn:hover {
    background: #1e1e2e;
  }
"""

# ===== HTML for the button =====
BACK_BTN_HTML = """\n<button class="sidebar-back-btn" id="sidebarBackBtn" title="Back to dashboard / Open sidebar">\u2630</button>
"""

# ===== JS for the button =====
BACK_BTN_JS = """
  /* Sidebar back button */
  var backBtn = document.getElementById('sidebarBackBtn');
  if (backBtn) {
    backBtn.addEventListener('click', function() {
      try {
        if (window.parent && window.parent !== window) {
          /* Inside iframe -- try to open parent sidebar */
          var pBtn = window.parent.document.getElementById('sidebarToggleBtn')
                 || window.parent.document.getElementById('sidebarCollapseBtn');
          if (pBtn) { pBtn.click(); return; }
          /* fallback: navigate parent to dashboard */
          window.parent.location.href = 'dashboard-enhanced.html';
        } else {
          /* Direct load -- go to dashboard */
          window.location.href = '../../../../../dashboard-enhanced.html';
        }
      } catch(e) {
        /* Cross-origin or error fallback */
        window.location.href = '../../../../../dashboard-enhanced.html';
      }
    });
  }
"""

count = 0
for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has the button
    if 'sidebarBackBtn' in content:
        print(f"  SKIP (already done): {os.path.relpath(fpath)}")
        continue

    modified = False

    # 1. Inject CSS before </style>
    style_end = content.rfind('</style>')
    if style_end == -1:
        print(f"  SKIP (no style tag): {os.path.relpath(fpath)}")
        continue
    content = content[:style_end] + '\n' + BACK_BTN_CSS + content[style_end:]
    modified = True

    # 2. Inject button HTML near the progress bar (after theme toggle or progress bar)
    # Find the progress-wrap div and add the button right after it
    prog_pos = content.find('id="progressWrap"')
    if prog_pos != -1:
        # Find the closing </div> of progressWrap, then insert after it (before theme toggle)
        prog_close = content.find('</div>', prog_pos)
        if prog_close != -1:
            # Find the next newline after </div>
            nl = content.find('\n', prog_close)
            insert_at = nl + 1 if nl != -1 else prog_close + 6
            # Before the theme toggle
            toggle_pos = content.find('id="themeFloatToggle"')
            if toggle_pos != -1 and toggle_pos < insert_at:
                insert_at = content.rfind('\n', 0, toggle_pos) + 1
            content = content[:insert_at] + BACK_BTN_HTML + content[insert_at:]
            modified = True

    # 3. Inject JS before </body>
    body_end = content.rfind('</body>')
    if body_end != -1:
        # Insert before the last <script> block (before </body>)
        # Find the last </script> and insert after it
        last_script = content.rfind('</script>')
        if last_script != -1 and last_script < body_end:
            insert_pos = content.find('\n', last_script)
            if insert_pos != -1:
                content = content[:insert_pos+1] + BACK_BTN_JS + content[insert_pos+1:]
            else:
                content = content[:last_script+9] + '\n' + BACK_BTN_JS + content[last_script+9:]
        else:
            content = content[:body_end] + '\n' + BACK_BTN_JS + content[body_end:]
        modified = True

    if modified:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"  OK: {os.path.relpath(fpath)}")
    else:
        print(f"  NO CHANGE: {os.path.relpath(fpath)}")

print(f"\nDone! Modified {count} files.")
