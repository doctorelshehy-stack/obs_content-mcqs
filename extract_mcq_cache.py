#!/usr/bin/env python3
"""Extract current MCQ data from enhanced files into JSON files for regeneration."""
import os, re, json

ENH = '/media/mohamed/projects3/projects/obstaric/obs app/enhanced-assets/second task/obstetric'
OUT = '/media/mohamed/projects3/projects/obstaric/obs app/mcq_data_cache'

os.makedirs(OUT, exist_ok=True)

# Robust pattern for <section id="..."> or <section class="..." id="..."> etc
id_pattern = re.compile(r'<(\w+)\s+[^>]*\bid="([^"]*)"')

def extract_mcqs_from_file(filepath):
    """Extract all MCQ data blocks from an enhanced HTML file, grouped by section."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find all sections/divs with IDs
    sections = []
    for m in id_pattern.finditer(html):
        tag = m.group(1)  # section, div, etc.
        if tag not in ('section', 'div'):
            continue
        sec_id = m.group(2)
        h_match = re.search(r'<h[234][^>]*>(.*?)</h[234]>', html[m.start():m.start()+2000])
        heading = re.sub(r'<[^>]+>', '', h_match.group(1)).strip() if h_match else sec_id
        sections.append({'id': sec_id, 'heading': heading, 'start': m.start()})
    
    for i in range(len(sections)):
        end = sections[i+1]['start'] if i+1 < len(sections) else len(html)
        sections[i]['end'] = end
    
    # Extract MCQs from each section
    section_data = {}
    for sec in sections:
        sec_html = html[sec['start']:sec['end']]
        # Find all mcq-block divs
        mcq_blocks = []
        idx = 0
        while True:
            start = sec_html.find('<div class="mcq-block"', idx)
            if start == -1:
                break
            # Find matching closing div
            depth = 1
            pos = start + len('<div class="mcq-block"')
            while depth > 0 and pos < len(sec_html):
                if sec_html[pos:pos+4] == '<div':
                    depth += 1
                    pos += 4
                elif sec_html[pos:pos+6] == '</div>':
                    depth -= 1
                    pos += 6
                else:
                    pos += 1
            block = sec_html[start:pos]
            mcq_blocks.append(block)
            idx = pos
        
        mcqs = []
        for block in mcq_blocks:
            q_match = re.search(r'<div class="mcq-question">(.*?)</div>', block, re.DOTALL)
            if not q_match:
                continue
            q_text = re.sub(r'<[^>]+>', '', q_match.group(1)).strip()
            
            options = []
            correct_idx = -1
            opt_pattern = re.compile(
                r'<label class="mcq-option" data-correct="(true|false)">.*?'
                r'<span class="mcq-text">(.*?)</span>', re.DOTALL)
            for oi, om in enumerate(opt_pattern.finditer(block)):
                is_correct = om.group(1) == 'true'
                opt_text = re.sub(r'<[^>]+>', '', om.group(2)).strip()
                options.append(opt_text)
                if is_correct:
                    correct_idx = oi
            
            explain_match = re.search(
                r'<div class="mcq-explanation"[^>]*>(.*?)</div>', block, re.DOTALL)
            explain = re.sub(r'<[^>]+>', '', explain_match.group(1)).strip() if explain_match else ''
            
            if q_text and options and correct_idx >= 0:
                mcqs.append({
                    'q': q_text,
                    'options': options,
                    'correct': correct_idx,
                    'explain': explain
                })
        
        if mcqs:
            section_data[sec['id']] = mcqs
    
    return section_data

def main():
    count = 0
    for root, dirs, files in os.walk(ENH):
        for f in sorted(files):
            if not f.endswith('.html'):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, ENH)
            
            try:
                data = extract_mcqs_from_file(path)
                if data:
                    key = rel.replace('/', '__').replace('.html', '')
                    outpath = os.path.join(OUT, f'mcq_{key}.json')
                    with open(outpath, 'w', encoding='utf-8') as fout:
                        json.dump(data, fout, indent=2, ensure_ascii=False)
                    count += 1
                    total_mcqs = sum(len(v) for v in data.values())
                    print(f"  {rel}: {total_mcqs} MCQs from {len(data)} sections")
            except Exception as e:
                print(f"  ERROR {rel}: {e}")
    
    print(f"\nDone: extracted {count} files to {OUT}/")

if __name__ == '__main__':
    main()
