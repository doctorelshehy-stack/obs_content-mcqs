#!/usr/bin/env python3
"""
FINAL regeneration from originals using cached MCQ data.
Preserves all good subagent MCQs, pads to 5, skips ILO/ref sections.
"""
import os, sys, re, json, glob

sys.path.insert(0, '/media/mohamed/projects3/projects/obstaric/obs app')
from inject_mcqs import process_file, parse_headings, generate_supplementary_mcqs
import inject_mcqs

ROOT = '/media/mohamed/projects3/projects/obstaric/obs app'
ORIG = os.path.join(ROOT, 'extracted/assets/second task/obstetric')
ENH = os.path.join(ROOT, 'enhanced-assets/second task/obstetric')
CACHE = os.path.join(ROOT, 'mcq_data_cache')

SKIP_KW = ['ilos', 'study activity', 'reference', 'questions', 'table of contents',
           'intended learning', 'contents', 'sources', 'student activity', 'toc',
           'ilos of', 'ilos —', 'student-activity', 'source image']

def is_skip(sec_id, sec_hdg):
    c = (sec_id + ' ' + sec_hdg).lower()
    return any(kw in c for kw in SKIP_KW)

def generate_mcqs_bank(heading, count=5):
    """Generate count MCQs from heading-based bank + generic fallback."""
    h = heading.lower()
    bank = inject_mcqs.SUPPLEMENTARY_MCQS
    generic = inject_mcqs.GENERIC_MCQS
    
    candidates = []
    for kw, qs in bank.items():
        if kw in h:
            candidates.extend(qs)
    candidates.extend(generic)
    
    import random
    random.seed(heading + str(count))
    random.shuffle(candidates)
    
    result = []
    used = set()
    for i in range(count * 3):
        mcq = candidates[i % len(candidates)].copy()
        if mcq['q'] not in used:
            result.append(mcq)
            used.add(mcq['q'])
        if len(result) >= count:
            break
    while len(result) < count:
        mcq = generic[len(result) % len(generic)].copy()
        result.append(mcq)
    return result

def pad_to_5(existing_mcqs, heading):
    """Pad existing MCQs to at least 5, generating extras from heading."""
    if len(existing_mcqs) >= 5:
        return existing_mcqs[:5]
    needed = 5 - len(existing_mcqs)
    extras = generate_mcqs_bank(heading, needed)
    return existing_mcqs + extras

def process_one_file(orig_path, enh_path, cached_data):
    with open(orig_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    sections = parse_headings(html)
    content_sections = [s for s in sections if not is_skip(s['id'], s['heading'])]
    
    # Build MCQ data dict
    mcq_data = {}
    for sec in content_sections:
        sec_id = sec['id']
        heading = sec['heading']
        
        # Check cache first
        cached = cached_data.get(sec_id) if cached_data else None
        if cached:
            mcq_data[sec_id] = pad_to_5(cached, heading)
        else:
            # No cached data — generate fresh
            mcq_data[sec_id] = generate_mcqs_bank(heading, 5)
    
    # Process
    os.makedirs(os.path.dirname(enh_path), exist_ok=True)
    process_file(orig_path, enh_path, mcq_data, min_mcqs=5)

def main():
    # Load cached data
    cache_by_rel = {}
    for cfile in glob.glob(os.path.join(CACHE, 'mcq_*.json')):
        key = os.path.basename(cfile).replace('mcq_', '').replace('.json', '')
        with open(cfile, 'r') as f:
            data = json.load(f)
        cache_by_rel[key] = data
    
    weeks = ['Week1', 'Week2', 'Week3', 'Week5']
    total = 0
    
    for week in weeks:
        orig_dir = os.path.join(ORIG, week)
        for root, dirs, files in os.walk(orig_dir):
            for f in sorted(files):
                if not f.endswith('.html'):
                    continue
                orig_path = os.path.join(root, f)
                rel = os.path.relpath(orig_path, ORIG)
                enh_path = os.path.join(ENH, rel)
                
                # Look up cache
                cache_key = rel.replace('/', '__').replace('.html', '')
                cached = cache_by_rel.get(cache_key)
                
                process_one_file(orig_path, enh_path, cached)
                
                # Quick verify
                with open(enh_path) as vf:
                    vhtml = vf.read()
                mcq_count = vhtml.count('class="mcq-block"')
                
                total += 1
                cache_status = "cached" if cached else "generated"
                print(f"  {rel}: {mcq_count} MCQs ({cache_status})")
    
    print(f"\n{'='*60}")
    print(f"DONE: {total} files regenerated from originals")

if __name__ == '__main__':
    main()
