#!/usr/bin/env python3
"""
Inject 2-4 MCQs per content section into all 7 Week 5 obstetrics files.
"""
import json, os, sys
sys.path.insert(0, '/media/mohamed/projects3/projects/obstaric/obs app')
from inject_mcqs import process_file

BASE = "/media/mohamed/projects3/projects/obstaric/obs app/extracted/assets/second task/obstetric/Week5"
ENH  = "/media/mohamed/projects3/projects/obstaric/obs app/enhanced-assets/second task/obstetric/Week5"

# ─── FILE 36: Third Stage Complications ───
mcqs_36 = {
  "s2": [
    {"q": "Which of the following BEST defines primary postpartum hemorrhage (PPH)?", "options": [
      "Blood loss >500 mL within the first 24 hours after delivery",
      "Blood loss >1000 mL within the first 24 hours after delivery",
      "Blood loss >500 mL from 24 hours to 6 weeks postpartum",
      "Blood loss >1000 mL regardless of timing"
    ], "correct": 0, "explain": "Primary PPH is defined as blood loss >500 mL within the first 24 hours after delivery."},
    {"q": "The most common cause of primary postpartum hemorrhage is:", "options": [
      "Trauma (lacerations/rupture)",
      "Uterine atony",
      "Retained placenta",
      "Coagulopathy (the 4th T)"
    ], "correct": 1, "explain": "Uterine atony accounts for approximately 70-80% of primary PPH cases."},
    {"q": "Which statement about PPH types is TRUE?", "options": [
      "Primary PPH occurs after 24 hours up to 6 weeks",
      "Secondary PPH occurs within the first 24 hours",
      "Primary PPH occurs within the first 24 hours after delivery",
      "Secondary PPH is always due to trauma"
    ], "correct": 2, "explain": "Primary PPH = first 24 hours; Secondary PPH = after 24 hours up to 6 weeks."}
  ],
  "s3": [
    {"q": "The '4 T's' of primary PPH etiology include all EXCEPT:", "options": [
      "Tone (uterine atony)",
      "Trauma (lacerations, rupture)",
      "Tissue (retained placenta)",
      "Toxins (sepsis)"
    ], "correct": 3, "explain": "The 4 T's are: Tone (atony), Trauma, Tissue (retained), and Thrombin (coagulopathy)."},
    {"q": "Which of the following is a risk factor for uterine atony?", "options": [
      "Prolonged labor",
      "Placenta previa",
      "Multiple pregnancy",
      "All of the above"
    ], "correct": 3, "explain": "All are risk factors. Overdistension (twins/polyhydramnios), prolonged labor, and placental abnormalities all predispose to atony."},
    {"q": "The most common type of PPH is due to:", "options": [
      "Coagulation disorders",
      "Genital tract trauma",
      "Uterine atony",
      "Retained placental tissue"
    ], "correct": 2, "explain": "Atonic PPH (uterine atony) is the single most common cause, accounting for ~80% of primary PPH."}
  ],
  "s4": [
    {"q": "The fastest bedside differentiator between atonic and traumatic PPH is:", "options": [
      "Color of the blood (dark vs bright red)",
      "Uterine tone (soft/boggy vs contracted)",
      "Amount of blood loss",
      "Maternal heart rate"
    ], "correct": 1, "explain": "A soft, boggy uterus = atony; a firm, contracted uterus with ongoing bleeding = trauma until proven otherwise."},
    {"q": "Which of the following is a preventive measure for PPH during labor?", "options": [
      "Correction of anemia in pregnancy",
      "Routine use of uterotonics (oxytocin) after delivery of the baby",
      "Exploration of the birth canal after delivery",
      "Careful observation in the 4th stage of labor"
    ], "correct": 1, "explain": "Routine uterotonics after delivery of the baby is the key intrapartum preventive measure. The other options are also valid but belong to different phases."}
  ],
  "s5": [
    {"q": "Which uterotonic is contraindicated in a woman with preeclampsia and PPH?", "options": [
      "Oxytocin",
      "Misoprostol",
      "Methylergonovine (Methergine)",
      "Carboprost"
    ], "correct": 2, "explain": "Ergot alkaloids (methylergonovine/ergometrine) are contraindicated in hypertension/preeclampsia as they raise blood pressure. Safe options: oxytocin and misoprostol."},
    {"q": "What is the FIRST step in managing atonic PPH?", "options": [
      "B-Lynch suture",
      "Uterine massage",
      "Hysterectomy",
      "Balloon tamponade"
    ], "correct": 1, "explain": "Uterine massage is the first-line mechanical treatment. The stepwise approach is: massage → aortic compression if severe → medications → surgery/balloon."},
    {"q": "Oxytocin is considered first-line medical treatment for PPH. Its recommended dose is:", "options": [
      "0.2-0.4 mg IM",
      "10-40 IU IM or IV drip",
      "0.25 mg intramyometrially",
      "200-1000 mcg sublingual"
    ], "correct": 1, "explain": "Oxytocin dose: 10-40 IU IM or IV drip. Options A, C, D correspond to ergometrine, carboprost, and misoprostol respectively."}
  ],
  "s6": [
    {"q": "Secondary postpartum hemorrhage is defined as bleeding after the first 24 hours up to:", "options": [
      "2 weeks postpartum",
      "6 weeks postpartum (end of puerperium)",
      "3 months postpartum",
      "1 year postpartum"
    ], "correct": 1, "explain": "Secondary PPH is bleeding after 24 hours until 6 weeks (end of puerperium). Its etiology is fundamentally different: infection + retention."},
    {"q": "Which of the following is a late complication of massive PPH?", "options": [
      "Transfusion-related lung injury",
      "Sheehan syndrome (postpartum hypopituitarism)",
      "Infections",
      "Hemolytic transfusion reaction"
    ], "correct": 1, "explain": "Sheehan syndrome = ischemic pituitary infarction following massive hemorrhage, leading to panhypopituitarism. The others are early/management-related complications."}
  ],
  "s7": [
    {"q": "Uterine inversion is defined as:", "options": [
      "Prolapse of the uterus into the vagina",
      "Collapse of the fundus into the uterine cavity — the uterus is turned inside out",
      "Retroversion of the gravid uterus",
      "Rupture of the lower uterine segment"
    ], "correct": 1, "explain": "Uterine inversion: the fundus collapses into the uterine cavity, turning the uterus inside outward."},
    {"q": "The MOST common cause of uterine inversion is:", "options": [
      "Spontaneous inversion from precipitate labor",
      "Iatrogenic — excessive cord traction with fundal placental attachment",
      "Severe coughing postpartum",
      "Short umbilical cord"
    ], "correct": 1, "explain": "Iatrogenic inversion (most common) from excessive cord traction with a fundal placenta or fundal pressure on a relaxed uterus."},
    {"q": "In 1st degree uterine inversion, the fundus is:", "options": [
      "Depressed within the endometrial cavity",
      "Protruding through the cervical os",
      "Protruding to or beyond the introitus",
      "Outside the vagina completely"
    ], "correct": 0, "explain": "1st degree (incomplete) = fundus depressed within endometrial cavity; 2nd = through cervical os; 3rd = to/beyond introitus."}
  ],
  "s8": [
    {"q": "Retained placenta is defined as failure of the placenta to spontaneously separate within:", "options": [
      "15 minutes after delivery of the fetus",
      "30 minutes after delivery of the fetus",
      "1 hour after delivery of the fetus",
      "Immediately after delivery of the fetus"
    ], "correct": 1, "explain": "Retained placenta = placenta fails to separate within 30 minutes after delivery of the fetus. It is the second leading cause of PPH."},
    {"q": "In placenta accreta, the chorionic villi penetrate:", "options": [
      "Up to the peritoneal coat",
      "The superficial layer of the myometrium",
      "The deep layer of the myometrium",
      "Only the decidua basalis"
    ], "correct": 1, "explain": "P. accreta = villi penetrate superficial myometrium; P. increta = deep myometrium; P. percreta = up to peritoneal coat."},
    {"q": "Which of the following is a cause of postpartum collapse?", "options": [
      "Amniotic fluid embolism",
      "Pulmonary embolism",
      "Rupture of the uterus",
      "All of the above"
    ], "correct": 3, "explain": "Postpartum collapse has 8 causes including anesthetic complications, MI, pulmonary embolism, AFE, rupture uterus, eclampsia, massive hemorrhage, and sepsis."}
  ]
}

# ─── FILE 37: Amniotic Fluid Embolism ───
mcqs_37 = {
  "s2": [
    {"q": "Amniotic fluid embolism (AFE) is BEST described as:", "options": [
      "A true mechanical obstruction of pulmonary arteries by fetal debris",
      "An anaphylactoid reaction to fetal fluid/tissue entering maternal circulation via the placental bed",
      "A form of septic shock",
      "A type of venous thromboembolism"
    ], "correct": 1, "explain": "AFE is an anaphylactoid (not purely embolic) reaction to fetal antigens. Modern term: 'anaphylactoid syndrome of pregnancy'."},
    {"q": "What is the approximate incidence of AFE?", "options": [
      "1-2 per 1,000 deliveries",
      "1-2 per 40,000 deliveries",
      "1 per 1,000 deliveries per year",
      "1 per 10,000 deliveries"
    ], "correct": 1, "explain": "AFE is rare (~1-2 per 40,000 deliveries) but accounts for 5-15% of maternal deaths in developed countries."}
  ],
  "s3": [
    {"q": "Which TWO conditions allow amniotic fluid to enter maternal circulation?", "options": [
      "Increased intrauterine pressure and opened uterine/endocervical veins",
      "Decreased intrauterine pressure and placental abruption",
      "Fetal distress and meconium staining",
      "Prolonged labor and maternal fever"
    ], "correct": 0, "explain": "Two gateway mechanisms: (1) increased intrauterine pressure (abruption, oxytocin overdose), (2) opened uterine/endocervical veins (lacerations, rupture)."},
    {"q": "Meconium in the setting of AFE:", "options": [
      "Is the primary cause of AFE",
      "Potentiates the toxic nature of amniotic fluid and worsens the condition",
      "Has no effect on the severity",
      "Protects against the anaphylactoid reaction"
    ], "correct": 1, "explain": "Meconium potentiates, does not initiate. It contains vasoactive substances that amplify the anaphylactoid reaction."}
  ],
  "s4": [
    {"q": "The pathophysiologic cascade of AFE begins with entry of AF into maternal veins, followed by:", "options": [
      "Acute cor pulmonale → anaphylaxis → DIC → hypoxia → death",
      "Acute anaphylactoid reaction → pulmonary vascular obstruction → acute cor pulmonale → hypoxia/cardiogenic shock → DIC → coma/death",
      "DIC → pulmonary obstruction → anaphylaxis → death",
      "Hypoxia → DIC → anaphylaxis → cor pulmonale → death"
    ], "correct": 1, "explain": "Correct cascade: Entry → Anaphylaxis → Pulmonary obstruction → Cor pulmonale → Hypoxia/Shock → DIC → Coma/death."},
    {"q": "In AFE, acute cor pulmonale results from:", "options": [
      "Left ventricular failure",
      "Abrupt increase in right ventricular afterload with decreased LV preload",
      "Pulmonary venous hypertension",
      "Myocardial infarction"
    ], "correct": 1, "explain": "Pulmonary vascular obstruction causes abrupt ↑ RV afterload and ↓ LV preload, leading to acute cor pulmonale."},
    {"q": "The final common pathway before death in AFE is:", "options": [
      "Renal failure",
      "Hepatic failure",
      "Hypoxic brain injury and multi-organ failure with DIC",
      "Cardiac arrhythmia alone"
    ], "correct": 2, "explain": "Step 7 of the cascade: deep coma → death from hypoxic brain injury and multi-organ failure. Immediate death occurs in >50% of cases."}
  ],
  "s5": [
    {"q": "Which of the following is a risk factor for AFE?", "options": [
      "Placenta previa",
      "Placental abruption",
      "Headache and visual disturbances",
      "Premature rupture of membranes"
    ], "correct": 1, "explain": "Placental abruption is a key risk factor as disruption of the placental barrier allows AF entry. Other RFs include operative delivery, cervical lacerations."},
    {"q": "Which of the following BEST describes AFE risk factor timing?", "options": [
      "Only occurs in the first trimester",
      "Only occurs during cesarean section",
      "Associated with conditions that disrupt the placental barrier or increase intrauterine pressure",
      "Primarily seen in post-term pregnancies"
    ], "correct": 2, "explain": "Any condition disrupting the placental bed (abruption, trauma, lacerations) or raising intrauterine pressure can precipitate AFE."}
  ],
  "s6": [
    {"q": "The classic clinical triad of AFE is:", "options": [
      "Fever, tachycardia, hypotension",
      "Hypoxia, cardiovascular collapse, DIC",
      "Bradycardia, hypertension, hyperthermia",
      "Chest pain, hemoptysis, dyspnea"
    ], "correct": 1, "explain": "The classic triad: hypoxia (severe dyspnea/cyanosis) + cardiovascular collapse + DIC, occurring within minutes of a difficult delivery."},
    {"q": "The hallmark cardiovascular finding in AFE is:", "options": [
      "Hypertension and bradycardia",
      "Hypotension, tachycardia, and signs of right heart failure",
      "Atrial fibrillation",
      "Widened pulse pressure"
    ], "correct": 1, "explain": "Cardiovascular: hypotension, tachycardia, signs of right heart failure from acute cor pulmonale."}
  ],
  "s7": [
    {"q": "Which laboratory finding is most consistent with DIC in AFE?", "options": [
      "Elevated fibrinogen, normal PT/PTT",
      "Prolonged PT/PTT, low fibrinogen, elevated D-dimer",
      "Normal PT/PTT, elevated platelets",
      "Low D-dimer, normal PT/PTT"
    ], "correct": 1, "explain": "DIC shows: ↑↑ PT/PTT, ↓↓ fibrinogen, ↑↑ D-dimer, ↓ platelets. This guides blood-product replacement."},
    {"q": "The definitive diagnostic finding for AFE is:", "options": [
      "CT chest showing pulmonary infiltrates",
      "Low serum calcium",
      "Identification of amniotic fluid debris (fetal squamous cells, lanugo, vernix) in pulmonary vessels at autopsy",
      "Elevated serum tryptase"
    ], "correct": 2, "explain": "Autopsy finding of AF debris in pulmonary vessels is the only histopathologically confirmatory test. In survivors, diagnosis remains presumptive."}
  ]
}

# ─── FILE 38: Normal and Abnormal Puerperium ───
mcqs_38 = {
  "s2": [
    {"q": "The puerperium is defined as:", "options": [
      "The period from delivery until 2 weeks postpartum",
      "The time from delivery until 6 weeks (42 days) postpartum",
      "The period of labor and delivery",
      "The first 24 hours after delivery"
    ], "correct": 1, "explain": "Puerperium = time from delivery till 6 weeks (42 days) postpartum when pregnancy changes resolve and the body reverts to the non-pregnant state."},
    {"q": "Which statement about the puerperium is TRUE?", "options": [
      "All pregnancy changes reverse within 2 weeks",
      "Six weeks is the standard duration of the puerperium",
      "Lactation prevents all uterine involution",
      "The uterus returns to normal size by 2 weeks"
    ], "correct": 1, "explain": "Six weeks is the standard duration. Uterine involution takes the full 6 weeks (1000g at delivery → 60-80g by 6 weeks)."}
  ],
  "s3": [
    {"q": "Immediately after labor, the uterine fundus is at:", "options": [
      "The xiphisternum",
      "The umbilicus",
      "2 cm below the umbilicus",
      "The symphysis pubis"
    ], "correct": 1, "explain": "Immediately after labor the fundus is at the umbilicus. It descends ~1-2 cm per day and should not be palpable abdominally by day 10-14."},
    {"q": "The uterine weight at the end of the puerperium is:", "options": [
      "1000 g",
      "500 g",
      "250 g",
      "60-80 g"
    ], "correct": 3, "explain": "Uterine involution: 1000 g (immediately) → 500 g (1 wk) → 250 g (2 wks) → 60-80 g (6 wks, non-pregnant)."},
    {"q": "In non-lactating women, ovulation and menses typically return:", "options": [
      "Within 4 weeks",
      "1.5-2 months postpartum",
      "6 months postpartum",
      "12 months postpartum"
    ], "correct": 1, "explain": "Non-lactating: menses return at 1.5-2 months. Lactating: 6 months or earlier (LAM criteria apply)."}
  ],
  "s4": [
    {"q": "Which of the following is a normal general body change during the puerperium?", "options": [
      "Bradycardia (<60 bpm) is common in the first week",
      "Tachycardia always indicates infection",
      "Striae remain red and prominent",
      "Blood volume increases"
    ], "correct": 0, "explain": "Bradycardia (not tachycardia) is normal in early puerperium. Tachycardia >100 bpm suggests infection or anemia."},
    {"q": "After-pains in the puerperium are:", "options": [
      "Abnormal and require investigation",
      "Painful uterine contractions that increase with suckling due to oxytocin release",
      "Always a sign of retained products",
      "Treated with oxytocin"
    ], "correct": 1, "explain": "After-pains are normal painful contractions, increasing with suckling (oxytocin release). Commoner in multiparas."}
  ],
  "s6": [
    {"q": "How frequently should uterine massage and bleeding monitoring be done in the immediate postpartum period?", "options": [
      "Every 5 minutes for 30 minutes",
      "Every 15 minutes for at least 1 hour",
      "Every 30 minutes for 2 hours",
      "Once on the first day"
    ], "correct": 1, "explain": "Every 15 min for at least 1 hr — this covers the highest-risk window for primary PPH."},
    {"q": "Anti-D immunoglobulin should be given to Rh-negative mothers with Rh-positive babies within:", "options": [
      "24 hours",
      "72 hours post-delivery",
      "1 week",
      "At the 6-week check"
    ], "correct": 1, "explain": "Anti-D must be given within the first 72 hours post-delivery. Ideally dose by Kleihauer-Betke test if fetomaternal hemorrhage is suspected."},
    {"q": "Which of the following is part of the 11-pillar management of normal puerperium?", "options": [
      "Semi-sitting position to encourage lochia drainage",
      "NPO for 24 hours after vaginal delivery",
      "Ambulation should be avoided for 3 days",
      "Constipation is encouraged to promote uterine involution"
    ], "correct": 0, "explain": "Semi-sitting position encourages drainage of lochia. Diet is allowed 2 hrs after uncomplicated vaginal delivery and ambulation is encouraged to prevent DVT."}
  ],
  "s7": [
    {"q": "The MOST common cause of puerperal pyrexia is:", "options": [
      "Puerperal sepsis",
      "Milk engorgement",
      "Urinary tract infection",
      "Respiratory infection"
    ], "correct": 1, "explain": "Milk engorgement (days 3-5) is the most common cause. However, puerperal sepsis is the most serious — 'sepsis until proved otherwise' is the rule."},
    {"q": "Puerperal pyrexia is defined as temperature of ≥38°C lasting ≥24 hours during the first:", "options": [
      "3 days of puerperium",
      "7 days of puerperium",
      "10 days of puerperium",
      "14 days of puerperium"
    ], "correct": 2, "explain": "Definition: temperature reaching 38°C or more AND lasting 24 hours or more during the first 10 days of puerperium."},
    {"q": "Which of the following is NOT a cause of uterine subinvolution?", "options": [
      "Retained placental fragments",
      "Infection",
      "Antepartum overdistension (e.g. multiple pregnancy)",
      "Lactation"
    ], "correct": 3, "explain": "Subinvolution causes (RIAN): Retained products, Infection, Antepartum overdistension, Non-lactating women. Lactation actually promotes involution."}
  ]
}

# ─── FILE 39: Puerperal Sepsis ───
mcqs_39 = {
  "s2": [
    {"q": "Puerperal sepsis is defined as:", "options": [
      "Any fever after childbirth",
      "A genital tract infection resulting from bacterial invasion during or after labor or abortion",
      "A urinary tract infection after delivery",
      "Wound infection after cesarean section"
    ], "correct": 1, "explain": "Puerperal sepsis is specifically a genital tract infection from bacterial invasion during or after labor or abortion."},
    {"q": "The timing window for puerperal sepsis includes:", "options": [
      "Only during labor",
      "During labor, after labor, or after abortion",
      "Only after hospital discharge",
      "Only before delivery"
    ], "correct": 1, "explain": "The timing window is broad: during labor, after labor, or after abortion."}
  ],
  "s3": [
    {"q": "The single most common causative organism in puerperal sepsis is:", "options": [
      "E. coli",
      "Staphylococcus aureus",
      "Anaerobic streptococci",
      "Clostridium welchii"
    ], "correct": 2, "explain": "Anaerobic streptococci is the single most common organism. Remember the mnemonic A-G-A: Aerobic Gram+/Gram−, Anaerobic Gram+ (commonest) + Gram−."},
    {"q": "Which of the following is an anaerobic Gram-negative organism causing puerperal sepsis?", "options": [
      "Hemolytic streptococcus group A",
      "Staphylococcus aureus",
      "Clostridium welchii",
      "E. coli"
    ], "correct": 2, "explain": "Clostridium welchii and Bacteroids are anaerobic Gram-negative organisms. Hemolytic streptococcus A and Staph aureus are aerobic Gram-positive."}
  ],
  "s4": [
    {"q": "The endogenous source of puerperal sepsis is:", "options": [
      "Infection from hospital instruments",
      "Infected attendants and dust",
      "Anaerobic streptococci normally present in the genital tract that become pathogenic in devitalized tissue",
      "Contaminated IV lines"
    ], "correct": 2, "explain": "Endogenous: organisms normally present (e.g., anaerobic streptococci) become pathogenic in presence of devitalized tissues."},
    {"q": "Which mode of infection is considered more insidious?", "options": [
      "Exogenous — from instruments and attendants",
      "Endogenous — normal commensals becoming pathogenic",
      "Airborne transmission",
      "Blood transfusion"
    ], "correct": 1, "explain": "The endogenous pathway is more insidious — harmless commensals before delivery become virulent once devitalized tissue provides a substrate."}
  ],
  "s5": [
    {"q": "Which of the following is a local predisposing factor for puerperal sepsis?", "options": [
      "Anemia",
      "Diabetes",
      "Prolonged labor",
      "Debilitating diseases"
    ], "correct": 2, "explain": "Prolonged labor is a local risk factor. Anemia, diabetes, and debilitating diseases are general predisposing factors."},
    {"q": "The mnemonic for local predisposing factors (7) is P-P-I-L-M-R-I. The 'M' stands for:", "options": [
      "Maternal age >35",
      "Marked blood loss",
      "Multiple pregnancy",
      "Malpresentation"
    ], "correct": 1, "explain": "P-P-I-L-M-R-I: PROM, Prolonged labor, Instrumental delivery, Lacerations, Marked blood loss, Retained products, Improper aseptic technique."}
  ],
  "s6": [
    {"q": "The primary sites of puerperal infection include:", "options": [
      "Kidneys and ureters",
      "Lacerations of the vulva/vagina/cervix and the placental site",
      "Lungs and pleura",
      "Heart valves"
    ], "correct": 1, "explain": "Primary sites: (1) lacerations of vulva/vagina/cervix, (2) uterus — placental site or retained products."},
    {"q": "Secondary spread from primary puerperal infection can occur via:", "options": [
      "Direct extension only",
      "Pelvic spread (PID, parametritis, abscess) and blood spread (bacteremia/septicemia)",
      "Lymphatic spread only",
      "Neural spread"
    ], "correct": 1, "explain": "Pelvic spread → acute PID, parametritis, pelvic abscess. Blood spread → bacteremia or septicemia."}
  ],
  "s7": [
    {"q": "The classic presentation of puerperal sepsis occurs:", "options": [
      "Immediately after delivery",
      "48-72 hours following labor or abortion",
      "One week postpartum",
      "At the 6-week postnatal check"
    ], "correct": 1, "explain": "Symptoms appear shortly (48-72 hours) following labor or abortion: fever/rigors, abdominal pain, offensive vaginal discharge."},
    {"q": "The diagnostic temperature criterion for puerperal sepsis is:", "options": [
      "Temperature >37.5°C for 12 hours",
      "Temperature >38°C for 24 hours",
      "Temperature >39°C at any single reading",
      "Temperature >40°C"
    ], "correct": 1, "explain": "Temperature >38°C for 24 hours is the key diagnostic criterion on general examination."}
  ],
  "s8": [
    {"q": "An early complication of puerperal sepsis is:", "options": [
      "Chronic pelvic pain",
      "Tubal infertility",
      "Spread to secondary sites e.g. pelvic abscess",
      "Ectopic pregnancy"
    ], "correct": 2, "explain": "Early: spread to secondary sites and complications of septicemia/pyemia. Remote: chronic PID, infertility, dyspareunia."},
    {"q": "Which of the following is a remote complication of puerperal sepsis?", "options": [
      "Pelvic abscess",
      "Septicemia",
      "Chronic pelvic inflammatory disease and infertility",
      "Septic shock"
    ], "correct": 2, "explain": "Remote complications include chronic PID, infertility, dyspareunia, menorrhagia, and intestinal obstruction. Pelvic abscess and septicemia are early."}
  ],
  "s9": [
    {"q": "Essential investigations in suspected puerperal sepsis include all EXCEPT:", "options": [
      "Blood picture (leucocytosis)",
      "Swab from cervix and upper vagina for aerobic and anaerobic culture",
      "Blood culture",
      "CT scan of the abdomen routinely"
    ], "correct": 3, "explain": "Investigations: blood picture, urine analysis/culture, cervical swab (aerobic + anaerobic), blood culture, U/S for retained parts/abscess. CT is not routine."},
    {"q": "Why must cervical swabs cover both aerobic and anaerobic cultures?", "options": [
      "Aerobic organisms are never present",
      "Most cases are caused by anaerobic streptococci which a standard aerobic-only culture would miss",
      "Anaerobic organisms are always drug-resistant",
      "Only anaerobes cause puerperal sepsis"
    ], "correct": 1, "explain": "Anaerobic streptococci are the most common organism. An aerobic-only culture would miss them, leading to incorrect treatment."}
  ],
  "s10": [
    {"q": "Which of the following is an intranatal preventive measure for puerperal sepsis?", "options": [
      "Proper diet and vitamins",
      "Treatment of anemia",
      "Prophylactic antibiotics in PROM and prolonged/instrumental delivery",
      "Care of perineal wounds postpartum"
    ], "correct": 2, "explain": "Intranatal measures: strict asepsis, minimize vaginal exams, avoid excessive blood loss, suture lacerations immediately, prophylactic antibiotics for PROM/prolonged labor."},
    {"q": "The prevention triad for puerperal sepsis follows the order:", "options": [
      "Postnatal → Intranatal → Antenatal",
      "Antenatal → Intranatal → Postnatal",
      "Intranatal → Antenatal → Postnatal",
      "Postnatal → Antenatal → Intranatal"
    ], "correct": 1, "explain": "Chronological triad: Antenatal (diet, treat anemia/infection) → Intranatal (asepsis, antibiotics) → Postnatal (perineal care, isolation)."}
  ],
  "s11": [
    {"q": "The recommended empirical antibiotic regimen for puerperal sepsis includes:", "options": [
      "Metronidazole alone",
      "Broad-spectrum antibiotic (ampicillin/cephalosporin) + gentamycin + metronidazole",
      "Gentamycin alone",
      "Amoxicillin + clavulanic acid alone"
    ], "correct": 1, "explain": "Triple therapy: broad-spectrum (ampicillin/cephalosporin) + gentamycin + metronidazole. Or clindamycin + gentamycin. Metronidazole covers anaerobes."},
    {"q": "Which of the following is a general measure in treating puerperal sepsis?", "options": [
      "Immediate hysterectomy",
      "Isolation in a separate room or fever hospital",
      "High-dose steroids",
      "Heparin therapy"
    ], "correct": 1, "explain": "General measures: isolation, light nutritious diet with plenty of fluids, IV fluids, correction of anemia."},
    {"q": "Antitoxin serum is specifically indicated in puerperal sepsis caused by:", "options": [
      "E. coli",
      "Staphylococcus aureus",
      "Clostridium welchii",
      "Anaerobic streptococci"
    ], "correct": 2, "explain": "Antitoxin serum is given specifically for Cl. welchii infection."}
  ]
}

# ─── FILE 34: Obstructed Labor ───
mcqs_34 = {
  "s2": [
    {"q": "Obstructed labor is defined as:", "options": [
      "Failure of delivery due to weak uterine contractions",
      "Failure of delivery of the fetus in spite of good uterine contractions due to mechanical obstruction",
      "Labor lasting more than 24 hours",
      "Failure of cervical dilation"
    ], "correct": 1, "explain": "Key: 'in spite of good uterine contractions' — obstructed labor is mechanical, not due to inefficient contractions (uterine inertia)."},
    {"q": "Why is it critical to distinguish obstructed labor from prolonged labor due to uterine inertia?", "options": [
      "Both are treated the same way",
      "In obstructed labor, more oxytocin will not help and may rupture the uterus",
      "Obstructed labor only occurs in primigravidas",
      "Prolonged labor always requires cesarean section"
    ], "correct": 1, "explain": "In obstructed labor, more oxytocin will not help and may cause uterine rupture. The definitive treatment is cesarean section."}
  ],
  "s3": [
    {"q": "Which of the following is a maternal cause of obstructed labor?", "options": [
      "Macrosomic baby",
      "Contracted pelvis",
      "Malpresentation",
      "Locked twins"
    ], "correct": 1, "explain": "Maternal (passages) causes: contracted pelvis, abnormal pelvis, pelvic tumor, cervical stenosis, vaginal septum. The others are fetal (passenger) causes."},
    {"q": "Which of the following is a fetal cause of obstructed labor?", "options": [
      "Contracted pelvis",
      "Pelvic tumor",
      "Hydrocephalos (hydrocephalus)",
      "Cervical stenosis"
    ], "correct": 2, "explain": "Fetal causes: macrosomia, malpresentation, malposition, malformed fetus (hydrocephalos, conjoint twins, fetal ascitis), locked twins."}
  ],
  "s4": [
    {"q": "The cardinal vaginal sign of obstructed labor is:", "options": [
      "Complete cervical dilation",
      "Dry and hot vagina",
      "Large caput succedaneum and moulding",
      "Ruptured membranes"
    ], "correct": 2, "explain": "Large caput + moulding = the cardinal vaginal sign. It tells you the head has been trying to descend but the pelvis is too small."},
    {"q": "Which of the following is an abdominal examination finding in obstructed labor?", "options": [
      "Soft, non-tender uterus",
      "Pathological retraction ring (Bandl's ring)",
      "Fetal heart sounds are always normal",
      "Bladder is empty"
    ], "correct": 1, "explain": "Abdominal findings: uterus hard and tender, pathological retraction ring, distended bladder, fetal distress or absent FHS."},
    {"q": "According to the source, the first diagnostic criterion for obstructed labor is labor lasting more than:", "options": [
      "6 hours",
      "12 hours",
      "24 hours",
      "48 hours"
    ], "correct": 1, "explain": "The source's first diagnostic criterion: labor lasting more than 12 hours — an operationalization of the WHO partogram's action line."}
  ],
  "s5": [
    {"q": "The MOST effective single tool for prevention of obstructed labor is:", "options": [
      "Ultrasound at every visit",
      "Strict partogram use",
      "Hospital delivery for all women",
      "Early induction of labor"
    ], "correct": 1, "explain": "The partogram is the single most effective bedside tool for early detection of prolonged labor and prevention of obstructed labor."},
    {"q": "General management of obstructed labor includes all EXCEPT:", "options": [
      "Correction of dehydration with IV fluids",
      "Broad-spectrum antibiotics",
      "Oxytocin augmentation",
      "Assessment of general condition"
    ], "correct": 2, "explain": "Oxytocin augmentation is contraindicated in obstructed labor (may rupture uterus). General management: IV fluids, antibiotics, assess the mother."}
  ],
  "s6": [
    {"q": "A maternal complication of obstructed labor is:", "options": [
      "Neonatal jaundice",
      "Uterine rupture",
      "Fetal fracture",
      "Cerebral palsy"
    ], "correct": 1, "explain": "Maternal complications: uterine rupture, postpartum hemorrhage, puerperal sepsis, vesicovaginal fistula, maternal death."},
    {"q": "A fetal complication of obstructed labor is:", "options": [
      "Maternal sepsis",
      "Vesicovaginal fistula",
      "Asphyxia and neonatal death",
      "Uterine rupture"
    ], "correct": 2, "explain": "Fetal complications: asphyxia, intracranial hemorrhage, fractures, nerve palsies, and neonatal death."}
  ]
}

# ─── FILE 35: Contracted Pelvis ───
mcqs_35 = {
  "s2": [
    {"q": "The anatomical definition of contracted pelvis is:", "options": [
      "A pelvis that interferes with normal childbirth",
      "A pelvis in which one or more diameters is reduced below normal by at least 1 cm",
      "A pelvis with a diagonal conjugate <10 cm",
      "A pelvis with an outlet diameter <8 cm"
    ], "correct": 1, "explain": "Anatomical: diameters reduced ≥1 cm below normal. Obstetric definition adds: interferes with normal childbirth."},
    {"q": "Which definition of contracted pelvis is more clinically relevant?", "options": [
      "The anatomical definition (measurement-based)",
      "The obstetric definition (interferes with the normal mechanism of labor)",
      "Both are equally important",
      "Neither is used in practice"
    ], "correct": 1, "explain": "The obstetric definition is more relevant because it couples the small diameter to interference with childbirth — this changes clinical management."}
  ],
  "s3": [
    {"q": "Naegele's pelvis is characterized by:", "options": [
      "Transversely contracted due to absence of 2 sacral alae",
      "Asymmetric/obliquely contracted due to absence of one sacral ala",
      "Sacrum made of 6 fused segments (high assimilation)",
      "Sacrum made of 4 fused segments (low assimilation)"
    ], "correct": 1, "explain": "Naegele's = asymmetric (one sacral ala missing → oblique contraction). Robert's = bilateral (double Naegele) → transverse contraction."},
    {"q": "Which acquired condition causes contracted pelvis through metabolic bone disease?", "options": [
      "Kyphosis",
      "Scoliosis",
      "Rickets or osteomalacia",
      "Spondylolisthesis"
    ], "correct": 2, "explain": "Rickets/osteomalacia are metabolic diseases affecting pelvic bones. The others (kyphosis, scoliosis, spondylolisthesis) are vertebral column causes."},
    {"q": "Acquired causes of contracted pelvis are classified into three compartments: pelvic bones, vertebral column, and:", "options": [
      "Lower limbs",
      "Joints",
      "Abdominal muscles",
      "Upper limbs"
    ], "correct": 0, "explain": "The B-V-L mnemonic: Bones (pelvic), Vertebrae (column), Legs (lower limb) = the 3 load-bearing columns shaping the pelvis."}
  ],
  "s4": [
    {"q": "Contracted pelvis with only the outlet affected is:", "options": [
      "The most common type",
      "Very rare (about 1% of cases)",
      "Always associated with inlet contraction",
      "The most severe form"
    ], "correct": 1, "explain": "Outlet contraction is the rarest (~1%). Midpelvic contraction is more common. There are 4 levels: inlet, midpelvic, outlet, and both inlet+outlet."},
    {"q": "Pelvic inlet contraction is diagnosed when the diagonal conjugate is:", "options": [
      "<13 cm",
      "<12 cm",
      "<11.5 cm",
      "<10 cm"
    ], "correct": 2, "explain": "Inlet contraction: A-P diameter <10 cm OR transverse <12 cm. Diagnosed by diagonal conjugate <11.5 cm."}
  ],
  "s5": [
    {"q": "In 1st degree contracted pelvis, the conjugate vera is:", "options": [
      "10-11 cm (normal is 11 cm)",
      "9-10 cm",
      "8-9 cm",
      "<8 cm"
    ], "correct": 0, "explain": "Four degrees: 1st (10-11 cm, normal = 11 cm), 2nd (9-10 cm), 3rd (8-9 cm), 4th (<8 cm)."},
    {"q": "A conjugate vera of 7.5 cm corresponds to which degree of pelvic contraction?", "options": [
      "1st degree",
      "2nd degree",
      "3rd degree",
      "4th degree"
    ], "correct": 3, "explain": "4th degree: conjugate vera <8 cm. 1st: 10-11 cm, 2nd: 9-10 cm, 3rd: 8-9 cm, 4th: <8 cm."}
  ],
  "s6": [
    {"q": "Radiological pelvimetry is indicated for:", "options": [
      "All pregnant women",
      "Suspected CPD (cephalo-pelvic disproportion) or cases with previous CS for CPD",
      "Only primigravidas",
      "Only women with breech presentation"
    ], "correct": 1, "explain": "Radiological pelvimetry is indicated for suspected CPD and previous CS for CPD."},
    {"q": "Clinical pelvimetry includes assessment of all EXCEPT:", "options": [
      "Diagonal conjugate",
      "Transverse diameter of inlet",
      "Fetal blood sampling",
      "Bi-spinous and bi-tuberous diameters"
    ], "correct": 2, "explain": "Clinical pelvimetry assesses diagonal conjugate, transverse diameter, bi-spinous, bi-tuberous, and outlet diameters. Fetal blood sampling is not pelvic assessment."}
  ],
  "s7": [
    {"q": "A common complication of contracted pelvis is:", "options": [
      "Preterm labor",
      "Prolonged labor and obstructed labor",
      "Polyhydramnios",
      "Placenta previa"
    ], "correct": 1, "explain": "Complications include prolonged/obstructed labor, postpartum hemorrhage, rupture uterus, puerperal sepsis, vesicovaginal fistula, and fetal complications."},
    {"q": "Which of the following is a fetal complication of contracted pelvis?", "options": [
      "Uterine rupture",
      "Vesicovaginal fistula",
      "Intracranial hemorrhage and nerve palsies",
      "Sepsis"
    ], "correct": 2, "explain": "Fetal: intracranial hemorrhage, nerve palsies, fractures, asphyxia, and neonatal death. Uterine rupture and VVF are maternal complications."}
  ],
  "s8": [
    {"q": "Management of contracted pelvis depends primarily on:", "options": [
      "Maternal age",
      "Degree of contraction and presence of CPD",
      "Fetal gender",
      "Gestational age at diagnosis"
    ], "correct": 1, "explain": "Management depends on degree of contraction and presence of CPD. Trial of labor may be attempted for mild/non-CPD cases; severe cases require CS."},
    {"q": "In mild contracted pelvis without CPD, the recommended approach is:", "options": [
      "Elective cesarean section at 39 weeks",
      "Trial of labor under close monitoring with partograph",
      "Induction of labor at 37 weeks",
      "Immediate cesarean section at diagnosis"
    ], "correct": 1, "explain": "A trial of labor with close partograph monitoring is appropriate for mild cases without CPD. Severe contraction or definite CPD = cesarean section."}
  ]
}

# ─── FILE 44: Fetal Birth Injuries ───
mcqs_44 = {
  "s2": [
    {"q": "Birth trauma is caused by:", "options": [
      "Only maternal factors",
      "Marked compression or sudden compression-decompression during delivery, including iatrogenic causes",
      "Only fetal factors",
      "Always due to congenital anomalies"
    ], "correct": 1, "explain": "Birth trauma arises from the 3 P's (Passages, Passenger, Power) plus iatrogenic causes (instrumental delivery, intrauterine manipulation)."},
    {"q": "Which of the following is an iatrogenic cause of birth trauma?", "options": [
      "Contracted pelvis",
      "Fetal macrosomia",
      "Forceps or ventouse delivery",
      "Precipitate labor"
    ], "correct": 2, "explain": "Iatrogenic: instrumental delivery (ventouse, forceps) and intrauterine manipulation (internal podalic version, breech extraction)."}
  ],
  "s3": [
    {"q": "The most frequent birth fracture is of the:", "options": [
      "Skull",
      "Humerus",
      "Clavicle",
      "Femur"
    ], "correct": 2, "explain": "Hierarchy of frequency: 1. Clavicle, 2. Humerus, 3. Femur, 4. Skull bones. Clavicular fractures are best treated conservatively."},
    {"q": "Skull fractures in the newborn are considered more serious because:", "options": [
      "They never heal",
      "There is a possibility of underlying hemorrhage",
      "Surgery is always required",
      "They always cause neurological deficits"
    ], "correct": 1, "explain": "Skull fractures: possibility of underlying hemorrhage must be considered. The majority of neonatal fractures heal with conservative treatment."}
  ],
  "s4": [
    {"q": "Cephalohematoma results from:", "options": [
      "Edema of the scalp present at birth",
      "Bleeding between the periosteum and skull bone",
      "Bleeding within the brain tissue",
      "Fracture of the skull base"
    ], "correct": 1, "explain": "Cephalohematoma = bleeding between the periosteum and skull bone, taking the shape of the underlying bone. Develops hours/days after birth."},
    {"q": "Which is a key distinguishing feature of cephalohematoma compared to caput succedaneum?", "options": [
      "Present at birth",
      "Crosses suture lines",
      "Develops hours or days after birth",
      "Is always pathological and requires drainage"
    ], "correct": 2, "explain": "Cephalohematoma develops hours-days after birth (vs present at birth for caput), does NOT cross suture lines (caput does), and is usually benign."}
  ],
  "s5": [
    {"q": "Erb-Duchenne palsy is caused by injury to nerve roots:", "options": [
      "C5-C6",
      "C7-C8",
      "C8-T1",
      "L3-L4"
    ], "correct": 0, "explain": "Erb-Duchenne palsy = C5-C6 (upper trunk). Klumpke's palsy = C8-T1 (lower trunk). Total arm paralysis = C5-T1."},
    {"q": "Klumpke's palsy affects which nerve roots?", "options": [
      "C5-C6",
      "C5-C6-C7",
      "C8-T1",
      "C5-T1"
    ], "correct": 2, "explain": "Klumpke's palsy = C8-T1 (lower trunk), affecting hand and forearm muscles. Erb-Duchenne = C5-C6."},
    {"q": "The prognosis for most brachial plexus injuries at birth is:", "options": [
      "Poor — most require surgery",
      "Usually good — most recover spontaneously",
      "Always fatal",
      "Requires lifelong physiotherapy without improvement"
    ], "correct": 1, "explain": "Most neonatal brachial plexus injuries recover spontaneously with conservative management (physiotherapy). Surgery is reserved for persistent cases."}
  ],
  "s6": [
    {"q": "Sternomastoid tumor is associated with:", "options": [
      "Forceps delivery",
      "Difficult delivery, especially with hyperextension of the neck or breech extraction",
      "Vacuum delivery",
      "Normal spontaneous vaginal delivery"
    ], "correct": 1, "explain": "Sternomastoid tumor results from difficult delivery with neck hyperextension or breech extraction, causing hematoma in the sternomastoid muscle."},
    {"q": "Treatment of sternomastoid tumor is:", "options": [
      "Surgical excision",
      "Radiotherapy",
      "Passive stretching exercises and physiotherapy",
      "No treatment required"
    ], "correct": 2, "explain": "Conservative: passive stretching exercises and physiotherapy. Most resolve spontaneously. Surgery only if persistent after 1 year."}
  ],
  "s7": [
    {"q": "Facial lacerations from birth trauma:", "options": [
      "Always require plastic surgery",
      "Usually heal well with conservative measures including cleansing and steri-strips",
      "Never occur in modern obstetrics",
      "Are always due to ventouse cup detachment"
    ], "correct": 1, "explain": "Most facial/soft tissue lacerations heal well with conservative management: cleansing, steri-strips, and observation."},
    {"q": "Scalp lacerations from fetal scalp electrodes or ventouse application:", "options": [
      "Require immediate suturing",
          "Usually heal well with local cleansing and monitoring for infection",
      "Always indicate underlying skull fracture",
      "Should be explored surgically"
    ], "correct": 1, "explain": "Scalp lacerations typically heal well with local cleansing and infection monitoring. The main concern is infection (cellulitis, abscess)."}
  ]
}

# ─── PROCESS ALL FILES ───
files_data = [
    ("Complications_of_3rd_stage_of_labour/36_Third_Stage_Complications.html", mcqs_36),
    ("Complications_of_3rd_stage_of_labour/37_Amniotic_Fluid_Embolism.html", mcqs_37),
    ("Complications_of_3rd_stage_of_labour/38_Normal_and_Abnormal_Puerperium.html", mcqs_38),
    ("Complications_of_3rd_stage_of_labour/39_Puerperal_Sepsis.html", mcqs_39),
    ("Contracted_pelvis_and_obstructed_labour/34_Obstructed_Labor.html", mcqs_34),
    ("Contracted_pelvis_and_obstructed_labour/35_Contracted_Pelvis.html", mcqs_35),
    ("Revision_and_common_obstetric_complaints/44_Fetal_Birth_Injuries.html", mcqs_44),
]

for rel_path, mcqs in files_data:
    input_path = os.path.join(BASE, rel_path)
    output_path = os.path.join(ENH, rel_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    process_file(input_path, output_path, mcqs)

print("\n✅ All 7 Week 5 files processed successfully!")
