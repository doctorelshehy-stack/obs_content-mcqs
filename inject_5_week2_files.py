#!/usr/bin/env python3
"""
Inject MCQs into 5 Week 2 Obstetric files.
Uses from inject_mcqs import process_file
"""
import sys, os, json

# Add cwd to path
sys.path.insert(0, '/media/mohamed/projects3/projects/obstaric/obs app')
from inject_mcqs import process_file

BASE = "/media/mohamed/projects3/projects/obstaric/obs app/extracted/assets/second task/obstetric/Week2"
ENH = "/media/mohamed/projects3/projects/obstaric/obs app/enhanced-assets/second task/obstetric/Week2"

# ========== FILE 1: 09_Vomiting_with_Pregnancy.html ==========
mcqs_09 = {
    "s2": [  # Causes of Vomiting in Pregnancy
        {
            "q": "A 28-year-old primigravida at 14 weeks gestation presents with vomiting. Which of the following is a gynaecological complication that can cause vomiting in pregnancy?",
            "options": ["Emesis gravidarum", "Red degeneration of fibroid", "Severe pre-eclampsia", "Appendicitis"],
            "correct": 1,
            "explain": "Gynaecological complications causing vomiting include red degeneration of fibroid and torsion of ovarian cyst. Emesis gravidarum is pregnancy-related, severe pre-eclampsia is a complication of pregnancy, and appendicitis is a surgical cause."
        },
        {
            "q": "Which of the following is considered a surgical cause of vomiting in pregnancy?",
            "options": ["Vesicular mole", "Hyperemesis gravidarum", "Peptic ulcer", "Pyelonephritis"],
            "correct": 2,
            "explain": "Surgical causes include appendicitis, gall stones, and peptic ulcer. Vesicular mole and hyperemesis gravidarum are pregnancy-related, while pyelonephritis is a medical cause."
        },
        {
            "q": "A pregnant woman presents with vomiting. Which medical cause should be considered in the differential diagnosis?",
            "options": ["Torsion of ovarian cyst", "Food poisoning", "Vesicular mole", "Red degeneration of fibroid"],
            "correct": 1,
            "explain": "Medical causes of vomiting in pregnancy include food poisoning, gastritis, cholecystitis, and pyelonephritis. Torsion of ovarian cyst and red degeneration of fibroid are gynaecological causes, while vesicular mole is pregnancy-related."
        },
        {
            "q": "Which of the following pregnancy-related conditions is associated with vomiting?",
            "options": ["Red degeneration of fibroid", "Appendicitis", "Vesicular mole", "Gastritis"],
            "correct": 2,
            "explain": "Vesicular mole (hydatidiform mole) is a complication of pregnancy that can cause severe vomiting due to elevated hCG levels. It is important to exclude molar pregnancy by ultrasound in patients with severe hyperemesis."
        }
    ],
    "s3": [  # Emesis Gravidarum vs. Hyperemesis Gravidarum
        {
            "q": "Which of the following best describes emesis gravidarum?",
            "options": ["Severe vomiting leading to weight loss and electrolyte imbalance", "Nausea and vomiting on getting up in the morning starting about the 12th week", "Vomiting associated with fundus changes and encephalopathy", "Vomiting requiring parenteral nutrition"],
            "correct": 1,
            "explain": "Emesis gravidarum is nausea and vomiting on getting up in the morning, starting early in pregnancy about the 12th week. It does NOT affect the general condition."
        },
        {
            "q": "Hyperemesis gravidarum is characterized by all of the following EXCEPT:",
            "options": ["Fluid and electrolyte imbalance", "Acid-base imbalance", "Does not affect the general condition", "Nutritional deficiency and weight loss"],
            "correct": 2,
            "explain": "Hyperemesis gravidarum leads to fluid, electrolyte and acid-base imbalance, nutritional deficiency and weight loss. 'Does not affect the general condition' describes emesis gravidarum, not hyperemesis."
        },
        {
            "q": "A key clinical feature that distinguishes hyperemesis gravidarum from simple emesis gravidarum is:",
            "options": ["Vomiting only in the morning", "Onset at 12 weeks gestation", "Measurable metabolic derangement", "Resolves spontaneously by 16 weeks"],
            "correct": 2,
            "explain": "Hyperemesis gravidarum produces measurable metabolic derangement (fluid, electrolyte, acid-base imbalance, weight loss), whereas emesis gravidarum is self-limiting and does not affect general condition."
        }
    ],
    "s4": [  # Etiology and Pathogenesis
        {
            "q": "Which of the following hormonal factors is implicated in the pathogenesis of nausea and vomiting in pregnancy?",
            "options": ["Low progesterone levels", "Elevated human chorionic gonadotropin (hCG) levels", "Decreased estrogen levels", "Low thyroid stimulating hormone"],
            "correct": 1,
            "explain": "NVP is worse in conditions with elevated hCG levels (molar pregnancies, multiple gestations, Down's syndrome). Progesterone decreases smooth muscle contractility and may alter gastric emptying. Thyroid dysfunction due to cross-reactivity between hCG and TSH receptor is also implicated."
        },
        {
            "q": "What percentage of hyperemesis gravidarum cases are infected with Helicobacter pylori?",
            "options": ["Approximately 50%", "Approximately 90%", "Approximately 25%", "Approximately 10%"],
            "correct": 1,
            "explain": "About 90% of hyperemesis gravidarum cases are infected with Helicobacter pylori, suggesting an infectious etiological factor."
        },
        {
            "q": "The allergic theory of hyperemesis gravidarum explains which of the following clinical observations?",
            "options": ["Symptoms worsen after the first trimester", "Antihistamines help and symptoms resolve after the first trimester", "Patients have elevated IgE levels", "Symptoms are worse in multiple pregnancies"],
            "correct": 1,
            "explain": "The allergic theory proposes that the patient is allergic to the corpus luteum of pregnancy. This explains why antihistamines help and why symptoms often resolve after the 1st trimester when the corpus luteum degenerates."
        }
    ],
    "s5": [  # Prevention
        {
            "q": "Which of the following is recommended for prevention of nausea and vomiting in pregnancy?",
            "options": ["Iron supplementation in high doses", "Multivitamin with folic acid in early pregnancy", "Prophylactic antiemetics", "Low carbohydrate diet"],
            "correct": 1,
            "explain": "Prevention includes multivitamin with folic acid in early pregnancy and treating heartburn and acid reflux. Iron supplements should be avoided as they can provoke nausea."
        }
    ],
    "s6": [  # Complications of Hyperemesis Gravidarum
        {
            "q": "The most feared complication of hyperemesis gravidarum is:",
            "options": ["Mallory-Weiss syndrome", "Wernicke encephalopathy", "Placental dysfunction", "Acute tubular necrosis"],
            "correct": 1,
            "explain": "Wernicke encephalopathy from vitamin B1 (thiamine) deficiency is the most feared complication of HG. It is preventable with thiamine BEFORE any glucose is given."
        },
        {
            "q": "Wernicke encephalopathy in hyperemesis gravidarum results from deficiency of which vitamin?",
            "options": ["Vitamin B12", "Vitamin B1 (Thiamine)", "Vitamin K", "Folic acid"],
            "correct": 1,
            "explain": "Wernicke encephalopathy results from thiamine (vitamin B1) deficiency. Glucose administration without prior thiamine can precipitate the encephalopathy by exhausting remaining thiamine stores."
        },
        {
            "q": "Which of the following is a complication of hyperemesis gravidarum due to vitamin K deficiency?",
            "options": ["Wernicke encephalopathy", "Bleeding diseases or embryopathy", "Mallory-Weiss tears", "Hepatic insufficiency"],
            "correct": 1,
            "explain": "Vitamin K deficiency in hyperemesis gravidarum can lead to bleeding diseases or embryopathy. Other complications include Wernicke encephalopathy (B1 deficiency), Mallory-Weiss tears (esophageal), and placental dysfunction."
        }
    ],
    "s7": [  # Investigations
        {
            "q": "Which investigation is essential in hyperemesis gravidarum to exclude correctable causes?",
            "options": ["MRI brain", "Upper GI endoscopy", "Ultrasonography", "CT abdomen"],
            "correct": 2,
            "explain": "Ultrasound is essential to exclude multiple pregnancy and vesicular mole, which are two of the most common correctable causes of severe HG."
        },
        {
            "q": "Laboratory investigations in hyperemesis gravidarum should include all of the following EXCEPT:",
            "options": ["Kidney and liver functions", "CBC and hematocrit", "Electrolytes and blood gases", "Autoimmune antibody panel"],
            "correct": 3,
            "explain": "Investigations include kidney & liver functions, CBC, hematocrit, electrolytes, blood gases, urine ketones, and fundus examination. Autoimmune antibody panel is not routinely indicated."
        }
    ],
    "s8": [  # Management Without Hypovolemia
        {
            "q": "The step-up approach for management of vomiting without hypovolemia includes all of the following EXCEPT:",
            "options": ["Dietary changes", "Trigger avoidance", "Oral pharmacotherapy", "Immediate hospitalization and IV fluids"],
            "correct": 3,
            "explain": "For the ambulant, non-dehydrated patient, the step-up approach is: dietary adjustment → trigger avoidance → oral pharmacotherapy. Hospitalization and IV fluids are reserved for patients with hypovolemia."
        }
    ],
    "s9": [  # Dietary Changes
        {
            "q": "Which dietary advice is appropriate for a patient with nausea and vomiting in pregnancy?",
            "options": ["Large meals three times a day", "Iron supplements to prevent anemia", "Small amounts of food every one to two hours", "Avoid all fluids with meals"],
            "correct": 2,
            "explain": "Meals and snacks should be eaten slowly and in small amounts every one to two hours. Fluids should be taken at least 30 minutes before or after solid food. Iron supplements should be avoided as they cause gastric irritation."
        },
        {
            "q": "Which type of fluids are better tolerated in patients with nausea and vomiting in pregnancy?",
            "options": ["Warm and still fluids", "Cold, clear, and carbonated fluids", "Hot beverages", "High-protein milkshakes"],
            "correct": 1,
            "explain": "Fluids are better tolerated if cold, clear, and carbonated. Patients should avoid coffee and spicy, odorous, high-fat, acidic, or very sweet foods."
        }
    ],
    "s10": [  # Trigger Avoidance & Pharmacotherapy
        {
            "q": "Which is the first-line antiemetic agent recommended for nausea and vomiting in pregnancy?",
            "options": ["Ondansetron", "Metoclopramide", "Pyridoxine (Vitamin B6)", "Promethazine"],
            "correct": 2,
            "explain": "Pyridoxine (Vitamin B6) is the first-line antiemetic and is safe in pregnancy. Treatment should start with the safest agent and step up to more potent antiemetics as needed."
        },
        {
            "q": "The only antiemetic combination formally classified as Category A (safe) in pregnancy is:",
            "options": ["Metoclopramide and ondansetron", "Pyridoxine (B6) and doxylamine", "Promethazine and diphenhydramine", "Meclizine and dimenhydrate"],
            "correct": 1,
            "explain": "Pyridoxine (B6) + doxylamine is the only antiemetic combination formally classified as safe (Category A) in pregnancy. Every other drug is used when first-line therapy fails."
        },
        {
            "q": "Which of the following is used for refractory cases of nausea and vomiting in pregnancy?",
            "options": ["Pyridoxine", "Doxylamine", "Ondansetron (Serotonin antagonist)", "Antacids"],
            "correct": 2,
            "explain": "Ondansetron, a serotonin antagonist, is used for refractory cases. Pyridoxine and doxylamine are first-line, and acid-reducing agents are adjunctive."
        }
    ],
    "s12": [  # Management with Hypovolemia (HG)
        {
            "q": "In the management of hyperemesis gravidarum with hypovolemia, thiamine supplementation should be given:",
            "options": ["After glucose administration", "Before glucose administration to prevent Wernicke encephalopathy", "Only if neurological symptoms develop", "As an alternative to intravenous fluids"],
            "correct": 1,
            "explain": "Thiamine (100 mg IM/IV) MUST be given BEFORE glucose in any patient with persistent vomiting. Administering glucose first risks precipitating Wernicke encephalopathy in a thiamine-depleted patient."
        },
        {
            "q": "Which of the following is used in refractory cases of hyperemesis gravidarum?",
            "options": ["Oral metoclopramide only", "Glucocorticoids (methylprednisolone or hydrocortisone)", "High-dose iron supplementation", "Beta-blockers"],
            "correct": 1,
            "explain": "Glucocorticoids such as methylprednisolone (16 mg) IV every 8 hours or hydrocortisone 100 mg IV twice daily are used for refractory cases of hyperemesis gravidarum."
        },
        {
            "q": "After a period of gut rest in hyperemesis gravidarum, the recommended diet to begin with is:",
            "options": ["High-protein solid foods", "Bananas and rice", "Citrus fruits and juices", "Dairy products"],
            "correct": 1,
            "explain": "After a short period of gut rest, begin with a diet consisting of bananas, rice, and then advance the diet as tolerated (the BRAT diet concept)."
        }
    ],
    "s13": [  # Indications for Termination
        {
            "q": "Which of the following is NOT an indication for termination of pregnancy in hyperemesis gravidarum?",
            "options": ["Appearance of jaundice", "Proteinuria and progressive oliguria", "Mild ketonuria without weight loss", "Encephalopathy"],
            "correct": 2,
            "explain": "Indications for termination include: appearance of jaundice, proteinuria & progressive oliguria, creatinine rise, deterioration of general condition despite treatment, encephalopathy, and fundus changes. Mild ketonuria alone is not an indication."
        },
        {
            "q": "The appearance of which clinical sign indicates that conservative management of hyperemesis gravidarum is failing and termination may be needed?",
            "options": ["Morning nausea", "Mild ketonuria", "Fundus changes", "Weight gain"],
            "correct": 2,
            "explain": "Fundus changes (retinal hemorrhages) indicate end-organ damage and that conservative management is failing. Other signs include jaundice, progressive oliguria, creatinine rise, and encephalopathy."
        }
    ]
}

# ========== FILE 2: 10_Anemia_with_Pregnancy.html ==========
mcqs_10 = {
    "s2": [  # Definition
        {
            "q": "Anemia in pregnancy is defined as:",
            "options": ["Increase in total RBC count", "Decrease in total RBCs or hemoglobin leading to decreased oxygen-carrying capacity", "Increase in plasma volume only", "Decrease in white blood cell count"],
            "correct": 1,
            "explain": "Anemia in pregnancy is a decrease in the total red blood cells or hemoglobin in the blood during pregnancy, leading to decrease in oxygen-carrying capacity."
        }
    ],
    "s3": [  # Normal Hemoglobin Values
        {
            "q": "The normal hemoglobin cutoff for the 2nd trimester of pregnancy is:",
            "options": ["> 11 g/dL", "> 10.5 g/dL", "> 12 g/dL", "> 10 g/dL"],
            "correct": 1,
            "explain": "The 2nd trimester cutoff is > 10.5 g/dL (not 11). The 1st and 3rd trimester cutoff is > 11 g/dL, and postpartum cutoff is > 10 g/dL."
        },
        {
            "q": "The hemoglobin cutoff for the postpartum period is:",
            "options": ["> 11 g/dL", "> 10.5 g/dL", "> 10 g/dL", "> 12 g/dL"],
            "correct": 2,
            "explain": "The postpartum hemoglobin cutoff is > 10 g/dL. The 1st and 3rd trimester cutoff is > 11 g/dL, and the 2nd trimester cutoff is > 10.5 g/dL."
        },
        {
            "q": "Why is the 2nd trimester hemoglobin cutoff lower than the 1st and 3rd trimesters?",
            "options": ["Increased RBC production", "Physiologic plasma-volume expansion causing dilution", "Increased iron absorption", "Decreased fetal demands"],
            "correct": 1,
            "explain": "The second-trimester cutoff is lower because of physiologic plasma-volume expansion. Plasma rises more than red cell mass, causing hemodilution and lowering the hemoglobin concentration without any true RBC deficit."
        }
    ],
    "s4": [  # Signs and Symptoms
        {
            "q": "Which of the following is a classic sign of iron and B-vitamin deficiency anemias in pregnancy?",
            "options": ["Glossitis (smooth, beefy-red, sore tongue)", "Polyhydramnios", "Hypertension", "Fetal macrosomia"],
            "correct": 0,
            "explain": "Tongue glossitis (smooth, beefy-red, sore tongue) is a classical finding in iron and B-vitamin deficiency anemias. Other symptoms include headache, fatigue, lethargy, tachycardia, tachypnea, paresthesia, and pallor."
        },
        {
            "q": "In severe anemia during pregnancy, which complication can occur?",
            "options": ["Polyhydramnios", "Congestive heart failure", "Gestational diabetes", "Macrosomia"],
            "correct": 1,
            "explain": "In severe cases, congestive heart failure can occur. Always auscultate the heart and check for a flow murmur or gallop rhythm in any pregnant patient with profound anemia."
        }
    ],
    "s5": [  # Causes
        {
            "q": "Which of the following is classified as a cause of impaired production of red blood cells?",
            "options": ["Hemolysis in sickle cell disease", "Iron deficiency", "Antepartum hemorrhage", "Hookworm infestation"],
            "correct": 1,
            "explain": "Impaired production anemias include iron deficiency, B12/folate deficiency, marrow failure, and chronic disease. Hemolysis (sickle cell, thalassemia, G6PD) causes increased destruction, while APH and hookworm cause blood loss."
        },
        {
            "q": "Thalassemia is classified as which type of anemia by mechanism?",
            "options": ["Impaired production", "Increased destruction (hemolysis)", "Blood loss", "Dilutional"],
            "correct": 1,
            "explain": "Thalassemia is classified under increased destruction (hemolysis) along with sickle cell disease and G6PD deficiency, as there is increased destruction of abnormal red blood cells."
        }
    ],
    "s6": [  # Physiologic Anemia
        {
            "q": "Physiologic (dilutional) anemia in pregnancy occurs because:",
            "options": ["RBC mass decreases while plasma volume increases", "Plasma volume increases more than RBC mass, causing hemodilution", "Iron absorption is impaired", "Fetal demands deplete maternal iron stores"],
            "correct": 1,
            "explain": "During pregnancy, plasma volume increases more than red blood cell mass. The resulting hemodilution lowers the hemoglobin concentration without any true RBC deficit. This is physiologic, not pathologic."
        },
        {
            "q": "What is the physiological purpose of dilutional anemia in pregnancy?",
            "options": ["To reduce maternal oxygen consumption", "To improve placental perfusion by reducing blood viscosity", "To prevent iron overload", "To stimulate fetal erythropoiesis"],
            "correct": 1,
            "explain": "Dilutional anemia is the body's way of improving placental perfusion by reducing blood viscosity. The mid-pregnancy Hb nadir (~10.5 g/dL) is when it is most pronounced."
        }
    ],
    "s7": [  # Effects of Anemia on Pregnancy
        {
            "q": "Which of the following is a maternal effect of anemia during pregnancy?",
            "options": ["Fetal macrosomia", "Pregnancy-induced hypertension", "Polyhydramnios", "Post-term pregnancy"],
            "correct": 1,
            "explain": "Maternal effects of anemia include pregnancy-induced hypertension, accidental hemorrhage, preterm labor, prolonged labor and inertia, and postpartum hemorrhage. Fetal effects include abortion, IUGR, and IUFD."
        },
        {
            "q": "Anemia during labor can lead to which complication?",
            "options": ["Precipitous labor", "Prolonged labor and uterine inertia", "Uterine rupture", "Shoulder dystocia"],
            "correct": 1,
            "explain": "During labor, anemia can cause prolonged labor and uterine inertia because the myometrium is a working muscle that fails in hypoxia. Anemic mothers bleed more, contract less, and tolerate blood loss worse."
        },
        {
            "q": "Which fetal effect is associated with maternal anemia?",
            "options": ["Fetal macrosomia", "Intrauterine growth restriction (IUGR)", "Post-term pregnancy", "Polyhydramnios"],
            "correct": 1,
            "explain": "Fetal effects of maternal anemia include abortion, intrauterine growth restriction (IUGR), and intrauterine fetal death (IUFD)."
        }
    ],
    "s9": [  # Iron Deficiency Anemia
        {
            "q": "The diagnostic test for iron deficiency anemia with a finding of less than 30 ng/mL is:",
            "options": ["Serum iron concentration", "Serum ferritin", "Iron binding capacity", "Blood film"],
            "correct": 1,
            "explain": "Serum ferritin is diagnostic for iron deficiency anemia when less than 30 ng/mL. Blood film shows microcytic hypochromic anemia, serum iron is decreased, and iron binding capacity is increased."
        },
        {
            "q": "Which of the following enhances iron absorption?",
            "options": ["Tannins in tea", "Phytates in cereals", "Ascorbic acid (Vitamin C)", "Calcium-rich foods"],
            "correct": 2,
            "explain": "Factors that enhance iron absorption include heme iron, ferrous iron (Fe²⁺), and ascorbic acid (vitamin C). Calcium, tannins in tea, and phytates in cereals inhibit iron absorption."
        },
        {
            "q": "Which of the following is a contraindication for IV iron therapy?",
            "options": ["Third trimester of pregnancy", "History of anaphylaxis to parenteral iron", "Iron deficiency confirmed by ferritin", "Postpartum period"],
            "correct": 1,
            "explain": "Contraindications for IV iron include history of anaphylaxis or reactions to parenteral iron therapy, first trimester of pregnancy, active acute or chronic infection, and chronic liver disease."
        },
        {
            "q": "The recommended daily prophylactic dose of supplemental oral iron in pregnancy is:",
            "options": ["100-200 mg daily", "27-30 mg daily", "5-10 mg daily", "500 mg daily"],
            "correct": 1,
            "explain": "Prophylactic supplemental oral iron is 27-30 mg daily. Therapeutic oral iron (ferrous sulphate, ferrous gluconate) ranges from 40-200 mg elemental iron daily."
        }
    ],
    "s10": [  # Megaloblastic Anemia — Folic Acid Deficiency
        {
            "q": "The daily requirement of folic acid during pregnancy is:",
            "options": ["50-100 μg/day", "200-300 μg/day", "500-800 μg/day", "1000-2000 μg/day"],
            "correct": 1,
            "explain": "The daily requirement of folic acid during pregnancy is 200-300 μg/day. For treatment of deficiency, folic acid 5-15 mg/day orally is given."
        },
        {
            "q": "Which blood film finding is characteristic of folic acid deficiency anemia in pregnancy?",
            "options": ["Microcytic hypochromic RBCs", "Macrocytic hyperchromic RBCs with hypersegmented neutrophils", "Normocytic normochromic RBCs", "Target cells and sickle cells"],
            "correct": 1,
            "explain": "Folic acid deficiency shows macrocytic hyperchromic RBCs and hypersegmented neutrophilic nuclei (>5 lobes). Hypersegmented neutrophils are often the earliest sign of folate deficiency."
        },
        {
            "q": "Which drug can cause folic acid deficiency in pregnancy?",
            "options": ["Iron supplements", "Anti-epileptic drugs", "Antacids", "Antihistamines"],
            "correct": 1,
            "explain": "Folic acid antagonists such as anti-epileptic drugs can cause folic acid deficiency. Other causes include inadequate intake, defective absorption, and increased demand (pregnancy)."
        }
    ],
    "s11": [  # Vitamin B12 Deficiency Anemia
        {
            "q": "A unique feature of vitamin B12 deficiency anemia compared to folic acid deficiency is:",
            "options": ["Macrocytic RBCs", "GIT manifestations", "Neurologic manifestations (subacute combined degeneration)", "Hypersegmented neutrophils"],
            "correct": 2,
            "explain": "Vitamin B12 deficiency can cause neurologic manifestations including subacute combined degeneration of the spinal cord and peripheral neuritis, which are potentially irreversible if treatment is delayed. This distinguishes it from folic acid deficiency."
        },
        {
            "q": "Which of the following is a cause of vitamin B12 deficiency in pregnancy?",
            "options": ["Iron deficiency", "Deficient intrinsic factor due to atrophic gastritis or gastrectomy", "Excessive dietary intake", "Increased iron absorption"],
            "correct": 1,
            "explain": "Causes of B12 deficiency include deficient intrinsic factor (atrophic gastritis, gastrectomy), inadequate intake (rare), malabsorption syndromes, and increased demand (pregnancy)."
        }
    ],
    "s12": [  # Thalassemia Definition
        {
            "q": "Thalassemia is best described as:",
            "options": ["A qualitative disorder with defective globin chains", "A quantitative disorder with failure to produce either α or β chains of hemoglobin", "A disorder of heme synthesis", "An acquired hemolytic anemia"],
            "correct": 1,
            "explain": "Thalassemia is a quantitative disorder — the globin chains are made in the wrong numbers. Sickle cell disease is a qualitative disorder — the chains are made but defective."
        }
    ],
    "s13": [  # α-Thalassemia
        {
            "q": "α-Thalassemia major (homozygous) in the fetus is associated with:",
            "options": ["Mild anemia only", "Polyhydramnios, erythroblastosis, anemia and hydrops fetalis", "No clinical effects", "Maternal diabetes"],
            "correct": 1,
            "explain": "The fetus with α-thalassemia major shows polyhydramnios, erythroblastosis, anemia and hydrops. The fetus does not survive due to inability of oxygen transfer as the α-chain is responsible for O₂ carrying capacity."
        },
        {
            "q": "Why is α-thalassemia major incompatible with extrauterine life?",
            "options": ["The fetus cannot make HbF which still requires α-chains", "The fetus produces only adult hemoglobin", "Maternal antibodies destroy fetal RBCs", "The placenta is abnormal"],
            "correct": 0,
            "explain": "α-Thalassemia major is incompatible with life because even fetal hemoglobin (HbF) still requires α-chains. Without α-chains, no functional hemoglobin can be formed."
        }
    ],
    "s15": [  # Thalassemia Investigations
        {
            "q": "Which test can differentiate iron deficiency anemia from thalassemia trait?",
            "options": ["Blood film alone", "Serum ferritin and hemoglobin electrophoresis", "Reticulocyte count", "Platelet count"],
            "correct": 1,
            "explain": "Both iron deficiency anemia and thalassemia show microcytic hypochromic anemia on blood film. Serum ferritin is low in IDA and normal/high in thalassemia trait, while hemoglobin electrophoresis is diagnostic for thalassemia."
        }
    ]
}

# ========== FILE 3: 11_Cardiac_Diseases_with_Pregnancy.html ==========
mcqs_11 = {
    "s2": [  # Cardiovascular Physiology
        {
            "q": "During pregnancy, cardiac output increases due to:",
            "options": ["Decreased stroke volume and decreased heart rate", "Increased stroke volume and increased heart rate", "Increased systemic vascular resistance", "Decreased blood volume"],
            "correct": 1,
            "explain": "Cardiac output increases due to increased stroke volume and increased heart rate. There is also reduced systemic vascular resistance. Cardiac output rises ~30-50% by the third trimester."
        },
        {
            "q": "Cardiac decompensation during pregnancy most commonly occurs at:",
            "options": ["12-16 weeks", "28-32 weeks, during labor, and immediately postpartum", "6-8 weeks", "Only in the first trimester"],
            "correct": 1,
            "explain": "Cardiac decompensation most often occurs at 28-32 weeks (peak blood volume), during labor, and immediately postpartum (autotransfusion from contracted uterus) — when blood volume and venous return are at their highest."
        }
    ],
    "s3": [  # Incidence and Etiology
        {
            "q": "The most common acquired heart disease in pregnancy is:",
            "options": ["Ischemic heart disease", "Rheumatic heart disease (85% of acquired cases)", "Cardiomyopathy", "Pericarditis"],
            "correct": 1,
            "explain": "Rheumatic heart disease accounts for 85% of acquired cardiac disease in pregnancy, and mitral stenosis is the most common valve lesion."
        },
        {
            "q": "Which congenital heart diseases are most commonly encountered in pregnancy?",
            "options": ["Tetralogy of Fallot and truncus arteriosus", "ASD, VSD, and PDA", "Ebstein anomaly and coarctation", "Transposition of great arteries"],
            "correct": 1,
            "explain": "The most common congenital heart diseases seen in pregnancy are ASD (atrial septal defect), VSD (ventricular septal defect), and PDA (patent ductus arteriosus)."
        },
        {
            "q": "The incidence of cardiac disease complicating pregnancy is approximately:",
            "options": ["5-10%", "1-4%", "10-15%", "0.1-0.5%"],
            "correct": 1,
            "explain": "Cardiac disease complicates 1-4% of pregnancies in most populations."
        }
    ],
    "s4": [  # NYHA Classification
        {
            "q": "A pregnant patient with cardiac disease who has marked limitation in activity and is only comfortable at rest would be classified as NYHA Class:",
            "options": ["Class I", "Class II", "Class III", "Class IV"],
            "correct": 2,
            "explain": "NYHA Class III: Marked limitation in activity, even during less than ordinary activity. Only comfortable at rest. Class IV has symptoms even at rest."
        },
        {
            "q": "Which statement about NYHA classification in pregnancy is true?",
            "options": ["It is static and determined only at booking", "It is dynamic and should be re-assessed at every antenatal visit", "It only applies to congenital heart disease", "It is not used in pregnancy"],
            "correct": 1,
            "explain": "NYHA class is dynamic in pregnancy — a Class II patient can deteriorate to Class III as blood volume rises, then improve again postpartum. Re-classify at every antenatal visit, not just at booking."
        }
    ],
    "s5": [  # Diagnosis - History
        {
            "q": "Which symptoms in a pregnant cardiac patient point away from physiologic pregnancy and toward true left-sided heart failure?",
            "options": ["Heartburn and fatigue", "Paroxysmal nocturnal dyspnea and orthopnea", "Back pain and headache", "Peripheral edema and leg cramps"],
            "correct": 1,
            "explain": "Paroxysmal nocturnal dyspnea and orthopnea are the two symptoms that point away from 'physiologic pregnancy' and toward true left-sided heart failure."
        }
    ],
    "s6": [  # Diagnosis - Examination
        {
            "q": "The earliest evidence of cardiac decompensation in pregnancy is:",
            "options": ["Peripheral edema", "Tachycardia > 100/min and crepitations at lung bases", "Palpitations without other signs", "Mild ankle swelling"],
            "correct": 1,
            "explain": "The classic triad of decompensation is tachycardia > 100/min + crepitations at lung bases + displaced apex. This is the earliest evidence of decompensation requiring immediate hospitalization."
        }
    ],
    "s7": [  # Investigations
        {
            "q": "The investigation of choice for cardiac disease in pregnancy is:",
            "options": ["Chest X-ray", "Electrocardiography", "Echocardiography", "Cardiac MRI with contrast"],
            "correct": 2,
            "explain": "Echocardiography is the investigation of choice in pregnancy — it is non-ionizing, gives structural and functional information, and is safe to repeat serially."
        }
    ],
    "s8": [  # Misleading Findings
        {
            "q": "Which of the following auscultatory findings can be NORMAL in pregnancy?",
            "options": ["Loud pansystolic murmur", "Systolic ejection murmur and third heart sound", "Mid-diastolic rumble with opening snap", "Continuous machinery murmur"],
            "correct": 1,
            "explain": "A systolic ejection murmur and a third heart sound are physiologic in most pregnancies due to hyperkinetic circulation. Other normal findings include increased JVP (up to +5 cm) and dyspnea/tachycardia."
        },
        {
            "q": "Increased jugular venous pressure during normal pregnancy may be up to:",
            "options": ["+1 cm", "+5 cm", "+10 cm", "+15 cm"],
            "correct": 1,
            "explain": "During normal pregnancy, increased neck venous pressure up to +5 cm is not uncommon due to high cardiac output."
        }
    ],
    "s9": [  # Effect of Pregnancy on Heart Disease
        {
            "q": "Pregnancy typically affects a patient with heart disease by:",
            "options": ["Improving functional class", "Deteriorating one functional class", "Having no effect on functional class", "Eliminating the need for medication"],
            "correct": 1,
            "explain": "Pregnancy typically deteriorates the patient one functional class. It may precipitate heart failure mostly at 28-32 weeks and during the 2nd, 3rd, and 4th stages of labor."
        },
        {
            "q": "Which complication is increased in pregnancy in women with cardiac disease?",
            "options": ["Gestational diabetes only", "Subacute bacterial endocarditis, thromboembolism, and rheumatic attacks", "Preterm labor only", "Post-term pregnancy"],
            "correct": 1,
            "explain": "Pregnancy increases the risk of subacute bacterial endocarditis, thromboembolism, and rheumatic attacks in women with cardiac disease."
        }
    ],
    "s10": [  # Effect of Heart Disease on Pregnancy
        {
            "q": "Which of the following is a fetal effect of maternal heart disease?",
            "options": ["Increased birth weight", "Increased incidence of congenital malformation", "Post-term pregnancy", "Decreased risk of IUGR"],
            "correct": 1,
            "explain": "Fetal effects of maternal heart disease include increased incidence of congenital malformation (CFMF), IUGR, and IUFD. Preconception counseling and detailed anatomy scan at 20-22 weeks are mandatory."
        },
        {
            "q": "All of the following are maternal/obstetric effects of heart disease EXCEPT:",
            "options": ["Polyhydramnios", "Preterm labor", "Fetal macrosomia", "Preeclampsia"],
            "correct": 2,
            "explain": "Maternal/obstetric effects include polyhydramnios, preterm labor, postpartum hemorrhage, abortion, preeclampsia, placental abruption, and gestational diabetes. Fetal macrosomia is not a typical effect."
        }
    ],
    "s11": [  # Management During Pregnancy
        {
            "q": "Which of the following is contraindicated in the 1st trimester of a pregnant patient with mechanical heart valves?",
            "options": ["Heparin", "Warfarin", "Digoxin", "Diuretics"],
            "correct": 1,
            "explain": "Warfarin is teratogenic in the 1st trimester (warfarin embryopathy). Patients with mechanical valves should be switched to heparin before conception or as soon as pregnancy is confirmed."
        },
        {
            "q": "Heparin during pregnancy is indicated in cardiac patients with:",
            "options": ["All patients with heart disease", "Artificial valves or atrial fibrillation", "Mild mitral regurgitation", "Physiologic murmurs"],
            "correct": 1,
            "explain": "Heparin is indicated in patients with artificial valves or atrial fibrillation. It is not indicated for all cardiac patients."
        }
    ],
    "s12": [  # Management During Delivery
        {
            "q": "Which of the following cardiac conditions is an indication for cesarean delivery rather than vaginal delivery?",
            "options": ["Mild mitral regurgitation", "Tight mitral stenosis", "Mild aortic regurgitation", "Healed infective endocarditis"],
            "correct": 1,
            "explain": "Vaginal delivery is contraindicated in patients with restricted cardiac output such as tight MS, severe AS, primary pulmonary hypertension, Eisenmenger syndrome, and Marfan's syndrome with aortic root > 4 cm."
        },
        {
            "q": "The recommended timing of delivery for a compensated cardiac patient is:",
            "options": ["At term, not allowed to go postterm", "Always at 34 weeks", "Only when heart failure develops", "At 42 weeks"],
            "correct": 0,
            "explain": "Delivery is usually at term except if heart failure happens. The patient is not allowed to go postterm. Induce at 38-39 weeks in compensated cardiac patients."
        }
    ],
    "s13": [  # Intrapartum Management
        {
            "q": "During the 3rd stage of labor in a cardiac patient, which drug should be avoided?",
            "options": ["Oxytocin", "Ergot alkaloids (methylergometrine)", "Controlled cord traction", "Misoprostol"],
            "correct": 1,
            "explain": "Ergot alkaloids (methylergometrine) should be avoided at the 3rd stage as they cause vasoconstriction and hypertension that can precipitate acute decompensation. Use oxytocin infusion and controlled cord traction instead."
        },
        {
            "q": "To shorten the 2nd stage of labor in a cardiac patient, the recommended approach is:",
            "options": ["Fundal pressure", "Instrumental delivery (forceps or ventouse)", "Wait for spontaneous delivery", "Increase oxytocin infusion"],
            "correct": 1,
            "explain": "'Shorten the 2nd stage' means instrumental delivery (forceps or ventouse) at the right station. A long, exhausting 2nd stage is the single most common precipitant of acute pulmonary edema in labor."
        }
    ],
    "s14": [  # Puerperium & Contraception
        {
            "q": "Postpartum observation for cardiac patients is essential for how long?",
            "options": ["12 hours", "48 hours", "1 week", "24 hours"],
            "correct": 1,
            "explain": "Postpartum observation for 48 hours is essential as the risk of heart failure is high in this period due to autotransfusion from the contracted uterus."
        },
        {
            "q": "Which contraceptive method is safe for cardiac patients with high thromboembolic risk?",
            "options": ["Estrogen-containing oral contraceptives", "Progesterone-only methods", "Combined hormonal patch", "Vaginal ring"],
            "correct": 1,
            "explain": "Estrogen-containing contraceptives should be avoided in patients with high thromboembolic risk. Progesterone-only methods (DMPA, implant, levonorgestrel IUD) are safe."
        }
    ]
}

# ========== FILE 4: 08_Antepartum_Hemorrhage.html ==========
mcqs_08 = {
    "s2": [  # Definition
        {
            "q": "Antepartum hemorrhage is defined as bleeding from the vagina:",
            "options": ["At any time during pregnancy", "After 20 weeks of pregnancy and before childbirth", "Only in the third trimester", "Before 20 weeks of pregnancy"],
            "correct": 1,
            "explain": "APH is defined as bleeding from the vagina occurring at any time after the 20th week of pregnancy and before childbirth. Bleeding before 20 weeks is classified as threatened/missed/inevitable abortion."
        }
    ],
    "s3": [  # Classification
        {
            "q": "Which of the following is NOT one of the four etiological categories of antepartum hemorrhage?",
            "options": ["Placenta previa", "Abruptio placentae", "Vasa previa", "Cervical incompetence"],
            "correct": 3,
            "explain": "The four etiological categories are: (1) Placenta previa, (2) Accidental hemorrhage/Abruptio placentae, (3) Vasa previa, and (4) Extraplacental bleeding (ruptured uterus, cervical/vaginal lesions). Cervical incompetence is not a cause of APH."
        },
        {
            "q": "Extraplacental antepartum hemorrhage includes:",
            "options": ["Only placenta previa", "Ruptured uterus and lesions of cervix or vagina", "Only vasa previa", "Abruptio placentae only"],
            "correct": 1,
            "explain": "Extraplacental bleeding (incidental hemorrhage) includes rupture uterus and hemorrhage due to lesions of the cervix or vagina as erosion, polyp or carcinoma."
        }
    ],
    "s4": [  # Placenta Previa Definition
        {
            "q": "The incidence of placenta previa is approximately:",
            "options": ["1 in 1000 pregnancies", "1 in 200 pregnancies", "1 in 50 pregnancies", "1 in 20 pregnancies"],
            "correct": 1,
            "explain": "Placenta previa affects approximately 1 in 200 pregnancies."
        },
        {
            "q": "Why does placenta previa cause profuse bleeding?",
            "options": ["The placenta has more blood vessels than normal", "The lower uterine segment is poorly contractile and vessels cannot constrict after separation", "The mother has a coagulation disorder", "The fetus presses on the placenta"],
            "correct": 1,
            "explain": "The lower uterine segment is a relatively passive, poorly contractile area. When the placenta implants here, the vessels that anchor it cannot constrict after separation — leading to profuse, sometimes catastrophic, bleeding."
        }
    ],
    "s5": [  # Types I-IV
        {
            "q": "In which type of placenta previa does the placenta cover the internal os completely whether the cervix is partially or fully dilated?",
            "options": ["Type I — Placenta previa lateralis", "Type II — Placenta previa marginalis", "Type III — Incomplete placenta previa centralis", "Type IV — Complete placenta previa centralis"],
            "correct": 3,
            "explain": "Type IV (Complete placenta previa centralis): The placenta covers the internal os completely whether the cervix is partially or fully dilated. Types III and IV are 'major' previa where cesarean delivery is mandatory."
        },
        {
            "q": "Which types of placenta previa are classified as 'minor' where vaginal delivery may be possible?",
            "options": ["Types I and II", "Types III and IV", "Types II and III", "Types I and IV"],
            "correct": 0,
            "explain": "Types I and II are sometimes grouped as 'minor' previa where vaginal delivery may be possible. Types III and IV are 'major' previa where cesarean delivery is mandatory."
        }
    ],
    "s6": [  # Clinical Picture of Placenta Previa
        {
            "q": "The classic triad of symptoms for placenta previa is:",
            "options": ["Painful bleeding, rigid abdomen, fetal distress", "Painless vaginal bleeding, soft lax abdomen, malpresentation/non-engagement", "Severe abdominal pain, board-like uterus, absent FHS", "Fever, uterine tenderness, foul discharge"],
            "correct": 1,
            "explain": "The classic bedside triad for placenta previa is: (1) painless vaginal bleeding, (2) soft lax abdomen, (3) malpresentation/non-engagement. Any one should prompt ultrasound before digital vaginal examination."
        },
        {
            "q": "The mean gestational age at diagnosis of placenta previa is:",
            "options": ["20 weeks", "28 weeks", "32 weeks", "36 weeks"],
            "correct": 2,
            "explain": "The mean gestational age at diagnosis of placenta previa is 32 weeks. It usually presents as painless, causeless, recurrent vaginal bleeding in the third trimester."
        }
    ],
    "s7": [  # Investigations
        {
            "q": "The diagnostic technique of choice for placenta previa is:",
            "options": ["Digital vaginal examination", "Transvaginal ultrasound", "Abdominal X-ray", "CT scan"],
            "correct": 1,
            "explain": "Ultrasound is the diagnostic technique of choice — especially transvaginal ultrasound. Digital vaginal examination is CONTRAINDICATED in suspected placenta previa as it can provoke catastrophic hemorrhage."
        }
    ],
    "s8": [  # Management
        {
            "q": "In expectant management of placenta previa remote from term, which drug is used as a tocolytic?",
            "options": ["Terbutaline", "Magnesium sulfate", "Nifedipine", "Atosiban"],
            "correct": 1,
            "explain": "If there are preterm contractions, magnesium sulfate can be used as a tocolytic. Steroids to enhance fetal lung maturity are given from 24-34 weeks."
        },
        {
            "q": "Delivery by elective cesarean section at 36-37 weeks is recommended for:",
            "options": ["Type I placenta previa", "Types III and IV (incomplete and complete centralis)", "All cases of placenta previa", "Only if there is active bleeding"],
            "correct": 1,
            "explain": "In incomplete and complete centralis (Types III and IV), the ideal is a well-planned elective cesarean section at 36-37 weeks. Vaginal delivery is allowed when the placental edge is more than 2 cm from the internal os."
        },
        {
            "q": "During expectant management of placenta previa, the target hematocrit should be maintained at:",
            "options": ["Greater than 20%", "Greater than 25%", "Greater than 30%", "Greater than 35%"],
            "correct": 2,
            "explain": "Replace blood loss to keep hematocrit greater than 30%. A fully cross-matched unit of blood must be available as lower-segment bleeding can be torrential within minutes."
        }
    ],
    "s9": [  # Abruptio Placentae Definition
        {
            "q": "Abruptio placentae is defined as:",
            "options": ["APH due to premature separation of abnormally situated placenta", "APH due to premature separation of normally situated placenta in the upper uterine segment", "Bleeding from fetal vessels", "Rupture of the uterine wall"],
            "correct": 1,
            "explain": "Abruptio placentae is APH due to premature separation of a normally situated placenta (upper uterine segment). The incidence is approximately 1 in 100 pregnancies."
        },
        {
            "q": "Which form of abruptio placentae is more dangerous?",
            "options": ["Revealed (visible) hemorrhage", "Concealed accidental hemorrhage", "Both equally", "Combined type only"],
            "correct": 1,
            "explain": "Concealed abruptio is the more dangerous form: less bleeding is seen externally, but the retroplacental hematoma can be large. The abdomen becomes tense, the uterus 'board-like,' and coagulopathy (DIC) can develop rapidly."
        }
    ],
    "s10": [  # Etiology of Abruptio Placentae
        {
            "q": "The single most important risk factor for abruptio placentae is:",
            "options": ["Trauma", "Hypertensive disorders with pregnancy (pre-eclampsia)", "Thrombophilia", "Submucous fibroid"],
            "correct": 1,
            "explain": "Pre-eclampsia (hypertensive disorders with pregnancy) is the single most important risk factor for abruptio placentae. Abruption is several-fold more common in women with hypertensive disorders of pregnancy."
        }
    ],
    "s11": [  # Clinical Picture
        {
            "q": "Which of the following is a characteristic feature of abruptio placentae on abdominal examination?",
            "options": ["Lax, soft abdomen", "Board-like abdomen with tenderness and rigidity", "Fetal parts easily felt", "Fundal level equals gestational age"],
            "correct": 1,
            "explain": "Abruptio placentae presents with a board-like, tender, rigid abdomen. Fundal level is greater than period of amenorrhea due to blood accumulation. Fetal parts are difficult to palpate due to rigidity."
        },
        {
            "q": "The percentage of patients with abruptio placentae who have visible vaginal bleeding is:",
            "options": ["20%", "50%", "80%", "100%"],
            "correct": 2,
            "explain": "Approximately 80% of patients with abruptio placentae have visible vaginal bleeding, while in 20% of patients the blood remains concealed."
        }
    ],
    "s12": [  # Investigations
        {
            "q": "Which statement about ultrasound diagnosis of abruptio placentae is true?",
            "options": ["Ultrasound is 100% sensitive", "Ultrasound has limited sensitivity and the diagnosis is largely clinical", "Ultrasound is the only diagnostic method", "MRI is required for diagnosis"],
            "correct": 1,
            "explain": "Ultrasound has limited sensitivity for abruptio placentae — a normal scan does not exclude it. The diagnosis is largely clinical (painful bleeding + tense uterus + fetal distress)."
        },
        {
            "q": "Coagulation profile in suspected abruptio placentae should include all EXCEPT:",
            "options": ["Prothrombin time", "Partial thromboplastin time", "Fibrinogen level and FDPs", "D-dimer only"],
            "correct": 3,
            "explain": "Coagulation profile includes PT, PTT, bleeding time, coagulation time, fibrinogen level, and fibrinogen degradation products. DIC is a feared complication due to consumption of clotting factors by the retroplacental clot."
        }
    ],
    "s13": [  # Complications
        {
            "q": "Which is the most feared complication of abruptio placentae?",
            "options": ["Postpartum hemorrhage", "Consumptive coagulopathy (DIC)", "Sheehan syndrome", "Amniotic fluid embolism"],
            "correct": 1,
            "explain": "Consumptive coagulopathy (DIC) is the most feared complication of abruptio placentae. Coagulation factors and fibrinogen are consumed by the retroplacental clot, producing a profound bleeding diathesis that can become uncontrollable."
        },
        {
            "q": "Which maternal complication is associated with abruptio placentae?",
            "options": ["Polyhydramnios", "Sheehan syndrome", "Cholestasis", "Gestational diabetes"],
            "correct": 1,
            "explain": "Maternal complications of abruptio placentae include hemorrhage, shock, ruptured uterus, acute renal failure, postpartum hemorrhage, Sheehan syndrome, amniotic fluid embolism, and consumptive coagulopathy (DIC)."
        }
    ],
    "s14": [  # Management
        {
            "q": "Termination of pregnancy in abruptio placentae is indicated when:",
            "options": ["Only at term", "If fetal distress is present or mother is unstable regardless of gestational age", "Only after 37 weeks", "Only if the patient requests it"],
            "correct": 1,
            "explain": "Termination is indicated if fetal distress is present or the mother is unstable regardless of gestational age while resuscitation is ongoing. Termination is by ARM and induction of labor or cesarean section."
        }
    ],
    "s15": [  # Ruptured Uterus
        {
            "q": "Ruptured uterus occurs in what percentage of multiparous women?",
            "options": ["50%", "75%", "95%", "100%"],
            "correct": 2,
            "explain": "95% of ruptured uterus cases occur in multiparous women. The primigravid uterus is rarely affected except in the presence of a congenital anomaly, trauma, or invasive procedure."
        },
        {
            "q": "The incidence of ruptured uterus is approximately:",
            "options": ["1-4 per 1000 pregnancies", "1-4 per 100 pregnancies", "1-4 per 10,000 pregnancies", "1-4 per 100,000 pregnancies"],
            "correct": 0,
            "explain": "The incidence of ruptured uterus is approximately 1-4 per 1000 pregnancies."
        }
    ],
    "s18": [  # Types, Site, Severity
        {
            "q": "Complete rupture of the uterus is defined as:",
            "options": ["Tearing of the endometrium only", "Tearing of the uterine wall including the peritoneum", "Tearing of the uterine wall without the peritoneum", "Tearing of the cervix only"],
            "correct": 1,
            "explain": "Complete rupture involves tearing of the uterine wall including the peritoneum. Incomplete rupture involves tearing without involving the peritoneum."
        },
        {
            "q": "During obstructed labor, the most common site of uterine rupture is:",
            "options": ["Fundus of the uterus", "Lower segment", "Cornual region", "Cervix"],
            "correct": 1,
            "explain": "Lower segment rupture occurs in obstructed labor. Other sites include the site of scar and extension of cervical tear into lower segment."
        }
    ],
    "s19": [  # Clinical Picture of Ruptured Uterus
        {
            "q": "A classic paradoxical sign of uterine rupture is:",
            "options": ["Intensification of contractions", "Cessation of contractions", "Increased fetal movements", "Rise in blood pressure"],
            "correct": 1,
            "explain": "'Cessation of contractions' is a paradoxical but classic sign: the uterine muscle has torn and can no longer generate effective contractions. Combined with sudden maternal tachycardia and hypotension, it requires immediate laparotomy."
        }
    ],
    "s20": [  # Management
        {
            "q": "Curative management of ruptured uterus involves:",
            "options": ["Expectant management with bed rest", "Emergent laparotomy with either repair or hysterectomy", "Vaginal delivery", "Antibiotics only"],
            "correct": 1,
            "explain": "Curative management of ruptured uterus is emergent laparotomy, followed by either repair or hysterectomy. Internal iliac artery ligation may be needed in cases of broad ligament hematoma."
        }
    ],
    "s21": [  # Vasa Previa
        {
            "q": "Vasa previa involves bleeding of which origin?",
            "options": ["Maternal origin only", "Fetal origin due to laceration of umbilical vessels", "Placental origin", "Uterine origin"],
            "correct": 1,
            "explain": "Vasa previa is fetal hemorrhage (bleeding of fetal origin) due to laceration of abnormally situated umbilical (fetal) vessels. Even 100 mL of fetal blood loss can cause hypovolemic shock and death."
        }
    ],
    "s22": [  # Causes of Vasa Previa
        {
            "q": "All of the following are causes of vasa previa EXCEPT:",
            "options": ["Bi-lobed placenta", "Velamentous insertion of the umbilical cord", "Succenturiate (accessory) lobe", "Single lobed placenta with central cord insertion"],
            "correct": 3,
            "explain": "Causes of vasa previa include bi-lobed placenta, velamentous insertion of the umbilical cord, and succenturiate (accessory) lobe. A single lobed placenta with central cord insertion is normal."
        }
    ],
    "s24": [  # Kleihauer-Betke Test
        {
            "q": "The Kleihauer-Betke test is used to:",
            "options": ["Diagnose placenta previa", "Measure the amount of fetal hemoglobin transferred to maternal blood", "Detect maternal anemia", "Diagnose vasa previa"],
            "correct": 1,
            "explain": "The Kleihauer-Betke test measures the amount of fetal hemoglobin transferred from a fetus to the mother's bloodstream. It is used to determine the required dose of Rh immune globulin and to detect fetomaternal hemorrhage."
        },
        {
            "q": "The Kleihauer-Betke test exploits the principle that:",
            "options": ["Fetal hemoglobin resists acid elution while adult hemoglobin does not", "Adult hemoglobin resists acid elution", "Both fetal and adult hemoglobin are affected equally", "Fetal cells are smaller than adult cells"],
            "correct": 0,
            "explain": "The Kleihauer-Betke test exploits the fact that fetal hemoglobin (HbF) resists acid elution, whereas adult hemoglobin does not. Fetal cells remain pink after acid treatment, adult cells become 'ghost' outlines."
        }
    ],
    "s25": [  # Apt Test
        {
            "q": "The Apt test is a rapid bedside test used to:",
            "options": ["Determine the fetal lung maturity", "Determine whether vaginal blood is of fetal or maternal origin", "Detect maternal anemia", "Diagnose DIC"],
            "correct": 1,
            "explain": "The Apt test allows the clinician to determine whether the source of blood is fetal (vasa previa) or maternal. Maternal blood turns yellow-green-brown, while fetal blood stays pink when NaOH is added."
        },
        {
            "q": "In the Apt test, what reagent is used to distinguish fetal from maternal blood?",
            "options": ["Hydrochloric acid", "Sodium hydroxide (NaOH)", "Hydrogen peroxide", "Ethanol"],
            "correct": 1,
            "explain": "The Apt test uses 10% NaOH. Maternal (adult) blood turns yellow-green-brown while fetal blood stays pink. This is based on the alkali denaturation of adult hemoglobin."
        }
    ],
    "s26": [  # Comparison Table
        {
            "q": "Which feature distinguishes placenta previa from abruptio placentae?",
            "options": ["Both present with painful bleeding", "Placenta previa presents with painless bleeding while abruptio placentae presents with painful bleeding", "Both present with board-like abdomen", "Both have equal incidence of fetal distress"],
            "correct": 1,
            "explain": "Painless vs. painful bleeding is the single most useful bedside distinction. Placenta previa: painless, causeless, recurrent bleeding. Abruptio placentae: painful, with uterine tenderness and rigidity."
        },
        {
            "q": "In abruptio placentae, the fundal level is typically:",
            "options": ["Equal to gestational age", "Greater than gestational age due to blood accumulation", "Less than gestational age", "Cannot be assessed"],
            "correct": 1,
            "explain": "In abruptio placentae, the fundal level is greater than gestational age due to blood accumulation behind the placenta. In placenta previa, the fundal level equals gestational age."
        }
    ]
}

# ========== FILE 5: 17_Infectious_Diseases_with_Pregnancy.html ==========
mcqs_17 = {
    "s2": [  # TORCH Acronym
        {
            "q": "The TORCH acronym in obstetrics stands for:",
            "options": ["Toxoplasma, Rubella, CMV, Herpes, and Others", "Tuberculosis, Rubella, Candidiasis, Hepatitis", "Toxoplasma, Rubella, Chlamydia, HSV, HIV", "Trichomonas, Rubella, CMV, HSV, HIV"],
            "correct": 0,
            "explain": "TORCH stands for Toxoplasma, Others (Parvovirus B19, VZV, measles, enteroviruses, HIV), Rubella, Cytomegalovirus, and Herpes simplex. These are infections known to produce congenital defects."
        },
        {
            "q": "Infections during pregnancy can develop in the neonate by all of the following routes EXCEPT:",
            "options": ["Transplacentally", "Perinatally (from vaginal secretions or blood)", "Postnatally (from breast milk)", "Through immunizations"],
            "correct": 3,
            "explain": "Infections can be transmitted transplacentally, perinatally (from vaginal secretions or blood), and postnatally (from breast milk or other sources). Immunizations are not a route of infection transmission."
        },
        {
            "q": "Which of the following is included under 'Others' in the TORCH acronym?",
            "options": ["Rubella virus", "Cytomegalovirus", "Parvovirus B19", "Toxoplasma gondii"],
            "correct": 2,
            "explain": "'Others' in TORCH includes Parvovirus B19 (B19V), varicella-zoster virus (VZV), measles virus, enteroviruses, and human immunodeficiency virus (HIV)."
        }
    ],
    "s3": [  # Toxoplasmosis
        {
            "q": "The definitive host for Toxoplasma gondii is:",
            "options": ["Dogs", "Cats", "Rats", "Birds"],
            "correct": 1,
            "explain": "Cats are the definitive hosts for Toxoplasma gondii. Maternal infection is acquired by eating undercooked meat. It is an obligate intracellular protozoan."
        },
        {
            "q": "The classic triad of congenital toxoplasmosis includes all of the following EXCEPT:",
            "options": ["Hydrocephalus", "Intracranial calcifications", "Chorioretinitis", "Microcephaly"],
            "correct": 3,
            "explain": "The classic triad of congenital toxoplasmosis is hydrocephalus, intracranial calcifications, and chorioretinitis. Microcephaly is more commonly associated with CMV and rubella."
        },
        {
            "q": "The drug of choice for toxoplasmosis during pregnancy is:",
            "options": ["Pyrimethamine alone", "Spiramycin", "Metronidazole", "Amoxicillin"],
            "correct": 1,
            "explain": "Spiramycin is the drug of choice during pregnancy for toxoplasmosis, which can reduce the risk of congenital transmission. Once fetal infection is confirmed, the regimen is typically switched to pyrimethamine + sulfadiazine + folinic acid after the 1st trimester."
        },
        {
            "q": "Congenital toxoplasmosis follows which pattern regarding transmission and severity?",
            "options": ["Transmission is highest in 1st trimester and most severe then too", "Transmission is lowest in 1st trimester but most severe when it occurs", "Transmission and severity are equal across all trimesters", "Transmission is highest in 3rd trimester and most severe then"],
            "correct": 1,
            "explain": "Toxoplasmosis has an inverse relationship: 1st-trimester transmission is rare (~15%) but severe (classic triad), while 3rd-trimester transmission is common (~65%) but subclinical at birth."
        }
    ],
    "s4": [  # Rubella
        {
            "q": "Congenital rubella syndrome (CRS) includes all of the following EXCEPT:",
            "options": ["Intrauterine growth restriction", "Cataracts", "Patent ductus arteriosus", "Hydrocephalus"],
            "correct": 3,
            "explain": "CRS includes IUGR, intracranial calcifications, microcephaly, cataracts, cardiac defects (most commonly PDA or pulmonary arterial hypoplasia), neurologic disease, osteitis, and hepatosplenomegaly. Hydrocephalus is more typical of toxoplasmosis."
        },
        {
            "q": "A pregnant woman with suspected rubella exposure has a confirmed positive IgM. What is the approximate risk of congenital rubella syndrome if infection occurred in the first trimester?",
            "options": ["25%", "50%", "85%", "100%"],
            "correct": 2,
            "explain": "First-trimester rubella infection has approximately an 85% risk of congenital rubella syndrome. The MMR vaccine (contraindicated in pregnancy) is the cornerstone of prevention."
        },
        {
            "q": "The MMR vaccine for rubella prevention is:",
            "options": ["Safe to give during pregnancy", "Contraindicated in pregnancy as it is a live attenuated vaccine", "Given only after delivery", "Not effective in preventing rubella"],
            "correct": 1,
            "explain": "MMR vaccine is a live attenuated vaccine and should not be given to pregnant women. It should be offered to all women of childbearing age before pregnancy."
        },
        {
            "q": "The incubation period for rubella is:",
            "options": ["1-2 days", "2-3 weeks", "4-6 weeks", "3 months"],
            "correct": 1,
            "explain": "Rubella has an incubation period of 2-3 weeks. Mode of infection is droplet infection. The classic rash is maculopapular and persists for 3 days."
        }
    ],
    "s5": [  # CMV
        {
            "q": "Cytomegalovirus (CMV) is characterized as:",
            "options": ["The rarest congenital viral infection", "The most common congenital viral infection", "Always symptomatic at birth", "Not transmissible via breast milk"],
            "correct": 1,
            "explain": "CMV is a double-stranded DNA herpes virus and is the most common congenital viral infection. It can be transmitted via saliva, urine, body fluids, transplacentally, and through breast milk."
        },
        {
            "q": "Congenital CMV is the leading non-genetic cause of:",
            "options": ["Visual impairment", "Sensorineural hearing loss in children", "Cardiac defects", "Facial clefts"],
            "correct": 1,
            "explain": "Congenital CMV is the leading non-genetic cause of sensorineural hearing loss in children. Even asymptomatic congenital CMV carries a 10-15% risk of late-onset hearing loss."
        },
        {
            "q": "Which of the following is NOT a consequence of transplacental CMV infection?",
            "options": ["Intrauterine growth restriction", "Sensorineural hearing loss", "Hydrocephalus", "Hydrops fetalis"],
            "correct": 3,
            "explain": "Transplacental CMV can cause IUGR, sensorineural hearing loss, intracranial calcifications, microcephaly, hydrocephalus, hepatosplenomegaly, delayed psychomotor development, and optic atrophy. Hydrops fetalis is more associated with α-thalassemia major."
        }
    ],
    "s6": [  # HSV
        {
            "q": "The risk of vertical transmission of HSV from mother to neonate during labor is:",
            "options": ["50% for primary HSV and 0-4% for recurrent HSV", "0-4% for primary and 50% for recurrent", "Equal for both primary and recurrent", "100% for both"],
            "correct": 0,
            "explain": "The risk is 50% for primary HSV infection in labor, and only 0-4% for recurrent disease. This dramatic difference reflects the absence of protective maternal IgG in primary infection."
        },
        {
            "q": "What is the recommended mode of delivery for pregnancies complicated by primary genital HSV in labor?",
            "options": ["Vaginal delivery", "Cesarean section", "Forceps delivery", "Vacuum extraction"],
            "correct": 1,
            "explain": "Cesarean section delivery is recommended for all pregnancies complicated by primary genital HSV in labor due to the 50% risk of vertical transmission."
        },
        {
            "q": "Which antiviral drug is considered safe for HSV in pregnancy?",
            "options": ["Ganciclovir", "Acyclovir", "Valganciclovir", "Foscarnet"],
            "correct": 1,
            "explain": "Acyclovir is safe in pregnancy (Category B) with extensive safety data. Suppressive acyclovir therapy from 36 weeks is used to reduce the risk of recurrence at delivery."
        }
    ]
}

# ========== PROCESS ALL 5 FILES ==========

files_to_process = [
    {
        "input": os.path.join(BASE, "Vomiting_anemia_heart_disease", "09_Vomiting_with_Pregnancy.html"),
        "output": os.path.join(ENH, "Vomiting_anemia_heart_disease", "09_Vomiting_with_Pregnancy.html"),
        "mcqs": mcqs_09,
        "name": "09_Vomiting_with_Pregnancy"
    },
    {
        "input": os.path.join(BASE, "Vomiting_anemia_heart_disease", "10_Anemia_with_Pregnancy.html"),
        "output": os.path.join(ENH, "Vomiting_anemia_heart_disease", "10_Anemia_with_Pregnancy.html"),
        "mcqs": mcqs_10,
        "name": "10_Anemia_with_Pregnancy"
    },
    {
        "input": os.path.join(BASE, "Vomiting_anemia_heart_disease", "11_Cardiac_Diseases_with_Pregnancy.html"),
        "output": os.path.join(ENH, "Vomiting_anemia_heart_disease", "11_Cardiac_Diseases_with_Pregnancy.html"),
        "mcqs": mcqs_11,
        "name": "11_Cardiac_Diseases_with_Pregnancy"
    },
    {
        "input": os.path.join(BASE, "Antepartum_hemorrhage", "08_Antepartum_Hemorrhage.html"),
        "output": os.path.join(ENH, "Antepartum_hemorrhage", "08_Antepartum_Hemorrhage.html"),
        "mcqs": mcqs_08,
        "name": "08_Antepartum_Hemorrhage"
    },
    {
        "input": os.path.join(BASE, "High_risk_pregnancy_identification", "17_Infectious_Diseases_with_Pregnancy.html"),
        "output": os.path.join(ENH, "High_risk_pregnancy_identification", "17_Infectious_Diseases_with_Pregnancy.html"),
        "mcqs": mcqs_17,
        "name": "17_Infectious_Diseases_with_Pregnancy"
    }
]

for f in files_to_process:
    print(f"\n{'='*60}")
    print(f"Processing: {f['name']}")
    print(f"  Input:  {f['input']}")
    print(f"  Output: {f['output']}")
    print(f"  MCQs: {sum(len(v) for v in f['mcqs'].values())} total questions in {len(f['mcqs'])} subtopics")
    try:
        process_file(f['input'], f['output'], f['mcqs'])
        print(f"  ✓ Success!")
    except Exception as e:
        print(f"  ✗ Error: {e}")

print(f"\n{'='*60}")
print("All 5 files processed!")
