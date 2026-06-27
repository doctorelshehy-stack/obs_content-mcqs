#!/usr/bin/env python3
"""Add a ⬆ TOC button inside the existing topic-navigation bar (like Back & Home).
Remove the floating 📋 scroll-toc-btn on the right side.
"""

import os, glob, re

BASE = '/media/mohamed/projects3/projects/obstaric/obs app/enhanced-assets/second task/obstetric'

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html
    changes = []

    # 1. Remove floating 📋 scroll-toc-btn HTML
    html = re.sub(r'\s*<button class="scroll-toc-btn"[^>]*>📋</button>\s*', '\n', html)

    # 2. Remove floating scroll-toc-btn CSS block (everything from the comment to </style> or next comment)
    html = re.sub(
        r'/\* ===== SCROLL TO TABLE OF CONTENTS BUTTON.*?===== \*/.*?(?=\n\s*/\*|\n</style>)',
        '',
        html,
        flags=re.DOTALL
    )

    # 3. Remove scroll-toc-btn JS block (simple search-and-delete)
    js_start = '/* Scroll to Table of Contents button */'
    js_end = '})();'
    while True:
        start_idx = html.find(js_start)
        if start_idx == -1:
            break
        end_idx = html.find(js_end, start_idx)
        if end_idx == -1:
            break
        html = html[:start_idx] + html[end_idx + len(js_end):]
        changes.append('removed old scroll-toc-btn JS')

    # 4. Add ⬆ TOC button inside topic-navigation (before </nav> but after existing items)
    toc_btn = '<a href="#" onclick="document.querySelector(\'nav.toc\')?.scrollIntoView({behavior:\'smooth\',block:\'start\'}) || window.scrollTo({top:0,behavior:\'smooth\'}); return false;" title="Go to Table of Contents">⬆ TOC</a>'
    
    if '⬆ TOC' not in html:
        # Insert before </nav>
        html = html.replace('</nav>', f'{toc_btn}\n</nav>')
        changes.append('added ⬆ TOC button to topic-navigation')
    
    # 5. If topic-navigation nav still has position: sticky, keep it as is (user said "like them")

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
