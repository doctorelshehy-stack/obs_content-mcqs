#!/usr/bin/env python3
"""Clean up the extracted Final 41 questions."""

import re

with open('/tmp/final41.txt', 'r') as f:
    text = f.read()

# Remove form feeds
text = text.replace('\f', '')

lines = text.split('\n')

# First pass: filter out unwanted lines
filtered = []
for line in lines:
    s = line.strip()
    # Skip header/footer
    if s in ['MFM41| Support', 'Written by Mai', '']:
        continue
    if s == 'Final 41 OBS':
        continue
    # Skip Arabic lines (Bismillah, closing duas)
    if re.search(r'[\u0600-\u06FF]', s) and len(s) > 10:
        continue
    filtered.append(line)

# Second pass: join continuation lines
# Lines that end mid-sentence (no punctuation at end, next line continues)
output = []
i = 0
while i < len(filtered):
    line = filtered[i].rstrip()
    s = line.strip()
    
    # Check if next line continues this one
    if i + 1 < len(filtered):
        next_line = filtered[i+1].strip()
        # If next line starts with lowercase or is short continuation
        # and current line doesn't end with sentence-ending punctuation
        if (s and next_line and 
            not s.endswith('.') and not s.endswith('?') and not s.endswith(')') and
            not s.endswith(':') and not s.endswith(';') and
            not s.startswith('- ') and not s.startswith('  ') and
            not next_line.startswith('- ') and not next_line.startswith('  ') and
            not re.match(r'^(Q\d+|I\)|II\)|III\))', s) and
            not re.match(r'^(Q\d+|I\)|II\)|III\))', next_line) and
            not re.match(r'^[A-G]\)', s) and
            not re.match(r'^\d+[\)-]', next_line) and
            len(s) < 80 and len(next_line) < 80):
            # Join with space
            output.append(s + ' ' + next_line)
            i += 2
            continue
    
    # Check if this is a question header line that shouldn't be alone
    q_match = re.match(r'^(Q\d+)\)?\s*\.?\s*(.*)', s)
    if q_match and not q_match.group(2):
        # Q alone on its line, next line has the text
        if i + 1 < len(filtered):
            next_s = filtered[i+1].strip()
            output.append(f'### {q_match.group(1)}. {next_s}')
            i += 2
            continue
    
    output.append(s)
    i += 1

# Third pass: format properly
md = []
md.append('# Final 41 — Obstetrics Exam Questions')
md.append('')
md.append('> Source: Support 41 Final 41 — Written by Mai')
md.append('')
md.append('---')
md.append('')

for line in output:
    if not line:
        md.append('')
        continue
    
    # Section headers
    if re.match(r'^I\) Short essay', line):
        md.append('## I) Short Essay Questions (15 marks)')
        md.append('')
        continue
    elif re.match(r'^II\) Problem solving', line):
        md.append('## II) Problem Solving Questions (20 marks, 5 marks each)')
        md.append('')
        continue
    elif re.match(r'^III\) Family Medicine', line):
        md.append('## III) Family Medicine Questions')
        md.append('')
        continue
    
    # Q8 sub-header
    if 'Extended matching' in line:
        md.append(f'### Q8. Extended Matching Questions (5 marks, 1 mark each)')
        md.append('')
        continue
    
    # Q9 sub-header
    if 'Multiple choice' in line:
        md.append(f'### Q9. Multiple Choice Questions (10 marks, 0.5 mark each)')
        md.append('')
        continue
    
    # Questions (already formatted)
    q_match = re.match(r'^### (Q\d+)\.\s*(.*)', line)
    if q_match:
        md.append(line)
        md.append('')
        continue
    
    # Options A-G)
    opt_match = re.match(r'^([A-G]\))\s*(.*)', line)
    if opt_match:
        md.append(f'- {opt_match.group(1)} {opt_match.group(2)}')
        continue
    
    # Family medicine sub-questions Q1-Q5
    fm_match = re.match(r'^(Q1?\.?)\s*(Enumerate|List|Mariam|What)', line)
    if fm_match:
        md.append(f'### {line}')
        md.append('')
        continue
    
    # Sub-questions like 1., 2., A-, B-
    sub_match = re.match(r'^(\d+)[-\)]\s*(.*)', line)
    if sub_match:
        md.append(f'  {sub_match.group(1)}. {sub_match.group(2)}')
        continue
    
    # Sub-questions like A- B-
    sub_letter = re.match(r'^([A-B])[-\)]\s*(.*)', line)
    if sub_letter:
        md.append(f'  {sub_letter.group(1)}. {sub_letter.group(2)}')
        continue
    
    # Blank lines for answers in matching questions
    if line.strip() == '(................)':
        md.append(f'  > {line.strip()}')
        continue
    
    md.append(line)

md.append('')
md.append('---')
md.append('*Extracted from: support 41 final 41.pdf*')

result = '\n'.join(md)

outpath = '/media/mohamed/projects4/projects/obstaric/obs app/question bank/raw materials/final_41_questions.md'
with open(outpath, 'w') as f:
    f.write(result)

print(f'Written: {outpath}')
print(f'Size: {len(result)} bytes ({len(result)//1024} KB)')
print(f'Lines: {len(md)}')

# Show preview
print('\n=== PREVIEW ===')
preview = '\n'.join(md[:50])
print(preview)
print('...')
