#!/usr/bin/env python3
"""Replace ☰ hamburger back button with ← single back-to-content-table button.
Also moves it OUTSIDE progress-wrap to avoid z-index/hiding issues.
"""

import os, glob, re

BASE = '/media/mohamed/projects3/projects/obstaric/obs app/enhanced-assets/second task/obstetric'
DASHBOARD_REL = '../../../../../dashboard-enhanced.html'

CSS_SNIPPET = '''
  /* ===== BACK TO CONTENT TABLE BUTTON (standalone, not inside progress-wrap) ===== */
  .back-content-btn {
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 99999;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: none;
    background: rgba(255,255,255,0.92);
    color: #1a202c;
    font-size: 18px;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    backdrop-filter: blur(4px);
    text-decoration: none;
    line-height: 1;
  }
  .back-content-btn:hover {
    background: #ffffff;
    box-shadow: 0 3px 14px rgba(0,0,0,0.2);
    transform: scale(1.1);
  }
  body.dark .back-content-btn {
    background: rgba(30,30,46,0.92);
    color: #e2e8f0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.35);
  }
  body.dark .back-content-btn:hover {
    background: #1e1e2e;
  }
'''

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    changes = []
    
    # 1. Remove OLD sidebar-back-btn CSS
    old_css_pattern = r'/\* ===== SIDEBAR BACK BUTTON ===== \*/.*?(?=</style>)'
    if re.search(old_css_pattern, html, re.DOTALL):
        html = re.sub(old_css_pattern, '', html, flags=re.DOTALL)
        changes.append('removed old sidebar-back-btn CSS')
    
    # 2. Remove OLD sidebar-back-btn HTML element
    old_html_pattern = r'\n?<button class="sidebar-back-btn"[^>]*>.*?</button>\n?'
    if re.search(old_html_pattern, html):
        html = re.sub(old_html_pattern, '', html)
        changes.append('removed old sidebar-back-btn HTML')
    
    # 3. Remove old sidebar-back-btn JS
    old_js_pattern = r'/\* Sidebar back button \*/.*?var backBtn.*?\}\s*\n?'
    if re.search(old_js_pattern, html, re.DOTALL):
        html = re.sub(old_js_pattern, '', html, flags=re.DOTALL)
        changes.append('removed old sidebar-back-btn JS')
    
    # 4. Add NEW CSS before </style>
    css_to_add = CSS_SNIPPET
    if '.back-content-btn' not in html:
        html = html.replace('</style>', f'{css_to_add}</style>')
        changes.append('added back-content-btn CSS')
    
    # 5. Add NEW button HTML after <body> (outside progress-wrap)
    btn_html = f'<a class="back-content-btn" id="backContentBtn" href="{DASHBOARD_REL}" title="Back to content table (Dashboard)">←</a>'
    if 'id="backContentBtn"' not in html:
        # Put it right after <body> but before progress-wrap
        html = html.replace('<body>', f'<body>\n{btn_html}')
        changes.append('added back-content-btn HTML')
    
    # 6. Remove old JS that was specifically for sidebar-back-btn (already done in step 3)
    #    Also check if there's any reference to sidebarBackBtn in the dark mode / progress JS
    html = html.replace("/* Sidebar back button */", "")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return changes

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
