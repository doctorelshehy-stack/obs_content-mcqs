#!/usr/bin/env python3
"""MCQ data for all remaining Weeks 2, 3, 5 files."""
import json, os

# ============================================================
# WEEK 2
# ============================================================

# 08_Antepartum_Hemorrhage
w2_08 = {
    "s2": [{"q": "Antepartum hemorrhage is defined as bleeding from the genital tract after:", "options": ["20 weeks of gestation", "24 weeks of gestation", "28 weeks of gestation", "32 weeks of gestation"], "correct": 1, "explain": "APH is bleeding from the genital tract from 24 weeks of gestation until delivery."}],
    "s4": [{"q": "Placenta previa occurs when the placenta is inserted into the:", "options": ["Upper uterine segment", "Lower uterine segment", "Fundus", "Posterior wall"], "correct": 1, "explain": "Placenta previa is the insertion of the placenta into the lower uterine segment."}],
    "s5": [{"q": "In type IV placenta previa, the placenta:", "options": ["Reaches the lower segment but not the os", "Reaches the internal os", "Covers the internal os completely when closed", "Covers the internal os completely even when fully dilated"], "correct": 3, "explain": "Type IV (centralis totalis): the placenta completely covers the internal os even when the cervix is fully dilated."}],
    "s6": [{"q": "The classic presentation of placenta previa is:", "options": ["Painful vaginal bleeding with uterine hypertonus", "Painless, recurrent, bright red vaginal bleeding", "Continuous bleeding with open cervix", "Blood-stained mucus discharge"], "correct": 1, "explain": "Placenta previa presents with painless, recurrent, bright red vaginal bleeding. The uterus is soft and non-tender."}],
    "s7": [{"q": "The gold standard investigation for diagnosing placenta previa is:", "options": ["Digital vaginal examination", "Transabdominal ultrasound", "Transvaginal ultrasound", "MRI"], "correct": 2, "explain": "Transvaginal ultrasound is the gold standard, providing accurate placental localization."}],
    "s9": [{"q": "Abruptio placentae is defined as:", "options": ["Placenta covering the internal os", "Premature separation of a normally situated placenta", "Placenta implanted in the lower segment", "Abnormal adherence of the placenta"], "correct": 1, "explain": "Abruptio placentae (placental abruption) is premature separation of a normally situated placenta from the uterine wall."}],
    "s11": [{"q": "A key distinguishing feature of abruptio placentae vs placenta previa is:", "options": ["Painless bleeding", "Painful, tender uterus with continuous bleeding", "Bright red blood", "Soft, non-tender uterus"], "correct": 1, "explain": "Abruption presents with painful vaginal bleeding with a tense, tender uterus (Couvelaire uterus)."],
    "s14": [{"q": "The definitive management of severe abruptio placentae is:", "options": ["Bed rest and observation", "Immediate delivery regardless of gestational age", "Tocolysis", "Transfusion only"], "correct": 1, "explain": "In severe abruption with maternal or fetal compromise, immediate delivery is indicated regardless of gestational age."}],
    "s15": [{"q": "Ruptured uterus is most commonly associated with:", "options": ["Normal spontaneous vaginal delivery", "Previous cesarean section scar", "Placenta previa", "Multiple pregnancy"], "correct": 1, "explain": "Previous cesarean section scar is the most common cause of uterine rupture."}],
    "s21": [{"q": "Vasa previa occurs when fetal blood vessels run across the:", "options": ["Lower uterine segment", "Internal cervical os in front of the presenting part", "Placental surface", "Umbilical cord"], "correct": 1, "explain": "In vasa previa, fetal vessels run across the internal os in front of the presenting part, often with velamentous insertion."}],
    "s24": [{"q": "The Kleihauer-Betke test is used to:", "options": ["Detect fetal RBCs in maternal circulation", "Diagnose placental abruption", "Assess fetal lung maturity", "Detect amniotic fluid embolism"], "correct": 0, "explain": "Kleihauer-Betke test detects fetal RBCs in maternal circulation, used in fetomaternal hemorrhage."}],
    "s25": [{"q": "The Apt test differentiates:", "options": ["Maternal from fetal hemoglobin", "Rh-positive from Rh-negative blood", "Placenta previa from abruption", "Arterial from venous blood"], "correct": 0, "explain": "The Apt test differentiates fetal from maternal hemoglobin using alkali denaturation."}]
}
w2_08 = {k:v for k,v in w2_08.items() if v}

# 09_Vomiting_with_Pregnancy
w2_09 = {
    "s2": [{"q": "Hyperemesis gravidarum is severe vomiting in pregnancy that leads to all EXCEPT:", "options": ["Dehydration", "Weight loss", "Mild nausea only", "Electrolyte imbalance"], "correct": 2, "explain": "Hyperemesis gravidarum is severe, persistent vomiting causing dehydration, weight loss, and electrolyte imbalance."}],
    "s3": [{"q": "Emesis gravidarum differs from hyperemesis gravidarum in that it:", "options": ["Requires hospitalization", "Causes weight loss >5%", "Is mild and self-limiting", "Needs IV fluids"], "correct": 2, "explain": "Emesis gravidarum (morning sickness) is mild, self-limiting nausea/vomiting, while hyperemesis is severe with complications."}],
    "s6": [{"q": "Complications of hyperemesis gravidarum include all EXCEPT:", "options": ["Wernicke's encephalopathy (thiamine deficiency)", "Hyponatremia and hypokalemia", "Fetal macrosomia", "Weight loss >5% of pre-pregnancy weight"], "correct": 2, "explain": "Complications include Wernicke's encephalopathy (thiamine deficiency), electrolyte imbalance, metabolic alkalosis, and weight loss."}],
    "s8": [{"q": "First-line pharmacotherapy for hyperemesis gravidarum is:", "options": ["Metoclopramide", "Ondansetron", "Pyridoxine (vitamin B6) ± doxylamine", "Corticosteroids"], "correct": 2, "explain": "Pyridoxine (vitamin B6) with or without doxylamine is first-line. Antiemetics are added if no response."}],
    "s12": [{"q": "Management of hyperemesis with hypovolemia includes all EXCEPT:", "options": ["IV fluid resuscitation (RL or NS)", "Thiamine supplementation", "Total parenteral nutrition as first line", "Monitor electrolytes"], "correct": 2, "explain": "IV fluids are first line with thiamine (to prevent Wernicke's). TPN is reserved for severe refractory cases."}]
}
w2_09 = {k:v for k,v in w2_09.items() if v}

# 10_Anemia_with_Pregnancy
w2_10 = {
    "s2": [{"q": "Anemia in pregnancy is defined as hemoglobin below:", "options": ["10 g/dL", "11 g/dL", "12 g/dL", "9 g/dL"], "correct": 1, "explain": "WHO defines anemia in pregnancy as Hb < 11 g/dL (or Hct < 33%)."},
    {"q": "The most common type of anemia in pregnancy is:", "options": ["Megaloblastic anemia", "Iron deficiency anemia", "Thalassemia", "Physiologic anemia"], "correct": 1, "explain": "Iron deficiency anemia is the most common type of anemia in pregnancy worldwide."}],
    "s9": [{"q": "Treatment of iron deficiency anemia in pregnancy includes all EXCEPT:", "options": ["Oral ferrous sulfate (200 mg daily)", "Vitamin C to enhance absorption", "Folic acid alone", "IV iron for severe cases or intolerance"], "correct": 2, "explain": "Treatment is oral iron with vitamin C. Folic acid is for megaloblastic anemia, not iron deficiency."}],
    "s10": [{"q": "Megaloblastic anemia in pregnancy is most commonly due to:", "options": ["Iron deficiency", "Folic acid deficiency", "Vitamin B12 deficiency", "Hemolysis"], "correct": 1, "explain": "Folic acid deficiency is the most common cause of megaloblastic anemia in pregnancy."}],
    "s12": [{"q": "Thalassemia is a disorder of:", "options": ["Iron metabolism", "Hemoglobin synthesis (quantitative)", "Hemoglobin structure (qualitative)", "RBC membrane"], "correct": 1, "explain": "Thalassemia is a quantitative disorder of hemoglobin synthesis with reduced globin chain production."}]
}
w2_10 = {k:v for k,v in w2_10.items() if v}

# 11_Cardiac_Diseases
w2_11 = {
    "s2": [{"q": "During pregnancy, cardiac output increases by approximately:", "options": ["10-20%", "30-50%", "60-80%", "100%"], "correct": 1, "explain": "Cardiac output increases by 30-50% during pregnancy, peaking at 28-32 weeks."}],
    "s4": [{"q": "In the NYHA classification, class III heart disease means:", "options": ["No limitation of physical activity", "Slight limitation — comfortable at rest, ordinary activity causes symptoms", "Marked limitation — less than ordinary activity causes symptoms", "Unable to carry out any physical activity without discomfort"], "correct": 2, "explain": "NYHA Class III: marked limitation with symptoms on less than ordinary activity, but comfortable at rest."}],
    "s10": [{"q": "The most dangerous period for a cardiac patient during labor is:", "options": ["Latent phase of first stage", "Immediately after delivery (first 24-48 hours)", "Active phase", "Early first stage"], "correct": 1, "explain": "Immediately after delivery (first 24-48 hours postpartum) is most dangerous due to fluid shifts, increased venous return, and cardiac overload."}],
    "s11": [{"q": "Pregnancy is contraindicated in all of the following cardiac conditions EXCEPT:", "options": ["Primary pulmonary hypertension", "Eisenmenger syndrome", "Mild mitral stenosis with NYHA class I", "Marfan syndrome with aortic root dilation"], "correct": 2, "explain": "Mild mitral stenosis with NYHA I may be manageable. Severe conditions with pulmonary hypertension are contraindicated."}]
}
w2_11 = {k:v for k,v in w2_11.items() if v}

# 17_Infectious_Diseases
w2_17 = {
    "s2": [{"q": "TORCH infections include all EXCEPT:", "options": ["Toxoplasmosis", "Rubella", "Cytomegalovirus", "Hepatitis B"], "correct": 3, "explain": "TORCH: Toxoplasmosis, Other (syphilis, varicella, HIV, parvovirus B19), Rubella, CMV, Herpes."}],
    "s3": [{"q": "Toxoplasmosis in pregnancy can cause all EXCEPT:", "options": ["Hydrocephalus", "Intracranial calcifications", "Chorioretinitis", "Deafness"], "correct": 3, "explain": "Classic triad: Hydrocephalus, intracranial calcifications, chorioretinitis. Deafness is more associated with CMV."}],
    "s4": [{"q": "Rubella infection in early pregnancy is associated with:", "options": ["Hydrops fetalis", "Congenital heart defects (especially PDA)", "Microcephaly only", "No fetal effects"], "correct": 1, "explain": "Congenital rubella syndrome: heart defects (PDA, pulmonary stenosis), cataracts, deafness if infected in first trimester."}],
    "s6": [{"q": "Neonatal herpes simplex virus infection is most commonly acquired:", "options": ["Transplacentally in first trimester", "During passage through an infected birth canal", "Via breastfeeding", "Postnatally"], "correct": 1, "explain": "Neonatal HSV is most commonly acquired during vaginal delivery through an infected birth canal."}]
}
w2_17 = {k:v for k,v in w2_17.items() if v}

# 30_Multiple_Pregnancy
w2_30 = {
    "s2": [{"q": "Dizygotic twins result from:", "options": ["Fertilization of one ovum by two sperm", "Fertilization of two separate ova by two separate sperm", "Splitting of one fertilized ovum", "Superfetation"], "correct": 1, "explain": "Dizygotic (fraternal) twins result from fertilization of two separate ova by two separate sperm."}],
    "s4": [{"q": "Monochorionic diamniotic twins result from splitting of the embryo at:", "options": ["Day 1-3", "Day 4-8", "Day 8-13", "Day 13-15"], "correct": 1, "explain": "Monochorionic diamniotic (day 4-8) is the most common monozygotic type. Day 1-3: dichorionic diamniotic. Day 8-13: monochorionic monoamniotic."}],
    "s12": [{"q": "Twin-to-twin transfusion syndrome (TTTS) is characterized by all EXCEPT:", "options": ["Discordant (unequal) amniotic fluid volumes", "Discordant fetal growth", "Both twins have equal hemoglobin levels", "Donor twin may be anemic and recipient polycythemic"], "correct": 2, "explain": "In TTTS, the donor twin is anemic-oliguric-oligohydramnios (stuck twin) and recipient is polycythemic-polyuric-polyhydramnios."}],
    "s10": [{"q": "A common maternal complication of multiple pregnancy is:", "options": ["Post-term pregnancy", "Polyhydramnios", "Fetal macrosomia", "Placenta previa"], "correct": 1, "explain": "Maternal complications: preeclampsia, anemia, polyhydramnios, preterm labor, postpartum hemorrhage."}]
}
w2_30 = {k:v for k,v in w2_30.items() if v}

# 18_Amniotic_Fluid_Abnormalities
w2_18 = {
    "s2": [{"q": "Polyhydramnios is defined as AFI >:", "options": ["18 cm", "24 cm", "30 cm", "8 cm"], "correct": 1, "explain": "Polyhydramnios: AFI > 24 cm or single deepest pocket > 8 cm. Oligohydramnios: AFI < 5 cm or SDP < 2 cm."}],
    "s3": [{"q": "A common cause of acute polyhydramnios is:", "options": ["Renal agenesis", "Monozygotic twins with TTTS", "Post-term pregnancy", "Placental abruption"], "correct": 1, "explain": "Acute polyhydramnios can occur in monozygotic twins (TTTS). Chronic polyhydramnios is often idiopathic or associated with fetal anomalies."}],
    "s5": [{"q": "Oligohydramnios is most commonly associated with:", "options": ["Fetal gastrointestinal obstruction", "Fetal renal anomalies", "Twins", "Diabetes mellitus"], "correct": 1, "explain": "Oligohydramnios is associated with fetal renal anomalies (renal agenesis, obstruction), post-term pregnancy, and IUGR."}]
}
w2_18 = {k:v for k,v in w2_18.items() if v}

# 29_Shoulder_Dystocia
w2_29 = {
    "s2": [{"q": "Shoulder dystocia is defined as:", "options": ["Delivery of the aftercoming head", "Delivery of the fetal shoulders requires additional maneuvers after the head", "Cord prolapse during delivery", "Transverse lie"], "correct": 1, "explain": "Shoulder dystocia occurs when delivery of the anterior shoulder is impacted after the head is delivered."}],
    "s5": [{"q": "The most important risk factor for shoulder dystocia is:", "options": ["Post-term pregnancy", "Fetal macrosomia", "Nulliparity", "Female fetus"], "correct": 1, "explain": "Fetal macrosomia (birth weight > 4000g) is the strongest risk factor. Others include maternal diabetes, obesity, and prolonged labor."}],
    "s6": [{"q": "The first maneuver in managing shoulder dystocia (HELPERR mnemonic) is:", "options": ["McRoberts maneuver with suprapubic pressure", "Episiotomy", "Wood's screw maneuver", "Delivery of posterior arm"], "correct": 0, "explain": "HELPERR: H-Help, E-Empty bladder, L-Legs (McRoberts), P-Suprapubic pressure, E-Enter, R-Remove posterior arm, R-Roll."}],
    "s8": [{"q": "A potential fetal complication of shoulder dystocia is:", "options": ["Cephalohematoma", "Brachial plexus injury (Erb-Duchenne palsy)", "Cerebral palsy", "Skull fracture"], "correct": 1, "explain": "Fetal complications: brachial plexus injury (Erb's palsy), clavicle fracture, hypoxia, and rarely permanent neurologic damage."}]
}
w2_29 = {k:v for k,v in w2_29.items() if v}

# 40_IUGR
w2_40 = {
    "s2": [{"q": "IUGR is defined as estimated fetal weight below:", "options": ["5th percentile for gestational age", "10th percentile for gestational age", "15th percentile for gestational age", "3rd percentile for gestational age"], "correct": 1, "explain": "IUGR is defined as EFW < 10th percentile for gestational age."}],
    "s3": [{"q": "Symmetrical (Type I) IUGR is characterized by:", "options": ["Disproportionately small abdomen, normal head", "All parameters proportionally small — early onset", "Normal growth until late second trimester then slowing", "Head circumference spared"], "correct": 1, "explain": "Symmetrical IUGR: All parameters proportionally small, early onset, due to intrinsic causes (genetic, infection). Asymmetrical IUGR: Late onset, head spared, abdomen small."}],
    "s5": [{"q": "A common maternal cause of IUGR is:", "options": ["Obesity", "Preeclampsia", "Multiple pregnancy", "Diabetes"], "correct": 1, "explain": "Maternal causes: preeclampsia, chronic hypertension, renal disease, smoking, and malnutrition."}],
    "s10": [{"q": "Management of IUGR includes all EXCEPT:", "options": ["Serial ultrasound growth scans and Doppler", "Early delivery if fetal compromise", "Increased caloric intake to accelerate growth", "Antenatal corticosteroids if early delivery anticipated"], "correct": 2, "explain": "IUGR management: serial monitoring, Doppler assessment, early delivery for compromise, and steroids for lung maturity. There is no treatment to accelerate growth."}]
}
w2_40 = {k:v for k,v in w2_40.items() if v}

# 42_Macrosomia
w2_42 = {
    "s2": [{"q": "Macrosomia is defined as birth weight >:", "options": ["3500 g", "4000 g", "4500 g", "5000 g"], "correct": 1, "explain": "Macrosomia is defined as birth weight > 4000 g (4 kg) regardless of gestational age."}],
    "s4": [{"q": "The most common cause of fetal macrosomia is:", "options": ["Post-term pregnancy", "Maternal diabetes mellitus", "Genetic syndromes", "Maternal obesity alone"], "correct": 1, "explain": "Maternal diabetes mellitus (especially uncontrolled) is the most common cause due to fetal hyperinsulinemia."}],
    "s6": [{"q": "Maternal complications of macrosomia include all EXCEPT:", "options": ["Shoulder dystocia", "Perineal lacerations", "Preterm labor", "Postpartum hemorrhage"], "correct": 2, "explain": "Maternal complications: shoulder dystocia, perineal trauma, PPH. Macrosomia is associated with post-term, not preterm labor."}]
}
w2_42 = {k:v for k,v in w2_42.items() if v}

# 31_Preterm_Labor
w2_31 = {
    "s2": [{"q": "Preterm labor is defined as labor commencing before:", "options": ["37 weeks (259 days) of gestation", "34 weeks of gestation", "32 weeks of gestation", "28 weeks of gestation"], "correct": 0, "explain": "Preterm labor is cervical change with regular contractions before 37 completed weeks."}],
    "s7": [{"q": "Prophylactic management to prevent preterm labor includes all EXCEPT:", "options": ["Progesterone supplementation in high-risk women", "Cervical cerclage for cervical incompetence", "Routine bed rest in all women", "Treating infections"], "correct": 2, "explain": "Evidence-based prophylaxis: progesterone, cervical cerclage, infection treatment, and lifestyle modification. Routine bed rest is not effective."}],
    "s9": [{"q": "Antenatal corticosteroids (betamethasone/dexamethasone) for fetal lung maturity:", "options": ["Are given only after delivery", "Should be given between 24-34 weeks if preterm delivery is anticipated", "Are contraindicated in preterm labor", "Have no effect on neonatal outcomes"], "correct": 1, "explain": "Betamethasone/dexamethasone given between 24-34 weeks reduces RDS, IVH, and neonatal mortality."}],
    "s10": [{"q": "Which of the following is a contraindication to tocolysis?", "options": ["Preterm labor at 30 weeks", "Chorioamnionitis", "Multiple pregnancy", "Preterm PROM"], "correct": 1, "explain": "Contraindications: chorioamnionitis, severe preeclampsia, fetal distress, placental abruption, and lethal fetal anomaly."}]
}
w2_31 = {k:v for k,v in w2_31.items() if v}

# 32_PROM
w2_32 = {
    "s2": [{"q": "PROM is defined as rupture of membranes:", "options": ["Before 37 weeks", "Before the onset of labor", "During labor", "After 42 weeks"], "correct": 1, "explain": "PROM is rupture of membranes before the onset of labor. Preterm PROM (pPROM) is PROM before 37 weeks."}],
    "s5": [{"q": "Diagnosis of PROM is confirmed by all EXCEPT:", "options": ["Pooling of fluid on speculum examination", "Ferning pattern on microscopy", "Nitrazine test (turns blue)", "Elevated WBC count"], "correct": 3, "explain": "Diagnosis: pooling of fluid, ferning (arborization), nitrazine positive (pH 7.0-7.5)."}]}
w2_32 = {k:v for k,v in w2_32.items() if v}

# 41_Postterm_Pregnancy
w2_41 = {
    "s2": [{"q": "Postterm pregnancy is defined as gestation beyond:", "options": ["40 weeks", "41 weeks", "42 weeks (294 days)", "43 weeks"], "correct": 2, "explain": "Postterm: pregnancy ≥ 42 completed weeks (294 days) from LMP."}],
    "s6": [{"q": "Fetal complications of postterm pregnancy include all EXCEPT:", "options": ["Macrosomia", "Meconium aspiration syndrome", "Preterm birth", "Dysmaturity (postmaturity syndrome)"], "correct": 2, "explain": "Fetal complications: macrosomia, meconium aspiration, oligohydramnios, dysmaturity, and stillbirth."}],
    "s7": [{"q": "Management of postterm pregnancy includes:", "options": ["Immediate cesarean section at 41 weeks", "Induction of labor by 41+0 to 42+0 weeks with fetal monitoring", "Wait until 44 weeks", "Routine amniocentesis"], "correct": 1, "explain": "Induction is recommended by 41+0 to 42+0 weeks with serial fetal monitoring (BPP, NST)."}]
}
w2_41 = {k:v for k,v in w2_41.items() if v}

# 43_IUD
w2_43 = {
    "s2": [{"q": "Intrauterine fetal death (IUD) is defined as fetal death after:", "options": ["20 weeks of gestation", "24 weeks of gestation", "28 weeks of gestation", "12 weeks of gestation"], "correct": 0, "explain": "IUD is fetal death in utero after 20 weeks of gestation."}],
    "s6": [{"q": "A serious complication of prolonged retention of a dead fetus is:", "options": ["Fetal macrosomia", "Disseminated intravascular coagulation (DIC)", "Preeclampsia", "Polyhydramnios"], "correct": 1, "explain": "DIC may occur with prolonged retention of dead fetus (especially >4 weeks) due to release of thromboplastins."}],
    "s7": [{"q": "Management of IUD includes:", "options": ["Immediate expectant management regardless of gestation", "Induction of labor after diagnosis and counseling", "Cesarean section routinely", "EMCO only"], "correct": 1, "explain": "After confirming diagnosis and counseling, induction of labor is offered unless expectant management is chosen."}]
}
w2_43 = {k:v for k,v in w2_43.items() if v}

# 46_Fetal_Wellbeing
w2_46 = {
    "s2": [{"q": "A reactive NST requires:", "options": ["2 accelerations of 15 bpm for 15 seconds in 20 minutes", "3 accelerations in 10 minutes", "No decelerations", "Baseline variability <5 bpm"], "correct": 0, "explain": "Reactive NST: ≥2 accelerations of 15 bpm above baseline lasting ≥15 seconds in 20 minutes."}],
    "s4": [{"q": "A reassuring CTG includes all EXCEPT:", "options": ["Baseline 110-160 bpm", "Variability ≥5 bpm", "Late decelerations", "No decelerations"], "correct": 2, "explain": "Reassuring CTG: baseline 110-160, variability ≥5 bpm, accelerations present, no late or variable decelerations."}],
    "s6": [{"q": "A Bishop score ≤6 and the fetus to be delivered is best managed by:", "options": ["Cesarean section", "Induction with oxytocin only", "Cervical ripening with prostaglandins then oxytocin", "Artificial rupture of membranes"], "correct": 2, "explain": "Unfavorable cervix (Bishop ≤6) requires cervical ripening (PGE1/PGE2) before oxytocin induction."}],
    "s7": [{"q": "A normal BPP score (8/8 or 8/10) indicates:", "options": ["Fetal distress", "Reassuring fetal status", "Immediate delivery", "Further testing required"], "correct": 1, "explain": "Normal BPP (8/8 or 8/10) is reassuring. 6/10 is equivocal. ≤4/10 suggests possible hypoxia requiring delivery."}]
}
w2_46 = {k:v for k,v in w2_46.items() if v}

# Save Week 2
for num, data in [('08', w2_08), ('09', w2_09), ('10', w2_10), ('11', w2_11),
                  ('17', w2_17), ('30', w2_30), ('18', w2_18), ('29', w2_29),
                  ('40', w2_40), ('42', w2_42), ('31', w2_31), ('32', w2_32),
                  ('41', w2_41), ('43', w2_43), ('46', w2_46)]:
    with open(f"/media/mohamed/projects3/projects/obstaric/obs app/mcq_data_w2_{num}.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"W2_{num}: {sum(len(v) for v in data.values())} MCQs, {len(data)} subtopics")

print("=== Week 2 saved ===")
