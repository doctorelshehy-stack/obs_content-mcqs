#!/usr/bin/env python3
"""Analyze MCQ distribution across all enhanced files."""
import os, re

ENH = "/media/mohamed/projects3/projects/obstaric/obs app/enhanced-assets/second task/obstetric"

skip_keywords = ['ilo', 'study activity', 'reference', 'questions', 'table of contents',
                 'intended learning', 'contents', 'sources', 'student activity', 'toc']

def analyze_file(filepath):
    """Return list of sections with MCQ counts and status."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find all sections
    pattern = re.compile(r'<(section|div)(?:\s+class="[^"]*")?\s+id="([^"]*)"(?:\s+class="[^"]*")?>')
    sections = []
    for m in pattern.finditer(html):
        tag_start = m.start()
        sec_id = m.group(2)
        h_match = re.search(r'<h[234][^>]*>(.*?)</h[234]>', html[m.start():m.start()+2000])
        heading = h_match.group(1) if h_match else sec_id
        heading = re.sub(r'<[^>]+>', '', heading).strip()
        
        # Count MCQs in this section
        end = len(html)
        sections.append({'id': sec_id, 'heading': heading, 'start': tag_start})
    
    # Set ends
    for i in range(len(sections)):
        end = sections[i+1]['start'] if i+1 < len(sections) else len(html)
        sec_html = html[sections[i]['start']:end]
        sections[i]['mcq_count'] = sec_html.count('class="mcq-block"')
        sections[i]['end'] = end
        
        sec_id_lower = sections[i]['id'].lower()
        sec_hdg_lower = sections[i]['heading'].lower()
        sections[i]['is_skip'] = any(kw in sec_id_lower or kw in sec_hdg_lower for kw in skip_keywords)
        sections[i]['needs_fix'] = (sections[i]['is_skip'] and sections[i]['mcq_count'] > 0) or \
                                   (not sections[i]['is_skip'] and sections[i]['mcq_count'] < 5)
    
    return sections

# Walk all files
issues = []
for root, dirs, files in os.walk(ENH):
    for f in sorted(files):
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        rel = os.path.relpath(path, ENH)
        secs = analyze_file(path)
        
        has_issue = any(s['needs_fix'] for s in secs)
        if has_issue:
            content_issues = []
            skip_issues = []
            for s in secs:
                if s['is_skip'] and s['mcq_count'] > 0:
                    skip_issues.append(f"    [{s['id']}] '{s['heading'][:40]}' → HAS {s['mcq_count']} MCQs (should be 0)")
                elif not s['is_skip'] and s['mcq_count'] < 5:
                    content_issues.append(f"    [{s['id']}] '{s['heading'][:40]}' → {s['mcq_count']}/5+ MCQs")
            
            if skip_issues:
                print(f"\n=== {rel} ===")
                print(f"  SECTIONS TO STRIP MCQs FROM:")
                for line in skip_issues:
                    print(line)
            if content_issues:
                print(f"\n=== {rel} ===")
                print(f"  SECTIONS NEEDING MORE MCQs:")
                for line in content_issues:
                    print(line)
            
            issues.append({'file': rel, 'skip': skip_issues, 'content': content_issues})

print(f"\n\n{'='*60}")
print(f"SUMMARY: {len(issues)} files with issues")
total_skip = sum(len(i['skip']) for i in issues)
total_content = sum(len(i['content']) for i in issues)
print(f"  {total_skip} sections to strip MCQs from")
print(f"  {total_content} sections needing 5+ MCQs")
