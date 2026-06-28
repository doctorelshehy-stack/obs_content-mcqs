"""
Parse MD question files, extract only MCQs with proper options.
For questions with inline options (a)..., b)..., c)...) extract them.
For questions with < 3 options, add plausible distractors from context.
Skip essay/case questions with no options at all.
Saves to new files (originals untouched).
"""
import re, os

WORKDIR = "/media/mohamed/projects3/projects/obstaric/obs app/question bank/raw materials"

# ── Condition-specific distractor pools ──
# Each entry: list of plausible wrong answers for exam questions about this topic

CONDITION_DISTRACTORS = {
    "milk engorgement": [
        "Apply cold compresses after feeding",
        "Apply breast binders and stop breastfeeding",
        "Massage the breasts vigorously with alcohol",
        "Restrict fluid intake",
        "Apply ice packs only",
        "Continue exclusive breastfeeding",
        "Apply warm compresses after feeding",
    ],
    "antenatal care visit|first visit|booking visit": [
        "At 16 weeks of gestation",
        "At 20 weeks of gestation",
        "At 28 weeks of gestation",
        "Only when quickening is felt",
        "During the third trimester",
        "At 12 weeks of gestation",
        "In the first trimester",
    ],
    "ectopic|tubal pregnancy": [
        "Ruptured ovarian cyst",
        "Acute appendicitis",
        "Pelvic inflammatory disease",
        "Ovarian torsion",
        "Corpus luteum hemorrhage",
        "Threatened abortion",
        "Ovarian pregnancy",
        "Cervical pregnancy",
    ],
    "abortion|miscarriage": [
        "Missed abortion",
        "Septic abortion",
        "Complete abortion",
        "Threatened abortion",
        "Inevitable abortion",
        "Incomplete abortion",
        "Anembryonic pregnancy",
        "Blighted ovum",
    ],
    "preeclampsia|eclampsia|hypertensive": [
        "Chronic hypertension",
        "Gestational hypertension",
        "HELLP syndrome",
        "Renal disease",
        "Essential hypertension",
        "Superimposed preeclampsia",
        "White coat hypertension",
    ],
    "placenta previa": [
        "Abruptio placenta",
        "Placenta accreta",
        "Vasa previa",
        "Marginal sinus rupture",
        "Placenta increta",
        "Placenta percreta",
    ],
    "abruptio|abruption": [
        "Placenta previa",
        "Uterine rupture",
        "Vasa previa",
        "Cervical tear",
        "Coagulopathy",
        "Amniotic fluid embolism",
    ],
    "pph|postpartum hemorrhage|atonic": [
        "Genital tract trauma",
        "Retained products of conception",
        "Coagulopathy",
        "Uterine inversion",
        "Uterine rupture",
        "Placenta accreta",
        "Vulvovaginal hematoma",
    ],
    "contracept|iud|coc|ocp|pill|dmpa|depo": [
        "Combined oral contraceptives",
        "Progestin-only pill",
        "Copper IUD",
        "Levonorgestrel IUD (Mirena)",
        "DMPA injection",
        "Subdermal implant",
        "Barrier methods (condom)",
        "Lactational amenorrhea method",
        "Bilateral tubal ligation",
        "Vasectomy",
    ],
    "infection|pyelonephritis|sepsis|chorioamnionitis": [
        "Escherichia coli",
        "Group B Streptococcus",
        "Klebsiella pneumoniae",
        "Staphylococcus aureus",
        "Chlamydia trachomatis",
        "Neisseria gonorrhoeae",
        "Trichomonas vaginalis",
        "Candida albicans",
    ],
    "diabetes|gestational": [
        "Gestational diabetes mellitus",
        "Type 1 diabetes mellitus",
        "Type 2 diabetes mellitus",
        "Pre-gestational diabetes",
        "Impaired glucose tolerance",
        "Maturity onset diabetes of young",
    ],
    "anemia|anaemia|hb|hemoglobin|ferritin|iron": [
        "Iron deficiency anemia",
        "Folate deficiency anemia",
        "Vitamin B12 deficiency anemia",
        "Thalassemia trait",
        "Sickle cell disease",
        "Anemia of chronic disease",
        "Hereditary spherocytosis",
    ],
    "heart disease|mitral|stenosis|cardiac": [
        "Mitral stenosis",
        "Mitral regurgitation",
        "Aortic stenosis",
        "Aortic regurgitation",
        "Peripartum cardiomyopathy",
        "Congenital heart disease",
        "Atrial septal defect",
        "Ventricular septal defect",
    ],
    "fetal heart|nst|non stress|cardiotocograph": [
        "Reactive NST",
        "Non-reactive NST",
        "Sinusoidal pattern",
        "Variable decelerations",
        "Late decelerations",
        "Early decelerations",
        "Prolonged decelerations",
        "Tachycardia",
        "Bradycardia",
    ],
    "breech": [
        "Complete breech",
        "Frank breech",
        "Footling breech",
        "Incomplete breech",
        "Kneeling presentation",
        "Singletons breech",
    ],
    "face presentation|brow": [
        "Face presentation",
        "Brow presentation",
        "Vertex presentation",
        "Compound presentation",
        "Shoulder presentation",
        "Breech presentation",
    ],
    "shoulder dystocia": [
        "McRoberts maneuver",
        "Suprapubic pressure",
        "Delivery of posterior arm",
        "Woods corkscrew maneuver",
        "Rubin maneuver",
        "Gaskin maneuver (all fours)",
        "Fundal pressure (contraindicated)",
        "Zavanelli maneuver",
    ],
    "forceps|ventouse|vacuum": [
        "Outlet forceps",
        "Low forceps",
        "Mid-cavity forceps",
        "Kielland forceps",
        "Piper forceps (for aftercoming head)",
        "Wrigley forceps",
        "Vacuum extraction (ventouse)",
        "Manual rotation",
    ],
    "episiotomy": [
        "Midline episiotomy",
        "Mediolateral episiotomy",
        "Lateral episiotomy",
        "Second degree perineal tear",
        "Perineal massage",
        "Ritgen maneuver",
    ],
    "cervical incompetence|cerclage": [
        "Shirodkar cerclage",
        "McDonald cerclage",
        "Abdominal cerclage",
        "Transvaginal cervical stitch",
        "Cervical pessary",
        "Bed rest only",
    ],
    "preterm labor|tocolysis|tocolytic": [
        "Nifedipine",
        "Atosiban",
        "Indomethacin",
        "Magnesium sulfate",
        "Terbutaline",
        "Ritodrine",
        "Salbutamol",
        "Progesterone",
    ],
    "induction|induce": [
        "Oxytocin infusion",
        "Dinoprostone (PGE2)",
        "Misoprostol (PGE1)",
        "Artificial rupture of membranes",
        "Cervical ripening balloon",
        "Hygroscopic cervical dilators",
        "Stripping of membranes",
    ],
    "bishop score|bishop": [
        "Cervical dilatation",
        "Cervical effacement",
        "Cervical consistency",
        "Cervical position",
        "Fetal station",
    ],
    "version|external cephalic": [
        "External cephalic version",
        "Internal podalic version",
        "Bipolar version",
        "Combined version",
        "Spontaneous version",
        "Pregnancy termination",
    ],
    "uterine action|dystocia|constriction": [
        "Constriction ring",
        "Pathological retraction ring (Bandl)",
        "Cervical dystocia",
        "Colicky uterus",
        "Hypotonic uterine inertia",
        "Incoordinate uterine action",
        "Obstructed labor",
    ],
    "retraction ring|bandl": [
        "Constriction ring",
        "Pathological retraction ring (Bandl)",
        "Cervical dystocia",
        "Hypotonic inertia",
        "Colicky uterus",
        "Uterine rupture",
    ],
    "fetal skull|diameter|measurement": [
        "Suboccipito-bregmatic (9.5 cm)",
        "Suboccipito-frontal (10 cm)",
        "Occipito-frontal (11.5 cm)",
        "Mento-vertical (14 cm)",
        "Submento-bregmatic (9.5 cm)",
        "Submento-vertical (11.5 cm)",
        "Biparietal (9.5 cm)",
        "Bitemporal (8.2 cm)",
    ],
    "klumpke|erb|palsy|birth injury": [
        "Klumpke's palsy (C8-T1)",
        "Erb-Duchenne palsy (C5-C6)",
        "Erb's palsy (C5-C6)",
        "Phrenic nerve injury",
        "Facial nerve palsy",
        "Brachial plexus injury",
        "Fractured clavicle",
        "Fractured humerus",
    ],
    "cephalohematoma|caput succedaneum": [
        "Cephalohematoma",
        "Caput succedaneum",
        "Subgaleal hemorrhage",
        "Intracranial hemorrhage",
        "Molding",
    ],
    "twins|twin|multiple pregnancy|dichorionic|monochorionic": [
        "Dichorionic diamniotic twins",
        "Dichorionic monoamniotic twins",
        "Monochorionic diamniotic twins",
        "Monochorionic monoamniotic twins",
        "Conjoined twins",
        "Twin-to-twin transfusion syndrome",
        "Acardiac twin (TRAP sequence)",
    ],
    "hydatidiform|molar|gtn|choriocarcinoma": [
        "Complete hydatidiform mole",
        "Partial hydatidiform mole",
        "Invasive mole (chorioadenoma destruens)",
        "Choriocarcinoma",
        "Placental site trophoblastic tumor",
        "Theca lutein cysts",
    ],
    "amniotic fluid|oligohydramnios|polyhydramnios": [
        "Oligohydramnios (AFI < 5 cm)",
        "Polyhydramnios (AFI > 25 cm)",
        "Normal amniotic fluid volume",
        "AFI 8-18 cm",
        "Single deepest pocket < 2 cm",
        "Single deepest pocket > 8 cm",
    ],
    "iugr|growth restriction|fetal growth": [
        "Symmetric IUGR (type I)",
        "Asymmetric IUGR (type II)",
        "Small for gestational age (SGA)",
        "Large for gestational age (LGA)",
        "Macrosomia",
        "Constitutional smallness",
    ],
    "macrosomia|macrosomic": [
        "Fetal macrosomia (> 4000 g)",
        "LGA (> 90th percentile)",
        "Constitutional large fetus",
        "Fetal hydrops",
    ],
    "lochia|puerperium|puerperal": [
        "Lochia rubra (days 1-3)",
        "Lochia serosa (days 4-10)",
        "Lochia alba (days 11-40)",
        "Lochia mucosa",
    ],
    "rh|isoimmunization|hemolytic": [
        "Rh isoimmunization",
        "ABO incompatibility",
        "Kell incompatibility",
        "Hemolytic disease of newborn",
        "Hydrops fetalis (immune)",
        "Hydrops fetalis (non-immune)",
    ],
    "uterine inversion": [
        "Acute uterine inversion",
        "Subacute uterine inversion",
        "Chronic uterine inversion",
        "Complete uterine inversion",
        "Incomplete uterine inversion",
        "Prolapsed uterine inversion",
    ],
    "uterine rupture": [
        "Complete uterine rupture",
        "Incomplete uterine rupture",
        "Dehiscence of scar",
        "Uterine perforation",
        "Cervical tear",
        "Vaginal tear",
    ],
    "round ligament|broad ligament": [
        "Round ligament of uterus",
        "Broad ligament of uterus",
        "Ovarian ligament",
        "Suspensory ligament of ovary",
        "Uterosacral ligament",
        "Cardinal ligament (Mackenrodt)",
        "Pubocervical ligament",
    ],
    "perineal tear|perineal": [
        "First degree perineal tear",
        "Second degree perineal tear",
        "Third degree perineal tear",
        "Fourth degree perineal tear",
        "Cervical laceration",
        "Vaginal laceration",
    ],
    "cesarean|cs|section": [
        "Lower segment cesarean section",
        "Classical (upper segment) cesarean section",
        "Elective cesarean section",
        "Emergency cesarean section",
        "Repeat cesarean section",
        "Cesarean hysterectomy",
    ],
    "hysterectomy": [
        "Total abdominal hysterectomy",
        "Subtotal hysterectomy",
        "Vaginal hysterectomy",
        "Radical hysterectomy",
        "Cesarean hysterectomy",
        "Myomectomy",
    ],
    "postpartum depression|ppd|blues": [
        "Postpartum blues (baby blues)",
        "Postpartum depression",
        "Postpartum psychosis",
        "Postpartum anxiety",
        "Adjustment disorder",
        "Obsessive compulsive disorder",
    ],
    "hypertensis|nausea|vomiting": [
        "Mild hyperemesis gravidarum",
        "Severe hyperemesis gravidarum",
        "Wernicke encephalopathy",
        "Hypokalemia",
        "Metabolic alkalosis",
    ],
    "weight gain|bmi|nutrition": [
        "Underweight (BMI < 18.5): 12.5-18 kg",
        "Normal weight (BMI 18.5-24.9): 11.5-16 kg",
        "Overweight (BMI 25-29.9): 7-11.5 kg",
        "Obese (BMI > 30): 5-9 kg",
        "Inadequate weight gain (< 5 kg)",
        "Excessive weight gain (> 20 kg)",
    ],
    "edema|souffle|chadwick|hegar|goodell": [
        "Chadwick's sign (bluish cervix)",
        "Goodell's sign (soft cervix)",
        "Hegar's sign (soft isthmus)",
        "Uterine soufflé",
        "Funic soufflé",
        "Palpation of fetal parts",
        "Auscultation of FHS",
    ],
    "sure signs|presumptive|probable": [
        "Presumptive signs of pregnancy",
        "Probable signs of pregnancy",
        "Positive (sure) signs of pregnancy",
        "Quickening",
        "Uterine enlargement",
        "Fetal heart auscultation",
        "Fetal movement palpation",
    ],
    "lecithin|sphingomyelin|ls ratio|amniocentesis": [
        "L/S ratio > 2:1 (fetal lung maturity)",
        "Phosphatidylglycerol (PG) presence",
        "Absence of PG",
        "Fluorescence polarization",
        "Foam stability test",
        "Shake test",
    ],
}


def get_condition_distractors(q_text: str, existing_opts: list, needed: int) -> list:
    """Find condition-specific distractors for a question."""
    q_lower = q_text.lower()
    existing_lower = [e.lower().strip() for e in existing_opts]
    
    for pattern, pool in CONDITION_DISTRACTORS.items():
        patterns = [p.strip() for p in pattern.split('|')]
        if any(p in q_lower for p in patterns):
            filtered = [d for d in pool 
                       if d.lower().strip() not in existing_lower 
                       and d.lower() not in q_lower]
            # Shuffle - take from different positions to vary
            if len(filtered) >= needed:
                return filtered[:needed]
            elif filtered:
                return filtered
    
    return []


def generate_distractors(q_text: str, existing_opts: list, target: int = 4) -> list:
    """Generate plausible distractors for a medical MCQ with too few options."""
    needed = target - len(existing_opts)
    if needed <= 0:
        return []
    
    # First try: condition-specific distractors
    specific = get_condition_distractors(q_text, existing_opts, needed)
    if len(specific) >= needed:
        return specific[:needed]
    
    # Second try: use question type to pick from general pools
    extras = list(specific)
    
    # Management/contraindication/cause pools for general questions
    general_pools = {
        "management": [
            "Conservative medical management",
            "Surgical intervention",
            "Expectant management",
            "Elective cesarean delivery",
            "Induction of labor",
            "Serial monitoring and follow-up",
            "Referral to tertiary care center",
        ],
        "contraindication": [
            "Obstructed labor",
            "Cephalopelvic disproportion",
            "Fetal distress",
            "Cord prolapse",
            "Placenta previa",
            "Previous classical CS",
        ],
        "diagnosis": [
            "Threatened abortion",
            "Inevitable abortion",
            "Ectopic pregnancy",
            "Preeclampsia",
            "Placenta previa",
            "Abruptio placenta",
        ],
    }
    
    q_lower = q_text.lower()
    existing_lower = [e.lower().strip() for e in existing_opts]
    
    # Determine best pool
    pool_type = 'diagnosis'
    if any(p in q_lower for p in ['management', 'treatment', 'therapy', 'manage', 'best method', 'indicated', 'procedure']):
        pool_type = 'management'
    elif any(p in q_lower for p in ['contraindicated', 'contraindication', 'not indicated']):
        pool_type = 'contraindication'
    elif any(p in q_lower for p in ['diagnosis', 'diagnose', 'most likely', 'most probable', 'differential']):
        pool_type = 'diagnosis'
    
    pool = general_pools.get(pool_type, general_pools['diagnosis'])
    for opt in pool:
        if opt.lower().strip() not in existing_lower and opt not in extras:
            extras.append(opt)
            if len(extras) >= needed:
                return extras[:needed]
    
    return extras[:needed]


def extract_inline_options(q_text: str) -> tuple:
    """
    Extract inline options like "a) Oxytocin b) Prostaglandins c) Atosiban" 
    or "a. Oxytocin b. Prostaglandins c. Atosiban" from question text.
    Returns (cleaned_question_text, list_of_options).
    """
    # Find the first option marker (a), b), etc)
    first_opt = re.search(r'\b([a-e])\)\s', q_text)
    sep = r'(?=[a-e]\)\s)'
    opt_re = r'^[a-e]\)'
    
    # Also try dot format with uppercase following
    if not first_opt:
        first_opt = re.search(r'\b([a-e])\.\s(?=[A-Z])', q_text)
        if first_opt:
            sep = r'(?=[a-e]\.\s)'
            opt_re = r'^[a-e]\.\s'
    
    if not first_opt:
        return q_text, []
    
    # Split: everything before first option marker is the question
    opt_start = first_opt.start()
    question = q_text[:opt_start].strip()
    opts_text = q_text[opt_start:]
    
    # Split on each option boundary
    parts = re.split(sep, opts_text)
    options = [p.strip() for p in parts if p.strip() and re.match(opt_re, p.strip())]
    
    # Clean question of trailing colon/comma/space
    question = re.sub(r'[:,\s]+$', '', question).strip()
    
    return question, options


def parse_md_file(filepath: str) -> list:
    """Parse an MD file and return list of (qnum, q_text, options) tuples."""
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    
    # Split into question blocks
    pattern = re.compile(r'^## Question (\d+)\n', re.MULTILINE)
    blocks = pattern.split(content)
    
    entries = []
    for i in range(1, len(blocks), 2):
        qnum = blocks[i]
        body = blocks[i+1]
        
        # Skip table content (blockquotes)
        if body.strip().startswith('>'):
            continue
        
        # Extract question text (first line after heading, before **Options:**)
        lines = body.strip().split('\n')
        
        q_lines = []
        opts = []
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
                    opt_text = stripped[2:].strip()
                    opts.append(opt_text)
            else:
                q_lines.append(stripped)
        
        if in_table_block:
            continue
        
        q_text = ' '.join(q_lines).strip()
        
        # Skip non-MCQ entries
        skip_patterns = [
            r'^Final \d+$',
            r'^اَلْحَمْدُ',
            r'^Old Quizzes$',
            r'^Quizzes \d+',
            r'^Inverted Questions$',
            r'^Family Medicine$',
            r'^Case \d+$',
        ]
        if any(re.match(p, q_text) for p in skip_patterns):
            continue
        if len(q_text) < 5:
            continue
        
        entries.append((int(qnum), q_text, opts))
    
    return entries


def process_entry(qnum: int, q_text: str, opts: list) -> dict:
    """Process a single MCQ entry: extract inline options, add distractors if needed."""
    result = {'qnum': qnum, 'q_text': q_text, 'options': [], 'original_opts': len(opts)}
    
    all_opts_raw = list(opts)
    
    # Look for inline options in the question text
    cleaned_text, inline_opts = extract_inline_options(q_text)
    result['q_text'] = cleaned_text
    
    # Parse inline options to extract clean text (without a) b) prefix)
    for io in inline_opts:
        clean = re.sub(r'^[a-e][\)\.]\s*', '', io).strip()
        all_opts_raw.append(clean)
    
    # Clean all options
    all_opts_clean = []
    for opt in all_opts_raw:
        cleaned = re.sub(r'^[a-e][\)\.]\s*', '', opt).strip()
        cleaned = re.sub(r'^- ', '', cleaned).strip()
        if cleaned:
            all_opts_clean.append(cleaned)
    
    all_opts = all_opts_clean
    
    # If we have < 3 options and at least 1 real option, add distractors
    if len(all_opts) < 3 and len(all_opts) > 0:
        extras = generate_distractors(result['q_text'], all_opts, 4)
        all_opts.extend(extras)
        result['added_options'] = len(extras)
    
    # If zero options after extraction, skip essay questions
    if len(all_opts) == 0:
        essay_patterns = [
            r'enumerate', r'list ', r'mention', r'define', r'describe',
            r'outline', r'explain', r'name the',
            r'components of', r'causes of',
        ]
        q_lower = q_text.lower()
        if any(re.search(p, q_lower) for p in essay_patterns):
            result['skip'] = True
            return result
        # Also skip questions with no options at all
        result['skip'] = True
        return result
    
    result['options'] = all_opts
    result['skip'] = False
    return result


def write_mcqs_md(input_fname: str, entries: list):
    """Write processed MCQs to a new MD file with proper labeled options."""
    basename = input_fname.replace('.md', ' - MCQs Only.md')
    outpath = os.path.join(WORKDIR, basename)
    
    source_label = input_fname.replace('.md', '')
    
    lines = []
    lines.append(f"# SUPPORT 41 — Obstetrics {source_label} — MCQs Only")
    lines.append("")
    lines.append(f"*Extracted and cleaned from `{input_fname}`. Only questions with options included.*")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    q_count = 0
    added_count = 0
    skipped_essay = 0
    
    # Labels for options
    opt_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    
    for entry in entries:
        if entry.get('skip'):
            skipped_essay += 1
            continue
        
        q_count += 1
        added = entry.get('added_options', 0)
        if added > 0:
            added_count += 1
        
        lines.append(f"## Question {q_count}")
        lines.append("")
        lines.append(entry['q_text'])
        lines.append("")
        if entry['options']:
            lines.append("**Options:**")
            lines.append("")
            for i, opt in enumerate(entry['options']):
                label = opt_labels[i] if i < len(opt_labels) else chr(ord('a') + i)
                lines.append(f"- {label}) {opt}")
            lines.append("")
    
    if skipped_essay > 0:
        lines.append("---")
        lines.append(f"\n*{skipped_essay} essay/case questions skipped (no options to extract).*\n")
    
    if added_count > 0:
        lines.append("")
        lines.append(f"*Note: {added_count} questions had <3 options and were supplemented with contextually relevant distractors.*")
        lines.append("")
    
    content = '\n'.join(lines)
    
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return outpath, q_count, added_count, skipped_essay


# ── Main ──
files = ['Exams Qs.md', 'Other Qs.md', 'Quizzes Qs.md']

for fname in files:
    filepath = os.path.join(WORKDIR, fname)
    print(f"\n{'='*60}")
    print(f"Processing: {fname}")
    
    if not os.path.exists(filepath):
        print(f"  File not found, skipping.")
        continue
    
    raw_entries = parse_md_file(filepath)
    print(f"  Parsed {len(raw_entries)} question blocks")
    
    processed = []
    for qnum, q_text, opts in raw_entries:
        result = process_entry(qnum, q_text, opts)
        processed.append(result)
    
    outpath, mcq_count, added_count, skipped = write_mcqs_md(fname, processed)
    print(f"  MCQs written: {mcq_count}")
    print(f"  Questions with added options: {added_count}")
    print(f"  Essay questions skipped: {skipped}")
    print(f"  Written to: {outpath}")

print(f"\n{'='*60}")
print("Done! All files saved in:")
print(WORKDIR)
