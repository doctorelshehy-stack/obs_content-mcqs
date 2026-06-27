#!/usr/bin/env python3
"""Inject MCQs into all 6 Week 3 obstetrics files."""

import sys, os, json
sys.path.insert(0, '/media/mohamed/projects3/projects/obstaric/obs app')

from inject_mcqs import process_file

BASE = "extracted/assets/second task/obstetric/Week3"
ENH  = "enhanced-assets/second task/obstetric/Week3"

# ─────────────────────────────────────────────────────────────
# 1) 20_Female_Pelvis.html
# ─────────────────────────────────────────────────────────────
mcq_data_20 = {
    "s2": [
        {"q": "Which of the following is NOT a compartment of the true pelvis?",
         "options": ["Pelvic inlet", "Pelvic cavity", "Pelvic outlet", "Pelvic diaphragm"],
         "correct": 3, "explain": "The true pelvis is divided into three compartments: pelvic inlet (brim), pelvic cavity, and pelvic outlet. The pelvic diaphragm is a muscular structure forming the pelvic floor, not a compartment."},
        {"q": "The pelvic inlet is also known as the:",
         "options": ["Pelvic diaphragm", "Pelvic brim", "Obstetric outlet", "Perineal body"],
         "correct": 1, "explain": "The pelvic inlet is also called the pelvic brim and represents the superior opening into the true pelvis."}
    ],
    "s4": [
        {"q": "Which anteroposterior diameter of the pelvic inlet is the shortest?",
         "options": ["True conjugate (11 cm)", "Obstetric conjugate (10.5 cm)", "Diagonal conjugate (12.5 cm)", "Anatomical transverse (13 cm)"],
         "correct": 1, "explain": "The obstetric conjugate is 10.5 cm — the shortest anteroposterior diameter of the inlet, measured from the sacral promontory to the most bulging point on the back of the symphysis pubis."},
        {"q": "Which conjugate can be measured clinically on vaginal examination?",
         "options": ["True conjugate", "Obstetric conjugate", "Diagonal conjugate", "Anatomical conjugate"],
         "correct": 2, "explain": "The diagonal conjugate (12.5 cm) is the only one that can be directly measured clinically. The true conjugate is inferred as diagonal minus 1.5 cm."},
        {"q": "The diagonal conjugate measures:",
         "options": ["10.5 cm", "11 cm", "12 cm", "12.5 cm"],
         "correct": 3, "explain": "The diagonal conjugate measures 12.5 cm, from the tip of the sacral promontory to the lower border of the symphysis pubis."}
    ],
    "s5": [
        {"q": "What is the largest diameter in the pelvis?",
         "options": ["Obstetric conjugate (10.5 cm)", "Anatomical transverse diameter (13 cm)", "Interspinous diameter (10.5 cm)", "Bituberous diameter (11 cm)"],
         "correct": 1, "explain": "The anatomical transverse diameter (13 cm) is the largest diameter in the pelvis, measured between the farthest two points on the iliopectineal lines."},
        {"q": "The obstetric transverse diameter of the inlet measures:",
         "options": ["11 cm", "12 cm", "13 cm", "10.5 cm"],
         "correct": 1, "explain": "The obstetric transverse diameter of the inlet measures 12 cm. It is slightly shorter than the anatomical transverse diameter (13 cm) and bisects the true conjugate."}
    ],
    "s6": [
        {"q": "Each oblique diameter of the pelvic inlet measures:",
         "options": ["9.5 cm", "11 cm", "12 cm", "13 cm"],
         "correct": 2, "explain": "Both right and left oblique diameters measure 12 cm. The right oblique runs from the right sacroiliac joint to the left iliopectineal eminence, and the left oblique runs opposite."},
        {"q": "The sacro-cotyloid diameters measure:",
         "options": ["9.5 cm", "10.5 cm", "12 cm", "13 cm"],
         "correct": 0, "explain": "The sacro-cotyloid diameters measure 9.5 cm, from the promontory of the sacrum to the right or left iliopectineal eminence."}
    ],
    "s7": [
        {"q": "The pelvic cavity is best described as:",
         "options": ["A flat plane between inlet and outlet", "The space between symphysis pubis and sacrum", "The area below the pelvic outlet", "The space between the ischial spines"],
         "correct": 1, "explain": "The pelvic cavity is the space between the symphysis pubis and the sacrum, with the roof being the plane of the pelvic brim and the floor being the plane of least pelvic dimension."}
    ],
    "s8": [
        {"q": "The anatomical outlet of the pelvis is described as:",
         "options": ["Circular", "Oval", "Lozenge-shaped", "Heart-shaped"],
         "correct": 2, "explain": "The anatomical outlet is lozenge-shaped, bounded by the lower border of the symphysis pubis, pubic arch, ischial tuberosities, sacrotuberous and sacrospinous ligaments, and the tip of the coccyx."}
    ],
    "s9": [
        {"q": "During the second stage of labor, what happens to the coccyx to increase the obstetric AP diameter of the outlet?",
         "options": ["It fractures", "It moves backwards", "It moves forwards", "It remains fixed"],
         "correct": 1, "explain": "The coccyx moves backwards during the second stage of labor, increasing the obstetric anteroposterior diameter of the outlet from 11 cm (anatomical) to 13 cm (obstetric)."},
        {"q": "The interspinous diameter (between ischial spines) measures:",
         "options": ["9.5 cm", "10.5 cm", "11 cm", "12 cm"],
         "correct": 1, "explain": "The interspinous diameter measures 10.5 cm and is widely cited as the smallest pelvic dimension, the plane at which the fetal head most commonly arrests in the second stage."}
    ],
    "s10": [
        {"q": "The obstetric axis (Curve of Carus) is described as:",
         "options": ["Straight line", "S-shaped", "J-shaped", "C-shaped"],
         "correct": 2, "explain": "The Curve of Carus is J-shaped: it passes downwards and backwards along the axis of the inlet to the ischial spines, then downwards and forwards along the axis of the pelvic outlet."}
    ],
    "s11": [
        {"q": "Which Caldwell-Moloy pelvic type is most common and optimally suited for vaginal delivery?",
         "options": ["Android (20%)", "Anthropoid (25%)", "Gynecoid (50%)", "Platypelloid (5%)"],
         "correct": 2, "explain": "The Gynecoid pelvis occurs in 50% of women and is the classic female pelvis optimally suited for vaginal delivery. Mnemonic: GAAAP (Gynecoid 50, Android 20, Anthropoid 25, Platypelloid 5)."},
        {"q": "Which pelvic type has an anteroposterior diameter greater than the transverse (ape-like inlet)?",
         "options": ["Gynecoid", "Android", "Anthropoid", "Platypelloid"],
         "correct": 2, "explain": "Anthropoid pelvis (25%) has an AP diameter greater than the transverse — an ape-like inlet shape."},
        {"q": "Platypelloid pelvis is characterized by:",
         "options": ["Round inlet", "Transverse diameter greater than AP (flat pelvis)", "Heart-shaped inlet", "AP diameter greater than transverse"],
         "correct": 1, "explain": "Platypelloid pelvis (5%) is a flat pelvis where the transverse diameter is greater than the anteroposterior diameter."}
    ],
    "s12": [
        {"q": "What is the minimum diagonal conjugate measurement suggesting an adequate pelvis?",
         "options": ["10.5 cm", "11 cm", "11.5 cm", "12.5 cm"],
         "correct": 2, "explain": "A diagonal conjugate ≥ 11.5 cm is the practical clinical cut-off suggesting the true conjugate is adequate for vaginal delivery."},
        {"q": "An adequate subpubic angle for vaginal delivery should be:",
         "options": ["Less than 60°", "About 75°", "≥ 90° (wide)", "Exactly 45°"],
         "correct": 2, "explain": "A wide subpubic angle ≥ 90° allows the pubic arch to admit two fingers and the fetal head to emerge."}
    ]
}

# ─────────────────────────────────────────────────────────────
# 2) 21_Fetal_Skull.html
# ─────────────────────────────────────────────────────────────
mcq_data_21 = {
    "s2": [
        {"q": "Which part of the fetal skull is compressible during labour, allowing moulding?",
         "options": ["Base", "Face", "Vault", "Foramen magnum"],
         "correct": 2, "explain": "The vault is compressible during labour — its five flat bones are joined by fibrous sutures that allow sliding. The base is rigid and non-compressible because bones are fused."},
        {"q": "The base of the fetal skull extends from:",
         "options": ["Chin to foramen magnum", "Chin to root of nose", "Root of nose to occiput", "Foramen magnum to vertex"],
         "correct": 0, "explain": "The base extends from the chin to the foramen magnum and is a rigid, non-compressible ring."}
    ],
    "s3": [
        {"q": "How many bones form the vault of the fetal skull?",
         "options": ["3", "4", "5", "6"],
         "correct": 2, "explain": "The vault is built from 5 flat bones: 2 frontal bones, 2 parietal bones, and 1 occipital bone."},
        {"q": "Which suture separates the two frontal bones?",
         "options": ["Sagittal suture", "Coronal suture", "Frontal suture", "Lambdoid suture"],
         "correct": 2, "explain": "The frontal suture separates the two frontal bones. The sagittal suture separates the two parietal bones."},
        {"q": "The lambdoid suture separates:",
         "options": ["Frontal from parietal bones", "The two parietal bones", "Parietal from temporal bones", "Occipital from parietal bones"],
         "correct": 3, "explain": "The lambdoid suture separates the occipital bone from the parietal bones."}
    ],
    "s4": [
        {"q": "The vertex of the fetal skull is bounded anteriorly by:",
         "options": ["Posterior fontanelle and lambdoid suture", "Anterior fontanelle and coronal suture", "Nose and supra-orbital ridges", "Parietal eminences"],
         "correct": 1, "explain": "The vertex is bounded anteriorly by the anterior fontanelle and coronal suture, posteriorly by the posterior fontanelle and lambdoid suture, and laterally by lines through the parietal eminences."},
        {"q": "The brow presentation has which engagement diameter?",
         "options": ["Suboccipito-bregmatic (9.5 cm)", "Submento-bregmatic (9.5 cm)", "Mento-vertical (13.5 cm)", "Occipito-frontal (11.5 cm)"],
         "correct": 2, "explain": "In brow presentation, the presenting diameter is the mento-vertical (13.5 cm), which exceeds the largest pelvic inlet diameter, so the head cannot enter the pelvis."}
    ],
    "s5": [
        {"q": "How many fontanelles are there in the fetal skull, and how many are obstetrically important?",
         "options": ["4 fontanelles, 2 important", "6 fontanelles, 2 important", "6 fontanelles, 4 important", "4 fontanelles, 4 important"],
         "correct": 1, "explain": "There are 6 fontanelles in the fetal skull. Only 2 are obstetrically important: the anterior and posterior fontanelles. The other 4 lie at the ends of the temporal sutures."},
        {"q": "The anterior and posterior fontanelles help diagnose all EXCEPT:",
         "options": ["Vertex presentation", "Position of the occiput", "Sex of the fetus", "Degree of flexion of the head"],
         "correct": 2, "explain": "The fontanelles help diagnose vertex presentation, the position of the occiput (by distinguishing diamond vs triangular shape), and the degree of flexion. They do not determine fetal sex."}
    ],
    "s6": [
        {"q": "The anterior fontanelle (bregma) is surrounded by how many bones?",
         "options": ["2 bones", "3 bones", "4 bones", "5 bones"],
         "correct": 2, "explain": "The anterior fontanelle is surrounded by 4 bones: 2 frontal and 2 parietal. It is large, lozenge-shaped, and closes about 1.5 years after birth."},
        {"q": "Which fontanelle has a bony floor at term?",
         "options": ["Anterior fontanelle", "Posterior fontanelle", "Both are membranous", "Neither — both are bony"],
         "correct": 1, "explain": "The posterior fontanelle has a bony floor and its surrounding bones overlap during moulding. The anterior fontanelle has a membranous floor."},
        {"q": "The posterior fontanelle closes:",
         "options": ["1.5 years after birth", "At full term", "6 months after birth", "At 2 years of age"],
         "correct": 1, "explain": "The posterior fontanelle closes (is completely ossified) at full term. Memory aid: Posterior = Pre-birth/at term."}
    ],
    "s8": [
        {"q": "Which diameter is the engagement diameter in occipito-anterior position with complete flexion?",
         "options": ["Suboccipito-frontal (10 cm)", "Suboccipito-bregmatic (9.5 cm)", "Occipito-frontal (11.5 cm)", "Mento-vertical (13.5 cm)"],
         "correct": 1, "explain": "The suboccipito-bregmatic diameter (9.5 cm) is the engagement diameter in occipito-anterior position with complete flexion — it is the smallest diameter presenting."},
        {"q": "The occipito-frontal diameter (11.5 cm) is the engagement diameter in:",
         "options": ["OA with complete flexion", "OA with incomplete flexion", "Occipito-posterior position", "Face presentation"],
         "correct": 2, "explain": "The occipito-frontal diameter (11.5 cm) is the engagement diameter in occipito-posterior position and also distends the vulva in face-to-pubis delivery."},
        {"q": "Why is brow presentation dangerous?",
         "options": ["The mento-vertical diameter (13.5 cm) exceeds the pelvic inlet diameters", "The head cannot flex", "The face presents first", "It causes cord prolapse"],
         "correct": 0, "explain": "The mento-vertical diameter (13.5 cm) is longer than the largest pelvic inlet diameter (anatomical transverse = 13 cm), so the head cannot enter the pelvis in brow presentation."}
    ],
    "s9": [
        {"q": "Which is the most important transverse diameter of the fetal skull?",
         "options": ["Bitemporal (8 cm)", "Biparietal (9.5 cm)", "Bimastoid (7.5 cm)", "Subparietal supraparietal (9 cm)"],
         "correct": 1, "explain": "The biparietal diameter (9.5 cm) is the most important transverse diameter — it is the standard sonographic measurement for estimating fetal head size and confirming engagement."},
        {"q": "The subparietal supraparietal diameter (9 cm) is the engagement diameter in:",
         "options": ["Vertex presentation", "Face presentation", "Asynclitism", "Brow presentation"],
         "correct": 2, "explain": "The subparietal supraparietal diameter is the engagement diameter in asynclitism, where the head is tilted laterally in the pelvis."}
    ]
}

# ─────────────────────────────────────────────────────────────
# 3) 19_Normal_Labor.html
# ─────────────────────────────────────────────────────────────
mcq_data_19 = {
    "s2": [
        {"q": "Which of the following is a cause of onset of normal labor?",
         "options": ["Decreased estrogen, increased progesterone", "Increased estrogen, decreased progesterone", "Decreased prostaglandin F2α", "Decreased oxytocin"],
         "correct": 1, "explain": "Onset of labor is associated with ↑ Estrogen, ↓ Progesterone, ↑ Prostaglandin F2α and ↑ Oxytocin, leading to uterine contractions. Mechanical factors (uterine distension) also contribute."}
    ],
    "s3": [
        {"q": "Prelabor (premonitory stage) begins how long before true labor in primigravida?",
         "options": ["A few days", "1 week", "2-3 weeks", "4-5 weeks"],
         "correct": 2, "explain": "Prelabor begins 2-3 weeks before true labor in primigravida and a few days before in multipara. It is associated with increased oxytocin receptors."},
        {"q": "Which of the following is NOT a change seen during prelabor?",
         "options": ["Lightening", "Cervical ripening", "Formation of bag of water", "False labor pains"],
         "correct": 2, "explain": "Changes during prelabor include lightening, cervical ripening, and false labor pains. The bag of water forms during true labor, not prelabor."}
    ],
    "s4": [
        {"q": "Which feature distinguishes true labor pains from false labor pains?",
         "options": ["Pain location is only lower abdomen", "Relief with enema/sedation", "Progressive cervical dilatation and effacement", "Irregular contractions"],
         "correct": 2, "explain": "True labor pains produce cervical changes (dilatation and effacement), while false labor pains do not. True contractions are regular and progressive, and show (blood-stained mucus) is present."}
    ],
    "s5": [
        {"q": "The first stage of labor ends with:",
         "options": ["Expulsion of the fetus", "Full dilatation of cervix (10 cm)", "Expulsion of placenta", "First hour after delivery"],
         "correct": 1, "explain": "The first stage starts with onset of true labor pain and ends with full dilatation of cervix (10 cm). Duration is 12 hours in primi and 6 hours in multipara."},
        {"q": "The third stage of labor normally lasts about:",
         "options": ["5 minutes", "15 minutes", "30 minutes", "1 hour"],
         "correct": 1, "explain": "The third stage (from fetal expulsion to placental expulsion) lasts about 15 minutes in both primi and multipara with expectant management, reduced to 5 minutes with active management."}
    ],
    "s6": [
        {"q": "The pacemaker of uterine contractions is situated at:",
         "options": ["The cervix", "The lower uterine segment", "The cornu (right predominates over left)", "The fundus only"],
         "correct": 2, "explain": "The pacemaker of uterine contractions is at the cornu, with the right pacemaker predominating over the left. Contractions spread at 2 cm/sec, depolarizing the whole organ within 15 seconds."},
        {"q": "A Montevideo unit measures uterine contractions as:",
         "options": ["Duration × frequency", "Intensity × number of contractions in 3 minutes", "Amplitude × duration", "Basal tone × frequency"],
         "correct": 1, "explain": "Montevideo unit (MV unit) = Intensity of uterine contraction × number of contractions in 3 minutes. It quantifies uterine activity."}
    ],
    "s7": [
        {"q": "In a normal labor, cephalic presentation occurs in what percentage of cases?",
         "options": ["99%", "95%", "90%", "85%"],
         "correct": 1, "explain": "Cephalic presentation occurs in 95% of labors, breech in 3.5%, and shoulder in 0.5%."},
        {"q": "The normal cervical dilatation rate in active phase for nulliparous women is:",
         "options": ["0.5 cm/hr", "1.2 cm/hr", "1.5 cm/hr", "2.0 cm/hr"],
         "correct": 1, "explain": "In the active phase, normal cervical dilatation rate is 1.2 cm/hr for primigravida and 1.5 cm/hr for multiparous women."},
        {"q": "The latent stage of first stage is mainly concerned with:",
         "options": ["Cervical dilatation", "Cervical effacement", "Descent of head", "Expulsion of fetus"],
         "correct": 1, "explain": "The latent stage is mainly concerned with cervical effacement, while the active stage is mainly concerned with cervical dilatation."}
    ],
    "s8": [
        {"q": "A prolonged latent phase is defined as greater than how many hours in nulliparous women?",
         "options": ["12 hours", "14 hours", "20 hours", "24 hours"],
         "correct": 2, "explain": "Prolonged latent phase is >20 hours in primigravida and >14 hours in multipara. Management includes a therapeutic test with morphine or oxytocin stimulation."},
        {"q": "Arrest of dilatation is defined as cessation of dilatation for:",
         "options": ["1 or more hours", "2 or more hours", "3 or more hours", "4 or more hours"],
         "correct": 1, "explain": "Arrest of dilatation is cessation of dilatation for 2 or more hours. Arrest of descent is cessation of descent for 1 or more hours."}
    ],
    "s9": [
        {"q": "Which of the following is NOT one of the cardinal movements of the mechanism of labor?",
         "options": ["Engagement", "Internal rotation", "External rotation", "Cervical dilatation"],
         "correct": 3, "explain": "The cardinal movements are: descent, engagement, increased flexion, internal rotation, extension, restitution, and external rotation. Cervical dilatation is not a fetal movement — it occurs due to uterine contractions."},
        {"q": "Engagement of the vertex is diagnosed vaginally when:",
         "options": ["The head is at +1 station", "The vertex is felt at or below the ischial spine (zero station)", "The cervix is fully dilated", "The membranes are ruptured"],
         "correct": 1, "explain": "Engagement is diagnosed vaginally when the vertex is at or below the ischial spine (zero station). Abdominally, 2/5 or less of the head is felt above the symphysis pubis."}
    ],
    "s10": [
        {"q": "The active management of the third stage reduces its duration to:",
         "options": ["15 minutes", "10 minutes", "5 minutes", "2 minutes"],
         "correct": 2, "explain": "Active management reduces the third stage duration from 15 minutes (expectant) to 5 minutes, lowering the risk of PPH and maternal mortality."},
        {"q": "Which of the following is a sign of placental separation?",
         "options": ["Fundus becomes low and soft", "Umbilical cord shortens", "Uterus becomes globular, hard, and mobile with a sudden gush of blood", "Cervix closes completely"],
         "correct": 2, "explain": "Signs include: uterus becomes globular/hard/mobile, sudden gush of blood, suprapubic bulge, rise of fundal level, lengthening of cord, and absence of cord pulsation."}
    ],
    "s11": [
        {"q": "Which of the following is NOT part of the active management of the first stage?",
         "options": ["Partogram recording", "Amniotomy", "Oxytocin augmentation", "Fundal pressure during contractions"],
         "correct": 3, "explain": "Active first-stage procedures include evacuation of rectum/bladder, analgesia, partogram, amniotomy, oxytocin augmentation, and fetal monitoring. Fundal pressure is not recommended."}
    ],
    "s12": [
        {"q": "Cord clamping is contraindicated in which of the following?",
         "options": ["Term baby", "Preterm baby and Rh-negative mothers", "Vertex presentation", "Multiparous women"],
         "correct": 1, "explain": "Cord clamping is contraindicated in preterm babies and Rh-negative mothers. The newborn care also includes airway clearance, APGAR scoring, examination, and eye care with antibiotics."}
    ]
}

# ─────────────────────────────────────────────────────────────
# 4) 33_Abnormal_Uterine_Action.html
# ─────────────────────────────────────────────────────────────
mcq_data_33 = {
    "s2": [
        {"q": "The 3 'P's of dystocia (difficult labor) are:",
         "options": ["Power, Presentation, Pelvis", "Power, Passages, Passenger", "Pain, Position, Presentation", "Pressure, Pattern, Placenta"],
         "correct": 1, "explain": "The 3 Ps are Power (uterine contractions), Passages (maternal pelvis + soft tissues), and Passenger (fetus). Abnormal uterine action falls under 'Power'."}
    ],
    "s3": [
        {"q": "A normal adequate uterine contraction has the following characteristics:",
         "options": ["Frequency 1 in 5 min, Duration 30 sec, Amplitude 40 mmHg", "Frequency 1 in 3 min, Duration 45 sec, Amplitude 60 mmHg", "Frequency 2 in 10 min, Duration 60 sec, Amplitude 80 mmHg", "Frequency 1 in 2 min, Duration 20 sec, Amplitude 30 mmHg"],
         "correct": 1, "explain": "The '3·45·60' rule: Frequency 1 in 3 min, Duration 45 sec, Amplitude 60 mmHg, with basal tone 5-20 mmHg."},
        {"q": "The normal basal tone of uterine muscle at relaxation during labor is:",
         "options": ["0-5 mmHg", "5-20 mmHg", "20-30 mmHg", "30-40 mmHg"],
         "correct": 1, "explain": "Normal basal tone at relaxation is in the range of 5-20 mmHg. Elevated basal tone >20 mmHg is defined as hypertonic uterine contraction."}
    ],
    "s4": [
        {"q": "Which method is the gold standard for measuring true intrauterine pressure in mmHg?",
         "options": ["External tocodynamometry", "Internal tocodynamometry (IUPC)", "Manual palpation", "Ultrasound"],
         "correct": 1, "explain": "Internal tocodynamometry using an intrauterine pressure catheter (IUPC) is the gold standard, giving true pressure in mmHg. External toco gives frequency and rough duration but unreliable absolute pressure."}
    ],
    "s6": [
        {"q": "Uterine tachysystole is defined as:",
         "options": ["A single contraction sustained >3 minutes", "Elevated basal tone >20 mmHg", "4 or more contractions in 10 minutes", "Contractions every 5 minutes"],
         "correct": 2, "explain": "Uterine tachysystole is defined as 4 or more contractions in 10 minutes (ACOG: >5 in 10 min averaged over 30 min). Hyperstimulation = tachysystole + oxytocin + FHR abnormality."},
        {"q": "A tetanic uterine contraction is defined as:",
         "options": ["More than 5 contractions in 10 min", "A single contraction sustained for >3 minutes", "Basal tone >20 mmHg", "Contractions lasting >60 seconds"],
         "correct": 1, "explain": "A tetanic uterine contraction is a single contraction sustained for more than 3 minutes."}
    ],
    "s7": [
        {"q": "The first step in managing uterine overactivity is:",
         "options": ["Administer tocolytic", "Discontinue oxytocin", "Positioning the patient into lateral position", "Consider immediate delivery"],
         "correct": 2, "explain": "The 5-step sequence: 1) Lateral positioning, 2) Oxygenation, 3) Discontinue oxytocin, 4) Administer tocolytic, 5) Consider immediate delivery if persistently ominous FHR tracing."}
    ],
    "s8": [
        {"q": "In coordinate (normal polarity) abnormal uterine action, the fundal dominance is:",
         "options": ["Lost", "Preserved", "Reversed", "Absent"],
         "correct": 1, "explain": "In coordinate abnormal uterine action, the fundal dominance is preserved — the contraction wave still starts at the fundus. Examples: precipitate labor, Bandl's ring, hypotonic inertia."},
        {"q": "Which of the following is an incoordinate (abnormal polarity) uterine action?",
         "options": ["Precipitate labor", "Hypotonic inertia", "Constriction ring", "Bandl's ring"],
         "correct": 2, "explain": "Constriction ring is an incoordinate uterine action where fundal dominance is lost. Others (precipitate labor, Bandl's, hypotonic inertia) are coordinate types."}
    ],
    "s9": [
        {"q": "Precipitate labor is defined as labor lasting less than:",
         "options": ["1 hour", "2 hours", "3 hours", "4 hours"],
         "correct": 2, "explain": "Precipitate labor lasts less than 3 hours. It is more common in multiparas with strong contractions, small baby, and roomy pelvis."},
        {"q": "Which is a fetal complication of precipitate labor?",
         "options": ["Postpartum hemorrhage", "Uterine inversion", "Intracranial hemorrhage due to sudden compression/decompression of head", "Cervical lacerations"],
         "correct": 2, "explain": "Fetal complications include intracranial hemorrhage (from sudden compression/decompression), fetal asphyxia, cord avulsion, and fetal injury. Maternal complications include lacerations, abruption, shock, inversion, PPH, and sepsis."}
    ],
    "s10": [
        {"q": "Bandl's (pathological retraction) ring is a sign of:",
         "options": ["Normal labor progression", "Impending uterine rupture", "Constriction ring", "Cervical dystocia"],
         "correct": 1, "explain": "Bandl's ring is a sign of obstructed labor with impending uterine rupture. The upper segment retracts and thickens while the lower segment is markedly stretched and thinned."},
        {"q": "Pathological retraction ring can be detected by:",
         "options": ["Only vaginally", "Only on ultrasound", "Visible abdominally and palpable as a transverse groove", "Only on CTG"],
         "correct": 2, "explain": "Bandl's ring is visible abdominally and palpable as a transverse groove rising between symphysis and umbilicus — in contrast to constriction ring which is felt only vaginally."}
    ],
    "s12": [
        {"q": "Hypotonic uterine inertia is characterized by:",
         "options": ["Frequent strong contractions", "Infrequent weak uterine contractions", "Irregular painful contractions with no relaxation", "Reversed polarity"],
         "correct": 1, "explain": "Hypotonic inertia features infrequent weak uterine contractions with slow cervical dilatation. Management includes amniotomy and oxytocin augmentation after excluding CPD."},
        {"q": "Which is a contraindication to oxytocin augmentation?",
         "options": ["Cervical dilatation >3 cm", "Cephalopelvic disproportion", "Ruptured membranes", "Engaged presenting part"],
         "correct": 1, "explain": "Contraindications to oxytocin include cephalopelvic disproportion, malpresentation, scarred uterus, and grand multipara."}
    ],
    "s13": [
        {"q": "A key difference between pathological retraction ring and constriction ring is:",
         "options": ["Constriction ring is felt only vaginally; Bandl's ring is seen and felt abdominally", "Constriction ring rises upward; Bandl's ring is fixed", "Bandl's ring is localized; constriction ring is global", "Both are managed the same way"],
         "correct": 0, "explain": "Bandl's ring is palpable abdominally as a rising transverse groove. Constriction ring is felt only vaginally and does not change position. This is the key bedside discriminator."}
    ],
    "s14": [
        {"q": "Hypertonic inertia represents:",
         "options": ["Strong fundal dominance", "Reversed polarity where fundal dominance is lacking", "Infrequent weak contractions", "Normal uterine activity"],
         "correct": 1, "explain": "Hypertonic inertia represents reversed polarity where fundal dominance is lacking. Types include spastic lower uterine segment and colicky uterus."},
        {"q": "Cervical dystocia is defined as:",
         "options": ["Prolonged latent phase", "Failure of cervix to dilate despite good regular contractions", "Full dilatation with no descent", "Cervical tear during delivery"],
         "correct": 1, "explain": "Cervical dystocia is failure of the cervix to dilate within a reasonable time in the presence of good regular uterine contractions. Cesarean section is mostly required."}
    ]
}

# ─────────────────────────────────────────────────────────────
# 5) 47_Operative_Obstetrics.html
# ─────────────────────────────────────────────────────────────
mcq_data_47 = {
    "s2": [
        {"q": "Cesarean section is defined as:",
         "options": ["Delivery of fetus through vaginal route with instruments", "Delivery of a viable fetus through an abdominal and uterine incision", "Removal of the uterus through an abdominal incision", "Incision of the perineum to facilitate delivery"],
         "correct": 1, "explain": "CS is delivery of a viable fetus through an abdominal and uterine incision. It is the most common major operation performed globally."},
        {"q": "The incidence of cesarean section in Egypt approaches approximately:",
         "options": ["30%", "50%", "70%", "90%"],
         "correct": 2, "explain": "Egypt has a CS rate approaching 70%, more than double the global average of about 30%."}
    ],
    "s3": [
        {"q": "Which of the following is an absolute indication for cesarean section?",
         "options": ["Previous CS", "Breech presentation", "Major degree of placenta previa", "Prolonged labor"],
         "correct": 2, "explain": "Absolute indications: extreme pelvic contraction, soft tissue obstruction, gross fetal anomalies, and major degree of placenta previa."},
        {"q": "The four major indications for CS accounting for >70% of operations include all EXCEPT:",
         "options": ["Previous C-section", "Dystocia", "Malpresentation", "Maternal request"],
         "correct": 3, "explain": "The four major indications are: 1) Previous C-section, 2) Dystocia, 3) Malpresentation, 4) Suspected acute fetal compromise."},
        {"q": "A contraindication to cesarean section is:",
         "options": ["Placenta previa", "Cephalopelvic disproportion", "Dead fetus", "Cord prolapse"],
         "correct": 2, "explain": "Contraindications to CS include dead fetus and gross anomalies of the fetus (though these may be relative depending on context)."}
    ],
    "s4": [
        {"q": "The most commonly used skin incision for lower segment CS is:",
         "options": ["Midline subumbilical", "Paramedian", "Pfannenstiel incision", "Joel Cohen incision"],
         "correct": 2, "explain": "Pfannenstiel incision (transverse suprapubic) is the most commonly used skin incision for lower segment CS. The uterine incision is closed in 2 layers."},
        {"q": "During lower segment CS, if the head is impacted in the pelvis, which forceps may be used for extraction?",
         "options": ["Kielland's forceps", "Piper forceps", "Wrigley's forceps", "Simpson forceps"],
         "correct": 2, "explain": "If the head is impacted in the pelvis, it may be extracted by Wrigley's forceps through the uterine incision, or an assistant pushes the head upward by a hand in the vagina."}
    ],
    "s5": [
        {"q": "Upper segment (classical) CS is indicated in which situation?",
         "options": ["Routine repeat CS", "Placenta previa and accreta", "Normal singleton vertex presentation", "Premature labor"],
         "correct": 1, "explain": "Indications for upper segment CS include placenta previa and accreta, extensive adhesions, large lower-segment fibroid, repaired fistulas, neglected shoulder presentation, planned hysterectomy, rapid delivery, and contraction ring."},
        {"q": "The uterine incision in upper segment CS is closed in how many layers?",
         "options": ["1 layer", "2 layers", "3 layers", "4 layers"],
         "correct": 2, "explain": "The uterine incision in upper segment CS is closed in 3 layers: deep muscle, main bulk of muscle, and superficial muscle + peritoneum. Lower segment CS is closed in 2 layers."}
    ],
    "s7": [
        {"q": "Which of the following is a complication of cesarean section?",
         "options": ["Postpartum hemorrhage due to uterine artery injury", "Increased fetal lung maturity", "Reduced risk of placenta previa", "Improved fertility"],
         "correct": 0, "explain": "Complications include hemorrhage (mainly from uterine artery injury), bladder injury, anesthesia complications, shock, infection, paralytic ileus, thrombosis, adhesions, and scar rupture in subsequent pregnancies."},
        {"q": "Vaginal birth after CS (VBAC) is allowed ONLY for women who have had:",
         "options": ["Upper segment CS", "Lower segment CS", "Classical CS", "Any previous CS"],
         "correct": 1, "explain": "VBAC is only allowed for lower segment CS. No vaginal delivery trial is allowed for upper segment CS due to higher risk of uterine rupture (4% or more)."}
    ],
    "s8": [
        {"q": "Cesarean hysterectomy is indicated for all EXCEPT:",
         "options": ["Uncontrolled PPH", "Placenta accreta", "Desire for future pregnancy", "Operable carcinoma of cervix"],
         "correct": 2, "explain": "Indications include uncontrolled PPH, concealed accidental hemorrhage, operable cervical carcinoma, placenta accreta, multiple fibroids in older patients. Postmortem CS is emergency CS within 10 minutes of maternal death."}
    ],
    "s9": [
        {"q": "During D&C, the cervix is gradually dilated up to which Hegar size?",
         "options": ["Hegar 6", "Hegar 8", "Hegar 10 or more", "Hegar 12"],
         "correct": 2, "explain": "During D&C, gradual dilatation of the cervix up to Hegar's 10 or more is performed before introducing the ovum forceps."}
    ],
    "s10": [
        {"q": "Kielland's forceps are specifically used for:",
         "options": ["After-coming head in breech", "Deep transverse arrest of the fetal head", "Routine outlet forceps", "Preterm delivery"],
         "correct": 1, "explain": "Kielland's forceps have a minimal pelvic curve and sliding pivot, used for rotation in deep transverse arrest. Piper forceps are for after-coming head in breech."},
        {"q": "Which condition must be fulfilled before forceps application?",
         "options": ["Partially dilated cervix", "Intact membranes", "Fully dilated cervix and engaged head", "Empty pelvis"],
         "correct": 2, "explain": "Conditions include: anesthesia, adequate pelvic outlet, asepsis, empty bladder/bowel, uterine contractions, fully dilated cervix, engaged head in favorable position, and ruptured membranes."}
    ],
    "s11": [
        {"q": "Which is a contraindication to vacuum extraction?",
         "options": ["Prolonged second stage", "Fetal distress", "Non-vertex presentation", "Maternal exhaustion"],
         "correct": 2, "explain": "Contraindications include severe CPD, non-vertex presentation, premature fetus, and intact membranes. Fetal complications include cephalohematoma, scalp laceration, and rarely intracranial hemorrhage."}
    ],
    "s12": [
        {"q": "The mediolateral episiotomy:",
         "options": ["Is easier to repair than median", "Has less risk of extension to anal sphincter", "Is performed in midline", "Requires less skill to repair"],
         "correct": 1, "explain": "Mediolateral episiotomy requires more skill for repair but carries a lower risk of unintended extension to the anal sphincter compared to median episiotomy."}
    ],
    "s13": [
        {"q": "External cephalic version is performed:",
         "options": ["During labor under general anesthesia", "Antenatally after 36 weeks", "Only for transverse lie", "In the first stage of labor"],
         "correct": 1, "explain": "External cephalic version is done antenatally after 36 weeks without anesthesia to turn a fetus from breech or transverse position to cephalic presentation."},
        {"q": "The only remaining indication for internal podalic version nowadays is:",
         "options": ["Breech presentation at term", "Transverse lie of a second co-twin after delivery of the first twin", "Cord prolapse", "Face presentation"],
         "correct": 1, "explain": "Currently, the only indication for internal podalic version is transverse lie of a second co-twin after delivery of the first twin."}
    ]
}

# ─────────────────────────────────────────────────────────────
# 6) 48_Instruments.html
# ─────────────────────────────────────────────────────────────
mcq_data_48 = {
    "s1": [
        {"q": "The uterine sound has which of the following characteristics?",
         "options": ["Rigid, sharp-tipped, straight", "Malleable, blunt-tipped, graduated and curved", "Flexible, rounded, ungraduated", "Metal, sharp-tipped, graduated"],
         "correct": 1, "explain": "The uterine sound is malleable, has a blunt tip (3-4 mm diameter), is graduated, and curved. It is used to measure cervical and uterine length."},
        {"q": "Which is a complication of using a uterine sound?",
         "options": ["Infection only", "Shock and perforation", "Hemorrhage", "Nerve injury"],
         "correct": 1, "explain": "Complications of uterine sound include shock and perforation of the uterus."}
    ],
    "s2": [
        {"q": "The female uterine catheter is used for:",
         "options": ["Measuring uterine length", "Emptying the bladder during gynecologic operations", "Dilating the cervix", "Evacuating products of conception"],
         "correct": 1, "explain": "The female uterine catheter (available in rubber, metal, or plastic) is used for emptying the bladder during gynecologic operations."}
    ],
    "s3": [
        {"q": "Which of the following is a type of cervical dilator?",
         "options": ["Sims", "Cusco", "Hegar", "Wrigley"],
         "correct": 2, "explain": "Cervical dilators include Hegar (graduated dilators) and Fenton (alternative design). They are used for dilatation of the cervix to facilitate intrauterine surgery."},
        {"q": "Complications of cervical dilators include all EXCEPT:",
         "options": ["Neurogenic shock", "Infection", "Perforation", "Uterine prolapse"],
         "correct": 3, "explain": "Complications include neurogenic shock, infection, perforation, and cervical lacerations. Uterine prolapse is not a complication of cervical dilatation."}
    ],
    "s4": [
        {"q": "The uterine curette is indicated for all EXCEPT:",
         "options": ["Evacuation in incomplete/missed abortion", "Abnormal uterine bleeding", "Delivery of a viable fetus", "Removal of decidua"],
         "correct": 2, "explain": "The uterine curette (blunt or sharp) is used for evacuation of the uterus in incomplete/missed abortion and abnormal uterine bleeding, not for delivery of a viable fetus."}
    ],
    "s5": [
        {"q": "Which forceps is used to hold the edges of the uterine incision during cesarean section?",
         "options": ["Ring forceps", "Ovum forceps", "Green Armytage forceps", "Vulsellum"],
         "correct": 2, "explain": "Green Armytage forceps hold the edges of the uterine incision in cesarean section. Ring forceps have a lock and grasp the cervix during cerclage/curettage."},
        {"q": "What distinguishes ovum forceps from ring forceps?",
         "options": ["Ovum forceps has a lock; ring forceps does not", "Ring forceps has a lock; ovum forceps does not", "Ovum forceps is used for CS", "Ring forceps is longer"],
         "correct": 1, "explain": "Ring forceps has a lock while ovum forceps has no lock. Both are used to remove products of conception."},
        {"q": "Vulsellum forceps are characterized by:",
         "options": ["Smooth grasping surface", "Single or multiple teeth for grasping cervix", "A lock and a long shank", "Used mainly for suturing"],
         "correct": 1, "explain": "Vulsellum has single-toothed or multi-toothed tips for holding the cervix in different operations."}
    ],
    "s6": [
        {"q": "Sims vaginal speculum is used for:",
         "options": ["Cervical visualization and Pap smear", "IUD removal", "Vaginal operations and diagnosis of VVF", "Cervical punch biopsy"],
         "correct": 2, "explain": "Sims speculum is used for vaginal operations and diagnosis of vesicovaginal fistula (VVF). Cusco (bivalve) speculum is used for cervical visualization, IUD removal, Pap smear, and punch biopsy."},
        {"q": "Cusco speculum is used for all of the following EXCEPT:",
         "options": ["IUD removal", "Pap smear", "Cervical punch biopsy", "Vaginal operations for VVF diagnosis"],
         "correct": 3, "explain": "Cusco (bivalve) speculum is used for cervical visualization in vaginal procedures, IUD removal, Pap smear, and cervical punch biopsy. Sims speculum is used for vaginal operations and VVF diagnosis."}
    ],
    "s7": [
        {"q": "The uterine holding clamp is used for:",
         "options": ["Removing products of conception", "Holding the uterus in hysterectomy or myomectomy", "Dilating the cervix", "Emptying the bladder"],
         "correct": 1, "explain": "The uterine holding clamp is used for holding the uterus in cases of hysterectomy or myomectomy."}
    ]
}

# ─────────────────────────────────────────────────────────────
# Process all files
# ─────────────────────────────────────────────────────────────

files = [
    ("Female_pelvis_fetus_fetal_skull/20_Female_Pelvis.html", mcq_data_20),
    ("Female_pelvis_fetus_fetal_skull/21_Fetal_Skull.html", mcq_data_21),
    ("Physiology_and_management_of_normal_labour/19_Normal_Labor.html", mcq_data_19),
    ("Stages_of_labour_partogram_FHR/33_Abnormal_Uterine_Action.html", mcq_data_33),
    ("Operative_obstetrics/47_Operative_Obstetrics.html", mcq_data_47),
    ("Operative_obstetrics/48_Instruments.html", mcq_data_48),
]

for rel_path, mcq_data in files:
    input_path  = os.path.join(BASE, rel_path)
    output_path = os.path.join(ENH, rel_path)
    
    # Create output directory if needed
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"Processing: {rel_path}")
    print(f"Output: {output_path}")
    print(f"{'='*60}")
    
    process_file(input_path, output_path, mcq_data)

print(f"\n{'='*60}")
print("All 6 Week 3 files processed successfully!")
print(f"{'='*60}")
