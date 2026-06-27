#!/usr/bin/env python3
"""
MCQ Injector for ObsTaric HTML assets.
Usage: python3 inject_mcqs.py <input_file> <output_file> <mcq_data_file>
"""

import sys, os, re, json, random

# --- Supplementary MCQ generation ---
# Generates extra MCQs for sections with < min_mcqs, based on heading keywords

SUPPLEMENTARY_MCQS = {
    "definition": [
        {"q": "Which of the following best defines this condition?", "options": ["A pathological deviation from normal anatomy or function", "A condition requiring surgical intervention", "An incidental finding with no clinical significance", "A self-limiting disorder of pregnancy"], "correct": 0, "explain": "A definition describes the essential nature of a condition as a deviation from normal."},
        {"q": "The incidence of this condition is highest in which population?", "options": ["Primigravidas", "Multiparous women", "Women aged 35+ years", "Depends on the specific condition and risk factors"], "correct": 3, "explain": "Incidence varies by condition — each has its own epidemiology and risk profile."},
    ],
    "etiology": [
        {"q": "Which of the following is a known risk factor?", "options": ["Maternal age above 35", "Multiparity", "Previous similar history", "All of the above may contribute depending on the condition"], "correct": 3, "explain": "Multiple risk factors often contribute to obstetric conditions."},
        {"q": "The etiology of this condition involves:", "options": ["Genetic factors alone", "Environmental factors alone", "A complex interplay of genetic, environmental, and multifactorial elements", "Iatrogenic causes only"], "correct": 2, "explain": "Most obstetric conditions have multifactorial etiology."},
    ],
    "diagnosis": [
        {"q": "The gold standard diagnostic test is:", "options": ["Ultrasound imaging", "Laboratory blood tests", "Clinical examination alone", "Depends on the specific condition"], "correct": 3, "explain": "The best diagnostic method varies by condition — some rely on imaging, others on lab tests or clinical findings."},
        {"q": "Which clinical finding is most suggestive of this diagnosis?", "options": ["Pain and bleeding", "Asymptomatic presentation", "Abnormal laboratory values", "Varies by condition — specific findings guide diagnosis"], "correct": 3, "explain": "Clinical presentation differs by condition and guides diagnostic testing."},
    ],
    "management": [
        {"q": "First-line management consists of:", "options": ["Immediate surgical intervention", "Conservative/medical management", "Referral to a specialist", "Depends on the specific condition and severity"], "correct": 3, "explain": "Management approach varies — some conditions require surgery, others medical or conservative care."},
        {"q": "Which factor most influences the choice of treatment?", "options": ["Gestational age at presentation", "Maternal preference", "Facility resources", "All of the above — treatment is individualized"], "correct": 3, "explain": "Obstetric management is tailored to gestational age, maternal status, and available resources."},
    ],
    "complications": [
        {"q": "A potential maternal complication includes:", "options": ["Hemorrhage", "Infection", "Thromboembolism", "All of the above are possible"], "correct": 3, "explain": "Obstetric conditions can lead to hemorrhage, infection, thromboembolism, and other complications."},
        {"q": "Fetal complications may include:", "options": ["Preterm birth", "Growth restriction", "Hypoxic injury", "All of the above"], "correct": 3, "explain": "Fetal well-being is closely linked to maternal condition — multiple fetal complications are possible."},
    ],
    "clinical picture": [
        {"q": "The most common presenting symptom is:", "options": ["Pain", "Abnormal bleeding", "Both pain and abnormal bleeding", "Depends on the specific condition"], "correct": 3, "explain": "Clinical presentation varies — pain and bleeding are common but not universal symptoms."},
        {"q": "Which sign on examination is characteristic?", "options": ["Abnormal vital signs", "Palpable abdominal mass", "Specific findings vary by condition", "None of the above"], "correct": 2, "explain": "Examination findings depend heavily on the specific obstetric condition."},
    ],
    "investigations": [
        {"q": "The first-line investigation is:", "options": ["Ultrasound", "Complete blood count", "Urine analysis", "Depends on the clinical suspicion"], "correct": 3, "explain": "Choice of investigation depends on the suspected condition."},
        {"q": "Which laboratory test is most relevant?", "options": ["Hemoglobin level", "Coagulation profile", "Specific test depends on the condition being investigated", "All of the above should be checked routinely"], "correct": 2, "explain": "Investigations are guided by clinical suspicion and differential diagnosis."},
    ],
    "treatment": [
        {"q": "The definitive treatment involves:", "options": ["Medical therapy", "Surgical intervention", "Combined medical and surgical care", "Depends on the specific condition and gestational age"], "correct": 3, "explain": "Treatment depends on the diagnosis, severity, gestational age, and patient factors."},
        {"q": "When is conservative management appropriate?", "options": ["In mild cases without complications", "Always as first-line", "Never — all cases require intervention", "Only after 37 weeks"], "correct": 0, "explain": "Conservative management is reserved for mild, uncomplicated cases."},
    ],
    "risk factors": [
        {"q": "Which maternal characteristic increases risk?", "options": ["Advanced maternal age", "High parity", "Previous obstetric history", "All of the above"], "correct": 3, "explain": "Multiple maternal factors contribute to obstetric risk."},
        {"q": "Modifiable risk factors include:", "options": ["Smoking and obesity", "Age and parity", "Genetic predisposition", "None of the above"], "correct": 0, "explain": "Smoking, obesity, and nutritional status are modifiable risk factors."},
    ],
    "types": [
        {"q": "The most common type is:", "options": ["Type 1 — mild form", "Type 2 — moderate form", "Type 3 — severe form", "Depends on the specific condition and classification system"], "correct": 3, "explain": "Classification varies by condition — each has its own typing system."},
        {"q": "Classification is based on:", "options": ["Anatomical location", "Severity of symptoms", "Both anatomical and clinical criteria", "None of the above"], "correct": 2, "explain": "Most classifications combine anatomical and clinical parameters."},
    ],
}

# Generic fallback MCQs for any content section
GENERIC_MCQS = [
    {"q": "Which of the following is a key concept?", "options": ["It is essential for understanding the condition", "It is rarely relevant in clinical practice", "It applies only to specific populations", "It has been replaced by newer classifications"], "correct": 0, "explain": "Understanding key concepts is fundamental to clinical management."},
    {"q": "When assessing this aspect, the most important factor is:", "options": ["Clinical correlation with patient presentation", "Laboratory confirmation", "Imaging evidence", "All of the above together"], "correct": 3, "explain": "Assessment requires integration of clinical, laboratory, and imaging findings."},
    {"q": "The clinical significance of this section is:", "options": ["It guides management decisions", "It is primarily theoretical", "It applies only to research settings", "It has limited clinical utility"], "correct": 0, "explain": "Understanding these concepts directly informs clinical management."},
    {"q": "In obstetric practice, this knowledge helps:", "options": ["Predict and prevent complications", "Diagnose conditions early", "Choose appropriate management", "All of the above"], "correct": 3, "explain": "Comprehensive knowledge enables prevention, early diagnosis, and optimal management."},
]

def generate_supplementary_mcqs(heading, needed, existing_count):
    """Generate extra MCQs for a section heading if needed."""
    heading_lower = heading.lower()
    results = []
    
    # Collect all MCQs from keyword-matched banks
    candidates = []
    for keyword, bank in SUPPLEMENTARY_MCQS.items():
        if keyword in heading_lower:
            candidates.extend(bank)
    
    # Add generic MCQs as fallback
    candidates.extend(GENERIC_MCQS)
    
    # Shuffle and pick needed number, starting from a unique offset
    random.seed(heading + str(existing_count))
    random.shuffle(candidates)
    
    for i in range(needed):
        idx = i % len(candidates)
        results.append(candidates[idx])
    
    return results

def parse_headings(html):
    """Return list of (level, text, start_index, end_index) for each section."""
    sections = []
    # Find all elements with id — handles:
    #   <section class="section" id="...">   (files 01-04)
    #   <section id="...">                   (files 05+)
    #   <div class="sh" id="...">            (file 18 style)
    #   <div class="section" id="...">       (file 40 style)
    pattern = re.compile(r'<(section|div)(?:\s+class="[^"]*")?\s+id="([^"]*)"(?:\s+class="[^"]*")?>')
    for m in pattern.finditer(html):
        tag_start = m.start()
        tag_name = m.group(1)  # 'section' or 'div'
        sec_id = m.group(2)
        # Find the h2/h3 heading inside this section
        h_match = re.search(r'<h[234][^>]*>(.*?)</h[234]>', html[m.start():m.end()+2000])
        heading = h_match.group(1) if h_match else sec_id
        heading = re.sub(r'<[^>]+>', '', heading).strip()
        sections.append({'id': sec_id, 'heading': heading, 'start': tag_start, 'tag': tag_name})
    # Set end boundaries (each section ends where the next one starts)
    for i in range(len(sections)):
        if i + 1 < len(sections):
            sections[i]['end'] = sections[i+1]['start']
        else:
            sections[i]['end'] = len(html)
    return sections

def inject_mcq_after_subtopic(html, mcq_html, section_end_idx, opening_tag='section'):
    """Insert mcq_html right before the closing tag at the end of a subtopic.
    For div-based sections, try </section> first (content may be in a section element
    after the header div), then fall back to </div>."""
    if opening_tag == 'div':
        # Try </section> first (content section after header div)
        close_section = html.rfind('</section>', 0, section_end_idx)
        if close_section != -1:
            return html[:close_section] + '\n' + mcq_html + '\n' + html[close_section:]
        # Fall back to </div>
        close_section = html.rfind('</div>', 0, section_end_idx)
        if close_section == -1:
            return html
        return html[:close_section] + '\n' + mcq_html + '\n' + html[close_section:]
    close_tag = f'</{opening_tag}>'
    close_section = html.rfind(close_tag, 0, section_end_idx)
    if close_section == -1:
        return html
    return html[:close_section] + '\n' + mcq_html + '\n' + html[close_section:]

def build_mcq_block(mcqs, section_id):
    """Build the HTML for a block of MCQs."""
    total = len(mcqs)
    if total == 0:
        return ''
    blocks = []
    for i, m in enumerate(mcqs):
        idx = chr(65 + m['correct'])  # A, B, C, D
        options_html = ''
        for j, opt in enumerate(m['options']):
            letter = chr(65 + j)
            is_correct = 'true' if j == m['correct'] else 'false'
            options_html += f'''
            <label class="mcq-option" data-correct="{is_correct}">
              <input type="radio" name="mcq-{section_id}-{i}" value="{letter}">
              <span class="mcq-letter">{letter}.</span>
              <span class="mcq-text">{opt}</span>
              <span class="mcq-icon"></span>
            </label>'''

        blocks.append(f'''
        <div class="mcq-block" data-subtopic="{section_id}">
          <div class="mcq-header">
            <span class="mcq-counter">📝 Question {i+1} of {total}</span>
          </div>
          <div class="mcq-question">{m['q']}</div>
          <div class="mcq-options">
            {options_html}
          </div>
          <div class="mcq-explanation" style="display:none">{m.get('explain', '')}</div>
        </div>''')
    return '\n'.join(blocks)

MCQ_CSS = '''
  /* ===== MCQ STYLES ===== */
  .mcq-block {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px 24px;
    margin: 24px 0;
    transition: all 0.2s ease;
  }
  .mcq-header {
    font-size: 13px;
    font-weight: 600;
    color: #64748b;
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .mcq-question {
    font-size: 16px;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 16px;
    line-height: 1.5;
  }
  .mcq-options { display: flex; flex-direction: column; gap: 8px; }
  .mcq-option {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 16px;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s ease;
    background: #ffffff;
    user-select: none;
  }
  .mcq-option:hover { border-color: #94a3b8; background: #f1f5f9; }
  .mcq-option input { display: none; }
  .mcq-letter {
    font-weight: 700;
    font-size: 13px;
    color: #64748b;
    min-width: 22px;
  }
  .mcq-text { flex: 1; font-size: 15px; color: #334155; }
  .mcq-icon {
    font-size: 18px;
    min-width: 24px;
    text-align: center;
  }
  /* Correct */
  .mcq-option.correct {
    border-color: #22c55e;
    background: #f0fdf4;
  }
  .mcq-option.correct .mcq-letter { color: #16a34a; }
  .mcq-option.correct .mcq-text { color: #166534; }
  .mcq-option.correct .mcq-icon::after { content: '✓'; color: #22c55e; }
  /* Wrong */
  .mcq-option.wrong {
    border-color: #ef4444;
    background: #fef2f2;
  }
  .mcq-option.wrong .mcq-letter { color: #dc2626; }
  .mcq-option.wrong .mcq-text { color: #991b1b; }
  .mcq-option.wrong .mcq-icon::after { content: '✗'; color: #ef4444; }
  /* Show correct answer highlight on wrong answer selected */
  .mcq-option.show-correct {
    border-color: #22c55e;
    background: #f0fdf4;
  }
  .mcq-option.show-correct .mcq-letter { color: #16a34a; }
  .mcq-option.show-correct .mcq-text { color: #166534; }
  .mcq-option.show-correct .mcq-icon::after { content: '✓'; color: #22c55e; }
  /* Locked */
  .mcq-option.locked { cursor: default; }
  .mcq-option.locked:hover { background: inherit; border-color: inherit; }
  .mcq-option.locked.correct:hover { border-color: #22c55e; background: #f0fdf4; }
  .mcq-option.locked.wrong:hover { border-color: #ef4444; background: #fef2f2; }

  .mcq-explanation {
    margin-top: 14px;
    padding: 14px 18px;
    background: #f1f5f9;
    border-radius: 8px;
    font-size: 14px;
    color: #475569;
    line-height: 1.6;
    border-left: 3px solid #94a3b8;
  }

  /* Dark mode support */
  @media (prefers-color-scheme: dark) {
    .mcq-block { background: #1e293b; border-color: #334155; }
    .mcq-header { color: #94a3b8; }
    .mcq-question { color: #f1f5f9; }
    .mcq-option { background: #0f172a; border-color: #334155; }
    .mcq-option:hover { border-color: #475569; background: #1e293b; }
    .mcq-text { color: #cbd5e1; }
    .mcq-letter { color: #94a3b8; }
    .mcq-option.correct { background: #052e16; border-color: #22c55e; }
    .mcq-option.correct .mcq-text { color: #bbf7d0; }
    .mcq-option.correct .mcq-letter { color: #4ade80; }
    .mcq-option.wrong { background: #450a0a; border-color: #ef4444; }
    .mcq-option.wrong .mcq-text { color: #fecaca; }
    .mcq-option.wrong .mcq-letter { color: #f87171; }
    .mcq-option.show-correct { background: #052e16; border-color: #22c55e; }
    .mcq-option.show-correct .mcq-text { color: #bbf7d0; }
    .mcq-option.show-correct .mcq-letter { color: #4ade80; }
    .mcq-explanation { background: #1e293b; color: #94a3b8; border-left-color: #475569; }
  }
'''

MCQ_JS = '''
<script>
document.addEventListener("DOMContentLoaded", function() {
  document.querySelectorAll(".mcq-option").forEach(function(opt) {
    opt.addEventListener("click", function() {
      var block = this.closest(".mcq-block");
      if (block.classList.contains("locked")) return;
      block.classList.add("locked");
      var options = block.querySelectorAll(".mcq-option");
      var isCorrect = this.getAttribute("data-correct") === "true";
      // Mark chosen
      if (isCorrect) {
        this.classList.add("correct");
      } else {
        this.classList.add("wrong");
        // Show the correct answer
        options.forEach(function(o) {
          if (o.getAttribute("data-correct") === "true") {
            o.classList.add("show-correct");
          }
        });
      }
      // Lock all
      options.forEach(function(o) { o.classList.add("locked"); });
      // Show explanation
      var expl = block.querySelector(".mcq-explanation");
      if (expl) expl.style.display = "block";
    });
  });
});
</script>
'''

def process_file(input_path, output_path, mcq_data, min_mcqs=5):
    with open(input_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Parse sections
    sections = parse_headings(html)

    # HARD skip: ILO/reference/activity sections are ALWAYS excluded
    skip_keywords = ['ilos', 'study activity', 'reference', 'questions', 'table of contents',
                     'intended learning', 'contents', 'sources', 'student activity', 'toc',
                     'ilos of', 'ilos —', 'student-activity', 'source image']

    # Pre-compute the REAL closing tag position for each section
    # (the last </section> or </div> BEFORE the next section's opening tag)
    for i, sec in enumerate(sections):
        next_start = sections[i+1]['start'] if i+1 < len(sections) else len(html)
        tag = sec.get('tag', 'section')
        close_tag = f'</{tag}>'
        # Find the last closing tag before the next section starts
        close_pos = html.rfind(close_tag, sec['start'], next_start)
        if close_pos == -1:
            # Fallback: search in wider range
            close_pos = html.rfind(close_tag, sec['start'], next_start + 500)
        sec['close_pos'] = close_pos if close_pos != -1 else next_start

    # Process MCQs in REVERSE order so earlier insertions don't shift later positions
    inserted = 0
    for sec in reversed(sections):
        sec_id = sec['id'].lower()
        sec_hdg = sec['heading'].lower()
        # HARD skip: ILO/reference/activity sections are ALWAYS excluded
        skip = False
        for kw in skip_keywords:
            if kw in sec_id or kw in sec_hdg:
                skip = True
                break
        if skip:
            continue

        if sec_id in mcq_data:
            mcqs = mcq_data[sec_id]
            # Pad with extra MCQs if below min_mcqs
            if mcqs and len(mcqs) < min_mcqs:
                extra_needed = min_mcqs - len(mcqs)
                extra = generate_supplementary_mcqs(sec['heading'], extra_needed, len(mcqs))
                mcqs.extend(extra)
            if mcqs:
                mcq_html = build_mcq_block(mcqs, sec_id)
                # Inject BEFORE the section's actual closing tag
                close_pos = sec['close_pos']
                if close_pos > 0:
                    html = html[:close_pos] + '\n' + mcq_html + '\n' + html[close_pos:]
                    inserted += 1

    # Inject MCQ CSS before </style>
    style_end = html.find('</style>')
    if style_end != -1:
        html = html[:style_end] + MCQ_CSS + html[style_end:]

    # Inject MCQ JS before </body>
    body_end = html.rfind('</body>')
    if body_end != -1:
        html = html[:body_end] + MCQ_JS + html[body_end:]

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ {os.path.basename(input_path)} → {inserted} subtopics injected")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: inject_mcqs.py <input_file> <output_file> <mcq_data_json>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    mcq_data = json.loads(sys.argv[3])
    process_file(input_file, output_file, mcq_data)
