#!/usr/bin/env python3
"""
Inject MCQs into all 4 Week 2 obstetrics files.
Usage: python3 run_inject_all.py
"""
import sys
import os

# Add current dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inject_mcqs import process_file

BASE = "extracted/assets/second task/obstetric/Week2"
ENH  = "enhanced-assets/second task/obstetric/Week2"

# =============================================================================
# FILE 1: 31_Preterm_Labor.html
# =============================================================================
mcq_31 = {
    # s2: Definition
    "s2": [
        {
            "q": "Preterm labor is defined as regular uterine contractions associated with cervical change occurring between:",
            "options": ["16 to 34 weeks' gestation", "20 to 37 weeks' gestation", "24 to 40 weeks' gestation", "28 to 36 weeks' gestation"],
            "correct": 1,
            "explain": "Preterm labor is defined as regular uterine contractions with cervical change between 20 and 37 weeks' gestation. The 20-week lower bound distinguishes it from late miscarriage."
        },
        {
            "q": "What distinguishes true preterm labor from Braxton-Hicks contractions?",
            "options": ["Pain intensity alone", "Effacement and dilatation of the cervix", "Maternal heart rate > 100 bpm", "Gestational age < 28 weeks"],
            "correct": 1,
            "explain": "Effacement and dilatation of the cervix distinguishes true labor from Braxton-Hicks contractions. Regular contractions alone are not sufficient for diagnosis."
        },
        {
            "q": "A premature infant is defined as an infant born:",
            "options": ["Before 34 completed weeks", "Before 37 completed weeks", "Before 40 completed weeks", "Before 32 completed weeks"],
            "correct": 1,
            "explain": "A premature infant is an infant born before 37 completed weeks of gestation."
        }
    ],
    # s3: Maternal RF
    "s3": [
        {
            "q": "What is the most common cause of preterm labor?",
            "options": ["Cervical incompetence", "Idiopathic (no specific risk factor identified)", "Multiple gestation", "Maternal infection"],
            "correct": 1,
            "explain": "The most common cause of preterm labor is idiopathic — i.e., when no specific risk factor is identified, idiopathic remains the leading cause."
        },
        {
            "q": "Which of the following is NOT a maternal risk factor for preterm labor?",
            "options": ["Uterine overdistension (multiple gestations, polyhydramnios)", "Previous preterm labor", "Fetal congenital anomalies", "Maternal age extremes (< 18 or > 35 years)"],
            "correct": 2,
            "explain": "Fetal congenital anomalies are a fetal cause/risk factor, not a maternal one. Maternal risk factors include previous preterm labor, infection, uterine anomalies, smoking, obesity, overdistension, maternal age extremes, and bleeding."
        },
        {
            "q": "Uterine overdistension as a maternal risk factor for PTL can result from:",
            "options": ["Uterine fibroids", "Multiple gestations and polyhydramnios", "Endometriosis", "Cervical incompetence"],
            "correct": 1,
            "explain": "Multiple gestations (twins, triplets) and polyhydramnios mechanically stretch the myometrium, leading to uterine overdistension — a recognized maternal risk factor for preterm labor."
        }
    ],
    # s4: Fetal causes
    "s4": [
        {
            "q": "Which of the following are fetal causes/risk factors for preterm labor?",
            "options": ["Smoking and obesity", "Previous preterm labor", "Fetal anomalies and IUGR", "Uterine anomalies and incompetent os"],
            "correct": 2,
            "explain": "Fetal causes of preterm labor include fetal anomalies (congenital structural malformations) and intrauterine growth restriction (IUGR)."
        },
        {
            "q": "A compromised fetus may trigger earlier delivery in preterm labor through which fetal risk factor?",
            "options": ["Fetal macrosomia", "Intrauterine growth restriction (IUGR)", "Polyhydramnios", "Cord prolapse"],
            "correct": 1,
            "explain": "IUGR (intrauterine growth restriction) — a compromised fetus may trigger earlier delivery as a fetal cause of preterm labor."
        },
        {
            "q": "Congenital structural malformations associated with preterm labor include all EXCEPT:",
            "options": ["Neural tube defects", "Cardiac anomalies", "Adrenal hypoplasia", "Hydrocephalus"],
            "correct": 2,
            "explain": "Adrenal hypoplasia is associated with postterm pregnancy (diminished fetal cortisol response), not preterm labor. Neural tube defects and cardiac anomalies are fetal causes of PTL."
        }
    ],
    # s5: Diagnosis sx/signs
    "s5": [
        {
            "q": "According to the textbook, the contraction-frequency threshold that defines active preterm labor is:",
            "options": ["2 contractions in 10 minutes", "4 contractions in 20 minutes or 8 in 60 minutes", "6 contractions in 30 minutes", "Continuous contractions lasting > 2 minutes"],
            "correct": 1,
            "explain": "The '4 in 20 / 8 in 60' rule is the textbook definition of active preterm labor — this frequency triggers tocolysis and corticosteroids."
        },
        {
            "q": "Which of the following is a symptom/sign of preterm labor?",
            "options": ["Decreased fetal movements", "Passage of blood-stained vaginal discharge (show)", "Polyhydramnios", "Maternal hypotension"],
            "correct": 1,
            "explain": "Symptoms and signs of PTL include uterine contractions (4 in 20 min or 8 in 60 min), lower back pain, passage of blood-stained vaginal discharge (show), sensation of pelvic pressure, and bulging membranes / rupture of membranes."
        },
        {
            "q": "The sensation of pelvic pressure in preterm labor is described as:",
            "options": ["Sharp stabbing pain in the upper abdomen", "Feeling that the fetus is pushing down", "Constant dull ache in the right flank", "Burning sensation during urination"],
            "correct": 1,
            "explain": "Sensation of pelvic pressure is described as a feeling that the fetus is pushing down — a classic symptom of preterm labor."
        }
    ],
    # s6: Investigations
    "s6": [
        {
            "q": "The normal shape of the cervix on transvaginal ultrasound progresses through which sequence as preterm labor approaches?",
            "options": ["U → V → Y → T", "T → Y → V → U", "Y → T → U → V", "V → U → T → Y"],
            "correct": 1,
            "explain": "The cervical shape progression is T → Y → V → U. A U-shaped cervix on TVUS indicates imminent delivery."
        },
        {
            "q": "What is the diagnostic window for the fetal fibronectin test in predicting preterm labor?",
            "options": ["20 to 28 weeks", "24 to 34 weeks", "28 to 37 weeks", "16 to 24 weeks"],
            "correct": 1,
            "explain": "The fetal fibronectin test is useful only between 24 and 34 weeks. Before 24 weeks, fibronectin may normally be present; after 34 weeks, its presence is no longer predictive."
        },
        {
            "q": "On transvaginal ultrasound, a cervical dilatation greater than what measurement suggests preterm labor?",
            "options": ["1 cm", "2 cm", "3 cm", "4 cm"],
            "correct": 1,
            "explain": "Transvaginal ultrasound showing dilatation of cervix > 2 cm is suggestive of preterm labor."
        }
    ],
    # s7: Prophylactic Mgmt
    "s7": [
        {
            "q": "Which of the following is a prophylactic measure for preterm labor in women with cervical incompetence?",
            "options": ["Bed rest at 20 weeks", "Cerclage surgery", "Antenatal corticosteroids at 28 weeks", "Tocolysis at 32 weeks"],
            "correct": 1,
            "explain": "Cerclage surgery (e.g., McDonald or Shirodkar suture) is placed prophylactically in women with a history of cervical insufficiency, typically at 12–14 weeks, and removed at 36–37 weeks."
        },
        {
            "q": "Prophylactic management of preterm labor includes all of the following EXCEPT:",
            "options": ["Smoking cessation", "Cerclage surgery", "Progesterone", "Intravenous tocolysis"],
            "correct": 3,
            "explain": "Prophylactic measures include stopping smoking, cerclage surgery (if cervical incompetence), and progesterone. IV tocolysis is part of curative/acute management, not prophylaxis."
        },
        {
            "q": "At what gestational age is a prophylactic cerclage typically placed?",
            "options": ["6–8 weeks", "12–14 weeks", "20–24 weeks", "28–32 weeks"],
            "correct": 1,
            "explain": "Cerclage is placed prophylactically at 12–14 weeks and removed at 36–37 weeks."
        }
    ],
    # s8: Curative Mgmt
    "s8": [
        {
            "q": "The three drug therapy pillars in curative management of established preterm labor are:",
            "options": ["Antibiotics, antihypertensives, and magnesium sulfate", "Corticosteroids, tocolytics, and antibiotics", "Oxytocin, prostaglandins, and ergometrine", "Analgesics, sedatives, and antispasmodics"],
            "correct": 1,
            "explain": "In established PTL, the three drug-therapy pillars are corticosteroids (for fetal lung maturity), tocolytics (to delay delivery 48 hours), and antibiotics (for GBS prophylaxis)."
        },
        {
            "q": "Why are tocolytics given alongside corticosteroids in preterm labor management?",
            "options": ["To prevent maternal hypertension", "To buy 48 hours for corticosteroids to act on fetal lung maturity", "To reduce fetal heart rate", "To treat chorioamnionitis"],
            "correct": 1,
            "explain": "Corticosteroids need ~48 hours to complete their effect on fetal lung surfactant production. Tocolytics are given to delay delivery for those 48 hours."
        },
        {
            "q": "Bed rest as part of curative management of PTL works by:",
            "options": ["Increasing uterine blood flow", "Reducing gravitational and mechanical stimulus on the cervix", "Preventing dehydration", "Stimulating surfactant production"],
            "correct": 1,
            "explain": "Bed rest reduces the gravitational and mechanical stimulus on the cervix, which may delay delivery."
        }
    ],
    # s9: Corticosteroids
    "s9": [
        {
            "q": "The recommended dose of betamethasone for fetal lung maturity is:",
            "options": ["6 mg IM × 4 doses, 12 hours apart", "12 mg IM × 2 doses, 24 hours apart", "12 mg IV × 2 doses, 12 hours apart", "6 mg IM × 2 doses, 24 hours apart"],
            "correct": 1,
            "explain": "Betamethasone is given as 2 doses of 12 mg IM, 24 hours apart."
        },
        {
            "q": "The recommended dose of dexamethasone for fetal lung maturity is:",
            "options": ["12 mg IM × 2 doses, 24 hours apart", "6 mg IM × 4 doses, 12 hours apart", "8 mg IV × 3 doses, 8 hours apart", "4 mg IM × 4 doses, 6 hours apart"],
            "correct": 1,
            "explain": "Dexamethasone is given as 4 doses of 6 mg IM, 12 hours apart."
        },
        {
            "q": "Corticosteroids in preterm labor decrease the risk of which neonatal complication?",
            "options": ["Neonatal jaundice", "Respiratory distress syndrome (RDS)", "Hypoglycemia", "Congenital pneumonia"],
            "correct": 1,
            "explain": "Corticosteroids decrease the chance of respiratory distress syndrome (RDS) and other prematurity complications including IVH, NEC, and neonatal mortality."
        }
    ],
    # s10: Tocolysis
    "s10": [
        {
            "q": "Which of the following is an absolute contraindication to tocolysis?",
            "options": ["Maternal diabetes", "Chorioamnionitis", "Oligohydramnios", "Multiple gestation"],
            "correct": 1,
            "explain": "Chorioamnionitis is an absolute contraindication to tocolysis. Others include advanced labor, pregnancy > 34 weeks, pre-eclampsia/eclampsia, abruptio placenta, fetal demise/distress, and lethal congenital anomaly."
        },
        {
            "q": "Which class of tocolytic drug does Nifedipine belong to?",
            "options": ["Prostaglandin synthetase inhibitor", "Calcium channel blocker", "Oxytocin antagonist", "Beta agonist"],
            "correct": 1,
            "explain": "Nifedipine is a calcium channel blocker. Its initial dose is 20 mg orally, followed by another 20 mg after 30 minutes, then maintenance 20 mg every 4-8 hours (max 160 mg/day)."
        },
        {
            "q": "Indomethacin should NOT be used after which gestational age due to risk of premature ductus arteriosus closure?",
            "options": ["24 weeks", "30 weeks", "34 weeks", "28 weeks"],
            "correct": 1,
            "explain": "Indomethacin, a prostaglandin synthetase inhibitor, is not used after 30 weeks' gestation due to the risk of premature closure of the ductus arteriosus."
        },
        {
            "q": "Atosiban is classified as which type of tocolytic drug?",
            "options": ["Beta agonist", "Calcium channel blocker", "Oxytocin antagonist", "Nitric oxide donor"],
            "correct": 2,
            "explain": "Atosiban is an oxytocin antagonist. Dosing: 6.75 mg IV bolus, then 300 μg/min IV for 3 hours, then 100 μg/min. It is very expensive."
        }
    ],
    # s12: Antibiotic+mode
    "s12": [
        {
            "q": "Which antibiotic is used for GBS prophylaxis in established preterm labor?",
            "options": ["Gentamicin", "Benzyl penicillin or ampicillin", "Metronidazole", "Ceftriaxone"],
            "correct": 1,
            "explain": "Benzyl penicillin or ampicillin should be given for established PTL as prophylaxis against early onset neonatal sepsis due to group B streptococcus. In penicillin allergy, clindamycin can be used."
        },
        {
            "q": "In a preterm labor patient with breech presentation at 32 weeks, the recommended mode of delivery is:",
            "options": ["Vaginal delivery", "Cesarean section", "Trial of forceps", "Vacuum extraction"],
            "correct": 1,
            "explain": "For breech presentation before 34 weeks, cesarean section is done. Vaginal delivery is allowed for breech only if more than 34 weeks."
        },
        {
            "q": "For preterm labor with cephalic presentation, the preferred mode of delivery is:",
            "options": ["Cesarean section for all gestations", "Vaginal delivery even if < 34 weeks", "Forceps delivery required", "Vacuum extraction"],
            "correct": 1,
            "explain": "With cephalic presentation, vaginal delivery is the preferred mode even if delivery is at < 34 weeks."
        }
    ]
}

# =============================================================================
# FILE 2: 32_Premature_Rupture_of_Membranes_PROM.html
# =============================================================================
mcq_32 = {
    # s2: Definition
    "s2": [
        {
            "q": "PROM is defined as:",
            "options": ["Rupture of membranes after the onset of labor", "Spontaneous rupture of fetal membranes before the onset of labor", "Rupture of membranes at full dilatation", "Artificial rupture of membranes during induction"],
            "correct": 1,
            "explain": "PROM is a spontaneous rupture of the fetal membranes before the onset of labor."
        },
        {
            "q": "Preterm PROM (PPROM) is defined as rupture of membranes occurring:",
            "options": ["After 42 weeks", "Before 37 completed weeks of gestation", "Between 37 and 40 weeks", "Before 20 weeks"],
            "correct": 1,
            "explain": "Preterm PROM (PPROM) is spontaneous rupture of membranes before 37 completed weeks of gestation."
        },
        {
            "q": "The key feature that distinguishes PROM from normal rupture of membranes is:",
            "options": ["The color of the fluid", "The volume of fluid lost", "Rupture occurring before the onset of labor", "The presence of pain"],
            "correct": 2,
            "explain": "The phrase 'before the onset of labor' is what distinguishes PROM from the normal rupture of membranes that occurs during labor."
        }
    ],
    # s3: Etiology
    "s3": [
        {
            "q": "Which of the following is the most clinically important cause of PROM?",
            "options": ["Prior history of PPROM", "Intrauterine infection", "Amniocentesis", "Trauma"],
            "correct": 1,
            "explain": "Intrauterine infection (chorioamnionitis, subclinical deciduitis) is the most clinically important cause — infection weakens the chorioamniotic membranes and predisposes them to rupture."
        },
        {
            "q": "Which of the following is NOT one of the 5 classic etiologies of PROM?",
            "options": ["Intrauterine infection", "Prior history of PPROM", "Fetal macrosomia", "Polyhydramnios"],
            "correct": 2,
            "explain": "The 5 classic etiologies are: intrauterine infection, prior history of PPROM, trauma, amniocentesis, and polyhydramnios."
        },
        {
            "q": "Polyhydramnios causes PROM through which mechanism?",
            "options": ["Direct damage to fetal membranes by inflammation", "Mechanical over-distension of the uterus increasing membrane stress", "Inhibition of surfactant production", "Premature placental aging"],
            "correct": 1,
            "explain": "Polyhydramnios causes PROM by mechanically over-distending the uterus, increasing wall tension and membrane stress."
        }
    ],
    # s4: Presentation
    "s4": [
        {
            "q": "The typical presentation of PROM is:",
            "options": ["Gradual leaking of thick white discharge", "Sudden gush of clear or pale yellow fluid from vagina", "Blood-stained mucus plug passage", "Painful uterine contractions with heavy bleeding"],
            "correct": 1,
            "explain": "Patients present with a typical history of sudden gush of clear or pale yellow fluid leaking from the vagina."
        },
        {
            "q": "Meconium-stained (green/brown) fluid in suspected PROM suggests:",
            "options": ["Chorioamnionitis", "Fetal distress", ["Normal finding in PROM", "Maternal infection"]],
            "correct": 1,
            "explain": "Meconium-stained (green/brown) fluid suggests fetal distress, while foul-smelling fluid suggests chorioamnionitis."
        },
        {
            "q": "A history of a sudden, single, large gush of fluid followed by continued leakage is characteristic of:",
            "options": ["Urinary incontinence", "PROM", "Excessive vaginal discharge", ["Bacterial vaginosis"]],
            "correct": 1,
            "explain": "A history of a sudden, single, large gush followed by continued leakage distinguishes PROM from urinary incontinence (continuous, no gush) or excessive vaginal discharge (gradual, no gush)."
        }
    ],
    # s5: Diagnosis
    "s5": [
        {
            "q": "What is the first step in the diagnosis of PROM?",
            "options": ["Ultrasound examination", "Speculum examination", "Nitrazine test", "Fern test"],
            "correct": 1,
            "explain": "Speculum examination is the first step in the diagnosis of PROM — it is used to directly demonstrate leaking of fluid from the cervical os."
        },
        {
            "q": "The nitrazine test for PROM is based on which principle?",
            "options": ["Specific gravity of amniotic fluid", "pH difference: amniotic fluid (7–7.5) vs vaginal discharge (3.5–4.5)", "Protein concentration of amniotic fluid", "Glucose content of amniotic fluid"],
            "correct": 1,
            "explain": "The pH of amniotic fluid is 7–7.5 (alkaline) while vaginal discharge pH is 3.5–4.5 (acidic). Yellow nitrazine paper turning blue indicates alkaline amniotic fluid."
        },
        {
            "q": "A positive fern test for PROM appears as:",
            "options": ["A blue coloration on the slide", "Fern pattern (arborization) under microscopy after slide dries", "Crystal formation at the bottom of the tube", "Foam formation after shaking"],
            "correct": 1,
            "explain": "Fluid from the posterior vaginal fornix is swabbed on a glass slide and allowed to dry for 10 minutes. If a fern pattern (arborization) appears, amniotic fluid is present."
        },
        {
            "q": "Fetal fibronectin is detected in what percentage of females with PROM?",
            "options": ["89%", "39%", "59%", "75%"],
            "correct": 1,
            "explain": "Fetal fibronectin can be detected in only 39% of females with PROM by means of an ELISA test. Its sensitivity is limited."
        }
    ],
    # s6: Effects
    "s6": [
        {
            "q": "Which of the following is NOT one of the 4 effects of preterm PROM?",
            "options": ["Preterm labor", "Pulmonary hypoplasia", "Fetal macrosomia", "Chorioamnionitis"],
            "correct": 2,
            "explain": "The 4 effects of preterm PROM are: preterm labor, pulmonary hypoplasia, skeletal and joint deformities, and chorioamnionitis. Fetal macrosomia is associated with postterm pregnancy, not PROM."
        },
        {
            "q": "Pulmonary hypoplasia from PROM results from:",
            "options": ["Direct infection of fetal lung tissue", "Severe oligohydramnios impairing lung development", "Toxic effects of meconium", "Premature closure of the ductus arteriosus"],
            "correct": 1,
            "explain": "Pulmonary hypoplasia is due to severe oligohydramnios — the fetus needs amniotic fluid for normal lung development; severe fluid loss impairs alveolar formation."
        },
        {
            "q": "Why is pulmonary hypoplasia from prolonged PPROM considered irreversible?",
            "options": ["It responds only to surfactant therapy", "The lungs never develop adequately after birth once alveolar formation is impaired in utero", "It requires fetal surgery to correct", "It resolves spontaneously after 34 weeks"],
            "correct": 1,
            "explain": "Pulmonary hypoplasia from prolonged severe oligohydramnios is not reversible after birth. This is why very early PPROM (< 24 weeks) carries very high neonatal mortality."
        }
    ],
    # s7: General Mgmt
    "s7": [
        {
            "q": "General management of PROM includes all EXCEPT:",
            "options": ["Bed rest", "Sterile pads for inspection", "Immediate induction of labor", "Monitoring for signs of meconium staining or infection"],
            "correct": 2,
            "explain": "General management includes bed rest and sterile pads for inspection for meconium staining, foul smell (infection), or blood. Immediate induction depends on gestational age."
        },
        {
            "q": "Sterile pads in PROM management are used to inspect for:",
            "options": ["Amniotic fluid volume only", "Meconium staining, foul smell (chorioamnionitis), and blood", "pH changes in vaginal fluid", "Fetal fibronectin levels"],
            "correct": 1,
            "explain": "Sterile pads are inspected for: meconium staining (greenish-brown — fetal distress), foul smell (chorioamnionitis), and blood (abruption or vasa previa)."
        },
        {
            "q": "Greenish-brown staining on sterile pads in a PROM patient suggests:",
            "options": ["Chorioamnionitis", "Fetal distress with meconium passage", ["Placental abruption", "Normal finding"]],
            "correct": 1,
            "explain": "Greenish-brown staining indicates meconium staining, which suggests fetal distress."
        }
    ],
    # s8: <26w management
    "s8": [
        {
            "q": "The recommended management for PROM occurring before 26 weeks is:",
            "options": ["Conservative management with antibiotics", "Termination of pregnancy", "Immediate tocolysis", "Amnioinfusion"],
            "correct": 1,
            "explain": "Before 26 weeks, the risk of developing chorioamnionitis is very high, so termination of pregnancy is recommended."
        },
        {
            "q": "Why is termination recommended for PROM before 26 weeks?",
            "options": ["Fetal lungs are too mature", "Very high chorioamnionitis risk and pulmonary hypoplasia is likely", "Maternal risk of hemorrhage is too high", "Fetus is too large for vaginal delivery"],
            "correct": 1,
            "explain": "Reasons include very high chorioamnionitis risk, likely pulmonary hypoplasia from oligohydramnios, likely skeletal deformities (Potter sequence), and fetal viability below 24-26 weeks."
        },
        {
            "q": "Potter sequence refers to:",
            "options": ["A specific genetic syndrome", "Compression-related skeletal deformities from prolonged severe oligohydramnios", "A pattern of maternal hypertension", "Fetal cardiac arrhythmia pattern"],
            "correct": 1,
            "explain": "Compression-related deformities such as clubfoot from prolonged severe oligohydramnios are known as Potter sequence."
        }
    ],
    # s9: 26-34w management
    "s9": [
        {
            "q": "Conservative management of PROM at 26-34 weeks includes how many pillars?",
            "options": ["3", "4", "5", "6"],
            "correct": 2,
            "explain": "The 5 pillars of conservative management at 26-34 weeks are: hospitalization, maternal observation, fetal observation (CTG), antibiotics, and corticosteroids with tocolysis for 48 hours."
        },
        {
            "q": "The IV antibiotic regimen for PPROM at 26-34 weeks is:",
            "options": ["Ampicillin 2 g IV + Gentamicin", "Ampicillin 2 g IV + Erythromycin 250 mg/6h", "Penicillin G + Clindamycin", "Ceftriaxone + Metronidazole"],
            "correct": 1,
            "explain": "The IV phase (48 hours) is ampicillin 2 g IV + erythromycin 250 mg/6 hours, followed by oral step-down: amoxicillin 250 mg/8h + erythromycin 250 mg/6h for 5 more days."
        },
        {
            "q": "The total antibiotic course duration for PPROM at 26-34 weeks is:",
            "options": ["5 days", "7 days (2 days IV + 5 days oral)", "10 days (5 days IV + 5 days oral)", "14 days (7 days IV + 7 days oral)"],
            "correct": 1,
            "explain": "Total antibiotic course is 7 days: 2 days IV (ampicillin + erythromycin) followed by 5 days oral (amoxicillin + erythromycin)."
        },
        {
            "q": "Tocolysis at 26-34 weeks in PPROM is given for how long primarily?",
            "options": ["12 hours", "24 hours", "48 hours (to allow corticosteroids to take effect)", "72 hours"],
            "correct": 2,
            "explain": "Tocolysis is given for 48 hours to delay delivery long enough for corticosteroids to mature the fetal lungs. After 48 hours, tocolysis is usually discontinued."
        }
    ],
    # s10: >34w management
    "s10": [
        {
            "q": "For PROM occurring after 34 weeks, the recommended management is:",
            "options": ["Conservative management with antibiotics", "Delivery", "Tocolysis for 48 hours", "Amnioinfusion"],
            "correct": 1,
            "explain": "After 34 weeks, the fetus is sufficiently mature that the risk of conservative management (chorioamnionitis, cord prolapse) outweighs the risk of prematurity. Delivery is indicated."
        },
        {
            "q": "Why is the cutoff for PROM management set at 34 weeks?",
            "options": ["Fetal skull is fully ossified by 34 weeks", "By 34 weeks, most fetuses produce enough endogenous surfactant, and risk of ongoing oligohydramnios dominates", "Maternal mortality drops after 34 weeks", "Cervical ripening is always successful after 34 weeks"],
            "correct": 1,
            "explain": "By 34 weeks, most fetuses have produced enough endogenous surfactant that additional benefit from corticosteroids is minimal, and the risk of ongoing oligohydramnios + ascending infection becomes the dominant clinical concern."
        },
        {
            "q": "The 34-week cutoff in PROM management is the same as in which other obstetric condition management?",
            "options": ["Postterm pregnancy", "Preterm labor (for tocolysis contraindication)", "Placenta previa", "Preeclampsia"],
            "correct": 1,
            "explain": "The 34-week cutoff is the same as in the management of preterm labor (Chapter 31) and is anchored on lung-maturation data."
        }
    ],
    # s11: Chorioamnionitis
    "s11": [
        {
            "q": "Chorioamnionitis is defined as:",
            "options": ["Infection of the placental parenchyma", "Inflammation of fetal membranes (intrauterine infection)", "Infection of the umbilical cord", "Infection of the endometrium"],
            "correct": 1,
            "explain": "Chorioamnionitis is defined as inflammation of fetal membranes, which means intrauterine infection."
        },
        {
            "q": "The diagnosis of chorioamnionitis requires fever > 38°C plus at least one of how many signs/investigations?",
            "options": ["3 signs", "5 signs", "7 signs", "9 signs"],
            "correct": 2,
            "explain": "The diagnosis is made when fever > 38°C is present PLUS at least one of the 7 signs: maternal tachycardia, fetal tachycardia, uterine tenderness, foul smelling amniotic fluid, maternal leukocytosis > 16,000/cc, raised CRP > 2.5, or positive high vaginal swab."
        },
        {
            "q": "Which of the following is a diagnostic sign of chorioamnionitis?",
            "options": ["Maternal bradycardia", "Maternal leukocytosis > 16,000/cc", "Decreased C-reactive protein", "Oliguria"],
            "correct": 1,
            "explain": "Maternal leukocytosis > 16,000/cc is one of the 7 diagnostic signs of chorioamnionitis (along with fever > 38°C)."
        }
    ],
    # s12: Chorio Mgmt
    "s12": [
        {
            "q": "The definitive treatment for chorioamnionitis is:",
            "options": ["Broad-spectrum antibiotics alone", "Delivery and evacuation of uterine contents", "Antipyretics and observation", "Uterine lavage"],
            "correct": 1,
            "explain": "The definitive treatment is delivery and evacuation of the uterine contents. Antibiotics alone are not curative while the infected focus (amniotic cavity) remains in place."
        },
        {
            "q": "The antibiotic regimen for chorioamnionitis until delivery is:",
            "options": ["Ceftriaxone + Metronidazole", "Ampicillin 2 g IV q6h + Gentamicin (2 mg/kg load, then 1.5 mg/kg IV q8h)", "Penicillin + Clindamycin", "Vancomycin + Gentamicin"],
            "correct": 1,
            "explain": "The regimen is ampicillin 2 g IV every 6 hours + gentamicin 2 mg/kg IV load then 1.5 mg/kg IV every 8 hours, continued until delivery."
        },
        {
            "q": "When is clindamycin or metronidazole added to the chorioamnionitis antibiotic regimen?",
            "options": ["Always, regardless of delivery mode", "Only if cesarean delivery is performed (for anaerobic coverage)", "Only if vaginal delivery is performed", "Only if the patient is penicillin-allergic"],
            "correct": 1,
            "explain": "If cesarean delivery is performed, clindamycin or metronidazole is added for anaerobic coverage because surgical incision exposes deep pelvic tissues to anaerobic flora from the vagina."
        }
    ]
}

# =============================================================================
# FILE 3: 41_Postterm_Pregnancy.html
# =============================================================================
mcq_41 = {
    # s2: Definition
    "s2": [
        {
            "q": "Postterm pregnancy is defined as a pregnancy continuing beyond:",
            "options": ["40 weeks", "41 weeks", "42 weeks", "43 weeks"],
            "correct": 2,
            "explain": "Postterm pregnancy is a pregnancy continuing beyond 42 weeks. Pregnancy between 41 to 42 weeks is called prolonged pregnancy."
        },
        {
            "q": "A pregnancy between 41 to 42 weeks is called:",
            "options": ["Postterm pregnancy", "Prolonged pregnancy", "Term pregnancy", "Preterm pregnancy"],
            "correct": 1,
            "explain": "Pregnancy between 41 to 42 weeks is called prolonged pregnancy, while beyond 42 weeks is postterm pregnancy."
        },
        {
            "q": "What is the key difference between prolonged and postterm pregnancy?",
            "options": ["There is no difference — the terms are interchangeable", "Prolonged is 41-42 weeks (monitored); postterm is >42 weeks (requires intervention)", "Prolonged requires induction; postterm is observed expectantly", "Prolonged has higher fetal risk than postterm"],
            "correct": 1,
            "explain": "Prolonged pregnancy (41-42 weeks) is monitored; postterm pregnancy (>42 weeks) requires intervention. Do not confuse the two — management differs."
        }
    ],
    # s3: Causes
    "s3": [
        {
            "q": "The most common cause of postterm pregnancy is:",
            "options": ["Fetal anencephaly", "Maternal diabetes", "Wrong date (incorrect gestational age calculation)", "Adrenal hypoplasia"],
            "correct": 2,
            "explain": "The most common cause of postterm pregnancy is wrong date, so a careful review of menstrual history is important in all such cases."
        },
        {
            "q": "Which fetal condition can cause postterm pregnancy?",
            "options": ["Fetal macrosomia", "Anencephaly and adrenal hypoplasia", "Fetal hydrops", "Polyhydramnios"],
            "correct": 1,
            "explain": "Fetal factors causing postterm pregnancy include anencephaly and adrenal hypoplasia (diminished fetal cortisol response). Anencephaly disrupts the fetal hypothalamic-pituitary-adrenal axis — without fetal cortisol, labor is not initiated."
        },
        {
            "q": "Maternal factors associated with postterm pregnancy include all EXCEPT:",
            "options": ["Primipara", "History of previous prolonged pregnancy", "Sedentary life", "Multiple gestation"],
            "correct": 3,
            "explain": "Maternal factors include primipara, history of previous prolonged pregnancy, and sedentary life. Multiple gestation is associated with preterm labor, not postterm pregnancy."
        }
    ],
    # s4: Antenatal Dx
    "s4": [
        {
            "q": "Which of the following is NOT an antenatal ultrasound finding in postterm pregnancy?",
            "options": ["Biparietal diameter more than 9.6 cm", "Oligohydramnios", "Increased placental calcification", "Polyhydramnios"],
            "correct": 3,
            "explain": "Antenatal ultrasound findings in postterm pregnancy include BPD > 9.6 cm, increased fetal weight, oligohydramnios, increased placental calcification, and Doppler evidence of placental insufficiency."
        },
        {
            "q": "Increased placental calcification on ultrasound in postterm pregnancy reflects:",
            "options": ["Normal aging of the placenta", "Placental aging and insufficiency", "Placental abruption", "Placenta previa"],
            "correct": 1,
            "explain": "Increased placental calcification on US is a hallmark of placental aging — it reflects the pathophysiology of postterm pregnancy where the placenta becomes insufficient."
        },
        {
            "q": "Oligohydramnios in a postterm pregnancy poses risk for all EXCEPT:",
            "options": ["Cord compression", "Fetal hypoxia", "Fetal macrosomia", "Meconium aspiration"],
            "correct": 2,
            "explain": "Oligohydramnios + placental insufficiency in a postterm pregnancy = high risk for cord compression, fetal hypoxia, and meconium aspiration. Fetal macrosomia is a separate complication of postterm pregnancy."
        }
    ],
    # s5: Postnatal Dx
    "s5": [
        {
            "q": "A postnatal sign of a postterm baby is:",
            "options": ["Birth weight more than 4.5 kg", "Birth weight less than 2.5 kg", "Head circumference less than 33 cm", "Skin that is thin and transparent"],
            "correct": 0,
            "explain": "Postnatal signs of a postterm baby include weight more than 4.5 kg, length more than 54 cm, well ossified skull with smaller fontanelles, and finger nails projecting beyond finger tips."
        },
        {
            "q": "Which mnemonic helps recall the postnatal signs of a postterm baby?",
            "options": ["L-W-S-F (Length, Weight, Skull, Fingernails)", "H-A-I-R (Head, Arms, Inches, Reflexes)", "B-A-B-Y (Breathing, Activity, Body, Yell)", "A-P-G-A-R (Appearance, Pulse, Grimace, Activity, Respiration)"],
            "correct": 0,
            "explain": "L-W-S-F: Length > 54 cm, Weight > 4.5 kg, Skull well ossified/small fontanelles, Fingernails beyond tips."
        },
        {
            "q": "A postterm baby's skull is characterized by:",
            "options": ["Wide open fontanelles", "Well ossified with smaller fontanelles", "Soft and compressible bones", "Overlapping sutures (Spalding sign)"],
            "correct": 1,
            "explain": "The skull is well ossified with smaller fontanelles in a postterm baby. (Spalding sign — overlapping skull bones — is seen in IUFD, not postterm.)"
        }
    ],
    # s6: Complications
    "s6": [
        {
            "q": "The cascade of complications in postterm pregnancy begins with:",
            "options": ["Fetal macrosomia", "Aging of placenta leading to placental insufficiency", "Oligohydramnios", "Postpartum hemorrhage"],
            "correct": 1,
            "explain": "The cascade: placental aging → placental insufficiency → fetal hypoxia → acidosis → stillbirth. Each day past 42 weeks increases this risk."
        },
        {
            "q": "Fetal macrosomia in postterm pregnancy increases the risk of:",
            "options": ["Preterm labor", "Shoulder dystocia and birth trauma", ["Chorioamnionitis", "Cord prolapse"]],
            "correct": 1,
            "explain": "Fetal macrosomia leads to shoulder dystocia, increases the chances of birth trauma (intracranial hemorrhage) and increases the chances of operative delivery."
        },
        {
            "q": "Complications of postterm pregnancy include all EXCEPT:",
            "options": ["Placental insufficiency and stillbirth", "Oligohydramnios and cord compression", "Pulmonary hypoplasia", "Postpartum hemorrhage and infection"],
            "correct": 2,
            "explain": "Pulmonary hypoplasia is a complication of preterm PROM, not postterm pregnancy. Postterm complications include placental insufficiency, fetal hypoxia/acidosis/stillbirth, oligohydramnios, cord compression, meconium aspiration, fetal macrosomia, shoulder dystocia, operative delivery, postpartum hemorrhage, and infection."
        }
    ],
    # s7: Management
    "s7": [
        {
            "q": "The management of postterm pregnancy is:",
            "options": ["Expectant observation until spontaneous labor", "Termination of pregnancy (induction of labor or cesarean)", "Administration of corticosteroids", "Tocolysis to prevent labor"],
            "correct": 1,
            "explain": "The source states management of postterm pregnancy is termination of pregnancy — induction of labor or cesarean section depending on cervical readiness and fetal status."
        },
        {
            "q": "The decision between induction of labor and cesarean section in postterm pregnancy depends on:",
            "options": ["Maternal preference alone", "Gestational age only", "Cervical readiness and fetal status", "Fetal gender"],
            "correct": 2,
            "explain": "Management depends on cervical readiness and fetal status, and the type of termination (induction of labor or cesarean section) is individualized."
        },
        {
            "q": "Why must dating be confirmed before diagnosing postterm pregnancy?",
            "options": ["Because management differs significantly between true postterm and wrong dates", "Because ultrasound is unreliable after 40 weeks", "Because the definition changes by country", "Because postterm cannot be diagnosed without a first-trimester scan"],
            "correct": 0,
            "explain": "The most common cause of postterm pregnancy is wrong date, so careful review of menstrual history and dating confirmation is essential before making the diagnosis."
        }
    ]
}

# =============================================================================
# FILE 4: 43_Intrauterine_Fetal_Death.html
# =============================================================================
mcq_43 = {
    # s2: Definition
    "s2": [
        {
            "q": "Intrauterine Fetal Death (IUFD) is defined as fetal death in-utero after:",
            "options": ["16 weeks of pregnancy or fetus weight > 350 gm", "20 weeks of pregnancy or fetus weight > 500 gm", "24 weeks of pregnancy or fetus weight > 600 gm", "28 weeks of pregnancy or fetus weight > 1000 gm"],
            "correct": 1,
            "explain": "IUFD is death of the fetus in-utero after 20 weeks of pregnancy or if the fetus weight is > 500 gm."
        },
        {
            "q": "The weight threshold defining IUFD is:",
            "options": ["> 350 gm", "> 500 gm", "> 750 gm", "> 1000 gm"],
            "correct": 1,
            "explain": "IUFD is defined when the fetus weight is > 500 gm (in addition to gestational age > 20 weeks)."
        },
        {
            "q": "Fetal death occurring before 20 weeks is classified as:",
            "options": ["IUFD", "Miscarriage or spontaneous abortion", "Stillbirth", "Neonatal death"],
            "correct": 1,
            "explain": "Fetal death before 20 weeks is classified as miscarriage or spontaneous abortion. IUFD specifically refers to death after 20 weeks or > 500 gm."
        }
    ],
    # s3: Causes
    "s3": [
        {
            "q": "Which of the following is a maternal cause of IUFD?",
            "options": ["Cord accident", "IUGR", "Antiphospholipid syndrome", "Congenital abnormality"],
            "correct": 2,
            "explain": "Maternal causes include diabetes, SLE, antiphospholipid syndrome, infection, hypertension, preeclampsia, eclampsia, uterine rupture, maternal trauma/death, and thrombophilias."
        },
        {
            "q": "Fetal causes of IUFD include all EXCEPT:",
            "options": ["Intrauterine growth restriction", "Congenital abnormality", "Cord accident", "Hydrops"],
            "correct": 2,
            "explain": "Fetal causes include IUGR, congenital abnormality, genetic abnormality, infection (Parvovirus B19, CMV, Listeria), and hydrops. Cord accident is a placental cause."
        },
        {
            "q": "Which infection is associated with IUFD?",
            "options": ["Group B Streptococcus", "Parvovirus B19", "Candida albicans", "Staphylococcus aureus"],
            "correct": 1,
            "explain": "Fetal infections associated with IUFD include Parvovirus B19, CMV, and Listeria."
        },
        {
            "q": "Placental causes of IUFD include:",
            "options": ["Diabetes and hypertension", "Cord accident, abruption, vasa previa, and placental insufficiency", "SLE and antiphospholipid syndrome", "Uterine rupture and maternal trauma"],
            "correct": 1,
            "explain": "Placental causes include cord accident, abruption, PROM, vasa previa, feto-maternal hemorrhage, and placental insufficiency."
        }
    ],
    # s4: Diagnosis
    "s4": [
        {
            "q": "Which of the following is a symptom of IUFD?",
            "options": ["Increased fetal movements", "Cessation of fetal movements", "Polyhydramnios", "Maternal weight gain"],
            "correct": 1,
            "explain": "Symptoms of IUFD include history of the cause, gradual disappearance of pregnancy symptoms, breast milk secretion, failure of abdominal enlargement, and cessation of fetal movements."
        },
        {
            "q": "A key sign of IUFD on examination is:",
            "options": ["Uterus larger than expected for dates", "Uterus smaller than the period of amenorrhea", "Easily palpable fetal parts", "Fetal heart rate > 160 bpm"],
            "correct": 1,
            "explain": "Signs of IUFD include uterus smaller than the period of amenorrhea, difficult palpation of fetal parts (due to absent muscle tone), and inaudible FHS by Doppler."
        },
        {
            "q": "In IUFD, fetal parts are difficult to palpate because of:",
            "options": ["Polyhydramnios", "Absent fetal muscle tone", "Maternal obesity", "Uterine hypertonicity"],
            "correct": 1,
            "explain": "Difficult palpation of fetal parts is due to absent muscle tone after fetal death."
        }
    ],
    # s5: Investigations
    "s5": [
        {
            "q": "Spalding sign on X-ray in IUFD refers to:",
            "options": ["Gas in fetal large vessels", "Hyperflexion of fetal spine", "Overlapping of fetal skull bones due to shrinkage of cerebrum", "Absence of fetal subcutaneous tissue"],
            "correct": 2,
            "explain": "Spalding sign is overlapping of fetal skull bones due to shrinkage of cerebrum after fetal death."
        },
        {
            "q": "Robert sign on X-ray in IUFD refers to:",
            "options": ["Overlapping of fetal skull bones", "Presence of gas in fetal large vessels", "Hyperflexion of fetal spine", "Collapse of fetal thoracic cage"],
            "correct": 1,
            "explain": "Robert sign is the presence of gas in fetal large vessels."
        },
        {
            "q": "Ball sign on X-ray in IUFD refers to:",
            "options": ["Overlapping of fetal skull bones", "Gas in fetal large vessels", "Hyperflexion of fetal spine", "Ballooning of fetal abdomen"],
            "correct": 2,
            "explain": "Ball sign is hyperflexion of fetal spine. The mnemonic SRB helps recall: Spalding (skull overlap), Robert (gas), Ball (spine)."
        }
    ],
    # s6: Complications
    "s6": [
        {
            "q": "After how many weeks of fetal death does the risk of maternal DIC and hypofibrinogenemia rise sharply?",
            "options": ["1 week", "2 weeks", "3 weeks", "4 weeks"],
            "correct": 2,
            "explain": "Once fetal death has persisted for > 3 weeks, the risk of maternal DIC and hypofibrinogenemia rises sharply."
        },
        {
            "q": "Complications of IUFD include all EXCEPT:",
            "options": ["Intrauterine infection", "DIC and hypofibrinogenemia", "Pulmonary hypoplasia", "Maternal coagulopathy"],
            "correct": 2,
            "explain": "Complications of IUFD include intrauterine infection and DIC/hypofibrinogenemia (after 3 weeks). Pulmonary hypoplasia is a complication of PROM."
        },
        {
            "q": "Why is DIC a concern in prolonged IUFD?",
            "options": ["The dead fetus releases thromboplastin into maternal circulation", "The placenta stops producing clotting factors", "Maternal liver failure occurs", "Fetal bone marrow releases thrombogenic substances"],
            "correct": 0,
            "explain": "DIC occurs because the retained dead fetus releases thromboplastin into the maternal circulation, triggering disseminated intravascular coagulation. This is why delivery is usually offered."
        }
    ],
    # s7: Management
    "s7": [
        {
            "q": "The first principle in management of IUFD is:",
            "options": ["Expectant management for 4 weeks", "Termination of pregnancy should be offered after diagnosis", "Immediate cesarean section", "Administration of corticosteroids"],
            "correct": 1,
            "explain": "The first principle is that termination of pregnancy should be offered after diagnosis."
        },
        {
            "q": "Induction of labor for IUFD is accomplished with:",
            "options": ["Tocolysis followed by observation", "Preinduction cervical ripening followed by IV oxytocin", "Immediate cesarean section", "Manual vacuum extraction"],
            "correct": 1,
            "explain": "Induction of labor can be accomplished with preinduction cervical ripening followed by intravenous oxytocin."
        },
        {
            "q": "If induction of labor fails in IUFD management, what is the next step?",
            "options": ["Repeat induction after 24 hours", "Cesarean section", "Continue expectant management", "Administer prostaglandin analogues"],
            "correct": 1,
            "explain": "If induction fails, cesarean section is done."
        }
    ]
}

# =============================================================================
# Run all injections
# =============================================================================

files = [
    ("PROM_preterm_post_term_pregnancy/31_Preterm_Labor.html", mcq_31),
    ("PROM_preterm_post_term_pregnancy/32_Premature_Rupture_of_Membranes_PROM.html", mcq_32),
    ("PROM_preterm_post_term_pregnancy/41_Postterm_Pregnancy.html", mcq_41),
    ("Assessment_of_fetal_wellbeing/43_Intrauterine_Fetal_Death.html", mcq_43),
]

for rel_path, mcq_data in files:
    input_path  = os.path.join(BASE, rel_path)
    output_path = os.path.join(ENH, rel_path)
    
    # Ensure output dir exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Processing: {rel_path}")
    try:
        process_file(input_path, output_path, mcq_data)
        # Count total MCQs
        total = sum(len(v) for v in mcq_data.values())
        sections = sum(1 for v in mcq_data.values() if v)
        print(f"  → {total} MCQs across {sections} sections injected")
    except Exception as e:
        print(f"  → ERROR: {e}")

print("\nDone! All 4 files processed.")
