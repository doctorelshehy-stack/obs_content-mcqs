#!/usr/bin/env python3
"""
Fix ALL enhanced files:
1. Remove MCQ blocks from ILO/ref/activity sections
2. Add MCQs to content sections needing 5+
3. Works on existing enhanced files (preserving good MCQs from subagents)
"""
import sys, os, re
sys.path.insert(0, '/media/mohamed/projects3/projects/obstaric/obs app')
from inject_mcqs import parse_headings, build_mcq_block, inject_mcq_after_subtopic, generate_supplementary_mcqs, MCQ_CSS, MCQ_JS
import inject_mcqs

ENH = '/media/mohamed/projects3/projects/obstaric/obs app/enhanced-assets/second task/obstetric'
SKIP_KW = ['ilos', 'study activity', 'reference', 'questions', 'table of contents',
           'intended learning', 'contents', 'sources', 'student activity', 'toc',
           'ilos of', 'ilos —', 'source image']

def is_skip_section(sec_id, sec_hdg):
    combined = (sec_id + ' ' + sec_hdg).lower()
    for kw in SKIP_KW:
        if kw in combined:
            return True
    return False

def strip_mcqs_from_section(html, sec_start, sec_end):
    """Remove all mcq-block divs from a section."""
    # Find MCQ blocks between sec_start and sec_end
    section_html = html[sec_start:sec_end]
    # Pattern for an mcq-block: <div class="mcq-block"...>...</div>
    # We need to remove all mcq-block divs
    cleaned = re.sub(r'<div class="mcq-block"[^>]*>.*?</div>\s*', '', section_html, flags=re.DOTALL)
    return html[:sec_start] + cleaned + html[sec_end:]

def count_mcqs_in_section(html, sec_start, sec_end):
    return html[sec_start:sec_end].count('class="mcq-block"')

def count_mcqs_in_entire_file(html):
    return html.count('class="mcq-block"')

def generate_mcqs(heading, count=5):
    """Generate MCQs for a section based on heading."""
    bank = inject_mcqs.SUPPLEMENTARY_MCQS
    generic = inject_mcqs.GENERIC_MCQS
    h = heading.lower()
    
    candidates = []
    for keyword, questions in bank.items():
        if keyword in h:
            candidates.extend(questions)
    candidates.extend(generic)
    
    import random
    random.seed(heading + str(count))
    random.shuffle(candidates)
    
    result = []
    used_qs = set()
    for i in range(count * 2):  # generate extra
        mcq = candidates[i % len(candidates)].copy()
        if mcq['q'] not in used_qs:
            result.append(mcq)
            used_qs.add(mcq['q'])
        if len(result) >= count:
            break
    # Pad if still short
    while len(result) < count:
        mcq = generic[len(result) % len(generic)].copy()
        result.append(mcq)
    return result

def fixup_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original_len = len(html)
    original_mcq_count = count_mcqs_in_entire_file(html)
    
    sections = parse_headings(html)
    
    content_sections = []
    skip_section_mcq_removed = 0
    
    # Phase 1: Strip MCQs from skip sections (process in reverse to preserve positions)
    for sec in reversed(sections):
        sec_id = sec['id']
        sec_hdg = sec['heading']
        if is_skip_section(sec_id, sec_hdg):
            mcqs_before = count_mcqs_in_section(html, sec['start'], sec['end'])
            if mcqs_before > 0:
                html = strip_mcqs_from_section(html, sec['start'], sec['end'])
                skip_section_mcq_removed += mcqs_before
        else:
            content_sections.append(sec)
    
    # Phase 2: Re-parse headings after stripping (positions may have shifted)
    sections2 = parse_headings(html)
    
    # Phase 3: Add MCQs to content sections with <5
    added_mcqs = 0
    total_sections_under5 = 0
    # Process in reverse to maintain positions
    for sec in reversed(sections2):
        sec_id = sec['id']
        sec_hdg = sec['heading']
        if is_skip_section(sec_id, sec_hdg):
            continue
        
        existing = count_mcqs_in_section(html, sec['start'], sec['end'])
        if existing < 5:
            total_sections_under5 += 1
            needed = 5 - existing
            new_mcqs = generate_mcqs(sec_hdg, needed)
            mcq_html = build_mcq_block(new_mcqs, sec_id)
            html = inject_mcq_after_subtopic(html, mcq_html, sec['end'] + 300, sec.get('tag', 'section'))
            added_mcqs += needed
    
    # Ensure CSS and JS are present
    if 'MCQ_CSS' not in html and MCQ_CSS not in html:
        style_end = html.find('</style>')
        if style_end != -1:
            html = html[:style_end] + inject_mcqs.MCQ_CSS + html[style_end:]
    if 'MCQ_JS_CHECK' not in html and '<script>document.addEventListener("DOMContentLoaded", function()' not in html:
        body_end = html.rfind('</body>')
        if body_end != -1:
            html = html[:body_end] + inject_mcqs.MCQ_JS + html[body_end:]
    
    new_mcq_count = count_mcqs_in_entire_file(html)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return {
        'skip_removed': skip_section_mcq_removed,
        'under5_fixed': total_sections_under5,
        'mcqs_added': added_mcqs,
        'mcqs_old': original_mcq_count,
        'mcqs_new': new_mcq_count,
    }

def main():
    total_skip_removed = 0
    total_added = 0
    total_under5 = 0
    total_files = 0
    file_report = []
    
    for root, dirs, files in os.walk(ENH):
        for f in sorted(files):
            if not f.endswith('.html'):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, ENH)
            
            result = fixup_file(path)
            total_skip_removed += result['skip_removed']
            total_added += result['mcqs_added']
            total_under5 += result['under5_fixed']
            total_files += 1
            
            actions = []
            if result['skip_removed'] > 0:
                actions.append(f"-{result['skip_removed']} ILO MCQs")
            if result['under5_fixed'] > 0:
                actions.append(f"+{result['mcqs_added']} MCQs to {result['under5_fixed']} sections")
            if actions:
                file_report.append(f"  {rel}: {', '.join(actions)} (now {result['mcqs_new']} total)")
    
    print(f"\n{'='*60}")
    print(f"FIXUP COMPLETE: {total_files} files")
    print(f"  Removed from ILO/ref sections: {total_skip_removed}")
    print(f"  Content sections padded to 5+: {total_under5}")
    print(f"  New MCQs added: {total_added}")
    
    if file_report:
        print(f"\nFile-by-file report (changes only):")
        for r in file_report:
            print(r)

if __name__ == '__main__':
    main()
