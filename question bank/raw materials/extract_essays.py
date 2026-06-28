"""
Extract essay questions and group with case scenarios.
Only groups ADJACENT questions — never skips over other question types.
"""
import re, os

WORKDIR = "/media/mohamed/projects4/projects/obstaric/obs app/question bank/raw materials"


def has_inline_mcq_options(q_text: str) -> bool:
    """Check if text has inline MCQ options like a) b) c) or a. b. c."""
    if re.search(r'\b([a-e])\s*\)\s+\S', q_text):
        return True
    if re.search(r'\b([a-e])\.\s+(?:\d+\.?\s*[a-z]|[A-Z])', q_text):
        return True
    if re.search(r'\b([a-e])\.\s+\d+', q_text):
        return True
    if re.search(r'\b[A-Z]\)\s+\w', q_text):  # Capital letter options like A. Complete abortion
        return True
    return False


def extract_inline_options(q_text: str) -> tuple:
    """Check for inline MCQ options and extract them."""
    first_opt = re.search(r'\b([a-e])\s*\)\s', q_text)
    sep = r'(?=[a-e]\s*\)\s)'
    opt_re = r'^[a-e]\s*\)'

    if not first_opt:
        first_opt = re.search(r'\b([a-e])\.\s+(?=[A-Z\d])', q_text)
        if first_opt:
            sep = r'(?=[a-e]\.\s+(?=[A-Z\d]))'
            opt_re = r'^[a-e]\.\s+'

    if not first_opt:
        return q_text, []

    opt_start = first_opt.start()
    question = q_text[:opt_start].strip()
    opts_text = q_text[opt_start:]

    parts = re.split(sep, opts_text)
    options = [p.strip() for p in parts if p.strip() and re.match(opt_re, p.strip())]
    question = re.sub(r'[:,\s]+$', '', question).strip()
    return question, options


def examine_question(body: str) -> dict:
    """Classify a question's raw body."""
    lines = body.strip().split('\n')
    q_lines = []
    bullet_opts = []
    in_options = False
    in_table_block = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('> **Table'):
            in_table_block = True
            break
        if stripped == '**Options:**':
            in_options = True
            continue
        if in_options:
            if stripped.startswith('- '):
                bullet_opts.append(stripped[2:].strip())
        else:
            q_lines.append(stripped)

    if in_table_block:
        return {'type': 'skip'}

    q_text = ' '.join(q_lines).strip()

    # Skip non-question entries
    skip_patterns = [
        r'^Final \d+$', r'^اَلْحَمْدُ', r'^Old Quizzes$',
        r'^Quizzes \d+', r'^Inverted Questions$',
        r'^Family Medicine$', r'^Case \d+$',
    ]
    if any(re.match(p, q_text) for p in skip_patterns):
        return {'type': 'skip'}
    if len(q_text) < 5:
        return {'type': 'skip'}

    # True/False lists are not essays
    if re.match(r'(?:True|False)\s*(?::|$)', q_text, re.IGNORECASE):
        return {'type': 'skip'}

    # Bullet options = MCQ
    if len(bullet_opts) > 0:
        return {'type': 'skip'}

    # Inline MCQ options
    if has_inline_mcq_options(q_text):
        return {'type': 'skip'}

    cleaned_text, inline_opts = extract_inline_options(q_text)
    if len(inline_opts) > 0:
        return {'type': 'skip'}

    # Extended Matching Question Options = skip
    if 'Extended Matching Question' in q_text or 'EMQ' in q_text[:50]:
        return {'type': 'skip'}

    q_lower = q_text.lower()

    # Check for sub-question numbering
    sub_match = re.match(r'^(\d+)[\.\)]\s', q_text)
    sub_num = int(sub_match.group(1)) if sub_match else 0

    # Essay keyword detection
    essay_keywords = [
        r'enumerate', r'^list ', r'mention', r'define', r'describe',
        r'outline', r'explain', r'name the', r'what is your',
        r'what are the', r'what is the', r'how can you', r'^how to ',
        r'most probable diagnosis', r'differential diagnosis',
        r'provisional diagnosis', r'management of', r'confirm the diagnosis',
        r'treatment of', r'indication', r'contraindication',
        r'predisposing factor', r'complication', r'^name of',
        r'follow up', r'investigation', r'^identify',
        r'causes of', r'reasons for', r'classify', r'what is correct about',
        r'which feature is true', r'^answer the following',
        r'what is the proper', r'what is the most appropriate',
        r'create a', r'summarize',
    ]

    # Skip empty "Answer the following:" headers
    if re.match(r'^[Aa]nswer the following', q_text) and len(q_text) < 40:
        return {'type': 'skip'}

    is_essay = any(re.search(p, q_lower) for p in essay_keywords)

    if not is_essay and sub_num == 0:
        # Could be a case description
        if len(q_text) > 20:
            has_case_markers = bool(re.search(
                r'(year[- ]old|years?\s+old|presents|visit(?:ed|s)?\s+her\s+physician|complaining of|admitted|gestation|weeks pregnant|G[\dP]+|primigravida|nullipara|delivery suite|ER |casualty|laboring woman|shown procedure|shown instrument|underwent|history of|history of PCO|'
                r'Pallor|proteinuria|edema|oedema|'
                r'Temp:|BP:|HR:|RR:|Pulse|Hb: |g/dL|g/dl|MCV|'
                r'mg/dL|mm Hg|mmHg|bpm|°C|°F)',
                q_lower
            ))
            if has_case_markers:
                return {
                    'type': 'case_desc',
                    'q_text': q_text,
                    'sub_num': 0,
                    'sub_questions': [],
                }
        return {'type': 'skip'}

    # Check for embedded case in sub-questions
    embedded_case = None
    if sub_num > 0 and len(q_text) > 80:
        # Find positions where a new case might start (after sentence break + uppercase/digit)
        for m in re.finditer(r'[?.!]\s+(?:Case\s+\d+\s+)?(?=[A-Z\d])', q_text):
            pos = m.end()
            # Only consider positions well into the question (not in the opening sub-Q)
            if pos > 25:
                case_candidate = q_text[pos:].strip()
                # Must start with a case-like phrase
                if re.match(r'(?:\w+\s+)?(?:\d+[-]year-old|G[\dP]+|nullipara|primigravida)', case_candidate, re.IGNORECASE):
                    # Stop at the next sub-question number or end
                    next_sub = re.search(r'\s+\d+[\.\)]\s', case_candidate)
                    if next_sub:
                        case_candidate = case_candidate[:next_sub.start()]
                    case_candidate = case_candidate.strip().rstrip('.,;').strip()
                    if len(case_candidate) > 15:
                        embedded_case = case_candidate
                        break

    # Extract sub-question list
    sub_qs = []
    if sub_num > 0:
        parts = re.split(r'(?:^|\s)(\d+[\.\)]\s)', q_text)
        current_q = ""
        for part in parts:
            if re.match(r'\d+[\.\)]\s', part):
                if current_q.strip():
                    sub_qs.append(current_q.strip())
                current_q = part
            else:
                current_q += part
        if current_q.strip():
            sub_qs.append(current_q.strip())

    return {
        'type': 'sub_q' if sub_num > 0 else 'other_essay',
        'q_text': q_text,
        'sub_num': sub_num,
        'sub_questions': sub_qs,
        'embedded_case': embedded_case,
    }


def parse_source_file(filepath: str) -> list:
    """Parse source MD file, return ordered list of question dicts."""
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    pattern = re.compile(r'^## Question (\d+)\n', re.MULTILINE)
    blocks = pattern.split(content)

    questions = []
    for i in range(1, len(blocks), 2):
        qnum = int(blocks[i])
        body = blocks[i+1]
        result = examine_question(body)
        if result.get('type') == 'skip':
            continue
        result['qnum'] = qnum
        result['raw_body'] = body.strip()
        questions.append(result)

    return questions


def group_essays(questions: list) -> list:
    """
    Group adjacent questions into essays.
    Accumulates multiple consecutive sub-questions/other_essays under one pending case.
    Only groups items with Q-number gap <= 2 to avoid cross-case pairing.
    """
    essays = []
    pending_case = None
    pending_embedded_case = None

    # Accumulator for current in-progress group
    cur = None  # {case_text, case_qnum, sub_questions, sub_qnums, note}

    def flush():
        nonlocal cur
        if cur is not None:
            essays.append(cur)
            cur = None

    def start(case_text=None, case_qnum=None, note=None):
        nonlocal cur
        flush()
        cur = {
            'case_text': case_text,
            'case_qnum': case_qnum,
            'sub_questions': [],
            'sub_qnums': [],
            'note': note,
        }

    def add_sub(sq, qnum):
        if cur is not None:
            cur['sub_questions'].append(sq)
            cur['sub_qnums'].append(qnum)

    def last_qnum():
        """Last question number added to current group, or None."""
        if cur is not None and cur['sub_qnums']:
            return cur['sub_qnums'][-1]
        return None

    def adjacent_to_last(qnum):
        """Check if qnum is within gap <= 2 of the last qnum in current group."""
        ln = last_qnum()
        return ln is not None and abs(qnum - ln) <= 2

    for q in questions:
        qnum = q['qnum']

        if q['type'] == 'case_desc':
            # Flush any previous non-empty group
            if cur is not None:
                # If it has sub-questions they stand on their own; if just a case flush
                if not cur['sub_questions'] and cur.get('case_text'):
                    flush()
            pending_case = q
            start(case_text=q['q_text'], case_qnum=qnum)
            pending_embedded_case = None
            continue

        if q['type'] == 'sub_q':
            sub_qs = q['sub_questions']
            has_embedded = q.get('embedded_case')
            sub_num = q['sub_num']

            # Case: sub#1 can attach to pending case or start a new group
            # sub#2+ always appends to the last group (if consecutive)
            if sub_num == 1:
                if pending_case and abs(qnum - pending_case['qnum']) <= 2:
                    # Attach to pending case
                    if cur is None:
                        start(case_text=pending_case['q_text'], case_qnum=pending_case['qnum'])
                    for sq in sub_qs:
                        add_sub(sq, qnum)
                elif pending_embedded_case:
                    start(case_text=pending_embedded_case, case_qnum=qnum, note='embedded')
                    pending_embedded_case = None
                    for sq in sub_qs:
                        add_sub(sq, qnum)
                else:
                    # Orphan sub#1 — start new group (flush if current exists)
                    if cur is not None:
                        flush()
                    start()
                    for sq in sub_qs:
                        add_sub(sq, qnum)
            else:  # sub_num > 1 — continuation
                if cur is not None and adjacent_to_last(qnum):
                    # Continuous — add to current group
                    for sq in sub_qs:
                        add_sub(sq, qnum)
                elif pending_case and abs(qnum - pending_case['qnum']) <= 2:
                    # Directly after a case (no sub#1 in between)
                    if cur is None:
                        start(case_text=pending_case['q_text'], case_qnum=pending_case['qnum'])
                    for sq in sub_qs:
                        add_sub(sq, qnum)
                else:
                    # Orphan continuation — flush and start new
                    if cur is not None:
                        flush()
                    start()
                    for sq in sub_qs:
                        add_sub(sq, qnum)

            # Check for embedded case in last sub-question
            if has_embedded and sub_qs and cur is not None:
                last_idx = len(cur['sub_questions']) - 1
                if last_idx >= 0:
                    last_sq = cur['sub_questions'][last_idx]
                    ec_pattern = re.escape(has_embedded[:30]) if len(has_embedded) > 30 else re.escape(has_embedded)
                    ec_search = re.search(r'(?:Case\s+\d+\s+)?' + ec_pattern, last_sq)
                    if ec_search and ec_search.start() > 0:
                        sq_before = last_sq[:ec_search.start()].strip().rstrip('?.,:;').strip()
                        if sq_before:
                            cur['sub_questions'][last_idx] = sq_before
                        else:
                            cur['sub_questions'].pop()
                        pending_embedded_case = has_embedded

        elif q['type'] == 'other_essay':
            q_text = q['q_text']

            if pending_case and abs(qnum - pending_case['qnum']) <= 2:
                # Attach to pending case (don't consume — keep accumulating)
                if cur is None:
                    start(case_text=pending_case['q_text'], case_qnum=pending_case['qnum'])
                add_sub(q_text, qnum)
            elif pending_embedded_case:
                start(case_text=pending_embedded_case, case_qnum=qnum, note='embedded')
                pending_embedded_case = None
                add_sub(q_text, qnum)
            elif cur is not None and adjacent_to_last(qnum):
                # Continuous other_essay — add to existing group
                add_sub(q_text, qnum)
            else:
                # Standalone — flush previous and start new
                if cur is not None:
                    flush()
                start()
                add_sub(q_text, qnum)

    # Flush remaining
    flush()
    if pending_case and not essays:
        # Unconsumed case with nothing attached
        start(case_text=pending_case['q_text'], case_qnum=pending_case['qnum'], note='standalone')
        flush()
    if pending_embedded_case:
        start(case_text=pending_embedded_case, case_qnum=None, note='embedded')
        flush()

    return essays


def format_essay(e: dict, idx: int) -> list:
    """Format a single essay as lines of markdown."""
    lines = []
    lines.append(f"### Essay {idx}")

    source_ref = []
    if e.get('case_qnum'):
        source_ref.append(f"Case Q{e['case_qnum']}")
    if e.get('sub_qnums'):
        qnums_str = ', '.join(f"Q{n}" for n in e['sub_qnums'])
        source_ref.append(f"Questions: {qnums_str}")
    lines.append(f"*(Source: {'; '.join(source_ref)})*")
    lines.append("")

    if e.get('case_text'):
        lines.append(e['case_text'])
        lines.append("")

    if e.get('sub_questions'):
        for sq in e['sub_questions']:
            lines.append(f"- {sq}")
        lines.append("")

    return lines


# ── Main ──
files = ['Exams Qs.md', 'Other Qs.md', 'Quizzes Qs.md']
all_essays = []
all_stats = {}

for fname in files:
    filepath = os.path.join(WORKDIR, fname)
    if not os.path.exists(filepath):
        continue

    questions = parse_source_file(filepath)
    type_counts = {}
    for q in questions:
        t = q['type']
        type_counts[t] = type_counts.get(t, 0) + 1

    essays = group_essays(questions)
    with_case = sum(1 for e in essays if e.get('case_text'))
    without_case = sum(1 for e in essays if not e.get('case_text'))

    all_stats[fname] = {
        'parsed': len(questions),
        'types': type_counts,
        'essays': len(essays),
        'with_case': with_case,
        'without_case': without_case,
    }

    print(f"{fname}:")
    print(f"  Parsed {len(questions)} questions → {type_counts}")
    print(f"  Grouped into {len(essays)} essays ({with_case} with case, {without_case} without)")

    all_essays.append((fname, essays))

# Write output file
outpath = os.path.join(WORKDIR, "essay questions.md")

lines = []
lines.append("# SUPPORT 41 — Obstetrics — Essay Questions")
lines.append("")
lines.append("*Collected from all 3 source files. Case scenarios grouped with adjacent sub-questions.*")
lines.append("")
lines.append("---")
lines.append("")

essay_idx = 0
for fname, essays in all_essays:
    source_label = fname.replace('.md', '')
    lines.append("")
    lines.append(f"## Source: {source_label}")
    lines.append("")

    for e in essays:
        essay_idx += 1
        lines.extend(format_essay(e, essay_idx))

lines.append("---")
lines.append("")
lines.append("### Statistics")
lines.append("")
total_essays = essay_idx
total_with_case = sum(s['with_case'] for s in all_stats.values())
total_without = sum(s['without_case'] for s in all_stats.values())
lines.append(f"- **Total essay groups:** {total_essays}")
lines.append(f"- **With case context:** {total_with_case}")
lines.append(f"- **Without case context:** {total_without}")
lines.append("")
for fname, stats in all_stats.items():
    lines.append(f"- `{fname}`: {stats['parsed']} parsed → {stats['essays']} essays ({stats['with_case']}+case, {stats['without_case']} orphan)")
lines.append("")

content = '\n'.join(lines)

with open(outpath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{'='*60}")
print(f"Written {total_essays} essay groups to:")
print(f"  {outpath}")
