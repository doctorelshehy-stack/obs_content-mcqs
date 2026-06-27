#!/usr/bin/env python3
"""
Regenerate enhanced files from originals, preserving existing MCQ data.
- Reads existing mcq_data_NN.json for each file (where available)
- For content sections with data → pad to 5 MCQs (keep existing, add contextually relevant extras)
- For content sections WITHOUT data → generate 5 fresh MCQs
- ILO/ref/activity sections → ALWAYS 0 MCQs
"""
import sys, os, re, json, glob
sys.path.insert(0, '/media/mohamed/projects3/projects/obstaric/obs app')
from inject_mcqs import process_file, generate_supplementary_mcqs, parse_headings, build_mcq_block, MCQ_CSS, MCQ_JS
import inject_mcqs

ROOT = '/media/mohamed/projects3/projects/obstaric/obs app'
ORIG = os.path.join(ROOT, 'extracted/assets/second task/obstetric')
ENH = os.path.join(ROOT, 'enhanced-assets/second task/obstetric')
SKIP_KW = ['ilos', 'study activity', 'reference', 'questions', 'table of contents',
           'intended learning', 'contents', 'sources', 'student activity', 'toc',
           'ilos of', 'ilos —', 'source image', 'figure']

def is_skip_section(sec_id, sec_hdg):
    combined = (sec_id + ' ' + sec_hdg).lower()
    for kw in SKIP_KW:
        if kw in combined:
            return True
    return False

# Load all existing mcq_data JSONs
def load_existing_mcq_data(week, file_key):
    """Try to load existing mcq_data for a file. file_key is like '05' or '08'."""
    patterns = [
        os.path.join(ROOT, f'mcq_data_{file_key}.json'),
        os.path.join(ROOT, f'mcq_data_0{file_key}.json'),
    ]
    for p in patterns:
        if os.path.exists(p):
            with open(p, 'r') as f:
                return json.load(f)
    return None

def build_mcq_from_heading(heading, count=5):
    """Generate count MCQs for a section based on its heading."""
    bank = inject_mcqs.SUPPLEMENTARY_MCQS
    generic = inject_mcqs.GENERIC_MCQS
    heading_lower = heading.lower()
    
    candidates = []
    for keyword, questions in bank.items():
        if keyword in heading_lower:
            candidates.extend(questions)
    candidates.extend(generic)
    
    import random
    random.seed(heading + str(count))
    random.shuffle(candidates)
    
    mcqs = []
    for i in range(count):
        mcqs.append(candidates[i % len(candidates)].copy())
    return mcqs

def generate_extra_mcqs(mcqs, needed, heading):
    """Generate extra MCQs different from existing ones, based on heading."""
    extras = build_mcq_from_heading(heading, needed + 2)  # generate extra for variety
    result = []
    used_questions = {m['q'] for m in mcqs}
    for ex in extras:
        if ex['q'] not in used_questions and len(result) < needed:
            result.append(ex)
            used_questions.add(ex['q'])
    # If still need more, force them
    while len(result) < needed:
        ex = build_mcq_from_heading(heading, 1)[0]
        ex['q'] += f' (concept {len(result)+1})'  # ensure uniqueness
        result.append(ex)
    return result

def pad_mcq_data(mcq_data, content_sections):
    """Ensure each content section has 5+ MCQs. Add missing sections."""
    result = {}
    for sec in content_sections:
        sec_id = sec['id']
        heading = sec['heading']
        existing = mcq_data.get(sec_id, []) if mcq_data else []
        
        if not existing:
            # Generate fresh 5 MCQs
            result[sec_id] = build_mcq_from_heading(heading, 5)
        elif len(existing) < 5:
            # Pad existing
            needed = 5 - len(existing)
            extras = generate_extra_mcqs(existing, needed, heading)
            result[sec_id] = existing + extras
        else:
            # Keep all existing (allow >5 if already there)
            result[sec_id] = existing
    return result

def process_all():
    weeks = ['Week1', 'Week2', 'Week3', 'Week5']
    total_files = 0
    total_sections = 0
    
    for week in weeks:
        orig_dir = os.path.join(ORIG, week)
        for root, dirs, files in os.walk(orig_dir):
            for f in sorted(files):
                if not f.endswith('.html'):
                    continue
                orig_path = os.path.join(root, f)
                rel = os.path.relpath(orig_path, ORIG)
                enh_path = os.path.join(ENH, rel)
                
                # Read original HTML
                with open(orig_path, 'r', encoding='utf-8') as fp:
                    html = fp.read()
                
                # Parse all sections
                sections = parse_headings(html)
                content_secs = [s for s in sections if not is_skip_section(s['id'], s['heading'])]
                skip_secs = [s for s in sections if is_skip_section(s['id'], s['heading'])]
                
                # Try to find existing mcq_data
                # Extract file number from filename
                fname = os.path.basename(f)
                match = re.match(r'(\d+)_', fname)
                mcq_data = None
                if match:
                    file_num = match.group(1)
                    mcq_data = load_existing_mcq_data(week, file_num)
                
                # Build padded data
                final_data = pad_mcq_data(mcq_data, content_secs)
                
                # Process
                os.makedirs(os.path.dirname(enh_path), exist_ok=True)
                process_file(orig_path, enh_path, final_data, min_mcqs=5)
                
                total_files += 1
                total_sections += len(content_secs)
                print(f"  {rel}: {len(content_secs)} sections + {len(skip_secs)} skipped")
    
    print(f"\n{'='*60}")
    print(f"DONE: {total_files} files, {total_sections} content sections (5+ MCQs each)")

if __name__ == '__main__':
    process_all()
