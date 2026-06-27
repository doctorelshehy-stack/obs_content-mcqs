#!/usr/bin/env python3
"""Generate and inject MCQs for all 10 remaining Week 2 HTML files."""

import sys, os, re, json, copy

# ─── Add working dir to path ───
sys.path.insert(0, '/media/mohamed/projects3/projects/obstaric/obs app')
from inject_mcqs import process_file, build_mcq_block, MCQ_CSS, MCQ_JS

# ─── Constants ───
BASE_IN = '/media/mohamed/projects3/projects/obstaric/obs app/extracted/assets/second task/obstetric/Week2'
BASE_OUT = '/media/mohamed/projects3/projects/obstaric/obs app/enhanced-assets/second task/obstetric/Week2'

# ─── MCQ data per file per section ───
# Each entry: { "section_id": [ {"q":..., "options":[...], "correct":N, "explain":...}, ... ] }

# ===== 1. 18_Amniotic_Fluid_Abnormalities =====
MCQ_18 = {
    "s2": [  # Dynamics & Function
        {"q": "During the first half of pregnancy, amniotic fluid is primarily produced from which source?",
         "options": ["Fetal urination", "Maternal circulation", "Fetal swallowing", "Amniotic epithelium secretion"],
         "correct": 1, "explain": "During the first half of pregnancy, amniotic fluid is derived from maternal circulation. In the second half, fetal urination becomes the main source."},
        {"q": "What is the main route of amniotic fluid resorption during the second half of pregnancy?",
         "options": ["Placental absorption", "Fetal swallowing", "Maternal circulation", "Transmembrane diffusion"],
         "correct": 1, "explain": "Fetal swallowing is the main route of amniotic fluid clearance during the second half of pregnancy."},
        {"q": "Which of the following is a function of amniotic fluid?",
         "options": ["Providing nutrition to the fetus", "Allowing fetal movement and musculoskeletal development", "Producing fetal red blood cells", "Stimulating uterine contractions"],
         "correct": 1, "explain": "Amniotic fluid surrounds the growing fetus, protects from injury and temperature changes, and allows fetal movement, which permits musculoskeletal development."},
        {"q": "The volume of amniotic fluid at any given time depends on the balance between:",
         "options": ["Fetal heart rate and maternal blood pressure", "Production and resorption of amniotic fluid", "Placental size and uterine volume", "Maternal diet and hydration"],
         "correct": 1, "explain": "Amniotic fluid is accumulated in a dynamic manner and its volume depends on the balance between production and resorption."},
    ],
    "s3": [  # Poly vs Oligo Comparison
        {"q": "What is the definition of polyhydramnios in terms of amniotic fluid volume?",
         "options": ["AFV < 500 mL", "AFV > 2,000 mL", "AFV > 1,000 mL", "AFV < 200 mL"],
         "correct": 1, "explain": "Polyhydramnios is defined as excess accumulation of amniotic fluid with AFV > 2,000 mL. Oligohydramnios is AFV < 500 mL."},
        {"q": "Which of the following is the most common cause of both polyhydramnios and oligohydramnios?",
         "options": ["Diabetes mellitus", "Fetal malformations", "Idiopathic", "Post-term pregnancy"],
         "correct": 2, "explain": "Idiopathic (unknown cause) is the most common etiology for both polyhydramnios and oligohydramnios."},
        {"q": "Which fetal malformation is associated with polyhydramnios?",
         "options": ["Renal agenesis", "Esophageal atresia", "PROM", "Placental insufficiency"],
         "correct": 1, "explain": "Esophageal and duodenal atresia (and anencephaly) are fetal malformations associated with polyhydramnios because the fetus cannot swallow and resorb amniotic fluid properly."},
        {"q": "On abdominal examination, which finding is characteristic of polyhydramnios?",
         "options": ["Uterus smaller than period of amenorrhea", "Easy palpation of fetal parts", "Difficult auscultation of FHS", "Easy auscultation of FHS"],
         "correct": 2, "explain": "In polyhydramnios, the uterus is larger than dates, fetal parts are difficult to palpate, and auscultation of FHS is difficult due to the excess fluid."},
        {"q": "Which investigation is recommended for polyhydramnios?",
         "options": ["Leukocytic count", "75 g oral glucose tolerance test", "Umbilical artery Doppler", "Amniocentesis for karyotype"],
         "correct": 1, "explain": "A 75 g oral glucose tolerance test is recommended to screen for diabetes mellitus as a cause of polyhydramnios."},
    ],
    "s4": [  # SDP & AFI
        {"q": "What is the SDP (Single Deepest Pocket) cutoff for diagnosing oligohydramnios?",
         "options": ["SDP < 1 cm", "SDP < 2 cm", "SDP < 3 cm", "SDP < 5 cm"],
         "correct": 1, "explain": "SDP < 2 cm = oligohydramnios. SDP between 2-8 cm = normal. SDP > 8 cm = polyhydramnios."},
        {"q": "What is the AFI cutoff for diagnosing polyhydramnios?",
         "options": ["AFI > 20 cm", "AFI > 25 cm", "AFI > 30 cm", "AFI > 15 cm"],
         "correct": 1, "explain": "AFI > 25 cm = polyhydramnios. AFI < 5 cm = oligohydramnios. AFI 10-20 cm = normal."},
        {"q": "The AFI is calculated by measuring the deepest vertical pocket in how many quadrants?",
         "options": ["2 quadrants", "3 quadrants", "4 quadrants", "1 quadrant"],
         "correct": 2, "explain": "AFI uses the 4-quadrant method: the deepest amniotic pocket in each of the four quadrants is measured vertically and the values are added together."},
        {"q": "What is the normal SDP range?",
         "options": ["1-5 cm", "2-8 cm", "3-10 cm", "5-15 cm"],
         "correct": 1, "explain": "Normal SDP is between 2 and 8 cm."},
    ],
    "s5": [  # Complications
        {"q": "Which of the following is a shared complication of both polyhydramnios and oligohydramnios?",
         "options": ["Pulmonary hypoplasia", "Umbilical cord prolapse", "Preterm labor", "Postpartum hemorrhage"],
         "correct": 2, "explain": "Both polyhydramnios and oligohydramnios share preterm labor and abnormal fetal presentation as complications."},
        {"q": "Which complication is specific to polyhydramnios and results from sudden uterine decompression after ROM?",
         "options": ["Pulmonary hypoplasia", "Umbilical cord prolapse", "Fetal growth restriction", "Post-term pregnancy"],
         "correct": 1, "explain": "Umbilical cord prolapse is a specific complication of polyhydramnios that occurs when there is sudden decompression of the overdistended uterus after rupture of membranes."},
        {"q": "Pulmonary hypoplasia is a major complication of which condition?",
         "options": ["Polyhydramnios", "Oligohydramnios", "Diabetes mellitus", "Multiple pregnancy"],
         "correct": 1, "explain": "Pulmonary hypoplasia is a major complication of oligohydramnios — the fetus needs amniotic fluid for normal lung development, and severe oligohydramnios impairs alveolar formation."},
        {"q": "Which maternal complication is associated with polyhydramnios?",
         "options": ["Pulmonary hypoplasia", "Maternal dyspnea", "Fetal renal agenesis", "Placental insufficiency"],
         "correct": 1, "explain": "Maternal dyspnea occurs in polyhydramnios due to diaphragmatic splinting from the overdistended uterus."},
    ],
    "s6": [  # Management
        {"q": "Which intervention is used for management of polyhydramnios?",
         "options": ["Amnio-infusion", "Amnio-reduction", "Maternal rehydration", "Indomethacin"],
         "correct": 1, "explain": "Amnio-reduction (therapeutic amniocentesis to drain excess fluid) is used to manage polyhydramnios."},
        {"q": "Which management option is specific to oligohydramnios?",
         "options": ["Amnio-reduction", "Prostaglandin synthetase inhibitor", "Amnio-infusion", "Treatment of diabetes"],
         "correct": 2, "explain": "Amnio-infusion (infusing fluid into the amniotic cavity) is used for oligohydramnios, along with maternal rehydration."},
        {"q": "In a post-term pregnancy with oligohydramnios, what is the recommended management?",
         "options": ["Conservative management", "Amnio-infusion", "Termination of pregnancy (delivery)", "Prostaglandin synthetase inhibitor"],
         "correct": 2, "explain": "Post-term pregnancy with oligohydramnios is managed by delivery (termination of pregnancy), as the risk of fetal compromise outweighs the benefit of continued pregnancy."},
        {"q": "Which drug is used in the management of polyhydramnios?",
         "options": ["Magnesium sulfate", "Prostaglandin synthetase inhibitor (Indomethacin)", "Oxytocin", "Nifedipine"],
         "correct": 1, "explain": "Prostaglandin synthetase inhibitors (e.g., Indomethacin) reduce fetal urine production and can decrease amniotic fluid volume in polyhydramnios."},
    ],
}

# ===== 2. 29_Shoulder_Dystocia =====
MCQ_29 = {
    "s2": [  # Definition & Incidence
        {"q": "What is the definition of shoulder dystocia?",
         "options": ["Failure of the fetal head to engage in the pelvic inlet", "Arrested delivery of fetal shoulder after delivery of fetal head requiring additional maneuvers", "Prolonged second stage of labor exceeding 3 hours", "Entrapment of the posterior shoulder behind the sacral promontory"],
         "correct": 1, "explain": "Shoulder dystocia is defined as arrested delivery of the fetal shoulder after delivery of the fetal head, requiring additional maneuvers to deliver the shoulder."},
        {"q": "What is the reported incidence of shoulder dystocia?",
         "options": ["0.1% of deliveries", "0.2-0.3% of deliveries", "1-2% of deliveries", "3-5% of deliveries"],
         "correct": 1, "explain": "Shoulder dystocia occurs in 0.2-0.3% of deliveries and is described as unpredictable and unpreventable."},
        {"q": "Which two adjectives best describe shoulder dystocia?",
         "options": ["Common and predictable", "Unpredictable and unpreventable", "Preventable and treatable", "Rare and benign"],
         "correct": 1, "explain": "Shoulder dystocia is described as unpredictable (cannot be reliably forecast even with known risk factors) and unpreventable (no prophylactic intervention reliably prevents it)."},
    ],
    "s5": [  # Risk factors
        {"q": "Which of the following is an antepartum risk factor for shoulder dystocia?",
         "options": ["Prolonged second stage of labor", "Oxytocin augmentation", "Previous shoulder dystocia", "Assisted vaginal delivery"],
         "correct": 2, "explain": "Previous shoulder dystocia (recurrence rate ~10%), macrosomia, diabetes mellitus, maternal BMI > 30, and induction of labor are the 5 antepartum risk factors."},
        {"q": "Which intrapartum risk factor for shoulder dystocia involves the operator applying force that may pull the head past the shoulders?",
         "options": ["Prolonged first stage", "Secondary arrest", "Oxytocin augmentation", "Assisted vaginal delivery (vacuum/forceps)"],
         "correct": 3, "explain": "Assisted vaginal delivery (vacuum or forceps) increases risk because the operator may pull the head past the shoulders before they have rotated to the oblique diameter."},
        {"q": "What is the single most common risk factor for shoulder dystocia?",
         "options": ["Maternal obesity", "Diabetes mellitus", "Macrosomia (birth weight > 4,000 g)", "Previous shoulder dystocia"],
         "correct": 2, "explain": "Macrosomia (birth weight > 4,000 g, or > 4,500 g in diabetic mothers) is the single most common risk factor for shoulder dystocia."},
        {"q": "How many antepartum and intrapartum risk factors are listed for shoulder dystocia?",
         "options": ["3 antepartum, 3 intrapartum", "5 antepartum, 5 intrapartum", "4 antepartum, 6 intrapartum", "2 antepartum, 8 intrapartum"],
         "correct": 1, "explain": "There are 5 antepartum risk factors (previous SD, macrosomia, DM, BMI > 30, induction) and 5 intrapartum risk factors (prolonged 1st stage, secondary arrest, prolonged 2nd stage, oxytocin augmentation, assisted vaginal delivery)."},
    ],
    "s6": [  # Management steps 1-5
        {"q": "What is the first step in management of shoulder dystocia?",
         "options": ["Perform episiotomy", "Apply McRobert's maneuver", "Call for help", "Deliver the posterior arm"],
         "correct": 2, "explain": "The first step is to call for help — senior obstetrician, pediatric resuscitation team, and anesthetist should be present. The operator must also stop pulling on the head."},
        {"q": "Which maneuver is described as the most effective single intervention for shoulder dystocia, resolving ~90% of cases when combined with suprapubic pressure?",
         "options": ["Delivery of posterior arm", "McRobert's maneuver", "Wood's corkscrew", "Zavanelli maneuver"],
         "correct": 1, "explain": "McRobert's maneuver (hyperflexion and abduction of maternal hips, positioning thighs on abdomen) is the most effective intervention and should be performed first. Combined with suprapubic pressure, it resolves ~90% of cases."},
        {"q": "What is the purpose of episiotomy in shoulder dystocia management?",
         "options": ["It alone resolves the shoulder dystocia", "It enlarges the vaginal opening to facilitate internal manipulation", "It reduces the bisacromial diameter", "It relaxes the uterine muscles"],
         "correct": 1, "explain": "Episiotomy alone does not resolve shoulder dystocia — the obstruction is at the pelvic brim. It enlarges the vaginal opening to give the operator room for internal maneuvers."},
        {"q": "Where is suprapubic pressure applied and in what direction?",
         "options": ["On the uterine fundus, directed downward", "Just above the pubic bone, directed downward and laterally toward the fetal back", "On the maternal abdomen at the level of the umbilicus", "On the perineum, directed upward"],
         "correct": 1, "explain": "Suprapubic pressure is applied by an assistant just above the maternal pubic bone, directed downward and laterally toward the fetal back to adduct the anterior shoulder and rotate it under the pubic symphysis."},
        {"q": "What are the three sub-steps for delivery of the posterior arm?",
         "options": ["Rotate → pull → deliver", "Flex elbow → sweep arm over chest → deliver posterior arm", "Apply traction → rotate shoulder → deliver head", "Push back → rotate → cesarean section"],
         "correct": 1, "explain": "The three sub-steps are: (1) Insert hand and flex the elbow, (2) Sweep arm over the chest, (3) Deliver the posterior arm. This reduces the bisacromial diameter."},
    ],
    "s7": [  # Management steps 6-11
        {"q": "Which internal rotational maneuver involves rotating the anterior fetal shoulder obliquely with a vaginal hand?",
         "options": ["Wood's corkscrew", "Rubin maneuver", "Gaskin maneuver", "Cleidotomy"],
         "correct": 1, "explain": "The Rubin maneuver rotates the anterior fetal shoulder obliquely with a vaginal hand. Wood's corkscrew rotates the posterior shoulder over 180 degrees."},
        {"q": "The Zavanelli maneuver involves:",
         "options": ["Cutting the fetal clavicle", "Incising the pubic symphysis", "Flexing the fetal head and pushing it back into the uterus for emergent cesarean section", "Turning the patient onto all fours"],
         "correct": 2, "explain": "The Zavanelli maneuver (step 11) involves flexing the fetal head and pushing it back up into the uterus, followed by emergent cesarean section."},
        {"q": "Which maneuver requires the patient to be turned onto all fours?",
         "options": ["Rubin maneuver", "Wood's corkscrew", "Gaskin maneuver", "Symphysiotomy"],
         "correct": 2, "explain": "The Gaskin maneuver (step 8) involves turning the patient onto 'all fours' (if no regional anesthesia), which inverts the anterior and posterior shoulders."},
        {"q": "What is the correct order of the six advanced maneuvers (steps 6-11)?",
         "options": ["Gaskin → Rubin → Wood → Cleidotomy → Symphysiotomy → Zavanelli", "Rubin → Wood → Gaskin → Cleidotomy → Symphysiotomy → Zavanelli", "Wood → Rubin → Gaskin → Symphysiotomy → Cleidotomy → Zavanelli", "Rubin → Gaskin → Wood → Cleidotomy → Zavanelli → Symphysiotomy"],
         "correct": 1, "explain": "The correct order is: Rubin → Wood corkscrew → Gaskin → Cleidotomy → Symphysiotomy → Zavanelli (mnemonic: R-W-G-C-S-Z)."},
    ],
    "s8": [  # Complications
        {"q": "Which fetal complication of shoulder dystocia specifically involves injury to the C5-C6 nerve roots causing 'waiter's tip' deformity?",
         "options": ["Brachial plexus injury (complete)", "Erb's palsy", "Klumpke's palsy", "Hypoxic brain injury"],
         "correct": 1, "explain": "Erb's palsy is a specific brachial plexus injury involving C5-C6 roots, causing 'waiter's tip' deformity (arm adducted, internally rotated, forearm pronated)."},
        {"q": "What is the most severe fetal complication of shoulder dystocia?",
         "options": ["Brachial plexus injury", "Bone fracture", "Hypoxic ischemic brain injury and fetal death", "Erb's palsy"],
         "correct": 2, "explain": "Hypoxic ischemic brain injury from prolonged cord compression and the worst outcome, fetal death, are the most severe fetal complications."},
        {"q": "Which maternal complication of shoulder dystocia is most common?",
         "options": ["Uterine rupture", "Post-partum hemorrhage from uterine atony or perineal trauma", "Maternal death", "Pulmonary embolism"],
         "correct": 1, "explain": "Post-partum hemorrhage, from uterine atony or perineal trauma, is a common maternal complication of shoulder dystocia."},
    ],
}

# ===== 3. 40_Intrauterine_Growth_Restriction =====
MCQ_40 = {
    "s2": [  # Definition
        {"q": "What is the definition of IUGR?",
         "options": ["Fetal weight less than 2,500 g at birth", "Fetal abdominal circumference or estimated fetal weight less than the 10th centile", "Fetal length less than 45 cm", "Head circumference less than the 5th centile"],
         "correct": 1, "explain": "IUGR is defined as fetal abdominal circumference (AC) or estimated fetal weight (EFW) less than the 10th centile for gestational age."},
        {"q": "What is the difference between IUGR and SGA (small for gestational age)?",
         "options": ["They are the same condition", "SGA fetuses are constitutionally small without increased risk of complications, while IUGR fetuses are pathologically small with increased morbidity", "IUGR only applies to preterm fetuses", "SGA has worse outcomes than IUGR"],
         "correct": 1, "explain": "SGA fetuses are constitutionally small without being at increased risk of complications, while IUGR refers to pathologically restricted growth associated with a 2- to 6-fold increase in perinatal morbidity and mortality."},
        {"q": "IUGR is associated with what magnitude of increased perinatal morbidity and mortality?",
         "options": ["No significant increase", "2- to 6-fold increase", "10- to 20-fold increase", "50% increase"],
         "correct": 1, "explain": "IUGR is associated with a 2- to 6-fold increase in perinatal morbidity and mortality compared to normally grown fetuses."},
    ],
    "s3": [  # Types
        {"q": "Which type of IUGR is characterized by disproportionate growth restriction with greater decrease in body and limbs compared to head circumference?",
         "options": ["Symmetric IUGR (Type I)", "Asymmetric IUGR (Type II)", "Constitutional SGA", "Microcephalic IUGR"],
         "correct": 1, "explain": "Asymmetric IUGR (Type II) is caused by extrinsic factors like placental insufficiency. Oxygen and nutrients are directed to vital organs (brain and heart) by passing other organs, resulting in disproportionate growth."},
        {"q": "Symmetric IUGR (Type I) is typically caused by:",
         "options": ["Placental insufficiency", "Intrinsic factors such as genetic abnormalities and intrauterine infections", "Maternal malnutrition", "Multiple pregnancy"],
         "correct": 1, "explain": "Symmetric IUGR is caused by intrinsic factors such as genetic abnormalities (aneuploidy) and early intrauterine infections (TORCH), affecting all parts of the fetus proportionally."},
        {"q": "In asymmetric IUGR, which organs are spared (preferentially perfused)?",
         "options": ["Liver, muscle, and fat tissue", "Brain and heart", "Lungs and kidneys", "Gastrointestinal tract"],
         "correct": 1, "explain": "In asymmetric IUGR (brain-sparing effect), oxygen and nutrients are directed towards vital organs (brain and heart) by passing other organs (liver, muscle, and fat tissue)."},
    ],
    "s5": [  # Maternal RF
        {"q": "Which maternal medical condition is NOT listed as a risk factor for IUGR?",
         "options": ["Pre-existing diabetes mellitus", "Chronic hypertension", "Hyperthyroidism", "Systemic lupus erythematosus"],
         "correct": 2, "explain": "Maternal medical risk factors include pre-existing DM, chronic hypertension, pre-eclampsia, SLE, APS, sickle cell disease, and severe anemia. Hyperthyroidism is not specifically listed."},
        {"q": "Which of the following is a teratogenic drug associated with IUGR?",
         "options": ["Folic acid", "ACE-inhibitors", "Iron supplements", "Prenatal vitamins"],
         "correct": 1, "explain": "ACE-inhibitors, warfarin, carbamazepine, phenytoin, cyclophosphamide, and valproic acid are teratogenic drugs associated with IUGR."},
        {"q": "Substance use is a risk factor for IUGR. Which of the following substances is NOT mentioned?",
         "options": ["Tobacco", "Alcohol", "Cocaine", "Caffeine"],
         "correct": 3, "explain": "Tobacco, alcohol, cocaine, and narcotics are listed as substance use risk factors. Caffeine is not mentioned in the source."},
    ],
    "s6": [  # Placental/fetal RF
        {"q": "Which of the following is a placental risk factor for IUGR?",
         "options": ["Fetal aneuploidy", "Placental insufficiency", "Cyanotic congenital heart disease", "TORCH infections"],
         "correct": 1, "explain": "Placental risk factors for IUGR include placental insufficiency, placenta previa or abruption, and multiple gestation."},
        {"q": "TORCH infections are a cause of which type of IUGR?",
         "options": ["Asymmetric IUGR", "Symmetric IUGR", "Both types equally", "Neither type"],
         "correct": 1, "explain": "TORCH infections (Toxoplasmosis, Other, Rubella, CMV, Herpes) cause symmetric IUGR because they affect the fetus intrinsically and early in development."},
        {"q": "Which congenital anomaly is listed as a fetal risk factor for IUGR?",
         "options": ["Ventricular septal defect", "Cyanotic congenital heart disease", "Atrial septal defect", "Patent ductus arteriosus"],
         "correct": 1, "explain": "Cyanotic congenital heart disease is listed as a fetal risk factor for IUGR among congenital anomalies."},
    ],
    "s7": [  # Diagnosis
        {"q": "What is the classic clinical sign of IUGR on abdominal examination?",
         "options": ["Fundal height more than gestational age in weeks", "Symphysial-fundal height at least 3 cm less than gestational age in weeks", "Uterus tense and tender", "Fetal parts difficult to palpate"],
         "correct": 1, "explain": "The classic clinical sign is SFH decreased compared to gestational age — at least 3 cm less than gestational age in weeks. However, serial measurements and ultrasound are more reliable."},
        {"q": "Which symptom in the context of a small-for-dates fetus should raise immediate suspicion of IUGR with fetal compromise?",
         "options": ["Maternal weight gain", "Reduced or absent fetal movements", "Heartburn", "Lower back pain"],
         "correct": 1, "explain": "Reduced or absent fetal movements in the context of a small-for-dates fetus should raise immediate suspicion of IUGR with fetal compromise — this is an obstetric emergency."},
        {"q": "What poor sensitivity does SFH measurement have for diagnosing IUGR?",
         "options": ["Excellent sensitivity, high specificity", "Poor sensitivity — serial measurements and ultrasound are more reliable", "SFH is diagnostic of IUGR", "SFH is only useful in multiple pregnancies"],
         "correct": 1, "explain": "SFH measurement has poor sensitivity — serial measurements and ultrasound are more reliable for diagnosing IUGR."},
    ],
    "s8": [  # Investigations
        {"q": "Which Doppler study is used in the investigation of IUGR?",
         "options": ["Middle cerebral artery Doppler", "Umbilical artery Doppler", "Uterine artery Doppler", "Ductus venosus Doppler"],
         "correct": 1, "explain": "Umbilical artery Doppler is used in IUGR assessment, showing abnormalities such as reduced or reversed diastolic flow."},
        {"q": "What Biophysical Profile (BPP) score indicates the need for delivery in IUGR?",
         "options": ["BPP ≤ 6", "BPP ≤ 4", "BPP = 8", "BPP = 10"],
         "correct": 1, "explain": "A BPP score of ≤ 4 indicates the need for delivery in cases of IUGR."},
        {"q": "Which three investigations form the IUGR assessment triad?",
         "options": ["NST, CST, CTG", "Umbilical Doppler, Amniotic fluid assessment, BPP", "Fetal biometry, kick count, glucose tolerance test", "Amniocentesis, cordocentesis, placental biopsy"],
         "correct": 1, "explain": "The IUGR assessment triad is: Umbilical Doppler (reduced/reversed diastolic flow) → Amniotic fluid (oligohydramnios) → BPP (≤ 4 = deliver)."},
        {"q": "Which finding on serial ultrasound scans is consistent with IUGR?",
         "options": ["Polyhydramnios", "Oligohydramnios", "Macrosomia", "Placental calcification"],
         "correct": 1, "explain": "Ultrasound findings in IUGR include decreased fetal growth and weight, small placenta, and oligohydramnios."},
    ],
    "s9": [  # Complications
        {"q": "Which hypothesis explains the link between IUGR and adult-onset diseases?",
         "options": ["Barker hypothesis (thrifty phenotype)", "Starling hypothesis", "Frank-Starling mechanism", "Bohr effect"],
         "correct": 0, "explain": "The Barker hypothesis (thrifty phenotype) states that fetal undernutrition leads to permanent metabolic adaptations that increase risk of adult-onset diseases including diabetes, obesity, coronary artery disease, and hypertension."},
        {"q": "Which of the following is NOT a listed complication of IUGR?",
         "options": ["Preterm labor and delivery", "Necrotising enterocolitis", "Gestational diabetes", "Stillbirth"],
         "correct": 2, "explain": "IUGR complications include preterm labor, stillbirth, perinatal asphyxia, NEC, cognitive delay, adult-onset diseases, motor/neurological disabilities, and death. GDM is a risk factor for IUGR, not a complication of it."},
        {"q": "IUGR programmes the fetus for which adult-onset diseases?",
         "options": ["Asthma and allergies", "Diabetes mellitus, obesity, coronary artery disease, and hypertension", "Autoimmune disorders", "Thyroid disease and osteoporosis"],
         "correct": 1, "explain": "Adults who were IUGR fetuses have increased risks of diabetes mellitus, obesity, coronary artery disease, and hypertension (Barker hypothesis)."},
    ],
    "s10": [  # Management
        {"q": "What is the recommended mode of delivery for IUGR?",
         "options": ["Vaginal delivery in all cases", "Cesarean section is the rule", "Vacuum-assisted delivery", "Trial of labor with close monitoring"],
         "correct": 1, "explain": "Cesarean section is the rule for IUGR because the fetus does not tolerate the reduced oxygen supply and birth trauma encountered during vaginal delivery."},
        {"q": "Which of the following is NOT part of antenatal management of IUGR?",
         "options": ["Treatment of the underlying cause", "Monitoring of fetal wellbeing", "Elective cesarean at 32 weeks", "Good diet"],
         "correct": 2, "explain": "Antenatal management includes: (1) Treatment of the underlying cause and no smoking, (2) Monitoring of fetal wellbeing, (3) Good diet. Timing of delivery depends on fetal status."},
        {"q": "Postnatal management of IUGR focuses on identifying and managing problems of:",
         "options": ["Dysmaturity", "Hyperglycemia", "Polyhydramnios", "Macrosomia"],
         "correct": 0, "explain": "Postnatal management focuses on dysmaturity complications: hypoglycemia, hypothermia, polycythemia, feeding difficulties, and long-term neurodevelopmental follow-up."},
    ],
}

# ===== 4. 42_Macrosomia =====
MCQ_42 = {
    "s2": [  # Definition
        {"q": "What is the definition of fetal macrosomia?",
         "options": ["Fetal weight > 3,500 g", "Fetal weight > 4,000 g", "Fetal weight > 4,500 g", "Fetal weight > 5,000 g"],
         "correct": 1, "explain": "Macrosomia is defined as a fetal weight > 4,000 grams, regardless of gestational age."},
    ],
    "s3": [  # Risk factors
        {"q": "Which of the following is a risk factor for fetal macrosomia?",
         "options": ["History of preterm delivery", "Maternal obesity", "Maternal age under 20", "Female infant"],
         "correct": 1, "explain": "Risk factors for macrosomia include history of fetal macrosomia, maternal obesity, excessive weight gain during pregnancy, increasing parity, male infants, and maternal age > 35."},
        {"q": "How does maternal age affect the risk of macrosomia?",
         "options": ["Women under 25 have highest risk", "Women older than 35 are more likely to have a baby with macrosomia", "Maternal age does not affect risk", "Teenage mothers have highest risk"],
         "correct": 1, "explain": "Women older than 35 years are more likely to have a baby diagnosed with fetal macrosomia."},
    ],
    "s4": [  # Causes
        {"q": "Which maternal condition is a cause of fetal macrosomia?",
         "options": ["Chronic hypertension", "Diabetes mellitus", "Thyroid disease", "Asthma"],
         "correct": 1, "explain": "Maternal diabetes mellitus is a recognized cause of fetal macrosomia because fetal hyperinsulinemia in response to maternal hyperglycemia promotes excessive fetal growth."},
        {"q": "Which of the following is NOT a cause of fetal macrosomia?",
         "options": ["Genetic factors", "Multiparity", "Postterm pregnancy", "Placental insufficiency"],
         "correct": 3, "explain": "Causes of macrosomia include genetic factors, maternal diabetes, multiparity, and postterm pregnancy. Placental insufficiency causes IUGR, not macrosomia."},
    ],
    "s5": [  # Clinical picture
        {"q": "Which clinical finding is associated with fetal macrosomia?",
         "options": ["Small fundal height", "Large fundal height", "Oligohydramnios", "Decreased fetal movements"],
         "correct": 1, "explain": "The clinical picture of macrosomia includes large fundal height and excessive amniotic fluid (polyhydramnios)."},
    ],
    "s6": [  # Complications
        {"q": "Which complication of macrosomia involves the fetal shoulder becoming impacted during delivery?",
         "options": ["Cord prolapse", "Shoulder dystocia", "Uterine atony", "Placental abruption"],
         "correct": 1, "explain": "Shoulder dystocia is a direct complication of macrosomia — the large fetal shoulders cannot pass through the pelvic inlet after delivery of the head."},
        {"q": "Which of the following is NOT a listed complication of fetal macrosomia?",
         "options": ["Prolonged and obstructed labor", "Meconium aspiration syndrome", "Preterm labor", "Uterine rupture"],
         "correct": 2, "explain": "Complications of macrosomia include prolonged/obstructed labor, shoulder dystocia, fetal injuries, meconium aspiration syndrome, genital tract lacerations, PPH, and uterine rupture. Preterm labor is not a typical complication."},
        {"q": "Postpartum hemorrhage in macrosomia may result from:",
         "options": ["Uterine atony from overdistended uterus", "Placental abruption", "Preeclampsia", "Amniotic fluid embolism"],
         "correct": 0, "explain": "Postpartum hemorrhage in macrosomia results from uterine atony (the overdistended uterus contracts poorly) and genital tract lacerations from delivering a large baby."},
    ],
    "s7": [  # Treatment
        {"q": "What is the recommended mode of delivery for fetal macrosomia?",
         "options": ["Vaginal delivery in all cases", "Cesarean section is safe for both mother and fetus", "Vacuum extraction", "Induction of labor at term"],
         "correct": 1, "explain": "Cesarean section is considered safe for both mother and fetus in cases of fetal macrosomia."},
        {"q": "What does antenatal care for macrosomia aim to achieve?",
         "options": ["Induce labor at 37 weeks", "Prevent macrosomia and diagnose it before labor", "Ensure vaginal delivery", "Reduce maternal weight gain"],
         "correct": 1, "explain": "Proper antenatal care aims to prevent macrosomia and diagnose it before labor so appropriate delivery planning can be made."},
    ],
}

# ===== 5. 31_Preterm_Labor =====
MCQ_31 = {
    "s2": [  # Definition
        {"q": "What is the definition of preterm labor (PTL)?",
         "options": ["Labor before 37 completed weeks (259 days) from the first day of the LMP", "Labor before 40 weeks", "Labor before 32 weeks", "Labor between 37 and 42 weeks"],
         "correct": 0, "explain": "Preterm labor is defined as the onset of labor before 37 completed weeks (259 days) from the first day of the last menstrual period."},
        {"q": "What range defines late preterm (near term)?",
         "options": ["32-36 weeks", "34-36+6 weeks", "28-32 weeks", "36-37 weeks"],
         "correct": 1, "explain": "Late preterm (near term) is defined as 34 to 36+6 weeks. The full classification also includes moderate preterm (32-33+6 weeks), very preterm (28-31+6 weeks), and extremely preterm (< 28 weeks)."},
    ],
    "s3": [  # Maternal RF
        {"q": "Which maternal infection is a risk factor for preterm labor?",
         "options": ["Upper respiratory infection", "Urinary tract infection (including asymptomatic bacteriuria)", "Skin infection", "Sinusitis"],
         "correct": 1, "explain": "Urinary tract infection, including asymptomatic bacteriuria, and other genital tract infections are maternal risk factors for preterm labor."},
        {"q": "Which of the following is NOT a maternal risk factor for preterm labor?",
         "options": ["Smoking", "Low pre-pregnancy BMI", "Advanced maternal age", "Multiple pregnancy"],
         "correct": 3, "explain": "Multiple pregnancy is a risk factor but it is classified under obstetric factors, not maternal. Maternal factors include smoking, UTI, low BMI, maternal age extremes, previous preterm birth, and cervical incompetence."},
    ],
    "s4": [  # Fetal causes
        {"q": "Which fetal condition can cause preterm labor?",
         "options": ["Fetal macrosomia", "Fetal anomalies (e.g., neural tube defects)", "Post-term pregnancy", "Fetal anemia"],
         "correct": 1, "explain": "Fetal causes of preterm labor include fetal anomalies (e.g., neural tube defects, cardiac anomalies) and IUGR."},
    ],
    "s5": [  # Diagnosis
        {"q": "What contraction frequency defines active preterm labor?",
         "options": ["2 contractions in 20 minutes", "4 contractions in 20 minutes or 8 in 60 minutes", "6 contractions in 60 minutes", "Continuous contractions"],
         "correct": 1, "explain": "The '4 in 20 / 8 in 60' rule defines active preterm labor — this is the threshold to start tocolysis and corticosteroids."},
        {"q": "Which symptom is NOT a typical feature of preterm labor?",
         "options": ["Uterine contractions", "Lower back pain", "Passage of blood-stained vaginal discharge (show)", "Severe vaginal bleeding"],
         "correct": 3, "explain": "Symptoms of preterm labor include uterine contractions (4 in 20 min or 8 in 60 min), lower back pain, blood-stained show, pelvic pressure, and bulging membranes/ROM. Severe vaginal bleeding suggests placental abruption, not PTL."},
    ],
    "s6": [  # Investigations
        {"q": "What is the progressive shape change of the cervix on TVUS as labor approaches?",
         "options": ["U → V → Y → T", "T → Y → V → U", "Y → T → U → V", "V → U → T → Y"],
         "correct": 1, "explain": "The cervical shape progresses from T shape (normal) → Y shape → V shape → U shape (imminent delivery) as the cervix shortens and opens."},
        {"q": "What test detects fibronectin glycoprotein in cervico-vaginal discharge between 24 and 34 weeks to predict PTL?",
         "options": ["Nitrazine test", "Fetal fibronectin test", "Fern test", "Amniocentesis"],
         "correct": 1, "explain": "The fetal fibronectin test detects fibronectin glycoprotein in cervico-vaginal discharge between 24 and 34 weeks and is a predictor of PTL."},
        {"q": "What cervical dilatation on TVUS suggests preterm labor?",
         "options": ["> 1 cm", "> 2 cm", "> 3 cm", "> 4 cm"],
         "correct": 1, "explain": "Dilatation of cervix > 2 cm on transvaginal ultrasound is suggestive of preterm labor."},
    ],
    "s7": [  # Prophylactic Mgmt
        {"q": "Which prophylactic measure for preterm labor involves a surgical suture placed around the cervix?",
         "options": ["Progesterone supplementation", "Cerclage surgery", "Cervical pessary", "Bed rest"],
         "correct": 1, "explain": "Cerclage (McDonald or Shirodkar suture) is placed prophylactically in women with cervical incompetence, typically at 12-14 weeks, and removed at 36-37 weeks."},
        {"q": "Which three prophylactic measures are recommended to prevent preterm labor?",
         "options": ["Bed rest, hydration, and antibiotics", "Stop smoking, cerclage, and progesterone", "Corticosteroids, tocolytics, and antibiotics", "Exercise, diet, and vitamins"],
         "correct": 1, "explain": "The three prophylactic measures are: (1) Stop smoking, (2) Cerclage surgery if cervical incompetence, (3) Progesterone."},
    ],
    "s8": [  # Curative Mgmt
        {"q": "Which three drug therapies are combined in the management of established preterm labor?",
         "options": ["Antihypertensives, antibiotics, and insulin", "Corticosteroids, tocolytics, and antibiotics", "Oxytocin, ergometrine, and misoprostol", "Magnesium sulfate, nifedipine, and betamethasone"],
         "correct": 1, "explain": "In established preterm labor, three drug therapy pillars are combined: corticosteroids (for fetal lung maturity), tocolytics (to delay delivery 48 hours), and antibiotics (for GBS prophylaxis)."},
    ],
    "s9": [  # Corticosteroids
        {"q": "What is the purpose of administering antenatal corticosteroids in preterm labor?",
         "options": ["To stop uterine contractions", "To decrease the risk of respiratory distress syndrome in the newborn", "To prevent maternal infection", "To induce fetal lung fluid production"],
         "correct": 1, "explain": "Antenatal corticosteroids decrease the chance of respiratory distress syndrome (RDS) and other prematurity complications (IVH, NEC, neonatal mortality)."},
        {"q": "What is the dosage regimen for betamethasone?",
         "options": ["4 doses of 6 mg IM, 12 hours apart", "2 doses of 12 mg IM, 24 hours apart", "Single dose of 24 mg IM", "2 doses of 6 mg IM, 6 hours apart"],
         "correct": 1, "explain": "Betamethasone is given as 2 doses of 12 mg intramuscularly, 24 hours apart. Dexamethasone is 4 doses of 6 mg IM, 12 hours apart."},
        {"q": "Why are tocolytics given together with corticosteroids in preterm labor?",
         "options": ["To enhance the effect of corticosteroids", "To buy the ~48 hours that corticosteroids need to complete their effect on fetal lung surfactant production", "To prevent side effects of corticosteroids", "To induce uterine contractions"],
         "correct": 1, "explain": "Corticosteroids need ~48 hours to complete their effect on fetal lung surfactant production. Tocolytic drugs are given to delay delivery for those 48 hours."},
    ],
    "s10": [  # Tocolysis
        {"q": "Which of the following is an absolute contraindication to tocolysis?",
         "options": ["Gestational diabetes", "Chorioamnionitis", "Mild anemia", "Previous cesarean section"],
         "correct": 1, "explain": "Chorioamnionitis is an absolute contraindication to tocolysis — delaying delivery in the presence of intrauterine infection would worsen the infection."},
        {"q": "Which class of tocolytic drug is Indomethacin?",
         "options": ["Calcium channel blocker", "Prostaglandin synthetase inhibitor", "Oxytocin antagonist", "Beta agonist"],
         "correct": 1, "explain": "Indomethacin is a prostaglandin synthetase inhibitor. It is not used after 30 weeks' gestation due to risk of premature closure of the ductus arteriosus."},
        {"q": "Nifedipine is which class of tocolytic and what is its oral loading dose?",
         "options": ["Beta agonist; 10 mg", "Calcium channel blocker; 20 mg orally followed by another 20 mg after 30 minutes", "Oxytocin antagonist; 6.75 mg IV", "Magnesium sulfate; 4-6 g IV"],
         "correct": 1, "explain": "Nifedipine is a calcium channel blocker. Initial dose: 20 mg orally, followed by another 20 mg after 30 minutes. Maintenance: 20 mg every 4-8 hours (max 160 mg/day)."},
        {"q": "Which tocolytic drug is known for its dangerous complication of heart failure?",
         "options": ["Atosiban", "Ritodrine (beta agonist)", "Indomethacin", "Magnesium sulfate"],
         "correct": 1, "explain": "Ritodrine (beta agonist) is associated with dangerous complications including heart failure, tachycardia, pulmonary edema, and hyperglycemia. It is now largely abandoned."},
    ],
    "s12": [  # Antibiotic + Mode
        {"q": "What antibiotic is given for GBS prophylaxis in established preterm labor?",
         "options": ["Gentamicin", "Benzyl penicillin or ampicillin", "Ceftriaxone", "Metronidazole"],
         "correct": 1, "explain": "Benzyl penicillin or ampicillin should be given for established PTL as prophylaxis against early-onset neonatal sepsis due to Group B Streptococcus. Clindamycin is used in penicillin allergy."},
        {"q": "What is the recommended mode of delivery for a preterm breech presentation at < 34 weeks?",
         "options": ["Vaginal delivery", "Cesarean section", "External cephalic version", "Vacuum extraction"],
         "correct": 1, "explain": "For breech presentation at < 34 weeks, cesarean section is done because the preterm fetal head and body are disproportionately small and fragile, making vaginal breech delivery risky."},
        {"q": "For preterm labor with cephalic presentation at < 34 weeks, what is the preferred mode of delivery?",
         "options": ["Cesarean section", "Vaginal delivery", "Instrumental delivery", "External version"],
         "correct": 1, "explain": "With cephalic presentation, the preferred mode is vaginal delivery even if delivery is at < 34 weeks."},
    ],
}

# ===== 6. 32_Premature_Rupture_of_Membranes =====
MCQ_32 = {
    "s2": [  # Definition
        {"q": "What is the definition of PROM?",
         "options": ["Rupture of membranes before the onset of labor", "Rupture of membranes after 42 weeks", "Rupture of membranes during active labor", "Rupture of membranes at term"],
         "correct": 0, "explain": "PROM is defined as rupture of the fetal membranes before the onset of labor. Preterm PROM (PPROM) refers to PROM occurring before 37 weeks."},
        {"q": "PPROM is defined as PROM occurring before how many weeks of gestation?",
         "options": ["Before 34 weeks", "Before 37 weeks", "Before 40 weeks", "Before 28 weeks"],
         "correct": 1, "explain": "PPROM (Preterm Premature Rupture of Membranes) is PROM occurring before 37 completed weeks of gestation."},
    ],
    "s3": [  # Etiology
        {"q": "Which of the following is the most important cause of PROM?",
         "options": ["Trauma", "Polyhydramnios", "Intrauterine infection", "Amniocentesis"],
         "correct": 2, "explain": "Intrauterine infection is the most important cause clinically because it is both a cause AND a complication of PROM (chorioamnionitis)."},
        {"q": "What are the 5 classic etiologies of PROM?",
         "options": ["Infection, prior PPROM, trauma, amniocentesis, polyhydramnios", "Infection, diabetes, hypertension, smoking, multiple pregnancy", "Trauma, smoking, alcohol, diabetes, obesity", "Prior PPROM, infection, postterm, IUGR, abruption"],
         "correct": 0, "explain": "The 5 classic etiologies of PROM are: INFECTION, PRIOR PPROM, TRAUMA, AMNIOCENTESIS, and POLYHYDRAMNIOS."},
    ],
    "s4": [  # Presentation
        {"q": "What is the typical presentation of PROM?",
         "options": ["Gradual onset of watery vaginal discharge over days", "Sudden gush of clear or pale yellow fluid leaking from the vagina", "Blood-stained vaginal discharge with abdominal pain", "Foul-smelling vaginal discharge with fever"],
         "correct": 1, "explain": "Patients typically present with a sudden gush of clear or pale yellow fluid leaking from the vagina. Meconium-stained (green/brown) fluid suggests fetal distress, while foul-smelling fluid suggests chorioamnionitis."},
    ],
    "s5": [  # Diagnosis
        {"q": "What is the first step in the diagnosis of PROM?",
         "options": ["Ultrasound examination", "Speculum examination", "Nitrazine test", "Fern test"],
         "correct": 1, "explain": "Speculum examination is the first step in the diagnosis of PROM — it is used to directly demonstrate leaking of fluid from the cervical os."},
        {"q": "The nitrazine test is based on the principle that amniotic fluid pH is:",
         "options": ["Acidic (3.5-4.5)", "Alkaline (7-7.5)", "Neutral (7.0)", "Highly acidic (2-3)"],
         "correct": 1, "explain": "Amniotic fluid pH is 7-7.5 (alkaline), while vaginal discharge pH is 3.5-4.5 (acidic). Yellow nitrazine paper turning blue indicates alkaline amniotic fluid, confirming PROM."},
        {"q": "What pattern does amniotic fluid form on a glass slide when dried (fern test)?",
         "options": ["Crystalline honeycomb pattern", "Fern pattern (arborization)", "Spiderweb pattern", "Linear streaks"],
         "correct": 1, "explain": "The fern test shows a fern pattern (arborization) on microscopy when amniotic fluid is swabbed from the posterior vaginal fornix, placed on a glass slide, and allowed to dry for 10 minutes."},
        {"q": "What is the sensitivity of fetal fibronectin for detecting PROM?",
         "options": ["Over 95%", "Only 39%", "About 75%", "Less than 10%"],
         "correct": 1, "explain": "Fetal fibronectin is detected in only 39% of females with PROM — its sensitivity is limited, making it more useful as a rule-out test than a rule-in test."},
    ],
    "s6": [  # Effects
        {"q": "What is the most immediate and common consequence of preterm PROM?",
         "options": ["Pulmonary hypoplasia", "Preterm labor", "Skeletal deformities", "Chorioamnionitis"],
         "correct": 1, "explain": "Preterm labor is the most immediate and common consequence of PPROM — once the membranes rupture, uterine contractions typically begin within hours to days."},
        {"q": "Which consequence of PPROM is irreversible and leads to high neonatal mortality when severe oligohydramnios is prolonged?",
         "options": ["Preterm labor", "Pulmonary hypoplasia", "Chorioamnionitis", "Skeletal deformities"],
         "correct": 1, "explain": "Pulmonary hypoplasia from prolonged severe oligohydramnios is not reversible after birth, which is why very early PPROM (< 24 weeks) carries very high neonatal mortality."},
    ],
    "s7": [  # General Mgmt
        {"q": "What are the two general management measures for PROM?",
         "options": ["Antibiotics and corticosteroids", "Bed rest and sterile pads for inspection", "Tocolysis and amniocentesis", "Induction of labor and cesarean section"],
         "correct": 1, "explain": "General management of PROM includes bed rest (to reduce mechanical stimulus on the cervix) and sterile pads for inspection of meconium staining and signs of infection."},
    ],
    "s8": [  # <26w
        {"q": "What is the recommended management for PROM before 26 weeks?",
         "options": ["Conservative management with antibiotics", "Termination of pregnancy is better", "Amnio-infusion and corticosteroids", "Immediate cesarean section"],
         "correct": 1, "explain": "Before 26 weeks, termination of pregnancy is recommended because the risk of chorioamnionitis is very high, pulmonary hypoplasia is likely, and fetal viability is below 24-26 weeks."},
    ],
    "s9": [  # 26-34w
        {"q": "What is the antibiotic regimen for conservative management of PPROM at 26-34 weeks?",
         "options": ["IV ampicillin 2 g + IV gentamicin until delivery", "IV ampicillin 2 g + erythromycin 250 mg/6h for 48 hours, then oral amoxicillin 250 mg/8h + erythromycin 250 mg/6h for 5 days", "Oral amoxicillin-clavulanate for 7 days", "IV ceftriaxone 1 g daily for 7 days"],
         "correct": 1, "explain": "The regimen is: IV ampicillin 2 g + erythromycin 250 mg/6h for 48 hours, then oral step-down with amoxicillin 250 mg/8h + erythromycin 250 mg/6h for 5 additional days (total 7 days)."},
        {"q": "For PPROM between 26-34 weeks, what is the goal of tocolysis?",
         "options": ["To stop labor permanently", "To delay delivery for the 48-hour window that corticosteroids need to work", "To prevent infection", "To reduce maternal pain"],
         "correct": 1, "explain": "Tocolysis is given to delay delivery for the ~48-hour window that corticosteroids need to complete their effect on fetal lung surfactant production."},
    ],
    "s10": [  # >34w
        {"q": "What is the recommended management for PROM after 34 weeks?",
         "options": ["Conservative management with antibiotics", "Delivery is indicated", "Amnio-infusion", "Corticosteroids and tocolysis"],
         "correct": 1, "explain": "After 34 weeks, the fetus is sufficiently mature that delivery is indicated because the risk of conservative management (chorioamnionitis, cord prolapse) outweighs the risk of prematurity."},
    ],
    "s11": [  # Chorioamnionitis
        {"q": "What is the diagnostic rule for chorioamnionitis?",
         "options": ["Fever > 39°C alone", "Fever > 38°C PLUS any of 7 signs (maternal tachycardia, fetal tachycardia, uterine tenderness, foul-smelling fluid, leukocytosis > 16,000/cc, raised CRP > 2.5, positive HVS culture)", "Positive amniotic fluid culture alone", "Uterine tenderness alone"],
         "correct": 1, "explain": "Chorioamnionitis is diagnosed when there is fever > 38°C with at least one of 7 signs: maternal tachycardia, fetal tachycardia, uterine tenderness, foul-smelling AF, leukocytosis > 16,000/cc, raised CRP > 2.5, or positive HVS."},
        {"q": "What is the single most important risk factor for chorioamnionitis?",
         "options": ["Prolonged labor", "Prolonged PROM", "Bacterial vaginosis", "Prenatal diagnostic procedures"],
         "correct": 1, "explain": "Prolonged PROM is the single most important risk factor for chorioamnionitis — ascending infection through the ruptured membranes."},
    ],
    "s12": [  # Chorioamnionitis Mgmt
        {"q": "What is the definitive treatment for chorioamnionitis?",
         "options": ["IV antibiotics alone", "Delivery and evacuation of uterine contents", "Amnio-reduction", "Antipyretics and antibiotics"],
         "correct": 1, "explain": "Definitive treatment is delivery and evacuation of the uterine contents. Antibiotics alone are not curative while the infected focus (amniotic cavity) remains in place."},
        {"q": "What is the antibiotic regimen for chorioamnionitis?",
         "options": ["Ampicillin 2 g IV q6h + Gentamicin 2 mg/kg IV load then 1.5 mg/kg IV q8h until delivery", "Ceftriaxone + metronidazole", "Amoxicillin-clavulanate alone", "Vancomycin + gentamicin"],
         "correct": 0, "explain": "The regimen is: Ampicillin 2 g IV q6h + Gentamicin 2 mg/kg IV load then 1.5 mg/kg IV q8h until delivery. If cesarean delivery is performed, clindamycin or metronidazole is added for anaerobic coverage."},
    ],
}

# ===== 7. 41_Postterm_Pregnancy =====
MCQ_41 = {
    "s2": [  # Definition
        {"q": "What is the definition of postterm pregnancy?",
         "options": ["Pregnancy continuing beyond 40 weeks", "Pregnancy continuing beyond 42 weeks", "Pregnancy continuing beyond 41 weeks", "Pregnancy continuing beyond 43 weeks"],
         "correct": 1, "explain": "Postterm pregnancy is a pregnancy continuing beyond 42 weeks. Pregnancy between 41-42 weeks is called prolonged pregnancy."},
        {"q": "What is the difference between prolonged pregnancy and postterm pregnancy?",
         "options": ["They are the same condition", "Prolonged = 41-42 weeks (monitored); Postterm = > 42 weeks (requires intervention)", "Prolonged = > 40 weeks; Postterm = > 42 weeks", "Prolonged = > 43 weeks; Postterm = > 42 weeks"],
         "correct": 1, "explain": "Prolonged pregnancy is 41-42 weeks (managed with monitoring), while postterm pregnancy is > 42 weeks (requires intervention). The distinction matters for management."},
    ],
    "s3": [  # Causes
        {"q": "What is the most common cause of postterm pregnancy?",
         "options": ["Maternal obesity", "Wrong date (incorrect dating)", "Primiparity", "Anencephaly"],
         "correct": 1, "explain": "The most common cause of postterm pregnancy is wrong date, so careful review of menstrual history is important in all such cases."},
        {"q": "Which fetal condition is associated with postterm pregnancy due to disruption of the hypothalamic-pituitary-adrenal axis?",
         "options": ["Hydrocephalus", "Anencephaly", "Spina bifida", "Congenital heart disease"],
         "correct": 1, "explain": "Anencephaly causes postterm pregnancy because the fetal hypothalamic-pituitary-adrenal axis is disrupted — without fetal cortisol, labor is not initiated."},
        {"q": "Which maternal factor is associated with postterm pregnancy?",
         "options": ["Multiparity", "Primipara", "Active lifestyle", "Young maternal age"],
         "correct": 1, "explain": "Maternal factors include primipara, history of previous prolonged pregnancy, and sedentary life."},
    ],
    "s4": [  # Diagnosis antenatal
        {"q": "Which ultrasound finding is characteristic of postterm pregnancy?",
         "options": ["Polyhydramnios", "Increased placental calcification", "Fetal macrosomia with normal placental grade", "Increased amniotic fluid volume"],
         "correct": 1, "explain": "Increased placental calcification on ultrasound is a hallmark of placental aging in postterm pregnancy, reflecting the pathophysiology of placental insufficiency."},
        {"q": "What BPD measurement on ultrasound suggests postterm pregnancy?",
         "options": ["BPD > 8.5 cm", "BPD > 9.6 cm", "BPD > 10 cm", "BPD > 7.5 cm"],
         "correct": 1, "explain": "Biparietal diameter more than 9.6 cm is an ultrasound finding suggestive of postterm pregnancy."},
    ],
    "s5": [  # Postnatal
        {"q": "Which postnatal sign is NOT characteristic of postterm baby?",
         "options": ["Baby length more than 54 cm", "Baby weight more than 4.5 kg", "Soft, open fontanelles", "Finger nails projecting beyond finger tips"],
         "correct": 2, "explain": "Postterm babies have well-ossified skulls with smaller fontanelles (not soft/open), length > 54 cm, weight > 4.5 kg, and fingernails projecting beyond fingertips."},
        {"q": "What is the mnemonics for postterm postnatal signs?",
         "options": ["L-W-S-F: Length > 54 cm, Weight > 4.5 kg, Skull well ossified/small fontanelles, Finger nails beyond tips", "H-W-S-F", "L-W-B-F", "H-B-S-N"],
         "correct": 0, "explain": "The mnemonic is L-W-S-F: Length > 54 cm, Weight > 4.5 kg, Skull well ossified with small fontanelles, Finger nails project beyond tips."},
    ],
    "s6": [  # Complications
        {"q": "What is the cascade of complications in postterm pregnancy?",
         "options": ["Placental aging → polyhydramnios → preterm labor", "Placental aging → hypoxia → acidosis → stillbirth", "Placental aging → macrosomia → shoulder dystocia", "Placental aging → preeclampsia → eclampsia"],
         "correct": 1, "explain": "The cascade is: placental aging → placental insufficiency → fetal hypoxia → acidosis → stillbirth. Each day past 42 weeks increases this risk."},
        {"q": "Which complication of postterm pregnancy results from oligohydramnios?",
         "options": ["Preeclampsia", "Cord compression and meconium aspiration", "Gestational diabetes", "Placental abruption"],
         "correct": 1, "explain": "Oligohydramnios in postterm pregnancy leads to cord compression and meconium aspiration, further contributing to fetal compromise."},
    ],
    "s7": [  # Management
        {"q": "What is the management of postterm pregnancy?",
         "options": ["Conservative management until 44 weeks", "Termination of pregnancy (induction of labor or cesarean section)", "Weekly monitoring only", "Corticosteroids and tocolysis"],
         "correct": 1, "explain": "Management of postterm pregnancy is termination of pregnancy — induction of labor or cesarean section depending on cervical readiness and fetal status."},
    ],
}

# ===== 8. 43_Intrauterine_Fetal_Death =====
MCQ_43 = {
    "s2": [  # Definition
        {"q": "What is the definition of Intrauterine Fetal Death (IUFD)?",
         "options": ["Death of fetus in-utero after 12 weeks of pregnancy", "Death of fetus in-utero after 20 weeks of pregnancy or if fetal weight > 500 g", "Death of fetus during labor", "Death of fetus in-utero at any gestational age"],
         "correct": 1, "explain": "IUFD is death of the fetus in-utero after 20 weeks of pregnancy or if the fetus weight is > 500 g."},
    ],
    "s3": [  # Causes
        {"q": "Which of the following is a maternal cause of IUFD?",
         "options": ["Cord accident", "Antiphospholipid syndrome", "Congenital abnormality", "Hydrops"],
         "correct": 1, "explain": "Maternal causes of IUFD include diabetes, SLE, APS, infection, hypertension, preeclampsia, eclampsia, uterine rupture, maternal trauma/death, and thrombophilias. Cord accident is a placental cause."},
        {"q": "Which placental cause of IUFD involves bleeding from aberrant fetal vessels at the membranes?",
         "options": ["Cord accident", "Abruption", "Vasa previa", "Placental insufficiency"],
         "correct": 2, "explain": "Vasa previa is a placental cause of IUFD. Other placental causes include cord accident, abruption, PROM, feto-maternal hemorrhage, and placental insufficiency."},
    ],
    "s4": [  # Diagnosis
        {"q": "Which symptom is NOT associated with the diagnosis of IUFD?",
         "options": ["Gradual disappearance of pregnancy symptoms", "Breast milk secretion", "Cessation of fetal movements", "Increased fetal activity"],
         "correct": 3, "explain": "Symptoms of IUFD include gradual disappearance of pregnancy symptoms, breast milk secretion, failure of abdominal enlargement, and cessation of fetal movements. Increased fetal activity is not a symptom."},
        {"q": "Which physical sign is characteristic of IUFD?",
         "options": ["Uterus larger than period of amenorrhea", "Uterus smaller than period of amenorrhea", "Easy palpation of well-defined fetal parts", "Increased FHS on Doppler"],
         "correct": 1, "explain": "Signs include uterus smaller than the period of amenorrhea, difficult palpation of fetal parts due to absent muscle tone, and inaudible FHS by Doppler."},
    ],
    "s5": [  # Investigations
        {"q": "Which X-ray sign of IUFD involves overlapping of fetal skull bones?",
         "options": ["Robert sign", "Spalding sign", "Ball sign", "Halo sign"],
         "correct": 1, "explain": "Spalding sign is the overlapping of fetal skull bones due to shrinkage of the cerebrum after fetal death."},
        {"q": "Robert sign of IUFD refers to:",
         "options": ["Hyperflexion of fetal spine", "Overlapping of skull bones", "Presence of gas in fetal large vessels", "Collapse of fetal chest"],
         "correct": 2, "explain": "Robert sign is the presence of gas in fetal large vessels. Ball sign is hyperflexion of the fetal spine. The mnemonic is SRB (Spalding, Robert, Ball)."},
    ],
    "s6": [  # Complications
        {"q": "What is the major complication if IUFD persists for more than 3 weeks?",
         "options": ["Intrauterine infection only", "DIC and hypofibrinogenemia", "Placental abruption", "Maternal hypertension"],
         "correct": 1, "explain": "Once fetal death has persisted for > 3 weeks, the risk of maternal DIC and hypofibrinogenemia rises sharply. This is why delivery is usually offered."},
        {"q": "What two complications are associated with IUFD?",
         "options": ["Preeclampsia and eclampsia", "Intrauterine infection and DIC/hypofibrinogenemia", "Placenta previa and abruption", "Postterm pregnancy and macrosomia"],
         "correct": 1, "explain": "The two complications of IUFD are: (1) Intrauterine infection, and (2) DIC and hypofibrinogenemia (especially after 3 weeks)."},
    ],
    "s7": [  # Management
        {"q": "What is the first principle of management after diagnosing IUFD?",
         "options": ["Expectant management for 4 weeks", "Termination of pregnancy should be offered", "Anticoagulation therapy", "Immediate cesarean section"],
         "correct": 1, "explain": "The first principle is that termination of pregnancy should be offered after diagnosis. Expectant management beyond 3-4 weeks without surveillance is dangerous."},
        {"q": "How is induction of labor accomplished in IUFD?",
         "options": ["Immediate cesarean section", "Preinduction cervical ripening followed by intravenous oxytocin", "Prostaglandin E2 alone", "Manual dilatation"],
         "correct": 1, "explain": "Induction of labor can be accomplished with preinduction cervical ripening followed by intravenous oxytocin. Cesarean section is reserved for failed induction."},
    ],
}

# ===== 9. 46_Assessment_of_Fetal_Well-being =====
MCQ_46 = {
    "s2": [  # NST
        {"q": "What defines a normal (reactive) non-stress test (NST)?",
         "options": ["Presence of two or more FHR accelerations peaking at ≥ 15 bpm above baseline, each lasting ≥ 15 seconds, within 20 minutes", "Baseline FHR of 120-160 bpm with no decelerations", "At least 3 fetal movements in 30 minutes", "FHR variability ≥ 6 bpm"],
         "correct": 0, "explain": "A reactive NST requires two or more accelerations that peak at ≥ 15 bpm above baseline, each lasting ≥ 15 seconds, all occurring within 20 minutes."},
        {"q": "What is the frequency of NST testing in high-risk pregnancies?",
         "options": ["Every 7 days", "More frequent than 7 days for postterm, type 1 DM, IUGR, or hypertension", "Daily", "Weekly after 36 weeks"],
         "correct": 1, "explain": "The standard interval is 7 days, but more frequent testing is recommended for women with postterm pregnancy, type 1 diabetes, IUGR, or maternal hypertension."},
        {"q": "What characterizes an abnormal NST?",
         "options": ["FHR accelerations with fetal movement", "FHR baseline oscillating less than 5 bpm", "FHR baseline > 160 bpm", "Presence of variable decelerations"],
         "correct": 1, "explain": "An abnormal NST is characterized by a fetal heart rate baseline that oscillates less than 5 beats per minute."},
    ],
    "s3": [  # CST
        {"q": "What defines a negative (normal) Contraction Stress Test (CST)?",
         "options": ["No late or significant variable decelerations", "Late decelerations following 50% or more of contractions", "Fewer than 3 contractions in 10 minutes", "Fetal tachycardia present"],
         "correct": 0, "explain": "A negative CST shows no late or significant variable decelerations. A positive CST shows late decelerations following 50% or more of contractions."},
        {"q": "How are uterine contractions induced during a CST?",
         "options": ["By maternal exercise", "By breast stimulation or oxytocin infusion", "By abdominal palpation", "By suprapubic pressure"],
         "correct": 1, "explain": "The CST evaluates FHR in response to uterine contractions induced by breast stimulation or oxytocin infusion, typically aiming for 3 contractions in a 10-minute period."},
    ],
    "s4": [  # CTG
        {"q": "What are the five components of CTG interpretation?",
         "options": ["FHR baseline, variability, accelerations, decelerations, uterine activity", "Fetal movement, breathing, tone, AF volume, reactivity", "NST, CST, BPP, Doppler, scalp pH", "Maternal heart rate, contractions, blood pressure, oxygen saturation, temperature"],
         "correct": 0, "explain": "The five components are: (1) Uterine activity (contractions), (2) Baseline FHR, (3) Baseline FHR variability, (4) Presence of accelerations, (5) Periodic or episodic decelerations."},
        {"q": "What is the definition of tachysystole on CTG?",
         "options": [">3 contractions in 10 minutes", ">5 contractions in 10 minutes, averaged over a 30-minute window", ">8 contractions in 10 minutes", ">10 contractions in 60 minutes"],
         "correct": 1, "explain": "Tachysystole is defined as >5 contractions in 10 minutes, averaged over a 30-minute window. Normal uterine activity is ≤ 5 contractions in 10 minutes."},
    ],
    "s5": [  # CTG parameters
        {"q": "According to NICE 2022, what is the normal baseline FHR on CTG?",
         "options": ["100-150 bpm", "110-160 bpm", "120-180 bpm", "90-140 bpm"],
         "correct": 1, "explain": "Normal baseline FHR is 110-160 beats per minute. Below 100 bpm is Red (abnormal), above 160 bpm is also Red (abnormal)."},
        {"q": "According to NICE 2022, what is normal FHR variability?",
         "options": ["Less than 5 bpm", "5-25 bpm", "More than 25 bpm", "10-30 bpm"],
         "correct": 1, "explain": "Normal FHR variability is 5-25 bpm. Fewer than 5 bpm for > 50 minutes is Red (abnormal), and more than 25 bpm for > 10 minutes is also Red (abnormal)."},
        {"q": "According to NICE 2022, what defines a Red (abnormal) CTG for decelerations?",
         "options": ["Early decelerations", "Repetitive variable decelerations > 30 minutes or repetitive late decelerations > 30 minutes", "No decelerations", "Variable decelerations < 30 minutes"],
         "correct": 1, "explain": "Red (abnormal) for decelerations is: repetitive variable decelerations for more than 30 minutes, or repetitive late decelerations for more than 30 minutes."},
    ],
    "s6": [  # BPP
        {"q": "What are the five components of the Biophysical Profile (BPP)?",
         "options": ["FHR reactivity, fetal tone, fetal movement, fetal breathing, amniotic fluid index", "NST, CST, CTG, Doppler, scalp pH", "FHR, EFW, AFI, placental grade, umbilical Doppler", "Fetal movement, kick count, NST, AFI, Doppler"],
         "correct": 0, "explain": "The 5 BPP components are: FHR reactivity (NST), fetal tone (extremity extension/flexion), fetal movement (≥ 3 gross body movements), fetal breathing (≥ 30 seconds), and amniotic fluid index (pocket > 2 cm or AFI > 5 cm)."},
        {"q": "What does a BPP score of 6 indicate?",
         "options": ["Normal fetal well-being", "Equivocal test, needs to be repeated", "Abnormal outcome, needs delivery", "Fetal death"],
         "correct": 1, "explain": "A BPP score of 8 or 10 indicates good fetal well-being. A score of 6 is equivocal and needs to be repeated. A score of 4 or less is a predictor of abnormal outcome."},
        {"q": "What is the maximum BPP score?",
         "options": ["8", "10", "12", "6"],
         "correct": 1, "explain": "The maximum BPP score is 10 (each of the 5 components scores either 2 for normal or 0 for abnormal). Components: FHR reactivity, fetal tone, fetal movement, fetal breathing, and AFI."},
    ],
    "s7": [  # Doppler
        {"q": "What does absent or reversed end-diastolic flow in the umbilical artery indicate?",
         "options": ["Normal placental function", "Increased resistance to umbilical artery blood flow, seen in extreme cases of fetal growth restriction", "Fetal anemia", "Maternal hypertension"],
         "correct": 1, "explain": "Absent or reversed end-diastolic flow indicates increased resistance to umbilical artery blood flow, resulting from poorly vascularized placental villi, seen in the most extreme cases of fetal growth restriction."},
        {"q": "What is the most commonly used index for umbilical artery Doppler assessment?",
         "options": ["Resistance index (RI)", "Pulsatility index (PI)", "Systolic/diastolic (S/D) ratio", "Peak systolic velocity (PSV)"],
         "correct": 2, "explain": "The umbilical artery systolic/diastolic (S/D) ratio is the most commonly used index, considered abnormal if above the 95th percentile for gestational age."},
    ],
    "s8": [  # Scalp blood
        {"q": "What is the purpose of fetal scalp blood sampling during labor?",
         "options": ["To determine fetal blood group", "For fetal acid-base determination to assess hypoxia/acidosis", "To check fetal hemoglobin level", "To diagnose fetal infection"],
         "correct": 1, "explain": "Fetal acid-base determination from a scalp blood sample is used to assess fetal hypoxia/acidosis during labor, though it carries risks of fetal infection and hemorrhage."},
    ],
}

# ===== 10. 30_Multiple_Pregnancy =====
MCQ_30 = {
    "s2": [  # Definition
        {"q": "What is the definition of multiple pregnancy?",
         "options": ["Pregnancy with more than 2 fetuses", "Pregnancy with more than 1 fetus inside the uterus", "Twin pregnancy only", "Pregnancy resulting from assisted reproduction"],
         "correct": 1, "explain": "Multiple pregnancy is defined as a pregnancy with more than 1 fetus inside the uterus."},
        {"q": "What is the incidence of twin pregnancy?",
         "options": ["1 in 40", "1 in 80", "1 in 200", "1 in 120"],
         "correct": 1, "explain": "The incidence of twins is 1 in 80 pregnancies. For triplets, it is 1 in 80² (approximately 1 in 6,400)."},
    ],
    "s4": [  # Monoz vs Dizyg
        {"q": "Dizygotic (fraternal) twins are always:",
         "options": ["Monochorionic", "Dichorionic-Diamniotic (DCDA)", "Monochorionic-Monoamniotic (MCMA)", "Conjoined"],
         "correct": 1, "explain": "Dizygotic twins always result in a dichorionic-diamniotic (DCDA) configuration because they arise from two separate zygotes with separate implantations."},
        {"q": "If monozygotic cleavage occurs at days 4-8 (blastocyst stage), what is the resulting configuration?",
         "options": ["DCDA (2 placentas, 2 sacs)", "MCDA (1 placenta, 2 sacs)", "MCMA (1 placenta, 1 sac)", "Conjoined twins"],
         "correct": 1, "explain": "Cleavage at days 4-8 (after chorion formation but before amnion formation) results in MCDA twins — one placenta (shared chorion) but two amniotic sacs."},
        {"q": "At what stage of monozygotic cleavage does conjoined twinning occur?",
         "options": ["Days 1-3 (morula stage)", "Days 4-8 (blastocyst stage)", "Days 8-12 (implanted blastocyst)", "Beyond day 12 (embryonic disc stage)"],
         "correct": 3, "explain": "Conjoined twins occur when monozygotic cleavage occurs beyond day 12, when the embryonic disc has already formed and complete separation is no longer possible."},
    ],
    "s6": [  # Diagnosis
        {"q": "Which ultrasound sign indicates dichorionic-diamniotic (DCDA) twins?",
         "options": ["T sign", "Lambda sign (thick triangular wedge of tissue)", "Absent intertwin membrane", "Single placental mass"],
         "correct": 1, "explain": "The Lambda sign (λ) — a thick, triangular protrusion of tissue leading up to the intertwin membrane — indicates DCDA twins (2 placentas, thick membrane)."},
        {"q": "What does the T sign on ultrasound indicate about chorionicity?",
         "options": ["DCDA (dichorionic)", "MCDA (monochorionic-diamniotic)", "MCMA (monochorionic-monoamniotic)", "Conjoined twins"],
         "correct": 1, "explain": "The T sign — where two thin amniotic membranes meet the placenta at a right angle with no wedge of chorion — indicates MCDA twins (one placenta, thin membrane)."},
        {"q": "Which clinical finding on abdominal examination suggests multiple pregnancy?",
         "options": ["Small fundal height", "Palpation of ≥ 3 fetal poles and hearing ≥ 2 fetal heart rates at least 10 bpm apart", "Single fetal pole palpated", "Oligohydramnios"],
         "correct": 1, "explain": "Diagnosis includes palpation of ≥ 3 fetal poles, ≥ 2 fetal heart rates at least 10 bpm apart, and Arnaux sign/gallop."},
    ],
    "s8": [  # Antenatal Mgmt
        {"q": "How many antenatal care adjustments are recommended for multiple pregnancy?",
         "options": ["3", "5", "7", "10"],
         "correct": 2, "explain": "Seven antenatal care adjustments are recommended: high-risk designation, more frequent visits, more frequent ultrasounds, adequate nutrition, monitoring for maternal complications, monitoring for fetal complications, and prevention of preterm delivery."},
        {"q": "Why is multiple pregnancy considered a high-risk pregnancy?",
         "options": ["It always requires cesarean section", "It concentrates the risks of singleton pregnancy and adds new risks", "It is always associated with fetal anomalies", "It requires hospitalization from 28 weeks"],
         "correct": 1, "explain": "A multiple pregnancy concentrates the risks of a singleton pregnancy and adds new risks of its own (TTTS, increased preeclampsia/GDM, higher preterm rate), so antenatal care is intensified proportionally."},
    ],
    "s9": [  # Obstetric Mgmt
        {"q": "When is cesarean section mandatory for twin delivery?",
         "options": ["Vertex/vertex presentation", "Non-vertex presenting twin, triplets, and monochorionic-monoamniotic twins", "Vertex/non-vertex presentation", "All twin pregnancies"],
         "correct": 1, "explain": "CS is mandatory for: (1) non-vertex presenting twin, (2) all higher-order multiples (triplets+), and (3) MCMA twins. Vertex/vertex = vaginal delivery candidate."},
        {"q": "What is the recommended timing of delivery for monochorionic-diamniotic twins?",
         "options": ["38 0/7 - 38 6/7 weeks", "34 0/7 - 37 6/7 weeks", "32 0/7 - 34 6/7 weeks", "39 0/7 - 40 6/7 weeks"],
         "correct": 1, "explain": "MCDA twins: 34 0/7 - 37 6/7 weeks. DCDA: 38 weeks. MCMA: 32-34 weeks. The more structures shared, the earlier the delivery."},
        {"q": "Which third-stage precaution is specifically important in multiple pregnancy?",
         "options": ["Fetal blood sampling", "Guard against postpartum hemorrhage by uterine massage and ecbolics", "External cephalic version", "Cord blood banking"],
         "correct": 1, "explain": "Guarding against postpartum hemorrhage by uterine massage and ecbolics is critical — the overdistended uterus is prone to atony. Other third-stage measures include placental examination, retained products management, genital exploration, and puerperal sepsis prevention."},
    ],
    "s10": [  # Maternal complications
        {"q": "Which maternal complication occurs 2-3 times more often in twin versus singleton pregnancies?",
         "options": ["Placental abruption", "GDM, preeclampsia, anemia, and PPH", "Umbilical cord prolapse", "Oligohydramnios"],
         "correct": 1, "explain": "GDM, preeclampsia, anemia, PPH, and preterm labor occur 2-3 times more often in twin pregnancies than in singleton pregnancies due to doubled placental mass and cardiovascular demand."},
        {"q": "Which of these is NOT a maternal complication of multiple pregnancy?",
         "options": ["Hyperemesis gravidarum", "Placental abnormalities (e.g., placenta previa)", "Twin-to-twin transfusion syndrome", "Excessive weight gain"],
         "correct": 2, "explain": "TTTS is a fetal complication (unique to monochorionic twins), not a maternal complication. Maternal complications include hyperemesis, GDM, hypertension, anemia, weight gain, PPH, miscarriage, previa, and increased CS rate."},
    ],
    "s11": [  # Fetal complications
        {"q": "What is the most common fetal complication of multiple pregnancy?",
         "options": ["Congenital anomalies", "Preterm labor and birth", "Discordant growth", "TTTS"],
         "correct": 1, "explain": "Preterm labor and birth is the most common fetal complication — the overdistended uterus triggers earlier labor. Mean gestational age for twins is ~36 weeks, with ~50% delivering before 37 weeks."},
    ],
    "s12": [  # TTTS
        {"q": "What percentage of monochorionic twins develop Twin-to-Twin Transfusion Syndrome (TTTS)?",
         "options": ["1-5%", "10-15%", "20-30%", "50-60%"],
         "correct": 1, "explain": "TTTS occurs in 10-15% of monochorionic twins due to arterio-venous anastomosis with imbalanced blood flow from the donor to the recipient."},
        {"q": "In TTTS, which findings characterize the donor twin?",
         "options": ["Polycythemia, macrosomia, polyhydramnios", "Anemia, growth restriction, oligohydramnios", "Normal growth, normal fluid", "Hydrops, heart failure"],
         "correct": 1, "explain": "The donor twin (gives blood away) develops: anemia (low red-cell mass), growth restriction (poor perfusion), and oligohydramnios (low fluid — 'stuck twin' sign)."},
        {"q": "In TTTS, which findings characterize the recipient twin?",
         "options": ["Anemia, growth restriction, oligohydramnios", "Polycythemia, macrosomia, polyhydramnios", "Normal blood count, normal growth", "IUGR, anhydramnios"],
         "correct": 1, "explain": "The recipient twin (receives excess blood) develops: polycythemia (high red-cell mass), macrosomia (excess perfusion), and polyhydramnios (overdistended sac)."},
        {"q": "What is the definitive treatment for severe TTTS?",
         "options": ["Amnioreduction alone", "Fetoscopic laser occlusion of placental vessels", "Selective reduction", "Early delivery"],
         "correct": 1, "explain": "Fetoscopic laser occlusion of placental vessels is the definitive treatment for severe TTTS — it separates the two fetal circulations by ablating the anastomoses. Amnioreduction is a temporizing measure."},
    ],
}

# ===== File mapping =====
# Each entry: (source_path_rel, output_path_rel, mcq_data)
# The output dir mirrors the input dir structure

FILE_MAP = [
    # 1
    ("Polyhydramnios_IUGR_shoulder_dystocia/18_Amniotic_Fluid_Abnormalities.html",
     "Polyhydramnios_IUGR_shoulder_dystocia/18_Amniotic_Fluid_Abnormalities.html",
     MCQ_18),
    # 2
    ("Polyhydramnios_IUGR_shoulder_dystocia/29_Shoulder_Dystocia.html",
     "Polyhydramnios_IUGR_shoulder_dystocia/29_Shoulder_Dystocia.html",
     MCQ_29),
    # 3
    ("Polyhydramnios_IUGR_shoulder_dystocia/40_Intrauterine_Growth_Restriction.html",
     "Polyhydramnios_IUGR_shoulder_dystocia/40_Intrauterine_Growth_Restriction.html",
     MCQ_40),
    # 4
    ("Polyhydramnios_IUGR_shoulder_dystocia/42_Macrosomia.html",
     "Polyhydramnios_IUGR_shoulder_dystocia/42_Macrosomia.html",
     MCQ_42),
    # 5
    ("PROM_preterm_post_term_pregnancy/31_Preterm_Labor.html",
     "PROM_preterm_post_term_pregnancy/31_Preterm_Labor.html",
     MCQ_31),
    # 6
    ("PROM_preterm_post_term_pregnancy/32_Premature_Rupture_of_Membranes_PROM.html",
     "PROM_preterm_post_term_pregnancy/32_Premature_Rupture_of_Membranes_PROM.html",
     MCQ_32),
    # 7
    ("PROM_preterm_post_term_pregnancy/41_Postterm_Pregnancy.html",
     "PROM_preterm_post_term_pregnancy/41_Postterm_Pregnancy.html",
     MCQ_41),
    # 8
    ("Assessment_of_fetal_wellbeing/43_Intrauterine_Fetal_Death.html",
     "Assessment_of_fetal_wellbeing/43_Intrauterine_Fetal_Death.html",
     MCQ_43),
    # 9
    ("Assessment_of_fetal_wellbeing/46_Assessment_of_Fetal_Well-being.html",
     "Assessment_of_fetal_wellbeing/46_Assessment_of_Fetal_Well-being.html",
     MCQ_46),
    # 10
    ("High_risk_pregnancy_identification/30_Multiple_Pregnancy.html",
     "High_risk_pregnancy_identification/30_Multiple_Pregnancy.html",
     MCQ_30),
]


def has_section_tags(html):
    """Check if HTML uses <section id=...> tags (process_file compatible)."""
    return bool(re.search(r'<section\s+(?:class="[^"]*"\s+)?id="[^"]*"', html))


def main():
    os.makedirs(BASE_OUT, exist_ok=True)
    
    # Also create subdirectories
    for rel_in, rel_out, _ in FILE_MAP:
        out_subdir = os.path.dirname(os.path.join(BASE_OUT, rel_out))
        os.makedirs(out_subdir, exist_ok=True)
    
    success = 0
    failed = 0
    
    for rel_in, rel_out, mcq_data in FILE_MAP:
        input_path = os.path.join(BASE_IN, rel_in)
        output_path = os.path.join(BASE_OUT, rel_out)
        
        if not os.path.exists(input_path):
            print(f"✗ NOT FOUND: {input_path}")
            failed += 1
            continue
        
        try:
            # Read the HTML
            with open(input_path, 'r', encoding='utf-8') as f:
                html = f.read()
            
            # Check if it uses <section> tags
            if has_section_tags(html):
                # Use process_file directly
                process_file(input_path, output_path, mcq_data)
            else:
                # Handle files with <div class="section" id="..."> or <div class="sh" id="...">
                # We need custom injection logic
                custom_inject(input_path, output_path, mcq_data, html)
            
            success += 1
            file_count = sum(len(v) for v in mcq_data.values())
            print(f"  └─ {file_count} MCQs across {len(mcq_data)} sections")
            
        except Exception as e:
            print(f"✗ ERROR processing {rel_in}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: {success} files processed successfully, {failed} failed")
    print(f"{'='*60}")


def custom_inject(input_path, output_path, mcq_data, html):
    """Custom injection for files that use <div class=... id=...> instead of <section id=...>."""
    
    # Find all section divs with ids
    # Pattern matches: <div class="section" id="sX"> or <div class="sh" id="sX">
    pattern = re.compile(r'<(?:div|section)(?:\s+class="[^"]*")?\s+id="([^"]*)"', re.IGNORECASE)
    
    sections = []
    for m in pattern.finditer(html):
        sec_id = m.group(1)
        # Find a heading within the next 500 chars
        after = html[m.start():m.start()+1500]
        h_match = re.search(r'<h[234][^>]*>(.*?)</h[234]>', after)
        heading = h_match.group(1) if h_match else sec_id
        heading = re.sub(r'<[^>]+>', '', heading).strip()
        sections.append({'id': sec_id, 'heading': heading, 'start': m.start()})
    
    # Sort and set end boundaries
    sections.sort(key=lambda s: s['start'])
    for i in range(len(sections)):
        if i + 1 < len(sections):
            sections[i]['end'] = sections[i+1]['start']
        else:
            sections[i]['end'] = len(html)
    
    # Skip sections with keywords
    skip_keywords = ['ilos', 'study activity', 'reference', 'questions', 'table of contents',
                     'intended learning', 'contents', 'sources']
    
    inserted = 0
    for sec in sections:
        sec_id = sec['id'].lower()
        sec_hdg = sec['heading'].lower()
        
        skip = False
        for kw in skip_keywords:
            if kw in sec_id or kw in sec_hdg:
                skip = True
                break
        
        if skip:
            continue
        
        if sec_id in mcq_data:
            mcqs = mcq_data[sec_id]
            if mcqs:
                mcq_html = build_mcq_block(mcqs, sec_id)
                # Inject before the next section's start or within current section
                section_end = sec['end']
                # Find closing tag (</section> or </div>)
                close_seg = html.rfind('</section>', 0, section_end)
                close_div = html.rfind('</div>', 0, section_end)
                close_idx = max(close_seg, close_div)
                
                # If no closing found near the end, try </section> or </div> 
                if close_idx == -1 or close_idx < sec['start']:
                    # Find the next occurrence after the section start
                    close_seg = html.find('</section>', sec['start'])
                    close_div = html.find('</div>', sec['start'])
                    if close_seg != -1 and (close_div == -1 or close_seg < close_div):
                        close_idx = close_seg
                    elif close_div != -1:
                        close_idx = close_div
                    else:
                        # Fall back to inserting at section_end
                        close_idx = section_end
                
                # Make sure we don't go beyond another section
                for other in sections:
                    if other['start'] > sec['start'] and other['start'] < close_idx:
                        close_idx = other['start']
                        break
                
                html = html[:close_idx] + '\n' + mcq_html + '\n' + html[close_idx:]
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
    
    print(f"✓ {os.path.basename(input_path)} → {inserted} subtopics injected (custom)")


if __name__ == '__main__':
    main()
