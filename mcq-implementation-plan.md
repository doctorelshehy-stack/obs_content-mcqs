# MCQs Implementation Plan — ObsTaric Dashboard

## Goal
Embed 5–10 interactive MCQs acording to bulk of the content after every subtopic (h2/h3 section) in each HTML asset file, creating enhanced copies for the ObsTaric study dashboard.

---

## Phase 1 — Pilot: Week 1 Only

### Objective
Validate the format, quality, and workflow on a small, representative set before scaling.

### Files to process (Week 1 — 7 topics, 12 HTML files)

| Topic | Files |
|---|---|
| Fertilization, Placenta & Membranes | `01_Physiology_of_Reproduction.html` |
| Maternal Adaptation & Diagnosis | `02_Maternal_Adaptation_to_Pregnancy.html`<br>`03_Diagnosis_of_Pregnancy.html`<br>`04_Antenatal_Care.html` |
| Bleeding in Early Pregnancy | `05_Abortion.html`<br>`06_Ectopic_Pregnancy.html`<br>`07_Gestational_Trophoblastic_Disease.html`<br>`16_Thromboembolism_during_Pregnancy.html` |
| Hypertensive Disorders & DIC | `12_Hypertension_with_Pregnancy.html` |
| Diabetes & UTI in Pregnancy | `14_Diabetes_Mellitus_with_Pregnancy.html`<br>`15_UTI_in_Pregnancy.html` |
| Thromboembolism & RH Isoimmunization | `13_Disseminated_Intravascular_Coagulopathy_DIC.html`<br>`45_RH_Incompatibility.html` |

### Steps

1. **Create `enhanced-assets/` directory** — mirror of `assets/second task/obstetric/`
2. **For each HTML file:**
   - Parse the DOM to identify h2 (major subtopic) boundaries
   - For each subtopic, read the content under that heading
   - Generate 5–10 single-best-answer MCQs from the content
   - Build an interactive MCQ block (radio buttons + instant visual feedback)
   - Insert the MCQ block at the end of the subtopic section
   - Write the enhanced file to `enhanced-assets/`
   - exclude ilos and study activty and referances subtopic 
3. **Update dashboard.html** — change `ASSETS_BASE` from `extracted/assets/...` to `enhanced-assets/...`
4. **Review** — open in browser, verify:
   - All 12 files load correctly
   - MCQs appear after each subtopic
   - Interactive feedback works (click → ✓ green / ✗ red, correct shown)
   - Images still render properly

### MCQ Format (Interactive)

```
┌──────────────────────────────────────┐
│ 📝 MCQ 1 of 7                        │
│                                      │
│ Which structure is responsible for   │
│ implantation of the blastocyst?      │
│                                      │
│ ○ A. Trophoblast                     │
│ ○ B. Decidua basalis                 │
│ ○ C. Yolk sac                        │
│ ○ D. Amnion                          │
│                                      │
│   (click one — instant feedback)     │
└──────────────────────────────────────┘
```

- Click an option → wrong turns red ✗, correct turns green ✓
- If wrong chosen, the correct answer also highlights green
- All options lock after first click
- Progress indicator: "MCQ 3 of 7"
- Small explanation shown below after answering

---

## Phase 2 — Week 2 & 3

### Files (29 HTML files)

| Topic | Files |
|---|---|
| Week 2 — Vomiting, Anemia, Cardiac | `09_Vomiting_with_Pregnancy.html`<br>`10_Anemia_with_Pregnancy.html`<br>`11_Cardiac_Diseases_with_Pregnancy.html` |
| Week 2 — Antepartum Hemorrhage | `08_Antepartum_Hemorrhage.html` |
| Week 2 — Fetal Wellbeing | `43_Intrauterine_Fetal_Death.html`<br>`46_Assessment_of_Fetal_Well-being.html` |
| Week 2 — High-Risk Pregnancy | `17_Infectious_Diseases_with_Pregnancy.html`<br>`30_Multiple_Pregnancy.html` |
| Week 2 — Polyhydramnios, IUGR, Shoulder Dystocia | `18_Amniotic_Fluid_Abnormalities.html`<br>`29_Shoulder_Dystocia.html`<br>`40_Intrauterine_Growth_Restriction.html`<br>`42_Macrosomia.html` |
| Week 2 — PROM, Preterm, Post-term | `31_Preterm_Labor.html`<br>`32_Premature_Rupture_of_Membranes_PROM.html`<br>`41_Postterm_Pregnancy.html` |
| Week 3 — Normal Labour | `19_Normal_Labor.html` |
| Week 3 — Pelvis & Fetal Skull | `20_Female_Pelvis.html`<br>`21_Fetal_Skull.html` |
| Week 3 — Malpresentations | `22_Occipitoposterior_Position.html` through `28_Cord_Presentation_and_Prolapse.html` (7 files) |
| Week 3 — Labour Stages, Partogram, FHR | `33_Abnormal_Uterine_Action.html` |
| Week 3 — Operative Obstetrics | `47_Operative_Obstetrics.html`<br>`48_Instruments.html` |
| Week 3 — Family Medicine | `FM01_Premarital_Care.html` through `FM06_Contraceptive_Methods.html` (6 files) |

### Steps
- Same process as Phase 1, applied to remaining Week 2 + Week 3 files
- Reuse the MCQ injection script (refine if needed based on pilot feedback)

---

## Phase 3 — Week 5

### Files (7 HTML files)

| Topic | Files |
|---|---|
| Complications of 3rd Stage of Labour | `36_Third_Stage_Complications.html`<br>`37_Amniotic_Fluid_Embolism.html`<br>`38_Normal_and_Abnormal_Puerperium.html`<br>`39_Puerperal_Sepsis.html` |
| Contracted Pelvis & Obstructed Labour | `34_Obstructed_Labor.html`<br>`35_Contracted_Pelvis.html` |
| Revision & Common Complaints | `44_Fetal_Birth_Injuries.html` |

### Steps
- Same process as previous phases

---

## Implementation Details

### MCQ Generation Strategy
Each MCQ is derived from the content of the subtopic it follows:

| Content Type | MCQ Style |
|---|---|
| Definition | "What is the definition of X?" |
| Classification | "Which of the following is NOT a type of X?" |
| Etiology/Risk factors | "Which is a risk factor for X?" |
| Clinical picture | "Which sign/symptom is characteristic of X?" |
| Management | "What is the first-line management for X?" |
| Complications | "Which of the following is a complication of X?" |

### Interactive MCQ HTML Structure
```html
<div class="mcq-block" data-subtopic="Fertilization">
  <div class="mcq-header">📝 MCQ <span class="mcq-num">1</span> of <span class="mcq-total">7</span></div>
  <p class="mcq-question">Question text here?</p>
  <div class="mcq-options">
    <label class="mcq-option" data-correct="false">
      <input type="radio" name="mcq-1" value="A"> A. Option text
      <span class="mcq-feedback"></span>
    </label>
    <label class="mcq-option" data-correct="true">
      <input type="radio" name="mcq-1" value="B"> B. Correct answer
      <span class="mcq-feedback"></span>
    </label>
    <!-- ... -->
  </div>
  <div class="mcq-explanation" style="display:none">Explanation text.</div>
</div>
```

### CSS (inserted into each enhanced HTML file's `<style>` block)
- Dark/light aware (using CSS variables or `prefers-color-scheme`)
- Card-style MCQ container with subtle border
- Green highlight on correct, red on wrong
- Smooth transition animation on feedback
- Responsive — full-width on mobile

### JavaScript (inserted at end of each enhanced HTML file)
```js
document.querySelectorAll('.mcq-option').forEach(opt => {
  opt.addEventListener('click', function() {
    // Lock all options in this MCQ
    // Mark correct green, wrong red if chosen
    // Show explanation
  });
});
```

---

## Files to Create

| File | Purpose |
|---|---|
| `enhanced-assets/second task/obstetric/Week{N}/.../*.html` | Enhanced copies with MCQs |
| `dashboard-enhanced.html` | Copy of dashboard pointing to enhanced-assets |
| (or patch dashboard.html `ASSETS_BASE` variable) | |

**No original files are modified.**

---

## Effort Estimate

| Phase | Files | Subtopics | MCQs | Cumulative |
|---|---|---|---|---|
| 1 — Pilot (Week 1) | 12 | ~140 | ~700–1,400 | 12 files |
| 2 — Week 2 & 3 | 29 | ~350 | ~1,750–3,500 | 41 files |
| 3 — Week 5 | 7 | ~80 | ~400–800 | 48 files |
| **Total** | **48** | **~570** | **~2,850–5,700** | |

---

## Review & Iterate

After Pilot (Phase 1), collect feedback on:
- MCQ difficulty (too easy / too hard?)
- Number of MCQs per subtopic (5? 7? 10?) 
- Interactive feedback feel
- Any content accuracy issues
- Page load time (with added JS/CSS)
