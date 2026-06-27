#!/usr/bin/env python3
"""Inject MCQs into the 4 Week 2 obstetrics files."""

import sys, os

sys.path.insert(0, '/media/mohamed/projects3/projects/obstaric/obs app')
from inject_mcqs import process_file

BASE = '/media/mohamed/projects3/projects/obstaric/obs app/extracted/assets/second task/obstetric/Week2'
ENH  = '/media/mohamed/projects3/projects/obstaric/obs app/enhanced-assets/second task/obstetric/Week2'
SUBDIR = 'Polyhydramnios_IUGR_shoulder_dystocia'

# ========================================================================
# FILE 1: 18_Amniotic_Fluid_Abnormalities.html
# ========================================================================
af_data = {
    "s2": [
        {
            "q": "Which of the following is the main source of amniotic fluid during the first half of pregnancy?",
            "options": ["Fetal urination", "Maternal circulation", "Fetal swallowing", "Amniotic epithelium"],
            "correct": 1,
            "explain": "In the first half of pregnancy, amniotic fluid is produced from maternal circulation. In the second half, fetal urination becomes the main source."
        },
        {
            "q": "What is the primary route of amniotic fluid resorption during the second half of pregnancy?",
            "options": ["Maternal absorption", "Fetal swallowing", "Placental transfer", "Transmembrane diffusion"],
            "correct": 1,
            "explain": "Fetal swallowing is the main route of amniotic fluid clearance during the second half of pregnancy."
        },
        {
            "q": "Which of the following is NOT a function of amniotic fluid?",
            "options": ["Protection from injury", "Temperature regulation", "Nutrient supply to the fetus", "Allowing fetal movement"],
            "correct": 2,
            "explain": "Amniotic fluid surrounds and protects the fetus, regulates temperature, and allows fetal movement. Nutrient supply is through the placenta."
        }
    ],
    "s3": [
        {
            "q": "Polyhydramnios is defined as an amniotic fluid volume (AFV) greater than:",
            "options": ["1,000 mL", "1,500 mL", "2,000 mL", "2,500 mL"],
            "correct": 2,
            "explain": "Polyhydramnios is defined as AFV > 2,000 mL. Oligohydramnios is defined as AFV < 500 mL."
        },
        {
            "q": "Which is the most common cause of both polyhydramnios and oligohydramnios?",
            "options": ["Diabetes mellitus", "Fetal malformations", "Idiopathic", "Premature rupture of membranes"],
            "correct": 2,
            "explain": "Idiopathic (unknown cause) is the most common etiology for both polyhydramnios and oligohydramnios."
        },
        {
            "q": "A patient has fundal height more than expected, difficult palpation and difficult FHS auscultation. Which condition is most likely?",
            "options": ["Oligohydramnios", "Polyhydramnios", "Normal pregnancy", "Placental insufficiency"],
            "correct": 1,
            "explain": "Classic polyhydramnios: uterus larger than dates, difficult palpation and auscultation of fetal parts and heart sounds."
        },
        {
            "q": "Which fetal malformation is associated with polyhydramnios?",
            "options": ["Renal agenesis", "Esophageal atresia", "Post-term pregnancy", "Placental insufficiency"],
            "correct": 1,
            "explain": "Fetal esophageal and duodenal atresia prevent fetal swallowing, leading to polyhydramnios. Renal agenesis causes oligohydramnios."
        }
    ],
    "s4": [
        {
            "q": "Using Single Deepest Pocket (SDP), oligohydramnios is diagnosed when SDP is:",
            "options": ["< 2 cm", "< 5 cm", "< 8 cm", "< 10 cm"],
            "correct": 0,
            "explain": "SDP < 2 cm = oligohydramnios. SDP 2-8 cm = normal. SDP > 8 cm = polyhydramnios."
        },
        {
            "q": "Using the Amniotic Fluid Index (AFI), polyhydramnios is defined as:",
            "options": ["AFI > 8 cm", "AFI > 20 cm", "AFI > 25 cm", "AFI > 30 cm"],
            "correct": 2,
            "explain": "AFI > 25 cm = polyhydramnios. AFI 10-20 cm = normal. AFI < 5 cm = oligohydramnios."
        },
        {
            "q": "The Amniotic Fluid Index (AFI) uses the:",
            "options": ["Single vertical pocket method", "4-quadrant method summing deepest pockets", "Multiplication of SDP by 4", "Total AF volume estimation"],
            "correct": 1,
            "explain": "AFI uses the 4-quadrant method: the deepest vertical amniotic pocket in each quadrant is measured and summed."
        }
    ],
    "s5": [
        {
            "q": "Which complication is specific to oligohydramnios and a major cause of neonatal mortality when prolonged?",
            "options": ["Umbilical cord prolapse", "Postpartum hemorrhage", "Fetal pulmonary hypoplasia", "Maternal dyspnea"],
            "correct": 2,
            "explain": "Pulmonary hypoplasia is a major complication of prolonged oligohydramnios as fetal lung development is impaired."
        },
        {
            "q": "Which complication is shared by both polyhydramnios and oligohydramnios?",
            "options": ["Umbilical cord prolapse", "Pulmonary hypoplasia", "Postpartum hemorrhage", "Preterm labor"],
            "correct": 3,
            "explain": "Both polyhydramnios and oligohydramnios share preterm labor and abnormal fetal presentation as common complications."
        },
        {
            "q": "Umbilical cord prolapse is more commonly associated with:",
            "options": ["Oligohydramnios", "Polyhydramnios", "Both equally", "Neither"],
            "correct": 1,
            "explain": "Umbilical cord prolapse is a complication of polyhydramnios, especially after sudden decompression following ROM."
        }
    ],
    "s6": [
        {
            "q": "Which is a management option for polyhydramnios?",
            "options": ["Amnio-infusion", "Amnio-reduction", "Maternal rehydration", "Termination"],
            "correct": 1,
            "explain": "Amnio-reduction (drainage of excess fluid) is used for polyhydramnios. Amnio-infusion is for oligohydramnios."
        },
        {
            "q": "A post-term pregnancy with oligohydramnios should be managed by:",
            "options": ["Watchful waiting", "Maternal rehydration", "Amnio-infusion", "Delivery"],
            "correct": 3,
            "explain": "When the pregnancy is post-term and AF is low, delivery rather than watchful waiting is indicated."
        },
        {
            "q": "Which medication can be used in managing polyhydramnios?",
            "options": ["Oxytocin", "Prostaglandin synthetase inhibitor", "Misoprostol", "Calcium gluconate"],
            "correct": 1,
            "explain": "A prostaglandin synthetase inhibitor (e.g., indomethacin) can reduce amniotic fluid production in polyhydramnios."
        }
    ],
}

# ========================================================================
# FILE 2: 29_Shoulder_Dystocia.html
# ========================================================================
sd_data = {
    "s2": [
        {
            "q": "What is the reported incidence of shoulder dystocia?",
            "options": ["0.1-0.2%", "0.2-0.3%", "1-2%", "2-3%"],
            "correct": 1,
            "explain": "Shoulder dystocia occurs in 0.2-0.3% of deliveries."
        },
        {
            "q": "Which two adjectives best describe shoulder dystocia?",
            "options": ["Common and preventable", "Predictable and treatable", "Unpredictable and unpreventable", "Rare and self-limiting"],
            "correct": 2,
            "explain": "Shoulder dystocia is unpredictable (cannot be reliably forecast) and unpreventable (no prophylactic intervention)."
        },
        {
            "q": "Shoulder dystocia is defined as:",
            "options": ["Arrested delivery of fetal head", "Arrested delivery of fetal shoulder after head delivery requiring additional maneuvers", "Failure of fetal rotation in pelvic outlet", "Prolonged second stage > 3 hours"],
            "correct": 1,
            "explain": "It is specifically the arrested delivery of the fetal shoulder after delivery of the fetal head, requiring additional maneuvers."
        }
    ],
    "s5": [
        {
            "q": "Which is an antepartum risk factor for shoulder dystocia?",
            "options": ["Prolonged first stage", "Secondary arrest", "Previous shoulder dystocia", "Oxytocin augmentation"],
            "correct": 2,
            "explain": "Previous shoulder dystocia (recurrence ~10%), macrosomia, DM, BMI > 30, and induction of labor are the 5 antepartum risk factors."
        },
        {
            "q": "Which is an intrapartum risk factor for shoulder dystocia?",
            "options": ["Macrosomia", "Diabetes mellitus", "Maternal obesity", "Prolonged second stage"],
            "correct": 3,
            "explain": "Prolonged 1st/2nd stage, secondary arrest, oxytocin augmentation, and assisted vaginal delivery are the 5 intrapartum risk factors."
        },
        {
            "q": "The single most common risk factor for shoulder dystocia is:",
            "options": ["Previous shoulder dystocia", "Macrosomia", "Diabetes mellitus", "Assisted delivery"],
            "correct": 1,
            "explain": "Macrosomia (BW > 4,000 g or > 4,500 g in diabetic mothers) is the single most common risk factor."
        }
    ],
    "s6": [
        {
            "q": "Which maneuver is the most effective single intervention in shoulder dystocia?",
            "options": ["Delivery of posterior arm", "Episiotomy", "McRobert's maneuver", "Suprapubic pressure"],
            "correct": 2,
            "explain": "McRobert's maneuver (hyperflexion of maternal hips) is the most effective intervention, resolving ~90% when combined with suprapubic pressure."
        },
        {
            "q": "McRobert's + suprapubic pressure resolves approximately what % of cases?",
            "options": ["50%", "70%", "90%", "99%"],
            "correct": 2,
            "explain": "The combination resolves approximately 90% of shoulder dystocia cases."
        },
        {
            "q": "What is the purpose of episiotomy in shoulder dystocia management?",
            "options": ["To resolve the impaction", "To facilitate internal maneuvers by enlarging the vaginal opening", "To reduce fetal head circumference", "To prevent perineal tearing"],
            "correct": 1,
            "explain": "Episiotomy alone does not resolve dystocia — it enlarges the opening to allow room for internal manipulation."
        },
        {
            "q": "Which complication is most associated with delivery of the posterior arm?",
            "options": ["Uterine rupture", "Fracture of humerus or clavicle", "Maternal hemorrhage", "Erb's palsy"],
            "correct": 1,
            "explain": "Delivery of the posterior arm carries a higher risk of fracturing the humerus or clavicle, which usually heal well."
        }
    ],
    "s8": [
        {
            "q": "Which fetal complication involves injury to C5-C6 nerve roots causing 'waiter's tip' deformity?",
            "options": ["Brachial plexus injury", "Erb's palsy", "Klumpke's palsy", "Hypoxic brain injury"],
            "correct": 1,
            "explain": "Erb's palsy affects C5-C6 roots, causing 'waiter's tip' deformity (arm adducted, internally rotated, forearm pronated)."
        },
        {
            "q": "Which is a maternal complication of shoulder dystocia?",
            "options": ["Brachial plexus injury", "Erb's palsy", "Post-partum hemorrhage", "Bone fractures"],
            "correct": 2,
            "explain": "PPH (from uterine atony or perineal trauma) is one of 4 maternal complications: PPH, lacerations/tears, uterine rupture, psychological stress."
        },
        {
            "q": "How many fetal vs maternal complications are listed for shoulder dystocia?",
            "options": ["4 fetal, 4 maternal", "5 fetal, 4 maternal", "3 fetal, 5 maternal", "6 fetal, 3 maternal"],
            "correct": 1,
            "explain": "5 fetal (brachial plexus injury, Erb's palsy, fractures, hypoxic brain injury, death) and 4 maternal."
        }
    ],
}

# ========================================================================
# FILE 3: 40_Intrauterine_Growth_Restriction.html
# ========================================================================
iugr_data = {
    "s2": [
        {
            "q": "IUGR is defined as fetal AC or EFW less than which centile for gestational age?",
            "options": ["5th centile", "10th centile", "15th centile", "3rd centile"],
            "correct": 1,
            "explain": "IUGR is defined as fetal abdominal circumference or estimated fetal weight less than the 10th centile for gestational age."
        },
        {
            "q": "IUGR fetuses have what increase in perinatal morbidity and mortality?",
            "options": ["2- to 6-fold", "1.5- to 3-fold", "5- to 10-fold", "10- to 15-fold"],
            "correct": 0,
            "explain": "Fetuses with IUGR have a 2- to 6-fold increase in perinatal morbidity and mortality."
        },
        {
            "q": "What distinguishes IUGR from constitutionally small SGA?",
            "options": ["IUGR implies pathological growth with abnormal Doppler findings", "IUGR only affects head circumference", "SGA always has abnormal Doppler studies", "The terms are interchangeable"],
            "correct": 0,
            "explain": "A constitutionally small fetus has normal growth velocity and Doppler studies; IUGR implies pathological restriction with abnormal Doppler findings."
        }
    ],
    "s3": [
        {
            "q": "Asymmetric IUGR is caused by which type of factors?",
            "options": ["Intrinsic factors like genetic abnormalities", "Extrinsic factors like placental insufficiency", "Maternal infections", "Fetal aneuploidy"],
            "correct": 1,
            "explain": "Asymmetric IUGR is caused by extrinsic factors such as placental insufficiency. Oxygen is shunted to vital organs (brain-sparing)."
        },
        {
            "q": "Which IUGR type shows 'brain-sparing' with a high HC-to-AC ratio?",
            "options": ["Symmetric IUGR", "Asymmetric IUGR", "Both equally", "Neither"],
            "correct": 1,
            "explain": "Asymmetric IUGR shows brain-sparing — preferential shunting to brain and heart produces a high head-to-abdomen ratio."
        },
        {
            "q": "Symmetric IUGR typically affects the fetus:",
            "options": ["Later in gestation", "Early in gestation", "Only in the third trimester", "After 36 weeks"],
            "correct": 1,
            "explain": "Symmetric IUGR affects the fetus early in gestation; asymmetric IUGR tends to affect the fetus later."
        },
        {
            "q": "Which is a cause of symmetric IUGR?",
            "options": ["Placental insufficiency", "Genetic abnormalities or intrauterine infections", "Maternal diabetes", "Multiple gestation"],
            "correct": 1,
            "explain": "Symmetric IUGR is caused by intrinsic factors like genetic abnormalities and intrauterine infections (TORCH)."
        }
    ],
    "s5": [
        {
            "q": "Which maternal medical condition is associated with IUGR?",
            "options": ["Gestational diabetes", "Chronic hypertension", "Mild iron deficiency", "Hypothyroidism"],
            "correct": 1,
            "explain": "Maternal conditions include pre-existing DM, chronic/GH hypertension, pre-eclampsia, SLE, APS, sickle cell disease, and severe anemia."
        },
        {
            "q": "Which teratogenic drug is associated with IUGR?",
            "options": ["Penicillin", "Acetaminophen", "ACE-inhibitors", "Omeprazole"],
            "correct": 2,
            "explain": "ACE-inhibitors, warfarin, carbamazepine, phenytoin, cyclophosphamide, and valproic acid are associated with IUGR."
        },
        {
            "q": "Which substance use is NOT listed as an IUGR maternal risk factor?",
            "options": ["Tobacco", "Alcohol", "Cocaine", "Caffeine"],
            "correct": 3,
            "explain": "Tobacco, alcohol, cocaine, and narcotics are listed. Caffeine is not mentioned as an IUGR risk factor."
        }
    ],
    "s6": [
        {
            "q": "Which is a placental risk factor for IUGR?",
            "options": ["Maternal diabetes", "Placental insufficiency", "Toxoplasmosis", "Fetal aneuploidy"],
            "correct": 1,
            "explain": "Placental risk factors include placental insufficiency, placenta previa, placental abruption, and multiple gestation."
        },
        {
            "q": "TORCH infections are a major cause of which type of IUGR?",
            "options": ["Asymmetric IUGR", "Symmetric IUGR", "Both equally", "Neither"],
            "correct": 1,
            "explain": "TORCH infections (Toxoplasmosis, Other, Rubella, CMV, Herpes) are a major fetal cause of symmetric IUGR."
        },
        {
            "q": "Which is a fetal risk factor for IUGR?",
            "options": ["Placenta previa", "Maternal obesity", "Cyanotic congenital heart disease", "Multiple gestation"],
            "correct": 2,
            "explain": "Fetal risk factors include congenital infections (TORCH), genetic abnormalities (aneuploidy), and congenital anomalies like cyanotic CHD."
        }
    ],
    "s7": [
        {
            "q": "What is the classic clinical sign of IUGR on abdominal examination?",
            "options": ["Fundal height > expected", "SFH at least 3 cm less than gestational age in weeks", "Polyhydramnios", "Increased fetal movements"],
            "correct": 1,
            "explain": "SFH lag of >= 3 cm below gestational age in weeks is the classic clinical sign of IUGR."
        },
        {
            "q": "Reduced fetal movements in a small-for-dates fetus should raise suspicion of:",
            "options": ["Normal variation", "IUGR with fetal compromise", "Multiple pregnancy", "Polyhydramnios"],
            "correct": 1,
            "explain": "Reduced or absent fetal movements in a small-for-dates fetus is an obstetric emergency suggesting IUGR with fetal compromise."
        },
        {
            "q": "What is the limitation of SFH measurement for IUGR diagnosis?",
            "options": ["It is too expensive", "Poor sensitivity; serial US is more reliable", "Can only be done after 36 weeks", "Requires fasting"],
            "correct": 1,
            "explain": "SFH has poor sensitivity; serial ultrasound measurements are more reliable for diagnosing IUGR."
        }
    ],
    "s8": [
        {
            "q": "Which is NOT part of the IUGR assessment triad?",
            "options": ["Umbilical artery Doppler", "Amniotic fluid volume", "Amniocentesis", "Biophysical profile"],
            "correct": 2,
            "explain": "IUGR triad: U-A-B (Umbilical Doppler, Amniotic fluid/oligohydramnios, BPP <= 4 = deliver)."
        },
        {
            "q": "A BPP score of what value indicates need for delivery in IUGR?",
            "options": ["<= 2", "<= 4", "<= 6", "<= 8"],
            "correct": 1,
            "explain": "A BPP score of <= 4 indicates the need for delivery in IUGR."
        },
        {
            "q": "Which Doppler finding is characteristic of IUGR?",
            "options": ["Increased diastolic flow", "Reduced or reversed diastolic flow in umbilical artery", "Normal flow velocity", "Increased peak systolic velocity"],
            "correct": 1,
            "explain": "Umbilical artery Doppler in IUGR shows reduced or reversed diastolic flow."
        }
    ],
    "s9": [
        {
            "q": "According to the Barker hypothesis, IUGR programs for which adult diseases?",
            "options": ["Alzheimer's and dementia", "Diabetes, obesity, CAD, and hypertension", "Asthma and COPD", "Osteoporosis and arthritis"],
            "correct": 1,
            "explain": "The Barker/thrifty phenotype hypothesis: fetal undernutrition leads to permanent metabolic adaptations increasing adult chronic disease risk."
        },
        {
            "q": "Which is a perinatal complication of IUGR?",
            "options": ["Macrosomia", "Polyhydramnios", "Necrotising enterocolitis", "Post-term delivery"],
            "correct": 2,
            "explain": "NEC is a perinatal IUGR complication along with preterm labor, stillbirth, perinatal asphyxia, cognitive delay, and neurological disabilities."
        },
        {
            "q": "All are IUGR complications EXCEPT:",
            "options": ["Stillbirth", "Preterm labor", "Fetal macrosomia", "Perinatal asphyxia"],
            "correct": 2,
            "explain": "Macrosomia (large fetus) is opposite to IUGR. IUGR complications include preterm labor, stillbirth, asphyxia, and NEC."
        }
    ],
    "s10": [
        {
            "q": "What is the recommended mode of delivery for IUGR?",
            "options": ["Vaginal with oxytocin", "Cesarean section", "Vacuum-assisted", "Forceps delivery"],
            "correct": 1,
            "explain": "CS is the rule — the IUGR fetus does not tolerate the reduced oxygen supply and birth trauma of vaginal delivery."
        },
        {
            "q": "Which is part of antenatal IUGR management?",
            "options": ["Immediate delivery", "CS", "Monitoring of fetal wellbeing", "Postnatal dysmaturity care"],
            "correct": 2,
            "explain": "Antenatal management includes treating the cause, no smoking, monitoring fetal wellbeing, and good diet."
        },
        {
            "q": "Postnatal IUGR management focuses on problems of:",
            "options": ["Macrosomia", "Dysmaturity", "Post-term complications", "Gestational diabetes"],
            "correct": 1,
            "explain": "Postnatal management focuses on dysmaturity: hypoglycemia, hypothermia, polycythemia, feeding difficulties, and neurodevelopmental follow-up."
        }
    ],
}

# ========================================================================
# FILE 4: 42_Macrosomia.html
# ========================================================================
macro_data = {
    "s2": [
        {
            "q": "Fetal macrosomia is defined as weight greater than:",
            "options": ["3,500 g", "4,000 g", "4,500 g", "5,000 g"],
            "correct": 1,
            "explain": "Macrosomia is defined as fetal weight > 4,000 grams."
        }
    ],
    "s3": [
        {
            "q": "Which is a risk factor for fetal macrosomia?",
            "options": ["Primiparity", "Female infant", "Maternal age > 35", "Low maternal BMI"],
            "correct": 2,
            "explain": "Risk factors: history of macrosomia, obesity, excessive weight gain, multiparity, male infants, and maternal age > 35."
        },
        {
            "q": "Male infants are at higher risk for macrosomia because:",
            "options": ["Larger head circumference", "They typically weigh slightly more", "Faster early growth", "Higher DM rates"],
            "correct": 1,
            "explain": "Male infants typically weigh slightly more than female infants, increasing macrosomia risk."
        },
        {
            "q": "The risk of macrosomia increases with:",
            "options": ["Decreasing maternal age", "Each subsequent pregnancy", "Low pre-pregnancy weight", "Female fetal gender"],
            "correct": 1,
            "explain": "The risk of macrosomia increases with each subsequent pregnancy."
        }
    ],
    "s4": [
        {
            "q": "Which maternal condition can cause fetal macrosomia?",
            "options": ["Chronic hypertension", "Diabetes", "SLE", "Sickle cell disease"],
            "correct": 1,
            "explain": "Maternal diabetes can cause fetal macrosomia. Other causes: genetic factors, multiparity, and postterm pregnancy."
        },
        {
            "q": "All are causes of macrosomia EXCEPT:",
            "options": ["Genetic factors", "Maternal diabetes", "Postterm pregnancy", "Placental insufficiency"],
            "correct": 3,
            "explain": "Placental insufficiency is associated with IUGR, not macrosomia."
        },
        {
            "q": "Which is a cause of macrosomia?",
            "options": ["Preterm labor", "Postterm pregnancy", "Oligohydramnios", "IUGR"],
            "correct": 1,
            "explain": "Postterm pregnancy causes continued fetal growth beyond term, resulting in a large-for-gestational-age fetus."
        }
    ],
    "s5": [
        {
            "q": "Which is a clinical feature of macrosomia?",
            "options": ["Decreased fundal height", "Large fundal height", "Oligohydramnios", "Decreased movements"],
            "correct": 1,
            "explain": "Clinical features: large fundal height and excessive amniotic fluid (polyhydramnios)."
        },
        {
            "q": "Which finding on examination may suggest macrosomia?",
            "options": ["Small fundal height", "Oligohydramnios", "Polyhydramnios", "Breech presentation"],
            "correct": 2,
            "explain": "Polyhydramnios (excessive AF) is a clinical feature of macrosomia along with large fundal height."
        }
    ],
    "s6": [
        {
            "q": "Which is a maternal complication of macrosomia?",
            "options": ["Fetal fractures", "Brachial plexus injury", "Postpartum hemorrhage", "Meconium aspiration"],
            "correct": 2,
            "explain": "PPH is a maternal complication. Fetal injuries, meconium aspiration, and shoulder dystocia are fetal/neonatal complications."
        },
        {
            "q": "Shoulder dystocia in macrosomia can cause:",
            "options": ["Maternal hypertension", "Fetal injuries including fractures and brachial plexus injury", "Gestational diabetes", "Preterm labor"],
            "correct": 1,
            "explain": "Shoulder dystocia can cause fetal injuries including fractures and brachial plexus injuries."
        },
        {
            "q": "All are complications of macrosomia EXCEPT:",
            "options": ["Shoulder dystocia", "Uterine rupture", "Fetal growth restriction", "PPH"],
            "correct": 2,
            "explain": "IUGR/fetal growth restriction is the opposite condition. Macrosomia complications include shoulder dystocia, fetal injuries, PPH, and uterine rupture."
        }
    ],
    "s7": [
        {
            "q": "Which delivery mode is recommended for macrosomia?",
            "options": ["Induction of labor", "Cesarean section", "Vacuum extraction", "Forceps"],
            "correct": 1,
            "explain": "Cesarean section is safe for both mother and fetus in cases of macrosomia."
        },
        {
            "q": "Which is part of antenatal management of macrosomia?",
            "options": ["Immediate delivery at 37 weeks", "Proper antenatal care to prevent and diagnose before labor", "ECV", "Amnio-reduction"],
            "correct": 1,
            "explain": "Proper antenatal care aims to prevent macrosomia and diagnose it before labor."
        },
        {
            "q": "Postnatal management of a macrosomic neonate includes:",
            "options": ["Immediate CS", "Proper examination and management of any problem", "Induction of labor", "Amnio-infusion"],
            "correct": 1,
            "explain": "Postnatal management involves proper examination of the neonate and management of any identified problems."
        }
    ],
}

def main():
    files = [
        ("18_Amniotic_Fluid_Abnormalities.html", af_data),
        ("29_Shoulder_Dystocia.html", sd_data),
        ("40_Intrauterine_Growth_Restriction.html", iugr_data),
        ("42_Macrosomia.html", macro_data),
    ]
    for fname, mcq_data in files:
        input_path  = os.path.join(BASE, SUBDIR, fname)
        output_path = os.path.join(ENH, SUBDIR, fname)
        print(f"Processing {fname}...")
        process_file(input_path, output_path, mcq_data)
        print(f"  Done -> {output_path}")

if __name__ == "__main__":
    main()
