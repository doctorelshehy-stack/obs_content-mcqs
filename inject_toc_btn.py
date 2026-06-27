#!/usr/bin/env python3
"""Replace the ← back-to-dashboard button with a 📋 scroll-to-TOC button on the RIGHT side.
Each enhanced file already has a <nav class="toc"> with section links.
This button smoothly scrolls to it.
"""

import os, glob, re

BASE = '/media/mohamed/projects3/projects/obstaric/obs app/enhanced-assets/second task/obstetric'

CSS_SNIPPET = '''
  /* ===== SCROLL TO TABLE OF CONTENTS BUTTON (right side) ===== */
  .scroll-toc-btn {
    position: fixed;
    right: 24px;
    bottom: 80px; /* above the theme toggle */
    z-index: 99999;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: none;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: #ffffff;
    font-size: 20px;
    cursor: pointer;
    box-shadow: 0 4px 16px rgba(37,99,235,0.35);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    text-decoration: none;
    line-height: 1;
    opacity: 0;
    transform: translateY(20px);
    pointer-events: none;
  }
  .scroll-toc-btn.visible {
    opacity: 1;
    transform: translateY(0);
    pointer-events: auto;
  }
  .scroll-toc-btn:hover {
    transform: translateY(-2px) scale(1.08);
    box-shadow: 0 6px 24px rgba(37,99,235,0.5);
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  }
  body.dark .scroll-toc-btn {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    box-shadow: 0 4px 16px rgba(59,130,246,0.3);
  }
  body.dark .scroll-toc-btn:hover {
    box-shadow: 0 6px 24px rgba(59,130,246,0.5);
  }
'''

JS_SNIPPET = '''
  /* Scroll to Table of Contents button */
  (function() {
    var tocBtn = document.getElementById('scrollTocBtn');
    if (!tocBtn) return;

    /* Show button when scrolled past the TOC */
    var tocNav = document.querySelector('nav.toc');
    var checkVisibility = function() {
      if (!tocNav) { tocBtn.classList.add('visible'); return; }
      var rect = tocNav.getBoundingClientRect();
      /* Show button when TOC is above viewport (scrolled past it) */
      if (rect.bottom < 0) {
        tocBtn.classList.add('visible');
      } else {
        tocBtn.classList.remove('visible');
      }
    };
    window.addEventListener('scroll', checkVisibility);
    checkVisibility();

    /* Smooth scroll to TOC on click */
    tocBtn.addEventListener('click', function(e) {
      e.preventDefault();
      if (tocNav) {
        tocNav.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } else {
        /* fallback: scroll to top of page */
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    });
  })();
'''

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html
    changes = []

    # 1. Remove OLD back-content-btn (← button that went to dashboard)
    # Remove the <a> tag
    html = re.sub(r'\s*<a class="back-content-btn"[^>]*>←</a>\s*', '\n', html)
    # Remove the CSS
    html = re.sub(r'/\* ===== BACK TO CONTENT TABLE BUTTON.*?===== \*/.*?(?=\n\s*/\*|</style>)', '', html, flags=re.DOTALL)
    # Clean up any leftover
    html = html.replace('.back-content-btn', '')

    # Clean blank lines
    html = re.sub(r'\n{3,}', '\n\n', html)

    # 2. Add new CSS before </style>
    if '.scroll-toc-btn' not in html:
        html = html.replace('</style>', f'{CSS_SNIPPET}</style>')
        changes.append('added scroll-toc-btn CSS')

    # 3. Add new button HTML after <body> (right before progress-wrap)
    btn_html = '<button class="scroll-toc-btn" id="scrollTocBtn" title="Jump to Table of Contents">📋</button>'
    if 'id="scrollTocBtn"' not in html:
        html = html.replace('<body>', f'<body>\n{btn_html}')
        changes.append('added scroll-toc-btn HTML')

    # 4. Add JS before </body>
    if 'scrollTocBtn' not in html[html.rfind('<script'):]:
        # Find the last </script> before </body> and add after it
        html = html.replace('</body>', f'{JS_SNIPPET}\n</body>')
        changes.append('added scroll-toc-btn JS')

    # 5. Remove any leftover scroll-toc-btn CSS that got duplicated
    # (in case the replace added it twice)
    css_count = html.count(CSS_SNIPPET)
    if css_count > 1:
        html = html.replace(CSS_SNIPPET, '', css_count - 1)
        changes.append('deduplicated CSS')

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return changes
    return []

def main():
    files = glob.glob(os.path.join(BASE, '**/*.html'), recursive=True)
    files.sort()
    updated = 0
    for fp in files:
        changes = process_file(fp)
        if changes:
            rel = os.path.relpath(fp, BASE)
            print(f'✓ {rel}')
            for c in changes:
                print(f'    → {c}')
            updated += 1
    print(f'\nDone. {updated}/{len(files)} files updated.')

if __name__ == '__main__':
    main()
