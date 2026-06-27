#!/usr/bin/env python3
"""Clean up leftover broken JS from old sidebar-back-btn logic in all 54 files."""

import os, glob, re

BASE = '/media/mohamed/projects3/projects/obstaric/obs app/enhanced-assets/second task/obstetric'

# Pattern for leftover JS (the broken code after </script> and before </body>)
# This matches the specific leftover:
#   /* fallback: navigate parent ... */
#   window.parent...  (indented)
#   } else { ... and the rest of the try/catch block
LEFTiVER_PATTERN = re.compile(
    r'\s*/\* fallback: navigate parent to dashboard \*/.*?'
    r'\}\s*\);\s*'   # closing of addEventListener
    r'\}\s*'          # closing of if(backBtn)
    r'</body>',
    re.DOTALL
)

# Simpler: just find the exact known leftover text and wipe it
LEFTOVER_TEXT = """  /* fallback: navigate parent to dashboard */
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

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html
    changes = []

    # 1. Remove the exact leftover text
    if LEFTOVER_TEXT in html:
        html = html.replace(LEFTOVER_TEXT, '')
        changes.append('removed leftover broken JS near </body>')

    # 2. Remove any orphaned "  /* Sidebar back button */" comments
    html = html.replace("  /* Sidebar back button */", "")
    html = html.replace("  /* Sidebar back button */\n", "")

    # 3. Remove any orphaned "  var backBtn = document.getElementById('sidebarBackBtn');" etc
    html = re.sub(r'\n  var backBtn = document.*?\n', '\n', html)

    # 4. Clean up double blank lines
    html = re.sub(r'\n{3,}', '\n\n', html)

    # 5. Make sure </body> comes right after last </script> or content
    # If there's a gap, trim it
    html = re.sub(r'\n+</body>\n*</html>\s*$', '\n</body>\n</html>\n', html)

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
        changes = clean_file(fp)
        if changes:
            rel = os.path.relpath(fp, BASE)
            print(f'✓ {rel}')
            for c in changes:
                print(f'    → {c}')
            updated += 1
    print(f'\nDone. {updated}/{len(files)} files cleaned.')

if __name__ == '__main__':
    main()
