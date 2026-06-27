#!/usr/bin/env python3
"""
Process 6 Week 3 Family Medicine files by injecting MCQs.
Uses inject_mcqs.py's process_file function.
"""
import sys, os, json

# Add current dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inject_mcqs import process_file

BASE = "extracted/assets/second task/obstetric/Week3"
ENH = "enhanced-assets/second task/obstetric/Week3"
WORK = "/media/mohamed/projects3/projects/obstaric/obs app"

def ensure_output(filepath):
    d = os.path.dirname(filepath)
    os.makedirs(d, exist_ok=True)

# ============================================================
# MCQ DATA FOR EACH FILE
# ============================================================

# --- FM01: Premarital Care ---
fm01_mcqs = {
    "s2": [  # Overview
        {
            "q": "What is the recommended minimum time before marriage to conduct premarital screening?",
            "options": ["One month", "Three months", "Six months", "One year"],
            "correct": 1,
            "explain": "Couples planning to marry are advised to conduct premarital screening at least three months before the marriage date."
        },
        {
            "q": "How long is the premarital compatibility certificate valid?",
            "options": ["Three months", "Four months", "Six months", "One year"],
            "correct": 2,
            "explain": "The premarital compatibility certificate is valid for only six months."
        },
        {
            "q": "Which of the following best defines premarital care?",
            "options": [
                "Care provided during marriage to treat hereditary diseases",
                "Specific service provided for couples before marriage to promote health of future parents and prevent health hazards",
                "Post-marital counselling for family planning",
                "A legal requirement only for consanguineous marriages"
            ],
            "correct": 1,
            "explain": "Premarital care is the specific service provided for the couples before marriage, aiming to promote health of future parents, prevent health hazards, and have healthy future generations."
        }
    ],
    "s3": [  # Components
        {
            "q": "Which of the following is NOT a component of premarital care?",
            "options": ["Premarital assessment and screening", "Premarital counselling", "Immunization (Rubella vaccination for females)", "Postpartum care planning"],
            "correct": 3,
            "explain": "The three main components of premarital care are: (1) Premarital Assessment, (2) Premarital Counselling, and (3) Immunization (Rubella vaccination for females)."
        },
        {
            "q": "Among offspring of consanguineous marriage, there is increased risk of all EXCEPT:",
            "options": ["Prenatal morbidity and mortality", "Congenital abnormalities", "Mental retardation", "Improved immune function"],
            "correct": 3,
            "explain": "Among offspring of consanguineous marriage, there is increased prenatal morbidity and mortality together with increased incidence of congenital abnormalities and mental retardation."
        }
    ],
    "s4": [  # Premarital Assessment
        {
            "q": "Which of the following is a routine obligatory investigation in premarital screening?",
            "options": ["Thyroid function tests", "HPLC (Hb variants)", "Mammography", "Random blood glucose"],
            "correct": 1,
            "explain": "Routine obligatory investigations include CBC, Blood group (ABO & Rh), HPLC (Hb variants), Sickledex, G6PD, Ferritin, HBsAg, and HCV."
        },
        {
            "q": "A 25-year-old man is undergoing premarital screening. Which genetic disorders should be specifically asked about in his family history?",
            "options": ["Cystic fibrosis, Huntington disease, Marfan syndrome", "SCD, Thalassemia, G6PD", "Hemophilia A and B", "Tay-Sachs disease and Niemann-Pick disease"],
            "correct": 1,
            "explain": "Family history should specifically ask about SCD, Thalassemia, G6PD, and congenital anomalies such as Marfan syndrome and deaf mutism."
        }
    ],
    "s5": [  # Algorithm
        {
            "q": "According to the premarital care algorithm, after reception and triage, what is the next step?",
            "options": ["Laboratory investigations", "Premarital Screening Clinic", "Immunization", "Referral to specialist"],
            "correct": 1,
            "explain": "After reception/registration and triage (vitals, anthropometric measurements), the client proceeds to the Premarital Screening Clinic."
        },
        {
            "q": "In the premarital care algorithm, what are the three main branches evaluated at the screening clinic?",
            "options": ["Counselling, immunization, and follow-up", "History, physical examination, and laboratory investigations", "Genetic testing, ultrasound, and blood work", "Social assessment, nutritional counselling, and exercise plan"],
            "correct": 1,
            "explain": "The premarital screening clinic evaluates three branches: History taking (personal data, consanguinity, genetic disorders), Physical examination (vitals, BMI, systemic exam), and Laboratory investigations (CBC, HPLC, Sickledex, etc.)."
        }
    ],
    "s6": [  # Premarital Counselling
        {
            "q": "Which type of premarital counselling involves studying the genogram of both parents to discover probability of genetic hazards?",
            "options": ["General counselling & health education", "Reproductive health counselling", "Relevant health problem counselling", "Genetic counselling"],
            "correct": 3,
            "explain": "Genetic counselling involves studying the genogram of both parents to discover probability of genetic hazards to offspring such as SCD, thalassemia, Marfan syndrome, and deaf mutism."
        },
        {
            "q": "Reproductive health counselling in premarital care includes advice about all EXCEPT:",
            "options": ["Appropriate time of first pregnancy", "Importance of early antenatal care", "Precautions during pregnancy to avoid teratogenic hazards", "Management of chronic diseases like diabetes"],
            "correct": 3,
            "explain": "Reproductive health counselling covers advice about appropriate time of first pregnancy, importance of early antenatal care, precautions during pregnancy (avoid drugs & teratogenic hazards), and safe delivery. Management of chronic diseases falls under relevant health problem counselling."
        }
    ],
    "s7": [  # Immunization
        {
            "q": "Which immunization is specifically recommended for females during premarital care?",
            "options": ["Hepatitis B vaccine", "Rubella vaccine", "Tetanus toxoid", "HPV vaccine"],
            "correct": 1,
            "explain": "Immunization of females against rubella is recommended, not less than 3 months before planning pregnancy to avoid congenital rubella syndrome."
        },
        {
            "q": "Why is rubella immunization recommended before pregnancy?",
            "options": ["To prevent neural tube defects", "To avoid congenital rubella syndrome if the female acquires infection during pregnancy", "To reduce the risk of miscarriage in the first trimester", "To prevent postpartum hemorrhage"],
            "correct": 1,
            "explain": "Rubella immunization is recommended to avoid congenital rubella syndrome if the female acquires the infection during pregnancy."
        }
    ],
    "s8": [  # Inter-conception Care
        {
            "q": "Which of the following is an objective of inter-conception care?",
            "options": ["Provide emergency obstetric care", "Decrease maternal and neonatal morbidity and mortality", "Manage acute postpartum hemorrhage", "Perform routine cesarean section"],
            "correct": 1,
            "explain": "Objectives of inter-conception care include: promoting health and nutritional status of mother, identifying risks for mother and future children, and decreasing maternal and neonatal morbidity and mortality."
        },
        {
            "q": "When can inter-conception care be provided?",
            "options": ["Only during the first trimester of pregnancy", "During postpartum care, when attending MCH for child care, and during home visits", "Only at the time of delivery", "Exclusively in the neonatal intensive care unit"],
            "correct": 1,
            "explain": "Inter-conception care can be provided during postpartum/post-abortive care, when attending the MCH for her child care, and during home visits."
        }
    ]
}

# --- FM02: Antenatal Care ---
fm02_mcqs = {
    "s2": [  # Definition/Goal
        {
            "q": "What is the ultimate goal of antenatal care?",
            "options": [
                "Ensure all pregnancies result in vaginal delivery",
                "Reduce maternal and perinatal mortality and morbidity rates",
                "Eliminate all pregnancy complications",
                "Guarantee a healthy newborn in every pregnancy"
            ],
            "correct": 1,
            "explain": "The ultimate goal of antenatal care is to reduce maternal and perinatal mortality and morbidity rates, prepare the woman for labor, lactation, and care of her infant, and detect and treat complicated conditions early."
        },
        {
            "q": "Which of the following is NOT a way the goal of ANC is achieved?",
            "options": [
                "Detection and management of complications",
                "Promotion of physical, mental, and social health of mother and baby",
                "Development of birth preparedness and complication readiness plan",
                "Scheduling routine cesarean delivery for all primigravida"
            ],
            "correct": 3,
            "explain": "The goal of ANC is achieved through detection and management of complications, promoting health, developing birth preparedness, and preparing the mother to breastfeed successfully. Routine C-section is not a goal of ANC."
        }
    ],
    "s3": [  # Components
        {
            "q": "How many main components of antenatal care are listed?",
            "options": ["5", "6", "7", "8"],
            "correct": 3,
            "explain": "The 8 components of ANC are: (1) Registration & history, (2) Periodic examination & lab, (3) High-risk pregnancy management, (4) Health education, (5) Nutritional care, (6) Emotional & social care, (7) Preventive measures (TT immunization), (8) Referral when needed."
        },
        {
            "q": "Which component of antenatal care includes tetanus toxoid immunization?",
            "options": ["Nutritional care", "Preventive measures", "Health education", "Referral when needed"],
            "correct": 1,
            "explain": "Preventive measures include tetanus toxoid immunization as a key component of antenatal care."
        }
    ],
    "s4": [  # Timing/Schedule
        {
            "q": "During which gestational age should a pregnant woman visit every 2 weeks?",
            "options": ["Till 28th week", "From 28th to 36th week", "From 36th week till labor", "First trimester only"],
            "correct": 1,
            "explain": "Standard visit frequency: Every 4 weeks till 28th week, every 2 weeks from 28th to 36th week, and every week from 36th week till labor."
        },
        {
            "q": "According to the minimum 8-visit schedule, when should GDM screening (50g GCT) be performed?",
            "options": ["First trimester", "20-26 weeks (Visit 2-3)", "30-34 weeks (Visit 4-5)", "36-38 weeks (Visit 6-7)"],
            "correct": 1,
            "explain": "GDM screening using 50g GCT is performed at 24-28 weeks, which falls in the 20-26 week visit window (Visit 2-3)."
        }
    ],
    "s5": [  # Barriers
        {
            "q": "Which of the following is listed as a barrier to effective antenatal care?",
            "options": ["Excessive number of healthcare providers", "Cultural norms requiring spouses' consent", "Too many ANC visits recommended", "Over-utilization of healthcare services"],
            "correct": 1,
            "explain": "Barriers include: poor access, poverty, cultural norms (women needing spouses' consent), poor quality perception, and inadequate facilities."
        },
        {
            "q": "How does poor quality perception act as a barrier to ANC?",
            "options": ["It makes pregnancy more complicated", "Prolonged waiting time and unprofessional conduct discourage women from seeking care", "It increases the cost of services", "It reduces the number of available medications"],
            "correct": 1,
            "explain": "Prolonged outpatient waiting time and unprofessional conduct of service providers create a perception of poor quality that discourages utilization."
        }
    ],
    "s6": [  # First Visit
        {
            "q": "How is the Expected Date of Delivery (EDD) calculated using Naegele's rule?",
            "options": ["Add 9 months and 7 days to LMP", "Subtract 3 months and add 7 days to the first day of LMP", "Add 280 days to the date of conception", "Subtract 1 month and add 14 days to LMP"],
            "correct": 1,
            "explain": "Naegele's rule: subtract 3 months, add 7 days to the first day of LMP."
        },
        {
            "q": "At what gestational age can fetal heart tones be auscultated using a Doppler?",
            "options": ["6-8 weeks", "10-12 weeks", "16-18 weeks", "20-22 weeks"],
            "correct": 1,
            "explain": "Fetal heart tones can be auscultated with Doppler at 10-12 weeks, and with Pinard's stethoscope after 20 weeks."
        }
    ],
    "s7": [  # Repeated Visits
        {
            "q": "What is the recommended total weight gain by the 20th week of pregnancy?",
            "options": ["~1.5 kg", "~3.5 kg", "~5 kg", "~7 kg"],
            "correct": 1,
            "explain": "At 20th week approximately 3.5 kg is gained, then about 0.5 kg/week. Total recommended: 11-16 kg."
        },
        {
            "q": "When should Leopold maneuvers to assess fetal presentation begin?",
            "options": ["20 weeks", "28 weeks", "32 weeks", "36 weeks"],
            "correct": 3,
            "explain": "Leopold maneuvers for abdominal palpation to assess fetal presentation begin at 36 weeks' gestation."
        },
        {
            "q": "Which screening test for trisomy and NTD is performed at 15-20 weeks?",
            "options": ["Glucose challenge test", "Triple or quadruple screen", "Nuchal translucency", "Amniocentesis"],
            "correct": 1,
            "explain": "Trisomy & NTD screening at 15-20 weeks uses triple screen (HCG, unconjugated estriol, α-fetoprotein) or quadruple screen (+ inhibin-A)."
        }
    ],
    "s8": [  # Weight Gain
        {
            "q": "What is the recommended total weight gain range for a pregnant woman with a healthy pre-pregnancy BMI (18.5-24.9)?",
            "options": ["7-11.5 kg", "11.5-16 kg", "12.5-18 kg", "5-9 kg"],
            "correct": 1,
            "explain": "For healthy weight (BMI 18.5-24.9), the recommended total weight gain is 11.5-16 kg."
        },
        {
            "q": "An obese pregnant woman (BMI ≥ 30) should gain how much weight during pregnancy?",
            "options": ["11.5-16 kg", "7-11.5 kg", "5-9 kg", "12.5-18 kg"],
            "correct": 2,
            "explain": "For obese women (BMI ≥ 30), the recommended total weight gain is 5-9 kg."
        }
    ],
    "s9": [  # High-Risk Detection
        {
            "q": "Which of the following is a risk factor detected from history that indicates high-risk pregnancy?",
            "options": ["Gestational diabetes detected at 28 weeks", "Mother's age <18 or >35 years", "Mild anemia at 32 weeks", "Occipitoposterior position at term"],
            "correct": 1,
            "explain": "Risk factors from history include: mother's age <18 or >35 years, primigravida or grand multipara, birth spacing <2 years, previous CS, chronic diseases, etc."
        },
        {
            "q": "Which of the following is a risk factor detected late in pregnancy?",
            "options": ["Severe anemia", "Chronic hypertension", "Severe PIH", "Diabetes mellitus"],
            "correct": 2,
            "explain": "Risk factors detected late in pregnancy include: severe PIH, antepartum hemorrhage, multiple pregnancy, IUGR, and abnormal presentation."
        }
    ],
    "s10": [  # Immunization
        {
            "q": "How many doses of tetanus toxoid are recommended for a pregnant woman in her first pregnancy?",
            "options": ["One dose", "Two doses with 4 weeks apart", "Three doses", "Single dose at delivery"],
            "correct": 1,
            "explain": "Two doses of TT with 4 weeks apart are recommended. For subsequent pregnancies, one dose is given."
        },
        {
            "q": "Which vaccine is strongly recommended during pregnancy according to the content?",
            "options": ["Rubella vaccine", "COVID-19 vaccines", "BCG vaccine", "Yellow fever vaccine"],
            "correct": 1,
            "explain": "COVID-19 vaccines are strongly recommended in pregnancy for best protection against known risks including ICU admission and premature birth."
        }
    ],
    "s11": [  # Health Ed
        {
            "q": "What is the best sleeping position recommended during pregnancy?",
            "options": ["Supine position", "Prone position", "Sims' position", "Trendelenburg position"],
            "correct": 2,
            "explain": "The best sleeping position during pregnancy is Sims' position."
        },
        {
            "q": "A pregnant woman should be advised to avoid all of the following EXCEPT:",
            "options": ["Hot baths", "Tight clothes and belts", "Regular walking exercise", "Prolonged standing"],
            "correct": 2,
            "explain": "Regular moderate exercise like walking (at least 30 min) is recommended. Hot baths, tight clothes, and prolonged standing should be avoided."
        },
        {
            "q": "Smoking during pregnancy increases the risk of all EXCEPT:",
            "options": ["Preterm birth", "Low birth weight", "Cleft lip/palate", "Post-term delivery"],
            "correct": 3,
            "explain": "Smoking increases risk of preterm birth, LBW, cleft lip/palate, and SIDS."
        }
    ],
    "s12": [  # Red Flags
        {
            "q": "Which of the following is a dangerous sign during pregnancy requiring immediate medical care?",
            "options": ["Mild nausea in first trimester", "Leakage of amniotic fluid", "Braxton Hicks contractions at 36 weeks", "Increased fetal movement in third trimester"],
            "correct": 1,
            "explain": "Danger signs include: vaginal bleeding, persistent abdominal pain, persistent headache, blurring of vision, leakage of amniotic fluid, fever, and stoppage of fetal movement for >4 hours."
        },
        {
            "q": "Stoppage of fetal movement for how many hours in late pregnancy is considered a red flag?",
            "options": ["2 hours", "4 hours", "6 hours", "8 hours"],
            "correct": 1,
            "explain": "Stoppage of fetal movement for >4 hours in late pregnancy is a red flag requiring immediate medical care."
        }
    ]
}

# --- FM03: Nutritional Care ---
fm03_mcqs = {
    "s2": [  # Introduction
        {
            "q": "Maternal underweight before pregnancy (BMI <19.8 kg/m²) increases the risk of:",
            "options": ["Macrosomia", "Low infant birth weight", "Post-term delivery", "Gestational diabetes"],
            "correct": 1,
            "explain": "Maternal underweight before pregnancy and low pregnancy weight gain increase risk of low infant birth weight."
        },
        {
            "q": "Which of the following is a pre-pregnancy preparation recommendation?",
            "options": ["Start iron supplementation immediately", "Achieve and maintain healthy body weight", "Schedule weekly prenatal visits", "Take high-dose vitamin A"],
            "correct": 1,
            "explain": "Pre-pregnancy preparation includes: achieving/maintaining healthy weight, balanced diet, physical activity, regular medical care, and managing chronic conditions."
        }
    ],
    "s3": [  # Components
        {
            "q": "Which of the following is NOT a component of nutritional care during pregnancy?",
            "options": ["Nutritional assessment", "Nutrition education", "Exercise prescription", "Correction of deficiencies (anemia, folate deficiency)"],
            "correct": 2,
            "explain": "The four components are: (1) Nutritional Assessment, (2) Nutrition Education, (3) Nutrition Supplementation (iron, folate, calcium), (4) Correction of Deficiencies."
        },
        {
            "q": "Which supplementation is included as part of routine nutritional care during pregnancy?",
            "options": ["Vitamin D", "Iron, folate, calcium", "Vitamin C", "Magnesium"],
            "correct": 1,
            "explain": "Nutrition supplementation includes iron, folate, and calcium as key components."
        }
    ],
    "s4": [  # Nutritional Assessment
        {
            "q": "What method is used for dietary history assessment in pregnancy?",
            "options": ["Food frequency questionnaire", "24-hour recall method", "3-day food diary", "Direct observation"],
            "correct": 1,
            "explain": "The 24-hour recall method is used for semi-quantitative/qualitative analysis to identify expected major deficiencies."
        },
        {
            "q": "According to Egyptian guidelines, anemia in pregnancy is defined as hemoglobin less than:",
            "options": ["12 g/dL", "11 g/dL", "10 g/dL", "9 g/dL"],
            "correct": 1,
            "explain": "By Egyptian guidelines, anemia in pregnancy is defined as Hb <11 g/dL in the first trimester."
        },
        {
            "q": "When should Vitamin D levels be measured in pregnancy?",
            "options": ["Routinely in all pregnant women", "Only in women with obesity, minimal sun exposure, malabsorption, or dark skin", "Only in the third trimester", "Routinely at every prenatal visit"],
            "correct": 1,
            "explain": "Routine broad-based screening for vitamin D is not necessary. Measure in: obesity, minimal sun exposure, malabsorption (celiac, IBD), vegan diet, dark skin."
        }
    ],
    "s5": [  # Weight Gain/Anemia
        {
            "q": "For a normal weight woman (BMI 18.5-24.9), what is the mean recommended rate of gestational weight gain per week?",
            "options": ["0.51 kg/wk", "0.42 kg/wk", "0.28 kg/wk", "0.22 kg/wk"],
            "correct": 1,
            "explain": "The mean rate for normal weight women (BMI 18.5-24.9) is 0.42 kg/week."
        },
        {
            "q": "Moderate anemia in pregnancy is defined as hemoglobin between:",
            "options": ["10-10.9 g/dL", "7-9.9 g/dL", "<7 g/dL", "11-12 g/dL"],
            "correct": 1,
            "explain": "Moderate anemia: Hb 7-9.9 g/dL. Mild: 10-10.9 g/dL. Severe: <7 g/dL."
        }
    ],
    "s6": [  # Nutrition Ed
        {
            "q": "Which of the following is a key component of healthy eating during pregnancy?",
            "options": ["Unlimited caffeine intake", "Limit added sugars, saturated fat, and sodium", "High-dose vitamin A supplementation", "Complete avoidance of all fats"],
            "correct": 1,
            "explain": "Key components include limiting added sugars, saturated fat, and sodium, appropriate supplementation, appropriate weight gain, avoiding alcohol, limiting caffeine to <200-300 mg/day, and safe food handling."
        },
        {
            "q": "What is the recommended caffeine limit during pregnancy?",
            "options": ["<100 mg/day", "<200-300 mg/day", "<400-500 mg/day", "Complete avoidance"],
            "correct": 1,
            "explain": "Caffeine should be limited to <200-300 mg/day during pregnancy."
        }
    ],
    "s7": [  # Food Pyramid
        {
            "q": "How many servings of vegetables per day are recommended in the Food Guide Pyramid during pregnancy?",
            "options": ["1-2 servings", "3-5 servings", "5-7 servings", "7-9 servings"],
            "correct": 1,
            "explain": "The Food Guide Pyramid recommends 3-5 servings of vegetables and 3-4 servings of fruit per day."
        },
        {
            "q": "How many servings per day from the milk group are recommended during pregnancy?",
            "options": ["2 servings", "3 servings", "4 servings", "5 servings"],
            "correct": 2,
            "explain": "The milk group (milk, yogurt, cheese) recommends 4 servings per day during pregnancy."
        }
    ],
    "s8": [  # Supplementation
        {
            "q": "What is the routine iron supplementation recommendation for pregnant women after 3 months?",
            "options": ["110 mg ferrous fumarate once daily", "220 mg ferrous fumarate/sulphate + folic acid once daily", "330 mg ferrous sulphate three times daily", "100 mg elemental iron weekly"],
            "correct": 1,
            "explain": "All pregnant mothers (after 3 months) should receive 220 mg ferrous fumarate/sulphate + folic acid once daily."
        },
        {
            "q": "What is the folic acid dose for women at high risk of NTD (previous NTD or NTD in either parent)?",
            "options": ["0.4 mg once daily", "2 mg once daily", "4 mg once daily prior to conception through first 12 weeks", "400 mg once daily"],
            "correct": 2,
            "explain": "High-risk women (previous NTD) should receive 4 mg folic acid once daily from at least 1 month prior to conception through first 12 weeks."
        },
        {
            "q": "Why should vitamin A supplementation be avoided during pregnancy?",
            "options": ["It causes maternal hypertension", "It may be teratogenic in doses above 700 micrograms", "It interferes with iron absorption", "It increases the risk of gestational diabetes"],
            "correct": 1,
            "explain": "Vitamin A intake above 700 micrograms might be teratogenic and should be avoided during pregnancy."
        }
    ],
    "s9": [  # Anemia Correction
        {
            "q": "What is the curative dose of ferrous fumarate for iron deficiency anemia in pregnancy?",
            "options": ["100 mg once daily", "200 mg 3 times daily", "300 mg once daily", "400 mg weekly"],
            "correct": 1,
            "explain": "Curative management of iron deficiency anemia: ferrous fumarate or sulphate 200 mg 3 times daily."
        },
        {
            "q": "Which of the following is an indication for IV iron administration in pregnancy?",
            "options": ["First trimester routine supplementation", "Hb above 11 g/dL", "Severe or symptomatic anemia, especially later in pregnancy", "Mild anemia discovered at booking"],
            "correct": 2,
            "explain": "IV iron is indicated: beyond 1st trimester and cannot tolerate oral iron, severe/symptomatic anemia (especially later in pregnancy), oral iron ineffective."
        },
        {
            "q": "Within what time frame should Hb increase by ≥1 g/dL after starting iron therapy?",
            "options": ["3-5 days", "2-3 weeks", "4-6 weeks", "8-10 weeks"],
            "correct": 1,
            "explain": "Hb should increase by ≥1 g/dL within 2-3 weeks of starting iron therapy."
        }
    ],
    "s10": [  # Folate Deficiency
        {
            "q": "Folate deficiency is the most common cause of which type of anemia during pregnancy?",
            "options": ["Iron deficiency anemia", "Megaloblastic anemia", "Hemolytic anemia", "Aplastic anemia"],
            "correct": 1,
            "explain": "Folate deficiency is the most common cause of megaloblastic anemia during pregnancy."
        },
        {
            "q": "Which birth defect is associated with folate deficiency in pregnancy?",
            "options": ["Congenital heart disease", "Neural tube defects", "Cleft lip and palate", "Limb reduction defects"],
            "correct": 1,
            "explain": "Folate deficiency is associated with neural tube defects including anencephaly and spina bifida."
        },
        {
            "q": "What is the recommended folic acid dose for most women planning pregnancy?",
            "options": ["0.1 mg once daily", "0.4 mg once daily beginning at least 1 month prior to conception through first trimester", "4 mg once daily", "10 mg once daily"],
            "correct": 1,
            "explain": "Most women should take 0.4 mg folic acid once daily beginning at least 1 month prior to conception through first trimester."
        }
    ]
}

# --- FM04: Postpartum Care ---
fm04_mcqs = {
    "s2": [  # Definition/Objectives
        {
            "q": "When does the postpartum period (puerperium) begin and how long does it last?",
            "options": ["Begins after delivery of placenta and continues for 4 weeks", "Begins about 2 hours after delivery of placenta and continues for 6 weeks", "Begins immediately after delivery and continues for 8 weeks", "Begins 24 hours after delivery and continues for 6 weeks"],
            "correct": 1,
            "explain": "The postpartum period starts about two hours after delivery of the placenta and continues for six weeks."
        },
        {
            "q": "Which of the following is an objective of postnatal care for the mother?",
            "options": ["Establishment of paternity", "Reproductive health promotion and prevention of complications", "Guarantee return to pre-pregnancy weight", "Ensure exclusive formula feeding"],
            "correct": 1,
            "explain": "Objectives for the mother include: reproductive health promotion, prevention of postpartum complications, early detection and referral, psychological support, and health education."
        }
    ],
    "s3": [  # History
        {
            "q": "On Day 1 postpartum, which item should be checked as given?",
            "options": ["Iron supplementation", "Vitamin A capsule (200,000 IU)", "Folic acid", "Calcium supplement"],
            "correct": 1,
            "explain": "On Day 1, the nurse should check that Vitamin A capsule (200,000 IU) has been given to the mother."
        },
        {
            "q": "On Day 4 postpartum, which symptom should be specifically asked about?",
            "options": ["Breast engorgement", "Calf pain (suggesting thrombosis)", "Umbilical stump condition", "Infant jaundice"],
            "correct": 1,
            "explain": "On Day 4, the nurse asks about calf pain (thrombotic), chest pain, foul-smelling discharge, and fever/chills."
        }
    ],
    "s4": [  # Physical Exam
        {
            "q": "What laboratory investigations are performed on Day 40 postpartum?",
            "options": ["Complete blood count and liver function tests", "Hemoglobin level and complete urine analysis", "Blood glucose and lipid profile", "Thyroid function tests and vitamin D level"],
            "correct": 1,
            "explain": "On Day 40, hemoglobin level and complete urine analysis are the recommended lab investigations."
        },
        {
            "q": "On Day 1 postpartum, what abdominal finding should be assessed?",
            "options": ["Abdominal musculature tone", "Fundal height and firmness by palpation", "C-section incision inspection", "Liver span"],
            "correct": 1,
            "explain": "On Day 1, fundal height and firmness by palpation and abdominal tenderness should be assessed to check uterine involution."
        }
    ],
    "s5": [  # Infant Assessment
        {
            "q": "What newborn screening should be performed within the first week of life?",
            "options": ["Hearing screening", "Congenital hypothyroidism screening", "Critical congenital heart disease screening", "Bilirubin level"],
            "correct": 1,
            "explain": "The mother should be counseled to have the infant screened for congenital hypothyroidism within the first week."
        },
        {
            "q": "By Day 7, what should have happened to the umbilical stump?",
            "options": ["It should be completely healed", "It should have fallen off or totally dried", "It should be covered with antibiotic ointment", "It needs surgical removal"],
            "correct": 1,
            "explain": "By Day 7, the umbilical stump should have fallen off or be totally dried."
        }
    ],
    "s6": [  # Danger Symptoms
        {
            "q": "Which of the following is a danger symptom in the mother requiring immediate medical care?",
            "options": ["Mild fatigue", "Painful calf muscle", "Slight breast tenderness", "Occasional headache"],
            "correct": 1,
            "explain": "Danger symptoms for the mother include: vaginal bleeding, severe headache, blurring of vision, convulsions, fever, foul discharge, painful calf muscle, chest pain, dyspnea, and fainting."
        },
        {
            "q": "Which of the following is a red flag in an infant requiring referral?",
            "options": ["Frequent breastfeeding", "Respiratory rate >60/min", "Mild jaundice resolving by Day 7", "Sleeping 16-18 hours per day"],
            "correct": 1,
            "explain": "Infant red flags include: temperature <36°C or >38°C, RR >60/min, flaccid/non-reactive, jaundice/cyanosis/pallor, nasal flaring, chest retraction, purulent umbilical discharge."
        }
    ],
    "s7": [  # Health Ed
        {
            "q": "When should contraception counseling be provided to postpartum mothers?",
            "options": ["Day 1 postpartum", "Day 7 postpartum", "Only on Day 40", "After 6 months"],
            "correct": 1,
            "explain": "Counseling about contraception should be done at Day 7 visit."
        },
        {
            "q": "Which of the following is a health education message for the mother?",
            "options": ["Avoid breastfeeding for the first week", "Encourage early ambulation", "Remain in bed for 40 days", "Restrict fluid intake"],
            "correct": 1,
            "explain": "Health education includes: encourage early ambulation, successful breastfeeding, good nutrition, abdominal exercises, contraception counseling, and day 40 visit."
        }
    ],
    "s8": [  # Timing
        {
            "q": "For home deliveries, on which days does the nurse visit?",
            "options": ["Days 1, 3, and 7", "Days 1, 4, and 7", "Days 2, 5, and 10", "Days 1, 7, and 14"],
            "correct": 1,
            "explain": "For home deliveries, nurse visits on Day 1 (within 24 hours), Day 4, and Day 7. Then mother visits center on Day 40."
        },
        {
            "q": "What is the purpose of the Day 40 visit?",
            "options": ["Routine weight check only", "Complete assessment and initiation of contraception", "Only infant vaccination", "Removal of sutures"],
            "correct": 1,
            "explain": "On Day 40, the mother visits the health facility for complete assessment and initiation of contraception."
        }
    ],
    "s9": [  # Flowchart
        {
            "q": "According to the postpartum care flowchart, what happens if a risk factor is detected?",
            "options": ["Continue routine care", "Refer to a higher level of health care facility", "Start iron supplementation", "Schedule a follow-up in 2 weeks"],
            "correct": 1,
            "explain": "If any risk factor (maternal or neonatal) is detected, the patient should be referred to a higher level of health care facility."
        },
        {
            "q": "What is the first step in the postpartum care protocol flowchart?",
            "options": ["Physical examination", "Postpartum care visits (home: Days 1, 4, 7; clinic: Day 40)", "Laboratory investigations", "Health education"],
            "correct": 1,
            "explain": "The first step is scheduling and conducting postpartum care visits: home visits on Days 1, 4, 7 and clinic visit on Day 40."
        }
    ]
}

# --- FM05: Postpartum Problems ---
fm05_mcqs = {
    "s1": [  # Physical Problems
        {
            "q": "Which of the following is a common postpartum physical problem?",
            "options": ["Hyperthyroidism", "Postpartum hemorrhage", "Polycystic ovary syndrome", "Gestational diabetes persistence"],
            "correct": 1,
            "explain": "Common postpartum physical problems include: postpartum hemorrhage, infections, breastfeeding issues, perineal pain, pelvic pain, urinary/bowel problems, fatigue and anemia, thyroid disorders, and contraception needs."
        },
        {
            "q": "Postpartum thyroiditis can lead to which condition?",
            "options": ["Permanent hypothyroidism requiring lifelong treatment", "Hyper- or hypothyroidism", "Only hyperthyroidism", "Only euthyroid state"],
            "correct": 1,
            "explain": "Postpartum thyroiditis can lead to hyper- or hypothyroidism."
        }
    ],
    "s2": [  # Emotional Issues
        {
            "q": "Which postpartum emotional condition requires urgent psychiatric care?",
            "options": ["Baby blues", "Postpartum depression", "Postpartum anxiety", "Postpartum psychosis"],
            "correct": 3,
            "explain": "Postpartum psychosis is rare but severe, presenting with hallucinations, delusions, and disorganized behavior — it requires urgent psychiatric care."
        },
        {
            "q": "What distinguishes postpartum depression (PPD) from baby blues?",
            "options": ["PPD occurs only in first-time mothers", "PPD is more severe and prolonged, affecting ability to care for self or baby", "Baby blues last longer than PPD", "PPD requires no treatment"],
            "correct": 1,
            "explain": "PPD is more severe and prolonged depressive symptoms affecting the mother's ability to care for herself or her baby, while baby blues are mild and transient."
        }
    ],
    "s3": [  # Psychosocial
        {
            "q": "Which of the following is a psychosocial concern during the postpartum period?",
            "options": ["Increased bone density", "Social isolation especially if support systems are limited", "Improved sleep patterns", "Enhanced immune function"],
            "correct": 1,
            "explain": "Psychosocial concerns include: adjustment to motherhood, relationship strain, social isolation, and work/financial stress."
        }
    ],
    "s4": [  # Breast Problems Overview
        {
            "q": "How many main postpartum breast problems are covered in the chapter?",
            "options": ["Two", "Three", "Four", "Five"],
            "correct": 1,
            "explain": "Three main postpartum breast problems are covered: breast engorgement, nipple fissure (cracked nipples), and insufficient milk supply."
        }
    ],
    "s5": [  # Breast Engorgement
        {
            "q": "Breast engorgement typically occurs when?",
            "options": ["Immediately after delivery", "3-5 days postpartum when milk 'comes in'", "2 weeks postpartum", "At 6 weeks postpartum"],
            "correct": 1,
            "explain": "Breast engorgement occurs when breasts become overly full, hard, and painful, usually 3-5 days postpartum when milk 'comes in'."
        },
        {
            "q": "Which of the following is a management strategy for breast engorgement?",
            "options": ["Decrease breastfeeding frequency", "Warm compresses before feeding, cold after", "Tight underwire bra for support", "Apply ice directly to nipples"],
            "correct": 1,
            "explain": "Management includes: frequent breastfeeding/pumping, hand expression to soften areola, warm compresses before feeding and cold after, supportive bra without underwire, and pain relief."
        }
    ],
    "s6": [  # Nipple Fissure
        {
            "q": "What is the most common cause of nipple fissure (cracked nipples)?",
            "options": ["Excessive milk production", "Improper latching and positioning", "Allergic reaction to breast milk", "Infant teeth eruption"],
            "correct": 1,
            "explain": "Nipple fissure is often due to improper latching, positioning, or excessive moisture."
        },
        {
            "q": "Which of the following is recommended for managing cracked nipples?",
            "options": ["Stop breastfeeding on the affected side", "Lanolin cream or breast milk on nipples", "Apply alcohol to dry the area", "Use tight bandages"],
            "correct": 1,
            "explain": "Management includes: correcting latch/positioning, lanolin cream or breast milk on nipples, air drying after feeds, and nipple shields in severe cases."
        }
    ],
    "s7": [  # Insufficient Milk
        {
            "q": "Which of the following is a cause of insufficient milk supply?",
            "options": ["Excessive breastfeeding", "Poor latch and infrequent feeds", "High maternal fluid intake", "Maternal obesity"],
            "correct": 1,
            "explain": "Causes include: poor latch, infrequent feeds, maternal stress, and dehydration."
        },
        {
            "q": "Which intervention helps stimulate milk production in cases of insufficient supply?",
            "options": ["Supplementing with formula", "Skin-to-skin contact", "Reducing fluid intake", "Pumping only once daily"],
            "correct": 1,
            "explain": "Management includes: frequent and effective breastfeeding, skin-to-skin contact to stimulate milk production, balanced diet, good hydration, and use of galactagogues."
        }
    ],
    "s8": [  # Prevention
        {
            "q": "Which of the following is a preventive measure for postpartum breast problems?",
            "options": ["Use of underwired bras for support", "Correct latching technique", "Limit breastfeeding to 5 minutes per session", "Apply baby powder to nipples"],
            "correct": 1,
            "explain": "Prevention includes: correct latching, frequent feeding, keeping nipples clean and dry, supportive bra without underwire, and balanced diet with hydration."
        }
    ],
    "s9": [  # Baby Blues
        {
            "q": "When do baby blues typically begin and how long can they last?",
            "options": ["Begin immediately after delivery, last up to 1 week", "Begin 2-3 days postpartum, last up to 2 weeks", "Begin 1 week postpartum, last up to 1 month", "Begin 2 weeks postpartum, last up to 6 weeks"],
            "correct": 1,
            "explain": "Baby blues typically begin 2-3 days postpartum and can last up to 2 weeks. They are mild and resolve on their own."
        },
        {
            "q": "What distinguishes baby blues from postpartum depression?",
            "options": ["Baby blues are more severe", "Baby blues require medication", "Baby blues are less severe and resolve on their own", "Baby blues only affect first-time mothers"],
            "correct": 2,
            "explain": "Baby blues are less severe than postpartum depression and resolve on their own. If symptoms last longer than 2 weeks or become more intense, it may indicate PPD."
        },
        {
            "q": "Which of the following is the primary cause of baby blues?",
            "options": ["Inadequate social support", "Hormonal changes (sudden drop in estrogen and progesterone after delivery)", "Lack of breastfeeding success", "Financial stress"],
            "correct": 1,
            "explain": "Causes of baby blues include: hormonal changes (sudden drop in estrogen & progesterone after delivery), physical stress of childbirth, emotional factors, and lack of sleep."
        }
    ]
}

# --- FM06: Contraceptive Methods ---
fm06_mcqs = {
    "s1": [  # Overview
        {
            "q": "According to the WHO definition, family planning is:",
            "options": [
                "The use of contraceptive methods to prevent all pregnancies",
                "The ability of individuals and couples to anticipate and attain their desired number of children and the spacing and timing of their births",
                "A government program to limit population growth",
                "Medical termination of unwanted pregnancies"
            ],
            "correct": 1,
            "explain": "WHO defines family planning as the ability of individuals and couples to anticipate and attain their desired number of children and the spacing and timing of their births."
        },
        {
            "q": "Which group represents the 'TOO Young' target for contraception?",
            "options": ["Under 16 years", "Under 20 years", "Under 18 years", "Under 25 years"],
            "correct": 1,
            "explain": "The Four 'TOO' are: TOO Young (<20 years), TOO Soon (spacing <2 years), TOO Many (5th+ pregnancy), TOO Old (>35 years)."
        }
    ],
    "s2": [  # Classification
        {
            "q": "Which of the following is a reversible contraceptive method?",
            "options": ["Tubal ligation", "Vasectomy", "Physiological methods (periodic abstinence, withdrawal, LAM)", "None of the above"],
            "correct": 2,
            "explain": "Reversible methods include: physiological, barrier, hormonal, and IUDs. Permanent methods (tubal ligation, vasectomy) are not reversible."
        },
        {
            "q": "Which contraceptive method provides STI protection?",
            "options": ["Combined oral contraceptives", "Male condoms", "IUD", "Progestin-only injectable"],
            "correct": 1,
            "explain": "Male condoms provide STI protection in addition to pregnancy prevention."
        }
    ],
    "s3": [  # Physiological
        {
            "q": "What are the three conditions that must ALL be met for Lactational Amenorrhea (LAM) to be effective?",
            "options": [
                "Baby is <6 months, mother exclusively pumps milk, mother uses backup contraception",
                "Mother's monthly bleeding has not returned, baby is fully/nearly fully breastfed often day and night, baby is <6 months old",
                "Baby is <3 months, mother has regular cycles, baby is formula-fed at night",
                "Mother has irregular periods, baby is <1 year, breastfeeding is supplemented with solids"
            ],
            "correct": 1,
            "explain": "All 3 conditions for LAM: (1) Mother's monthly bleeding has not returned, (2) Baby is fully or nearly fully breastfed, fed often day and night, (3) Baby is less than 6 months old."
        },
        {
            "q": "The Standard Days Method of periodic abstinence involves avoiding unprotected intercourse on which days?",
            "options": ["Days 1-7 of the menstrual cycle", "Days 8 through 19 of regular menstrual cycles", "Days 20-28 of the cycle", "Days 14-28 of the cycle"],
            "correct": 1,
            "explain": "The Standard Days Method: avoid unprotected intercourse on days 8 through 19 of regular menstrual cycles."
        }
    ],
    "s4": [  # Barrier
        {
            "q": "Which barrier method is placed in the vagina before intercourse and used with spermicides?",
            "options": ["Male condom", "Vaginal diaphragm and cervical cap", "Female condom", "Spermicide alone"],
            "correct": 1,
            "explain": "The vaginal diaphragm and cervical cap are shallow cups placed in vagina before intercourse, used with spermicides for increased efficacy."
        },
        {
            "q": "Which of the following is a non-contraceptive advantage of barrier methods?",
            "options": ["Regulates menstrual cycles", "Reduces risk of ovarian cancer", "Possible protection against some STIs and reduced cervical cancer risk", "Improves bone density"],
            "correct": 2,
            "explain": "Non-contraceptive advantages include: ease of use, non-prescription, low cost, possible STI protection (GC, Chlamydia, Trichomonas), and reduced cervical cancer risk."
        }
    ],
    "s5": [  # Hormonal MOA
        {
            "q": "What is the primary mechanism of action of combined hormonal contraceptives?",
            "options": ["Thickening cervical mucus", "Suppression of ovulation", "Endometrial changes preventing implantation", "Sperm immobilization"],
            "correct": 1,
            "explain": "The triple mechanism of hormonal methods: (1) Suppression of ovulation (primary for combined), (2) Thickened cervical mucus, (3) Endometrial changes."
        },
        {
            "q": "Which of the following is NOT a mechanism of action of hormonal contraceptives?",
            "options": ["Suppression of ovulation", "Thickened cervical mucus", "Endometrial changes", "Direct killing of sperm"],
            "correct": 3,
            "explain": "The three mechanisms are: ovulation suppression, thickened cervical mucus, and endometrial changes. Direct killing of sperm is not a mechanism."
        }
    ],
    "s6": [  # Combined E+P
        {
            "q": "Which combined hormonal method is administered every 4 weeks?",
            "options": ["Combined oral contraceptives", "Combined monthly injectable", "Combined patch", "Combined vaginal ring"],
            "correct": 1,
            "explain": "The combined monthly injectable is given every 4 weeks (±7 days) and does not require daily administration."
        },
        {
            "q": "What is the typical regimen for the combined vaginal ring?",
            "options": ["3 weeks in, 1 week off", "Inserted daily", "Changed monthly", "24 weeks continuous use"],
            "correct": 0,
            "explain": "The combined vaginal ring is used for 3 weeks in, 1 week off."
        }
    ],
    "s7": [  # COCs
        {
            "q": "When should a fully breastfeeding woman start COCs?",
            "options": ["Immediately after delivery", "4 weeks after giving birth", "6 months after giving birth", "At weaning"],
            "correct": 2,
            "explain": "For fully breastfeeding women, COCs should be started 6 months after giving birth."
        },
        {
            "q": "Which of the following is a contraindication to COCs?",
            "options": ["Age under 30", "History of migraine with aura or any migraine", "History of DVT, stroke, MI, or serious heart problems", "Nulliparity"],
            "correct": 2,
            "explain": "Contraindications include: breastfeeding baby <6 months, age ≥35 and smokes, HTN, diabetes >20 years, history of DVT/stroke/MI, breast cancer, migraine, liver disease, etc."
        },
        {
            "q": "What should a woman do if she misses 3 or more pills in week 3 of her COC pack?",
            "options": ["Take the missed pill and continue as usual", "Stop the pack and take a 7-day break", "Take the most recent pill, finish the pack, start new pack immediately without 7-day break, use backup for 7 days", "Take two pills daily for the rest of the pack"],
            "correct": 2,
            "explain": "If ≥3 pills missed in Week 3: take most recent pill ASAP, finish all pills, start new pack immediately without 7-day break, use backup for 7 days."
        }
    ],
    "s8": [  # Progestin-only
        {
            "q": "How often is DMPA progestin-only injectable given?",
            "options": ["Monthly", "Every 2 months (±2 weeks)", "Every 3 months (±2 weeks)", "Every 6 months"],
            "correct": 2,
            "explain": "DMPA is given every 3 months (±2 weeks). NET-EN is given every 2 months (±2 weeks)."
        },
        {
            "q": "What is the primary mechanism of action of progestin-only pills (minipills)?",
            "options": ["Suppression of ovulation in 100% of women", "Thickening cervical mucus", "Inducing endometrial atrophy", "Blocking sperm production"],
            "correct": 1,
            "explain": "The primary mechanism of minipills is thickening cervical mucus. Secondary: prevents ovulation in ~50% of women."
        },
        {
            "q": "How long can contraceptive implants provide protection?",
            "options": ["1-2 years", "3-5 years depending on type", "7-10 years", "Lifelong"],
            "correct": 1,
            "explain": "Implants provide long-term protection for 3-5 years depending on type and are immediately reversible upon removal."
        }
    ],
    "s9": [  # IUDs
        {
            "q": "How long is the TCu-380A copper IUD effective?",
            "options": ["5 years", "10 years", "15 years", "Lifelong"],
            "correct": 1,
            "explain": "The TCu-380A copper IUD is effective for 10 years."
        },
        {
            "q": "Which IUD type provides non-contraceptive advantages including reduction of heavy menstrual bleeding and dysmenorrhea?",
            "options": ["Copper IUD (Cu-IUD)", "Levonorgestrel IUD (LNG-IUD)", "Both equally", "Neither"],
            "correct": 1,
            "explain": "The LNG-IUD reduces dysmenorrhea, heavy menstrual bleeding, and endometriosis symptoms. The Cu-IUD may cause menorrhagia."
        },
        {
            "q": "When is the postpartum period during which IUD insertion is contraindicated?",
            "options": ["First 48 hours postpartum", "Between 48 hours and 4 weeks postpartum", "From 4-6 weeks postpartum", "From 6-8 weeks postpartum"],
            "correct": 1,
            "explain": "IUD insertion is contraindicated between 48 hours and 4 weeks postpartum."
        }
    ],
    "s10": [  # Emergency Contraception
        {
            "q": "Up to how many days after unprotected intercourse can emergency contraception be used?",
            "options": ["24 hours for all methods", "Progestin-only pills up to 3 days (72 hrs); Combined pills and Cu-IUD up to 5 days", "Up to 7 days for all methods", "Up to 14 days for Cu-IUD"],
            "correct": 1,
            "explain": "Progestin-only pills: up to 3 days (72 hrs). Combined oral pills and Copper IUD: up to 5 days (120 hrs)."
        },
        {
            "q": "Which emergency contraception method has the longest window and is most effective?",
            "options": ["Progestin-only pills", "Combined oral pills", "Copper IUD", "All have the same window"],
            "correct": 2,
            "explain": "The Copper IUD can be inserted up to 5 days (120 hrs) after unprotected sex and is the most effective emergency contraception."
        }
    ],
    "s11": [  # Permanent
        {
            "q": "What is the male sterilization procedure?",
            "options": ["Orchidectomy", "Vasectomy — the vas deferens is cut or blocked", "Circumcision", "Prostatectomy"],
            "correct": 1,
            "explain": "Vasectomy is the cutting or blocking of the vas deferens to prevent sperm from entering the semen."
        },
        {
            "q": "Which statement about permanent contraceptive methods is TRUE?",
            "options": ["They are easily reversible", "Reversal is usually not possible", "They provide protection for 10 years", "They also protect against STIs"],
            "correct": 1,
            "explain": "Permanent methods are intended to provide lifelong, permanent protection. Reversal is usually not possible."
        }
    ],
    "s12": [  # WHO MEC
        {
            "q": "What does WHO MEC Category 2 indicate?",
            "options": ["No restrictions for use", "Generally use; some follow-up may be needed", "Usually not recommended; requires clinical judgment", "Method should not be used"],
            "correct": 1,
            "explain": "WHO MEC categories: 1 = No restrictions, 2 = Generally use (some follow-up), 3 = Usually not recommended (clinical judgment needed), 4 = Should not be used."
        },
        {
            "q": "What does WHO MEC Category 4 indicate?",
            "options": ["No restrictions for use", "Generally use; some follow-up may be needed", "Usually not recommended; requires clinical judgment", "Method should not be used"],
            "correct": 3,
            "explain": "Category 4 means the method should not be used due to unacceptable health risk."
        }
    ]
}

# ============================================================
# PROCESS ALL FILES
# ============================================================

files = [
    {
        "name": "Family_medicine/FM01_Premarital_Care.html",
        "mcq_data": fm01_mcqs
    },
    {
        "name": "Family_medicine/FM02_Antenatal_Care.html",
        "mcq_data": fm02_mcqs
    },
    {
        "name": "Family_medicine/FM03_Nutritional_Care.html",
        "mcq_data": fm03_mcqs
    },
    {
        "name": "Family_medicine/FM04_Postpartum_Care.html",
        "mcq_data": fm04_mcqs
    },
    {
        "name": "Family_medicine/FM05_Postpartum_Problems.html",
        "mcq_data": fm05_mcqs
    },
    {
        "name": "Family_medicine/FM06_Contraceptive_Methods.html",
        "mcq_data": fm06_mcqs
    }
]

total_mcqs = 0
total_sections = 0

for f in files:
    input_path = os.path.join(WORK, BASE, f["name"])
    output_path = os.path.join(WORK, ENH, f["name"])
    ensure_output(output_path)
    
    mcq_data = f["mcq_data"]
    # Count MCQs
    sec_count = len(mcq_data)
    mcq_count = sum(len(v) for v in mcq_data.values())
    total_sections += sec_count
    total_mcqs += mcq_count
    
    print(f"\n{'='*60}")
    print(f"Processing: {f['name']}")
    print(f"Sections with MCQs: {sec_count}, Total MCQs: {mcq_count}")
    
    process_file(input_path, output_path, mcq_data)

print(f"\n{'='*60}")
print(f"DONE! Total files: {len(files)}")
print(f"Total sections injected: {total_sections}")
print(f"Total MCQs injected: {total_mcqs}")
print(f"Output in: {ENH}")
